import json

def parse(json_string):
    return  json.loads(json_string)

def get_by_key(data, key):
    if key in data:
        return data[key]
    else:
        raise Exception(key + " does not exists.")

def parse_from_file(path):
    jsonFile = open('../settings.json', "r")
    return json.loads(jsonFile.read())

def serialize(obj):
    return json.dumps(obj)