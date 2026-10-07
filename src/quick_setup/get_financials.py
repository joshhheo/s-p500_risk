from edgar import Company

def get_financial_data(ticker):
    company = Company(ticker)
    return company.get_financials()