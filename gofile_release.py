import os
import re
import json
import requests
from datetime import datetime

GOFILE_URL = os.getenv("GOFILE_URL")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")


def get_content_id(url):
    match = re.search(r"/d/([A-Za-zA-Z0-9]+)", url)
    if not match:
        raise Exception(f"Invalid GoFile URL: {url}")
    return match.group(1)


def get_gofile_token():
    r = requests.post("https://api.gofile.io/accounts")
    r.raise_for_status()

    data = r.json()

    if "data" not in data:
        raise Exception(f"Unable to get GoFile token\n{data}")

    return data["data"]["token"]


def get_gofile_content(content_id, token):
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

    response = r.json()

    print("===== GOFILE RESPONSE =====")
    print(json.dumps(response, indent=2))
    print("===========================")

    if "data" not in response:
        raise Exception(
            f"Unexpected GoFile response:\n{json.dumps(response, indent=2)}"
        )

    return response["data"]


def collect_files(node):
    files = []

    if not isinstance(node, dict):
        return files

    if node.get("type") == "file":
        files.append(node)
        return files

    children = node.get("children")

    if isinstance(children, dict):
        for child in children.values():
            files.extend(collect_files(child))

    return files


def create_release():
    tag = datetime.utcnow().strftime(
        "gofile-%Y%m%d-%H%M%S"
    )

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    payload = {
        "tag_name": tag,
        "name": tag,
        "draft": False,
        "prerelease": False
    }

    r = requests.post(
        f"https://api.github.com/repos/{GITHUB_REPOSITORY}/releases",
        headers=headers,
        json=payload
    )

    r.raise_for_status()

    release = r.json()

    print("Release Created:")
    print(release["html_url"])

    return release


def download_file(url, filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()

        with open(filename, "wb") as f:
            for chunk in r.iter_content(1024 * 1024):
                if chunk:
                    f.write(chunk)


def upload_asset(upload_url, filepath):
    upload_url = upload_url.split("{")[0]

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/octet-stream"
    }

    with open(filepath, "rb") as f:
        r = requests.post(
            f"{upload_url}?name={os.path.basename(filepath)}",
            headers=headers,
            data=f
        )

    r.raise_for_status()

    print(
        f"Uploaded: {os.path.basename(filepath)}"
    )


def main():
    if not GOFILE_URL:
        raise Exception("GOFILE_URL missing")

    content_id = get_content_id(GOFILE_URL)

    print(f"Content ID: {content_id}")

    token = get_gofile_token()

    data = get_gofile_content(
        content_id,
        token
    )

    files = collect_files(data)

    if not files:
        print("No files detected.")
        print(json.dumps(data, indent=2))
        raise Exception(
            "GoFile returned no downloadable files."
        )

    print(f"Found {len(files)} files")

    release = create_release()

    upload_url = release["upload_url"]

    for file_info in files:

        name = file_info.get("name")
        link = file_info.get("link")

        if not link:
            print(f"Skipping {name}")
            continue

        print(f"Downloading {name}")

        download_file(link, name)

        print(f"Uploading {name}")

        upload_asset(upload_url, name)

        try:
            os.remove(name)
        except Exception:
            pass

    print("Completed Successfully")


if __name__ == "__main__":
    main()
