"""
Different utilities and helper methods.

"""
from boltons.iterutils import remap


def clean_list(raw_tools: list) -> list:
    """
    Clean the list of tools.

    :param raw_tools: The raw list of tools.
    :return: The cleaned list of tools.
    """
    # Clean the list
    drop_false = lambda path, key, value: bool(value)
    return remap(raw_tools, visit=drop_false)
