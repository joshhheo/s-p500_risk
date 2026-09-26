import sys
sys.path.append("src")
from edgar import Company
from setup_sec import setup_sec_identity

setup_sec_identity()

company = Company("AAPL")
financial_data = company.get_financials()

print(financial_data.xb.period_of_report)