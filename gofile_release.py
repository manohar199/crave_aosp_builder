import os
import re
import json
import requests
from datetime import datetime

GOFILE_URL = os.environ["GOFILE_URL"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GITHUB_REPOSITORY = os.environ["GITHUB_REPOSITORY"]


def get_content_id(url):
    match = re.search(r"/d/([A-Za-z0-9]+)", url)
    if not match:
        raise Exception(f"Invalid GoFile URL: {url}")
    return match.group(1)


def get_gofile_token():
    r = requests.post(
        "https://api.gofile.io/accounts",
        timeout=30
    )
    r.raise_for_status()

    data = r.json()

    if "data" not in data or "token" not in data["data"]:
        raise Exception(
            f"Unable to get GoFile token:\n{json.dumps(data, indent=2)}"
        )

    return data["data"]["token"]


def get_content(content_id, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    urls = [
        f"https://api.gofile.io/contents/{content_id}?contentFilter=all&page=1",
        f"https://api.gofile.io/contents/{content_id}"
    ]

    last_response = None

    for url in urls:
        try:
            r = requests.get(
                url,
                headers=headers,
                timeout=60
            )
            r.raise_for_status()

            response = r.json()
            last_response = response

            print(json.dumps(response, indent=2))

            if "data" in response:
                return response["data"]

        except Exception as e:
            print(e)

    raise Exception(
        f"Failed to get content:\n{json.dumps(last_response, indent=2) if last_response else 'No response'}"
    )


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

    if node.get("link"):
        files.append(node)

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
        json=payload,
        timeout=60
    )

    r.raise_for_status()

    return r.json()


def download_file(url, filename):
    with requests.get(url, stream=True, timeout=600) as r:
        r.raise_for_status()

        with open(filename, "wb") as f:
            for chunk in r.iter_content(1024 * 1024):
                if chunk:
                    f.write(chunk)


def upload_asset(upload_url, file_path):
    upload_url = upload_url.split("{")[0]

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/octet-stream"
    }

    with open(file_path, "rb") as f:
        r = requests.post(
            f"{upload_url}?name={os.path.basename(file_path)}",
            headers=headers,
            data=f,
            timeout=3600
        )

    r.raise_for_status()

    print(f"Uploaded: {os.path.basename(file_path)}")


def main():
    content_id = get_content_id(GOFILE_URL)

    print(f"Content ID: {content_id}")

    token = get_gofile_token()

    data = get_content(content_id, token)

    files = collect_files(data)

    unique = []
    seen = set()

    for item in files:
        link = item.get("link")

        if link and link not in seen:
            seen.add(link)
            unique.append(item)

    files = unique

    if not files:
        raise Exception(
            "No downloadable files found.\n"
            + json.dumps(data, indent=2)
        )

    print(f"Found {len(files)} file(s)")

    release = create_release()

    upload_url = release["upload_url"]

    for item in files:
        name = item.get("name", "file.bin")
        link = item.get("link")

        if not link:
            continue

        print(f"Downloading: {name}")

        download_file(link, name)

        print(f"Uploading: {name}")

        upload_asset(upload_url, name)

        try:
            os.remove(name)
        except Exception:
            pass

    print("Completed Successfully")
    print(release["html_url"])


if __name__ == "__main__":
    main()
