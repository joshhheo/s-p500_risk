def get_value(financial_data, concept_name):

    if financial_data is None:
        return None

    df = (financial_data.xb.query().by_concept(concept_name, exact=True).to_dataframe())
    if df.empty:
        return None

    dimensioned = df[df["is_dimensioned"] == False]
    if dimensioned.empty:
        return None
    
    sorted_dimentioned = dimensioned.sort_values("period_instant", ascending=False)
    latest_dimentioned = sorted_dimentioned.iloc[0]
    values = latest_dimentioned["numeric_value"]
    
    return values


def get_asset_liability_equity(financial_data):
    assets = get_value(financial_data, "us-gaap:Assets")

    liabilities = get_value(financial_data, "us-gaap:Liabilities")
    if liabilities is None:
        current = get_value(financial_data, "us-gaap:LiabilitiesCurrent")
        noncurrent = get_value(financial_data, "us-gaap:LiabilitiesNoncurrent")
        if current is not None and noncurrent is not None:
            liabilities = current + noncurrent

    equity_and_nci = "us-gaap:StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"
    equity = get_value(financial_data, equity_and_nci)
    if equity is None:
        parent = get_value(financial_data, "us-gaap:StockholdersEquity")
        noncontrolling = get_value(financial_data, "us-gaap:MinorityInterest")
        if parent is not None:
            equity = parent
            if noncontrolling is not None:
                equity += noncontrolling

    return {"assets": assets, "liabilities": liabilities, "equity": equity}
