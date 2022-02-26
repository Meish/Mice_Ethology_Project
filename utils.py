import yaml
import json
import pandas as pd


def read_excel(path_to_excel):
    df = pd.read_excel(path_to_excel)
    return df


def read_yaml(path_to_yaml):
    with open(path_to_yaml, "r") as stream:
        return yaml.safe_load(stream)

def read_json(path_to_json):
    with open(path_to_json, "r") as stream:
        return json.load(stream)
