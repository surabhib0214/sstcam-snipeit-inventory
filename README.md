# SSTCam Snipe-IT Inventory

Python-based automation tools for managing the SSTCam inventory through the Snipe-IT REST API.

The project provides command-line tools for asset management, component management, barcode scanning, Target Module management, ECAMi inventory, and inventory auditing.

## Features

* Asset lookup and management
* Asset check-in and check-out
* Barcode scanner workflow
* Report inventory issues in Snipe-IT asset Notes
* Component management
* Add and remove components from the Camera Unit
* Target Module management
* Add and remove Target Modules from ECAMi
* ECAMi inventory overview
* Inventory auditing
* Asset and component field comparison
* Experimental/development scripts kept separately in `old_tests`

## Project Structure

### Main Scripts

| Script                         | Description                                                                |
| ------------------------------ | -------------------------------------------------------------------------- |
| `scanner_workflow.py`          | Main barcode-based workflow for assets and components                      |
| `report_issue.py`              | Find an asset by barcode/asset tag/serial and report an issue in its Notes |
| `checkin_asset.py`             | Check an asset into inventory                                              |
| `checkout_asset.py`            | Check an asset out to another destination                                  |
| `camera_components.py`         | Add, view, and remove components assigned to the Camera Unit               |
| `tm_scanner.py`                | Scan and manage Target Modules                                             |
| `ecami_tms.py`                 | List Target Modules in ECAMi and Target Modules ready to deploy            |
| `ecami_tm_manager.py`          | Interactive Target Module management                                       |
| `snipe_it_add_tm_to_ecami.py`  | Add a Target Module to ECAMi from the command line                         |
| `snipe_it_rm_tm_from_ecami.py` | Remove a Target Module from ECAMi from the command line                    |
| `ecami_inventory.py`           | Display assets currently assigned to ECAMi, grouped by category            |
| `inventory_audit.py`           | Read-only audit of inventory data                                          |
| `compare_fields.py`            | Compare fields available for assets and components                         |
| `inventory_api.py`             | Shared Snipe-IT REST API helper functions                                  |

### `old_tests`

The `old_tests` directory contains scripts created during development and API testing.

These scripts are retained for reference and troubleshooting but are not part of the main workflow.

Examples include:

* `asset_details.py`
* `asset_notes.py`
* `assigned_assets.py`
* `barcode_test.py`
* `barcode_test_v2.py`
* `clean_test_notes.py`
* `component_api_test.py`
* `component_assignments.py`
* `component_checkin_test.py`
* `component_checkout_test.py`
* `find_asset.py`
* `get_asset.py`
* `list_assets.py`
* `list_locations.py`
* `pagination_test.py`
* `update_notes.py`

## Configuration

The project uses a local `config.py` file for the Snipe-IT API configuration.

Example:

```python
API_KEY = "YOUR_SNIPE_IT_API_TOKEN"
BASE_URL = "https://sstcam-inventory.ecap.work/api/v1"
ECAMI_ASSET_ID = 126
```

`config.py` is excluded from Git using `.gitignore`.

**Never commit API tokens or other credentials to the repository.**

## Requirements

* Python 3
* `requests`
* Access to the SSTCam Snipe-IT instance
* A valid Snipe-IT API token
* Optional: USB or Bluetooth barcode scanner

Install the Python dependency with:

```text
py -m pip install requests
```

## Running the Main Tools

From the project directory:

```text
py scanner_workflow.py
```

```text
py report_issue.py
```

```text
py camera_components.py
```

```text
py tm_scanner.py
```

```text
py ecami_tms.py
```

```text
py ecami_inventory.py
```

## Target Module Management

### Add a Target Module to ECAMi

```text
py snipe_it_add_tm_to_ecami.py <TM_ID>
```

Example:

```text
py snipe_it_add_tm_to_ecami.py 117
```

The script verifies that the selected asset is a Target Module and checks whether it is already assigned before checking it out to ECAMi.

### Remove a Target Module from ECAMi

```text
py snipe_it_rm_tm_from_ecami.py <TM_ID>
```

Example:

```text
py snipe_it_rm_tm_from_ecami.py 117
```

The script verifies that the selected asset is a Target Module and is currently assigned to ECAMi before checking it in.

## Barcode Scanner

The scanner workflow is designed to work with USB or Bluetooth barcode scanners that operate as keyboard/HID devices.

The scanner enters the barcode or asset tag into the Python program, normally followed by Enter.

QR codes can also contain direct Snipe-IT URLs for assets or components.

## Components

The project supports managing components assigned to the Camera Unit.

The component workflow can:

1. List components assigned to the Camera Unit.
2. Add a component to the Camera Unit.
3. Specify the quantity being assigned.
4. Remove a component from the Camera Unit.
5. Return the selected quantity to inventory.

## Report Issue

`report_issue.py` provides a simple way to report an inventory problem.

The workflow:

1. Scan or enter an asset tag/serial.
2. Find the corresponding Snipe-IT asset.
3. Enter the problem description.
4. Add the issue to the asset's Notes field.

Example:

```text
Issue: Camera housing damaged
```

## ECAMi Inventory

`ecami_inventory.py` provides an overview of assets currently assigned to the ECAMi Camera Unit.

The inventory is grouped by category to make the contents of ECAMi easier to inspect.

## Inventory Audit

`inventory_audit.py` performs a read-only audit of the inventory.

It checks for missing important fields such as:

* Asset tags
* Serial numbers
* Models
* Categories
* Status
* Component locations

The audit does **not** automatically modify inventory data.

## Field Comparison

`compare_fields.py` compares the fields returned by the Snipe-IT API for assets and components.

This helps identify differences between the two object types and supports future improvements to the inventory workflow.

## Security

API credentials are stored locally and excluded from Git using `.gitignore`.

Never commit:

* API tokens
* Passwords
* Authentication credentials
* Other sensitive configuration

If an API token is compromised, revoke it in Snipe-IT and create a new token.

## Git Repository

This project is maintained in a private GitHub repository.

The repository can later be shared with other members of the SSTCam group by adding them as GitHub collaborators.

## Future GUI

A NiceGUI interface is planned as the next major development stage.

The planned interface will provide a graphical frontend for the existing Python/Snipe-IT backend.

Planned functionality includes:

* Barcode scanning
* Asset check-in/check-out
* Component management
* Report Issue
* ECAMi inventory overview
* Target Module management
* Add/remove Target Modules from ECAMi
* Lists and dropdowns for inventory selection

The existing command-line tools will remain useful as backend functionality and for testing.
