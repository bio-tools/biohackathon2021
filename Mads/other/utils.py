import json

import requests


def download_whole_biotools():
    url: str = "https://bio.tools/api/t/?format=json"
    tools: list = []
    next_page: str = ""
    page_number: int = 1
    while next_page is not None:
        print(f"Page number: {page_number}")
        resp = requests.get(url + next_page.replace("?", "&"))
        resp.raise_for_status()
        data = resp.json()
        tools.extend(data["list"])
        next_page = data["next"]
        page_number += 1

    print(len(tools))

    with open("Resources/FullTools.json", "w") as f:
        f.write(json.dumps(tools))


def get_certain_tools():
    with open("Resources/FullCollection/FullTools.json", "r") as f:
        tools = json.load(f)

    with open("Resources/electron_microscopy_domain.txt", "r") as f:
        tools_ids = [tool_id.lower().strip() for tool_id in f.readlines()]
    tool_collection = [tool for tool in tools if tool["biotoolsID"].lower() in tools_ids]

    with open("Resources/ElectronMicroscopyTools.json", "w") as f:
        f.write(json.dumps(tool_collection))



def main():
    get_certain_tools()


if __name__ == "__main__":
    main()
    pass
