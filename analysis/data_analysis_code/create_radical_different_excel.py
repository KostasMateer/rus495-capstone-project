"""
Radical Different Articles Data Processor

This script reads a JSON file containing articles with various sentiments and converts 
this data into a structured Excel file. It processes each article, extracts key 
information like sentiment, site name, search term, title, date, and URL, and organizes 
this data into a pandas DataFrame. The DataFrame is then saved as an Excel file for 
easier analysis and reporting.

Author: Kostas Mateer
Date: 16NOV23
RUS 495: Dr. Ewington
"""

import json
import pandas as pd

# Path to your JSON file
json_file_path = 'radical_different_articles.json'

# Load the JSON data
with open(json_file_path, 'r', encoding='utf-8') as file:
    radical_different_articles = json.load(file)

# Initialize a list to hold the article data
articles_data = []

# Iterate through the sentiment categories and their articles
for sentiment, articles in radical_different_articles.items():
    for article in articles:
        # Extract the required information from each article
        article_info = {
            "Sentiment Combination": sentiment,
            "Site Name": article.get("site name", ""),
            "Search Term": article.get("search term", {}).get("search term", ""),
            "Title": article.get("article", {}).get("title", ""),
            "Date": article.get("article", {}).get("date", ""),
            "URL": article.get("article", {}).get("url", "")
        }
        articles_data.append(article_info)

# Convert the data into a pandas DataFrame
df = pd.DataFrame(articles_data)

# Save the DataFrame to an Excel file
excel_file_path = 'radical_different_articles.xlsx'
df.to_excel(excel_file_path, index=False)

print(f"Data saved to {excel_file_path}")
