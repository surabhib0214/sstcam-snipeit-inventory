from inventory_api import get, put

asset_id = input("Enter asset ID: ").strip()

asset = get(f"/hardware/{asset_id}")

print()
print("Asset:", asset.get("name"))
print("Asset tag:", asset.get("asset_tag"))

current_notes = asset.get("notes") or ""

print()
print("Current notes:")
print("-" * 40)

if current_notes:
    print(current_notes)
else:
    print("(none)")

print()

new_note = input("Enter new note: ").strip()

if not new_note:
    print("No note entered. Nothing changed.")
    exit()

if current_notes:
    updated_notes = current_notes + "\n" + new_note
else:
    updated_notes = new_note

payload = {
    "notes": updated_notes
}

put(f"/hardware/{asset_id}", payload)

print()
print("✔ Notes updated successfully.")