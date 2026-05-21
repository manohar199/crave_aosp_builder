import requests
import html
import os

# --- Configuration ---
# CHANGE THESE TWO LINES TO MATCH YOUR REPOSITORY
GITHUB_OWNER = 'your_github_username'  
GITHUB_REPO = 'your_repository_name'   

# These will be securely injected by GitHub Actions later
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
# ---------------------

def get_latest_release_files():
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
    print(f"Fetching latest release for {GITHUB_OWNER}/{GITHUB_REPO}...")
    
    response = requests.get(url)
    response.raise_for_status()
    release_data = response.json()
    
    files_content = {}
    
    for asset in release_data.get('assets', []):
        download_url = asset['browser_download_url']
        file_name = asset['name']
        print(f"Downloading {file_name}...")
        
        file_response = requests.get(download_url)
        file_response.raise_for_status()
        
        try:
            files_content[file_name] = file_response.text
        except Exception as e:
            print(f"Skipping {file_name} - not text: {e}")
            
    return files_content

def send_to_telegram(file_name, content):
    max_length = 4000 
    if len(content) > max_length:
        content = content[:max_length] + "\n\n... [TRUNCATED]"
        
    safe_content = html.escape(content)
    message = f"File: {file_name}\n{safe_content}"
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"Failed to send {file_name}: {response.text}")
    else:
        print(f"Successfully sent {file_name}.")

def main():
    try:
        files = get_latest_release_files()
        if not files:
            print("No files found.")
            return
        for name, content in files.items():
            send_to_telegram(name, content)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()