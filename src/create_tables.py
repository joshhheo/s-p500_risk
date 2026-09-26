import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

connection_string = os.getenv("db_connection_string")
engine = create_engine(connection_string)

# store queries as string
# primary key to avoid repeating constants
create_companies_table = """
CREATE TABLE companies (
    ticker TEXT PRIMARY KEY,
    company_name TEXT,
    sector TEXT
);
"""

# composite key allows duplicate tickers
create_financials_table = """
CREATE TABLE financials (
    ticker TEXT REFERENCES companies(ticker),
    fiscal_period_end DATE,
    debt_to_assets_ratio NUMERIC,
    liabilities_method TEXT
    PRIMARY KEY (ticker, fiscal_period_end)
);
"""

# with statement to close connection automatically
with engine.connect() as connection:
    connection.execute(text(create_companies_table))
    connection.execute(text(create_financials_table))
    connection.commit()
 
print("finished")
