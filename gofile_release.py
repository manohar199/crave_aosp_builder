import os
import re
import json
import requests
from datetime import datetime

GOFILE_URL = os.environ["GOFILE_URL"]
TOKEN = os.environ["GITHUB_TOKEN"]
REPO = os.environ["GITHUB_REPOSITORY"]


def extract_id(url):
    m = re.search(r"/d/([A-Za-z0-9]+)", url)
    if not m:
        raise Exception(f"Invalid GoFile URL: {url}")
    return m.group(1)


def create_guest_token():
    r = requests.post("https://api.gofile.io/accounts")
    r.raise_for_status()

    data = r.json()

    if "data" not in data:
        raise Exception(f"Failed to get GoFile token: {data}")

    return data["data"]["token"]


def get_content(content_id, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    url = (
        f"https://api.gofile.io/contents/{content_id}"
        "?contentFilter=all"
        "&page=1"
    )

    r = requests.get(url, headers=headers)
    r.raise_for_status()

    result = r.json()

    print("==== GOFILE RESPONSE ====")
    print(json.dumps(result, indent=2))
    print("=========================")

    if "data" not in result:
        raise Exception(f"Unexpected GoFile response: {result}")

    return result["data"]


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

    release = r.json()

    print("Created Release:")
    print(release["html_url"])

    return release


def download_file(url, filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()

        with open(filename, "wb") as f:
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

    print(f"Uploaded: {os.path.basename(file_path)}")


def collect_files(node):
    files = []

    # Folder
    if "children" in node:
        for child in node["children"].values():
            files.extend(collect_files(child))

    # File
    elif node.get("type") == "file":
        files.append(node)

    return files


def main():
    content_id = extract_id(GOFILE_URL)

    print("Content ID:", content_id)

    gofile_token = create_guest_token()

    data = get_content(content_id, gofile_token)

    files = collect_files(data)

    if not files:
        raise Exception(
            "No downloadable files found in GoFile response"
        )

    print(f"Found {len(files)} file(s)")

    release = create_release()

    upload_url = release["upload_url"]

    for item in files:

        name = item.get("name")
        link = item.get("link")

        if not link:
            print(f"Skipping {name} (no download link)")
            continue

        print(f"Downloading: {name}")

        download_file(link, name)

        print(f"Uploading: {name}")

        upload_asset(upload_url, name)

        try:
            os.remove(name)
        except Exception:
            pass

    print("Done")


if __name__ == "__main__":
    main()
