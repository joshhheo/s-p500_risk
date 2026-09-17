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

perfect_calculate = 0
cannot_calculate = 0
estimate_calculate = 0

start_time = time.time()

for ticker in tickers:
    company = Company(ticker)
    financial_data = company.get_financials()

    if financial_data is None:
        cannot_calculate += 1
        time.sleep(0.1)
        # skips to next iteration of loop
        continue

    assets = financial_data.get_total_assets()
    stockholders_equity = financial_data.get_stockholders_equity()
    liabilities = financial_data.get_total_liabilities()

    if assets is not None and liabilities is not None:
        perfect_calculate += 1
    elif (assets is not None or liabilities is not None) and stockholders_equity is not None:
        estimate_calculate += 1
    else:
        cannot_calculate += 1

    # SEC EDGAR rates limit at 10 requests per second
    # next request only executes after prior request gets response
    time.sleep(0.1)

end_time = time.time() - start_time

# 362 companies record total assets and total liabilities
# 128 companies record either total assets or total liabilities, but records stockholders equity
# 13 companies do not record assets, liabilties, equity totals enough to directly calculate with tool

print(perfect_calculate)
print(cannot_calculate)
print(estimate_calculate)
print(end_time)