from inventory_api import get

data = get("/hardware")

print()
print("Assigned assets")
print("=" * 60)

for asset in data["rows"]:
    assigned = asset.get("assigned_to")

    if assigned:
        print(
            "ID:", asset.get("id"),
            "| Tag:", asset.get("asset_tag"),
            "| Name:", asset.get("name"),
            "| Assigned to:", assigned.get("name"),
            "| Type:", assigned.get("type")
        )