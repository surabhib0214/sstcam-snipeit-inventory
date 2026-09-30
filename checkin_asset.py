from inventory_api import get, post

asset_id = input("Enter asset ID: ").strip()

asset = get(f"/hardware/{asset_id}")

print()
print("=" * 50)
print("ASSET TO CHECK IN")
print("=" * 50)

print("ID:", asset.get("id"))
print("Asset tag:", asset.get("asset_tag"))
print("Name:", asset.get("name"))

assigned_to = asset.get("assigned_to")

if assigned_to:
    print("Currently assigned to:", assigned_to.get("name"))
    print("Assignment type:", assigned_to.get("type"))
else:
    print("Currently assigned to: Nobody")

print()

confirmation = input(
    "Type CHECK IN to continue: "
).strip()

if confirmation != "CHECK IN":
    print("Nothing changed.")
    exit()

result = post(f"/hardware/{asset_id}/checkin")

print()
print("✔ Asset checked in successfully.")