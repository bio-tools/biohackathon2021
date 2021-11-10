import matplotlib.pyplot as plt
import pandas as pd
import requests
from boltons.iterutils import remap
from collections import defaultdict
import json
import seaborn as sns

from requests import Response


def main():
    # Read the tools
    with open("Resources/ProteomicsTools.json", "r", encoding="utf8") as f:
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

    #with open("Resources/ProteomicsTopics.json", "w") as f:
    #    f.write(json.dumps(topic_stats, indent=4, cls=SetEncoder))

    # Convert to dataframe
    topic_stats_df: pd.DataFrame = pd.DataFrame.from_dict(topic_stats, orient="index")
    del topic_stats_df["strict_ids"]
    del topic_stats_df["total_ids"]

    topic_stats_df.columns = ["Term", "Depth", "Strict", "Total"]
    topic_stats_df["Term ID"] = topic_stats_df.index
    # Remove terms, which was not found in the index list
    topic_stats_df = topic_stats_df[topic_stats_df.Depth != -1]
    topic_stats_df = topic_stats_df.reset_index()

    topic_stats_df = topic_stats_df.melt(id_vars=["Term", "Term ID", "Depth"], value_vars=["Strict", "Total"],
                                         var_name="Count Type", value_name="Count")

    topic_stats_df["Label"] = pd.Series([f"{term} ({depth})"
                                         for (term, term_id, depth) in
                                         zip(topic_stats_df['Term'], topic_stats_df['Term ID'], topic_stats_df['Depth'])
                                         ])

    topic_stats_df = topic_stats_df.sort_values("Depth")

    #topic_stats_df.to_excel("Resources/ProteomicsTopicsDf.xlsx")

    sns.set(rc={"figure.figsize": (10, 10)})
    g = sns.catplot(data=topic_stats_df, x="Label", y="Count", hue="Count Type", ci=None, kind="bar", orient="v",
                    legend=False)
    plt.legend(loc='upper right')
    g.axes[0, 0].set_xlabel("Term and depth")
    g.fig.suptitle("Terms for the Proteomics collection")
    g.set_xticklabels(rotation=90)
    plt.show()


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


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


if __name__ == "__main__":
    main()
