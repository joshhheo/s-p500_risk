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

    # assets fallback: current + noncurrent
    if assets is None:
        current_assets = get_value(
            financial_data, "us-gaap:AssetsCurrent", fiscal_period_end
        )
        noncurrent_assets = get_value(
            financial_data, "us-gaap:AssetsNoncurrent", fiscal_period_end
        )

        if current_assets is not None and noncurrent_assets is not None:
            assets = current_assets + noncurrent_assets

    # liabilities fallback: current + noncurrent
    if liabilities is None:
        current_liabilities = get_value(
            financial_data, "us-gaap:LiabilitiesCurrent", fiscal_period_end
        )
        noncurrent_liabilities = get_value(
            financial_data, "us-gaap:LiabilitiesNoncurrent", fiscal_period_end
        )

        if current_liabilities is not None and noncurrent_liabilities is not None:
            liabilities = current_liabilities + noncurrent_liabilities

    # assets fallback: liabilities + equity
    if assets is None:
        assets = get_value(
            financial_data,
            "us-gaap:LiabilitiesAndStockholdersEquity",
            fiscal_period_end,
        )

    # fallback for assets or liabilities: equity
    if assets is None or liabilities is None:
        equity = get_value(
            financial_data,
            "us-gaap:StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest",
            fiscal_period_end,
        )
        # fallback for equity: parent + noncontrolling
        if equity is None:
            parent_equity = get_value(
                financial_data, "us-gaap:StockholdersEquity", fiscal_period_end
            )
            noncontrolling_equity = get_value(
                financial_data, "us-gaap:MinorityInterest", fiscal_period_end
            )

            if parent_equity is not None and noncontrolling_equity is not None:
                equity = parent_equity + noncontrolling_equity

        temporary_equity = get_value(
            financial_data,
            "us-gaap:TemporaryEquityCarryingAmountIncludingPortionAttributableToNoncontrollingInterests",
            fiscal_period_end,
        )

        if equity is not None and temporary_equity is not None:
            if liabilities is None and assets is not None:
                liabilities = assets - equity - temporary_equity

            if assets is None and liabilities is not None:
                assets = liabilities + equity + temporary_equity

    return {"assets": assets, "liabilities": liabilities}
