# fiscal period paramter TEST: multiyear data
def get_value(financial_data, concept_name, fiscal_period_end = None):
    
    if financial_data is None:
        return None

    df = (financial_data.xb.query().by_concept(concept_name, exact=True).to_dataframe())
    if df.empty:
        return None
    
    dimensioned = df[df["is_dimensioned"] == False]

    # TEST: multiyear data
    if fiscal_period_end is not None:
        dimensioned = dimensioned[
        dimensioned["period_instant"].astype(str).str[:10]
        == fiscal_period_end
    ]
        
    if dimensioned.empty:
        return None
    
    sorted_dimentioned = dimensioned.sort_values("period_instant", ascending=False)
    latest_dimentioned = sorted_dimentioned.iloc[0]
    values = latest_dimentioned["numeric_value"]
    
    return values

# fiscal period paramter TEST: multiyear data
def get_asset_liability_equity(financial_data, fiscal_period_end = None):
    assets = get_value(financial_data, "us-gaap:Assets", fiscal_period_end)

    liabilities = get_value(financial_data, "us-gaap:Liabilities", fiscal_period_end)
    if liabilities is None:
        current = get_value(financial_data, "us-gaap:LiabilitiesCurrent", fiscal_period_end)
        noncurrent = get_value(financial_data, "us-gaap:LiabilitiesNoncurrent", fiscal_period_end)
        if current is not None and noncurrent is not None:
            liabilities = current + noncurrent

    equity_and_nci = "us-gaap:StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"
    equity = get_value(financial_data, equity_and_nci, fiscal_period_end)
    if equity is None:
        parent = get_value(financial_data, "us-gaap:StockholdersEquity", fiscal_period_end)
        noncontrolling = get_value(financial_data, "us-gaap:MinorityInterest", fiscal_period_end)
        if parent is not None:
            equity = parent
            if noncontrolling is not None:
                equity += noncontrolling

    return {"assets": assets, "liabilities": liabilities, "equity": equity}
