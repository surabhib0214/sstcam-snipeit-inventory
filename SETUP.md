# SSTCam Snipe-IT Inventory — Setup Guide

This guide explains how to install and use the SSTCam Snipe-IT inventory automation tools on a new Windows computer.

The project communicates with the SSTCam Snipe-IT installation through its REST API.

---

## 1. Requirements

Before starting, you need:

* Windows computer
* Internet/network access to the SSTCam Snipe-IT server
* Python 3
* A Snipe-IT user account
* A Snipe-IT API token with the permissions required for the operations you want to perform
* Optional: USB or Bluetooth barcode scanner

---

## 2. Install Python

Install Python 3 on the computer.

After installation, open Command Prompt and check:

```bat
py --version
```

The command should return the installed Python version.

The project uses the `py` command on Windows.

---

## 3. Download the Project

Clone the private GitHub repository:

```bat
git clone https://github.com/surabhib0214/sstcam-snipeit-inventory.git
```

Enter the project directory:

```bat
cd sstcam-snipeit-inventory
```

If Git is not installed, install Git for Windows first.

---

## 4. Install the Python Dependency

Install the required Python package:

```bat
py -m pip install -r requirements.txt
```

The project currently uses the `requests` package to communicate with the Snipe-IT API.

---

## 5. Create the Local Configuration

The repository does not contain `config.py`.

This is intentional because `config.py` contains the Snipe-IT API token.

The repository contains:

```text
config.example.py
```

Copy it to:

```text
config.py
```

From Command Prompt:

```bat
copy config.example.py config.py
```

Open the new configuration file:

```bat
notepad config.py
```

It will look like:

```python
API_KEY = "YOUR_SNIPE_IT_API_TOKEN_HERE"
BASE_URL = "https://sstcam-inventory.ecap.work/api/v1"
ECAMI_ASSET_ID = 126
```

Replace:

```text
YOUR_SNIPE_IT_API_TOKEN_HERE
```

with your own Snipe-IT API token.

Do not share the token publicly.

Do not commit `config.py` to Git.

---

## 6. Verify the Configuration

Make sure the following values are correct:

### API key

Your own Snipe-IT API token.

### API URL

```text
https://sstcam-inventory.ecap.work/api/v1
```

### ECAMi asset ID

```text
126
```

This is the Snipe-IT asset ID used by the project for the ECAMi Camera Unit.

If the ECAMi asset changes in the future, update this value in the local `config.py`.

---

## 7. Test the Installation

Run:

```bat
py ecami_inventory.py
```

If the configuration is correct, the program should connect to Snipe-IT and display the inventory assigned to ECAMi.

You can also test:

```bat
py ecami_tms.py
```

and:

```bat
py inventory_audit.py
```

These are useful read-only tests because they do not intentionally modify inventory.

---

# 8. Using the Barcode Scanner

A USB or Bluetooth barcode scanner that operates as a keyboard/HID device can normally be used directly with the command-line tools.

No special Python scanner library is required for this type of scanner.

The workflow is:

```text
Scan barcode
     ↓
Scanner types barcode into the program
     ↓
Scanner sends Enter
     ↓
Python receives the barcode
     ↓
Snipe-IT asset is found
```

For example, an asset with:

```text
Asset ID: 217
Asset tag: 11100144
Serial: SiPM0019
```

should normally be scanned using:

```text
11100144
```

The Snipe-IT database ID (`217`) is not normally what the physical barcode scanner reads.

---

# 9. Main Programs

## Asset and Component Scanner

Run:

```bat
py scanner_workflow.py
```

This provides the main command-line workflow for assets and components.

---

## Report an Issue

Run:

```bat
py report_issue.py
```

The workflow allows an asset to be identified and an issue to be added to its Snipe-IT Notes.

Example issue:

```text
Issue: Camera housing damaged
```

Use this carefully because it modifies the asset's Notes.

---

## Camera Components

Run:

```bat
py camera_components.py
```

This allows components to be viewed, added to, and removed from the Camera Unit.

---

## Target Module Scanner

Run:

```bat
py tm_scanner.py
```

This can be used to identify and manage Target Modules.

A Target Module can be identified using its asset tag, for example:

```text
11100044
```

---

## ECAMi Target Modules

To list Target Modules:

```bat
py ecami_tms.py
```

This provides information about Target Modules currently assigned to ECAMi and Target Modules that are ready to deploy.

---

## ECAMi Inventory

Run:

```bat
py ecami_inventory.py
```

This displays assets currently assigned to ECAMi, grouped by category.

---

# 10. Target Module Command-Line Tools

Two command-line tools are available for Target Module management.

## Add a Target Module to ECAMi

```bat
py snipe_it_add_tm_to_ecami.py <TM_ID>
```

Example:

```bat
py snipe_it_add_tm_to_ecami.py 117
```

The script checks that the selected asset is a Target Module before attempting to assign it to ECAMi.

---

## Remove a Target Module from ECAMi

```bat
py snipe_it_rm_tm_from_ecami.py <TM_ID>
```

Example:

```bat
py snipe_it_rm_tm_from_ecami.py 117
```

The script checks that the selected asset is a Target Module and is currently assigned to ECAMi before checking it in.

---

# 11. Inventory Audit

Run:

```bat
py inventory_audit.py
```

This is a read-only inventory audit.

It checks for missing or incomplete inventory information.

The audit can identify things such as:

* Missing asset tags
* Missing serial numbers
* Missing models
* Missing categories
* Missing statuses
* Missing component locations

The audit does not automatically modify inventory data.

---

# 12. Comparing Asset and Component Fields

Run:

```bat
py compare_fields.py
```

This compares the fields returned by Snipe-IT for assets and components.

It is useful when developing or extending the inventory automation.

---

# 13. Important Security Rules

### Never share your API token

Your API token provides access to Snipe-IT through the API.

Treat it like a password.

### Never commit `config.py`

The project includes `config.py` in `.gitignore`.

Check before pushing changes:

```bat
git status
```

`config.py` should not appear as an untracked or staged file.

### If a token is compromised

Immediately revoke the compromised token in Snipe-IT and create a new one.

Then update the local:

```text
config.py
```

with the new token.

---

# 14. `old_tests` Directory

The repository contains an `old_tests` directory.

These scripts were used during development to test individual Snipe-IT API operations and investigate the API behaviour.

They are kept for reference and troubleshooting.

They are not required for normal use of the project.

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

---

# 15. Recommended First-Time Test

After installation and configuration, perform the following read-only tests:

```bat
py ecami_inventory.py
```

```bat
py ecami_tms.py
```

```bat
py inventory_audit.py
```

Then test the scanner workflow:

```bat
py scanner_workflow.py
```

If a barcode scanner is connected, scan an asset barcode.

---

# 16. Future GUI

A NiceGUI graphical interface is planned for the project.

The GUI is intended to provide an easier interface for:

* Barcode scanning
* Asset check-in/check-out
* Component management
* Report Issue
* ECAMi inventory
* Target Module management
* Adding and removing Target Modules from ECAMi

The existing Python scripts and API functions provide the backend functionality for the future GUI.
