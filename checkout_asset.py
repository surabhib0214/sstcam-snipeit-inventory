from inventory_api import get, post

asset_id = input("Enter asset ID: ").strip()

asset = get(f"/hardware/{asset_id}")

print()
print("=" * 50)
print("ASSET TO CHECK OUT")
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

target_id = input("Enter destination asset ID: ").strip()

if not target_id:
    print("No destination entered. Nothing changed.")
    exit()

if not target_id.isdigit():
    print("Destination asset ID must be a number.")
    exit()

print()
print("Destination asset ID:", target_id)
print()

confirmation = input(
    "Type CHECK OUT to continue: "
).strip()

if confirmation != "CHECK OUT":
    print("Nothing changed.")
    exit()

payload = {
    "checkout_to_type": "asset",
    "assigned_asset": int(target_id)
}

print()
print("Sending checkout request...")

result = post(
    f"/hardware/{asset_id}/checkout",
    payload
)

print()
print("API response:")
print(result)

print()
print("✔ Checkout request completed.")
