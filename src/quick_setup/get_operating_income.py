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

    values = matches["numeric_value"].dropna().unique()
    if len(values) != 1:
        return None

    return values[0]


def get_operating_income(financial_data, period_start, period_end):
    operating_income = get_annual_value(
        financial_data, "us-gaap:OperatingIncomeLoss", period_start, period_end
    )

    if operating_income is not None:
        return operating_income

    gross_profit = get_annual_value(
        financial_data, "us-gaap:GrossProfit", period_start, period_end
    )
    operating_expenses = get_annual_value(
        financial_data, "us-gaap:OperatingExpenses", period_start, period_end
    )

    # Assumes OperatingExpenses covers all operating costs below gross profit.
    if gross_profit is not None and operating_expenses is not None:
        return gross_profit - operating_expenses

    return None