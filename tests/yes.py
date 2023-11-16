import json

def fix_json_structure(file_path):
    # Read the original JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Fix the structure of the 'articles' list
    fixed_articles = []
    i = 1
    for article in data['articles']:
        # Extract the nested article
        for key in article:
            fixed_articles.append({f'article{i}': article[key][key]})
        i+=1

    # Update the 'articles' list in the original data
    data['articles'] = fixed_articles

    # Write the fixed data to a new JSON file
    with open('fixed_data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Replace 'your_file_path.json' with the path to your JSON file
fix_json_structure('analysis\sentiment_results\PERVYI_KANAL_results\sentiment analysis мобилизацияpervyikanal.json')
