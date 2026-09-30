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
        exit()

    return asset


def main():

    if len(sys.argv) != 2:
        print()
        print("Usage:")
        print("py snipe_it_rm_tm_from_ecami.py <TM_ID>")
        print()
        return

    tm_id = sys.argv[1]

    if not tm_id.isdigit():
        print("TM ID must be a number.")
        return

    tm_id = int(tm_id)

    tm = get_tm(tm_id)

    assigned = tm.get("assigned_to")

    if not assigned:
        print()
        print("This Target Module is not currently assigned to anything.")
        return

    if (
        assigned.get("type") != "asset"
        or assigned.get("id") != ECAMI_ASSET_ID
    ):
        print()
        print("This Target Module is not currently in ECAMi.")
        print()
        print("Currently assigned to:", assigned.get("name"))
        return

    print()
    print("=" * 70)
    print("REMOVE TARGET MODULE FROM ECAMi")
    print("=" * 70)

    print("ID:", tm.get("id"))
    print("Asset tag:", tm.get("asset_tag"))
    print("Serial:", tm.get("serial"))
    print("Model:", TM_MODEL_NAME)
    print()
    print("Current destination: ECAMi")
    print()

    confirmation = input(
        "Type REMOVE TM to continue: "
    ).strip()

    if confirmation != "REMOVE TM":
        print()
        print("Nothing changed.")
        return

    print()
    print("Checking TM in...")

    result = post(
        f"/hardware/{tm_id}/checkin"
    )

    print()
    print("API response:")
    print(result)

    if result.get("status") == "success":
        print()
        print("✔ Target Module removed from ECAMi.")
    else:
        print()
        print("❌ Check-in may have failed.")


main()