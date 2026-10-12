# Alberta’s Export Growth and Diversification Potential
## Research note for the Assistant Deputy Minister's Office

### Abstract
We reconstruct Alberta's calendar-year 2025 domestic merchandise exports by destination and HS4 from supplied Statistics Canada records. We separately investigate whether a seven-economy 2024 HS4 bilateral dataset can support Alberta-specific opportunity rankings. An initial held-out-exporter gradient boosting benchmark performs poorly (R² 0.032), and the sample cannot support a worldwide predicted top ten. We report actual 2025 exports but withhold unsupported claims of predicted 2025 potential.

### Research questions
1. Which countries received the most Alberta-produced merchandise in 2025, and which HS4 groups dominate each market?
2. Do gravity-informed models generalize across trading economies sufficiently to identify Alberta's product-destination potential?
3. Does estimated market potential differ from current trade in ways suggesting diversification opportunities?

### Brief literature review and economic framework
Tinbergen (1962) introduced the trade-gravity analogy; Anderson (1979) and Anderson and van Wincoop (2003) gave microfoundations and multilateral-resistance implications. Eaton and Kortum (2002) connect trade patterns to technology and geographic barriers. Helpman, Melitz and Rubinstein (2008) emphasize extensive margins and zero trade. Santos Silva and Tenreyro (2006; 2022 review) establish the case for PPML rather than naive log-linear OLS under heteroskedasticity. Head and Mayer (2014) survey practical theory-consistent gravity estimation. Modern ML is complementary for prediction but does not identify causal effects of trade agreements or market-access policies from a single cross-section.

A defensible specification is E[X_ijh | Z] = exp(alpha_i + gamma_j + delta_h + beta_1 ln GDP_i + beta_2 ln GDP_j + beta_3 ln distance_ij + beta_4 border_ij + beta_5 language_ij + beta_6 FTA_ij + sector interactions). Exporter and importer effects may absorb time-invariant GDP measures in a one-year panel: avoid including collinear effects. A two-part model first predicts Pr(X>0) and then E[X | X>0].

### Data and methodology
CIMT 2025 monthly HS6 records are filtered to Alberta province of origin and aggregated to HS4 (first four HS6 digits), destination, and year. Values are Canadian dollars. BACI 2024 HS6 values are aggregated to HS4 for directed pairs among CA, US, MX, CN, KR, JP, GB; values are USD thousands. All 42 directed pairs are represented; missing HS4 flows are explicitly zero-filled in model training. Additional supplied covariates include WDI, CEPII Gravity, Alberta GDP, Alberta population, and Canadian FTA partner indicators. They are **not yet joined in the fitted exploratory model**. In a completed model Alberta GDP and population should replace Canada's, and missing Alberta development or other indicators should use Canadian proxies, flagged at feature level. GDP basis/currency must be reconciled.

### Exploratory benchmark and validation
The current benchmark is histogram gradient boosting on HS4 numeric code, HS2 chapter and destination imports from other members of the seven-country sample. It is trained on five exporter economies and tested on held-out Mexico and United Kingdom exporters. Import totals are computed using 2024 outcomes; thus this is **same-year explanatory benchmarking, not genuine ex-ante 2025 forecasting**. HS code treated as numeric imposes artificial ordering. Held-out R² 0.032 indicates poor value-level transferability. Model scores are subsequently weighted by Alberta's 2024 HS4 export composition and normalized to the six destination 2024 Alberta total. These are merely illustrative 2024-scale allocations and must not be presented as forecasts of 2025 export potential.

### Findings: observed 2025 exports
See `../data/processed/observed_top10_top5_2025.csv` for the requested 50 HS4 destination/product observations, in CAD. Destination ranking in the accompanying README and main response is computed from the underlying HS6 domestic export file.

### Interpretation and policy implications
The United States is overwhelmingly dominant in Alberta's observed exports. This concentration makes product-market diversification a legitimate risk-management question, but a credible ranking of alternative export destinations requires coverage beyond the seven model economies. The current model is not sufficiently predictive to support capital allocation or numerical export-growth targets. Validate sector-specific feasible capacity and market barriers before recommending product-country investments.

### Limitations
HS4 names are not yet official HS4 heading labels; the output has HS6 example descriptions. The fitted benchmark omits the supplied gravity, development and agreement covariates. Cross-sectional 2024 modeling cannot isolate 2025 shocks, tariff changes, commodity price shifts or causal policy impacts. Seven economies cannot yield ten distinct predicted destination countries. No interval estimates or validated global opportunity estimates are available.

### References (original sources / DOI, no tracking parameters)
- Tinbergen, J. (1962). *Shaping the World Economy*. https://hdl.handle.net/1765/16826
- Anderson, J. (1979). A Theoretical Foundation for the Gravity Equation. https://doi.org/10.2307/1925976
- Anderson, J. & van Wincoop, E. (2003). Gravity with Gravitas. https://doi.org/10.1257/000282803321455214
- Eaton, J. & Kortum, S. (2002). Technology, Geography, and Trade. https://doi.org/10.1111/1468-0262.00352
- Helpman, E., Melitz, M. & Rubinstein, Y. (2008). Estimating Trade Flows. https://doi.org/10.1162/qjec.2008.123.2.441
- Santos Silva, J. & Tenreyro, S. (2006). The Log of Gravity. https://doi.org/10.1162/rest.88.4.641
- Santos Silva, J. & Tenreyro, S. (2022). The Log of Gravity at 15. https://doi.org/10.1007/s10258-021-00203-w
- Head, K. & Mayer, T. (2014). Gravity Equations: Workhorse, Toolkit, and Cookbook. https://doi.org/10.1016/B978-0-444-54314-1.00003-3
- CEPII BACI database. https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37
- Statistics Canada population table 17-10-0009-01. https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901
- Statistics Canada GDP table 36-10-0402-01. https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3610040201
