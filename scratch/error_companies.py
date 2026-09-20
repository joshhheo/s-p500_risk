import os
from dotenv import load_dotenv
from edgar import set_identity, Company
from wiki_pull import get_wiki_dataframe
import pandas as pd

load_dotenv()

user_agent = os.getenv("SEC_user_agent")

set_identity(user_agent)

df = get_wiki_dataframe()

tickers = df["Symbol"]

results = []

for ticker in tickers:
    company = Company(ticker)
    financial_data = company.get_financials()

    if financial_data is None:
        results.append({"ticker": ticker, "status": "cannot calculate"})
        continue

    assets = financial_data.get_total_assets()
    stockholders_equity = financial_data.get_stockholders_equity()
    liabilities = financial_data.get_total_liabilities()

    if assets is not None and liabilities is not None:
        status = "perfect"
    elif (assets is not None or liabilities is not None) and stockholders_equity is not None:
        status = "estimate"
    else:
        status = "cannot calculate"

    results.append(
    {
    "ticker": ticker,
    "status": status,
    "assets_missing": assets is None,
    "liabilities_missing": liabilities is None,
    "equity_missing": stockholders_equity is None,
    }
    )

company_status_df = pd.DataFrame(results)
company_status_df = company_status_df.sort_values("status")
company_status_df.to_csv("src/leverage_status.csv", index=False)
