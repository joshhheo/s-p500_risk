# unchecked test
import os
import sys
sys.path.append("src")
 
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
 
from get_financials import get_financial_data
from concept_search import get_value_via_concept
from setup_sec import setup_sec_identity

setup_sec_identity()

TOL = 0.001  # 0.1%; these should be the same number, so this is already generous
 
load_dotenv()
engine = create_engine(os.getenv("db_connection_string"))
 
 
def check(ticker):
    try:
        fd = get_financial_data(ticker)
        a = get_value_via_concept(fd, "us-gaap:Assets")
        lae = get_value_via_concept(fd, "us-gaap:LiabilitiesAndStockholdersEquity")
    except Exception as ex:
        return dict(ticker=ticker, status=f"error: {type(ex).__name__}: {ex}")
    row = dict(ticker=ticker, assets=a, liab_and_equity=lae)
    if a is None and lae is None:
        row["status"] = "both_missing"
    elif a is None:
        row["status"] = "assets_missing"
    elif lae is None:
        row["status"] = "lae_missing"
    else:
        row["diff_pct"] = (a - lae) / abs(a)
        row["status"] = "agree" if abs(row["diff_pct"]) <= TOL else "DISAGREE"
    return row
 
 
if __name__ == "__main__":
    if len(sys.argv) > 1:
        tickers = sys.argv[1:]
    else:
        with engine.connect() as c:
            tickers = [r[0] for r in c.execute(text("SELECT ticker FROM companies ORDER BY ticker"))]
    rows = []
    for i, t in enumerate(tickers, 1):
        rows.append(check(t))
        print(f"[{i}/{len(tickers)}] {t}: {rows[-1]['status']}")
    df = pd.DataFrame(rows)
    df.to_csv("scratch/assets_check.csv", index=False)
    print("\n", df["status"].str.split(":").str[0].value_counts())
    bad = df[df["status"] != "agree"]
    print("\nNot-agreeing rows:\n", bad.to_string(index=False))
