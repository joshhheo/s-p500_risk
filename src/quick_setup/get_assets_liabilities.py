def get_value(financial_data, concept_name, fiscal_period_end):
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
        matches["period_instant"].astype(str).str[:10]
        == fiscal_period_end
    ]

    matches = matches.dropna(subset=["numeric_value"])

    if matches.empty:
        return None

    return matches.iloc[0]["numeric_value"]


def get_assets_liabilities(financial_data, fiscal_period_end):
    assets = get_value(
        financial_data, "us-gaap:Assets", fiscal_period_end
    )

    liabilities = get_value(
        financial_data, "us-gaap:Liabilities", fiscal_period_end
    )

    if liabilities is None:
        current = get_value(
            financial_data,
            "us-gaap:LiabilitiesCurrent",
            fiscal_period_end,
        )

        noncurrent = get_value(
            financial_data,
            "us-gaap:LiabilitiesNoncurrent",
            fiscal_period_end,
        )

        if current is not None and noncurrent is not None:
            liabilities = current + noncurrent

    return {"assets": assets, "liabilities": liabilities}