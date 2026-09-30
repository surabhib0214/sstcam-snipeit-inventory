from inventory_api import get

ECAMI_ASSET_ID = 126
TM_MODEL_NAME = "SSTCAM Target Module"


def get_all_assets():
    data = get("/hardware")
    return data["rows"]


def get_ecami_tms(assets):
    tms = []

    for asset in assets:
        model = asset.get("model") or {}
        assigned = asset.get("assigned_to")

        if model.get("name") != TM_MODEL_NAME:
            continue

        if not assigned:
            continue

        if assigned.get("type") != "asset":
            continue

        if assigned.get("id") != ECAMI_ASSET_ID:
            continue

        tms.append(asset)

    return tms


def get_available_tms(assets):
    tms = []

    for asset in assets:
        model = asset.get("model") or {}
        assigned = asset.get("assigned_to")
        status = asset.get("status_label") or {}

        if model.get("name") != TM_MODEL_NAME:
            continue

        if status.get("name") != "Ready to Deploy":
            continue

        if assigned:
            if (
                assigned.get("type") == "asset"
                and assigned.get("id") == ECAMI_ASSET_ID
            ):
                continue

        tms.append(asset)

    return tms


def print_tm(tm):
    print(
        "ID:",
        tm.get("id"),
        "| Tag:",
        tm.get("asset_tag"),
        "| Name:",
        tm.get("name"),
        "| Serial:",
        tm.get("serial")
    )


print("=" * 70)
print("ECAMi TARGET MODULE MANAGEMENT")
print("=" * 70)

assets = get_all_assets()

ecami_tms = get_ecami_tms(assets)
available_tms = get_available_tms(assets)

print()
print("TARGET MODULES CURRENTLY IN ECAMi")
print("-" * 70)

if ecami_tms:
    for tm in ecami_tms:
        print_tm(tm)
else:
    print("No Target Modules currently assigned to ECAMi.")

print()
print("TARGET MODULES READY TO DEPLOY")
print("-" * 70)

if available_tms:
    for tm in available_tms:
        print_tm(tm)
else:
    print("No Target Modules available.")

print()
print("=" * 70)
print("Total in ECAMi:", len(ecami_tms))
print("Total available:", len(available_tms))
print("=" * 70)