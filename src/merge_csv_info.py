import pandas as pd
import sys
sys.path.append("data")

status_df = pd.read_csv("data/raw/debt_to_assets_status.csv")
ratios_df = pd.read_csv("data/processed/debt_to_assets_ratios.csv")

merged_df = ratios_df.merge(status_df[["ticker", "liabilities_method"]], on="ticker")

merged_df.to_csv("data/processed/debt_to_assets_ratios.csv", index=False)
