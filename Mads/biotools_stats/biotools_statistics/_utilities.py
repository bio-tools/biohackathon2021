"""
Different utilities and helper methods.

"""
import datetime

import dateutil
from dateutil import parser
import pytz
from boltons.iterutils import remap


def clean_and_filter_tool_list(raw_tools: list, upper_time_limit: datetime.datetime) -> list:
    """
    Clean the list of tools.

    :param raw_tools: The raw list of tools.
    :param upper_time_limit: Calculate the statistics for tools added up to the time limit.
        Default: datetime.datetime.today()
    :return: The cleaned list of tools.
    """
    # Clean the list
    drop_false = lambda path, key, value: bool(value)
    unfiltered_tools = remap(raw_tools, visit=drop_false)
    # Filter the tools according to the upper time limit
    return [tool for tool in unfiltered_tools
            if dateutil.parser.isoparse(tool["additionDate"]) < pytz.utc.localize(upper_time_limit)]
