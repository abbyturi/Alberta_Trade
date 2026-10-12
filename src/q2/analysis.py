"""Q2: independently reproducible provincial 2025 domestic-export denominator;
fail-closed Section 338 tariff/prohibition HS6 exposure join.
"""
from pathlib import Path
import csv, io, json, re, zipfile
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
RAW=ROOT/'data/raw/q2/CIMT-CICM_Dom_Exp_2025.zip'
OUT=ROOT/'data/processed/q2'
POL=ROOT/'data/source/q2/verified_legal_measures.csv'
PROVINCES={'NL':'Newfoundland and Labrador','PE':'Prince Edward Island','NS':'Nova Scotia','NB':'New Brunswick','QC':'Quebec','ON':'Ontario','MB':'Manitoba','SK':'Saskatchewan','AB':'Alberta','BC':'British Columbia','YT':'Yukon','NT':'Northwest Territories','NU':'Nunavut'}
REQUIRED=['hts_code','measure_type','active_from','active_to','legal_url','coverage_status','verified']
def digits(code):return re.sub(r'\D','',str(code))
def policy():
    p=pd.read_csv(POL,dtype=str).fillna('')
    assert set(REQUIRED).issubset(p.columns)
    if len(p)==0:return p
    assert p.verified.eq('yes').all(), 'Unverified legal coverage; refusing to calculate exposure'
    assert p.measure_type.isin(['tariff','prohibition']).all()
    assert p.hts_code.map(lambda x:len(digits(x)) in (8,10)).all()
    assert p.legal_url.str.startswith('https://').all()
    assert p.coverage_status.isin(['full','partial','unresolved']).all()
    assert not p.coverage_status.eq('unresolved').any(), 'Unresolved mapping; stop before reporting exposure'
    p['hs6']=p.hts_code.map(lambda x:digits(x)[:6]);p['hs4']=p.hs6.str[:4]
    p=p[(p.active_from<='2026-10-12') & ((p.active_to=='') | (p.active_to>='2026-10-12'))]
    return p

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(RAW) as z:
        name=next(n for n in z.namelist() if 'ODPFN018_' in n and n.endswith('.csv'))
        frames=[]
        with z.open(name) as fh:
            for chunk in pd.read_csv(fh,dtype={'HS6':str,'Country/Pays':str,'Province':str},chunksize=200000):
                chunk=chunk[(chunk['Country/Pays']=='US') & (chunk['Province'].isin(PROVINCES))].copy()
                chunk['hs6']=chunk.HS6.str.zfill(6)
                chunk=chunk[chunk.hs6.str.fullmatch(r'\d{6}')]
                chunk['year']=pd.to_numeric(chunk['YearMonth/AnnéeMois'].astype(str).str[:4],errors='coerce')
                chunk=chunk[chunk.year==2025]
                chunk['value_cad']=pd.to_numeric(chunk['Value/Valeur'],errors='raise')
                frames.append(chunk.groupby(['Province','hs6'],as_index=False).value_cad.sum())
    d=pd.concat(frames).groupby(['Province','hs6'],as_index=False).value_cad.sum()
    d=d.rename(columns={'Province':'province_code'});d['province_name']=d.province_code.map(PROVINCES)
    d['hs4']=d.hs6.str[:4];d['year']=2025;d['destination']='US'
    d=d[['year','province_code','province_name','destination','hs6','hs4','value_cad']]
    d.to_csv(OUT/'provincial_us_domestic_exports_2025_hs6.csv',index=False)
    totals=d.groupby(['province_code','province_name'],as_index=False).value_cad.sum().sort_values('value_cad',ascending=False)
    totals.to_csv(OUT/'provincial_us_exports_2025_denominators.csv',index=False)
    p=policy()
    status={'export_source':'Original supplied Statistics Canada CIMT 2025 domestic exports ODPFN018 HS6','year':2025,'province_count':len(totals),'total_canada_us_domestic_exports_cad':float(totals.value_cad.sum()),'legal_measure_rows_verified':len(p),'policy_as_of':'2026-10-12','tariff_exposure_status':'BLOCKED_UNTIL_VERIFIED_HTS_LIST' if p.empty else 'CALCULATED','prohibition_exposure_status':'BLOCKED_UNTIL_VERIFIED_HTS_LIST' if p.empty else 'CALCULATED','legal_review_status':'INCOMPLETE_ANNEX_CODE_VERIFICATION' if p.empty else 'REVIEWED_INPUT_ASSUMED','warning':'Do not equate HS6 exposure with exact HTS8/HTS10 coverage; partial matches are upper-bound category values.'}
    if len(p):
        # Deduplicate per HS6/measure so multiple US HTS codes never multiply Canadian export values.
        for kind in ['tariff','prohibition']:
            q=p[p.measure_type==kind].copy()
            hs=q.groupby('hs6').agg(coverage_status=('coverage_status',lambda x:'partial' if 'partial' in x.values else 'full'),legal_url=('legal_url',lambda x:'; '.join(sorted(set(x))))).reset_index()
            merged=d.merge(hs,on='hs6',how='left',validate='many_to_one')
            merged['exposed_cad']=merged.value_cad.where(merged.coverage_status.notna(),0)
            merged['full_hs6_lower_bound_cad']=merged.value_cad.where(merged.coverage_status.eq('full'),0)
            merged['all_matched_hs6_upper_bound_cad']=merged.exposed_cad
            merged.to_csv(OUT/f'{kind}_hs6_category_exposure_detail.csv',index=False)
            prov=merged.groupby(['province_code','province_name'],as_index=False).agg(export_value_cad=('value_cad','sum'),hs6_category_exposure_cad=('exposed_cad','sum'),full_hs6_lower_bound_cad=('full_hs6_lower_bound_cad','sum'),all_matched_hs6_upper_bound_cad=('all_matched_hs6_upper_bound_cad','sum'))
            prov['exposure_intensity_pct']=100*prov.hs6_category_exposure_cad/prov.export_value_cad
            prov['share_of_canadian_category_exposure_pct']=100*prov.hs6_category_exposure_cad/prov.hs6_category_exposure_cad.sum() if prov.hs6_category_exposure_cad.sum()>0 else 0
            prov.to_csv(OUT/f'{kind}_province_exposure.csv',index=False)
            ab=merged[merged.province_code=='AB'].groupby('hs4',as_index=False).agg(export_value_cad=('value_cad','sum'),hs6_category_exposure_cad=('exposed_cad','sum'),full_hs6_lower_bound_cad=('full_hs6_lower_bound_cad','sum'),all_matched_hs6_upper_bound_cad=('all_matched_hs6_upper_bound_cad','sum'))
            ab['hs4_exposure_intensity_pct']=100*ab.hs6_category_exposure_cad/ab.export_value_cad
            ab.sort_values('hs6_category_exposure_cad',ascending=False).to_csv(OUT/f'{kind}_alberta_hs4_exposure.csv',index=False)
    (OUT/'status.json').write_text(json.dumps(status,indent=2))
    print(json.dumps(status,indent=2));print(totals.to_string(index=False))
if __name__=='__main__':main()
