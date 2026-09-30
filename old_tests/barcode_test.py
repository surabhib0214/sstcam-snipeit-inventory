from inventory_api import get

print("=" * 50)
print("SSTCAM BARCODE TEST")
print("=" * 50)
print()
print("Scan an asset barcode.")
print("You can also type an asset tag or serial number.")
print()

search = input("Scan barcode: ").strip()

if not search:
    print("Nothing entered.")
    exit()

data = get("/hardware")

asset = None

for item in data["rows"]:
    asset_tag = str(item.get("asset_tag", "")).strip()
    serial = str(item.get("serial", "")).strip()

    if search == asset_tag or search == serial:
        asset = item
        break

if not asset:
    print()
    print("❌ Asset not found.")
    exit()

print()
print("=" * 50)
print("ASSET FOUND")
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
    print("Assignment type:", assigned_to.get("type"))
else:
    print("Assigned to: Nobody")

print()
print("✔ Barcode lookup successful.")

