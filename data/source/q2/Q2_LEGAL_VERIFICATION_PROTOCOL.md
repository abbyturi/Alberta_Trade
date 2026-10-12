# Section 338 legal coverage protocol — as of 2026-10-12

## Confirmed legal events, not confirmed tariff-line coverage
See `legal_source_register.csv`. The USITC HTS Revision 21 (October 9) is a classification reference, **not** an exhaustive Section 338 list. Official proclamations 11046–11048 initiated measures, 11056 postponed commencement to August 22, 11065 modified motor-vehicle coverage effective September 15, and 11063 introduced distinct import prohibitions effective September 29. These are confirmed by the linked government documents, but their annex codes have NOT been independently transcribed or validated here.

## Required completion sequence
1. Download each original proclamation and annex, all amendments and prohibitions. Check for any subsequent actions before October 12, 2026.
2. Transcribe each HTS8/HTS10 product line into `legal_events_template.csv`, including legal document, annex, action (`add`, `remove`, `suspend`, `resume`, `prohibit`, `unprohibit`), effective date, rate and source URL. For annexes embedded as images, visually verify the codes against the PDF; do not rely on HTML text alone.
3. Apply events in effective-date order, independently for tariff and prohibition; a prohibition superseding a tariff must not be counted in the tariff headline unless the legal text explicitly retains the duty.
4. Verify HTS codes against the October 9 USITC schedule; derive HS6 from the first six digits only after checking HS revision compatibility with Canadian 2025 HS6.
5. Flag partial HTS8/HTS10 coverage of an HS6 as `partial`. A single covered subline does not mean all Canadian exports in the HS6 paid the tariff.
6. Only after legal verification, populate `verified_legal_measures.csv` with one row per active legal HTS line, `verified=yes`, and `coverage_status=full` or `partial`.
7. Run `python run_q2.py`. An empty coverage file intentionally produces no exposure totals. Do not interpret zero verified lines as zero tariff exposure.

## Interpretation
`full_HS6_lower_bound_cad` is a conservative HS6 classification bound (only categories fully covered). `all_matched_HS6_upper_bound_cad` counts full and partial HS6 categories. Neither is the actual customs-assessed tariff burden. Tariff and import-prohibition exposure are computed separately.

## Economic evidence
- Caliendo and Parro (2015), *Estimates of the Trade and Welfare Effects of NAFTA*, https://doi.org/10.1093/restud/rdu035 — multi-sector quantitative trade, useful for extensions, not the baseline accounting.
- Amiti, Redding and Weinstein (2019), *The Impact of the 2018 Tariffs on Prices and Welfare*, https://doi.org/10.1257/jep.33.4.187 — tariff incidence; not a source of Section 338 coverage.
- Fajgelbaum et al. (2020), *The Return to Protectionism*, https://doi.org/10.1093/qje/qjz036 — trade-war impacts; not a Section 338 elasticity estimate.

Do not treat exposure values as predicted export losses or tariff payments. Q1 code and data are preserved.
