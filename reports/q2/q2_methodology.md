# Question 2 - reproducible baseline and legal-coverage verification (12 October 2026)

## Status: trade denominators complete; Section 338 tariff exposure 

The Q2 pipeline extracts all US-destination HS6 domestic exports by province/territory, annualizes 2025 monthly records and retains all 13 jurisdictions. The observed Canada-to-US domestic export total is **CAD 517,282,733,046**; Alberta **CAD 152,042,164,486**. These are **all-product denominators**, NOT Section 338 tariff-exposed amounts. 

## Exposure estimands

For province p and HS6 h, `X_ph` is 2025 CAD domestic exports to the United States. `H_T` is the verified set of active tariff-associated HS6 categories. `E_p = Σ_{h∈H_T} X_ph`. `I_p = 100 E_p / Σ_h X_ph`. Provincial share of national HS6 category exposure = `100 E_p / Σ_p E_p`. Alberta HS4 k intensity = `100 Σ_{h∈k∩H_T} X_AB,h / Σ_{h∈k} X_AB,h`. All exposure values are **gross exports in associated categories**, not lost exports, tariff revenue, or causal economic damages. For prohibitions use a distinct set `H_P` and separate reports.

## Economic model choice and identification

**Primary (identified from available inputs):** static accounting exposure; product-level and province-level intensities. This is the appropriate model for the assessment's requested *exposure*. It needs no estimated trade elasticity.

**Optional :** partial-equilibrium Armington demand response `Δ ln Q ≈ -σ Δ ln(1+t)` conditional on incidence/pass-through, substitution elasticity σ, and counterfactual tariff wedge. Without product-specific elasticities and observed post-policy trade, such numbers would be hypothetical sensitivity scenarios, not empirically estimated losses. For intermediate input linkages and general equilibrium, a multi-sector Ricardian/input-output model is appropriate but requires sectoral input-output coefficients and credible elasticities not available in the supplied data. Do not apply Q1's low-performing trade ML model to causal tariff losses.

**Evidence:** Anderson & van Wincoop (2003) structural gravity; Caliendo & Parro (2015) multi-sector trade/input-output linkages; Amiti, Redding & Weinstein (2019) tariff pass-through and welfare; Fajgelbaum et al. (2020) trade-war effects. These studies support model choice and mechanisms.

## Reference 

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
