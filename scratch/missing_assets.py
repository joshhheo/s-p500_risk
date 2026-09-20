import pandas as pd
from edgar import Company, set_identity
import os
from dotenv import load_dotenv

load_dotenv()

user_agent = os.getenv("SEC_user_agent")

set_identity(user_agent)

df = pd.read_csv("data/raw/leverage_status.csv")

assets_missing = df[df["assets_missing"] == True]
no_filing = df[df["has_filing"] == False]

# assets = None indicates no filing
# assets = False indicates yes filing but no assets
print(len(assets_missing))
print(len(no_filing))
print(no_filing["ticker"])
