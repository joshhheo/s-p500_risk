import pandas as pd
from wiki_pull import get_wiki_dataframe

def create_company_status_csv():
    companies = get_wiki_dataframe()
    results = []

    for _, company in companies.iterrows():
        results.append({
            "ticker": company["Symbol"],
            "cik": int(company["CIK"]),
            "company_name": company["Security"],
            "sector": company["GICS Sector"],
        })

    df = pd.DataFrame(results)
    df.to_csv("data/company_status.csv", index=False)


if __name__ == "__main__":
    create_company_status_csv()