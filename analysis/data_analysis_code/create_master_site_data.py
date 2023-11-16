"""
News Data Aggregator

This script aggregates news article data from various JSON files. It compiles
information about the total number of articles, sentiments (negative, neutral, positive),
and detailed sentiment analysis based on different models. The aggregated data
is then stored in a master JSON file for further analysis or reporting.

The script processes multiple news sources, updates the master data structure with
sentiment analysis from each source, and handles potential errors in file handling
and data processing.

Author: Kostas Mateer
Date: 15NOV23
RUS 495: Dr. Ewington
"""

import json

# Paths to the JSON files containing news articles data
MEDUZA_path = 'MEDUZA_articles_organized.json'
NOVAYA_GAZETA_path = 'NOVAYA_GAZETA_articles_organized.json'
PERVYI_KANAL_path = 'PERVYI_KANAL_articles_organized.json'
TASS_path = 'TASS_articles_organized.json'

# Initialize an empty structure for the master data
master_data = {
    "total articles of all sites": 0,
    "total sentiment of all sites": {
        "NEGATIVE": 0,
        "NEUTRAL": 0,
        "POSITIVE": 0
    },
    "total sentiment from all articles by modal": {
        "RuSentiment Model Totals": {"NEGATIVE": 0, "NEUTRAL": 0, "POSITIVE": 0},
        "Kaggle News Model Totals": {"NEGATIVE": 0, "NEUTRAL": 0, "POSITIVE": 0},
        "General Model Totals": {"NEGATIVE": 0, "NEUTRAL": 0, "POSITIVE": 0}
    },
    "sentiment by term": {}
}

def update_master_data_from_file(file_path, master_data):
    """
    Updates the master data dictionary with data from a given JSON file.

    Args:
    file_path (str): The path to the JSON file containing news data.
    master_data (dict): The master dictionary to be updated with news data.

    The function reads data from the specified file and updates the master_data
    dictionary accordingly. It handles FileNotFoundError, JSONDecodeError, and KeyError.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            news_data = json.load(file)

        # Update total articles and sentiment totals
        master_data['total articles of all sites'] += news_data['total articles']

        for sentiment in ["NEGATIVE", "NEUTRAL", "POSITIVE"]:
            master_data["total sentiment of all sites"][sentiment] += news_data['total sentiment from all articles'][sentiment]

            for model in news_data["total sentiment from all articles by modal"]:
                master_data["total sentiment from all articles by modal"][model][sentiment] += news_data["total sentiment from all articles by modal"][model][sentiment]

        # Update sentiment by term
        for term, term_data in news_data["sentiment by term"].items():
            if term not in master_data["sentiment by term"]:
                master_data["sentiment by term"][term] = {
                    "total articles": 0,
                    "Term Sentiment Totals": {"NEGATIVE": 0, "NEUTRAL": 0, "POSITIVE": 0},
                    "Specific Model Totals": {
                        "RuSentiment Model Totals": {"NEGATIVE": 0, "NEUTRAL": 0, "POSITIVE": 0},
                        "Kaggle News Model Totals": {"NEGATIVE": 0, "NEUTRAL": 0, "POSITIVE": 0},
                        "General Model Totals": {"NEGATIVE": 0, "NEUTRAL": 0, "POSITIVE": 0}
                    }
                }

            master_data["sentiment by term"][term]["total articles"] += term_data["total articles"]

            for sentiment in ["NEGATIVE", "NEUTRAL", "POSITIVE"]:
                master_data["sentiment by term"][term]["Term Sentiment Totals"][sentiment] += term_data["Term Sentiment Totals"][sentiment]

                for model in term_data["Specific Model Totals"]:
                    master_data["sentiment by term"][term]["Specific Model Totals"][model][sentiment] += term_data["Specific Model Totals"][model][sentiment]

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
    except KeyError as e:
        print(f"Missing expected key {e} in data from file: {file_path}")

# List of file paths
file_paths = [MEDUZA_path, NOVAYA_GAZETA_path, PERVYI_KANAL_path, TASS_path]

# Process each file
for path in file_paths:
    update_master_data_from_file(path, master_data)

# Write the compiled master data to a JSON file
with open('master_data.json', 'w', encoding='utf-8') as f:
    json.dump(master_data, f, ensure_ascii=False, indent=2)
