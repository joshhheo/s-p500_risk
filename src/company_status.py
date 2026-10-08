import pandas as pd
from wiki_pull import get_wiki_dataframe
from quick_setup.get_financials import get_financial_data
from quick_setup.get_asset_liability_equity import get_asset_liability_equity
from quick_setup.setup_sec_identity import setup_sec_identity

def create_company_status_csv():
    setup_sec_identity()
    companies = get_wiki_dataframe()
    results = []

    for ticker in companies["Symbol"]:
        financial_data = get_financial_data(ticker)
        values = get_asset_liability_equity(financial_data)

        assets = values["assets"]
        liabilities = values["liabilities"]
        equity = values["equity"]

        results.append({
            "ticker": ticker,
            "has_assets": assets,
            "has_liabilities": liabilities,
            "has_equity": equity,
            "can_calculate_debt_to_assets": (
                assets is not None
                and (liabilities is not None or equity is not None)
            )
            or (
            liabilities is not None
            and (assets is not None or equity is not None)
            )
        })

    df = pd.DataFrame(results)
    df.to_csv("data/raw/company_status.csv", index=False)


if __name__ == "__main__":
    create_company_status_csv()
