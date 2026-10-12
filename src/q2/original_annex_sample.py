"""Manually checked FIRST PAGE ONLY of two original annexes; not complete coverage."""
from pathlib import Path
import csv,re
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'data/source/q2/original_annex_first_page_verified_PARTIAL.csv'
# Page 5 of original Federal Register PDFs; source PDF page index 4.
ALCOHOL='''2203.00.00 2204.10.00 2204.21.20 2204.21.30 2204.21.50 2204.21.60 2204.21.80 2204.22.20 2204.22.40 2204.22.60 2204.22.80 2204.29.61 2204.29.81 2205.10.30 2206.00.15 2206.00.30 2206.00.45 2206.00.60 2206.00.90 2207.10.30 2208.20.10'''.split()
DAIRY='''0402.10.05 0402.10.10 0402.10.50 0402.21.02 0402.21.05 0402.21.25 0402.21.27 0402.21.30 0402.21.50 0402.21.73 0402.21.75'''.split()
rows=[]
for p,fn,fr,ls in [('11046','2026-14991.pdf','46643',ALCOHOL),('11047','2026-14992.pdf','46657',DAIRY)]:
 for code in ls:
  assert len(re.sub('[^0-9]','',code))==8
  rows.append({'proclamation':p,'hts_code':code,'hs6':re.sub('[^0-9]','',code)[:6],'annex':'I','pdf_page':5,'federal_register_page':fr,'source_pdf':fn,'official_url':f'https://www.govinfo.gov/content/pkg/FR-2026-07-23/pdf/{fn}','verification':'manually_read_original_page_5_only','is_complete_proclamation':'no'})
OUT.parent.mkdir(parents=True,exist_ok=True)
with OUT.open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('Verified page-five original annex entries:',len(rows))
if __name__=='__main__':pass
