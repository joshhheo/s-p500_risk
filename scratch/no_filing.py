import sys
sys.path.append("src")

from edgar import Company
from quick_setup.setup_sec import setup_sec_identity

setup_sec_identity()

ticker = "HONA"

company = Company(ticker)
financial_data = company.get_financials()

if financial_data is None:
    print("no filing")
else:
    print("filing availible")
