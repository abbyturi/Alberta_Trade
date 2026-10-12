# Model audit: actual seven-economy 2024 bilateral HS4 flows

## Research question
Can country-pair economic size, distance, historical connections and importer demand help predict the value of bilateral HS4 merchandise trade, and how far can that evidence be transported to Alberta?

## Data and identification
The target is 2024 BACI bilateral HS4 value (USD thousands) for the seven specified economies. Country-pair predictors come from the **2021** CEPII Gravity archive (latest supplied vintage). These include GDP, population, GDP per capita, distance, common border, common official language and shared colonial relationship. Destination-HS4 demand is calculated excluding the current exporting pair, avoiding direct use of the target itself, but it still includes flows from held-out origins in the evaluation sample; therefore this is a **same-year explanatory prediction** and not a strict prospective 2025 forecasting backtest. Missing WDI 2024 data were not silently imputed as real observations.

## Methods
Predict log(1+trade value) with regularized linear regression, random forest, extra trees and histogram gradient boosting, back-transform to USD thousands. A zero prediction is the naive baseline. Separately predict trade presence using logistic regression. Hold out all observations exported by Mexico and the United Kingdom. Evaluate MAE, RMSE, R², WAPE, and log-scale RMSE. Explainability uses held-out permutation importance. These are predictive associations, not causal effects.

## Empirical findings
Read `data/processed/model_comparison.csv`, `extensive_margin_metrics.json`, and `permutation_importance.csv` for measured results. The best model by log-scale RMSE is histogram gradient boosting, but **R² in trade value levels is only about 0.041 and WAPE about 0.946** on held-out exporters. This is weak generalization and rules out decision-grade export values.

## Unresolved work / research boundaries
- The provided training universe contains only six foreign destinations for Alberta. A top-ten prediction requires additional destination coverage, ideally matched training and candidate universes.
- Alberta cannot be naively treated as a seventh/eighth country with a Canada feature vector and CEPII country-pair distance; an Alberta-to-partner geographical measure must be estimated and validated.
- The WDI workbook is present but not incorporated in the fitted run. CEPII GDP/population are from 2021, not 2024.
- Official HS4 descriptions must be linked to the 2022 nomenclature before publication. HS6 descriptions are not HS4 heading labels.
- The current benchmark does not include gravity PPML, repeated temporal validation, production capacity, tariffs, exchange-rate harmonization or independently identified absolute potential.
- No defensible **2025 predicted top ten or predicted HS4 values** can be claimed from the available trained model.

## Policy use
Observed exports are usable as descriptive evidence. The conditional six-market scenario is **only a ranking/sensitivity illustration anchored to 2024 realized values**, not a potential estimate. It must not be mixed with observed 2025 exports.
