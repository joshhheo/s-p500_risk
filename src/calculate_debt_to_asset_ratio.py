import pandas as pd

def calculate_debt_to_assets():
    df = pd.read_csv("data/raw/company_status.csv")
    results = []

    for _, row in df.iterrows():
        assets = row["has_assets"]
        liabilities = row["has_liabilities"]
        equity = row["has_equity"]

        if pd.isna(liabilities) and pd.notna(assets) and pd.notna(equity):
            liabilities = assets - equity

        if pd.isna(assets) and pd.notna(liabilities) and pd.notna(equity):
            assets = liabilities + equity

        ratio = None
        if pd.notna(assets) and pd.notna(liabilities):
            ratio = liabilities / assets

        results.append({"ticker": row["ticker"], "debt_to_assets_ratio": ratio})

    pd.DataFrame(results).to_csv("data/processed/debt_to_assets_ratios.csv", index=False)

if __name__ == "__main__":
    calculate_debt_to_assets()
