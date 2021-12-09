"""
The script for calculating the different statistics for a given tool list.
"""
from datetime import datetime
from typing import Dict, Union, List

from ._utilities import clean_and_filter_tool_list


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
    # TODO: Consider non-hardcoded approach
    LICENSE_TYPES: List[str] = ["OSIApproved", "FSFApproved", "Freeware", "Proprietary", "Other", "NoLicense",
                                "DeprecatedIdentifier", "0BSD", "AAL", "ADSL", "AFL-1.1", "AFL-1.2", "AFL-2.0",
                                "AFL-2.1", "AFL-3.0", "AGPL-1.0", "AGPL-3.0", "AMDPLPA", "AML", "AMPAS", "ANTLR-PD",
                                "APAFML", "APL-1.0", "APSL-1.0", "APSL-1.1", "APSL-1.2", "APSL-2.0", "Abstyles",
                                "Adobe-2006", "Adobe-Glyph", "Afmparse", "Aladdin", "Apache-1.0", "Apache-1.1",
                                "Apache-2.0", "Artistic-1.0", "Artistic-1.0-Perl", "Artistic-1.0-cl8", "Artistic-2.0",
                                "BSD-2-Clause", "BSD-2-Clause-FreeBSD", "BSD-2-Clause-NetBSD", "BSD-3-Clause",
                                "BSD-3-Clause-Attribution", "BSD-3-Clause-Clear", "BSD-3-Clause-LBNL",
                                "BSD-3-Clause-No-Nuclear-License", "BSD-3-Clause-No-Nuclear-License-2014",
                                "BSD-3-Clause-No-Nuclear-Warranty", "BSD-4-Clause", "BSD-4-Clause-UC", "BSD-Protection",
                                "BSD-Source-Code", "BSL-1.0", "Bahyph", "Barr", "Beerware", "BitTorrent-1.0",
                                "BitTorrent-1.1", "Borceux", "CATOSL-1.1", "CC-BY-1.0", "CC-BY-2.0", "CC-BY-2.5",
                                "CC-BY-3.0", "CC-BY-4.0", "CC-BY-NC-1.0", "CC-BY-NC-2.0", "CC-BY-NC-2.5",
                                "CC-BY-NC-3.0", "CC-BY-NC-4.0", "CC-BY-NC-ND-1.0", "CC-BY-NC-ND-2.0", "CC-BY-NC-ND-2.5",
                                "CC-BY-NC-ND-3.0", "CC-BY-NC-ND-4.0", "CC-BY-NC-SA-1.0", "CC-BY-NC-SA-2.0",
                                "CC-BY-NC-SA-2.5", "CC-BY-NC-SA-3.0", "CC-BY-NC-SA-4.0", "CC-BY-ND-1.0",
                                "CC-BY-ND-2.0", "CC-BY-ND-2.5", "CC-BY-ND-3.0", "CC-BY-ND-4.0", "CC-BY-SA-1.0",
                                "CC-BY-SA-2.0", "CC-BY-SA-2.5", "CC-BY-SA-3.0", "CC-BY-SA-4.0", "CC0-1.0", "CDDL-1.0",
                                "CDDL-1.1", "CECILL-1.0", "CECILL-1.1", "CECILL-2.0", "CECILL-2.1", "CECILL-B",
                                "CECILL-C", "CNRI-Jython", "CNRI-Python", "CNRI-Python-GPL-Compatible", "CPAL-1.0",
                                "CPL-1.0", "CPOL-1.02", "CUA-OPL-1.0", "Caldera", "ClArtistic", "Condor-1.1",
                                "Crossword", "CrystalStacker", "Cube", "D-FSL-1.0", "DOC", "DSDP", "Dotseqn",
                                "ECL-1.0", "ECL-2.0", "EFL-1.0", "EFL-2.0", "EPL-1.0", "EUDatagrid", "EUPL-1.0",
                                "EUPL-1.1", "Entessa", "ErlPL-1.1", "Eurosym", "FSFAP", "FSFUL", "FSFULLR", "FTL",
                                "Fair", "Frameworx-1.0", "FreeImage", "GFDL-1.1", "GFDL-1.2", "GFDL-1.3", "GL2PS",
                                "GPL-1.0", "GPL-2.0", "GPL-3.0", "Giftware", "Glide", "Glulxe", "HPND", "HaskellReport",
                                "IBM-pibs", "ICU", "IJG", "IPA", "IPL-1.0", "ISC", "ImageMagick", "Imlib2", "Info-ZIP",
                                "Intel", "Intel-ACPI", "Interbase-1.0", "JSON", "JasPer-2.0", "LAL-1.2", "LAL-1.3",
                                "LGPL-2.0", "LGPL-2.1", "LGPL-3.0", "LGPLLR", "LPL-1.0", "LPL-1.02", "LPPL-1.0",
                                "LPPL-1.1", "LPPL-1.2", "LPPL-1.3a", "LPPL-1.3c", "Latex2e", "Leptonica", "LiLiQ-P-1.1",
                                "LiLiQ-R-1.1", "LiLiQ-Rplus-1.1", "Libpng", "MIT", "MIT-CMU", "MIT-advertising",
                                "MIT-enna", "MIT-feh", "MITNFA", "MPL-1.0", "MPL-1.1", "MPL-2.0",
                                "MPL-2.0-no-copyleft-exception", "MS-PL", "MS-RL", "MTLL", "MakeIndex", "MirOS",
                                "Motosoto", "Multics", "Mup", "NASA-1.3", "NBPL-1.0", "NCSA", "NGPL", "NLOD-1.0",
                                "NLPL", "NOSL", "NPL-1.0", "NPL-1.1", "NPOSL-3.0", "NRL", "NTP", "Naumen", "NetCDF",
                                "Newsletr", "Nokia", "Noweb", "Nunit", "OCCT-PL", "OCLC-2.0", "ODbL-1.0", "OFL-1.0",
                                "OFL-1.1", "OGTSL", "OLDAP-1.1", "OLDAP-1.2", "OLDAP-1.3", "OLDAP-1.4", "OLDAP-2.0",
                                "OLDAP-2.0.1", "OLDAP-2.1", "OLDAP-2.2", "OLDAP-2.2.1", "OLDAP-2.2.2", "OLDAP-2.3",
                                "OLDAP-2.4", "OLDAP-2.5", "OLDAP-2.6", "OLDAP-2.7", "OLDAP-2.8", "OML", "OPL-1.0",
                                "OSET-PL-2.1", "OSL-1.0", "OSL-1.1", "OSL-2.0", "OSL-2.1", "OSL-3.0", "OpenSSL",
                                "PDDL-1.0", "PHP-3.0", "PHP-3.01", "Plexus", "PostgreSQL", "Python-2.0", "QPL-1.0",
                                "Qhull", "RHeCos-1.1", "RPL-1.1", "RPL-1.5", "RPSL-1.0", "RSA-MD", "RSCPL", "Rdisc",
                                "Ruby", "SAX-PD", "SCEA", "SGI-B-1.0", "SGI-B-1.1", "SGI-B-2.0", "SISSL", "SISSL-1.2",
                                "SMLNJ", "SMPPL", "SNIA", "SPL-1.0", "SWL", "Saxpath", "Sendmail", "SimPL-2.0",
                                "Sleepycat", "Spencer-86", "Spencer-94", "Spencer-99", "SugarCRM-1.1.3", "TCL", "TMate",
                                "TORQUE-1.1", "TOSL", "UPL-1.0", "Unicode-TOU", "Unlicense", "VOSTROM", "VSL-1.0",
                                "Vim", "W3C", "W3C-19980720", "WTFPL", "Watcom-1.0", "Wsuipa", "X11", "XFree86-1.1",
                                "XSkat", "Xerox", "Xnet", "YPL-1.0", "YPL-1.1", "ZPL-1.1", "ZPL-2.0", "ZPL-2.1", "Zed",
                                "Zend-2.0", "Zimbra-1.3", "Zimbra-1.4", "Zlib", "bzip2-1.0.5", "bzip2-1.0.6", "curl",
                                "diffmark", "dvipdfm", "eGenix", "gSOAP-1.3b", "gnuplot", "iMatix", "libtiff", "mpich2",
                                "psfrag", "psutils", "xinetd", "xpp", "zlib-acknowledgement"]
    OSI_APPROVED_LICENSES: List[str] = ["0BSD", "AAL", "APL-1.0", "APSL-1.0", "APSL-1.1", "APSL-1.2", "Artistic-1.0",
                                        "Artistic-1.0-cl8", "Artistic-1.0-Perl", "BSD-1-Clause", "BSD-2-Clause-Patent",
                                        "BSD-3-Clause-LBNL", "CAL-1.0", "CAL-1.0-Combined-Work-Exception", "CATOSL-1.1",
                                        "CECILL-2.1", "CERN-OHL-P-2.0", "CERN-OHL-S-2.0", "CERN-OHL-W-2.0",
                                        "CNRI-Python", "CUA-OPL-1.0", "ECL-1.0", "EFL-1.0", "Entessa", "Fair",
                                        "Frameworx-1.0", "LGPL-2.0-only", "LGPL-2.0-or-later", "LiLiQ-P-1.1",
                                        "LiLiQ-R-1.1", "LiLiQ-Rplus-1.1", "LPL-1.0", "LPPL-1.3c", "MirOS", "MIT-0",
                                        "MIT-Modern-Variant", "Motosoto", "MPL-1.0", "MPL-2.0-no-copyleft-exception",
                                        "MulanPSL-2.0", "Multics", "NASA-1.3", "Naumen", "NGPL", "NPOSL-3.0", "NTP",
                                        "OCLC-2.0", "OFL-1.1-no-RFN", "OFL-1.1-RFN", "OGTSL", "OLDAP-2.8",
                                        "OSET-PL-2.1", "PHP-3.0", "PostgreSQL", "RPL-1.1", "RPL-1.5", "RSCPL",
                                        "SimPL-2.0", "UCL-1.0", "Unicode-DFS-2016", "VSL-1.0", "Watcom-1.0", "Xnet",
                                        "AFL-1.1", "AFL-1.2", "AFL-2.0", "AFL-2.1", "AFL-3.0", "AGPL-3.0-only",
                                        "AGPL-3.0-or-later", "Apache-1.1", "Apache-2.0", "APSL-2.0", "Artistic-2.0",
                                        "BSD-2-Clause", "BSD-3-Clause", "BSL-1.0", "CDDL-1.0", "CPAL-1.0", "CPL-1.0",
                                        "ECL-2.0", "EFL-2.0", "EPL-1.0", "EPL-2.0", "EUDatagrid", "EUPL-1.1",
                                        "EUPL-1.2", "GPL-2.0-only", "GPL-2.0-or-later", "GPL-3.0-only",
                                        "GPL-3.0-or-later", "HPND", "Intel", "IPA", "IPL-1.0", "ISC",
                                        "LGPL-2.1-only", "LGPL-2.1-or-later", "LGPL-3.0-only", "LGPL-3.0-or-later",
                                        "LPL-1.02", "MIT", "MPL-1.1", "MPL-2.0", "MS-PL", "MS-RL", "NCSA", "Nokia",
                                        "OFL-1.1", "OSL-1.0", "OSL-2.0", "OSL-2.1", "OSL-3.0", "PHP-3.01", "Python-2.0",
                                        "QPL-1.0", "RPSL-1.0", "SISSL", "Sleepycat", "SPL-1.0", "Unlicense", "UPL-1.0",
                                        "W3C", "Zlib", "ZPL-2.0", "ZPL-2.1"]
    FSF_APPROVED_LICENSES: List[str] = ["ZPL-2.1", "ZPL-2.0", "Zlib", "Zimbra-1.3", "Zend-2.0", "YPL-1.1", "xinetd",
                                        "XFree86-1.1", "X11", "WTFPL", "W3C", "Vim", "UPL-1.0", "Unlicense", "SPL-1.0",
                                        "SMLNJ", "Sleepycat", "SISSL", "SGI-B-2.0", "Ruby", "RPSL-1.0", "QPL-1.0",
                                        "Python-2.0", "PHP-3.01", "OSL-3.0", "OSL-2.1", "OSL-2.0", "OSL-1.1", "OSL-1.0",
                                        "OpenSSL", "OLDAP-2.7", "OLDAP-2.3", "OFL-1.1", "OFL-1.0", "ODbL-1.0",
                                        "NPL-1.1", "NPL-1.0", "NOSL", "Nokia", "NCSA", "MS-RL", "MS-PL", "MPL-2.0",
                                        "MPL-1.1", "MIT", "LPPL-1.3a", "LPPL-1.2", "LPL-1.02", "LGPL-3.0-or-later",
                                        "LGPL-3.0-only", "LGPL-2.1-or-later", "LGPL-2.1-only", "ISC", "IPL-1.0", "IPA",
                                        "Intel", "Imlib2", "iMatix", "IJG", "HPND", "GPL-3.0-or-later", "GPL-3.0-only",
                                        "GPL-2.0-or-later", "GPL-2.0-only", "gnuplot", "GFDL-1.3-or-later",
                                        "GFDL-1.3-only", "GFDL-1.2-or-later", "GFDL-1.2-only", "GFDL-1.1-or-later",
                                        "GFDL-1.1-only", "FTL", "FSFAP", "EUPL-1.2", "EUPL-1.1", "EUDatagrid",
                                        "EPL-2.0", "EPL-1.0", "EFL-2.0", "ECL-2.0", "CPL-1.0", "CPAL-1.0", "Condor-1.1",
                                        "ClArtistic", "CECILL-C", "CECILL-B", "CECILL-2.0", "CDDL-1.0", "CC0-1.0",
                                        "CC-BY-SA-4.0", "CC-BY-4.0", "BSL-1.0", "BSD-4-Clause", "BSD-3-Clause-Clear",
                                        "BSD-3-Clause", "BSD-2-Clause", "BitTorrent-1.1", "Artistic-2.0", "APSL-2.0",
                                        "Apache-2.0", "Apache-1.1", "Apache-1.0", "AGPL-3.0-or-later", "AGPL-3.0-only",
                                        "AFL-3.0", "AFL-2.1", "AFL-2.0", "AFL-1.2", "AFL-1.1"]
    DEPRECATED_LICENSE_IDENTIFIERS: List[str] = ["AGPL-1.0", "AGPL-3.0", "BSD-2-Clause-FreeBSD", "BSD-2-Clause-NetBSD",
                                                 "eCos-2.0", "GFDL-1.1", "GFDL-1.2", "GFDL-1.3", "GPL-1.0", "GPL-1.0+",
                                                 "GPL-2.0", "GPL-2.0+", "GPL-2.0-with-autoconf-exception",
                                                 "GPL-2.0-with-bison-exception", "GPL-2.0-with-classpath-exception",
                                                 "GPL-2.0-with-font-exception", "GPL-2.0-with-GCC-exception", "GPL-3.0",
                                                 "GPL-3.0+", "GPL-3.0-with-autoconf-exception",
                                                 "GPL-3.0-with-GCC-exception", "LGPL-2.0", "LGPL-2.0+", "LGPL-2.1",
                                                 "LGPL-2.1+", "LGPL-3.0", "LGPL-3.0+", "Nunit", "StandardML-NJ",
                                                 "wxWindows"]
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
