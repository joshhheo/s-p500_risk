import pandas as pd
from quick_setup.get_financials import get_financial_data
from quick_setup.setup_sec_identity import setup_sec_identity

def calculate_debt_to_assets():
    setup_sec_identity()
    df = pd.read_csv("data/raw/company_status.csv")
    results = []

    for _, row in df.iterrows():
        financial_data = get_financial_data(row["cik"])
        fiscal_period_end = None
        if financial_data is not None:
            fiscal_period_end = financial_data.xb.period_of_report

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

        results.append({
            "ticker": row["ticker"],
            "fiscal_period_end": fiscal_period_end,
            "debt_to_assets_ratio": ratio,
        })

    pd.DataFrame(results).to_csv("data/processed/debt_to_assets_ratios.csv", index=False)

if __name__ == "__main__":
    calculate_debt_to_assets()
