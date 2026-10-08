# unchecked test
import sys
sys.path.append("src")

from quick_setup.setup_sec_identity import setup_sec_identity
from quick_setup.get_financials import get_financial_data

setup_sec_identity()
financial_data = get_financial_data("AMZN")

if financial_data is None:
    print("No financial data")
else:
    concepts = [
        "Assets",
        "Liabilities",
        "LiabilitiesCurrent",
        "LiabilitiesNoncurrent",
        "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest",
        "StockholdersEquity",
        "MinorityInterest",
    ]

    for concept in concepts:
        print(f"\n{concept}")

        df = (
            financial_data.xb.query()
            .by_concept(f"us-gaap:{concept}", exact=True)
            .to_dataframe()
        )

        if df.empty:
            print("No matching facts")
            continue

        print(
            df[["period_instant", "numeric_value", "is_dimensioned"]]
            .sort_values("period_instant", ascending=False)
            .to_string(index=False)
        )