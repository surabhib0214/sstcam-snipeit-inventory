from inventory_api import get

asset_id = input("Enter asset ID: ").strip()

asset = get(f"/hardware/{asset_id}")

print()
print("Asset:", asset.get("name"))
print("Asset tag:", asset.get("asset_tag"))
print()

notes = asset.get("notes")

if notes:
    print("Current Notes:")
    print("-" * 40)
    print(notes)
else:
    print("No notes currently recorded.")