# unchecked test
import sys
sys.path.append("src")
import pandas as pd
from sqlalchemy import text

from get_financials import get_financial_data
from concept_search import get_value_via_concept
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from setup_sec import setup_sec_identity

setup_sec_identity()

TOL = 0.01 

load_dotenv()

connection_string = os.getenv("db_connection_string")
get_engine = create_engine(connection_string)

def get_equity(fd):
    # NCI-inclusive first: the identity needs total equity, not parent-only.
    v = get_value_via_concept(fd, "us-gaap:StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest")
    if v is not None:
        return v
    return get_value_via_concept(fd, "us-gaap:StockholdersEquity")

def check(ticker):
    try:
        fd = get_financial_data(ticker)
        a = get_value_via_concept(fd, "us-gaap:Assets")
        l = get_value_via_concept(fd, "us-gaap:Liabilities")
        e = get_equity(fd)
    except Exception as ex:
        return dict(ticker=ticker, status=f"error: {type(ex).__name__}: {ex}")
    row = dict(ticker=ticker, assets=a, liabilities=l, equity=e)
    if a is None or l is None or e is None:
        missing = [n for n, v in (("assets", a), ("liabilities", l), ("equity", e)) if v is None]
        row["status"] = "missing: " + ",".join(missing)
    else:
        row["diff_pct"] = (a - l - e) / abs(a)
        row["status"] = "ok" if abs(row["diff_pct"]) <= TOL else "FAIL"
    return row

if __name__ == "__main__":
    if len(sys.argv) > 1:
        tickers = sys.argv[1:]
    else:
        with get_engine.connect() as c:
            tickers = [r[0] for r in c.execute(text("SELECT ticker FROM companies ORDER BY ticker"))]
    rows = []
    for i, t in enumerate(tickers, 1):
        rows.append(check(t))
        print(f"[{i}/{len(tickers)}] {t}: {rows[-1]['status']}")
    df = pd.DataFrame(rows)
    df.to_csv("scratch/identity_check.csv", index=False)
    print("\n", df["status"].str.split(":").str[0].value_counts())
    print("\nFAIL / missing rows:\n", df[df["status"] != "ok"].to_string(index=False))