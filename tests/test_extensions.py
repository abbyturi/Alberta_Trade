from pathlib import Path
import pandas as pd
P=Path(__file__).resolve().parents[1]
def test_global_scenario_ten():
 p=P/'data/processed/global_top10_demand_share_scenario_NOT_2025_FORECAST.csv'
 if p.exists():
  d=pd.read_csv(p);assert len(d)==10;assert d.allocated_cad_2024_supply_anchor.ge(0).all()
def test_wdi_country_coverage():
 p=P/'data/source/wdi_2024_or_2023_latest_available.csv'
 if p.exists():
  d=pd.read_csv(p);assert {'CAN','USA','CHN'}.issubset(set(d.iso3))
