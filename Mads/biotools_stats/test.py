"""
The test script for the biotools_statistic package.
Used for showing plots etc.

If script is to run on other machines, please be aware of the file path.
"""
import requests
import seaborn as sns
import matplotlib.pyplot as plt
import json

from requests import Response

from biotools_statistics import calculate_general_statistics
from biotools_statistics import calculate_edam_term_statistics


def _get_index_list(term_type: str):
    """
    Get the index list.

    :param term_type: The EDAM term type.
    :return: The index list.
    """
    if term_type.capitalize() not in ["Topic", "Operation", "Format", "Data"]:
        raise ValueError(f"The term type '{term_type}' is not valid. Must be 'Topic', 'Operation', 'Format', or"
                         f"'Data'.")

    resp: Response = requests.get(f"https://bio.tools/api/o/index_EDAM_{term_type}?format=json")
    resp.raise_for_status()
    index_list: dict = resp.json()["data"]
    return index_list


def main():
    """
    The main entry point of the script.
    """
    with open("Tools.json", "r") as f:
        tools = json.load(f)

    term_stats = calculate_edam_term_statistics(tools=tools, term_type="format", index_list=_get_index_list("format"))
    print(json.dumps(term_stats, indent=4))
    # terms = extract_edam_topics(tools=tools)
    # print(json.dumps(terms, indent=4))
    # print("\n"*2)
    #
    # terms = extract_edam_operation(tools=tools)
    # print(json.dumps(terms, indent=4))
    # print("\n"*2)
    #
    # terms = extract_edam_format(tools=tools)
    # print(json.dumps(terms, indent=4))
    # print("\n"*2)
    #
    # terms = extract_edam_data(tools=tools)
    # print(json.dumps(terms, indent=4))
    # print("\n"*2)

    # stats = calculate_general_statistics(tools=tools)
    # print(json.dumps(stats, indent=4))


if __name__ == "__main__":
    main()
