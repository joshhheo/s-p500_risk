from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import pandas as pd

def financials_table_info():
    load_dotenv()

    connection_string = os.getenv("db_connection_string")

    engine = create_engine(connection_string)

    df = pd.read_csv("data/processed/debt_to_assets_ratios.csv")
    # gets rid of empty financial info companies
    df = df.dropna(subset=["fiscal_period_end", "debt_to_assets_ratio"])

    upsert_query = """
    INSERT INTO financials (ticker, fiscal_period_end, debt_to_assets_ratio, liabilities_method)
    VALUES (:ticker, :fiscal_period_end, :debt_to_assets_ratio, :liabilities_method)
    ON CONFLICT (ticker, fiscal_period_end)
    DO UPDATE SET
        debt_to_assets_ratio = EXCLUDED.debt_to_assets_ratio,
        liabilities_method = EXCLUDED.liabilities_method;
    """

    with engine.connect() as connection:
        for _, row in df.iterrows():
            connection.execute(text(upsert_query), {
                "ticker": row["ticker"],
                "fiscal_period_end": row["fiscal_period_end"],
                "debt_to_assets_ratio": row["debt_to_assets_ratio"],
                "liabilities_method": row["liabilities_method"]
            })
        connection.commit()
