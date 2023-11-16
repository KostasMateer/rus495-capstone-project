"""
News Sentiment Analysis Organizer

This script is designed to analyze sentiment data from various news articles.
It processes JSON files containing sentiment analysis results from multiple models
(RuSentiment, Kaggle News, and General Model) for a specified news site. The script 
aggregates sentiment data, organizes articles by search term, and identifies articles 
with radically different sentiment assessments across models. 

The final output is a JSON file containing comprehensive sentiment data, 
including counts and detailed lists of articles with diverse sentiment interpretations.

Author: Kostas Mateer
Date: 14NOV23
RUS 495: Dr. Ewington
"""

import json
import glob

# User input for the news site name
NEWS_SITE = input("Insert news site name in caps: ")

# Pattern to match all JSON files for the specified news site
json_file_pattern = f'analysis/sentiment_results/{NEWS_SITE}_results/*.json'

# Container for organized data
organized_data = {
    'site name': NEWS_SITE,
    'total articles': 0, 
    'total sentiment from all articles': {
        'NEGATIVE': 0,
        'NEUTRAL': 0,
        'POSITIVE': 0,
    },
    'total sentiment from all articles by modal': {
        'RuSentiment Model Totals': {'NEGATIVE': 0, 'NEUTRAL': 0, 'POSITIVE': 0},
        'Kaggle News Model Totals': {'NEGATIVE': 0, 'NEUTRAL': 0, 'POSITIVE': 0},
        'General Model Totals': {'NEGATIVE': 0, 'NEUTRAL': 0, 'POSITIVE': 0}
    },
    'sentiment by term': {},
    'total of radically different sentiment articles': 0,
    'radical different sentiment articles': [],
    'articles by term': {}
}

# Process each file matching the pattern
for file in glob.glob(json_file_pattern):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        search_term = data['search term']

        # Create a dictionary for each search term if it doesn't exist
        if search_term not in organized_data['sentiment by term']:
            organized_data['sentiment by term'][search_term] = {
                'total articles': 0,
                'Term Sentiment Totals': {
                    'NEGATIVE': 0,
                    'NEUTRAL': 0,
                    'POSITIVE': 0,
                },
                'Specific Model Totals': {
                    'RuSentiment Model Totals' : {
                        'NEGATIVE' : 0,
                        'NEUTRAL' : 0,
                        'POSITIVE': 0,
                    },
                    'Kaggle News Model Totals' : {
                        'NEGATIVE' : 0,
                        'NEUTRAL' : 0,
                        'POSITIVE': 0,
                    },
                    'General Model Totals' : {
                        'NEGATIVE' : 0,
                        'NEUTRAL' : 0,
                        'POSITIVE': 0,
                    }},
            }

        for i in range(len(data['articles'])):
            article = next(iter(data['articles'][i].values()))

            if 'title' not in article:
                data['total articles'] -= 1
                continue
            
            sentiment_model_rusentiment_label = article['RuSentiment Model']['label']
            if sentiment_model_rusentiment_label == 'NEUTRAL':
                organized_data['sentiment by term'][search_term]['Specific Model Totals']['RuSentiment Model Totals']['NEUTRAL']+=1
                organized_data['total sentiment from all articles by modal']['RuSentiment Model Totals']['NEUTRAL']+=1
            elif sentiment_model_rusentiment_label == 'POSITIVE':
                organized_data['sentiment by term'][search_term]['Specific Model Totals']['RuSentiment Model Totals']['POSITIVE']+=1
                organized_data['total sentiment from all articles by modal']['RuSentiment Model Totals']['POSITIVE']+=1
            else:
                organized_data['sentiment by term'][search_term]['Specific Model Totals']['RuSentiment Model Totals']['NEGATIVE']+=1
                organized_data['total sentiment from all articles by modal']['RuSentiment Model Totals']['NEGATIVE']+=1
            
            sentiment_model_kaggle_label = article['Kaggle News Model']['label']
            if sentiment_model_kaggle_label == 'NEUTRAL':
                organized_data['sentiment by term'][search_term]['Specific Model Totals']['Kaggle News Model Totals']['NEUTRAL']+=1
                organized_data['total sentiment from all articles by modal']['Kaggle News Model Totals']['NEUTRAL']+=1
            elif sentiment_model_kaggle_label == 'POSITIVE':
                organized_data['sentiment by term'][search_term]['Specific Model Totals']['Kaggle News Model Totals']['POSITIVE']+=1
                organized_data['total sentiment from all articles by modal']['Kaggle News Model Totals']['POSITIVE']+=1
            else:
                organized_data['sentiment by term'][search_term]['Specific Model Totals']['Kaggle News Model Totals']['NEGATIVE']+=1
                organized_data['total sentiment from all articles by modal']['Kaggle News Model Totals']['NEGATIVE']+=1
            
            sentiment_model_general_label = article['General Model']['label']
            if sentiment_model_general_label == 'NEUTRAL':
                organized_data['sentiment by term'][search_term]['Specific Model Totals']['General Model Totals']['NEUTRAL']+=1
                organized_data['total sentiment from all articles by modal']['General Model Totals']['NEUTRAL']+=1
            elif sentiment_model_general_label == 'POSITIVE':
                organized_data['sentiment by term'][search_term]['Specific Model Totals']['General Model Totals']['POSITIVE']+=1
                organized_data['total sentiment from all articles by modal']['General Model Totals']['POSITIVE']+=1
            else:
                organized_data['sentiment by term'][search_term]['Specific Model Totals']['General Model Totals']['NEGATIVE']+=1
                organized_data['total sentiment from all articles by modal']['General Model Totals']['NEGATIVE']+=1

            if (sentiment_model_rusentiment_label or sentiment_model_kaggle_label or sentiment_model_general_label != 'NEUTRAL'):
                if (sentiment_model_rusentiment_label == 'POSITIVE' and (sentiment_model_kaggle_label == 'NEGATIVE' or sentiment_model_general_label == 'NEGATIVE')):
                    organized_data['radical different sentiment articles'].append([{"search term" : search_term}, data['articles'][i]])
                elif (sentiment_model_rusentiment_label == 'NEGATIVE' and (sentiment_model_kaggle_label == 'POSITIVE' or sentiment_model_general_label == 'POSITIVE')):
                    organized_data['radical different sentiment articles'].append([{"search term" : search_term}, data['articles'][i]])

                elif (sentiment_model_kaggle_label == 'POSITIVE' and (sentiment_model_rusentiment_label == 'NEGATIVE' or sentiment_model_general_label == 'NEGATIVE')):
                    organized_data['radical different sentiment articles'].append([{"search term" : search_term}, data['articles'][i]])
                elif (sentiment_model_kaggle_label == 'NEGATIVE' and (sentiment_model_rusentiment_label == 'POSITIVE' or sentiment_model_general_label == 'POSITIVE')):
                    organized_data['radical different sentiment articles'].append([{"search term" : search_term}, data['articles'][i]])

                elif (sentiment_model_general_label == 'POSITIVE' and (sentiment_model_rusentiment_label == 'NEGATIVE' or sentiment_model_kaggle_label == 'NEGATIVE')):
                    organized_data['radical different sentiment articles'].append([{"search term" : search_term}, data['articles'][i]])
                elif (sentiment_model_general_label == 'NEGATIVE' and (sentiment_model_rusentiment_label == 'POSITIVE' or sentiment_model_kaggle_label == 'POSITIVE')):
                    organized_data['radical different sentiment articles'].append([{"search term" : search_term}, data['articles'][i]])

        
        organized_data['sentiment by term'][search_term]['Term Sentiment Totals']['NEGATIVE'] += organized_data['sentiment by term'][search_term]['Specific Model Totals']['RuSentiment Model Totals']['NEGATIVE']
        organized_data['sentiment by term'][search_term]['Term Sentiment Totals']['NEGATIVE'] += organized_data['sentiment by term'][search_term]['Specific Model Totals']['Kaggle News Model Totals']['NEGATIVE']
        organized_data['sentiment by term'][search_term]['Term Sentiment Totals']['NEGATIVE'] += organized_data['sentiment by term'][search_term]['Specific Model Totals']['General Model Totals']['NEGATIVE']  

        organized_data['sentiment by term'][search_term]['Term Sentiment Totals']['NEUTRAL'] += organized_data['sentiment by term'][search_term]['Specific Model Totals']['RuSentiment Model Totals']['NEUTRAL']
        organized_data['sentiment by term'][search_term]['Term Sentiment Totals']['NEUTRAL'] += organized_data['sentiment by term'][search_term]['Specific Model Totals']['Kaggle News Model Totals']['NEUTRAL']
        organized_data['sentiment by term'][search_term]['Term Sentiment Totals']['NEUTRAL'] += organized_data['sentiment by term'][search_term]['Specific Model Totals']['General Model Totals']['NEUTRAL']

        organized_data['sentiment by term'][search_term]['Term Sentiment Totals']['POSITIVE'] += organized_data['sentiment by term'][search_term]['Specific Model Totals']['RuSentiment Model Totals']['POSITIVE']
        organized_data['sentiment by term'][search_term]['Term Sentiment Totals']['POSITIVE'] += organized_data['sentiment by term'][search_term]['Specific Model Totals']['Kaggle News Model Totals']['POSITIVE']
        organized_data['sentiment by term'][search_term]['Term Sentiment Totals']['POSITIVE'] += organized_data['sentiment by term'][search_term]['Specific Model Totals']['General Model Totals']['POSITIVE']

        # Update total articles and append the articles
        organized_data['sentiment by term'][search_term]['total articles'] += data['total articles']
        organized_data['total articles'] += data['total articles']

        organized_data['total sentiment from all articles']['NEGATIVE'] += organized_data['sentiment by term'][search_term]['Term Sentiment Totals']['NEGATIVE']
        organized_data['total sentiment from all articles']['NEUTRAL'] += organized_data['sentiment by term'][search_term]['Term Sentiment Totals']['NEUTRAL']
        organized_data['total sentiment from all articles']['POSITIVE'] +=  organized_data['sentiment by term'][search_term]['Term Sentiment Totals']['POSITIVE']

        # organized_data['total sentiment from each search term'] = organized_data[search_term]
        organized_data['articles by term'][search_term] = data
        # print()
        # organized_data[search_term]['articles'].extend(data['articles'])

organized_data['total of radically different sentiment articles'] += len(organized_data['radical different sentiment articles'])

# Write the organized data to a new file
with open(f'{NEWS_SITE}_articles_organized.json', 'w', encoding='utf-8') as f:
    json.dump(organized_data, f, ensure_ascii=False, indent=2)
