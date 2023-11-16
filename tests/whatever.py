import json

FILE_NAME = "специальная военная операцияpervyikanal.json"
with open(f"json files\pervyi kanal\{FILE_NAME}", 'r', encoding='utf-8') as f:
        data = json.load(f)

for i in range(len(data['articles'])):
        data['articles'][i] = {f"article{i+1}": data['articles'][i]}

with open(f"{FILE_NAME}", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
print(data)