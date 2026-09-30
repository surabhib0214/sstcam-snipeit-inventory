from nicegui import ui

from inventory_api import get, post, put

import os


# =========================================================
# Configuration
# =========================================================

ECAMI_ASSET_ID = 126


# =========================================================
# General helpers
# =========================================================

def get_all_assets():
    result = get("/hardware")

    if isinstance(result, dict):
        return result.get("rows", [])

    return result or []


def get_all_components():
    result = get("/components")

    if isinstance(result, dict):
        return result.get("rows", [])

    return result or []


def asset_label(asset):
    asset_tag = asset.get("asset_tag") or "-"
    serial = asset.get("serial") or "-"
    name = asset.get("name") or "-"

    return f"{asset_tag} | {serial} | {name}"


def is_ecami_asset(asset):
    assigned_to = asset.get("assigned_to") or {}
    assigned_asset = (
        asset.get("assigned_asset")
        or asset.get("assigned_asset_id")
        or {}
    )

    if isinstance(assigned_to, dict):
        if assigned_to.get("id") == ECAMI_ASSET_ID:
            return True

        if assigned_to.get("asset_id") == ECAMI_ASSET_ID:
            return True

    if isinstance(assigned_asset, dict):
        if assigned_asset.get("id") == ECAMI_ASSET_ID:
            return True

    if assigned_asset == ECAMI_ASSET_ID:
        return True

    return False


def get_assignment_text(asset):
    """
    Return a clear human-readable assignment.
    """

    assigned_to = asset.get("assigned_to")

    if not assigned_to:
        return "Not assigned"

    if isinstance(assigned_to, dict):

        name = (
            assigned_to.get("name")
            or assigned_to.get("display_name")
            or assigned_to.get("asset_tag")
            or assigned_to.get("serial")
        )

        if name:
            return str(name)

    if isinstance(assigned_to, str):
        return assigned_to

    assigned_asset = asset.get("assigned_asset")

    if isinstance(assigned_asset, dict):

        name = (
            assigned_asset.get("name")
            or assigned_asset.get("asset_tag")
            or assigned_asset.get("serial")
        )

        if name:
            return str(name)

    return "Assigned"


def find_asset(search_value):
    search_value = str(search_value).strip().lower()

    if not search_value:
        return None

    assets = get_all_assets()

    for asset in assets:

        asset_id = str(asset.get("id") or "").lower()
        asset_tag = str(asset.get("asset_tag") or "").lower()
        serial = str(asset.get("serial") or "").lower()
        name = str(asset.get("name") or "").lower()

        if search_value in {
            asset_id,
            asset_tag,
            serial,
            name,
        }:
            return asset

    for asset in assets:

        values = [
            str(asset.get("asset_tag") or "").lower(),
            str(asset.get("serial") or "").lower(),
            str(asset.get("name") or "").lower(),
        ]

        if any(search_value in value for value in values):
            return asset

    return None


def find_tm(search_value):
    search_value = str(search_value).strip().lower()

    if not search_value:
        return None

    assets = get_all_assets()

    for asset in assets:

        model = asset.get("model") or {}
        model_name = ""

        if isinstance(model, dict):
            model_name = str(
                model.get("name") or ""
            ).lower()
        else:
            model_name = str(model).lower()

        category = asset.get("category") or {}
        category_name = ""

        if isinstance(category, dict):
            category_name = str(
                category.get("name") or ""
            ).lower()
        else:
            category_name = str(category).lower()

        asset_tag = str(
            asset.get("asset_tag") or ""
        ).lower()

        serial = str(
            asset.get("serial") or ""
        ).lower()

        name = str(
            asset.get("name") or ""
        ).lower()

        is_target_module = (
            "target module" in model_name
            or "target module" in category_name
            or asset_tag.startswith("tm")
            or serial.startswith("tm")
            or name.startswith("tm")
        )

        if not is_target_module:
            continue

        if search_value in {
            str(asset.get("id") or "").lower(),
            asset_tag,
            serial,
            name,
        }:
            return asset

        if (
            search_value in asset_tag
            or search_value in serial
            or search_value in name
        ):
            return asset

    return None


def show_error(message):
    ui.notify(
        message,
        type="negative",
        position="top"
    )


def show_success(message):
    ui.notify(
        message,
        type="positive",
        position="top"
    )


def show_info(message):
    ui.notify(
        message,
        type="info",
        position="top"
    )


# =========================================================
# Header
# =========================================================

ui.page_title("SSTCam Inventory")

with ui.header().classes(
    "items-center justify-between"
):

    with ui.row().classes("items-center"):

        ui.icon(
            "inventory_2",
            size="32px"
        )

        ui.label(
            "SSTCam Inventory"
        ).classes("text-h5")

    ui.label(
        "Snipe-IT"
    ).classes("text-grey-3")


# =========================================================
# Tabs
# =========================================================

with ui.tabs().classes("w-full") as tabs:

    dashboard_tab = ui.tab(
        "Dashboard",
        icon="dashboard"
    )

    assets_tab = ui.tab(
        "Assets",
        icon="qr_code_scanner"
    )

    ecami_tab = ui.tab(
        "ECAMi",
        icon="camera"
    )

    tm_tab = ui.tab(
        "Target Modules",
        icon="memory"
    )

    components_tab = ui.tab(
        "Components",
        icon="construction"
    )

    audit_tab = ui.tab(
        "Audit",
        icon="fact_check"
    )


with ui.tab_panels(
    tabs,
    value=dashboard_tab
).classes("w-full"):


    # =====================================================
    # Dashboard
    # =====================================================

    with ui.tab_panel(dashboard_tab):

        ui.label(
            "Inventory Dashboard"
        ).classes("text-h4")

        ui.label(
            "Quick overview of the SSTCam inventory."
        ).classes("text-grey-7")

        dashboard_cards = ui.row().classes(
            "w-full gap-4"
        )

        def load_dashboard():

            dashboard_cards.clear()

            with dashboard_cards:

                for title, icon in [
                    ("Assets", "inventory_2"),
                    ("Components", "construction"),
                    ("ECAMi Assets", "camera"),
                    ("Target Modules", "memory"),
                ]:

                    with ui.card().classes("w-60"):

                        with ui.row().classes(
                            "items-center"
                        ):

                            ui.icon(
                                icon,
                                size="28px"
                            )

                            ui.label(
                                title
                            ).classes("text-subtitle1")

                        ui.label(
                            "Loading..."
                        ).classes("text-h5")

            try:

                assets = get_all_assets()
                components = get_all_components()

                ecami_assets = [
                    asset
                    for asset in assets
                    if is_ecami_asset(asset)
                ]

                target_modules = []

                for asset in assets:

                    model = asset.get("model") or {}

                    if isinstance(model, dict):
                        model_name = str(
                            model.get("name") or ""
                        ).lower()
                    else:
                        model_name = str(model).lower()

                    if "target module" in model_name:
                        target_modules.append(asset)

                dashboard_cards.clear()

                with dashboard_cards:

                    values = [
                        (
                            "Assets",
                            len(assets),
                            "inventory_2"
                        ),
                        (
                            "Components",
                            len(components),
                            "construction"
                        ),
                        (
                            "ECAMi Assets",
                            len(ecami_assets),
                            "camera"
                        ),
                        (
                            "Target Modules",
                            len(target_modules),
                            "memory"
                        ),
                    ]

                    for title, value, icon in values:

                        with ui.card().classes("w-60"):

                            with ui.row().classes(
                                "items-center"
                            ):

                                ui.icon(
                                    icon,
                                    size="28px"
                                )

                                ui.label(
                                    title
                                ).classes("text-subtitle1")

                            ui.label(
                                str(value)
                            ).classes("text-h4")

            except Exception as error:

                dashboard_cards.clear()

                with dashboard_cards:

                    ui.label(
                        f"Could not load dashboard: {error}"
                    ).classes("text-negative")

        ui.button(
            "Refresh Dashboard",
            icon="refresh",
            on_click=load_dashboard
        )

        load_dashboard()


    # =====================================================
    # Assets
    # =====================================================

    with ui.tab_panel(assets_tab):

        ui.label(
            "Asset Scanner"
        ).classes("text-h4")

        ui.label(
            "Scan a barcode or enter an asset tag, serial number, "
            "name, or Snipe-IT asset ID."
        ).classes("text-grey-7")

        asset_search = ui.input(
            label="Scan or search asset",
            placeholder="Scan barcode and press Enter"
        ).props(
            "outlined clearable"
        ).classes(
            "w-full"
        )

        asset_result = ui.column().classes(
            "w-full"
        )

        asset_actions = ui.row().classes(
            "w-full"
        )

        current_asset = {
            "value": None
        }

        def display_asset(asset):

            current_asset["value"] = asset

            asset_result.clear()
            asset_actions.clear()

            if not asset:

                with asset_result:

                    ui.label(
                        "Asset not found."
                    ).classes("text-negative")

                return

            assignment = get_assignment_text(asset)

            with asset_result:

                with ui.card().classes(
                    "w-full"
                ):

                    ui.label(
                        asset.get("name") or "-"
                    ).classes("text-h5")

                    ui.separator()

                    ui.label(
                        f"Asset ID: {asset.get('id') or '-'}"
                    )

                    ui.label(
                        f"Asset Tag: {asset.get('asset_tag') or '-'}"
                    )

                    ui.label(
                        f"Serial: {asset.get('serial') or '-'}"
                    )

                    model = asset.get("model") or {}

                    if isinstance(model, dict):
                        model_name = (
                            model.get("name") or "-"
                        )
                    else:
                        model_name = str(model)

                    ui.label(
                        f"Model: {model_name}"
                    )

                    category = asset.get("category") or {}

                    if isinstance(category, dict):
                        category_name = (
                            category.get("name") or "-"
                        )
                    else:
                        category_name = str(category)

                    ui.label(
                        f"Category: {category_name}"
                    )

                    status = asset.get("status_label") or {}

                    if isinstance(status, dict):
                        status_name = (
                            status.get("name") or "-"
                        )
                    else:
                        status_name = str(status)

                    ui.label(
                        f"Status: {status_name}"
                    )

                    location = asset.get("location") or {}

                    if isinstance(location, dict):
                        location_name = (
                            location.get("name") or "-"
                        )
                    else:
                        location_name = str(location)

                    ui.label(
                        f"Location: {location_name}"
                    )

                    # -------------------------------------
                    # NEW: Assignment display
                    # -------------------------------------

                    ui.separator()

                    with ui.row().classes(
                        "items-center"
                    ):

                        ui.icon(
                            "assignment_ind"
                        )

                        ui.label(
                            "Assigned To:"
                        ).classes(
                            "text-subtitle1"
                        )

                        assignment_label = ui.label(
                            assignment
                        )

                        if assignment == "Not assigned":

                            assignment_label.classes(
                                "text-grey-7"
                            )

                        else:

                            assignment_label.classes(
                                "text-positive"
                            )

                    if is_ecami_asset(asset):

                        ui.label(
                            "Currently assigned to ECAMi"
                        ).classes(
                            "text-positive"
                        )

                    notes = asset.get("notes")

                    if notes:

                        ui.separator()

                        ui.label(
                            f"Notes: {notes}"
                        )

            with asset_actions:

                ui.button(
                    "Check Out to ECAMi",
                    icon="output",
                    on_click=checkout_current_asset
                )

                ui.button(
                    "Check In",
                    icon="input",
                    on_click=checkin_current_asset
                )

                ui.button(
                    "Report Issue",
                    icon="report_problem",
                    on_click=report_current_asset_issue
                )

                ui.button(
                    "Refresh",
                    icon="refresh",
                    on_click=refresh_current_asset
                ).props("flat")

        def search_asset():

            value = asset_search.value

            if not value:

                show_info(
                    "Scan or enter an asset first."
                )

                return

            try:

                asset = find_asset(value)

                display_asset(asset)

                if asset:

                    show_success(
                        "Asset found."
                    )

                else:

                    show_error(
                        "Asset not found."
                    )

            except Exception as error:

                asset_result.clear()

                with asset_result:

                    ui.label(
                        f"Search failed: {error}"
                    ).classes("text-negative")

                show_error(
                    "Could not search for the asset."
                )

        def refresh_current_asset():

            asset = current_asset.get("value")

            if not asset:

                show_info(
                    "No asset selected."
                )

                return

            try:

                refreshed = get(
                    f"/hardware/{asset.get('id')}"
                )

                display_asset(refreshed)

                show_success(
                    "Asset refreshed."
                )

            except Exception as error:

                show_error(
                    f"Refresh failed: {error}"
                )

        def checkout_current_asset():

            asset = current_asset.get("value")

            if not asset:

                show_info(
                    "Select an asset first."
                )

                return

            asset_id = asset.get("id")

            with ui.dialog() as dialog:

                with ui.card():

                    ui.label(
                        "Check Out Asset"
                    ).classes("text-h6")

                    ui.label(
                        "This will assign the selected asset to ECAMi."
                    )

                    ui.label(
                        asset_label(asset)
                    ).classes("text-grey-7")

                    with ui.row():

                        ui.button(
                            "Cancel",
                            on_click=dialog.close
                        ).props("flat")

                        def confirm_checkout():

                            try:

                                post(
                                    f"/hardware/{asset_id}/checkout",
                                    {
                                        "checkout_to_type": "asset",
                                        "assigned_asset": ECAMI_ASSET_ID,
                                    }
                                )

                                dialog.close()

                                show_success(
                                    "Asset checked out to ECAMi."
                                )

                                refresh_current_asset()

                            except Exception as error:

                                show_error(
                                    f"Checkout failed: {error}"
                                )

                        ui.button(
                            "Check Out",
                            on_click=confirm_checkout
                        )

            dialog.open()

        def checkin_current_asset():

            asset = current_asset.get("value")

            if not asset:

                show_info(
                    "Select an asset first."
                )

                return

            asset_id = asset.get("id")

            with ui.dialog() as dialog:

                with ui.card():

                    ui.label(
                        "Check In Asset"
                    ).classes("text-h6")

                    ui.label(
                        "This will check the asset back into inventory."
                    )

                    ui.label(
                        asset_label(asset)
                    ).classes("text-grey-7")

                    with ui.row():

                        ui.button(
                            "Cancel",
                            on_click=dialog.close
                        ).props("flat")

                        def confirm_checkin():

                            try:

                                post(
                                    f"/hardware/{asset_id}/checkin"
                                )

                                dialog.close()

                                show_success(
                                    "Asset checked in."
                                )

                                refresh_current_asset()

                            except Exception as error:

                                show_error(
                                    f"Check-in failed: {error}"
                                )

                        ui.button(
                            "Check In",
                            on_click=confirm_checkin
                        )

            dialog.open()

        def report_current_asset_issue():

            asset = current_asset.get("value")

            if not asset:

                show_info(
                    "Select an asset first."
                )

                return

            with ui.dialog() as dialog:

                with ui.card().classes("w-96"):

                    ui.label(
                        "Report Issue"
                    ).classes("text-h6")

                    issue_input = ui.textarea(
                        label="Describe the problem"
                    ).props(
                        "outlined"
                    ).classes(
                        "w-full"
                    )

                    with ui.row():

                        ui.button(
                            "Cancel",
                            on_click=dialog.close
                        ).props("flat")

                        def save_issue():

                            problem = (
                                issue_input.value or ""
                            ).strip()

                            if not problem:

                                show_info(
                                    "Enter a problem description."
                                )

                                return

                            try:

                                asset_id = asset.get("id")

                                existing_notes = (
                                    asset.get("notes") or ""
                                )

                                issue_text = (
                                    f"Issue: {problem}"
                                )

                                if existing_notes:

                                    new_notes = (
                                        existing_notes
                                        + "\n"
                                        + issue_text
                                    )

                                else:

                                    new_notes = issue_text

                                put(
                                    f"/hardware/{asset_id}",
                                    {
                                        "notes": new_notes
                                    }
                                )

                                dialog.close()

                                show_success(
                                    "Issue reported."
                                )

                                refresh_current_asset()

                            except Exception as error:

                                show_error(
                                    f"Could not report issue: {error}"
                                )

                        ui.button(
                            "Report Issue",
                            icon="report_problem",
                            on_click=save_issue
                        )

            dialog.open()

        asset_search.on(
            "keydown.enter",
            lambda e: search_asset()
        )

        with ui.row():

            ui.button(
                "Search",
                icon="search",
                on_click=search_asset
            )

            ui.button(
                "Clear",
                icon="clear",
                on_click=lambda: (
                    setattr(
                        asset_search,
                        "value",
                        ""
                    ),
                    asset_result.clear(),
                    asset_actions.clear()
                )
            ).props("flat")


    # =====================================================
    # ECAMi
    # =====================================================

    with ui.tab_panel(ecami_tab):

        ui.label(
            "ECAMi Inventory"
        ).classes("text-h4")

        ui.label(
            "Assets currently assigned to the ECAMi camera unit."
        ).classes("text-grey-7")

        ecami_result = ui.column().classes(
            "w-full"
        )

        def load_ecami_inventory():

            ecami_result.clear()

            with ecami_result:

                ui.label(
                    "Loading ECAMi inventory..."
                ).classes("text-grey-7")

            try:

                assets = get_all_assets()

                ecami_assets = [
                    asset
                    for asset in assets
                    if is_ecami_asset(asset)
                ]

                categories = {}

                for asset in ecami_assets:

                    category = asset.get("category") or {}

                    category_name = (
                        category.get("name")
                        or "Uncategorized"
                    )

                    categories.setdefault(
                        category_name,
                        []
                    ).append(asset)

                ecami_result.clear()

                with ecami_result:

                    with ui.row().classes(
                        "w-full items-center justify-between"
                    ):

                        ui.label(
                            f"{len(ecami_assets)} assets assigned to ECAMi"
                        ).classes("text-h6")

                        ui.button(
                            "Refresh",
                            icon="refresh",
                            on_click=load_ecami_inventory
                        ).props("flat")

                    if not ecami_assets:

                        ui.label(
                            "No assets are currently assigned to ECAMi."
                        ).classes("text-grey-7")

                        return

                    for category_name in sorted(categories):

                        category_assets = categories[
                            category_name
                        ]

                        with ui.expansion(
                            f"{category_name} "
                            f"({len(category_assets)})",
                            icon="folder"
                        ).classes("w-full"):

                            for asset in sorted(
                                category_assets,
                                key=asset_label
                            ):

                                ui.label(
                                    f"{asset.get('asset_tag') or '-'} | "
                                    f"{asset.get('serial') or '-'} | "
                                    f"{asset.get('name') or '-'}"
                                )

            except Exception as error:

                ecami_result.clear()

                with ecami_result:

                    ui.label(
                        f"Could not load ECAMi inventory: {error}"
                    ).classes("text-negative")

        ui.button(
            "Load / Refresh ECAMi Inventory",
            icon="refresh",
            on_click=load_ecami_inventory
        )

        load_ecami_inventory()


    # =====================================================
    # Target Modules
    # =====================================================

    with ui.tab_panel(tm_tab):

        ui.label(
            "Target Modules"
        ).classes("text-h4")

        ui.label(
            "Search, view, add, or remove Target Modules."
        ).classes("text-grey-7")

        tm_search = ui.input(
            label="Search Target Module",
            placeholder="TM0051, asset tag, serial, or ID"
        ).props(
            "outlined clearable"
        ).classes(
            "w-full"
        )

        tm_result = ui.column().classes(
            "w-full"
        )

        tm_actions = ui.row().classes(
            "w-full"
        )

        current_tm = {
            "value": None
        }

        def display_tm(asset):

            current_tm["value"] = asset

            tm_result.clear()
            tm_actions.clear()

            if not asset:

                with tm_result:

                    ui.label(
                        "Target Module not found."
                    ).classes("text-negative")

                return

            with tm_result:

                with ui.card().classes(
                    "w-full"
                ):

                    ui.label(
                        asset.get("name") or "-"
                    ).classes("text-h5")

                    ui.label(
                        f"Asset ID: {asset.get('id') or '-'}"
                    )

                    ui.label(
                        f"Asset Tag: {asset.get('asset_tag') or '-'}"
                    )

                    ui.label(
                        f"Serial: {asset.get('serial') or '-'}"
                    )

                    model = asset.get("model") or {}

                    if isinstance(model, dict):
                        model_name = (
                            model.get("name") or "-"
                        )
                    else:
                        model_name = str(model)

                    ui.label(
                        f"Model: {model_name}"
                    )

                    ui.label(
                        f"Assigned To: "
                        f"{get_assignment_text(asset)}"
                    )

                    if is_ecami_asset(asset):

                        ui.label(
                            "Currently assigned to ECAMi"
                        ).classes("text-positive")

                    else:

                        ui.label(
                            "Not currently assigned to ECAMi"
                        ).classes("text-grey-7")

            with tm_actions:

                if is_ecami_asset(asset):

                    ui.button(
                        "Remove from ECAMi",
                        icon="remove_circle",
                        on_click=remove_current_tm
                    )

                else:

                    ui.button(
                        "Add to ECAMi",
                        icon="add_circle",
                        on_click=add_current_tm
                    )

        def search_tm():

            value = tm_search.value

            if not value:

                show_info(
                    "Enter a Target Module search value."
                )

                return

            try:

                asset = find_tm(value)

                display_tm(asset)

                if asset:

                    show_success(
                        "Target Module found."
                    )

                else:

                    show_error(
                        "Target Module not found."
                    )

            except Exception as error:

                show_error(
                    f"Search failed: {error}"
                )

        def add_current_tm():

            asset = current_tm.get("value")

            if not asset:
                return

            with ui.dialog() as dialog:

                with ui.card():

                    ui.label(
                        "Add Target Module"
                    ).classes("text-h6")

                    ui.label(
                        f"Add {asset_label(asset)} to ECAMi?"
                    )

                    with ui.row():

                        ui.button(
                            "Cancel",
                            on_click=dialog.close
                        ).props("flat")

                        def confirm_add():

                            try:

                                post(
                                    f"/hardware/{asset.get('id')}/checkout",
                                    {
                                        "checkout_to_type": "asset",
                                        "assigned_asset": ECAMI_ASSET_ID,
                                    }
                                )

                                dialog.close()

                                show_success(
                                    "Target Module added to ECAMi."
                                )

                                refreshed = get(
                                    f"/hardware/{asset.get('id')}"
                                )

                                display_tm(refreshed)

                            except Exception as error:

                                show_error(
                                    f"Could not add Target Module: {error}"
                                )

                        ui.button(
                            "Add to ECAMi",
                            on_click=confirm_add
                        )

            dialog.open()

        def remove_current_tm():

            asset = current_tm.get("value")

            if not asset:
                return

            with ui.dialog() as dialog:

                with ui.card():

                    ui.label(
                        "Remove Target Module"
                    ).classes("text-h6")

                    ui.label(
                        f"Remove {asset_label(asset)} from ECAMi?"
                    )

                    with ui.row():

                        ui.button(
                            "Cancel",
                            on_click=dialog.close
                        ).props("flat")

                        def confirm_remove():

                            try:

                                post(
                                    f"/hardware/{asset.get('id')}/checkin"
                                )

                                dialog.close()

                                show_success(
                                    "Target Module removed from ECAMi."
                                )

                                refreshed = get(
                                    f"/hardware/{asset.get('id')}"
                                )

                                display_tm(refreshed)

                            except Exception as error:

                                show_error(
                                    f"Could not remove Target Module: {error}"
                                )

                        ui.button(
                            "Remove",
                            on_click=confirm_remove
                        )

            dialog.open()

        def load_target_modules():

            tm_result.clear()

            with tm_result:

                ui.label(
                    "Loading Target Modules..."
                ).classes("text-grey-7")

            try:

                assets = get_all_assets()

                ecami_tms = []
                available_tms = []

                for asset in assets:

                    model = asset.get("model") or {}

                    if isinstance(model, dict):

                        model_name = str(
                            model.get("name") or ""
                        ).lower()

                    else:

                        model_name = str(
                            model
                        ).lower()

                    category = asset.get("category") or {}

                    if isinstance(category, dict):

                        category_name = str(
                            category.get("name") or ""
                        ).lower()

                    else:

                        category_name = str(
                            category
                        ).lower()

                    if (
                        "target module" not in model_name
                        and "target module" not in category_name
                    ):
                        continue

                    if is_ecami_asset(asset):

                        ecami_tms.append(asset)

                    else:

                        available_tms.append(asset)

                tm_result.clear()

                with tm_result:

                    with ui.row().classes(
                        "w-full items-center justify-between"
                    ):

                        ui.label(
                            f"{len(ecami_tms)} Target Modules in ECAMi"
                        ).classes("text-h6")

                        ui.button(
                            "Refresh",
                            icon="refresh",
                            on_click=load_target_modules
                        ).props("flat")

                    if ecami_tms:

                        with ui.expansion(
                            f"In ECAMi ({len(ecami_tms)})",
                            icon="memory"
                        ).classes("w-full"):

                            for asset in sorted(
                                ecami_tms,
                                key=asset_label
                            ):

                                ui.label(
                                    asset_label(asset)
                                )

                    else:

                        ui.label(
                            "No Target Modules are currently in ECAMi."
                        ).classes("text-grey-7")

                    with ui.expansion(
                        f"Available ({len(available_tms)})",
                        icon="inventory_2"
                    ).classes("w-full"):

                        for asset in sorted(
                            available_tms,
                            key=asset_label
                        ):

                            ui.label(
                                asset_label(asset)
                            )

            except Exception as error:

                tm_result.clear()

                with tm_result:

                    ui.label(
                        f"Could not load Target Modules: {error}"
                    ).classes("text-negative")

        with ui.row():

            ui.button(
                "Search",
                icon="search",
                on_click=search_tm
            )

            ui.button(
                "Refresh Lists",
                icon="refresh",
                on_click=load_target_modules
            ).props("flat")

        tm_search.on(
            "keydown.enter",
            lambda e: search_tm()
        )

        load_target_modules()


    # =====================================================
    # Components
    # =====================================================

    with ui.tab_panel(components_tab):

        ui.label(
            "Camera Components"
        ).classes("text-h4")

        ui.label(
            "View components assigned to the ECAMi camera unit."
        ).classes("text-grey-7")

        component_result = ui.column().classes(
            "w-full"
        )

        def load_components():

            component_result.clear()

            with component_result:

                ui.label(
                    "Loading components..."
                ).classes("text-grey-7")

            try:

                result = get(
                    f"/hardware/{ECAMI_ASSET_ID}"
                )

                component_result.clear()

                with component_result:

                    ui.label(
                        "ECAMi Camera Unit"
                    ).classes("text-h6")

                    components = (
                        result.get("components")
                        or []
                    )

                    if not components:

                        ui.label(
                            "No components assigned to ECAMi."
                        ).classes("text-grey-7")

                    else:

                        for component in components:

                            with ui.card().classes(
                                "w-full"
                            ):

                                ui.label(
                                    component.get("name") or "-"
                                ).classes(
                                    "text-subtitle1"
                                )

                                pivot = (
                                    component.get("pivot")
                                    or {}
                                )

                                qty = (
                                    pivot.get("assigned_qty")
                                    if isinstance(
                                        pivot,
                                        dict
                                    )
                                    else None
                                )

                                ui.label(
                                    f"Quantity: {qty or '-'}"
                                )

            except Exception as error:

                component_result.clear()

                with component_result:

                    ui.label(
                        f"Could not load components: {error}"
                    ).classes("text-negative")

        def add_component():

            try:

                components = get_all_components()

            except Exception as error:

                show_error(
                    f"Could not load components: {error}"
                )

                return

            options = {}

            for component in components:

                component_id = component.get("id")

                if component_id is None:
                    continue

                options[
                    str(component_id)
                ] = (
                    component.get("name")
                    or f"Component {component_id}"
                )

            if not options:

                show_info(
                    "No components were found."
                )

                return

            with ui.dialog() as dialog:

                with ui.card().classes("w-96"):

                    ui.label(
                        "Add Component"
                    ).classes("text-h6")

                    component_select = ui.select(
                        options,
                        label="Component"
                    ).props(
                        "outlined"
                    ).classes(
                        "w-full"
                    )

                    quantity_input = ui.number(
                        label="Quantity",
                        value=1,
                        min=1,
                        step=1
                    ).props(
                        "outlined"
                    ).classes(
                        "w-full"
                    )

                    with ui.row():

                        ui.button(
                            "Cancel",
                            on_click=dialog.close
                        ).props("flat")

                        def confirm_add_component():

                            if not component_select.value:

                                show_info(
                                    "Select a component."
                                )

                                return

                            try:

                                component_id = int(
                                    component_select.value
                                )

                                quantity = int(
                                    quantity_input.value or 1
                                )

                                post(
                                    f"/components/{component_id}/checkout",
                                    {
                                        "assigned_to": ECAMI_ASSET_ID,
                                        "assigned_qty": quantity,
                                    }
                                )

                                dialog.close()

                                show_success(
                                    "Component added to ECAMi."
                                )

                                load_components()

                            except Exception as error:

                                show_error(
                                    f"Could not add component: {error}"
                                )

                        ui.button(
                            "Add Component",
                            icon="add",
                            on_click=confirm_add_component
                        )

            dialog.open()

        def remove_component():

            try:

                camera = get(
                    f"/hardware/{ECAMI_ASSET_ID}"
                )

                components = (
                    camera.get("components")
                    or []
                )

            except Exception as error:

                show_error(
                    f"Could not load assigned components: {error}"
                )

                return

            if not components:

                show_info(
                    "No components are assigned to ECAMi."
                )

                return

            options = {}

            for component in components:

                component_id = component.get("id")

                if component_id is None:
                    continue

                options[
                    str(component_id)
                ] = (
                    component.get("name")
                    or f"Component {component_id}"
                )

            with ui.dialog() as dialog:

                with ui.card().classes("w-96"):

                    ui.label(
                        "Remove Component"
                    ).classes("text-h6")

                    component_select = ui.select(
                        options,
                        label="Component"
                    ).props(
                        "outlined"
                    ).classes(
                        "w-full"
                    )

                    quantity_input = ui.number(
                        label="Quantity",
                        value=1,
                        min=1,
                        step=1
                    ).props(
                        "outlined"
                    ).classes(
                        "w-full"
                    )

                    with ui.row():

                        ui.button(
                            "Cancel",
                            on_click=dialog.close
                        ).props("flat")

                        def confirm_remove_component():

                            if not component_select.value:

                                show_info(
                                    "Select a component."
                                )

                                return

                            try:

                                component_id = int(
                                    component_select.value
                                )

                                quantity = int(
                                    quantity_input.value or 1
                                )

                                assignments = get(
                                    f"/components/{component_id}/assets"
                                )

                                rows = []

                                if isinstance(
                                    assignments,
                                    dict
                                ):

                                    rows = (
                                        assignments.get("rows")
                                        or []
                                    )

                                else:

                                    rows = assignments or []

                                assignment = None

                                for row in rows:

                                    assigned_asset = (
                                        row.get("assigned_asset")
                                        or {}
                                    )

                                    assigned_asset_id = (
                                        assigned_asset.get("id")
                                        if isinstance(
                                            assigned_asset,
                                            dict
                                        )
                                        else assigned_asset
                                    )

                                    if (
                                        assigned_asset_id
                                        == ECAMI_ASSET_ID
                                    ):

                                        assignment = row
                                        break

                                if not assignment:

                                    raise RuntimeError(
                                        "Could not find the ECAMi component assignment."
                                    )

                                assignment_id = (
                                    assignment.get(
                                        "assigned_pivot_id"
                                    )
                                    or assignment.get("id")
                                )

                                post(
                                    f"/components/{assignment_id}/checkin",
                                    {
                                        "checkin_qty": quantity
                                    }
                                )

                                dialog.close()

                                show_success(
                                    "Component removed from ECAMi."
                                )

                                load_components()

                            except Exception as error:

                                show_error(
                                    f"Could not remove component: {error}"
                                )

                        ui.button(
                            "Remove Component",
                            icon="remove",
                            on_click=confirm_remove_component
                        )

            dialog.open()

        with ui.row():

            ui.button(
                "Refresh",
                icon="refresh",
                on_click=load_components
            )

            ui.button(
                "Add Component",
                icon="add",
                on_click=add_component
            )

            ui.button(
                "Remove Component",
                icon="remove",
                on_click=remove_component
            )

        load_components()


    # =====================================================
    # Audit
    # =====================================================

    with ui.tab_panel(audit_tab):

        ui.label(
            "Inventory Audit"
        ).classes("text-h4")

        ui.label(
            "Read-only inventory checks. No inventory data is modified."
        ).classes("text-grey-7")

        audit_result = ui.column().classes(
            "w-full"
        )

        def run_audit():

            audit_result.clear()

            with audit_result:

                ui.label(
                    "Running audit..."
                ).classes("text-grey-7")

            try:

                assets = get_all_assets()
                components = get_all_components()

                assets_missing_tag = [
                    asset
                    for asset in assets
                    if not asset.get("asset_tag")
                ]

                assets_missing_serial = [
                    asset
                    for asset in assets
                    if not asset.get("serial")
                ]

                components_missing_location = [
                    component
                    for component in components
                    if not component.get("location")
                ]

                audit_result.clear()

                with audit_result:

                    ui.label(
                        "Audit Summary"
                    ).classes("text-h6")

                    ui.label(
                        f"Total assets: {len(assets)}"
                    )

                    ui.label(
                        f"Total components: {len(components)}"
                    )

                    ui.label(
                        f"Assets missing asset tag: "
                        f"{len(assets_missing_tag)}"
                    )

                    ui.label(
                        f"Assets missing serial: "
                        f"{len(assets_missing_serial)}"
                    )

                    ui.label(
                        f"Components missing location: "
                        f"{len(components_missing_location)}"
                    )

                    ui.separator()

                    if assets_missing_tag:

                        with ui.expansion(
                            "Assets missing asset tag",
                            icon="warning"
                        ).classes("w-full"):

                            for asset in assets_missing_tag:

                                ui.label(
                                    asset_label(asset)
                                )

                    if assets_missing_serial:

                        with ui.expansion(
                            "Assets missing serial",
                            icon="warning"
                        ).classes("w-full"):

                            for asset in assets_missing_serial:

                                ui.label(
                                    asset_label(asset)
                                )

                    if components_missing_location:

                        with ui.expansion(
                            "Components missing location",
                            icon="warning"
                        ).classes("w-full"):

                            for component in components_missing_location:

                                ui.label(
                                    f"{component.get('name') or '-'} "
                                    f"| ID {component.get('id') or '-'}"
                                )

                    if (
                        not assets_missing_tag
                        and not assets_missing_serial
                        and not components_missing_location
                    ):

                        ui.label(
                            "No audit issues found."
                        ).classes("text-positive")

            except Exception as error:

                audit_result.clear()

                with audit_result:

                    ui.label(
                        f"Audit failed: {error}"
                    ).classes("text-negative")

        ui.button(
            "Run Audit",
            icon="fact_check",
            on_click=run_audit
        )

        run_audit()


# =========================================================
# Start application
# =========================================================


ui.run(
    host="0.0.0.0",
    port=int(os.getenv("PORT", "10000")),
    reload=False,
    show=False
)