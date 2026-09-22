import sys
sys.path.append("src")

from edgar import Company
import pandas as pd
from setup_sec import setup_sec_identity

setup_sec_identity()

df = pd.read_csv("data/raw/debt_to_assets_status.csv")
candidates = df[df["liabilities_missing"] == True]["ticker"]

multirow_dimensioned_only = []

for ticker in candidates:
    company = Company(ticker)
    financial_data = company.get_financials()
    if financial_data is None:
        continue

    result = financial_data.xb.query().by_concept("us-gaap:Liabilities", exact=True).to_dataframe()

    if len(result) > 1 and (result["is_dimensioned"] == True).all():
        multirow_dimensioned_only.append(ticker)

print(len(multirow_dimensioned_only))
print(multirow_dimensioned_only)

if multirow_dimensioned_only:
    print("use ticker to manually test sec_pull fallback")
else:
    print("no company with multirow dataset and only dimensioned")
