from inventory_api import get


print("Getting assets from SSTCam inventory...")
print()


data = get("/hardware")


print("Number of assets returned:", len(data["rows"]))
print()


for asset in data["rows"]:

    asset_id = asset.get("id")
    asset_tag = asset.get("asset_tag")
    name = asset.get("name")

    print(
        asset_id,
        "|",
        asset_tag,
        "|",
        name
    )