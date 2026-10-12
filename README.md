# Trade Analytics: Export Diversification and Tariff Exposure

This project applies **data science, machine learning, and international trade economics** to assess Alberta’s export growth potential and Canada’s exposure to U.S. trade measures.

The analysis focuses on two key areas:

- **Export Growth & Diversification:** Analyzing bilateral trade flows at the HS4 product level and developing predictive models using macroeconomic, geographic, and socioeconomic indicators to identify potential export markets and products.
- **Tariff Exposure & Economic Risk:** Quantifying Canada's export exposure to U.S. trade measures using harmonized HS6 product classifications, provincial comparisons, and exposure intensity metrics.

**Technical Focus:** Trade data integration, feature engineering, predictive machine learning, economic modelling, HS product classification, risk quantification, and data visualization.

**Data Sources:** Statistics Canada, CEPII BACI, World Bank Development Indicators, and U.S. tariff schedules.

The project aims to translate complex trade data into actionable insights for evidence-based economic policy, export diversification, and strategic decision-making.

> **Current entry point:** `python run.py` for both questions. See [RUN_GUIDE.md](RUN_GUIDE.md). 

# Alberta merchandise exports: reproducible evidence and model audit

## Reproducible execution

```bash
conda env create -f environment.yml
conda activate alberta-trade
python run_complete.py
```

`python run.py` runs the legacy descriptive prototype and requires editing its raw path; prefer `run_complete.py`. The complete-analysis script is modularized in `src/complete_analysis.py`. It reads the actual supplied archives in `data/raw/` and writes outputs in `data/processed/`.

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

## Data 

- `data/raw/`: all **original unmodified supplied** archives, and the original data-source documentation. Large files are intentionally included in the full distribution.
- `data/source/`: small, relevant, extracted analysis input subsets: 2024 and 2025 Alberta HS4 values, seven-economy 2024 BACI, and 2021 CEPII pair factors. They are useful for inspecting inputs without decompressing the original archives.
- `data/processed/`: modeling matrix, held-out model comparison, explainability, extensive-margin metrics, conditional market scenario and observed destination-product outputs.

## References

\- Anderson, J. E., & van Wincoop, E. (2003). Gravity with gravitas: A solution to the border puzzle. American Economic Review, 93(1), 170–192. [https://doi.org/10.1257/000282803321455214](https://doi.org/10.1257/000282803321455214)

\- Bank of Canada. (n.d.). Exchange rates. [https://www.bankofcanada.ca/rates/exchange/](https://www.bankofcanada.ca/rates/exchange/)

\- Centre d'Études Prospectives et d'Informations Internationales (CEPII). (n.d.). BACI: International trade database at the product level. [https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37](https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37)

\- Centre d'Études Prospectives et d'Informations Internationales (CEPII). (n.d.). Gravity database. [https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=8](https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=8)

\- Conte, M., Cotterlaz, P., & Mayer, T. (2022). The CEPII gravity database (Working Paper No. 2022-05). CEPII. [https://www.cepii.fr/PDF_PUB/wp/2022/wp2022-05.pdf](https://www.cepii.fr/PDF_PUB/wp/2022/wp2022-05.pdf)

\- Global Affairs Canada. (n.d.). Trade and investment agreements. [https://www.international.gc.ca/trade-commerce/trade-agreements-accords-commerciaux/agr-acc/index.aspx?lang=eng](https://www.international.gc.ca/trade-commerce/trade-agreements-accords-commerciaux/agr-acc/index.aspx?lang=eng)

\- Head, K., & Mayer, T. (2014). Gravity equations: Workhorse, toolkit, and cookbook. In G. Gopinath, E. Helpman, & K. Rogoff (Eds.), Handbook of international economics (Vol. 4, pp. 131–195). Elsevier. [https://doi.org/10.1016/B978-0-444-54314-1.00003-3](https://doi.org/10.1016/B978-0-444-54314-1.00003-3)

\- Office of the Federal Register. (n.d.). Federal Register: Section 338 trade measures concerning Canada. [https://www.federalregister.gov/documents/search?conditions%5Bterm%5D=section%20338%20Canada%202026](https://www.federalregister.gov/documents/search?conditions%5Bterm%5D=section%20338%20Canada%202026)

\- Office of the Federal Register. (n.d.). Federal Register: Section 338 import prohibitions involving Canada. [https://www.federalregister.gov/documents/search?conditions%5Bterm%5D=section%20338%20import%20prohibition%20Canada](https://www.federalregister.gov/documents/search?conditions%5Bterm%5D=section%20338%20import%20prohibition%20Canada)

\- Santos Silva, J. M. C., & Tenreyro, S. (2006). The log of gravity. The Review of Economics and Statistics, 88(4), 641–658. [https://doi.org/10.1162/rest.88.4.641](https://doi.org/10.1162/rest.88.4.641)

\- Statistics Canada. (n.d.). Canadian international merchandise trade (CIMT) web application. [https://www150.statcan.gc.ca/n1/pub/71-607-x/71-607-x2021004-eng.htm](https://www150.statcan.gc.ca/n1/pub/71-607-x/71-607-x2021004-eng.htm)

\- Statistics Canada. (n.d.). Table 12-10-0173-01: International merchandise trade by province/territory [Data table]. [https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1210017301](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1210017301)

\- Statistics Canada. (n.d.). Table 12-10-0175-01: International merchandise trade by province/territory [Data table]. [https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1210017501](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1210017501)

\- Statistics Canada. (n.d.). Table 17-10-0009-01: Population estimates, quarterly [Data table]. [https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901)

\- Statistics Canada. (n.d.). Table 36-10-0402-01: Gross domestic product (GDP) at basic prices, by industry, provinces and territories [Data table]. [https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3610040201](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3610040201)

\- Statistics Canada. (2023). Canadian international merchandise trade: Domestic exports, 2023 [Data set]. [https://www150.statcan.gc.ca/n1/pub/71-607-x/2021004/zip/CIMT-CICM_Dom_Exp_2023.zip](https://www150.statcan.gc.ca/n1/pub/71-607-x/2021004/zip/CIMT-CICM_Dom_Exp_2023.zip)

\- Statistics Canada. (2024). Canadian international merchandise trade: Domestic exports, 2024 [Data set]. [https://www150.statcan.gc.ca/n1/pub/71-607-x/2021004/zip/CIMT-CICM_Dom_Exp_2024.zip](https://www150.statcan.gc.ca/n1/pub/71-607-x/2021004/zip/CIMT-CICM_Dom_Exp_2024.zip)

\- Statistics Canada. (2025). Canadian international merchandise trade: Domestic exports, 2025 [Data set]. [https://www150.statcan.gc.ca/n1/pub/71-607-x/2021004/zip/CIMT-CICM_Dom_Exp_2025.zip](https://www150.statcan.gc.ca/n1/pub/71-607-x/2021004/zip/CIMT-CICM_Dom_Exp_2025.zip)

\- United Nations Statistics Division. (n.d.). Classification of international trade. [https://unstats.un.org/unsd/tradekb/Knowledgebase/50018/Classification-of-International-Trade](https://unstats.un.org/unsd/tradekb/Knowledgebase/50018/Classification-of-International-Trade)

\- United Nations Statistics Division. (n.d.). Economic classifications: Harmonized Commodity Description and Coding System (HS). [https://unstats.un.org/unsd/classifications/Econ](https://unstats.un.org/unsd/classifications/Econ)

\- United Nations Statistics Division. (n.d.). UN Comtrade API. [https://comtradeapi.un.org/public/v1/preview/C/A/2024](https://comtradeapi.un.org/public/v1/preview/C/A/2024)

\- U.S. Census Bureau. (n.d.). Foreign trade: Data. [https://www.census.gov/foreign-trade/data/index.html](https://www.census.gov/foreign-trade/data/index.html)

\- U.S. Government Publishing Office. (n.d.). Federal Register collection. [https://www.govinfo.gov/app/collection/fr](https://www.govinfo.gov/app/collection/fr)

\- U.S. Government Publishing Office. (2026, September 14). Federal Register document 2026-18839 [Proclamation and annexes]. [https://www.govinfo.gov/content/pkg/FR-2026-09-14/pdf/2026-18839.pdf](https://www.govinfo.gov/content/pkg/FR-2026-09-14/pdf/2026-18839.pdf)

\- U.S. International Trade Commission. (n.d.). DataWeb: U.S. international trade statistics. [https://dataweb.usitc.gov/](https://dataweb.usitc.gov/)

\- U.S. International Trade Commission. (n.d.). Harmonized Tariff Schedule archives. [https://www.usitc.gov/harmonized_tariff_information/hts/archive/list](https://www.usitc.gov/harmonized_tariff_information/hts/archive/list)

\- U.S. International Trade Commission. (n.d.). Harmonized Tariff Schedule of the United States. [https://hts.usitc.gov/](https://hts.usitc.gov/)

\- World Bank. (n.d.). Logistics Performance Index. [https://lpi.worldbank.org/](https://lpi.worldbank.org/)

\- World Bank. (n.d.). World Development Indicators. [https://datatopics.worldbank.org/world-development-indicators/](https://datatopics.worldbank.org/world-development-indicators/)

\- World Bank. (n.d.). Worldwide Governance Indicators. [https://www.worldbank.org/en/publication/worldwide-governance-indicators](https://www.worldbank.org/en/publication/worldwide-governance-indicators)

\- World Trade Organization. (n.d.). WTO tariff & trade data. [https://tariffdata.wto.org/](https://tariffdata.wto.org/)







