from src.q2.analysis import PROVINCES, digits

def test_thirteen_jurisdictions():
    assert len(PROVINCES)==13

def test_us_hts_to_hs6():
    assert digits('8708.29.5060')[:6]=='870829'
    assert digits('0406.90.95')[:6]=='040690'
