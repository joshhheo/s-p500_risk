# unchecked test
import sys

sys.path.append("src")

from edgar import Company
from quick_setup.setup_sec_identity import setup_sec_identity


setup_sec_identity()

ticker = "MSFT"

filing = Company(ticker).get_filings(
    form="10-K",
    amendments=False,
).latest()

print(filing)

period_end = str(filing.period_of_report)[:10]
financial_data = filing.obj().financials

print(financial_data.income_statement())

# Inspect facts throughout the filing, including the notes.
facts = financial_data.xb.query().to_dataframe()

# Find possible operating-income and interest-related facts.
matches = (
    facts["concept"].str.contains(
        "OperatingIncome|Interest",
        case=False,
        na=False,
    )
    | facts["label"].str.contains(
        r"operating (income|loss)|interest",
        case=False,
        na=False,
    )
)

candidates = facts[
    matches
    & (facts["is_dimensioned"] == False)
    & (facts["period_end"].astype(str).str[:10] == period_end)
]

columns = [
    "concept",
    "label",
    "period_start",
    "period_end",
    "numeric_value",
]

print("\nCandidate facts ending on:", period_end)

print(
    candidates[columns]
    .sort_values(["concept", "period_start"])
    .to_string(index=False)
)