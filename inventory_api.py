import os
import requests

# Snipe-IT API base URL
BASE_URL = "https://sstcam-inventory.ecap.work/api/v1"

# Local laptop:
#   Uses API_KEY from config.py
#
# Cloud/server:
#   Uses SNIPEIT_API_KEY environment variable
#
# Environment variable takes priority when available.

try:
    from config import API_KEY as LOCAL_API_KEY
except ImportError:
    LOCAL_API_KEY = None

API_KEY = os.getenv("SNIPEIT_API_KEY") or LOCAL_API_KEY

if not API_KEY:
    raise RuntimeError(
        "Snipe-IT API key is not configured. "
        "Create config.py for local use or set SNIPEIT_API_KEY for server deployment."
    )

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}


def get(endpoint):
    url = f"{BASE_URL}{endpoint}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()


def post(endpoint, data):
    url = f"{BASE_URL}{endpoint}"
    response = requests.post(url, headers=HEADERS, json=data)
    response.raise_for_status()
    return response.json()


def put(endpoint, data):
    url = f"{BASE_URL}{endpoint}"
    response = requests.put(url, headers=HEADERS, json=data)
    response.raise_for_status()
    return response.json()