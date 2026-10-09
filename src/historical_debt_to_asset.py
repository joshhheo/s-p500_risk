import pandas as pd
from edgar import Company

from quick_setup.setup_sec_identity import setup_sec_identity
from quick_setup.get_asset_liability_equity import get_asset_liability_equity


def create_historical_ratios():
    setup_sec_identity()

    companies = companies = pd.read_csv("data/raw/company_status.csv")

    results = []

    # amendments can be non-financial
    for _, company in companies.iterrows():
        ticker = company["ticker"]
        cik = int(company["cik"])
        filings = Company(cik).get_filings(
            form="10-K",
            amendments=False,
        )

        periods = []

        for filing in filings:
            if not filing.period_of_report:
                continue

            # date format is YYYY-MM-DD
            period_end = str(filing.period_of_report)[:10]

            # Don't calculate the same annual period twice
            if period_end in periods:
                continue

            periods.append(period_end)

            # obj parses the filings into object
            annual_report = filing.obj()
            financial_data = None
            if annual_report is not None:
                financial_data = annual_report.financials

            values = get_asset_liability_equity(financial_data, period_end)

            assets = values["assets"]
            liabilities = values["liabilities"]
            equity = values["equity"]

            if (
                liabilities is None
                and assets is not None
                and equity is not None
            ):
                liabilities = assets - equity

            if (
                assets is None
                and liabilities is not None
                and equity is not None
            ):
                assets = liabilities + equity

            ratio = None
            if (
                assets is not None
                and liabilities is not None
            ):
                ratio = liabilities / assets

            results.append({
                "ticker": ticker,
                "fiscal_period_end": period_end,
                "debt_to_assets_ratio": ratio,
            })

            if len(periods) == 5:
                break

    pd.DataFrame(results).to_csv(
        "data/processed/historical_debt_to_assets_ratios.csv",
        index=False,
    )


if __name__ == "__main__":
    create_historical_ratios()