import sys
sys.path.append("src")

import os
from dotenv import load_dotenv
from edgar import set_identity, Company

load_dotenv()
set_identity(os.getenv("SEC_user_agent"))

ticker = "HONA"

company = Company(ticker)
financial_data = company.get_financials()

if financial_data is None:
    print("no filing")
else:
    print("filing availible")