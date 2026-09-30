from inventory_api import get, post, put

BASE_URL = "https://sstcam-inventory.ecap.work"


# ============================================================
# ASSET FUNCTIONS
# ============================================================

def find_asset_by_tag_or_serial(search):
    data = get("/hardware")

    for item in data["rows"]:
        asset_tag = str(item.get("asset_tag", "")).strip()
        serial = str(item.get("serial", "")).strip()

        if search == asset_tag or search == serial:
            return item

    return None


def show_asset(asset):
    print()
    print("=" * 60)
    print("ASSET")
    print("=" * 60)

    print("ID:", asset.get("id"))
    print("Asset tag:", asset.get("asset_tag"))
    print("Name:", asset.get("name"))
    print("Serial:", asset.get("serial"))

    model = asset.get("model") or {}
    print("Model:", model.get("name"))

    category = asset.get("category") or {}
    print("Category:", category.get("name"))

    status = asset.get("status_label") or {}
    print("Status:", status.get("name"))

    location = asset.get("location")

    if location:
        print("Location:", location.get("name"))
    else:
        print("Location: Not assigned")

    assigned_to = asset.get("assigned_to")

    if assigned_to:
        print("Assigned to:", assigned_to.get("name"))
        print("Assignment type:", assigned_to.get("type"))
    else:
        print("Assigned to: Nobody")


def checkin_asset(asset):
    asset_id = asset.get("id")

    print()

    confirmation = input(
        "Type CHECK IN to check this asset in: "
    ).strip()

    if confirmation != "CHECK IN":
        print("Nothing changed.")
        return

    result = post(
        f"/hardware/{asset_id}/checkin"
    )

    print()
    print("API response:")
    print(result)

    if result.get("status") == "success":
        print()
        print("✔ Asset checked in.")
    else:
        print()
        print("❌ Check-in may have failed.")


def checkout_asset(asset):
    asset_id = asset.get("id")

    print()

    destination = input(
        "Enter destination asset ID: "
    ).strip()

    if not destination:
        print("No destination entered. Nothing changed.")
        return

    if not destination.isdigit():
        print("Destination asset ID must be a number.")
        return

    print()
    print("Destination asset ID:", destination)

    confirmation = input(
        "Type CHECK OUT to continue: "
    ).strip()

    if confirmation != "CHECK OUT":
        print("Nothing changed.")
        return

    payload = {
        "checkout_to_type": "asset",
        "assigned_asset": int(destination)
    }

    result = post(
        f"/hardware/{asset_id}/checkout",
        payload
    )

    print()
    print("API response:")
    print(result)

    if result.get("status") == "success":
        print()
        print("✔ Asset checked out.")
    else:
        print()
        print("❌ Checkout may have failed.")


def report_asset_issue(asset):
    asset_id = asset.get("id")

    print()

    problem = input(
        "Enter the problem: "
    ).strip()

    if not problem:
        print("No problem entered. Nothing changed.")
        return

    current_notes = asset.get("notes") or ""

    issue_note = f"Issue: {problem}"

    if current_notes:
        updated_notes = current_notes + "\n" + issue_note
    else:
        updated_notes = issue_note

    payload = {
        "notes": updated_notes
    }

    result = put(
        f"/hardware/{asset_id}",
        payload
    )

    print()
    print("API response:")
    print(result)

    if result.get("status") == "success":
        print()
        print("✔ Issue recorded.")
    else:
        print()
        print("❌ Issue may not have been recorded.")


# ============================================================
# ASSET MENU
# ============================================================

def asset_menu(asset):
    while True:
        print()
        print("=" * 60)
        print("ASSET ACTIONS")
        print("=" * 60)

        print("1. View details")
        print("2. Check in")
        print("3. Check out")
        print("4. Report issue")
        print("5. Scan another")
        print("0. Exit")

        print()

        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_asset(asset)

        elif choice == "2":
            checkin_asset(asset)

            asset = get(
                f"/hardware/{asset.get('id')}"
            )

            show_asset(asset)

        elif choice == "3":
            checkout_asset(asset)

            asset = get(
                f"/hardware/{asset.get('id')}"
            )

            show_asset(asset)

        elif choice == "4":
            report_asset_issue(asset)

            asset = get(
                f"/hardware/{asset.get('id')}"
            )

            show_asset(asset)

        elif choice == "5":
            return

        elif choice == "0":
            print()
            print("Goodbye.")
            exit()

        else:
            print()
            print("Invalid option.")


# ============================================================
# COMPONENT FUNCTIONS
# ============================================================

def show_component(component):
    print()
    print("=" * 60)
    print("COMPONENT")
    print("=" * 60)

    print("ID:", component.get("id"))
    print("Name:", component.get("name"))
    print("Serial:", component.get("serial"))
    print("Asset tag:", component.get("asset_tag"))

    category = component.get("category") or {}
    print("Category:", category.get("name"))

    location = component.get("location")

    if location:
        print("Location:", location.get("name"))
    else:
        print("Location: Not assigned")

    print("Available quantity:", component.get("remaining"))
    print("Total quantity:", component.get("qty"))

    notes = component.get("notes")

    if notes:
        print()
        print("Notes:")
        print("-" * 60)
        print(notes)


def get_component_assignments(component_id):
    return get(
        f"/components/{component_id}/assets"
    )


def component_checkout(component):
    component_id = component.get("id")

    available = component.get("remaining") or 0

    print()

    if available <= 0:
        print("No components are currently available.")
        return

    destination = input(
        "Enter destination asset ID: "
    ).strip()

    if not destination:
        print("No destination entered. Nothing changed.")
        return

    if not destination.isdigit():
        print("Destination asset ID must be a number.")
        return

    destination_asset = get(
        f"/hardware/{destination}"
    )

    print()

    print("=" * 60)
    print("COMPONENT CHECKOUT")
    print("=" * 60)

    print("Component:", component.get("name"))
    print("Available quantity:", available)

    print(
        "Destination:",
        destination_asset.get("name")
    )

    print(
        "Asset tag:",
        destination_asset.get("asset_tag")
    )

    print()

    quantity = input(
        "Enter quantity to check out: "
    ).strip()

    if not quantity.isdigit():
        print("Quantity must be a number.")
        return

    quantity = int(quantity)

    if quantity <= 0:
        print("Quantity must be greater than 0.")
        return

    if quantity > available:
        print("Not enough components available.")
        print("Available:", available)
        return

    print()

    confirmation = input(
        "Type CHECK OUT to continue: "
    ).strip()

    if confirmation != "CHECK OUT":
        print("Nothing changed.")
        return

    payload = {
        "assigned_to": int(destination),
        "assigned_qty": quantity
    }

    result = post(
        f"/components/{component_id}/checkout",
        payload
    )

    print()
    print("API response:")
    print(result)

    if result.get("status") == "success":
        print()
        print("✔ Component checked out successfully.")
    else:
        print()
        print("❌ Component checkout may have failed.")


def component_checkin(component):
    component_id = component.get("id")

    print()
    print("Finding component assignments...")

    assignments = get_component_assignments(
        component_id
    )

    rows = assignments.get("rows", [])

    if not rows:
        print()
        print("No component assignments found.")
        return

    print()
    print("=" * 60)
    print("COMPONENT ASSIGNMENTS")
    print("=" * 60)

    for assignment in rows:
        print()
        print(
            "Assignment ID:",
            assignment.get("assigned_pivot_id")
        )

        print(
            "Asset ID:",
            assignment.get("id")
        )

        print(
            "Asset:",
            assignment.get("name")
        )

        print(
            "Quantity:",
            assignment.get("qty")
        )

    print()

    assignment_id = input(
        "Enter assignment ID to check in: "
    ).strip()

    if not assignment_id.isdigit():
        print("Assignment ID must be a number.")
        return

    assignment = None

    for item in rows:
        if str(
            item.get("assigned_pivot_id")
        ) == assignment_id:
            assignment = item
            break

    if not assignment:
        print()
        print("Assignment not found.")
        return

    assigned_quantity = assignment.get("qty", 0)

    print()
    print("=" * 60)
    print("COMPONENT CHECK IN")
    print("=" * 60)

    print("Component:", component.get("name"))
    print("Assignment ID:", assignment_id)
    print("Asset:", assignment.get("name"))
    print("Quantity assigned:", assigned_quantity)

    print()

    quantity = input(
        "Enter quantity to check in: "
    ).strip()

    if not quantity.isdigit():
        print("Quantity must be a number.")
        return

    quantity = int(quantity)

    if quantity <= 0:
        print("Quantity must be greater than 0.")
        return

    if quantity > assigned_quantity:
        print(
            "Cannot check in more than the assigned quantity."
        )

        print(
            "Assigned quantity:",
            assigned_quantity
        )

        return

    print()

    confirmation = input(
        "Type CHECK IN to continue: "
    ).strip()

    if confirmation != "CHECK IN":
        print("Nothing changed.")
        return

    payload = {
        "checkin_qty": quantity
    }

    result = post(
        f"/components/{assignment_id}/checkin",
        payload
    )

    print()
    print("API response:")
    print(result)

    if result.get("status") == "success":
        print()
        print("✔ Component checked in successfully.")
    else:
        print()
        print("❌ Component check-in may have failed.")


def report_component_issue(component):
    component_id = component.get("id")

    print()

    problem = input(
        "Enter the problem: "
    ).strip()

    if not problem:
        print("No problem entered. Nothing changed.")
        return

    current_notes = component.get("notes") or ""

    issue_note = f"Issue: {problem}"

    if current_notes:
        updated_notes = (
            current_notes
            + "\n"
            + issue_note
        )
    else:
        updated_notes = issue_note

    payload = {
        "notes": updated_notes
    }

    result = put(
        f"/components/{component_id}",
        payload
    )

    print()
    print("API response:")
    print(result)

    if result.get("status") == "success":
        print()
        print("✔ Component issue recorded.")
    else:
        print()
        print("❌ Component issue may not have been recorded.")


# ============================================================
# COMPONENT MENU
# ============================================================

def component_menu(component):
    while True:
        print()
        print("=" * 60)
        print("COMPONENT ACTIONS")
        print("=" * 60)

        print("1. View details")
        print("2. Check in")
        print("3. Check out")
        print("4. Report issue")
        print("5. Scan another")
        print("0. Exit")

        print()

        choice = input(
            "Choose an option: "
        ).strip()

        if choice == "1":
            show_component(component)

        elif choice == "2":
            component_checkin(component)

            component = get(
                f"/components/{component.get('id')}"
            )

            show_component(component)

        elif choice == "3":
            component_checkout(component)

            component = get(
                f"/components/{component.get('id')}"
            )

            show_component(component)

        elif choice == "4":
            report_component_issue(component)

            component = get(
                f"/components/{component.get('id')}"
            )

            show_component(component)

        elif choice == "5":
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

def scan_object():
    print()
    print("=" * 60)
    print("SCAN BARCODE / QR CODE")
    print("=" * 60)

    print()
    print("Scan an asset or component.")
    print()

    scan = input("Scan: ").strip()

    if not scan:
        print("No scan entered.")
        return

    # --------------------------------------------------------
    # Snipe-IT URL
    # --------------------------------------------------------

    if scan.startswith(BASE_URL):

        # Asset / hardware QR code
        if "/hardware/" in scan:

            asset_id = (
                scan
                .split("/hardware/")[-1]
                .split("/")[0]
            )

            if not asset_id.isdigit():
                print("Invalid asset URL.")
                return

            asset = get(
                f"/hardware/{asset_id}"
            )

            show_asset(asset)
            asset_menu(asset)

            return

        # Component QR code
        if "/components/" in scan:

            component_id = (
                scan
                .split("/components/")[-1]
                .split("/")[0]
            )

            if not component_id.isdigit():
                print("Invalid component URL.")
                return

            component = get(
                f"/components/{component_id}"
            )

            show_component(component)
            component_menu(component)

            return

        print("Snipe-IT URL not recognised.")
        return

    # --------------------------------------------------------
    # Asset tag / serial number
    # --------------------------------------------------------

    asset = find_asset_by_tag_or_serial(scan)

    if not asset:
        print()
        print("❌ Asset not found.")
        return

    show_asset(asset)
    asset_menu(asset)


# ============================================================
# MAIN PROGRAM
# ============================================================

print("=" * 60)
print("SSTCAM INVENTORY SCANNER")
print("=" * 60)

while True:
    scan_object()