# Question 2 — evidence-based interim analysis (12 October 2026)

## Completed and reproducible

- Original Federal Register PDFs 11046, 11047 and 11048 preserved under `data/raw/q2/original_proclamations/`, with SHA-256 hashes.
- 2025 Statistics Canada provincial and territorial U.S.-bound domestic export data, by HS6, retained from the existing pipeline.
- Original Annex I, **page 5 only**, manually transcribed for 11046 (21 HTS8 entries) and 11047 (11 HTS8 entries). This is a *small subset*, not full original coverage.
- Previously recorded Proclamation 11065 amendment Annex II (82 additions and 8 removals) reconciled as an **amendment-only** screening set. The eight removals cannot be applied correctly until original codes are fully transcribed.
- Prohibition event 11063 remains in a **separate** file, not counted as tariff exposure.
- Code produces partial HTS8/HTS10→HS6 category screens and Alberta HS4 breakdown, without multiplying trade values when several U.S. lines map to one HS6.

## Blocking requirements for final national Section 338 exposure

1. Transcribe **all remaining pages** of original 11046, 11047 and 11048 annexes, especially the long 11048 annex. Validate against original PDF images and HTS schedule.
2. Confirm all intervening legal actions and effective dates; apply additions, deletions, suspension, exclusions and Section 232 interaction to the same as-of date.
3. Obtain October 9, 2026 USITC HTS revision and compare every HTS8/HTS10 classification and its descendants. An HS6 category may contain both covered and uncovered U.S. tariff lines.
4. Independently reconcile the provincial export denominator to Statistics Canada published totals and confirm HS revision concordance.
5. Only after (1)–(4), populate `data/source/q2/verified_legal_measures.csv` and run `python run_q2.py` for final results.

**Do not publish partial category screens as national exposure.** An HS6 category screen is an upper-bound classification measure for a partially covered code, not a measured tariff payment, export loss, or exact legally covered trade value. The conservative fully-covered HS6 lower bound cannot be established without a complete HTS descendant universe.

## Source links

- Original 11046: https://www.govinfo.gov/content/pkg/FR-2026-07-23/pdf/2026-14991.pdf
- Original 11047: https://www.govinfo.gov/content/pkg/FR-2026-07-23/pdf/2026-14992.pdf
- Original 11048: https://www.govinfo.gov/content/pkg/FR-2026-07-23/pdf/2026-14997.pdf
- Amendment 11065: https://www.govinfo.gov/content/pkg/FR-2026-09-14/pdf/2026-18839.pdf
- USITC archive: https://www.usitc.gov/harmonized_tariff_information/hts/archive/list
