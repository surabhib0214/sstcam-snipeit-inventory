from inventory_api import put

ASSET_ID = 134

print("=" * 60)
print("CLEAN TEST NOTES")
print("=" * 60)

print()
print("Asset ID:", ASSET_ID)
print("Asset tag: 11100061")
print()
print("The following test notes will be removed:")
print()
print("Python API test - 2026-09-23")
print("Issue: Describe the problem: Test issue from Python")
print()

confirmation = input(
    "Type REMOVE TEST NOTES to continue: "
).strip()

if confirmation != "REMOVE TEST NOTES":
    print()
    print("Nothing changed.")
    exit()

payload = {
    "notes": ""
}

result = put(
    f"/hardware/{ASSET_ID}",
    payload
)

print()
print("API response:")
print(result)

if result.get("status") == "success":
    print()
    print("✔ Test notes removed.")
else:
    print()
    print("❌ The notes may not have been removed.")