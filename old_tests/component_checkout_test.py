from inventory_api import get, post


component_id = input("Enter component ID: ").strip()

if not component_id.isdigit():
    print("Component ID must be a number.")
    exit()


component = get(f"/components/{component_id}")


print()
print("=" * 60)
print("COMPONENT")
print("=" * 60)

print("ID:", component.get("id"))
print("Name:", component.get("name"))
print("Available quantity:", component.get("remaining"))
print("Total quantity:", component.get("qty"))

print()


asset_id = input(
    "Enter destination asset ID: "
).strip()

if not asset_id.isdigit():
    print("Asset ID must be a number.")
    exit()


quantity = input(
    "Enter quantity to check out: "
).strip()

if not quantity.isdigit():
    print("Quantity must be a number.")
    exit()


quantity = int(quantity)


if quantity <= 0:
    print("Quantity must be greater than 0.")
    exit()


available = component.get("remaining") or 0

if quantity > available:
    print("Not enough components available.")
    print("Available:", available)
    exit()


destination = get(
    f"/hardware/{asset_id}"
)


print()
print("=" * 60)
print("CHECKOUT")
print("=" * 60)

print("Component:", component.get("name"))
print("Quantity:", quantity)

print(
    "Destination:",
    destination.get("name")
)

print(
    "Asset tag:",
    destination.get("asset_tag")
)

print()


confirmation = input(
    "Type CHECK OUT to continue: "
).strip()


if confirmation != "CHECK OUT":
    print("Nothing changed.")
    exit()


payload = {
    "assigned_to": int(asset_id),
    "assigned_qty": quantity
}


print()
print("Sending checkout request...")


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