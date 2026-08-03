import json
from collections import Counter

with open("data/chunks.json") as f:
    chunks = json.load(f)

sections = [c["section"] for c in chunks]
print(Counter(sections))