from wiki_pull import get_wiki_dataframe
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

connection_string = os.getenv("db_connection_string")

engine = create_engine(connection_string)

wiki_df = get_wiki_dataframe()
wiki_df = wiki_df.rename(columns={"Symbol": "ticker", "Security": "company_name", "GICS Sector": "sector"})

wiki_df.to_sql("companies", engine, if_exists="append", index=False)
