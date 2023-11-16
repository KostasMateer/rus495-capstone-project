# from getPervyiKanalArticles import fetchAllData
from getPervyiKanalArticlescopy import fetch_all_data

SEARCH_TERM = "в оенная служба по контракту"

data = fetch_all_data(SEARCH_TERM, f"{SEARCH_TERM}pervyikanal.json")
print('sweet')