from inventory_api import get, post


BASE_URL = "https://sstcam-inventory.ecap.work"

ECAMI_ASSET_ID = 126
TM_MODEL_NAME = "SSTCAM Target Module"


# ============================================================
# FIND TARGET MODULE
# ============================================================

def find_tm_by_tag_or_serial(search):

    data = get("/hardware")

    for asset in data["rows"]:

        model = asset.get("model") or {}

        if model.get("name") != TM_MODEL_NAME:
            continue

        asset_tag = str(
            asset.get("asset_tag") or ""
        ).strip()

        serial = str(
            asset.get("serial") or ""
        ).strip()

        if search == asset_tag or search == serial:
            return asset

    return None


# ============================================================
# GET TM FROM URL
# ============================================================

def get_tm_from_url(scan):

    if "/hardware/" not in scan:
        return None

    asset_id = (
        scan
        .split("/hardware/")[-1]
        .split("/")[0]
    )

    if not asset_id.isdigit():
        return None

    asset = get(
        f"/hardware/{asset_id}"
    )

    model = asset.get("model") or {}

    if model.get("name") != TM_MODEL_NAME:
        return None

    return asset


# ============================================================
# SHOW TM
# ============================================================

def show_tm(tm):

    print()
    print("=" * 70)
    print("TARGET MODULE")
    print("=" * 70)

    print("ID:", tm.get("id"))
    print("Asset tag:", tm.get("asset_tag"))
    print("Serial:", tm.get("serial"))

    model = tm.get("model") or {}
    print("Model:", model.get("name"))

    status = tm.get("status_label") or {}
    print("Status:", status.get("name"))

    location = tm.get("location")

    if location:
        print("Location:", location.get("name"))
    else:
        print("Location: Not assigned")

    assigned = tm.get("assigned_to")

    if assigned:
        print("Assigned to:", assigned.get("name"))
        print("Assignment type:", assigned.get("type"))
    else:
        print("Assigned to: Nobody")


# ============================================================
# CHECK IF TM IS IN ECAMi
# ============================================================

def is_in_ecami(tm):

    assigned = tm.get("assigned_to")

    if not assigned:
        return False

    return (
        assigned.get("type") == "asset"
        and assigned.get("id") == ECAMI_ASSET_ID
    )


# ============================================================
# ADD TM TO ECAMi
# ============================================================

def add_tm_to_ecami(tm):

    tm_id = tm.get("id")

    print()
    print("Destination: ECAMi")
    print("ECAMi asset ID:", ECAMI_ASSET_ID)

    print()

    confirmation = input(
        "Type ADD TM to continue: "
    ).strip()

    if confirmation != "ADD TM":

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
    print("API response:")
    print(result)

    if result.get("status") == "success":

        print()
        print("✔ Target Module added to ECAMi.")

    else:

        print()
        print("❌ Operation may have failed.")


# ============================================================
# REMOVE TM FROM ECAMi
# ============================================================

def remove_tm_from_ecami(tm):

    tm_id = tm.get("id")

    print()
    print("Current destination: ECAMi")

    print()

    confirmation = input(
        "Type REMOVE TM to continue: "
    ).strip()

    if confirmation != "REMOVE TM":

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
        print("❌ Operation may have failed.")


# ============================================================
# TM MENU
# ============================================================

def tm_menu(tm):

    while True:

        print()

        if is_in_ecami(tm):

            print("=" * 70)
            print("TM IS CURRENTLY IN ECAMi")
            print("=" * 70)

            print("1. View details")
            print("2. Remove from ECAMi")
            print("3. Scan another")
            print("0. Exit")

        else:

            print("=" * 70)
            print("TM IS NOT IN ECAMi")
            print("=" * 70)

            print("1. View details")
            print("2. Add to ECAMi")
            print("3. Scan another")
            print("0. Exit")

        print()

        choice = input(
            "Choose an option: "
        ).strip()

        if choice == "1":

            show_tm(tm)

        elif choice == "2":

            if is_in_ecami(tm):

                remove_tm_from_ecami(tm)

            else:

                add_tm_to_ecami(tm)

            # Refresh information from Snipe-IT

            tm = get(
                f"/hardware/{tm.get('id')}"
            )

            show_tm(tm)

        elif choice == "3":

            return

        elif choice == "0":

            print()
            print("Goodbye.")
            exit()

        else:

            print()
            print("Invalid option.")


# ============================================================
# SCANNER
# ============================================================

def scan_tm():

    print()
    print("=" * 70)
    print("SCAN TARGET MODULE")
    print("=" * 70)

    print()
    print("Scan a Target Module QR code/barcode.")
    print()

    scan = input("Scan: ").strip()

    if not scan:

        print("No scan entered.")
        return

    # --------------------------------------------------------
    # Snipe-IT hardware URL
    # --------------------------------------------------------

    if "/hardware/" in scan:

        tm = get_tm_from_url(scan)

        if not tm:

            print()
            print("❌ Target Module not found.")
            return

        show_tm(tm)
        tm_menu(tm)

        return

    # --------------------------------------------------------
    # Asset tag or serial number
    # --------------------------------------------------------

    tm = find_tm_by_tag_or_serial(scan)

    if not tm:

        print()
        print("❌ Target Module not found.")
        return

    show_tm(tm)
    tm_menu(tm)


# ============================================================
# MAIN
# ============================================================

print("=" * 70)
print("SSTCAM TARGET MODULE SCANNER")
print("=" * 70)

while True:

    scan_tm()