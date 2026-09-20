import sys
# to use modules from different folder
sys.path.append("src")

import os
from dotenv import load_dotenv
from edgar import set_identity, Company

load_dotenv()
set_identity(os.getenv("SEC_user_agent"))

ticker = "GOOGL"

company = Company(ticker)
financial_data = company.get_financials()

no_prefix = financial_data.xb.query().by_concept("Liabilities", exact=True).to_dataframe()
with_prefix = financial_data.xb.query().by_concept("us-gaap:Liabilities", exact=True).to_dataframe()

if no_prefix.empty and not with_prefix.empty:
    print("prefix required")
else:
    print("no prefix required")
