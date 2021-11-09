import json

import requests
from boltons.iterutils import remap


def __temporary__download_tools():
    resp = requests.get("https://bio.tools/api/t/?format=json")
    resp.raise_for_status()
    data = resp.json()["list"]
    with open("Resources/SmallTools.json", "w") as f:
        f.write(json.dumps(data))


def calculate_statistics(raw_tools: dict):
    """
    Calculate statistics

    :param raw_tools:
    :return:
    """
    # Clean the data
    drop_false = lambda path, key, value: bool(value)
    tools = remap(raw_tools, visit=drop_false)

    # Calculate the statistics



def calculate_edam_topic_statistics():
    pass


def main():
    with open("Resources/SmallTools.json") as f:
        tools = json.load(f)
    calculate_statistics(raw_tools=tools)


if __name__ == "__main__":
    main()
