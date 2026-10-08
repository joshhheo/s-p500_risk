import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


def companies_table_info():
    load_dotenv()
    engine = create_engine(os.getenv("db_connection_string"))

    companies = pd.read_csv("data/raw/company_status.csv")

    upsert_query = """
    INSERT INTO companies (ticker, company_name, sector)
    VALUES (:ticker, :company_name, :sector)
    ON CONFLICT (ticker)
    DO UPDATE SET
        company_name = EXCLUDED.company_name,
        sector = EXCLUDED.sector;
    """

    with engine.begin() as connection:
        for _, row in companies.iterrows():
            connection.execute(text(upsert_query), {
                "ticker": row["ticker"],
                "company_name": row["company_name"],
                "sector": row["sector"],
            })
