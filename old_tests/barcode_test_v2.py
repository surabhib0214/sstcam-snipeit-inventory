from inventory_api import get

print("=" * 60)
print("SSTCAM SNIPE-IT QR / BARCODE TEST")
print("=" * 60)
print()
print("Scan a barcode or QR code.")
print("You can also type an asset tag or serial number.")
print()

scan = input("Scan: ").strip()

if not scan:
    print("Nothing entered.")
    exit()


# --------------------------------------------------
# Check if this is a Snipe-IT URL
# --------------------------------------------------

if scan.startswith("https://sstcam-inventory.ecap.work/"):

    print()
    print("Snipe-IT URL detected.")
    print("URL:", scan)

    # Hardware URL
    if "/hardware/" in scan:
        asset_id = scan.split("/hardware/")[-1].split("/")[0]

        if asset_id.isdigit():
            print("Detected asset ID:", asset_id)

            asset = get(f"/hardware/{asset_id}")

            print()
            print("=" * 60)
            print("ASSET FOUND")
            print("=" * 60)

            print("ID:", asset.get("id"))
            print("Asset tag:", asset.get("asset_tag"))
            print("Name:", asset.get("name"))
            print("Serial:", asset.get("serial"))

            model = asset.get("model") or {}
            print("Model:", model.get("name"))

            category = asset.get("category") or {}
            print("Category:", category.get("name"))

            status = asset.get("status_label") or {}
            print("Status:", status.get("name"))

            location = asset.get("location")

            if location:
                print("Location:", location.get("name"))
            else:
                print("Location: Not assigned")

            assigned_to = asset.get("assigned_to")

            if assigned_to:
                print("Assigned to:", assigned_to.get("name"))
                print("Assignment type:", assigned_to.get("type"))
            else:
                print("Assigned to: Nobody")

            print()
            print("✔ Asset QR lookup successful.")
            exit()

    # Component URL
    if "/components/" in scan:
        component_id = scan.split("/components/")[-1].split("/")[0]

        if component_id.isdigit():
            print("Detected component ID:", component_id)

            component = get(f"/components/{component_id}")

            print()
            print("=" * 60)
            print("COMPONENT FOUND")
            print("=" * 60)

            print("ID:", component.get("id"))
            print("Name:", component.get("name"))
            print("Serial:", component.get("serial"))
            print("Asset tag:", component.get("asset_tag"))

            category = component.get("category") or {}
            print("Category:", category.get("name"))

            print()
            print("✔ Component QR lookup successful.")
            exit()

    print()
    print("❌ Snipe-IT URL format not recognised.")
    exit()


# --------------------------------------------------
# Otherwise treat the scan as an asset tag/serial
# --------------------------------------------------

print()
print("Searching asset tag / serial number...")

data = get("/hardware")

asset = None

for item in data["rows"]:

    asset_tag = str(item.get("asset_tag", "")).strip()
    serial = str(item.get("serial", "")).strip()

    if scan == asset_tag or scan == serial:
        asset = item
        break


if not asset:
    print()
    print("❌ Asset not found.")
    exit()


print()
print("=" * 60)
print("ASSET FOUND")
print("=" * 60)

print("ID:", asset.get("id"))
print("Asset tag:", asset.get("asset_tag"))
print("Name:", asset.get("name"))
print("Serial:", asset.get("serial"))

model = asset.get("model") or {}
print("Model:", model.get("name"))

category = asset.get("category") or {}
print("Category:", category.get("name"))

status = asset.get("status_label") or {}
print("Status:", status.get("name"))

location = asset.get("location")

if location:
    print("Location:", location.get("name"))
else:
    print("Location: Not assigned")

assigned_to = asset.get("assigned_to")

if assigned_to:
    print("Assigned to:", assigned_to.get("name"))
    print("Assignment type:", assigned_to.get("type"))
else:
    print("Assigned to: Nobody")

print()
print("✔ Barcode lookup successful.")
