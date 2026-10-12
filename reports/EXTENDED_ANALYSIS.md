# Alberta exports: extended empirical analysis and identification audit

## Executive interpretation
The repository now includes actual 2024 BACI global importer demand, supplied 2024 Alberta HS4 supply, available World Bank indicators (2023 fallback), a penalized Poisson quasi-maximum-likelihood (PPML) gravity benchmark, and a transparent global demand-share scenario. **The scenario is NOT an independently identified forecast of 2025 Alberta exports.** The initial assignment cannot be fully answered as stated from the supplied single-year seven-economy estimation sample without strong out-of-sample assumptions and external calibration. The report does not present speculative numbers as measured potential.

## Research question
Which 2025 markets and HS4 goods are Alberta's observed domestic export leaders, and which destinations are attractive under an internationally observed 2024 HS4 demand-share allocation? How reliably can a 2024 seven-economy model extrapolate to Alberta and unobserved destination economies?

## Sources and data construction
- Statistics Canada provincial domestic merchandise exports, 2024–2025: original supplied export archive, CAD nominal. The 2025 top-ten observed market/product table is `data/processed/observed_top10_top5_2025.csv`.
- CEPII Gravity V202211: supplied archive, 2021 bilateral measures. Seven-economy subset `data/source/gravity_2021_seven_economies.csv`.
- World Bank WDI: supplied WDIEXCEL.xlsx. **For the seven economies, 2024 GDP/population are missing from the supplied workbook**; `data/source/wdi_2024_or_2023_latest_available.csv` uses the available 2024 value, otherwise 2023. Most country GDP/population observations are 2023. Reproducible extraction in `src/final_extensions.py`.
- CEPII 2021 GDP is not a 2024 GDP estimate and must not be silently substituted for the WDI year.
- BACI HS2022 2024 bilateral HS6 flows, aggregated to HS4 in USD thousands; global importer-by-HS4 demand is in `data/source/baci_global_importer_hs4_demand_2024.csv`.
- BACI `product_codes_HS22_V202601.csv` supplies HS6 descriptions only. It is **not an authoritative HS4 heading concordance**. Official HS4 heading descriptions remain unverified; never present a representative HS6 description as an official HS4 heading. See https://unstats.un.org/unsd/classifications/Econ .

## Methods
Seven-economy PPML benchmark uses conditional mean exp(beta0 + beta' X) with standardized log GDP, population, CEPII distance, contiguity, common language, colonial links and HS2 numeric index. The model is regularized PoissonRegressor with 2024 BACI trade (scaled from USD thousands to USD millions). Mexico and UK exporters are held out. Regularization, absence of exporter/importer multilateral-resistance fixed effects, and treating HS2 as numeric limit structural interpretation. Coefficients are predictive associations, not causal estimates. Logistic, ridge, forest, extra-trees and boosting comparators remain available in `data/processed/model_comparison.csv`.

Global scenario: for each HS4, distribute Alberta's *observed 2024 product export value* across importers proportionally to their *observed 2024 global BACI import demand*. Rank the resulting scenario totals. This is a benchmark constrained to actual 2024 Alberta product supply, NOT an independent 2025 prediction. No 2025 price forecasts, exchange-rate conversion, Alberta-to-partner shipping distances, tariff barriers, or independently validated production capacity are available. The demand-share ranking is a counterfactual allocation, not a gravity prediction. Countries without matched WDI GDP and population are excluded, potentially biasing ranks.

## Validation and limitations
`data/processed/ppml_metrics.json` contains held-out metrics. A high WAPE means PPML is not reliable for decision-grade value predictions. Global extrapolation from only seven economies is unvalidated; global demand allocation cannot repair this. Current-year GDP, exact provincial distance matrix, official HS4 labels and actual independent 2025 global export potential remain unresolved. The research should not claim those gaps are complete.

## Alberta geographic treatment
A Canadian bilateral CEPII distance is not an Alberta-specific distance. The seven-country training data cannot identify a credible Alberta geographic coefficient. An Alberta-to-market great-circle measure would require a documented coordinate convention (Edmonton/Calgary), importer economic-centre coordinates, and a port/logistics sensitivity analysis. No unverified distances have been substituted.

## Primary sources
- Anderson and van Wincoop (2003), Gravity with Gravitas, https://doi.org/10.1257/000282803321455214
- Santos Silva and Tenreyro (2006), The Log of Gravity, https://doi.org/10.1162/rest.88.4.641
- Head and Mayer (2014), Gravity Equations: Workhorse, Toolkit, and Cookbook, https://doi.org/10.1016/B978-0-444-54314-1.00003-3
- CEPII Gravity, https://www.cepii.fr/PDF_PUB/wp/2022/wp2022-05.pdf
- World Bank WDI, https://databank.worldbank.org/source/world-development-indicators
- UN HS classifications, https://unstats.un.org/unsd/classifications/Econ
- Statistics Canada provincial GDP table 36-10-0222-01, https://doi.org/10.25318/3610022201-eng
