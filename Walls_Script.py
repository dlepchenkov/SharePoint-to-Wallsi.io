import os
import csv
import requests
import time
from msal import PublicClientApplication

# --- Azure AD OAuth2 (Delegated Flow) ---
TENANT_ID = "TENANT_ID"
CLIENT_ID = "CLIENT_ID"
AUTHORITY = f"AUTHORITY/{TENANT_ID}"
SCOPES = ["SCOPES"]

# --- Walls.io Settings ---
WALLSIO_TOKEN = "WALLSIO_TOKEN"
WALLSIO_USER = "..."
WALLSIO_AVATAR = "WALLSIO_AVATAR"
WALLSIO_API = "https://api.walls.io/v1"

# --- Local folders ---
TEMP_DIR = "downloaded"
os.makedirs(TEMP_DIR, exist_ok=True)

# --- CSV-File für Geschichte ---
CSV_FILE = "posted.csv"
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["filename"])

def is_posted(filename):
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # пропустить заголовок
        return filename in (row[0] for row in reader)

def mark_as_posted(filename):
    if not is_posted(filename):
        with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([filename])

# --- OAuth2 ---
app = PublicClientApplication(CLIENT_ID, authority=AUTHORITY)

def get_graph_token():
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
    else:
        flow = app.initiate_device_flow(scopes=SCOPES)
        print(flow["message"])
        result = app.acquire_token_by_device_flow(flow)
    if "access_token" not in result:
        raise RuntimeError("Authentication failed.")
    return result["access_token"]

# --- Graph API ---
def get_folder_id(folder_path, headers):
    url = f"https://graph.microsoft.com/v1.0/me/drive/root:/{folder_path}"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()["id"]

def list_files(folder_id, headers):
    url = f"https://graph.microsoft.com/v1.0/me/drive/items/{folder_id}/children"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json().get("value", [])

def download_file(file_id, save_to, headers):
    url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/content"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    with open(save_to, 'wb') as f:
        f.write(r.content)

# --- Main Logic ---
def process_folder():
    token = get_graph_token()
    headers = {"Authorization": f"Bearer {token}"}
    folder_id = get_folder_id("Walls.io", headers)
    files = list_files(folder_id, headers)
    file_dict = {f["name"]: f for f in files}

    for txt in [f for f in file_dict if f.endswith(".txt")]:
        if is_posted(txt):
            continue

        base = txt[:-4]
        image = base + "foto.png"
        if image not in file_dict:
            continue

        txt_path = os.path.join(TEMP_DIR, txt)
        img_path = os.path.join(TEMP_DIR, image)

        download_file(file_dict[txt]["id"], txt_path, headers)
        download_file(file_dict[image]["id"], img_path, headers)

        with open(txt_path, "r", encoding="utf-8") as f:
            post_text = f.read().strip()

        with open(img_path, "rb") as img_file:
            r = requests.post(
                f"{WALLSIO_API}/media_upload",
                files={"image": img_file},
                data={"access_token": WALLSIO_TOKEN}
            )
        if r.status_code != 200:
            print(f"❌ Failure of posting image: {r.text}")
            continue

        media_id = r.json().get("data", {}).get("id")
        if not media_id:
            print("❌ media_id is not there")
            continue

        post_data = {
            "access_token": WALLSIO_TOKEN,
            "text": post_text,
            "user_name": WALLSIO_USER,
            "user_image": WALLSIO_AVATAR,
            "status": 1,
            "image": media_id
        }
        r2 = requests.post(f"{WALLSIO_API}/posts", json=post_data)
        if r2.status_code == 200:
            print(f"✅ Posted: {txt}")
            mark_as_posted(txt)
        else:
            print(f"❌ Failure while posing: {r2.status_code}, {r2.text}")

        os.remove(txt_path)
        os.remove(img_path)

# --- Cycle---
def main_loop():
    print("▶ OneDrive checking...")
    while True:
        try:
            process_folder()
        except Exception as e:
            print(f"⚠ Failure: {e}")
        time.sleep(30)

if __name__ == "__main__":
    main_loop()
