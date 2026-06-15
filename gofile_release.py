import os
import re
import requests
from datetime import datetime

GOFILE_URL = os.environ["GOFILE_URL"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
GITHUB_REPOSITORY = os.environ["GITHUB_REPOSITORY"]


def get_content_id(url):
    m = re.search(r"/d/([A-Za-z0-9]+)", url)
    if not m:
        raise Exception(f"Invalid GoFile URL: {url}")
    return m.group(1)


def github_headers():
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }


def create_release():
    tag = datetime.utcnow().strftime("gofile-%Y%m%d-%H%M%S")
    r = requests.post(
        f"https://api.github.com/repos/{GITHUB_REPOSITORY}/releases",
        headers=github_headers(),
        json={"tag_name": tag, "name": tag, "draft": False, "prerelease": False},
        timeout=60,
    )
    r.raise_for_status()
    return r.json()


def upload_asset(upload_url, file_path):
    upload_url = upload_url.split("{")[0]
    with open(file_path, "rb") as f:
        r = requests.post(
            f"{upload_url}?name={os.path.basename(file_path)}",
            headers={
                "Authorization": f"Bearer {GITHUB_TOKEN}",
                "Content-Type": "application/octet-stream",
            },
            data=f,
            timeout=7200,
        )
    r.raise_for_status()


def download_file(url, output, token):
    with requests.get(
        url,
        stream=True,
        timeout=7200,
        headers={"Cookie": f"accountToken={token}"},
    ) as r:
        r.raise_for_status()
        with open(output, "wb") as f:
            for chunk in r.iter_content(1024 * 1024):
                if chunk:
                    f.write(chunk)


def get_guest_token():
    r = requests.post(
        "https://api.gofile.io/accounts",
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    if data.get("status") != "ok":
        raise Exception(f"Failed to get guest token: {data}")
    return data["data"]["token"]


def get_files(content_id, token):
    r = requests.get(
        f"https://api.gofile.io/contents/{content_id}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=60,
    )
    r.raise_for_status()
    data = r.json()
    if data.get("status") != "ok":
        raise Exception(f"GoFile API error: {data}")

    content = data["data"]
    files = []

    def collect(node):
        if node.get("type") == "file":
            files.append({
                "name": node["name"],
                "link": node["link"],
            })
        elif node.get("type") == "folder":
            for child in node.get("children", {}).values():
                collect(child)

    collect(content)
    return files


def main():
    content_id = get_content_id(GOFILE_URL)
    print(f"Content ID: {content_id}")

    print("Getting guest token...")
    token = get_guest_token()

    print("Fetching file list from GoFile API...")
    files = get_files(content_id, token)

    if not files:
        raise Exception("No files found in GoFile folder")

    print(f"Found {len(files)} file(s): {[f['name'] for f in files]}")

    release = create_release()
    upload_url = release["upload_url"]
    print(f"Created release: {release['html_url']}")

    for item in files:
        name = item["name"]
        link = item["link"]
        try:
            print(f"Downloading: {name}")
            download_file(link, name, token)

            print(f"Uploading: {name}")
            upload_asset(upload_url, name)

            os.remove(name)
            print(f"Done: {name}")
        except Exception as e:
            print(f"Failed {name}: {e}")

    print("Release URL:")
    print(release["html_url"])


if __name__ == "__main__":
    main()
