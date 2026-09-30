from inventory_api import get

search = input("Enter asset tag or serial number: ").strip()

data = get("/hardware")

found = []

for asset in data["rows"]:
    asset_tag = str(asset.get("asset_tag", "")).strip()
    serial = str(asset.get("serial", "")).strip()

    if search == asset_tag or search == serial:
        found.append(asset)

if not found:
    print()
    print("No asset found.")
else:
    print()
    print("Asset found")
    print("=" * 40)

    for asset in found:
        print("ID:", asset.get("id"))
        print("Asset tag:", asset.get("asset_tag"))
        print("Name:", asset.get("name"))
        print("Serial:", asset.get("serial"))

        model = asset.get("model") or {}
        print("Model:", model.get("name"))

        status = asset.get("status_label") or {}
        print("Status:", status.get("name"))

        print()