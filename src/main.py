import time

from company_status import create_company_status_csv
from generate_ratios import generate_ratios
from database.create_tables import create_tables
from database.companies_table_info import companies_table_info
from database.financials_table_info import financials_table_info
from database.refresh_view import refresh_view

def main():
    total_start = time.time()

    start = time.time()
    create_company_status_csv()
    print(f"Company status CSV: {time.time() - start:.2f} seconds")

    start = time.time()
    generate_ratios()
    print(f"Ratios CSV(api requests): {time.time() - start:.2f} seconds")

    start = time.time()
    create_tables()
    print(f"Create tables: {time.time() - start:.2f} seconds")

    start = time.time()
    companies_table_info()
    print(f"Load companies: {time.time() - start:.2f} seconds")

    start = time.time()
    financials_table_info()
    print(f"Load financials: {time.time() - start:.2f} seconds")

    start = time.time()
    refresh_view()
    print(f"Refresh view: {time.time() - start:.2f} seconds")

    print(f"Total runtime: {time.time() - total_start:.2f} seconds")


if __name__ == "__main__":
    main()