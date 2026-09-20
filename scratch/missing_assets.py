import pandas as pd

df = pd.read_csv("data/raw/leverage_status.csv")

assets_missing = df[df["assets_missing"] == True]
no_filing = df[df["has_filing"] == False]

# assets = None indicates no filing
# assets = False indicates yes filing but no assets
print(len(assets_missing))
print(len(no_filing))
print(no_filing["ticker"])
