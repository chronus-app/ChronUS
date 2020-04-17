import json


def get_degrees():
    with open('core/data/degrees.json', encoding='utf-8') as json_file: 
        degrees = json.load(json_file)

    return list(degrees.items())