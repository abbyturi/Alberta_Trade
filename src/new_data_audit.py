"""Audit and integrate user-provided expanded archives; never fabricate missing headings."""
from pathlib import Path
import zipfile,io,json,hashlib
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]; D=ROOT/'data'; S=D/'source'; P=D/'processed';R=D/'raw'
S.mkdir(exist_ok=True,parents=True);P.mkdir(exist_ok=True,parents=True);R.mkdir(exist_ok=True,parents=True)
YEARS=(2022,2023,2024)
ISO={'USA','CAN','MEX','CHN','KOR','JPN','GBR'}
def audit_and_extract():
 path=R/'BACI_HS22_V202601.zip'; meta=R/'data_complete.zip'
 if not path.exists():raise FileNotFoundError(f'Place expanded BACI archive at {path}')
 if not meta.exists():raise FileNotFoundError(f'Place supplemental data archive at {meta}')
 with zipfile.ZipFile(path) as z:
  codes=pd.read_csv(z.open('country_codes_V202601.csv')); codes.to_csv(S/'baci_country_codes.csv',index=False)
  ids=set(codes.loc[codes.country_iso3.isin(ISO),'country_code'])
  product=pd.read_csv(z.open('product_codes_HS22_V202601.csv'),dtype=str);product.code=product.code.str.zfill(6)
  product.to_csv(S/'baci_hs6_reference.csv',index=False)
  panel=[]; coverage=[]
  for year in YEARS:
   name=f'BACI_HS22_Y{year}_V202601.csv'; segments=[]; n=0
   for c in pd.read_csv(z.open(name),usecols=['i','j','k','v'],dtype={'i':'int32','j':'int32','k':str,'v':'float64'},chunksize=1100000):
    n+=len(c); c=c[c.i.isin(ids)&c.j.isin(ids)&(c.i!=c.j)].copy();c['hs4']=c.k.str.zfill(6).str[:4]
    segments.append(c.groupby(['i','j','hs4'],as_index=False).v.sum())
   d=pd.concat(segments).groupby(['i','j','hs4'],as_index=False).v.sum();d['year']=year
   d=d.merge(codes[['country_code','country_iso3']],left_on='i',right_on='country_code').rename(columns={'country_iso3':'exporter_iso3'}).drop(columns='country_code')
   d=d.merge(codes[['country_code','country_iso3']],left_on='j',right_on='country_code').rename(columns={'country_iso3':'importer_iso3'}).drop(columns='country_code')
   panel.append(d[['year','exporter_iso3','importer_iso3','hs4','v']]);coverage.append({'year':year,'raw_rows':n,'seven_economy_nonzero_rows':len(d)})
  out=pd.concat(panel,ignore_index=True);out.to_csv(S/'baci_seven_economies_2022_2024_hs4.csv',index=False)
 with zipfile.ZipFile(meta) as z:
  for name in ['data/FX_RATES_ANNUAL-sd-2017-01-01.csv','data/canada_trade_agreements_partner_status.csv','data/1710000901_databaseLoadingData.csv','data/3610040201_databaseLoadingData.csv']:
   (S/Path(name).name).write_bytes(z.read(name))
  concordance=pd.read_csv(z.open('data/shared_hs_product_concordance.csv'))
  status={'expanded_baci_years':list(YEARS),'baci_coverage':coverage,'hs4_concordance_rows':len(concordance),'hs4_heading_status':'MISSING: supplied concordance has zero records; HS6 descriptions must not be mislabeled HS4','baci_units':'USD thousands','baci_trade_flow_status':'positive flows only; missing exporter/importer/product cells are not necessarily observed zeros','source_2025_observed':'previously extracted Statistics Canada domestic export records, CAD','global_predictions':'Not independently identified by seven-country training data'}
 (P/'new_source_audit.json').write_text(json.dumps(status,indent=2));return out,status
if __name__=='__main__':
 _,r=audit_and_extract();print(json.dumps(r,indent=2))
