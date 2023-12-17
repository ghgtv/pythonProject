import json


def get_configure():
    jsonfile = open("ClientConfig.json", "r")
    config = json.load(jsonfile)
    jsonfile.close()
    return config


def update_config(param, value):
    config = get_configure()
    jsonfile = open("ClientConfig.json", "w")
    config[param] = value
    json.dump(config, jsonfile)
