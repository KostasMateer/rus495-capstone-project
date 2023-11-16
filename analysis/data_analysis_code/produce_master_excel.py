"""
News Data Export to Excel

This script takes sentiment analysis data from multiple news sites, which is stored 
in JSON format, and compiles it into a comprehensive Excel workbook. The workbook 
includes a master summary sheet with overall sentiment counts, individual sheets for 
each news site with detailed sentiment counts, and separate sheets for sentiment 
analysis based on specific search terms.

The sentiment data is categorized into negative, neutral, and positive sentiments, 
and includes data from different sentiment analysis models.

Author: Kostas Mateer
Date: 16NOV23
RUS 495: Dr. Ewington
"""

import pandas as pd
import json

# Load master data from JSON file
with open('master_data.json', 'r', encoding='utf-8') as file:
    master_data = json.load(file)

# Paths to the JSON files containing site-specific data
site_data_files = [
    'MEDUZA_articles_organized.json', 
    'NOVAYA_GAZETA_articles_organized.json',
    'PERVYI_KANAL_articles_organized.json',
    'TASS_articles_organized.json'
]
site_data_list = []

# Load site-specific data from files
for file_name in site_data_files:
    with open(file_name, 'r', encoding='utf-8') as file:
        site_data = json.load(file)
        site_data_list.append(site_data)

# Write data to an Excel workbook
with pd.ExcelWriter('news_data.xlsx', engine='xlsxwriter') as writer:
    # Master Summary Sheet
    master_df = pd.DataFrame({'Total Articles of All Sites': [master_data['total articles of all sites']],
                              'Negative': [master_data['total sentiment of all sites']['NEGATIVE']],
                              'Neutral': [master_data['total sentiment of all sites']['NEUTRAL']],
                              'Positive': [master_data['total sentiment of all sites']['POSITIVE']]})
    master_df.to_excel(writer, sheet_name='Master Summary', index=False)

    # Site Specific Sheets
    for site in site_data_list:
        site_name = site["site name"]
        site_df = pd.DataFrame({'Total Articles': [site['total articles']],
                                'Negative': [site['total sentiment from all articles']['NEGATIVE']],
                                'Neutral': [site['total sentiment from all articles']['NEUTRAL']],
                                'Positive': [site['total sentiment from all articles']['POSITIVE']]})
        site_df.to_excel(writer, sheet_name=site_name, index=False)

        # Add specific model totals below the main data
        model_totals_df = pd.DataFrame(site['total sentiment from all articles by modal']).transpose()
        model_totals_df.to_excel(writer, sheet_name=site_name, startrow=5)

    # Term Sentiment Sheets
    for term in master_data['sentiment by term'].keys():
        frames = []  # List to store DataFrames for each site
        for site in site_data_list:
            if term in site['sentiment by term']:
                term_data = site['sentiment by term'][term]
                site_df = pd.DataFrame({
                    'Site': [site['site name']],
                    'Total Articles': [term_data['total articles']],
                    'Negative': [term_data['Term Sentiment Totals']['NEGATIVE']],
                    'Neutral': [term_data['Term Sentiment Totals']['NEUTRAL']],
                    'Positive': [term_data['Term Sentiment Totals']['POSITIVE']]
                })
                frames.append(site_df)
        term_df = pd.concat(frames, ignore_index=True)


        term_df.to_excel(writer, sheet_name=term, index=False)