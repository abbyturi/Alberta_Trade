"""Audit-ready *partial* Section 338 legal event reconciliation; never certifies completeness.

Legal HTS 8/10-digit codes are converted to 6-digit screening categories. An HTS
heading containing 8 digits is not equivalent to full Canadian HS6 coverage.
"""
from pathlib import Path
import argparse, json, re
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'data/source/q2'
OUT=ROOT/'data/processed/q2'
DATE='2026-10-12'
def normalize(x):
    s=re.sub('[^0-9]','',str(x))
    if len(s) not in (8,10):raise ValueError(f'Invalid US HTS8/HTS10 {x!r}')
    return s

def reconcile(date=DATE):
    """Events are not a complete universe. Never write verified_legal_measures.csv."""
    events=pd.read_csv(SOURCE/'verified_annex_events_partial.csv',dtype=str).fillna('')
    events['hts_digits']=events.hts_code.map(normalize)
    events['hs6']=events.hts_digits.str[:6]
    events['hs4']=events.hts_digits.str[:4]
    events=events[events.effective_from.le(date)].copy()
    events=events.sort_values(['effective_from','document_id','hts_digits'])
    # Apply exact-code removals and parent-heading removals (8-digit removal can
    # encompass prior 10-digit descendants). Retain unresolved ambiguity for review.
    active={}; issues=[]
    for e in events.itertuples():
        if e.measure_type!='tariff':continue
        if e.action=='add':
            active[e.hts_digits]=dict(hts_code=e.hts_digits,hs6=e.hs6,hs4=e.hs4,legal_url=e.legal_url,document_id=e.document_id,source_action='add',effective_from=e.effective_from)
        elif e.action=='remove':
            hits=[k for k in active if k==e.hts_digits or (len(e.hts_digits)==8 and k.startswith(e.hts_digits))]
            for k in hits:del active[k]
            if not hits:issues.append(dict(code=e.hts_digits,issue='Removal not found among known amendment additions; may remove original coverage',document_id=e.document_id))
    # An original-proclamation tariff list has NOT been included in the active
    # map. Hence even these remaining entries are amendment-only, not total.
    OUT.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(list(active.values()),columns=['hts_code','hs6','hs4','legal_url','document_id','source_action','effective_from']).to_csv(OUT/'amendment_only_active_codes_NOT_COMPLETE.csv',index=False)
    pd.DataFrame(issues,columns=['code','issue','document_id']).to_csv(OUT/'legal_reconciliation_unresolved.csv',index=False)
    exports=pd.read_csv(OUT/'provincial_us_domestic_exports_2025_hs6.csv',dtype={'hs6':str,'hs4':str})
    codes=set(x['hs6'] for x in active.values())
    matched=exports[exports.hs6.isin(codes)].copy()
    matched.to_csv(OUT/'amendment_only_hs6_detail_NOT_TOTAL_EXPOSURE.csv',index=False)
    provincial=matched.groupby(['province_code','province_name'],as_index=False).value_cad.sum().rename(columns={'value_cad':'matched_hs6_category_cad'})
    denom=exports.groupby(['province_code','province_name'],as_index=False).value_cad.sum().rename(columns={'value_cad':'total_us_domestic_exports_cad'})
    provincial=denom.merge(provincial,how='left',on=['province_code','province_name']).fillna({'matched_hs6_category_cad':0})
    provincial['category_screen_pct']=100*provincial.matched_hs6_category_cad/provincial.total_us_domestic_exports_cad
    provincial['scope']='Amendment additions only; not total Section 338 exposure'
    provincial.sort_values('matched_hs6_category_cad',ascending=False).to_csv(OUT/'amendment_only_province_screen_NOT_TOTAL_EXPOSURE.csv',index=False)
    ab=matched[matched.province_code=='AB'].groupby('hs4',as_index=False).value_cad.sum().sort_values('value_cad',ascending=False)
    ab.rename(columns={'value_cad':'matched_hs6_category_cad'}).to_csv(OUT/'amendment_only_alberta_hs4_screen_NOT_TOTAL_EXPOSURE.csv',index=False)
    prohib=events[events.measure_type=='prohibition'].copy()
    prohib.to_csv(OUT/'prohibition_events_SEPARATE.csv',index=False)
    status={'as_of':date,'active_tariff_universe_complete':False,'certified_exposure_permitted':False,'original_proclamation_annexes_extracted_completely':False,'known_amendment_additions_active':len(active),'unique_amendment_hs6':len(codes),'unmatched_removals_to_reconcile_against_originals':len(issues),'prohibition_events_separate':len(prohib),'note':'Partial HS6 category screening only; do not interpret as duties paid, trade lost, or total Section 338 exposure.'}
    (OUT/'legal_reconciliation_status.json').write_text(json.dumps(status,indent=2))
    return status
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--date',default=DATE);args=parser.parse_args();print(json.dumps(reconcile(args.date),indent=2))
