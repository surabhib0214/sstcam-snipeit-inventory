from inventory_api import get


def get_all_assets():
    data = get("/hardware")
    return data.get("rows", [])


def get_all_components():
    data = get("/components")
    return data.get("rows", [])


def audit_assets(assets):
    print()
    print("=" * 70)
    print("ASSET AUDIT")
    print("=" * 70)

    print("Total assets:", len(assets))
    print()

    missing_asset_tag = []
    missing_serial = []
    missing_model = []
    missing_category = []
    missing_status = []

    for asset in assets:

        asset_id = asset.get("id")
        asset_tag = asset.get("asset_tag")
        serial = asset.get("serial")
        model = asset.get("model")
        category = asset.get("category")
        status = asset.get("status_label")

        if not asset_tag:
            missing_asset_tag.append(asset)

        if not serial:
            missing_serial.append(asset)

        if not model:
            missing_model.append(asset)

        if not category:
            missing_category.append(asset)

        if not status:
            missing_status.append(asset)

    print("Missing asset tag:", len(missing_asset_tag))
    print("Missing serial:", len(missing_serial))
    print("Missing model:", len(missing_model))
    print("Missing category:", len(missing_category))
    print("Missing status:", len(missing_status))

    print()

    if missing_asset_tag:
        print("Assets missing asset tag:")
        for asset in missing_asset_tag:
            print(
                "  ID:", asset.get("id"),
                "| Name:", asset.get("name")
            )
        print()

    if missing_model:
        print("Assets missing model:")
        for asset in missing_model:
            print(
                "  ID:", asset.get("id"),
                "| Tag:", asset.get("asset_tag"),
                "| Name:", asset.get("name")
            )
        print()

    if missing_category:
        print("Assets missing category:")
        for asset in missing_category:
            print(
                "  ID:", asset.get("id"),
                "| Tag:", asset.get("asset_tag"),
                "| Name:", asset.get("name")
            )
        print()


def audit_components(components):
    print()
    print("=" * 70)
    print("COMPONENT AUDIT")
    print("=" * 70)

    print("Total components:", len(components))
    print()

    missing_category = []
    missing_location = []

    for component in components:

        category = component.get("category")
        location = component.get("location")

        if not category:
            missing_category.append(component)

        if not location:
            missing_location.append(component)

    print("Missing category:", len(missing_category))
    print("Missing location:", len(missing_location))

    print()

    if missing_category:
        print("Components missing category:")
        for component in missing_category:
            print(
                "  ID:", component.get("id"),
                "| Name:", component.get("name")
            )
        print()

    if missing_location:
        print("Components missing location:")
        for component in missing_location:
            print(
                "  ID:", component.get("id"),
                "| Name:", component.get("name")
            )
        print()


print("=" * 70)
print("SSTCAM INVENTORY AUDIT")
print("=" * 70)

print()
print("Reading inventory...")
print("No changes will be made.")

assets = get_all_assets()
components = get_all_components()

audit_assets(assets)
audit_components(components)

print()
print("=" * 70)
print("AUDIT COMPLETE")
print("=" * 70)
print()
print("NO CHANGES WERE MADE TO THE INVENTORY.")