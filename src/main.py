from sec_pull import sec_pull
from calculate_debt_to_assets_ratio import calculate_debt_to_assets
from merge_csv_info import merge_csv_info
from create_tables import create_tables
from companies_table_info import companies_table_info
from financials_table_info import financials_table_info
from read_sql import refresh_view
import time

def main():
    startapi = time.time()
    sec_pull()
    elapsedapi = time.time() - startapi
    print(f"api+wiki time(one csv):{elapsedapi}")
    startcsv = time.time()
    calculate_debt_to_assets()
    merge_csv_info()
    elapsedcsv = time.time() - startcsv
    print(f"csv+calculate time:{elapsedcsv}")
    startsql = time.time()
    create_tables()
    companies_table_info()
    financials_table_info()
    refresh_view()
    elapsedsql = time.time() - startsql
    print(f"sql time:{elapsedsql}")

# only runs when ran directly
if __name__ == "__main__":
    main()
    print("finished")
