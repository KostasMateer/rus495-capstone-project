"""
Sentiment Analysis Aggregator for News Articles

This script processes news articles from multiple JSON files and aggregates the
data based on the sentiment analysis results from three different models: RuSentiment,
Kaggle News, and General Model. It focuses on identifying and counting articles with 
radically different sentiment combinations, such as those where one model indicates 
positive sentiment while another indicates negative. The script also compiles these 
articles into a separate collection for detailed review.

The aggregated sentiment counts and article details are then saved into separate JSON
files for further analysis or reporting.

Author: Kostas Mateer
Date: 15NOV23
RUS 495: Dr. Ewington
"""

import json

# Paths to the JSON files containing news articles data
site_data_files = [
    'MEDUZA_articles_organized.json', 
    'NOVAYA_GAZETA_articles_organized.json',
    'PERVYI_KANAL_articles_organized.json',
    'TASS_articles_organized.json'
]

# Initialize the counts for different sentiment combinations
radical_different_sentiments = {
    "RuSentiment POSITIVE, Kaggle News POSITIVE, General Model NEGATIVE": 0,
    "RuSentiment POSITIVE, Kaggle News NEGATIVE, General Model POSITIVE": 0,
    "RuSentiment POSITIVE, Kaggle News NEGATIVE, General Model NEGATIVE": 0,
    "RuSentiment NEGATIVE, Kaggle News NEGATIVE, General Model POSITIVE": 0,
    "RuSentiment NEGATIVE, Kaggle News POSITIVE, General Model NEGATIVE": 0,
    "RuSentiment NEGATIVE, Kaggle News NEGATIVE, General Model NEGATIVE": 0,
    "RuSentiment POSITIVE, Kaggle News POSITIVE, General Model POSITIVE": 0
}

# Initialize a collection to store articles with radical sentiment differences
radical_different_articles = {key: [] for key in radical_different_sentiments}

# Process each file
for file_name in site_data_files:
    with open(file_name, 'r', encoding='utf-8') as file:
        site_data = json.load(file)
        
        # Iterate through each article's sentiments
        for article_bundle in site_data['radical different sentiment articles']:
            for article_info in article_bundle[1:]:
                article_id = list(article_info.keys())[0]
                article = article_info[article_id]

                # Get the sentiment labels from the models
                rs_label = article['RuSentiment Model']['label']
                kn_label = article['Kaggle News Model']['label']
                gm_label = article['General Model']['label']
                
                # Ignore neutral sentiments
                labels = [rs_label, kn_label, gm_label]
                if 'NEUTRAL' in labels:
                    continue

                # Check for all POSITIVE or all NEGATIVE
                if labels.count('POSITIVE') == 3 or labels.count('NEGATIVE') == 3:
                    # Construct the key for radical sentiment combinations
                    key = f"RuSentiment {rs_label}, Kaggle News {kn_label}, General Model {gm_label}"
                    radical_different_sentiments[key] += 1
                    radical_different_articles[key].append({
                        'site name': site_data['site name'],
                        'search term': article_bundle[0],
                        'article': article
                    })

# Save the updated counts and articles to JSON files
with open('radical_different_sentiments.json', 'w', encoding='utf-8') as file:
    json.dump(radical_different_sentiments, file, ensure_ascii=False, indent=2)

with open('radical_different_articles.json', 'w', encoding='utf-8') as file:
    json.dump(radical_different_articles, file, ensure_ascii=False, indent=2)
