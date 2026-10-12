#!/usr/bin/env python3
"""Single standard entry point for Alberta Trade Q1 and Q2.

Run `python run.py --help`. Existing src modules remain the authoritative logic.
No stage certifies a Q2 total unless the legal coverage is complete.
"""
from __future__ import annotations
import argparse
import importlib
import json
import subprocess
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent

STAGES = {
    'q1': ('src.complete_analysis', 'main'),
    'q1-sources': ('src.new_data_audit', 'audit_and_extract'),
    'q1-temporal': ('src.temporal_validation', 'run'),
    'q2': ('src.q2.analysis', 'main'),
    'q2-legal': ('src.q2.legal_reconcile', 'reconcile'),
}


OPTIONAL_INPUTS = {
    'q1-sources': ['data/raw/BACI_HS22_V202601.zip', 'data/raw/data_complete.zip'],
    'q1-temporal': ['data/source/baci_seven_economies_2022_2024_hs4.csv'],
}


def missing_inputs(stage: str):
    return [path for path in OPTIONAL_INPUTS.get(stage, []) if not (ROOT / path).is_file()]


def execute(stage: str):
    module, name = STAGES[stage]
    fn = getattr(importlib.import_module(module), name)
    result = fn()
    if result is not None:
        print(f'[{stage}] result: {str(result)[:1200]}', flush=True)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description='Unified, auditable Q1/Q2 pipeline')
    parser.add_argument('--question', choices=['all','q1','q2'], default='all', help='Default: both questions')
    parser.add_argument('--new-sources', action='store_true', help='Also audit expanded Q1 sources and run temporal validation')
    parser.add_argument('--legal-audit', action='store_true', help='Also run partial Q2 legal reconciliation')
    parser.add_argument('--tests', action='store_true', help='Run pytest after analysis')
    parser.add_argument('--continue-on-error', action='store_true', help='Continue other stages on error; exit remains nonzero')
    parser.add_argument('--strict-inputs', action='store_true', help='Fail instead of skipping optional stages with missing source files')
    parser.add_argument('--dry-run', action='store_true', help='Show planned stages without modifying outputs')
    args = parser.parse_args(argv)
    stages=[]
    if args.question in ('all','q1'):
        stages.append('q1')
        if args.new_sources: stages.extend(['q1-sources','q1-temporal'])
    if args.question in ('all','q2'):
        stages.append('q2')
        if args.legal_audit: stages.append('q2-legal')
    if args.dry_run:
        print('Planned stages:', ' -> '.join(stages) or '(none)')
        if args.tests: print('Then: pytest -q tests')
        return 0
    status=[]
    skipped=set()
    for stage in stages:
        missing=missing_inputs(stage)
        if stage == 'q1-temporal' and 'q1-sources' in skipped:
            missing = missing or ['data/source/baci_seven_economies_2022_2024_hs4.csv (depends on skipped q1-sources)']
        if missing:
            print(f'\n=== SKIP {stage}: missing optional source data ===', flush=True)
            for path in missing: print(f'  Missing: {path}', flush=True)
            print('  Restore original input archives to these paths and rerun to enable this stage.', flush=True)
            status.append({'stage':stage,'status':'failed' if args.strict_inputs else 'skipped_missing_inputs','missing':missing})
            skipped.add(stage)
            if args.strict_inputs and not args.continue_on_error: break
            continue
        print(f'\n=== START {stage} ===', flush=True)
        try:
            execute(stage)
            status.append({'stage':stage,'status':'ok'})
            print(f'=== FINISH {stage}: OK ===', flush=True)
        except Exception as exc:
            status.append({'stage':stage,'status':'failed','error':f'{type(exc).__name__}: {exc}'})
            traceback.print_exc()
            if not args.continue_on_error: break
    if args.tests and (args.continue_on_error or all(x['status'] in ('ok','skipped_missing_inputs') for x in status)):
        cp=subprocess.run([sys.executable,'-m','pytest','-q','tests'],cwd=ROOT,check=False)
        status.append({'stage':'tests','status':'ok' if cp.returncode==0 else 'failed','returncode':cp.returncode})
    log=ROOT/'reports'/'pipeline_last_run.json'
    log.parent.mkdir(parents=True,exist_ok=True)
    log.write_text(json.dumps({'run_utc':datetime.now(timezone.utc).isoformat(), 'arguments':vars(args), 'stages':status,
       'interpretation':'Q2 partial legal screening is NOT certified total tariff exposure; Q1 scenario is NOT a validated forecast.'},indent=2)+'\n')
    print(f'\nRun manifest: {log.relative_to(ROOT)}')
    return 1 if any(x['status']=='failed' for x in status) else 0


if __name__ == '__main__':
    sys.exit(main())
