def get_value(financial_data, concept_name):

    if financial_data is None:
        return None

    rows = financial_data.xb.query().by_concept(concept_name, exact=True)

    df = rows.to_dataframe()

    df = df[df["is_dimensioned"] == False]

    df = df.sort_values("period_instant", ascending=False)

    if df.empty:
        return None

    return df.iloc[0]["numeric_value"]


# gets the 3 values for one company
def get_asset_liability_equity(financial_data):
    equity = get_value(
        financial_data,
        "us-gaap:StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"
    )

    if equity is None:
        equity = get_value(
            financial_data,
            "us-gaap:StockholdersEquity"
        )

    return {
        "assets": get_value(financial_data, "us-gaap:Assets"),
        "liabilities": get_value(financial_data, "us-gaap:Liabilities"),
        "equity": equity
    }
