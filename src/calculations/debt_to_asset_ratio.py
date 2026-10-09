from quick_setup.get_asset_liability_equity import get_asset_liability_equity

def calculate_debt_to_assets(financial_data, fiscal_period_end):
    values = get_asset_liability_equity(financial_data, fiscal_period_end)

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
    if assets is not None and liabilities is not None:
        ratio = liabilities / assets

    return ratio