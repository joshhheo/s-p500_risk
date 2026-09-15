# wikipedia needed for company selection and sector info
import requests
# abbreviation
import pandas as pd
# to convert html string to file-like object
import io

wiki_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
# header to get past 403 error
# header adds meta data to the request (not bot traffic)
# non-browser like strings work for wikipedia
headers = {"User-Agent": "plsgivemedata"}

wiki_pull = requests.get(wiki_url, headers=headers)

html_string = wiki_pull.text

# newer versions of pandas requires file-like object to read html tables
html_file = io.StringIO(html_string)

print(pd.read_html(html_file)[0])
