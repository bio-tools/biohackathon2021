"""
Functions for calculating EDAM statistics for tools in https://bio.tools.
"""
import json
from collections import defaultdict


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
