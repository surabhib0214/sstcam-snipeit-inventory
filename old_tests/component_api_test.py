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
print("Serial:", component.get("serial"))
print("Asset tag:", component.get("asset_tag"))

category = component.get("category") or {}
print("Category:", category.get("name"))

print()
print("Full component data:")
print(component)