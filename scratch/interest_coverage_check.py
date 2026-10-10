# unchecked test
import sys


sys.path.append("src")

from quick_setup.get_operating_income_interest_expense import (
    get_operating_income_interest_expense,
)
from edgar import Company
from quick_setup.setup_sec_identity import setup_sec_identity


setup_sec_identity()

ticker = "WMT"

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

period_start = None

for period in financial_data.xb.reporting_periods:
    if period["type"] != "duration":
        continue

    if period["period_type"] != "Annual":
        continue

    if period["end_date"] != period_end:
        continue

    period_start = period["start_date"]
    break

print("Annual start:", period_start)
print("Annual end:", period_end)

if period_start is not None:
    values = get_operating_income_interest_expense(
        financial_data,
        period_start,
        period_end,
    )

    print(values)