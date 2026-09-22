# assets/liabilities

from setup_sec import setup_sec_identity
import pandas as pd
from edgar import Company

setup_sec_identity()

df = pd.read_csv("data/raw/debt_to_assets_status.csv")

results = []

# index manditory for .iterrows
# _ when unused manditory value
for _, row in df.iterrows():
    ticker = row["ticker"]
    method = row["liabilities_method"]
    can_calculate = row["can_calculate_ratio"]

    if can_calculate == False:
        results.append({"ticker": ticker, "leverage_ratio": None})
        continue

    company = Company(ticker)
    financial_data = company.get_financials()
    assets = financial_data.get_total_assets()

    if method == "direct":
        liabilities = financial_data.get_total_liabilities()
    elif method == "concept_search":
        result = financial_data.xb.query().by_concept("us-gaap:Liabilities", exact=True).to_dataframe()
        if len(result) > 1:
            undimensioned = result[result["is_dimensioned"] == False]
            # handles multiple year only dimensioned case
            if not undimensioned.empty:
                result = undimensioned
        result = result.sort_values("fiscal_year", ascending=False)
        liabilities = result.iloc[0]["numeric_value"]
    elif method == "derived":
        equity = financial_data.get_stockholders_equity()
        liabilities = assets - equity

    debt_to_assets_ratio = liabilities / assets

    results.append({"ticker": ticker, "debt_to_assets_ratio": debt_to_assets_ratio})

debt_to_assets_df = pd.DataFrame(results)
debt_to_assets_df.to_csv("data/processed/debt_to_assets_ratios.csv", index=False)