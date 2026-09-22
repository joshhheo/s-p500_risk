import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

connection_string = os.getenv("db_connection_string")

engine = create_engine(connection_string)

with engine.connect() as connection:
    # requests db to return 1
    result = connection.execute(text("SELECT 1"))
    # fetchone returns first row
    print(result.fetchone())