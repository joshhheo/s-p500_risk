import sys
sys.path.append("src")
from edgar import Company
from setup_sec import setup_sec_identity

setup_sec_identity()

company = Company("UHS")
financial_data = company.get_financials()
print("assets:", financial_data.get_total_assets())
print("equity:", financial_data.get_stockholders_equity())
print(financial_data.get_total_liabilities())

result = financial_data.xb.query().by_concept("us-gaap:StockholdersEquity", exact=True).to_dataframe()
print(result[["fiscal_year", "numeric_value", "is_dimensioned", "label"]].to_string(index=False))