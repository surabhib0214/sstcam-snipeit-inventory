from collections import defaultdict

from inventory_api import get


ECAMI_ASSET_ID = 126


def get_all_assets():
    data = get("/hardware")
    return data.get("rows", [])


def get_ecami_assets(assets):
    ecami_assets = []

    for asset in assets:

        assigned = asset.get("assigned_to")

        if not assigned:
            continue

        if assigned.get("type") != "asset":
            continue

        if assigned.get("id") != ECAMI_ASSET_ID:
            continue

        ecami_assets.append(asset)

    return ecami_assets


def group_by_category(assets):
    categories = defaultdict(list)

    for asset in assets:

        category = asset.get("category") or {}

        category_name = category.get("name") or "Uncategorised"

        categories[category_name].append(asset)

    return categories


def print_asset(asset):
    print(
        "ID:", asset.get("id"),
        "| Tag:", asset.get("asset_tag"),
        "| Name:", asset.get("name"),
        "| Serial:", asset.get("serial")
    )


print("=" * 70)
print("ECAMi INVENTORY")
print("=" * 70)

print()
print("ECAMi asset ID:", ECAMI_ASSET_ID)

print()
print("Reading inventory...")

assets = get_all_assets()

ecami_assets = get_ecami_assets(assets)

categories = group_by_category(ecami_assets)

print()
print("=" * 70)
print("ASSETS CHECKED OUT TO ECAMi")
print("=" * 70)

if not ecami_assets:

    print()
    print("No assets are currently checked out to ECAMi.")

else:

    for category_name in sorted(categories):

        print()
        print(category_name)
        print("-" * 70)

        category_assets = categories[category_name]

        for asset in category_assets:
            print_asset(asset)

        print()
        print("Category total:", len(category_assets))


print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)

print()
print("Total assets in ECAMi:", len(ecami_assets))

print()
print("Categories represented:", len(categories))

print()
print("=" * 70)
print("NO CHANGES WERE MADE.")
print("=" * 70)