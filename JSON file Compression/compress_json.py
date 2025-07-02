import json
with open('result_comp_cleaned.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('result_comp_cleaned.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, separators=(',', ':'))
