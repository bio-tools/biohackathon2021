"""
The test script for the biotools_statistic package.
Used for showing plots etc.

If script is to run on other machines, please be aware of the file path.
"""
import seaborn as sns
import matplotlib.pyplot as plt
import json

from biotools_statistics import calculate_general_statistics


def main():
    """
    The main entry point of the script.
    """
    with open("Tools.json", "r") as f:
        tools = json.load(f)

    stats = calculate_general_statistics(tools=tools)
    print(json.dumps(stats, indent=4))


if __name__ == "__main__":
    main()
