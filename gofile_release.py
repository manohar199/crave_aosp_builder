import os
import re
import json
import requests
from datetime import datetime

GOFILE_URL = os.environ["GOFILE_URL"]
TOKEN = os.environ["GITHUB_TOKEN"]
REPO = os.environ["GITHUB_REPOSITORY"]

def extract_id(url):
    return re.search(r"/d/([A-Za-z0-9]+)", url).group(1)

def guest_token():
    r = requests.post("https://api.gofile.io/accounts")
    return r.json()["data"]["token"]

def folder_data(content_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(
        f"https://api.gofile.io/contents/{content_id}",
        headers=headers
    )
    return r.json()["data"]

def create_release():
    tag = datetime.utcnow().strftime("gofile-%Y%m%d-%H%M%S")

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    payload = {
        "tag_name": tag,
        "name": tag,
        "draft": False,
        "prerelease": False
    }

    r = requests.post(
        f"https://api.github.com/repos/{REPO}/releases",
        headers=headers,
        json=payload
    )

    r.raise_for_status()
    return r.json()

def download(url, path):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()

        with open(path, "wb") as f:
            for chunk in r.iter_content(1024 * 1024):
                if chunk:
                    f.write(chunk)

def upload_asset(upload_url, file_path):
    upload_url = upload_url.split("{")[0]

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/octet-stream"
    }

    with open(file_path, "rb") as f:
        r = requests.post(
            f"{upload_url}?name={os.path.basename(file_path)}",
            headers=headers,
            data=f
        )

    r.raise_for_status()

token = guest_token()
content_id = extract_id(GOFILE_URL)

data = folder_data(content_id, token)

release = create_release()
upload_url = release["upload_url"]

for item in data["children"].values():

    if item["type"] != "file":
        continue

    name = item["name"]

    print("Downloading:", name)

    download(item["link"], name)

    print("Uploading:", name)

    upload_asset(upload_url, name)

    os.remove(name)

print("Done")
