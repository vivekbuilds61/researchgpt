import json

with open("data/metadata.json") as f:
    papers = json.load(f)

for p in papers[:10]:
    print(p["categories"], "-", p["title"])