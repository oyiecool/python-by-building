employees = [
    {"name": "Ana", "dept": "IT", "salary": 52000},
    {"name": "Ben", "dept": "HR", "salary": 41000},
    {"name": "Cara", "dept": "IT", "salary": 61000},
]
it_staff = [e["name"] for e in employees if e["dept"] == "IT"]
top = max(employees, key=lambda e: e["salary"])
print(it_staff, top["name"])
