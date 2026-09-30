from inventory_api import get, post

CAMERA_ID = 126


def get_camera():
    return get(f"/hardware/{CAMERA_ID}")


def show_camera():
    camera = get_camera()

    print()
    print("=" * 70)
    print("CAMERA")
    print("=" * 70)

    print("ID:", camera.get("id"))
    print("Asset tag:", camera.get("asset_tag"))
    print("Name:", camera.get("name"))
    print("Serial:", camera.get("serial"))

    model = camera.get("model") or {}
    print("Model:", model.get("name"))

    status = camera.get("status_label") or {}
    print("Status:", status.get("name"))

    location = camera.get("location")
    if location:
        print("Location:", location.get("name"))
    else:
        print("Location: Not assigned")


def get_all_components():
    data = get("/components")
    return data.get("rows", [])


def get_component_assignments(component_id):
    data = get(f"/components/{component_id}/assets")
    return data.get("rows", [])


def get_camera_components():
    """
    Find all components currently assigned to the Camera Unit.

    The hardware/{id}/components endpoint is not available on this
    Snipe-IT installation, so we look at each component's assignments.
    """

    components = get_all_components()
    assigned_components = []

    for component in components:
        component_id = component.get("id")

        if not component_id:
            continue

        assignments = get_component_assignments(component_id)

        for assignment in assignments:
            assigned_asset_id = assignment.get("id")

            if assigned_asset_id == CAMERA_ID:
                assigned_components.append({
                    "component": component,
                    "assignment": assignment
                })

    return assigned_components


def show_components():
    print()
    print("=" * 70)
    print("COMPONENTS ASSIGNED TO CAMERA")
    print("=" * 70)

    assigned_components = get_camera_components()

    if not assigned_components:
        print()
        print("No components are currently assigned to the camera.")
        return

    print()

    for number, item in enumerate(assigned_components, start=1):
        component = item["component"]
        assignment = item["assignment"]

        print(
            number,
            "| ID:", component.get("id"),
            "| Name:", component.get("name"),
            "| Quantity:", assignment.get("qty")
        )

    print()
    print("Total component types:", len(assigned_components))


def add_component():
    print()
    print("=" * 70)
    print("ADD COMPONENT TO CAMERA")
    print("=" * 70)

    component_id = input("Enter component ID: ").strip()

    if not component_id.isdigit():
        print("Component ID must be a number.")
        return

    component_id = int(component_id)

    component = get(f"/components/{component_id}")

    print()
    print("Component:", component.get("name"))
    print("Component ID:", component.get("id"))
    print("Available quantity:", component.get("remaining"))

    available = component.get("remaining") or 0

    if available <= 0:
        print()
        print("No quantity is currently available.")
        return

    print()

    quantity = input("Enter quantity to add: ").strip()

    if not quantity.isdigit():
        print("Quantity must be a number.")
        return

    quantity = int(quantity)

    if quantity <= 0:
        print("Quantity must be greater than 0.")
        return

    if quantity > available:
        print()
        print("Not enough components available.")
        print("Available:", available)
        return

    print()
    print("Destination: Camera Unit")
    print("Camera ID:", CAMERA_ID)
    print("Quantity:", quantity)
    print()

    confirmation = input(
        "Type ADD COMPONENT to continue: "
    ).strip()

    if confirmation != "ADD COMPONENT":
        print("Nothing changed.")
        return

    payload = {
        "assigned_to": CAMERA_ID,
        "assigned_qty": quantity
    }

    print()
    print("Checking component out to camera...")

    result = post(
        f"/components/{component_id}/checkout",
        payload
    )

    print()
    print("API response:")
    print(result)

    if result.get("status") == "success":
        print()
        print("✔ Component added to camera.")
    else:
        print()
        print("❌ Component checkout may have failed.")


def remove_component():
    print()
    print("=" * 70)
    print("REMOVE COMPONENT FROM CAMERA")
    print("=" * 70)

    assigned_components = get_camera_components()

    if not assigned_components:
        print()
        print("No components are currently assigned to the camera.")
        return

    print()

    for number, item in enumerate(assigned_components, start=1):
        component = item["component"]
        assignment = item["assignment"]

        print(
            number,
            "| ID:", component.get("id"),
            "| Name:", component.get("name"),
            "| Quantity:", assignment.get("qty")
        )

    print()

    choice = input(
        "Enter the number of the component to remove: "
    ).strip()

    if not choice.isdigit():
        print("Please enter a number.")
        return

    choice = int(choice)

    if choice < 1 or choice > len(assigned_components):
        print("Invalid selection.")
        return

    selected = assigned_components[choice - 1]

    component = selected["component"]
    assignment = selected["assignment"]

    component_id = component.get("id")
    assignment_id = assignment.get("assigned_pivot_id")
    assigned_quantity = assignment.get("qty") or 0

    print()
    print("=" * 70)
    print("SELECTED COMPONENT")
    print("=" * 70)

    print("Component ID:", component_id)
    print("Component:", component.get("name"))
    print("Assignment ID:", assignment_id)
    print("Quantity assigned:", assigned_quantity)

    print()

    quantity = input(
        "Enter quantity to remove: "
    ).strip()

    if not quantity.isdigit():
        print("Quantity must be a number.")
        return

    quantity = int(quantity)

    if quantity <= 0:
        print("Quantity must be greater than 0.")
        return

    if quantity > assigned_quantity:
        print()
        print("Cannot remove more than the assigned quantity.")
        print("Assigned quantity:", assigned_quantity)
        return

    print()

    confirmation = input(
        "Type REMOVE COMPONENT to continue: "
    ).strip()

    if confirmation != "REMOVE COMPONENT":
        print("Nothing changed.")
        return

    payload = {
        "checkin_qty": quantity
    }

    print()
    print("Checking component in...")

    result = post(
        f"/components/{assignment_id}/checkin",
        payload
    )

    print()
    print("API response:")
    print(result)

    if result.get("status") == "success":
        print()
        print("✔ Component removed from camera.")
    else:
        print()
        print("❌ Component check-in may have failed.")


while True:

    print()
    print("=" * 70)
    print("CAMERA COMPONENT MANAGER")
    print("=" * 70)

    print("Camera ID:", CAMERA_ID)
    print()

    print("1. View camera")
    print("2. List assigned components")
    print("3. Add component to camera")
    print("4. Remove component from camera")
    print("0. Exit")

    print()

    choice = input("Choose an option: ").strip()

    if choice == "1":
        show_camera()

    elif choice == "2":
        show_components()

    elif choice == "3":
        add_component()

    elif choice == "4":
        remove_component()

    elif choice == "0":
        print()
        print("Goodbye.")
        break

    else:
        print()
        print("Invalid option.")