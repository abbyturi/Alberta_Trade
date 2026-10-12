# Trade Analytics: Export Diversification and Tariff Exposure

This project applies **data science, machine learning, and international trade economics** to assess Alberta’s export growth potential and Canada’s exposure to U.S. trade measures.

The analysis focuses on two key areas:

- **Export Growth & Diversification:** Analyzing bilateral trade flows at the HS4 product level and developing predictive models using macroeconomic, geographic, and socioeconomic indicators to identify potential export markets and products.
- **Tariff Exposure & Economic Risk:** Quantifying Canada's export exposure to U.S. trade measures using harmonized HS6 product classifications, provincial comparisons, and exposure intensity metrics.

**Technical Focus:** Trade data integration, feature engineering, predictive machine learning, economic modelling, HS product classification, risk quantification, and data visualization.

**Data Sources:** Statistics Canada, CEPII BACI, World Bank Development Indicators, and U.S. tariff schedules.

The project aims to translate complex trade data into actionable insights for evidence-based economic policy, export diversification, and strategic decision-making.

> **Current entry point:** `python run.py` for both questions. See [RUN_GUIDE.md](RUN_GUIDE.md). 

## Standard commands and missing input handling

```bash
# Run both questions
python run.py

# Run Question 1 only
python run.py --question q1

# Run Question 2 with legal reconciliation
python run.py --question q2 --legal-audit

# Run all available stages and tests
python run.py --new-sources --legal-audit --tests

# Require every optional source archive to be present (nonzero exit otherwise)
python run.py --new-sources --legal-audit --tests --strict-inputs
```

**Missing original Q1 archives:** `--extended` requires `data/raw/data/Alberta_Q1_03_model_factors.zip` and `data/raw/data/Alberta_Q1_02_BACI_2024.zip`. `--new-sources` requires `data/raw/BACI_HS22_V202601.zip` and `data/raw/data_complete.zip`. These source archives were **not bundled** in the cleaned repository. By default, the runner explicitly **skips** optional stages whose inputs are missing, records `skipped_missing_inputs` in `reports/pipeline_last_run.json`, and continues with independent stages. A skipped stage has not executed. Add `--strict-inputs` to make missing optional inputs an error. Main Q1 and Q2 analyses are unaffected. Q2 legal exposure remains provisional.

# Alberta merchandise exports: reproducible evidence and model audit

## Reproducible execution

```bash
conda env create -f environment.yml
conda activate alberta-trade
python run_complete.py
```

`python run.py` runs the legacy descriptive prototype and requires editing its raw path; prefer `run_complete.py`. The complete-analysis script is modularized in `src/complete_analysis.py`. It reads the actual supplied archives in `data/raw/` and writes outputs in `data/processed/`.

## Data 

- `data/raw/`: all **original unmodified supplied** archives, and the original data-source documentation. Large files are intentionally included in the full distribution.
- `data/source/`: small, relevant, extracted analysis input subsets: 2024 and 2025 Alberta HS4 values, seven-economy 2024 BACI, and 2021 CEPII pair factors. They are useful for inspecting inputs without decompressing the original archives.
- `data/processed/`: modeling matrix, held-out model comparison, explainability, extensive-margin metrics, conditional market scenario and observed destination-product outputs.

## References

- Anderson and van Wincoop (2003), *Gravity with Gravitas*, https://doi.org/10.1257/000282803321455214
- Santos Silva and Tenreyro (2006), *The Log of Gravity*, https://doi.org/10.1162/rest.88.4.641
- Head and Mayer (2014), *Gravity Equations: Workhorse, Toolkit, and Cookbook*, https://doi.org/10.1016/B978-0-444-54314-1.00003-3
- Conte, Cotterlaz and Mayer (2022), *CEPII Gravity Database*, https://www.cepii.fr/PDF_PUB/wp/2022/wp2022-05.pdf
- UN Statistics Division, HS classifications, https://unstats.un.org/unsd/classifications/Econ 



## Standard run commands

Run these commands from the repository root after installing the required dependencies.

```bash
# Run both questions
python run.py

# Run Question 1 only
python run.py --question q1

# Run Question 2 with legal reconciliation
python run.py --question q2 --legal-audit

# Run all available analysis stages and tests
python run.py --new-sources --legal-audit --tests
```


