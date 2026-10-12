# Official legal annex extraction — partial, verified progress

As of 2026-10-12, transcribed from the **printed** annexes, not the HTML body:

- Proclamation 11065, Annex II (Federal Register p. 58346): 82 inserted U.S. HTS tariff lines and 8 deleted lines, effective September 15, 2026. Source: https://www.govinfo.gov/content/pkg/FR-2026-09-14/pdf/2026-18839.pdf
- Proclamation 11063, Annex I (Federal Register p. 58329): HTS 8711.50.00 import prohibition effective September 29, 2026. Source: https://www.govinfo.gov/content/pkg/FR-2026-09-14/pdf/2026-18837.pdf

**CRITICAL**: This is only an amendment delta and a prohibition. It does not enumerate the original Proclamations 11046, 11047, 11048 tariff universe or all later amendments. `verified_legal_measures.csv` intentionally remains empty; `run_q2.py` must not publish national tariff exposure.

The 2025 province-HS6 screening files are NOT total tariff exposure; partial HTS8/HTS10 coverage means an HS6 category match is an upper-bound *category* screen. For a complete tariff calculation, obtain original annexes, apply all effective amendments in date order, identify exclusions, and independently review every active line. U.S. 10-digit suffixes are not Canadian 10-digit codes.

Source evidence: Federal Register 91 FR 58339–58346 and 91 FR 58325–58329. For 11065, Annex I and Annex II use different granularity in a few lines; use the actual HTS note amendment in Annex II as the authoritative insertion/deletion instruction, subject to HTS revision reconciliation.
