import pandas as pd

from wiki_pull import get_wiki_dataframe
from get_financials import get_financial_data
from get_balance_sheet import get_debt_to_assets_ratio_values


def validate_sp500_companies():

    companies = get_wiki_dataframe()

    results = []

    for _, company in companies.iterrows():

        ticker = company["Symbol"]
        name = company["Security"]
        sector = company["GICS Sector"]

        print(f"Processing {ticker}...")

        # Get SEC financial data
        financial_data = get_financial_data(ticker)

        # Whole filing/data missing
        if financial_data is None:
            results.append({
                "ticker": ticker,
                "company": name,
                "sector": sector,
                "missing_filing": True,
                "missing_assets": True,
                "missing_liabilities": True,
                "missing_equity": True,
                "can_calculate_debt_to_assets": False
            })

            continue

        # Get balance sheet values
        values = get_debt_to_assets_ratio_values(financial_data)

        assets = values["assets"]
        liabilities = values["liabilities"]
        equity = values["equity"]

        # Determine whether ratio can be calculated
        can_calculate_ratio = (
            assets is not None
            and liabilities is not None
            and assets != 0
        )

        results.append({
            "ticker": ticker,
            "company": name,
            "sector": sector,
            "missing_filing": False,
            "missing_assets": assets is None,
            "missing_liabilities": liabilities is None,
            "missing_equity": equity is None,
            "can_calculate_debt_to_assets": can_calculate_ratio
        })

    return pd.DataFrame(results)


if __name__ == "__main__":

    df = validate_sp500_companies()

    df.to_csv(
        "sp500_balance_sheet_validation.csv",
        index=False
    )

    print(df)