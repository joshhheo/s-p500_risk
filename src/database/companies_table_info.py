import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from wiki_pull import get_wiki_dataframe

def companies_table_info():
    load_dotenv()
    engine = create_engine(os.getenv("db_connection_string"))

    wiki_df = get_wiki_dataframe()
    wiki_df = wiki_df.rename(columns={
        "Symbol": "ticker",
        "Security": "company_name",
        "GICS Sector": "sector",
    })

    # inserts new row if not exist, or updates existing row
    # parameterization to avoid apostrophes breaking query
    upsert_query = """
    INSERT INTO companies (ticker, company_name, sector)
    VALUES (:ticker, :company_name, :sector)
    ON CONFLICT (ticker)
    DO UPDATE SET
        company_name = EXCLUDED.company_name,
        sector = EXCLUDED.sector;
    """

    current_tickers = wiki_df["ticker"].tolist()
    # delete financials first because it is dependant
    delete_financials = "DELETE FROM financials WHERE ticker <> ALL(:tickers);"
    delete_companies = "DELETE FROM companies WHERE ticker <> ALL(:tickers);"

    with engine.connect() as connection:
        for _, row in wiki_df.iterrows():
            connection.execute(text(upsert_query), {
                "ticker": row["ticker"],
                "company_name": row["company_name"],
                "sector": row["sector"],
            })

        connection.execute(text(delete_financials), {"tickers": current_tickers})
        connection.execute(text(delete_companies), {"tickers": current_tickers})
        connection.commit()

    