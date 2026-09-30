import sys

from inventory_api import get, post

ECAMI_ASSET_ID = 126
TM_MODEL_NAME = "SSTCAM Target Module"


def get_tm(tm_id):
    asset = get(f"/hardware/{tm_id}")

    model = asset.get("model") or {}

    if model.get("name") != TM_MODEL_NAME:
        print()
        print("❌ This asset is not a Target Module.")
        print("Model:", model.get("name"))
        return None

    return asset


def main():
    if len(sys.argv) != 2:
        print()
        print("Usage:")
        print("py snipe_it_add_tm_to_ecami.py <TM_ID>")
        print()
        return

    tm_id = sys.argv[1]

    if not tm_id.isdigit():
        print("TM ID must be a number.")
        return

    tm_id = int(tm_id)

    tm = get_tm(tm_id)

    if tm is None:
        return

    assigned = tm.get("assigned_to")

    print()
    print("=" * 70)
    print("ADD TARGET MODULE TO ECAMi")
    print("=" * 70)

    print("ID:", tm.get("id"))
    print("Asset tag:", tm.get("asset_tag"))
    print("Serial:", tm.get("serial"))
    print("Model:", TM_MODEL_NAME)
    print()

    if assigned:
        print("Current assignment:", assigned.get("name"))

        if (
            assigned.get("type") == "asset"
            and assigned.get("id") == ECAMI_ASSET_ID
        ):
            print()
            print("This Target Module is already in ECAMi.")
            return

        print()
        print("❌ This Target Module is currently assigned somewhere else.")
        print("Remove it from its current assignment first.")
        return

    print("Current destination: Not assigned")
    print()
    confirmation = input("Type ADD TM to continue: ").strip()

    if confirmation != "ADD TM":
        print()
        print("Nothing changed.")
        return

    payload = {
        "checkout_to_type": "asset",
        "assigned_asset": ECAMI_ASSET_ID
    }

    print()
    print("Checking TM out to ECAMi...")

    result = post(
        f"/hardware/{tm_id}/checkout",
        payload
    )

    print()

    if result.get("status") == "success":
        print("✔ Target Module added to ECAMi.")
    else:
        print("❌ Check-out may have failed.")
        print()
        print("API response:")
        print(result)


main()