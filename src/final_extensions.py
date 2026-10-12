"""Additional sourced covariates, PPML benchmark and global screening sensitivity.
No unverified HS4 descriptions or independently calibrated 2025 levels are invented.
"""
from pathlib import Path
import io,zipfile,json
import numpy as np,pandas as pd
from sklearn.linear_model import PoissonRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_absolute_error,r2_score
ROOT=Path(__file__).resolve().parents[1]; RAW=ROOT/'data/raw/data'; SOURCE=ROOT/'data/source'; OUT=ROOT/'data/processed'; SOURCE.mkdir(exist_ok=True);OUT.mkdir(exist_ok=True)
IND={'NY.GDP.MKTP.CD':'gdp_usd','SP.POP.TOTL':'population','NY.GDP.PCAP.CD':'gdp_per_capita_usd','IT.NET.USER.ZS':'internet_users_pct','NE.TRD.GNFS.ZS':'trade_pct_gdp'}

def extract_wdi():
 import openpyxl
 with zipfile.ZipFile(RAW/'Alberta_Q1_03_model_factors.zip') as z:
  with zipfile.ZipFile(io.BytesIO(z.read('WDI_excel.zip'))) as inner:
   wb=openpyxl.load_workbook(io.BytesIO(inner.read('WDIEXCEL.xlsx')),read_only=True,data_only=True)
   sh=wb['Data']; it=sh.iter_rows(values_only=True); header=next(it); idx=header.index('2024'); prev=header.index('2023'); records=[]
   for row in it:
    if row[3] in IND and row[1]:
     val=row[idx] if isinstance(row[idx],(int,float)) else row[prev]
     if isinstance(val,(int,float)):records.append((row[1],IND[row[3]],float(val),'2024' if isinstance(row[idx],(int,float)) else '2023'))
   wb.close()
 d=pd.DataFrame(records,columns=['iso3','indicator','value','vintage']).pivot_table(index='iso3',columns='indicator',values='value',aggfunc='first').reset_index();d.columns.name=None
 d.to_csv(SOURCE/'wdi_2024_or_2023_latest_available.csv',index=False)
 d[d.iso3.isin(['USA','CAN','MEX','CHN','KOR','JPN','GBR'])].to_csv(OUT/'wdi_2024_seven_economies.csv',index=False)
 return d

def country_codes():
 with zipfile.ZipFile(RAW/'Alberta_Q1_02_BACI_2024.zip') as z:
  d=pd.read_csv(z.open('country_codes_V202601.csv'))
 d.to_csv(SOURCE/'baci_country_codes.csv',index=False)
 return d

def hs6_reference():
 with zipfile.ZipFile(RAW/'Alberta_Q1_02_BACI_2024.zip') as z:d=pd.read_csv(z.open('product_codes_HS22_V202601.csv'),dtype=str)
 d.to_csv(SOURCE/'baci_hs6_reference.csv',index=False)
 # HS6 descriptions are not HS4 heading descriptions; do not misrepresent them.
 return d

def ppml_evaluation():
 d=pd.read_csv(OUT/'training_2024_hs4_with_factors.csv',dtype={'hs4':str})
 w=pd.read_csv(OUT/'wdi_2024_seven_economies.csv').set_index('iso3')
 iso={'US':'USA','CA':'CAN','MX':'MEX','CN':'CHN','KR':'KOR','JP':'JPN','GB':'GBR'}
 for side in ['o','d']:
  d[f'gdp2024_{side}']=d[{'o':'origin','d':'destination'}[side]].map(iso).map(w.gdp_usd)
  d[f'pop2024_{side}']=d[{'o':'origin','d':'destination'}[side]].map(iso).map(w.population)
  d[f'internet2024_{side}']=d[{'o':'origin','d':'destination'}[side]].map(iso).map(w.internet_users_pct)
  for col in ['gdp2024','pop2024']:d[f'log_{col}_{side}']=np.log1p(d[f'{col}_{side}'])
 cols=['log_gdp2024_o','log_gdp2024_d','log_pop2024_o','log_pop2024_d','log_dist','contig','comlang_off','comcol','hs2']
 for col in cols:d[col]=pd.to_numeric(d[col],errors='coerce').fillna(d[col].median())
 d.to_csv(OUT/'training_2024_hs4_wdi_integrated.csv',index=False)
 train=~d.origin.isin(['MX','GB']); test=~train
 # Trade is in BACI USD thousands, Poisson quasi-ML allows noninteger values and zero flows.
 # Scaling response to USD millions improves numerical stability; rescale predictions afterward.
 model=make_pipeline(StandardScaler(),PoissonRegressor(alpha=5,max_iter=220,tol=1e-5))
 model.fit(d.loc[train,cols],d.loc[train,'v']/1000)
 p=np.clip(model.predict(d.loc[test,cols])*1000,0,None); y=d.loc[test,'v'].to_numpy()
 result={'model':'PPML ridge-penalized baseline','test_exporters':['MX','GB'],'n_train':int(train.sum()),'n_test':int(test.sum()),'mae_usd_thousands':float(mean_absolute_error(y,p)),'r2_value':float(r2_score(y,p)),'wape':float(np.abs(y-p).sum()/max(y.sum(),1)),'caveat':'Penalized Poisson quasi-likelihood; not a structural gravity estimate; missing multilateral resistance and HS4 fixed effects.'}
 (OUT/'ppml_metrics.json').write_text(json.dumps(result,indent=2));pd.DataFrame({'feature':cols,'scaled_coefficient':model.named_steps['poissonregressor'].coef_}).to_csv(OUT/'ppml_coefficients.csv',index=False)
 return model,cols,w

def global_screen(model,cols,w):
 # Global importer demand is derived from the actual supplied 2024 BACI records.
 cc=country_codes();print('BACI country columns',cc.columns.tolist(),flush=True)
 with zipfile.ZipFile(RAW/'Alberta_Q1_02_BACI_2024.zip') as z:
  chunks=[]
  for chunk in pd.read_csv(z.open('BACI_HS22_Y2024_V202601.csv'),usecols=['j','k','v'],dtype={'j':'int32','k':str,'v':'float64'},chunksize=1500000):
   chunk['hs4']=chunk.k.str[:4];chunks.append(chunk.groupby(['j','hs4'],as_index=False).v.sum())
 demand=pd.concat(chunks).groupby(['j','hs4'],as_index=False).v.sum();demand.to_csv(SOURCE/'baci_global_importer_hs4_demand_2024.csv',index=False)
 # map BACI numeric codes to ISO3, using original country-code file
 print(cc.head(2).to_string(index=False),flush=True)
 cols_cc=cc.columns.tolist();num=next((c for c in cols_cc if 'country_code' in c.lower() or c.lower() in ('i','code')),cols_cc[0]);iso=next((c for c in cols_cc if 'iso3' in c.lower()),None)
 if iso is None:
  # If country code file has no ISO3, refuse to invent mapping.
  (OUT/'global_screen_status.json').write_text(json.dumps({'status':'not generated','reason':'No ISO3 mapping in BACI country code table; cannot map global WDI safely.'},indent=2));return
 cc[num]=pd.to_numeric(cc[num],errors='coerce');demand=demand.merge(cc[[num,iso]],left_on='j',right_on=num,how='left');demand=demand.merge(w,left_on=iso,right_on='iso3',how='left')
 demand=demand[demand.gdp_usd.gt(0)&demand.population.gt(0)&(demand[iso]!='CAN')].copy()
 # Alberta-as-Canada proxy on exporter GDP/population, and Canada-to-partner distance not available globally.
 # Global ranking therefore uses a demand-only transparent benchmark, NOT fabricated gravity distances.
 a=pd.read_csv(OUT/'alberta_2024_hs4.csv',dtype={'hs4':str});supply=a.groupby('hs4').cad.sum()
 demand['alberta_supply_2024_cad']=demand.hs4.map(supply).fillna(0)
 demand=demand[demand.alberta_supply_2024_cad.gt(0)].copy()
 # Demand shares across global importers, anchored to actual 2024 Alberta product export totals.
 # A global scenario, not a 2025 independent export-value forecast.
 denom=demand.groupby('hs4').v.transform('sum');demand['allocated_cad_2024_supply_anchor']=demand.alberta_supply_2024_cad*demand.v/denom
 agg=demand.groupby(iso,as_index=False).allocated_cad_2024_supply_anchor.sum().sort_values('allocated_cad_2024_supply_anchor',ascending=False).head(10)
 agg.to_csv(OUT/'global_top10_demand_share_scenario_NOT_2025_FORECAST.csv',index=False)
 top=demand[demand[iso].isin(agg[iso])].sort_values('allocated_cad_2024_supply_anchor',ascending=False).groupby(iso).head(5)
 top[[iso,'hs4','allocated_cad_2024_supply_anchor','alberta_supply_2024_cad']].to_csv(OUT/'global_top10_top5_demand_share_scenario_NOT_2025_FORECAST.csv',index=False)
 (OUT/'global_screen_status.json').write_text(json.dumps({'status':'completed as demand-share sensitivity ONLY','caveat':'Uses actual 2024 global import demand and Alberta 2024 HS4 supply; does not estimate absolute 2025 export potential or bilateral Alberta trade costs.'},indent=2))

def main():
 w=extract_wdi();print('WDI latest available 2023/2024 country rows',len(w),flush=True)
 hs6_reference();m,cols,ww=ppml_evaluation();print('PPML completed',flush=True)
 global_screen(m,cols,w);print('Global demand sensitivity completed',flush=True)
if __name__=='__main__':main()
