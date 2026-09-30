from inventory_api import get, put

search = input("Scan asset tag or enter serial number: ").strip()

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

asset_id = asset.get("id")

print()
print("=" * 50)
print("ASSET FOUND")
print("=" * 50)

print("ID:", asset_id)
print("Asset tag:", asset.get("asset_tag"))
print("Name:", asset.get("name"))
print("Serial:", asset.get("serial"))

model = asset.get("model") or {}
print("Model:", model.get("name"))

location = asset.get("location")
if location:
    print("Location:", location.get("name"))
else:
    print("Location: Not assigned")

print()

current_notes = asset.get("notes") or ""

print("Current notes:")
print("-" * 50)

if current_notes:
    print(current_notes)
else:
    print("(none)")

print()

problem = input("Enter the problem: ").strip()

if not problem:
    print("No problem entered. Nothing changed.")
    exit()

issue_note = f"Issue: {problem}"

if current_notes:
    updated_notes = current_notes + "\n" + issue_note
else:
    updated_notes = issue_note

payload = {
    "notes": updated_notes
}

put(f"/hardware/{asset_id}", payload)

print()
print("✔ Issue recorded successfully.")