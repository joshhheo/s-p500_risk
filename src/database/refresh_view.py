import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

def refresh_view():

    load_dotenv()
    connection_string = os.getenv("db_connection_string")
    engine = create_engine(connection_string)

    with open("src/database/sql/sector_leverage.sql") as f:
        view_query = f.read()
    with engine.begin() as connection:
        connection.execute(text(view_query))
