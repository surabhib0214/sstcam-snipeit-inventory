from inventory_api import get

asset_id = input("Enter asset ID: ").strip()

asset = get(f"/hardware/{asset_id}")

print()
print("Asset Details")
print("=" * 50)

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
    print("Assigned type:", assigned_to.get("type"))
else:
    print("Assigned to: Nobody")