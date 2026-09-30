from inventory_api import get

asset_id = input("Enter asset ID: ")

asset = get(f"/hardware/{asset_id}")

print()
print("Asset information")
print("=" * 40)

print("ID:", asset.get("id"))
print("Asset tag:", asset.get("asset_tag"))
print("Name:", asset.get("name"))

model = asset.get("model") or {}
print("Model:", model.get("name"))

category = asset.get("category") or {}
print("Category:", category.get("name"))

status = asset.get("status_label") or {}
print("Status:", status.get("name"))

print("Serial:", asset.get("serial"))