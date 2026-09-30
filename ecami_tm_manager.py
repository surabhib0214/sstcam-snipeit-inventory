from inventory_api import get, post


ECAMI_ASSET_ID = 126
TM_MODEL_NAME = "SSTCAM Target Module"


# ============================================================
# GET TARGET MODULES
# ============================================================

def get_all_assets():
    data = get("/hardware")
    return data["rows"]


def get_ecami_tms(assets):
    tms = []

    for asset in assets:
        model = asset.get("model") or {}
        assigned = asset.get("assigned_to")

        if model.get("name") != TM_MODEL_NAME:
            continue

        if not assigned:
            continue

        if assigned.get("type") != "asset":
            continue

        if assigned.get("id") != ECAMI_ASSET_ID:
            continue

        tms.append(asset)

    return tms


def get_available_tms(assets):
    tms = []

    for asset in assets:
        model = asset.get("model") or {}
        assigned = asset.get("assigned_to")
        status = asset.get("status_label") or {}

        if model.get("name") != TM_MODEL_NAME:
            continue

        if status.get("name") != "Ready to Deploy":
            continue

        if assigned:
            if (
                assigned.get("type") == "asset"
                and assigned.get("id") == ECAMI_ASSET_ID
            ):
                continue

        tms.append(asset)

    return tms


# ============================================================
# DISPLAY
# ============================================================

def print_tm(tm, number=None):

    if number is not None:
        print(
            number,
            "|",
            "ID:", tm.get("id"),
            "| Tag:", tm.get("asset_tag"),
            "| Serial:", tm.get("serial")
        )

    else:
        print(
            "ID:", tm.get("id"),
            "| Tag:", tm.get("asset_tag"),
            "| Serial:", tm.get("serial")
        )


# ============================================================
# LIST TMs IN ECAMi
# ============================================================

def show_ecami_tms():

    assets = get_all_assets()
    tms = get_ecami_tms(assets)

    print()
    print("=" * 70)
    print("TARGET MODULES IN ECAMi")
    print("=" * 70)

    if not tms:
        print("No Target Modules are currently in ECAMi.")
        return

    for number, tm in enumerate(tms, start=1):
        print_tm(tm, number)

    print()
    print("Total:", len(tms))


# ============================================================
# LIST AVAILABLE TMs
# ============================================================

def show_available_tms():

    assets = get_all_assets()
    tms = get_available_tms(assets)

    print()
    print("=" * 70)
    print("TARGET MODULES READY TO DEPLOY")
    print("=" * 70)

    if not tms:
        print("No Target Modules are currently available.")
        return

    for number, tm in enumerate(tms, start=1):
        print_tm(tm, number)

    print()
    print("Total:", len(tms))


# ============================================================
# ADD TM TO ECAMi
# ============================================================

def add_tm_to_ecami():

    assets = get_all_assets()
    tms = get_available_tms(assets)

    print()
    print("=" * 70)
    print("ADD TARGET MODULE TO ECAMi")
    print("=" * 70)

    if not tms:
        print("No Target Modules are currently available.")
        return

    for number, tm in enumerate(tms, start=1):
        print_tm(tm, number)

    print()

    choice = input(
        "Enter the number of the TM to add: "
    ).strip()

    if not choice.isdigit():
        print("Please enter a number.")
        return

    choice = int(choice)

    if choice < 1 or choice > len(tms):
        print("Invalid selection.")
        return

    tm = tms[choice - 1]

    print()
    print("=" * 70)
    print("SELECTED TARGET MODULE")
    print("=" * 70)

    print("ID:", tm.get("id"))
    print("Asset tag:", tm.get("asset_tag"))
    print("Serial:", tm.get("serial"))

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

    tm_id = tm.get("id")

    payload = {
        "checkout_to_type": "asset",
        "assigned_asset": ECAMI_ASSET_ID
    }

    print()
    print("Sending checkout request...")

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
        print("❌ Checkout may have failed.")


# ============================================================
# REMOVE TM FROM ECAMi
# ============================================================

def remove_tm_from_ecami():

    assets = get_all_assets()
    tms = get_ecami_tms(assets)

    print()
    print("=" * 70)
    print("REMOVE TARGET MODULE FROM ECAMi")
    print("=" * 70)

    if not tms:
        print("No Target Modules are currently in ECAMi.")
        return

    for number, tm in enumerate(tms, start=1):
        print_tm(tm, number)

    print()

    choice = input(
        "Enter the number of the TM to remove: "
    ).strip()

    if not choice.isdigit():
        print("Please enter a number.")
        return

    choice = int(choice)

    if choice < 1 or choice > len(tms):
        print("Invalid selection.")
        return

    tm = tms[choice - 1]

    print()
    print("=" * 70)
    print("SELECTED TARGET MODULE")
    print("=" * 70)

    print("ID:", tm.get("id"))
    print("Asset tag:", tm.get("asset_tag"))
    print("Serial:", tm.get("serial"))

    print()
    print("Current destination: ECAMi")

    print()

    confirmation = input(
        "Type REMOVE TM to continue: "
    ).strip()

    if confirmation != "REMOVE TM":
        print("Nothing changed.")
        return

    tm_id = tm.get("id")

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


# ============================================================
# MAIN MENU
# ============================================================

while True:

    print()
    print("=" * 70)
    print("ECAMi TARGET MODULE MANAGER")
    print("=" * 70)

    print("1. List TMs in ECAMi")
    print("2. List TMs ready to deploy")
    print("3. Add TM to ECAMi")
    print("4. Remove TM from ECAMi")
    print("0. Exit")

    print()

    choice = input("Choose an option: ").strip()

    if choice == "1":

        show_ecami_tms()

    elif choice == "2":

        show_available_tms()

    elif choice == "3":

        add_tm_to_ecami()

    elif choice == "4":

        remove_tm_from_ecami()

    elif choice == "0":

        print()
        print("Goodbye.")
        break

    else:

        print()
        print("Invalid option.")