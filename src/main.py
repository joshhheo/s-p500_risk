from sec_pull import sec_pull
from calculate_debt_to_assets_ratio import calculate_debt_to_assets
from merge_csv_info import merge_csv_info
from create_tables import create_tables
from companies_table_info import companies_table_info
from financials_table_info import financials_table_info
from read_sql import refresh_view
import time

def main():
    sec_pull()
    calculate_debt_to_assets()
    merge_csv_info()

    create_tables()
    companies_table_info()
    financials_table_info()
    refresh_view()

# only runs when ran directly
if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    elapsed = end - start
    print("finished")
    print(elapsed)
