import sys
sys.path.append("src")

from edgar import Company
from setup_sec import setup_sec_identity

setup_sec_identity()

ticker = "GOOGL"

company = Company(ticker)
financial_data = company.get_financials()

result = financial_data.xb.query().by_concept("us-gaap:Liabilities", exact=True).to_dataframe()
print(result[["fiscal_year", "numeric_value", "is_dimensioned"]])
