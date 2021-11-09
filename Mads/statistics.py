import requests
from boltons.iterutils import remap
from collections import defaultdict
import json

from requests import Response


def main():
    # Read the tools
    with open("Resources/SmallTools.json", "r", encoding="utf8") as f:
        tools = json.load(f)

    calculate_statistics(raw_tools=tools)


def calculate_statistics(raw_tools: list):
    """
    Calculate the statistics (Main function).

    :param raw_tools: The raw list of tools.
    :return:
    """
    # Clean the list
    drop_false = lambda path, key, value: bool(value)
    tools = remap(raw_tools, visit=drop_false)

    # Calculate the EDAM term statistics
    topic_stats = calculate_edam_topic_statistics(tools=tools)

    with open("Resources/Topics.json", "w") as f:
        f.write(json.dumps(topic_stats, indent=4, cls=SetEncoder))


def calculate_edam_topic_statistics(tools: list) -> dict:
    """
    Calculate the statistics for EDAM topics.

    :param tools: The tool list.
    :return: The dictionary with the terms, the IDs and counts for strict (Only the specific term)
        and total (for parent terms).
    """
    # Create the dictionary to hold the topic statistics with the default fields.
    statistics = defaultdict(
        lambda: {'strict_ids': set(), 'total_ids': set(), 'strict_count': 0, 'total_count': 0})
    # Get the index list
    index_list: dict = _get_index_list(term_type="topic")

    # Loop over the tools and the topics
    for tool in tools:
        if "topic" in tool:
            for term in tool["topic"]:
                statistics = _add_terms(stats=statistics, term=term, tool_id=tool["biotoolsID"], index_list=index_list)

    # Loop over the statistics
    for term in statistics.keys():
        statistics[term]["strict_count"] = len(statistics[term]["strict_ids"])
        statistics[term]["total_count"] = len(statistics[term]["total_ids"])

    return statistics


def _get_index_list(term_type: str):
    """
    Get the index list

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


def _add_terms(stats: dict, term: dict, tool_id: dict, index_list: dict) -> dict:
    """
    Add term to the statistics.

    :param stats: The statistics dictionary.
    :param term: The EDAM term.
    :param tool_id: The bio.tools ID.
    :param index_list: The index list.
    :return: The statistics dictionary.
    """
    # Get the term id
    term_id = term["uri"].split("/")[3]  # Example split: ['http:', '', 'edamontology.org', 'topic_3577']
    # Add to the id lists
    stats[term_id]["strict_ids"].add(tool_id)
    stats[term_id]["total_ids"].add(tool_id)

    # Go through the branches
    for branch_term in _get_branch_terms(term_id=term_id, term_index=index_list):
        stats[branch_term]["total_ids"].add(tool_id)

    return stats


def _get_branch_terms(term_id: str, term_index: dict) -> list:
    """
    Get the branch terms.

    :param term_id: The term ID.
    :param term_index: The term index list.
    :return: The list of branch terms.
    """
    terms: list = []
    for branch in term_index[term_id]["path"]:
        terms.extend(branch["key"].split("||"))
    return terms


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


if __name__ == "__main__":
    main()