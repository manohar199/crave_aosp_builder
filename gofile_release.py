import os
import re
import json
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
        "Accept": "application/vnd.github+json"
    }


def create_release():
    tag = datetime.utcnow().strftime("gofile-%Y%m%d-%H%M%S")

    payload = {
        "tag_name": tag,
        "name": tag,
        "draft": False,
        "prerelease": False
    }

    r = requests.post(
        f"https://api.github.com/repos/{GITHUB_REPOSITORY}/releases",
        headers=github_headers(),
        json=payload,
        timeout=60
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
                "Content-Type": "application/octet-stream"
            },
            data=f,
            timeout=7200
        )

    r.raise_for_status()


def download_file(url, output):
    with requests.get(url, stream=True, timeout=7200) as r:
        r.raise_for_status()

        with open(output, "wb") as f:
            for chunk in r.iter_content(1024 * 1024):
                if chunk:
                    f.write(chunk)


def get_gofile_page(content_id):
    r = requests.get(
        f"https://gofile.io/d/{content_id}",
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=60
    )

    r.raise_for_status()
    return r.text


def extract_download_links(html):
    patterns = [
        r'https://store[^"\']+',
        r'https://[^"\']+gofile[^"\']+download[^"\']+',
        r'"link":"(https:[^"]+)"'
    ]

    links = []

    for pattern in patterns:
        matches = re.findall(pattern, html)

        for m in matches:
            m = m.replace("\\/", "/")

            if m not in links:
                links.append(m)

    return links


def main():
    content_id = get_content_id(GOFILE_URL)

    print("Content ID:", content_id)

    html = get_gofile_page(content_id)

    links = extract_download_links(html)

    if not links:
        print(html[:5000])
        raise Exception(
            "No downloadable files found in page source"
        )

    release = create_release()

    upload_url = release["upload_url"]

    for index, link in enumerate(links, start=1):
        filename = f"file_{index}"

        try:
            print(f"Downloading {filename}")

            download_file(link, filename)

            print(f"Uploading {filename}")

            upload_asset(upload_url, filename)

            os.remove(filename)

        except Exception as e:
            print(f"Failed: {e}")

    print("Release URL:")
    print(release["html_url"])


if __name__ == "__main__":
    main()
