import json
import concurrent.futures
from transformers import pipeline


# Setup Hugging Face Pipelines
pipe1 = pipeline("text-classification", model="sismetanin/rubert-ru-sentiment-rusentiment")
pipe2 = pipeline("text-classification", model="blanchefort/rubert-base-cased-sentiment")
pipe3 = pipeline("text-classification", model="sismetanin/sbert-ru-sentiment-krnd")

loser = pipe3("tester")

# Function to perform sentiment analysis
def analyze_sentiment(headline):
    result1 = pipe1(headline)
    result2 = pipe2(headline)
    return (result1[0], result2[0])

# Concurrent sentiment analysis
def process_articles(articles):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Create a list to hold all future results
        futures = []
        for article_wrapper in articles:
            # There should be only one key per dictionary, like 'article1', 'article2', etc.
            for article_key, article in article_wrapper.items():
                # Check if 'article' dictionary has the 'title' key before processing
                if 'title' not in article:
                    print(f"Skipping article with key {article_key}: 'title' not found.")
                    continue  # Skip this article and go to the next one

                # Now 'article' is the dictionary with the 'title', 'date', and 'url'
                # Submit the sentiment analysis task for the 'title'
                future = executor.submit(analyze_sentiment, article['title'])
                futures.append((future, article))

        # As each future completes, get the result and store it in the corresponding article
        for future, article in futures:
            try:
                sentiment_results = future.result()
                article['sentiment_pipe1'], article['sentiment_pipe2'] = sentiment_results
            except Exception as exc:
                print(f'Generated an exception for article with title {article.get("title", "Unknown")}: {exc}')
            else:
                print(f'Article processed with title: {article["title"]}')

# Process the articles using concurrent computing
process_articles(data['articles'])

# Save or use the sentiment data as needed
# For example, save back to JSON
with open('sentiment_analysis_results.json', 'w', encoding='utf-8') as f_out:
    json.dump(data, f_out, ensure_ascii=False, indent=2)