# Data Composition and Source Documentation

Question 1: Alberta's Export Growth and Diversification Potential

## 1. Purpose

This document describes the composition, provenance, and intended use of the datasets selected for the analysis of Alberta's export markets and export diversification potential.

The data collection supports two components of the assignment:

1. Observed export performance: Identify Alberta's ten largest export destination countries in 2025, ranked by domestic export value, and report the five leading HS4 products exported to each destination.
2. Model-estimated export potential: Develop a machine-learning model using 2024 bilateral HS4 merchandise trade flows among Canada, the United States, Mexico, China, South Korea, Japan, and the United Kingdom, supplemented by economic, demographic, geographic, and trade policy indicators. Apply the model to Alberta as a separate economic entity to estimate potential export destinations and product-level values.

The data package contains ten selected source files, organized into three archives. The original source files have been retained without modification. No observations have been filtered, aggregated, transformed, or imputed as part of the data composition.

## 2. Data package composition

| Archive                           | Contents                                                                                          | Number of files |
| --------------------------------- | ------------------------------------------------------------------------------------------------- | --------------- |
| `Alberta_Q1_01_exports.zip`       | Alberta domestic merchandise exports for 2024 and 2025                                            | 2               |
| `Alberta_Q1_02_BACI_2024.zip`     | Bilateral trade flows, product classifications, and country codes                                 | 3               |
| `Alberta_Q1_03_model_factors.zip` | GDP, population, international development indicators, geographic variables, and trade agreements | 5               |
| Total                             |                                                                                                   | 10              |

## 3. Dataset inventory and source references

### 3.1 Alberta domestic merchandise exports

Source: Statistics Canada, Canadian International Merchandise Trade (CIMT), domestic exports.

Official reference: [Statistics Canada Data Portal](https://www150.statcan.gc.ca/n1/en/type/data)

| Original file                | Reference year | Intended use                                                       |
| ---------------------------- | -------------- | ------------------------------------------------------------------ |
| `CIMT-CICM_Dom_Exp_2025.zip` | 2025           | Calculate observed export destinations and leading HS4 products    |
| `CIMT-CICM_Dom_Exp_2024.zip` | 2024           | Establish historical Alberta export patterns and baseline features |

The domestic export data provides export values classified by province of origin, destination country, commodity, and reporting period. The supplied 2025 archive includes HS6-level records that can be aggregated to HS4 by retaining the first four digits of the HS6 code.

For the observed analysis, the Alberta records will be selected, monthly values aggregated to calendar-year totals, and export destinations ranked by total value. The five leading HS4 products will then be identified for each of the ten highest-ranked destinations.

Domestic exports are used rather than total exports to focus on merchandise produced or substantially transformed in Canada, consistent with the assignment.

### 3.2 International bilateral merchandise trade

Source: CEPII, BACI International Trade Database, HS 2022 classification, January 2026 release.

Official reference: [CEPII BACI Database](https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37)

| Original file                    | Intended use                                                     |
| -------------------------------- | ---------------------------------------------------------------- |
| `BACI_HS22_Y2024_V202601.csv`    | 2024 bilateral merchandise trade observations for model training |
| `product_codes_HS22_V202601.csv` | Harmonized product codes and descriptions                        |
| `country_codes_V202601.csv`      | Country identifiers and reference mapping                        |

BACI provides harmonized bilateral merchandise trade data by exporter, importer, product, and year. The 2024 trade observations form the principal dependent variable for the machine-learning model.

BACI reports products at the HS6 level. HS4 trade values will be constructed by aggregating HS6 observations according to the first four digits of each product code. The accompanying reference tables support product identification and country-code consistency.

The training sample will cover directed trade relationships among the seven economies specified in the assignment. Domestic exporter-importer pairs will be excluded.

### 3.3 Alberta population

Source: Statistics Canada, Table 17-10-0009-01, Population estimates, quarterly.

Official reference: [Statistics Canada Table 17-10-0009-01](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901)

| Original file                        | Reference observation | Unit    |
| ------------------------------------ | --------------------- | ------- |
| `1710000901_databaseLoadingData.csv` | Alberta, July 1, 2024 | Persons |

The dataset provides Alberta-specific population estimates. The July 1, 2024 observation is selected as the annual population reference for the 2024 explanatory variables.

Population represents an economy's demographic scale and is included as an explanatory variable for exporters and importers. Alberta's own population will be used for its predictions rather than the Canadian national population.

### 3.4 Alberta gross domestic product

Source: Statistics Canada, Table 36-10-0402-01, Gross domestic product (GDP) at basic prices, by industry, provinces and territories.

Official reference: [Statistics Canada Table 36-10-0402-01](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3610040201)

| Original file                        | Reference observation         | Measurement                             |
| ------------------------------------ | ----------------------------- | --------------------------------------- |
| `3610040201_databaseLoadingData.csv` | Alberta, 2024, all industries | Chained 2017 Canadian dollars, millions |

The GDP dataset measures Alberta's real economic output by industry. The all-industries aggregate is the relevant observation for representing Alberta's economic size.

This dataset is retained as originally supplied. Its measurement basis differs from the current-price GDP measures commonly used in international gravity models. Consistent valuation and currency treatment will therefore be required before combining the provincial and international GDP variables.

### 3.5 International macroeconomic and development indicators

Source: World Bank, World Development Indicators (WDI).

Official reference: [World Bank World Development Indicators](https://databank.worldbank.org/source/world-development-indicators)

| Original file   | Relevant indicators                                        |
| --------------- | ---------------------------------------------------------- |
| `WDI_excel.zip` | GDP, total population, and selected development indicators |

The World Development Indicators dataset provides internationally comparable economic and demographic information for the seven training economies and additional export destinations considered during prediction.

The principal indicators are:

| Indicator         | World Bank code  | Intended use                        |
| ----------------- | ---------------- | ----------------------------------- |
| GDP, current US$  | `NY.GDP.MKTP.CD` | Exporter and importer economic size |
| Population, total | `SP.POP.TOTL`    | Exporter and importer population    |

The reference year for the model inputs is 2024. Additional development indicators may be considered where coverage and relevance justify inclusion. The supplied archive's indicator-level completeness must be verified before model estimation.

### 3.6 Bilateral geographic characteristics

Source: CEPII, Gravity Database.

Official reference: [CEPII Gravity Database](https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=8)

| Original file             | Intended use                                    |
| ------------------------- | ----------------------------------------------- |
| `Gravity_csv_V202211.zip` | Geographic and bilateral relationship variables |

The CEPII Gravity Database contains measures commonly used in empirical international trade models. The relevant variables include bilateral distance, shared borders, and common language.

These indicators represent geographic and informational trade frictions that may influence bilateral merchandise flows.

For Alberta predictions, geographic measures must be assigned consistently. Any use of Canadian national measures as proxies for unavailable Alberta-specific characteristics will be documented in the methodology.

### 3.7 Trade agreement indicators

Source: Compiled Canadian trade agreement partner-status dataset included in the supplied archive.

Primary official reference for checking agreement status: [Global Affairs Canada, Trade Agreements](https://www.international.gc.ca/trade-commerce/trade-agreements-accords-commerciaux/agr-acc/index.aspx?lang=eng)

| Original file                                | Intended use                                                                                  |
| -------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `canada_trade_agreements_partner_status.csv` | Identify preferential trade relationships involving Canada and relevant destination economies |

Trade agreements may influence market access and bilateral trade costs. The dataset is intended to support a trade agreement indicator where partner coverage and effective dates can be established.

The supplied file is a compiled reference dataset. Its original compiler and derivation method are not independently established by the filename. Agreement status and applicability in 2024 should therefore be checked against official government records before use.

## 4. Data integrity and preservation

The composition process was limited to selecting relevant source files from the uploaded archives and organizing them into three thematic ZIP packages.

The following preservation principles apply:

- Original filenames and file formats are retained.
- Original observations, classifications, and measurement units are unchanged.
- No duplicate removal, missing-value treatment, statistical adjustment, or currency conversion has been performed.
- No additional external datasets have been inserted into the composed archives.
- Source references are documented separately from the underlying data.

The official references identify the publishers and relevant source collections. They do not imply that the composed files were redownloaded or replaced with newer releases.

## 5. Data preparation requirements

The source files are retained in their original form. Subsequent analysis will require the following operations:

| Preparation activity      | Required treatment                                                                               |
| ------------------------- | ------------------------------------------------------------------------------------------------ |
| Alberta export selection  | Restrict Statistics Canada records to Alberta                                                    |
| Annual aggregation        | Sum monthly 2025 domestic export values                                                          |
| HS4 classification        | Aggregate HS6 trade values to four-digit HS categories                                           |
| Country harmonization     | Match Statistics Canada destination identifiers to BACI country identifiers                      |
| Model sample construction | Select 2024 bilateral flows among the seven specified economies                                  |
| Explanatory variables     | Align GDP, population, geographic characteristics, and trade agreement indicators                |
| Alberta-specific inputs   | Use Alberta GDP and population, with Canadian proxies where provincial variables are unavailable |
| Prediction destinations   | Define a destination universe containing at least ten eligible foreign markets                   |
| Model validation          | Evaluate predictive performance using observations excluded from model training                  |

These activities belong to the analytical processing stage and are not part of the original data composition.

## 6. Source limitations and methodological considerations

Trade classification: The international BACI dataset uses HS 2022. Statistics Canada's domestic export classification must be checked for compatibility before combining product-level observations. Aggregation to HS4 does not automatically resolve all classification differences.

Trade valuation: Statistics Canada domestic exports and BACI bilateral trade values originate from different statistical systems. Currency, valuation conventions, and reporting definitions must be aligned or clearly distinguished.

GDP comparability: The supplied Alberta GDP dataset measures output in chained 2017 Canadian dollars at basic prices. The World Bank current-US-dollar GDP series measures nominal output at market prices. These measures are not directly interchangeable. Statistics Canada also cautions that chained-dollar GDP is not appropriate for comparing nominal economic levels.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www150.statcan.gc.ca\&sz=32)

Statistics Canada

+1



Population reference: Alberta's population is represented by the July 1, 2024 estimate from Statistics Canada Table 17-10-0009-01.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www150.statcan.gc.ca\&sz=32)

Statistics Canada



Geographic variables: National bilateral distance and geographic indicators may not fully capture Alberta's location or transport connectivity. Any Canadian proxy values used for Alberta must be explicitly identified.

Prediction interpretation: Model-estimated export potential represents conditional predictions based on the specified training data, explanatory variables, and modeling assumptions. It must not be interpreted as observed exports or guaranteed additional export opportunities.

## 7. Data provenance summary

| Data provider         | Dataset                                                        | Official reference                                                                                                                  |
| --------------------- | -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Statistics Canada     | Canadian International Merchandise Trade                       | [International merchandise trade](https://www.statcan.gc.ca/en/subjects-start/international_trade)                                  |
| Statistics Canada     | Population estimates, Table 17-10-0009-01                      | [DOI: 10.25318/1710000901-eng](https://doi.org/10.25318/1710000901-eng)                                                             |
| Statistics Canada     | Provincial GDP, Table 36-10-0402-01                            | [DOI: 10.25318/3610040201-eng](https://doi.org/10.25318/3610040201-eng)                                                             |
| CEPII                 | BACI International Trade Database                              | [BACI](https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37)                                                          |
| CEPII                 | Gravity Database                                               | [Gravity](https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=8)                                                        |
| World Bank            | World Development Indicators                                   | [WDI](https://databank.worldbank.org/source/world-development-indicators)                                                           |
| Global Affairs Canada | Canadian trade agreements, official reference for verification | [Trade agreements](https://www.international.gc.ca/trade-commerce/trade-agreements-accords-commerciaux/agr-acc/index.aspx?lang=eng) |

## 8. Documentation scope

This documentation records the ten original files selected for the Alberta export analysis, their statistical sources, reference periods, intended analytical roles, and known compatibility considerations.

It documents the composition of the supplied data package only. It does not represent completion of data cleaning, feature engineering, model estimation, validation, or export-potential forecasting.