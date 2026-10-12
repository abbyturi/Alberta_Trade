from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
def test_observed_top_five_per_market():
 d=pd.read_csv(ROOT/'data/processed/observed_top10_top5_2025.csv',dtype={'hs4':str})
 assert len(d)==50
 assert d.destination.nunique()==10
 assert (d.hs4.str.len()==4).all()
 assert d.groupby('destination').size().eq(5).all()
def test_three_data_subfolders():
 assert {p.name for p in (ROOT/'data').iterdir() if p.is_dir()}=={'raw','source','processed'}
def test_models_present():
 d=pd.read_csv(ROOT/'data/processed/model_comparison.csv')
 assert {'zero_naive','ridge_log','random_forest','extra_trees','hist_gradient_boosting'}<=set(d.model)
