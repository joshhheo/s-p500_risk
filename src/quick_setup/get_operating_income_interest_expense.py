def get_annual_value(financial_data, concept_name, period_start, period_end):
    if financial_data is None:
        return None

    facts = (
        financial_data.xb.query()
        .by_concept(concept_name, exact=True)
        .to_dataframe()
    )

    if facts.empty:
        return None

    matches = facts[facts["is_dimensioned"] == False]

    matches = matches[
        matches["period_start"].astype(str).str[:10] == period_start
    ]

    matches = matches[
        matches["period_end"].astype(str).str[:10] == period_end
    ]

    matches = matches.dropna(subset=["numeric_value"])

    if matches.empty:
        return None

    return matches.iloc[0]["numeric_value"]


def get_operating_income_interest_expense(
    financial_data, period_start, period_end
):
    operating_income = get_annual_value(
        financial_data,
        "us-gaap:OperatingIncomeLoss",
        period_start,
        period_end,
    )

    interest_expense = get_annual_value(
        financial_data,
        "us-gaap:InterestExpense",
        period_start,
        period_end,
    )

    if interest_expense is None:
        operating_interest = get_annual_value(
            financial_data,
            "us-gaap:InterestExpenseOperating",
            period_start,
            period_end,
        )

        nonoperating_interest = get_annual_value(
            financial_data,
            "us-gaap:InterestExpenseNonoperating",
            period_start,
            period_end,
        )

        if operating_interest is not None and nonoperating_interest is not None:
            interest_expense = operating_interest + nonoperating_interest

    return {
        "operating_income": operating_income,
        "interest_expense": interest_expense,
    }