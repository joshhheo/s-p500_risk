import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

connection_string = os.getenv("db_connection_string")
engine = create_engine(connection_string)

# store queries as string
create_companies_table = """
CREATE TABLE comapnies(
    ticker TEXT PRIMARY KEY,
    company_name TEXT,
    sector TEXT
    );
"""

# with statement automatically closes connnection
with engine.connect() as connection:
    connection.execute(text(create_companies_table))
    connection.commit()

print("finished")