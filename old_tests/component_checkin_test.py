from inventory_api import get, post


component_id = input("Enter component ID: ").strip()

if not component_id.isdigit():
    print("Component ID must be a number.")
    exit()


component = get(
    f"/components/{component_id}"
)


print()
print("=" * 60)
print("COMPONENT")
print("=" * 60)

print("ID:", component.get("id"))
print("Name:", component.get("name"))
print("Available quantity:", component.get("remaining"))
print("Total quantity:", component.get("qty"))

print()


print("Finding component assignments...")

assignments = get(
    f"/components/{component_id}/assets"
)


if assignments.get("total", 0) == 0:
    print()
    print("No assignments found.")
    exit()


print()
print("=" * 60)
print("ASSIGNMENTS")
print("=" * 60)


rows = assignments.get("rows", [])

for assignment in rows:
    print()
    print("Assignment ID:", assignment.get("assigned_pivot_id"))
    print("Asset ID:", assignment.get("id"))
    print("Asset:", assignment.get("name"))
    print("Quantity:", assignment.get("qty"))
    print("Type:", assignment.get("type"))


print()


assignment_id = input(
    "Enter assignment ID to check in: "
).strip()


if not assignment_id.isdigit():
    print("Assignment ID must be a number.")
    exit()


assignment = None

for item in rows:
    if str(item.get("assigned_pivot_id")) == assignment_id:
        assignment = item
        break


if not assignment:
    print()
    print("Assignment not found.")
    exit()


assigned_quantity = assignment.get("qty", 0)


print()
print("=" * 60)
print("CHECK IN")
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
    exit()


quantity = int(quantity)


if quantity <= 0:
    print("Quantity must be greater than 0.")
    exit()


if quantity > assigned_quantity:
    print("Cannot check in more than the assigned quantity.")
    print("Assigned quantity:", assigned_quantity)
    exit()


print()

confirmation = input(
    "Type CHECK IN to continue: "
).strip()


if confirmation != "CHECK IN":
    print("Nothing changed.")
    exit()


payload = {
    "checkin_qty": quantity
}


print()
print("Sending check-in request...")


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