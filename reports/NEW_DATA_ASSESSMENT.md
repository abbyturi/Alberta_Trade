# Expanded source audit and temporal backtest

## What the two new archives fix

- The new BACI HS2022 v202601 archive provides **2022, 2023 and 2024** bilateral HS6 observations. We aggregated the specified seven trading economies to HS4 for all three years, retaining the original BACI units (**thousands of US dollars**).
- The new `data(4).zip` provides trade-agreement status, annual FX rates, population and real GDP files, and a World Bank workbook. Relevant small tabular files have been extracted to `data/source/`.
- An out-of-time **2024 holdout** is now implemented, training on 2022–2023 positive reported flows. Results are in `data/processed/temporal_2024_model_comparison.csv`.

## What remains unresolved by the supplied archives

- **HS4 heading descriptions:** `shared_hs_product_concordance.csv` contains **zero rows**. BACI `product_codes_HS22_V202601.csv` provides HS6 descriptions, not official HS4 headings. The project therefore refuses to pass these off as verified HS4 headings. Obtain the HS2022 headings from the UN Statistics Division or Statistics Canada and validate the revision and code coverage.
- **2025 potential values:** BACI supplies through 2024, not 2025. The added 2022–2024 panel supports temporal validation, but does not identify an Alberta-specific 2025 potential level. Global importer-demand shares remain a **scenario** rather than calibrated bilateral 2025 predictions.
- **Alberta geographic distance:** the new archives do not provide provincial-to-partner economic-center distances or transport-mode-specific trade costs. A geocoded external dataset and sensitivity analysis are needed. The Canadian bilateral gravity measures cannot simply be labeled Alberta-specific.
- **Nominal Alberta GDP:** supplied `3610040201_databaseLoadingData.csv` reports chained 2017 CAD; a nominal provincial GDP series at current prices is needed for GDP-level calibration. The annual FX table alone does not solve this.
- **PPML:** the prior penalized Poisson benchmark is not a structural gravity model; exporter/importer multilateral-resistance treatment, appropriate zero-flow sampling, cluster-robust inference and identification checks remain required.

## Temporal evaluation caveats

The temporal backtest uses **positive observed BACI flows**. Missing combinations are not presumed to be true zero trade. This avoids inventing zeros, but means the backtest cannot assess entry into previously unserved markets. The test is 2024, not 2025, and it is not a provincial transfer validation. Predictions use USD thousands.

## Reproducibility

Run `python run_new_sources.py` to recreate the extracted panel and temporal comparison. The two original new archives are in `data/raw/`, the curated inputs are in `data/source/`, and generated results are in `data/processed/`.

## References

- CEPII BACI: https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37
- United Nations HS classifications: https://unstats.un.org/unsd/classifications/Econ
- Statistics Canada Canadian Export Classification: https://www150.statcan.gc.ca/n1/en/catalogue/65-209-x
- World Bank WDI: https://databank.worldbank.org/source/world-development-indicators
- Anderson and van Wincoop (2003): https://doi.org/10.1257/000282803321455214
- Santos Silva and Tenreyro (2006): https://doi.org/10.1162/rest.88.4.641
