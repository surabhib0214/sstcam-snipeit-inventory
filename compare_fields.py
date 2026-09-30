from inventory_api import get


def get_asset():
    data = get("/hardware")

    if not data.get("rows"):
        return {}

    return data["rows"][0]


def get_component():
    data = get("/components")

    if not data.get("rows"):
        return {}

    return data["rows"][0]


asset = get_asset()
component = get_component()

asset_fields = set(asset.keys())
component_fields = set(component.keys())

common_fields = sorted(asset_fields & component_fields)
asset_only = sorted(asset_fields - component_fields)
component_only = sorted(component_fields - asset_fields)


print("=" * 70)
print("SSTCAM ASSET / COMPONENT FIELD COMPARISON")
print("=" * 70)

print()
print("COMMON FIELDS")
print("-" * 70)

for field in common_fields:
    print(field)

print()
print("ASSET-ONLY FIELDS")
print("-" * 70)

for field in asset_only:
    print(field)

print()
print("COMPONENT-ONLY FIELDS")
print("-" * 70)

for field in component_only:
    print(field)

print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)

print("Asset fields:", len(asset_fields))
print("Component fields:", len(component_fields))
print("Common fields:", len(common_fields))
print("Asset-only fields:", len(asset_only))
print("Component-only fields:", len(component_only))

print()
print("NO CHANGES WERE MADE.")