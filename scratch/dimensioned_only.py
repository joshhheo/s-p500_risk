import sys
sys.path.append("src")

import os
from dotenv import load_dotenv
from edgar import set_identity, Company

load_dotenv()
set_identity(os.getenv("SEC_user_agent"))

ticker = "CAH"

company = Company(ticker)
financial_data = company.get_financials()

result = financial_data.xb.query().by_concept("us-gaap:Liabilities", exact=True).to_dataframe()

print(result[["fiscal_year", "numeric_value", "is_dimensioned"]])
