import json
import random

with open('../text.json', "r") as data_file:
    text = json.load(data_file)

random.shuffle(text["message"])

with open('../text.json', 'w') as outfile:
    json.dump(text, outfile, ensure_ascii=False, indent=2)