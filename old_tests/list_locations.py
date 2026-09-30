from inventory_api import get


def get_locations():
    data = get("/locations")
    return data.get("rows", [])


locations = get_locations()

print("=" * 70)
print("SSTCAM LOCATIONS")
print("=" * 70)

print()
print("Total locations:", len(locations))
print()

for location in locations:

    print(
        "ID:", location.get("id"),
        "| Name:", location.get("name")
    )

print()
print("=" * 70)
print("LOCATION LIST COMPLETE")
print("=" * 70)

print()
print("NO CHANGES WERE MADE.")