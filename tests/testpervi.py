import requests
import re
import json

html_content = requests.get("https://www.1tv.ru/search.js?limit=100&offset=100&q=text%3A%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F")
html_content = html_content.text

pattern = r'<a class=\\"result\\" href=\\"(.*?)\\".*?<div class=\\"show-name[^\\]*\\">(.*?)<\\/div><div class=\\"date\\">(.*?)<\\/div><div class=\\"lead\\">(.*?)<\\/div>'

# Find all matches in the string
matches = re.findall(pattern, html_content)

# List to store articles
articles_list = []

months = {
    'января': '01',
    'февраля': '02',
    'марта': '03',
    'апреля': '04',
    'мая': '05',
    'июня': '06',
    'июля': '07',
    'августа': '08',
    'сентября': '09',
    'октября': '10',
    'ноября': '11',
    'декабря': '12'
}

def convert_date(russian_date):
    # Split the date into components
    day, month_name, year = russian_date.split()
    # Map the Russian month name to a number
    month = months.get(month_name)
    # Construct the new date format
    return f"{month}/{day}/{year}"

# Iterate over each match and store details in a dictionary
for i, match in enumerate(matches):
    url, title, date, lead = match
    article_dict = {
        f"article{i + 1}": {
            "title": title,
            "subtitle": "",  # Since subtitle is not provided, it's left empty
            "date": convert_date(date),
            "url": "https://www.1tv.ru" + url  # Concatenate the base URL with the relative URL
        }
    }
    articles_list.append(article_dict)

# Dictionary for the entire JSON structure
json_structure = {
    "news site": "pervyi kanal",
    "articles": articles_list
}

# Write to a JSON file
with open('pervyikanalmobilizatsiya.json', 'w', encoding='utf-8') as f:
    json.dump(json_structure, f, ensure_ascii=False, indent=2)
