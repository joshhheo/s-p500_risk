def get_value(financial_data, concept_name):
    rows = financial_data.xb.query().by_concept(
        concept_name,
        exact=True
    ).to_dataframe()

    rows = rows[rows["is_dimensioned"] == False]

    rows = rows.sort_values("period_instant", ascending=False)

    if rows.empty:
        return None

    return rows.iloc[0]["numeric_value"]


# gets the 3 values for one company
def get_balance_sheet_values(financial_data):
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
        "equity": equity,
    }


if __name__ == "__main__":
    import setup_sec
    from get_financials import get_financial_data
    import pandas as pd

    setup_sec.setup_sec_identity()

    get_financial_data("AAPL")

    df = pd.DataFrame([
        get_balance_sheet_values(get_financial_data("AAPL"))
    ])

    print(df)