from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

connection_string = os.getenv("db_connection_string")

engine = create_engine(connection_string)

df = pd.read_csv("data/processed/debt_to_assets_ratios.csv")

upsert_query = """
INSERT INTO financials
