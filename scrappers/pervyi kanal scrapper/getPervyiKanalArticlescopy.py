"""
This script is designed to scrape news articles from the '1tv.ru' website based on a search term. 
It extracts details such as the article's title, date, and summary, then converts the date format 
to a standard 'mm/dd/yyyy' format and stores the information in a JSON file.

The scraping is performed by making HTTP requests to the website's search API and parsing the returned HTML content 
using regular expressions. The script includes pagination handling to fetch all relevant articles across multiple pages.

This file contains the following functions:
- `convert_date(russian_date)`: Converts a date from Russian format to a standard format.
- `fetchAllData(searchTerm, filename)`: Fetches all articles for a given search term and stores them in a JSON file.
- `write_JSON_file(jsonOBJ, file_name)`: Writes a given JSON object to a specified file.

Author: Kostas Mateer
Date: 11/07/23
RUS 495: Dr. Ewington
"""

import time
import requests
import re
import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Constants
MAX_CONCURRENT_REQUESTS = 10
MAX_RETRIES = 5
RETRY_DELAY = 2  # seconds
BATCH_DELAY = 0.1  # seconds
MAX_CONSECUTIVE_FAILURES = 20
JITTER = 1  # seconds

def delay(seconds):
    time.sleep(seconds)

def convert_date(russian_date):
    """
    Converts a date from Russian format to a standard format.
    """
    months = {
        'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05',
        'июня': '06', 'июля': '07', 'августа': '08', 'сентября': '09', 'октября': '10',
        'ноября': '11', 'декабря': '12'
    }
    day, month_name, year = russian_date.split()
    month = months.get(month_name)
    return f"{month}/{day}/{year}"

logging.basicConfig(level=logging.INFO)

def fetch_page_data(session, url, seen_urls):
    """
    Fetches data from a single page and processes articles.
    """
    try:
        response = session.get(url)
        response.raise_for_status()
        html_content = response.text
        PATTERN = r'<a class=\\"result\\" href=\\"(.*?)\\".*?<div class=\\"show-name[^\\]*\\">(.*?)<\\/div><div class=\\"date\\">(.*?)<\\/div><div class=\\"lead\\">(.*?)<\\/div>'
        matches = re.findall(PATTERN, html_content)

        page_articles = []
        for url, title, date, lead in matches:
            full_url = "https://www.1tv.ru" + url
            if full_url in seen_urls:
                print(f'seen url: {full_url}')
                continue
            seen_urls.add(full_url)
            new_date = convert_date(date)
            if int(new_date.split('/')[-1]) < 2014:
                print('older article')
                continue
            page_articles.append({
                "title": title,
                "subtitle": lead,
                "date": new_date,
                "url": full_url
            })
        return page_articles
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
        return []

def fetch_all_data(search_term, filename):
    """
    Fetches all articles related to a search term from 1tv.ru using concurrent requests.
    """
    articles_list = []
    seen_urls = set()
    session = requests.Session()
    offset = 0

    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_REQUESTS) as executor:
        while True:
            futures = []
            for _ in range(MAX_CONCURRENT_REQUESTS):
                api_url = f"https://www.1tv.ru/search.js?limit=100&offset={offset}&q=text%3A{search_term}"
                time.sleep(0.5)
                futures.append(executor.submit(fetch_page_data, session, api_url, seen_urls))
                offset += 1

            all_empty = True
            for future in as_completed(futures):
                page_articles = future.result()
                if page_articles:
                    articles_list.extend(page_articles)
                    all_empty = False
                else:
                    print('missed a page')

            if all_empty:
                break

            print(f"pages complete {offset}")
            delay(BATCH_DELAY)

    data = {
        "news site": "1tv.ru",
        "search term": search_term,
        "total articles": len(articles_list),
        "articles": articles_list
    }

    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"Total articles collected: {len(articles_list)}")
    return data

def write_JSON_file(jsonOBJ, file_name):
    """
    Write a JSON object to a file.
    
    Args:
        jsonOBJ (dict): The JSON object to write to the file.
        file_name (str): The name of the file to write to.
    """
    # Write to a JSON file
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(jsonOBJ, f, ensure_ascii=False, indent=2)

# def fetchAllData(searchTerm, filename):
#     """
#     Fetches all articles related to a search term from a website and stores the data in a JSON file.
    
#     Args:
#         searchTerm (str): The search term to query the website.
#         filename (str): The name of the JSON file to which the results will be saved.
        
#     Returns:
#         dict: A dictionary object containing all articles related to the search term.
#     """
#     pageNumber = 0
#     apiURL = f"https://www.1tv.ru/search.js?limit=100&offset={pageNumber}&q=text%3A{searchTerm}"
#     articles_list = []
#     seen_urls = set()  # A set to store already encountered URLs

#     html_content = requests.get(apiURL)
#     html_content = html_content.text
#     PATTERN = r'<a class=\\"result\\" href=\\"(.*?)\\".*?<div class=\\"show-name[^\\]*\\">(.*?)<\\/div><div class=\\"date\\">(.*?)<\\/div><div class=\\"lead\\">(.*?)<\\/div>'
    
#     # Find all matches in the string
#     matches = re.findall(PATTERN, html_content)
    
#     article_number = 1

#     FLAG2014 = 0 #flag for breaking the loops once older than 2014 is found
#     while True:
#         # Iterate over each match and store details in a dictionary
#         for i, match in enumerate(matches):
#             url, title, date, lead = match
#             full_url = "https://www.1tv.ru" + url 

#             # Check if the URL has already been processed
#             if full_url in seen_urls:
#                 continue  # Skip this article as it's a repeat

#              # Add the URL to the set of seen URLs
#             seen_urls.add(full_url)

#             new_date = convert_date(date)
#             if int(new_date.split('/')[-1]) < 2014:
#                 FLAG2014+=1
#                 continue
#             article_dict = {
#                 f"article{article_number}": {
#                     "title": title,
#                     "subtitle": lead,  # Since subtitle is not provided, it's left empty
#                     "date": new_date,
#                     "url": full_url  # Concatenate the base URL with the relative URL
#                 }
#             }
#             articles_list.append(article_dict)
#             article_number+=1
        
#         if FLAG2014 > 5:
#             break
#         pageNumber+=1
#         print(f"Loading page {pageNumber}")
#         apiURL = f"https://www.1tv.ru/search.js?limit=100&offset={pageNumber}&q=text%3A{searchTerm}"
#         html_content = requests.get(apiURL)
#         html_content = html_content.text

#         matches = re.findall(PATTERN, html_content)

#         if len(matches) == 0:
#             break

    
#     pervyikanalArticles = {
#         "news site": "pervyi kanal",
#         'search term' : f"{searchTerm}",
#         "articles": articles_list
#     }

#     write_JSON_file(pervyikanalArticles, filename)
#     return pervyikanalArticles