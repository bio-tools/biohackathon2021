import json

import requests

def main():
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


if __name__ == "__main__":
    # main()
    pass
