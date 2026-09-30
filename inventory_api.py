import os
import requests

BASE_URL = "https://sstcam-inventory.ecap.work/api/v1"

API_KEY = os.getenv("SNIPEIT_API_KEY")

if not API_KEY:
    raise RuntimeError("SNIPEIT_API_KEY environment variable is not set")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
}


def get(endpoint):
    """Send a GET request to the Snipe-IT API."""

    url = f"{BASE_URL}{endpoint}"

    response = requests.get(
        url,
        headers=HEADERS
    )

    if response.status_code != 200:
        print("API request failed")
        print("Status:", response.status_code)
        print("Response:", response.text)

    response.raise_for_status()

    return response.json()


def post(endpoint, payload=None):
    """Send a POST request to the Snipe-IT API."""

    url = f"{BASE_URL}{endpoint}"

    response = requests.post(
        url,
        headers=HEADERS,
        json=payload or {}
    )

    if response.status_code not in [200, 201]:
        print("API request failed")
        print("Status:", response.status_code)
        print("Response:", response.text)

    response.raise_for_status()

    return response.json()
def put(endpoint, payload=None):
    """Send a PUT request to the Snipe-IT API."""

    url = f"{BASE_URL}{endpoint}"

    response = requests.put(
        url,
        headers=HEADERS,
        json=payload or {}
    )

    if response.status_code not in [200, 201]:
        print("API request failed")
        print("Status:", response.status_code)
        print("Response:", response.text)

    response.raise_for_status()

    return response.json()