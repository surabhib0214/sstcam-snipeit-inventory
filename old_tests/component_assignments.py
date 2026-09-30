from inventory_api import get


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
print("Checking which assets have this component...")
print()

result = get(f"/components/{component_id}/assets")

print("=" * 60)
print("COMPONENT ASSIGNMENTS")
print("=" * 60)

print(result)