import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from wiki_pull import get_wiki_dataframe

load_dotenv()
engine = create_engine(os.getenv("db_connection_string"))

wiki_df = get_wiki_dataframe()
wiki_df = wiki_df.rename(columns={
    "Symbol": "ticker",
    "Security": "company_name",
    "GICS Sector": "sector",
})

# inserts new row if not exist, or updates existing row
# parameterization to avoid apostrophes breaking
upsert_query = """
INSERT INTO companies (ticker, company_name, sector)
VALUES (:ticker, :company_name, :sector)
ON CONFLICT (ticker)
DO UPDATE SET
    company_name = EXCLUDED.company_name,
    sector = EXCLUDED.sector;
"""

with engine.connect() as connection:
    for _, row in wiki_df.iterrows():
        connection.execute(text(upsert_query), {
            "ticker": row["ticker"],
            "company_name": row["company_name"],
            "sector": row["sector"],
        })
    connection.commit()
