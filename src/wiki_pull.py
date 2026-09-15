# wikipedia needed for company selection and sector info
import requests
# abbreviation
import pandas as pd

wiki_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
# header to get past 403 error
# header adds meta data to the request (not bot traffic)
# non-browser like strings work for wikipedia
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

wiki_pull = requests.get(wiki_url, headers=headers)

wiki_pull.status_code


html_string = wiki_pull.text

print(pd.read_html(html_string))