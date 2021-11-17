"""
The scripts for calculating statistics for the EDAM terms for the terms.

"""
import itertools
from collections import defaultdict
from datetime import datetime


def calculate_edam_term_statistics(tools: dict, term_type: str, index_list: dict) -> dict:
    """
    Calculate the statistics for EDAM terms.

    :param tools: The tool list.
    :param term_type: The term type to calculate statistics for.
    :param index_list: The index list for the terms.
    :return: The dictionary with the terms, the IDs and counts for strict (Only the specific term)
        and total (for parent terms).
    """
    # Create the dictionary to hold the topic statistics with the default fields.
    statistics = defaultdict(
        lambda: {"name": "", "depth": -1,
                 "strict_ids": set(), "total_ids": set(),
                 "strict_count": 0, "total_count": 0})

    # TODO: Determine the best way to add the data, if at all
    # statistics["termType"] = term_type.lower()
    # statistics["date"] = datetime.today().strftime("%Y-%m-%d")
    tool_terms: dict = _extract_terms(tools=tools, term_type=term_type)
    # Loop over the tools and the topics
    for toolID in tool_terms:
        for term in tool_terms[toolID]:
            statistics = _add_terms(stats=statistics, term=term, tool_id=toolID, index_list=index_list)

    # Loop over the statistics
    for term in statistics:
        if term == "termType" or term == "date":
            continue
        statistics[term]["strict_ids"] = list(statistics[term]["strict_ids"])
        statistics[term]["total_ids"] = list(statistics[term]["total_ids"])
        statistics[term]["strict_count"] = len(statistics[term]["strict_ids"])
        statistics[term]["total_count"] = len(statistics[term]["total_ids"])

    return statistics


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

            # Calculate the term depth
            path_depths: list = []
            for path in index_list[term_id]["path"]:
                path_depths.append(len(path["key"].split("||")))
            stats[term_id]["depth"] = min(path_depths) - 1  # Ensure topic is depth 0 = Root

    return stats


def _extract_terms(tools: dict, term_type: str) -> dict:
    """
    Extract terms from the tools.

    :param tools: The list of tools.
    :param term_type: The term type.
    :return: The dictionary with the tool ID and the terms.
    """
    term_type = term_type.capitalize()

    if term_type == "Topic":
        return _extract_edam_topics(tools=tools)
    elif term_type == "Operation":
        return _extract_edam_operation(tools=tools)
    elif term_type == "Format":
        return _extract_edam_format(tools=tools)
    elif term_type == "Data":
        return _extract_edam_data(tools=tools)
    else:
        raise ValueError(f"The term type '{term_type}' is not valid. Must be 'Topic', 'Operation', 'Format', or"
                         f"'Data'.")


def _extract_edam_topics(tools: dict) -> dict:
    """
    Get the EDAM topics for each tool.

    :param tools: The list of tools.
    :return: The dictionary with the tool id and the topics.
    """
    terms: defaultdict = defaultdict(lambda: [])

    for tool in tools:
        terms[tool["biotoolsID"]].extend([topic for topic in tool["topic"]])

    return terms


def _extract_edam_operation(tools: dict) -> dict:
    """
    Get the EDAM operation for each tool.

    :param tools: The list of tools.
    :return: The dictionary with the tool id and the operations.
    """
    terms: defaultdict = defaultdict(lambda: [])

    for tool in tools:
        terms[tool["biotoolsID"]].extend(*[function["operation"] for function in tool["function"]])

    return terms


def _extract_edam_format(tools: dict) -> dict:
    """
    Get the EDAM format for each tool.

    :param tools: The list of tools.
    :return: The dictionary with the tool id and the formats.
    """
    terms: defaultdict = defaultdict(lambda: [])

    for tool in tools:
        terms[tool["biotoolsID"]].extend(itertools.chain(*_get_inputs_outputs_info(tool=tool, term_type="format")))
    return terms


def _extract_edam_data(tools: dict) -> dict:
    """
    Get the EDAM data for each tool.

    :param tools: The list of tools.
    :return: The dictionary with the tool id and the topics.
    """
    terms: defaultdict = defaultdict(lambda: [])
    for tool in tools:
        terms[tool["biotoolsID"]].extend(_get_inputs_outputs_info(tool=tool, term_type="data"))
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

    return list(terms)
