"""
The script for calculating the different statistics for a given tool list.
"""
from datetime import datetime
from typing import Dict, Union, List

from ._utilities import clean_list


def calculate_general_statistics(tools: list, upper_time_limit: datetime = datetime.today()):
    """
    Calculate the general statistics for a list of tools.

    :param tools: The list of tools.
    :param upper_time_limit: Calculate the statistics for tools added up to the time limit.
        Default: datetime.datetime.today()
    :return: The dictionary with the statistics.
    """
    # Clean the list of tools
    tools = clean_list(raw_tools=tools)

    # Filter the tools according to the upper time limit
    tools = [tool for tool in tools
             if datetime.strptime(tool["additionDate"], "%Y-%m-%dT%H:%M:%SZ") < upper_time_limit]

    # Create the dictionary to hold the statistics and calculate the statistics
    stats: Dict[str, Union[int, Dict[str, int]]] = {}
    stats["toolCount"] = len(tools)

    stats["hasToolType"] = len([tool for tool in tools if "toolType" in tool])
    stats["toolTypeCount"] = sum([len(tool["toolType"]) for tool in tools if "toolType" in tool])
    stats["toolTypes"] = _calculate_tool_type_statistics(tools=tools)

    stats["hasTopic"] = len([tool for tool in tools if len(tool["topic"]) > 0])
    stats["topicCount"] = sum([len(tool["topic"]) for tool in tools])

    stats["hasOperatingSystem"] = len([tool for tool in tools if "operatingSystem" in tool])
    stats["operatingSystemCount"] = sum([len(tool["operatingSystem"]) for tool in tools if "operatingSystem" in tool])
    stats["operatingSystem"] = _calculate_os_statistics(tools=tools)

    stats["hasLanguage"] = len([tool for tool in tools if "language" in tool])
    stats["languageCount"] = sum([len(tool["language"]) for tool in tools if "language" in tool])
    stats["languages"] = _calculate_language_statistics(tools=tools)

    stats["hasLicense"] = len([tool for tool in tools if "license" in tool])
    stats["licenses"] = _calculate_license_statistics(tools=tools)

    stats["hasCollection"] = len([tool for tool in tools if "collectionID" in tool])
    stats["collectionCount"] = sum([len(tool["collectionID"]) for tool in tools if "collectionID" in tool])

    stats["hasLinks"] = len([tool for tool in tools if "link" in tool])
    stats["linkCount"] = sum([len(tool["link"]) for tool in tools if "link" in tool])

    stats["hasDownloads"] = len([tool for tool in tools if "download" in tool])
    stats["downloadCount"] = sum([len(tool["download"]) for tool in tools if "download" in tool])

    stats["hasDocumentation"] = len([tool for tool in tools if "documentation" in tool])
    stats["documentationCount"] = sum([len(tool["documentation"]) for tool in tools if "documentation" in tool])

    stats["hasPublications"] = len([tool for tool in tools if "publication" in tool])
    stats["publicationCount"] = sum([len(tool["publication"]) for tool in tools if "publication" in tool])

    stats["hasCredit"] = len([tool for tool in tools if "credit" in tool])
    stats["creditCount"] = sum([len(tool["credit"]) for tool in tools if "credit" in tool])

    stats["hasCommunity"] = len([tool for tool in tools if "community" in tool])
    stats["communityCount"] = sum([len(tool["community"]) for tool in tools if "community" in tool])

    stats["hasRelation"] = len([tool for tool in tools if "relation" in tool])
    stats["relationCount"] = sum([len(tool["relation"]) for tool in tools if "relation" in tool])

    return stats


def _calculate_os_statistics(tools: list) -> dict:
    """
    Calculate the Operating system statistics for the tools.

    :param tools: The list of tools.
    :return: The OS statistics.
    """
    OPERATING_SYSTEMS: List[str] = ["Mac", "Linux", "Windows"]
    os_stats: Dict[str, int] = {key: 0 for key in OPERATING_SYSTEMS}

    for systems in [tool["operatingSystem"] for tool in tools if "operatingSystem" in tool]:
        for system in systems:
            os_stats[system] += 1

    return os_stats


def _calculate_tool_type_statistics(tools: list) -> dict:
    """
    Calculate the tool type statistics for the tools.

    :param tools: The list of tools.
    :return: The tool type statistics.
    """
    TOOL_TYPES: List[str] = ["Bioinformatics portal", "Command-line tool", "Database portal", "Desktop application",
                             "Library", "Ontology", "Plug-in", "Script", "SPARQL endpoint", "Suite", "Web application",
                             "Web API", "Web service", "Workbench", "Workflow"]
    tool_type_stats: Dict[str, int] = {key: 0 for key in TOOL_TYPES}

    for tool_types in [tool["toolType"] for tool in tools if "toolType" in tool]:
        for tool_type in tool_types:
            tool_type_stats[tool_type] += 1

    return tool_type_stats


def _calculate_language_statistics(tools: list) -> dict:
    """
    Calculate the language statistics for the tools.

    :param tools: The list of tools.
    :return: The language statistics.
    """
    LANGUAGES: List[str] = ["Scala", "R", "Lua", "Haskell", "Prolog", "ActionScript", "CWL", "Smalltalk", "Perl",
                            "JavaScript", "Mathematica", "OCaml", "Verilog", "Elm", "Java", "Shell", "Ruby", "Lisp",
                            "PyMOL", "Fortran", "Visual Basic", "LabVIEW", "Racket", "Maple", "Julia", "AWK", "Delphi",
                            "MATLAB", "C++", "Python", "Forth", "Other", "SAS", "VHDL", "PHP", "JSP", "Groovy", "Bash",
                            "Ada", "C#", "SQL", "C", "Pascal", "D"]
    language_stats: Dict[str, int] = {key: 0 for key in LANGUAGES}

    for languages in [tool["language"] for tool in tools if "language" in tool]:
        for language in languages:
            language_stats[language] += 1

    return language_stats


def _calculate_license_statistics(tools: list) -> dict:
    """
    Calculate the license statistics for the tools.

    :param tools: The list of tools.
    :return: The license statistics.
    """
    LICENSE_TYPES: List[str] = ["OSIApproved", "Proprietary", "Other", "NoLicense"]
    # Obtained from: https://opensource.org/licenses/alphabetical
    OSI_APPROVED_LICENSES: List[str] = ["ISC", "CDDL-1.0", "AFL-3.0", "APL-1.0", "MPL-1.1", "OSL-2.1", "GPL-3.0",
                                        "MPL-2.0", "MIT", "Unlicense", "CECILL-2.1", "EPL-1.0", "NCSA", "GPL-2.0",
                                        "BSD-2-Clause", "Artistic-2.0", "AGPL-3.0", "LGPL-2.1", "OSL-3.0",
                                        "BSD-3-Clause", "Artistic-1.0", "Apache-2.0", "LGPL-3.0", "CPL-1.0"]
    license_stats: Dict[str, int] = {key: 0 for key in LICENSE_TYPES}

    for licens in [tool["license"] for tool in tools if "license" in tool]:
        if licens in LICENSE_TYPES:
            license_stats[licens] += 1
        elif licens == "Not licensed":
            license_stats["NoLicense"] += 1
        elif licens in OSI_APPROVED_LICENSES:
            # Check if it is an OSI approved license
            license_stats["OSIApproved"] += 1

    return license_stats
