import os
from dotenv import load_dotenv
from edgar import set_identity, Company
from wiki_pull import get_wiki_dataframe
import time

# writes environment variables to os environment
load_dotenv()

# accesses variable from os environment
user_agent = os.getenv("SEC_user_agent")

set_identity(user_agent)

df = get_wiki_dataframe()

tickers = df["Symbol"]

for ticker in tickers[:10]:
    company = Company(ticker)
    financial_data = company.get_financials()
    assets = financial_data.get_total_assets()
    liabilities = financial_data.get_total_liabilities()

    print(f"Ticker: {ticker}")
    print(f"Assets: {assets}")
    print(f"Liabilities: {liabilities}")
    # SEC EDGAR rates limit at 10 requests per second
    # give margin for request time variability
    time.sleep(0.2)
