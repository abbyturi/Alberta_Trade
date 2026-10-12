"""Reproducible seven-economy 2024 trade benchmark and Alberta conditional scenario."""
from pathlib import Path
import io,json,zipfile,warnings
import numpy as np,pandas as pd
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
from sklearn.ensemble import HistGradientBoostingRegressor,RandomForestRegressor,ExtraTreesRegressor
from sklearn.linear_model import Ridge,LogisticRegression,PoissonRegressor
from sklearn.inspection import permutation_importance
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
P=Path(__file__).resolve().parents[1]; D=P/'data'; S=D/'raw'; O=D/'processed'; O.mkdir(exist_ok=True)
ISO={'US':'USA','CA':'CAN','MX':'MEX','CN':'CHN','KR':'KOR','JP':'JPN','GB':'GBR'}
FEATURES=['log_gdp_o','log_gdp_d','log_pop_o','log_pop_d','log_dist','contig','comlang_off','comcol','log_gdpcap_o','log_gdpcap_d','log_import_demand_excl_pair','hs2','hs4num']
def factors():
 if not (S/'Alberta_Q1_03_model_factors.zip').exists():
  # Portable repository: use the already-extracted source inputs.
  g=pd.read_csv(D/'source'/'gravity_2021_seven_economies.csv')
  g.to_csv(O/'gravity_2021_seven_economies.csv',index=False)
  wd=pd.read_csv(D/'source'/'wdi_2024_or_2023_latest_available_seven_economies.csv')
  wd.to_csv(O/'wdi_2024_seven_economies.csv',index=False)
  return g,wd
 with zipfile.ZipFile(S/'Alberta_Q1_03_model_factors.zip') as z:
  gravity=zipfile.ZipFile(io.BytesIO(z.read('Gravity_csv_V202211.zip')))
  cols=['year','iso3_o','iso3_d','dist','contig','comlang_off','comcol','gdp_o','gdp_d','pop_o','pop_d','gdpcap_o','gdpcap_d']
  arr=[]
  for c in pd.read_csv(gravity.open('Gravity_V202211.csv'),usecols=cols,chunksize=250000,low_memory=False):
   t=c[(c.year==2021)&c.iso3_o.isin(ISO.values())&c.iso3_d.isin(ISO.values())&(c.iso3_o!=c.iso3_d)]
   if len(t):arr.append(t)
  g=pd.concat(arr).drop_duplicates(['iso3_o','iso3_d']);g.to_csv(O/'gravity_2021_seven_economies.csv',index=False)
  # WDI workbook is retained in source; country-level 2024 extract is optional.
  # Default reproducible fast path uses CEPII 2021 GDP/population with explicit vintage labels.
  wd=pd.DataFrame({'iso3':list(ISO.values())})
  for c in ['gdp_usd','population','gdp_per_capita_usd','internet_users_pct']:
   wd[c]=np.nan
  wd.to_csv(O/'wdi_2024_seven_economies.csv',index=False)
  return g,wd

def build(g,wd):
 b=pd.read_csv(O/'baci_2024_seven_economies_hs4_usd_thousands.csv',dtype={'hs4':str});b.hs4=b.hs4.str.zfill(4)
 prods=sorted(b.hs4.unique());pairs=b[['origin','destination']].drop_duplicates();df=pairs.assign(k=1).merge(pd.DataFrame({'hs4':prods,'k':1}),on='k').drop(columns='k').merge(b[['origin','destination','hs4','v']],how='left',on=['origin','destination','hs4']);df.v=df.v.fillna(0)
 rev={v:k for k,v in ISO.items()};g=g.copy();g['origin']=g.iso3_o.map(rev);g['destination']=g.iso3_d.map(rev)
 df=df.merge(g.drop(columns=['year','iso3_o','iso3_d']),on=['origin','destination'],how='left',validate='many_to_one')
 for side,col in [('o','origin'),('d','destination')]:
  d=wd.rename(columns={'iso3':col}).copy();d[col]=d[col].map(rev)
  df=df.merge(d[[col,'gdp_usd','population','gdp_per_capita_usd','internet_users_pct']].rename(columns={'gdp_usd':f'gdp_wdi_{side}','population':f'pop_wdi_{side}','gdp_per_capita_usd':f'gdppc_wdi_{side}','internet_users_pct':f'internet_{side}'}),on=col,how='left')
  for src,target in [('gdp_wdi','gdp'),('pop_wdi','pop'),('gdppc_wdi','gdpcap')]:df[f'{target}_{side}']=df[f'{src}_{side}'].fillna(df[f'{target}_{side}'])
 # Leakage-free: importer HS4 total minus current pair flow; validation must be leave-pair-out.
 sums=df.groupby(['destination','hs4']).v.transform('sum');df['log_import_demand_excl_pair']=np.log1p((sums-df.v).clip(lower=0))
 for col in ['gdp_o','gdp_d','pop_o','pop_d','gdpcap_o','gdpcap_d','dist']:
  df['log_'+col]=np.log1p(pd.to_numeric(df[col],errors='coerce').clip(lower=0))
 df['hs2']=df.hs4.str[:2].astype(int);df['hs4num']=df.hs4.astype(int)
 for c in FEATURES:df[c]=df[c].replace([np.inf,-np.inf],np.nan).fillna(df[c].median() if df[c].notna().any() else 0)
 df.to_csv(O/'training_2024_hs4_with_factors.csv',index=False)
 return df

def evaluate(df):
 # Hold out two exporter identities; avoids same exporter appearing in training and test.
 test=df.origin.isin(['MX','GB']);train=df.loc[~test];valid=df.loc[test]
 X=train[FEATURES];y=np.log1p(train.v);Xt=valid[FEATURES];actual=valid.v.to_numpy()
 models={'zero_naive':None,'ridge_log':make_pipeline(StandardScaler(),Ridge(alpha=100)), 'random_forest':RandomForestRegressor(n_estimators=65,max_depth=12,min_samples_leaf=10,n_jobs=-1,random_state=42),'extra_trees':ExtraTreesRegressor(n_estimators=65,max_depth=12,min_samples_leaf=10,n_jobs=-1,random_state=42),'hist_gradient_boosting':HistGradientBoostingRegressor(max_iter=160,max_leaf_nodes=20,l2_regularization=8,random_state=42)}
 scores=[]; fitted={}
 for name,m in models.items():
  if m is None:pred=np.zeros(len(valid))
  else:
   m.fit(X,y);fitted[name]=m;pred=np.expm1(m.predict(Xt)).clip(0)
  scores.append({'model':name,'train_n':len(train),'test_n':len(valid),'test_exporters':'MX;GB','mae_usd_thousands':mean_absolute_error(actual,pred),'rmse_usd_thousands':np.sqrt(mean_squared_error(actual,pred)),'r2_value':r2_score(actual,pred),'wape':np.abs(actual-pred).sum()/max(actual.sum(),1),'log1p_rmse':np.sqrt(np.mean((np.log1p(actual)-np.log1p(pred))**2))})
 # Separate extensive-margin binary model, not confused with trade value estimation.
 cl=make_pipeline(StandardScaler(),LogisticRegression(max_iter=350,class_weight='balanced'))
 cl.fit(X,(train.v>0).astype(int));prob=cl.predict_proba(Xt)[:,1]
 from sklearn.metrics import roc_auc_score,average_precision_score
 classification={'roc_auc':float(roc_auc_score(valid.v>0,prob)),'average_precision':float(average_precision_score(valid.v>0,prob)),'test_positive_share':float((valid.v>0).mean())}
 pd.DataFrame(scores).sort_values('log1p_rmse').to_csv(O/'model_comparison.csv',index=False)
 (O/'extensive_margin_metrics.json').write_text(json.dumps(classification,indent=2))
 best=min((r for r in scores if r['model']!='zero_naive'),key=lambda r:r['log1p_rmse'])['model']
 # Held-out permutation importance on log-target, group-robust interpretation only.
 sample=valid.sample(min(1800,len(valid)),random_state=42)
 imp=permutation_importance(fitted[best],sample[FEATURES],np.log1p(sample.v),n_repeats=3,random_state=42,scoring='neg_mean_squared_error',n_jobs=1)
 pd.DataFrame({'feature':FEATURES,'importance_log_mse':imp.importances_mean,'std':imp.importances_std}).sort_values('importance_log_mse',ascending=False).to_csv(O/'permutation_importance.csv',index=False)
 # Conservative scenario: only destinations within the trained seven-country universe, six excluding CA.
 # Alberta-specific 2024 HS4 exports are the supply constraint; model destination attractiveness reweights them.
 a=pd.read_csv(O/'alberta_2024_hs4.csv',dtype={'hs4':str});a.hs4=a.hs4.str.zfill(4)
 supply=a.groupby('hs4').cad.sum();candidate=df[(df.origin=='CA')&(df.destination!='CA')].copy()
 candidate['model_score']=np.expm1(fitted[best].predict(candidate[FEATURES])).clip(0)
 candidate['alberta_supply_2024_cad']=candidate.hs4.map(supply).fillna(0)
 candidate['weighted_score']=candidate.model_score*np.sqrt(candidate.alberta_supply_2024_cad+1)
 # Anchored to observed 2024 Alberta exports to six countries, explicitly NOT independently estimated 2025 levels.
 total=a[a.destination.isin(candidate.destination.unique())].cad.sum();den=candidate.weighted_score.sum()
 candidate['scenario_allocated_cad']=candidate.weighted_score/den*total if den>0 else 0
 candidate[['destination','hs4','model_score','alberta_supply_2024_cad','scenario_allocated_cad']].to_csv(O/'conditional_six_market_scenario.csv',index=False)
 pd.DataFrame(scores).to_json(O/'model_comparison.json',orient='records',indent=2)
 return scores,best

def main():
 g,w=factors();print('WDI',len(w),'gravity',len(g),flush=True)
 df=build(g,w);print('TRAINING MATRIX',df.shape,flush=True)
 scores,best=evaluate(df);print('BEST',best,flush=True);print(pd.DataFrame(scores).to_string(index=False),flush=True)
if __name__=='__main__':main()
