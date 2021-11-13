"""
Functions for calculating EDAM statistics for tools in https://bio.tools.
"""
import json
from collections import defaultdict
from typing import Tuple

import pandas as pd
import requests
from requests import Response


def find_top_terms(tools: dict, term_type: str, top_n: int) -> dict:
    """
    Find top terms.

    :param tools: The list of tools.
    :param term_type: The term type. Must be topic, operation, format, and data.
    :param top_n: The top number of terms to be returned.
    :return: A dictionary with the term name, term ID and number of terms.
    """
    counting_dict: defaultdict = defaultdict(lambda: {"term": "", "term_id": "", "count": 0})
    # Get the term list
    if term_type.lower() == "topic":
        term_dict = get_edam_topics(tools=tools)
    elif term_type.lower() == "operation":
        term_dict = get_edam_operation(tools=tools)
    elif term_type.lower() == "format":
        term_dict = get_edam_format(tools=tools)
    elif term_type.lower() == "data":
        term_dict = get_edam_data(tools=tools)
    else:
        raise ValueError(f"The term_type {term_type.lower()} is not supported. "
                         f"Must be 'topic', 'operation', 'data', or 'format'.")
    # Count the terms
    for tool_id in term_dict.keys():
        for term in term_dict[tool_id]["term"]:
            if counting_dict[term["term"]]["term"] == "":
                counting_dict[term["term"]]["term"] = term["term"]
                # Example split: ['http:', '', 'edamontology.org', 'topic_3577']
                counting_dict[term["term"]]["term_id"] = term["uri"].split("/")[3]
            counting_dict[term["term"]]["count"] += 1

    ranked_terms = sorted(counting_dict, key=lambda x: (counting_dict[x]['count']), reverse=True)[:top_n]


def get_edam_topics(tools: dict):
    """
    Get the EDAM topics for each tool.

    :param tools: The list of tools.
    :return: The dictionary with the tool id and the topics.
    """
    terms: defaultdict = defaultdict(lambda: {"term": list})

    for tool in tools:
        terms[tool["biotoolsID"]]["term"] = [topic for topic in tool["topic"]]

    return terms


def get_edam_operation(tools: dict):
    """
    Get the EDAM operation for each tool.

    :param tools: The list of tools.
    :return: The dictionary with the tool id and the operations.
    """
    terms: defaultdict = defaultdict(lambda: {"term": list})

    for tool in tools:
        terms[tool["biotoolsID"]]["term"] = [function["operation"] for function in tool["function"]]

    return terms


def get_edam_format(tools: dict):
    """
    Get the EDAM format for each tool.

    :param tools: The list of tools.
    :return: The dictionary with the tool id and the formats.
    """
    terms: defaultdict = defaultdict(lambda: {"term": list})

    for tool in tools:
        terms[tool["biotoolsID"]]["term"] = _get_inputs_outputs_info(tool=tool, term_type="format")
    return terms


def get_edam_data(tools: dict):
    """
    Get the EDAM data for each tool.

    :param tools: The list of tools.
    :return: The dictionary with the tool id and the topics.
    """
    terms: defaultdict = defaultdict(lambda: {"term": list})
    for tool in tools:
        terms[tool["biotoolsID"]]["term"] = _get_inputs_outputs_info(tool=tool, term_type="data")
    return terms


def _get_inputs_outputs_info(tool: dict, term_type: str) -> list:
    """
    Get the inputs and outputs for a tool.

    :param tool: The tool dict.
    :param term_type: The term type.
    :return: The list with the specific terms.
    """
    terms: list = []

    for function in tool["function"]:
        if "input" in function:
            for i in function["input"]:
                if term_type in i:
                    terms.append(i[term_type])
        if "output" in function:
            for o in function["output"]:
                if term_type in o:
                    terms.append(o[term_type])

    return terms


def calculate_edam_topic_statistics(tools: list) -> dict:
    """
    Calculate the statistics for EDAM topics.

    :param tools: The tool list.
    :return: The dictionary with the terms, the IDs and counts for strict (Only the specific term)
        and total (for parent terms).
    """
    # Create the dictionary to hold the topic statistics with the default fields.
    statistics = defaultdict(
        lambda: {"name": "", "depth": -1,
                 "strict_ids": set(), "total_ids": set(),
                 "strict_count": 0, "total_count": 0})

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

    # Add topic name and depth if not added
    stats = _add_term_info(stats=stats, term_id=term_id, index_list=index_list)

    # Go through the branches
    for branch_term in _get_branch_terms(term_id=term_id, term_index=index_list):
        # Add topic name and depth if not added
        stats = _add_term_info(stats=stats, term_id=branch_term, index_list=index_list)
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
    if term_id in term_index:
        for branch in term_index[term_id]["path"]:
            terms.extend(branch["key"].split("||"))
    return terms


def _add_term_info(stats: dict, term_id: str, index_list: dict) -> dict:
    """
    Add term information, if none exists.

    :param stats: The statistics dictionary.
    :param term_id: The EDAM term.
    :param index_list: The index list.
    :return: The statistics dictionary.
    """
    if term_id in index_list:
        if stats[term_id]["name"] == "":
            stats[term_id]["name"] = index_list[term_id]["name"]

            path_depths: list = []
            for path in index_list[term_id]["path"]:
                path_depths.append(len(path["key"].split("||")))

            # stats[term_id]["depth"] = len(index_list[term_id]["path"][0]["key"].split("||"))
            stats[term_id]["depth"] = min(path_depths) - 1  # Ensure topic is depth 0 = Root

    return stats