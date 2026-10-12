"""True temporal 2024 holdout using 2022-23 BACI; nonzero-flow sample only."""
from pathlib import Path
import numpy as np,pandas as pd,json
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import Ridge
from sklearn.ensemble import HistGradientBoostingRegressor,RandomForestRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'data/source';P=ROOT/'data/processed'
def run():
 d=pd.read_csv(S/'baci_seven_economies_2022_2024_hs4.csv',dtype={'hs4':str})
 # Training on 2022/2023, held-out 2024; HS4/country codes treated as categorical identifiers, not ordinal.
 x=pd.get_dummies(d[['exporter_iso3','importer_iso3','hs4']],dtype='float32');x['year']=d.year.astype('float32')-2022
 train=d.year.lt(2024);test=~train;y=np.log1p(d.v)
 models={'median_log_naive':DummyRegressor(strategy='median'),'ridge':make_pipeline(StandardScaler(with_mean=False),Ridge(alpha=100)), 'hist_gradient_boosting':HistGradientBoostingRegressor(max_iter=110,max_leaf_nodes=20,random_state=42),'random_forest':RandomForestRegressor(n_estimators=40,max_depth=12,min_samples_leaf=8,n_jobs=-1,random_state=42)}
 result=[];predictions=[]
 for name,model in models.items():
  model.fit(x.loc[train],y.loc[train]);pred=np.expm1(model.predict(x.loc[test])).clip(0);actual=d.loc[test,'v'].to_numpy()
  result.append({'model':name,'train_years':'2022;2023','test_year':2024,'train_nonzero':int(train.sum()),'test_nonzero':int(test.sum()),'mae_usd_thousands':float(mean_absolute_error(actual,pred)),'rmse_usd_thousands':float(np.sqrt(mean_squared_error(actual,pred))),'r2_value':float(r2_score(actual,pred)),'wape':float(np.abs(actual-pred).sum()/actual.sum()),'log_rmse':float(np.sqrt(np.mean((np.log1p(actual)-np.log1p(pred))**2)))})
  predictions.append(pd.DataFrame({'model':name,'year':2024,'actual_usd_thousands':actual,'predicted_usd_thousands':pred}))
 pd.DataFrame(result).to_csv(P/'temporal_2024_model_comparison.csv',index=False)
 (P/'temporal_validation_limitations.json').write_text(json.dumps({'caution':'Sample contains reported positive trade flows only, so cannot evaluate extensive margin or new market entry. No 2025 BACI outcome is available. 2024 holdout is for backtesting, not an independently calibrated Alberta 2025 potential forecast. Country/product one-hot codes do not encode economic mechanisms.'},indent=2))
 return result
if __name__=='__main__':print(pd.DataFrame(run()).to_string(index=False))
