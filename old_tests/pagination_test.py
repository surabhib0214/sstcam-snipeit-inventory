from inventory_api import get

data = get("/hardware")

print("Total:", data.get("total"))
print("Rows returned:", len(data.get("rows", [])))
print("Limit:", data.get("limit"))
print("Offset:", data.get("offset"))