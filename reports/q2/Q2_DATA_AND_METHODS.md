# Question 2 — reproducible baseline and legal-coverage verification (12 October 2026)

## Status: trade denominators complete; Section 338 tariff exposure NOT YET IDENTIFIED

The supplied `data(6).zip` contains the **original** 2025 Statistics Canada CIMT domestic-export ZIP. The Q2 pipeline extracts all US-destination HS6 domestic exports by province/territory, annualizes 2025 monthly records and retains all 13 jurisdictions. The observed Canada-to-US domestic export total is **CAD 517,282,733,046**; Alberta **CAD 152,042,164,486**. These are **all-product denominators**, NOT Section 338 tariff-exposed amounts. Q1 code and Q1 data have not been edited.

**Missing critical input:** authoritative transcription of active 2026 US Section 338 legal tariff and prohibition annexes (original proclamations 11046–11048, temporary suspension 11056, prohibition proclamations 11061–11063, September tariff amendments, and any later changes), with HTS8/HTS10, coverage and effective dates. The official USITC HTS Revision 21 is a general tariff schedule and **must not be mistaken for a Section 338 covered-products list**. Its revision archive confirms relevant proclamations, but the annex product codes are not established in this project. Accordingly, `verified_legal_measures.csv` is intentionally header-only. The script fails closed: it will NOT manufacture tariff exposure, prohibition exposure, or HS4 rankings.

## Reproduction

```bash
conda activate alberta-trade
python run_q2.py
```

Q1 remains independently runnable using `python run_complete.py`. Q2 has no dependency on Q1's model or outputs, but shares the raw-source convention and repository environment.

## Required legal dataset and HS6 concordance

Populate `data/source/q2/verified_legal_measures.csv` ONLY after verifying annex text against official sources. Columns: `hts_code,measure_type,active_from,active_to,legal_url,coverage_status,verified`. Each row must be a verified 8- or 10-digit HTS product code, `measure_type` must be `tariff` or `prohibition`, dates are `YYYY-MM-DD`, coverage is `full` or `partial`, and `verified=yes`. HTS8/HTS10 → HS6 is the first six digits, *provided the HS revision is compatible*. The join is at HS6 only, and is de-duplicated to avoid double-counting multiple U.S. tariff lines mapping to the same HS6. The policy snapshot is 2026-10-12. A partially covered HS6 is a **category upper-bound proxy**, not exact affected trade. A 2026 legal policy list is compared to a 2025 baseline (counterfactual exposure, not 2025 tariffs paid).

Tariff and prohibition outcomes are calculated **separately**. No import prohibition is treated as an additional tariff. The script does not add tariff percentages across overlapping tariff provisions. Legal exemptions, chapter 99 conditions, exclusion and suspension need human review before legal rows are marked verified.

## Exposure estimands

For province p and HS6 h, `X_ph` is 2025 CAD domestic exports to the United States. `H_T` is the verified set of active tariff-associated HS6 categories. `E_p = Σ_{h∈H_T} X_ph`. `I_p = 100 E_p / Σ_h X_ph`. Provincial share of national HS6 category exposure = `100 E_p / Σ_p E_p`. Alberta HS4 k intensity = `100 Σ_{h∈k∩H_T} X_AB,h / Σ_{h∈k} X_AB,h`. All exposure values are **gross exports in associated categories**, not lost exports, tariff revenue, or causal economic damages. For prohibitions use a distinct set `H_P` and separate reports.

## Economic model choice and identification

**Primary (identified from available inputs):** static accounting exposure; product-level and province-level intensities. This is the appropriate model for the assessment's requested *exposure*, not a claim of tariff-induced export losses. It needs no estimated trade elasticity.

**Optional (NOT estimated here):** partial-equilibrium Armington demand response `Δ ln Q ≈ -σ Δ ln(1+t)` conditional on incidence/pass-through, substitution elasticity σ, and counterfactual tariff wedge. Without product-specific elasticities and observed post-policy trade, such numbers would be hypothetical sensitivity scenarios, not empirically estimated losses. For intermediate input linkages and general equilibrium, a multi-sector Ricardian/input-output model is appropriate but requires sectoral input-output coefficients and credible elasticities not available in the supplied data. Do not apply Q1's low-performing trade ML model to causal tariff losses.

**Evidence:** Anderson & van Wincoop (2003) structural gravity; Caliendo & Parro (2015) multi-sector trade/input-output linkages; Amiti, Redding & Weinstein (2019) tariff pass-through and welfare; Fajgelbaum et al. (2020) trade-war effects. These studies support model choice and mechanisms but do **not** supply Section 338-specific 2026 treatment effects.

## Verified functioning reference URLs (no tracking query parameters)

- Official Statistics Canada CIMT: https://www150.statcan.gc.ca/n1/pub/71-607-x/71-607-x2021004-eng.htm
- 2025 domestic exports ZIP: https://www150.statcan.gc.ca/n1/pub/71-607-x/2021004/zip/CIMT-CICM_Dom_Exp_2025.zip
- USITC 2026 HTS revision archive: https://www.usitc.gov/harmonized_tariff_information/hts/archive/list
- USITC 2026 Revision 21: https://www.usitc.gov/2026_hts_revision_21
- Proclamation 11065 and its annex (Federal Register): https://www.govinfo.gov/content/pkg/FR-2026-09-14/pdf/2026-18839.pdf
- GovInfo Federal Register collections: https://www.govinfo.gov/app/collection/fr
- Anderson & van Wincoop (2003): https://doi.org/10.1257/000282803321455214
- Caliendo & Parro (2015): https://doi.org/10.1093/restud/rdu035
- Amiti, Redding & Weinstein (2019): https://doi.org/10.1257/jep.33.4.187
- Fajgelbaum et al. (2020): https://doi.org/10.1093/qje/qjz036

## Submission gate

**Not suitable as a final Q2 quantitative submission yet.** The authoritative HTS tariff/prohibition product-code annexes are missing. Any numerical tariff exposure or ranking at this stage would be fabricated. Once legal annexes are transcribed, the pipeline will generate province and Alberta HS4 outputs and allow an assessment-formatted one-page narrative plus up to four pages of exhibits.
