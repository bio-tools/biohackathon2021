import datetime
import json
from collections import defaultdict

from boltons.iterutils import remap
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import seaborn as sns


def main():
    plt.style.use("ggplot")
    # Read the tools
    collection_name: str = ""
    with open(f"Resources/{collection_name.title().replace(' ', '')}Collection/Tools.json", "r", encoding="utf8") as f:
        tools = json.load(f)

    calculate_statistics(raw_tools=tools, collection_name=collection_name)


def calculate_statistics(raw_tools: list, collection_name: str, ):
    """
        Calculate the statistics (Main function).

        :param raw_tools: The raw list of tools.
        :param collection_name: The name of the collection.
        :return:
        """
    # Clean the list
    drop_false = lambda path, key, value: bool(value)
    tools = remap(raw_tools, visit=drop_false)

    stats_dict: dict = calculate_total_entries_per_time(tools=tools)
    _create_total_entries_plot(stats_dict=stats_dict, collection_name=collection_name)


def calculate_total_entries_per_time(tools: list):
    """
    Calculate the total entries over time.
    :param tools: The raw list of tools.
    :return: The statistics dictionary.
    """

    tool_time: dict = {tool["biotoolsID"]: datetime.datetime.fromisoformat(tool["additionDate"].split("T")[0]).date()
                       for tool in tools}

    tool_time_df: pd.DataFrame = pd.DataFrame.from_dict(data=tool_time, orient="index")
    tool_time_df = tool_time_df.reset_index()
    tool_time_df.columns = ["ID", "AdditionDate"]

    stats_dict: defaultdict = defaultdict(lambda: {"count": 0})

    for date in daterange(start_date=min(tool_time_df["AdditionDate"]), end_date=max(tool_time_df["AdditionDate"])):
        stats_dict[date] = len(tool_time_df[(tool_time_df["AdditionDate"] <= date)])

    return stats_dict


def _create_total_entries_plot(stats_dict, collection_name):
    """

    :param stats_dict: The stats dictionary
    :param collection_name: The name of the collection.
    """
    stats_df: pd.DataFrame = pd.DataFrame.from_dict(stats_dict, orient="index", columns=["Count"])
    # Format the axis
    fig, ax = plt.subplots()
    ax = sns.lineplot(data=stats_df, x=stats_df.index, y="Count")
    ax.set_xlabel("Time")
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))  # Every 2 month
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.set_title(f"The number of tools over time in the {collection_name} collection")
    ax.set_xlim(xmin=min(stats_df.index), xmax=max(stats_df.index))
    fig.autofmt_xdate()
    plt.show()


def daterange(start_date, end_date):
    """
    Helper methods for iterating through the dates (Modified from https://stackoverflow.com/a/1060330).

    :param start_date: The start date.
    :param end_date: The end date (modified to be inclusive instead of exclusive).
    :return: The generator.
    """
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + datetime.timedelta(n)


if __name__ == "__main__":
    main()
