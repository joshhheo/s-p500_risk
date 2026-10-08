from edgar import Company

def get_financial_data(cik):
    company = Company(int(cik))
    return company.get_financials()