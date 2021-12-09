"""
The script for calculating the different statistics for a given tool list.
"""
from datetime import datetime
from typing import Dict, Union, List

from ._utilities import clean_and_filter_tool_list
from ._spdx_license_parser import parse_license_list, LicensesData


def calculate_general_statistics(tools: list, upper_time_limit: datetime = datetime.today()):
    """
    Calculate the general statistics for a list of tools.

    :param tools: The list of tools.
    :param upper_time_limit: Calculate the statistics for tools added up to the time limit.
        Default: datetime.datetime.today()
    :return: The dictionary with the statistics.
    """
    # Clean the list of tools
    tools = clean_and_filter_tool_list(raw_tools=tools, upper_time_limit=upper_time_limit)

    # Create the dictionary to hold the statistics and calculate the statistics
    stats: Dict[str, Union[str, int, Dict[str, int]]] = {}
    stats["date"] = upper_time_limit.isoformat(timespec="seconds")
    stats["toolCount"] = len(tools)

    stats["hasToolType"] = len([tool for tool in tools if "toolType" in tool])
    stats["toolTypeCount"] = sum([len(tool["toolType"]) for tool in tools if "toolType" in tool])
    stats["toolTypes"] = _calculate_tool_type_statistics(tools=tools)

    stats["hasTopic"] = len([tool for tool in tools if "topic" in tool])
    stats["topicCount"] = sum([len(tool["topic"]) for tool in tools if "topic" in tool])

    stats["hasOperatingSystem"] = len([tool for tool in tools if "operatingSystem" in tool])
    stats["operatingSystemCount"] = sum([len(tool["operatingSystem"]) for tool in tools if "operatingSystem" in tool])
    stats["operatingSystem"] = _calculate_os_statistics(tools=tools)

    stats["hasLanguage"] = len([tool for tool in tools if "language" in tool])
    stats["languageCount"] = sum([len(tool["language"]) for tool in tools if "language" in tool])
    stats["languages"] = _calculate_language_statistics(tools=tools)

    stats["hasLicense"] = len([tool for tool in tools if "license" in tool])
    stats["licenses"] = _calculate_license_statistics(tools=tools)

    stats["hasMaturity"] = len([tool for tool in tools if "maturity" in tool])
    stats["maturity"] = _calculate_maturity_statistics(tools=tools)

    stats["hasCost"] = len([tool for tool in tools if "cost" in tool])
    stats["costs"] = _calculate_cost_statistics(tools=tools)

    stats["hasCollection"] = len([tool for tool in tools if "collectionID" in tool])
    stats["collectionCount"] = sum([len(tool["collectionID"]) for tool in tools if "collectionID" in tool])

    stats["hasCodeAccessibility"] = len([tool for tool in tools if "accessibility" in tool])
    stats["accessibility"] = _calculate_code_accessibility_statistics(tools=tools)

    stats["hasElixirPlatform"] = len([tool for tool in tools if "elixirPlatform" in tool])
    stats["elixirPlatformCount"] = sum([len(tool["elixirPlatform"]) for tool in tools if "elixirPlatform" in tool])
    stats["elixirPlatform"] = _calculate_elixir_platform_statistics(tools=tools)

    stats["hasElixirNode"] = len([tool for tool in tools if "elixirNode" in tool])
    stats["elixirNodeCount"] = sum([len(tool["elixirNode"]) for tool in tools if "elixirNode" in tool])
    stats["elixirNodes"] = _calculate_elixir_node_statistics(tools=tools)

    stats["hasElixirCommunity"] = len([tool for tool in tools if "elixirCommunity" in tool])
    stats["elixirCommunityCount"] = sum([len(tool["elixirCommunity"]) for tool in tools if "elixirCommunity" in tool])
    stats["elixirCommunity"] = _calculate_elixir_community_statistics(tools=tools)

    stats["hasLinks"] = len([tool for tool in tools if "link" in tool])
    stats["linkCount"] = sum([len(tool["link"]) for tool in tools if "link" in tool])
    stats["linkTypes"] = _calculate_link_type_statistics(tools=tools)

    stats["hasDownloads"] = len([tool for tool in tools if "download" in tool])
    stats["downloadCount"] = sum([len(tool["download"]) for tool in tools if "download" in tool])
    stats["downloadTypes"] = _calculate_download_type_statistics(tools=tools)

    stats["hasDocumentation"] = len([tool for tool in tools if "documentation" in tool])
    stats["documentationCount"] = sum([len(tool["documentation"]) for tool in tools if "documentation" in tool])
    stats["documentationTypes"] = _calculate_documentation_type_statistics(tools=tools)

    stats["hasPublications"] = len([tool for tool in tools if "publication" in tool])
    stats["publicationCount"] = sum([len(tool["publication"]) for tool in tools if "publication" in tool])
    stats["publicationTypes"] = _calculate_publication_type_statistics(tools=tools)

    stats["hasCredit"] = len([tool for tool in tools if "credit" in tool])
    stats["creditCount"] = sum([len(tool["credit"]) for tool in tools if "credit" in tool])
    stats["creditRoleTypes"] = _calculate_credit_role_type_statistics(tools=tools)

    stats["hasRelation"] = len([tool for tool in tools if "relation" in tool])
    stats["relationCount"] = sum([len(tool["relation"]) for tool in tools if "relation" in tool])
    stats["relations"] = _calculate_relation_statistics(tools=tools)

    stats["hasBiolib"] = len([tool for tool in tools if "community" in tool])
    stats["BiolibCount"] = sum([len(tool["community"]) for tool in tools if "community" in tool])

    return stats


def _calculate_tool_type_statistics(tools: list) -> dict:
    """
    Calculate the tool type statistics for the tools.

    :param tools: The list of tools.
    :return: The tool type statistics.
    """
    # TODO: Consider non-hardcoded approach
    TOOL_TYPES: List[str] = ["Bioinformatics portal", "Command-line tool", "Database portal", "Desktop application",
                             "Library", "Ontology", "Plug-in", "Script", "SPARQL endpoint", "Suite", "Web application",
                             "Web API", "Web service", "Workbench", "Workflow"]
    tool_type_stats: Dict[str, int] = {key: 0 for key in TOOL_TYPES}

    for tool_types in [tool["toolType"] for tool in tools if "toolType" in tool]:
        for tool_type in tool_types:
            tool_type_stats[tool_type] += 1

    return tool_type_stats


def _calculate_os_statistics(tools: list) -> dict:
    """
    Calculate the Operating system statistics for the tools.

    :param tools: The list of tools.
    :return: The OS statistics.
    """
    # TODO: Consider non-hardcoded approach
    OPERATING_SYSTEMS: List[str] = ["Mac", "Linux", "Windows"]
    os_stats: Dict[str, int] = {key: 0 for key in OPERATING_SYSTEMS}

    for systems in [tool["operatingSystem"] for tool in tools if "operatingSystem" in tool]:
        for system in systems:
            os_stats[system] += 1

    return os_stats


def _calculate_language_statistics(tools: list) -> dict:
    """
    Calculate the language statistics for the tools.

    :param tools: The list of tools.
    :return: The language statistics.
    """
    # TODO: Consider non-hardcoded approach
    LANGUAGES: List[str] = ["ActionScript", "Ada", "AppleScript", "Assembly language", "AWK", "Bash", "C", "C#", "C++",
                            "COBOL", "ColdFusion", "CWL", "D", "Delphi", "Dylan", "Eiffel", "Elm", "Forth", "Fortran",
                            "Groovy", "Haskell", "Icarus", "Java", "JavaScript", "JSP", "Julia", "LabVIEW", "Lisp",
                            "Lua", "Maple", "Mathematica", "MATLAB", "MLXTRAN", "NMTRAN", "OCaml", "Pascal", "Perl",
                            "PHP", "Prolog", "PyMOL", "Python", "R", "Racket", "REXX", "Ruby", "SAS", "Scala", "Scheme",
                            "Shell", "Smalltalk", "SQL", "Turing", "Verilog", "VHDL", "Visual Basic", "XAML", "Other"]
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
    license_info: LicensesData = parse_license_list()

    LICENSE_TYPES: List[str] = ["OSIApproved", "FSFApproved", "Freeware", "Proprietary", "Other", "NoLicense",
                                "DeprecatedIdentifier"] + license_info.licenses_list
    OSI_APPROVED_LICENSES: List[str] = license_info.osi_approved_licenses
    FSF_APPROVED_LICENSES: List[str] = license_info.fsf_approved_licenses
    DEPRECATED_LICENSE_IDENTIFIERS: List[str] = license_info.deprecated_licenses

    license_stats: Dict[str, int] = {key: 0 for key in LICENSE_TYPES}

    for licens in [tool["license"] for tool in tools if "license" in tool]:
        if licens in LICENSE_TYPES:
            license_stats[licens] += 1
        elif licens == "Not licensed":
            license_stats["NoLicense"] += 1
        if licens in OSI_APPROVED_LICENSES:
            # Check if it is an OSI approved license
            license_stats["OSIApproved"] += 1
        if licens in FSF_APPROVED_LICENSES:
            # Check if it is an FSF approved license
            license_stats["FSFApproved"] += 1
        if licens in DEPRECATED_LICENSE_IDENTIFIERS:
            # Check if the license has a deprecated license identifier
            license_stats["DeprecatedIdentifier"] += 1
    return license_stats


def _calculate_maturity_statistics(tools: list) -> dict:
    """
    Calculate the code accessibility statistics for the tools.

    :param tools: The list of tools.
    :return: The code accessibility language statistics.
    """
    # TODO: Consider non-hardcoded approach
    MATURITY: List[str] = ["Emerging", "Mature", "Legacy"]
    maturity_stats: Dict[str, int] = {key: 0 for key in MATURITY}

    for maturity in [tool["maturity"] for tool in tools if "maturity" in tool]:
        maturity_stats[maturity] += 1

    return maturity_stats


def _calculate_cost_statistics(tools: list) -> dict:
    """
    Calculate the cost statistics for the tools.

    :param tools: The list of tools.
    :return: The cost statistics.
    """
    # TODO: Consider non-hardcoded approach
    COSTS: List[str] = ["Free of charge", "Free of charge (with restrictions)", "Commercial"]
    cost_stats: Dict[str, int] = {key: 0 for key in COSTS}

    for cost in [tool["cost"] for tool in tools if "cost" in tool]:
        cost_stats[cost] += 1

    return cost_stats


def _calculate_code_accessibility_statistics(tools: list) -> dict:
    """
    Calculate the code accessibility statistics for the tools.

    :param tools: The list of tools.
    :return: The code accessibility language statistics.
    """
    # TODO: Consider non-hardcoded approach
    ACCESSIBILITY: List[str] = ["Restricted access", "Open access", "Open access (with restrictions)"]
    accessibility_stats: Dict[str, int] = {key: 0 for key in ACCESSIBILITY}

    for accessibility in [tool["accessibility"] for tool in tools if "accessibility" in tool]:
        accessibility_stats[accessibility] += 1

    return accessibility_stats


def _calculate_elixir_platform_statistics(tools: list) -> dict:
    """
    Calculate the ELIXIR platform statistics for the tools.

    :param tools: The list of tools.
    :return: The ELIXIR platform statistics.
    """
    # TODO: Consider non-hardcoded approach
    PLATFORMS: List[str] = ["Data", "Tools", "Compute", "Interoperability", "Training"]
    platform_stats: Dict[str, int] = {key: 0 for key in PLATFORMS}

    for platforms in [tool["elixirPlatform"] for tool in tools if "elixirPlatform" in tool]:
        for platform in platforms:
            platform_stats[platform] += 1

    return platform_stats


def _calculate_elixir_node_statistics(tools: list) -> dict:
    """
    Calculate the ELIXIR node statistics for the tools.

    :param tools: The list of tools.
    :return: The ELIXIR node statistics.
    """
    # TODO: Consider non-hardcoded approach
    NODES: List[str] = ["Belgium", "Czech Republic", "Denmark", "EMBL", "Estonia", "Finland", "France", "Germany",
                        "Greece", "Hungary", "Ireland", "Israel", "Italy", "Luxembourg", "Netherlands", "Norway",
                        "Portugal", "Slovenia", "Spain", "Sweden", "Switzerland", "UK"]
    node_stats: Dict[str, int] = {key: 0 for key in NODES}

    for nodes in [tool["elixirNode"] for tool in tools if "elixirNode" in tool]:
        for node in nodes:
            node_stats[node] += 1

    return node_stats


def _calculate_elixir_community_statistics(tools: list) -> dict:
    """
    Calculate the ELIXIR community statistics for the tools.

    :param tools: The list of tools.
    :return: The ELIXIR community statistics.
    """
    # TODO: Consider non-hardcoded approach
    COMMUNITY: List[str] = ["3D-BioInfo", "Federated Human Data", "Galaxy", "Human Copy Number Variation",
                            "Intrinsically Disordered Proteins", "Marine Metagenomics", "Metabolomics",
                            "Microbial Biotechnology", "Plant Sciences", "Proteomics", "Rare Diseases"]
    community_stats: Dict[str, int] = {key: 0 for key in COMMUNITY}

    for communities in [tool["elixirCommunity"] for tool in tools if "elixirCommunity" in tool]:
        for community in communities:
            community_stats[community] += 1

    return community_stats


def _calculate_link_type_statistics(tools: list) -> dict:
    """
    Calculate the link type statistics for the tools.

    :param tools: The list of tools.
    :return: The link type statistics.
    """
    # TODO: Consider non-hardcoded approach
    LINK_TYPES: List[str] = ["Discussion forum", "Galaxy service", "Helpdesk", "Issue tracker", "Mailing list",
                             "Mirror", "Software catalogue", "Repository", "Social media", "Service",
                             "Technical monitoring", "Other"]
    link_type_stats: Dict[str, int] = {key: 0 for key in LINK_TYPES}

    for links in [tool["link"] for tool in tools if "link" in tool]:
        for link in links:
            for link_type in [t for t in link["type"]]:
                link_type_stats[link_type] += 1

    return link_type_stats


def _calculate_download_type_statistics(tools: list) -> dict:
    """
    Calculate the download type statistics for the tools.

    :param tools: The list of tools.
    :return: The download type statistics.
    """
    # TODO: Consider non-hardcoded approach
    DOWNLOAD_TYPES: List[str] = ["API specification", "Biological data", "Binaries", "Command-line specification",
                                 "Container file", "Icon", "Screenshot", "Source code", "Software package", "Test data",
                                 "Test script", "Tool wrapper (CWL)", "Tool wrapper (Galaxy)", "Tool wrapper (Taverna)",
                                 "Tool wrapper (Other)", "VM image", "Downloads page", "Other"]
    download_type_stats: Dict[str, int] = {key: 0 for key in DOWNLOAD_TYPES}

    for downloads in [tool["download"] for tool in tools if "download" in tool]:
        for download in downloads:
            download_type_stats[download["type"]] += 1

    return download_type_stats


def _calculate_documentation_type_statistics(tools: list) -> dict:
    """
    Calculate the documentation type statistics for the tools.

    :param tools: The list of tools.
    :return: The documentation type statistics.
    """
    # TODO: Consider non-hardcoded approach
    DOCUMENTATION_TYPES: List[str] = ["API documentation", "Citation instructions", "Code of conduct",
                                      "Command-line options", "Contributions policy", "FAQ", "General",
                                      "Governance", "Installation instructions", "Quick start guide", "Release notes",
                                      "Terms of use", "Training material", "User manual", "Other"]
    documentation_type_stats: Dict[str, int] = {key: 0 for key in DOCUMENTATION_TYPES}

    for documentations in [tool["documentation"] for tool in tools if "documentation" in tool]:
        for documentation in documentations:
            for link_type in [t for t in documentation["type"]]:
                documentation_type_stats[link_type] += 1

    return documentation_type_stats


def _calculate_publication_type_statistics(tools: list) -> dict:
    """
    Calculate the publication type statistics for the tools.

    :param tools: The list of tools.
    :return: The publication type statistics.
    """
    # TODO: Consider non-hardcoded approach
    PUBLICATION_TYPES: List[str] = ["Primary", "Method", "Usage", "Benchmarking study", "Review", "Other"]
    publication_type_stats: Dict[str, int] = {key: 0 for key in PUBLICATION_TYPES}

    for publications in [tool["publication"] for tool in tools if "publication" in tool]:
        for publication in [pub for pub in publications if "type" in pub]:
            for pub_type in [t for t in publication["type"]]:
                publication_type_stats[pub_type] += 1

    return publication_type_stats


def _calculate_credit_role_type_statistics(tools: list) -> dict:
    """
    Calculate the credit role type statistics for the tools.

    :param tools: The list of tools.
    :return: The credit role type statistics.
    """
    # TODO: Consider non-hardcoded approach
    CREDIT_ROLE_TYPES: List[str] = ["Developer", "Maintainer", "Provider", "Documentor", "Contributor", "Support",
                                    "Primary contact"]
    credit_role_type_stats: Dict[str, int] = {key: 0 for key in CREDIT_ROLE_TYPES}

    for creds in [tool["credit"] for tool in tools if "credit" in tool]:
        for credit in creds:
            for credit_type in [t for t in credit["typeRole"] if "typeRole" in credit]:
                credit_role_type_stats[credit_type] += 1
    return credit_role_type_stats


def _calculate_relation_statistics(tools: list) -> dict:
    """
    Calculate the relation statistics for the tools.

    :param tools: The list of tools.
    :return: The relation statistics.
    """
    # TODO: Consider non-hardcoded approach
    RELATION_TYPES: List[str] = ["isNewVersionOf", "hasNewVersion", "uses", "usedBy", "includes", "includedIn"]
    relation_stats: Dict[str, int] = {key: 0 for key in RELATION_TYPES}

    for relations in [tool["relation"] for tool in tools if "relation" in tool]:
        for relation in relations:
            relation_stats[relation["type"]] += 1

    return relation_stats
