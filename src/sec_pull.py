from edgar import Company
from wiki_pull import get_wiki_dataframe
import pandas as pd
import time
from setup_sec import setup_sec_identity

setup_sec_identity()

df = get_wiki_dataframe()
tickers = df["Symbol"]

start_time = time.time()

results = []

for ticker in tickers:
    company = Company(ticker)
    financial_data = company.get_financials()

    if financial_data is None:
        results.append({
            "ticker": ticker,
            "has_filing": False,
            "assets_missing": None,
            "liabilities_missing": None,
            "equity_missing": None,
            "liabilities_method": "unavailable",
            "can_calculate_ratio": False,
        })
        continue

    assets = financial_data.get_total_assets()
    liabilities = financial_data.get_total_liabilities()
    equity = financial_data.get_stockholders_equity()

    liabilities_method = "direct"

    if liabilities is None:
        result = financial_data.xb.query().by_concept("us-gaap:Liabilities", exact=True).to_dataframe()

        # undimentioned data is consolodated data in XBRL standard
        if len(result) > 1:
            undimensioned = result[result["is_dimensioned"] == False]
            # companies with only one is_dimensioned category sometimes only dimensioned
            if not undimensioned.empty:
                result = undimensioned
            result = result.sort_values("fiscal_year", ascending=False)

        if not result.empty:
            # select row by index
            liabilities = result.iloc[0]["numeric_value"]
            liabilities_method = "concept_search"
        elif equity is not None:
            liabilities = assets - equity
            liabilities_method = "derived"
        else:
            liabilities_method = "unavailable"

    can_calculate = assets is not None and liabilities is not None

    results.append({
        "ticker": ticker,
        "has_filing": True,
        "assets_missing": assets is None,
        "liabilities_missing": liabilities is None,
        "equity_missing": equity is None,
        "liabilities_method": liabilities_method,
        "can_calculate_ratio": can_calculate,
    })

elapsed = time.time() - start_time

status_df = pd.DataFrame(results)
status_df.to_csv("data/raw/debt_to_assets_status.csv", index=False)

print(status_df["liabilities_method"].value_counts())
print(f"can_calculate_ratio counts: {status_df['can_calculate_ratio'].value_counts()}")
print(f"total time: {elapsed:.1f} seconds")
