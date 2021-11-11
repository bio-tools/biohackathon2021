import json

from boltons.iterutils import remap
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import seaborn as sns

from biotools_statistics import calculate_collection_statistics


def main():
    plt.style.use("ggplot")
    # Read the tools
    collection_name: str = ""
    with open(f"Resources/{collection_name.title().replace(' ', '')}Collection/Tools.json", "r", encoding="utf8") as f:
        raw_tools = json.load(f)

    drop_false = lambda path, key, value: bool(value)
    tools = remap(raw_tools, visit=drop_false)

    calculate_statistics(raw_tools=tools, collection_name=collection_name)

    stats_dict = calculate_collection_statistics(tools=tools)

def calculate_statistics(raw_tools: list, collection_name: str, ):
    """
        Calculate the statistics.

        :param raw_tools: The raw list of tools.
        :param collection_name: The name of the collection.
        :return:
        """
    # Clean the list


    #stats_dict: dict = calculate_total_entries_over_time(tools=tools)


    # _create_total_entries_plot(stats_dict=stats_dict, collection_name=collection_name)


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


if __name__ == "__main__":
    main()
