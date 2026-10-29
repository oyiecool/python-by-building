from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill

wb = Workbook()
ws = wb.active
ws.title = "Budget"
ws.append(["Item", "Planned", "Actual", "Difference"])
for item, planned, actual in [("Rent", 12000, 12000), ("Food", 5500, 6120), ("Transport", 1500, 980)]:
    ws.append([item, planned, actual])
    r = ws.max_row
    ws[f"D{r}"] = f"=B{r}-C{r}"                 # a live Excel formula
ws["A5"], ws["B5"], ws["C5"], ws["D5"] = "Total", "=SUM(B2:B4)", "=SUM(C2:C4)", "=SUM(D2:D4)"
for cell in ws[1]:
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor="1F4E78")
ws.column_dimensions["A"].width = 14
wb.save("budget.xlsx")

# reading: data_only=True returns the values Excel last calculated instead of the formulas
ws = load_workbook("budget.xlsx", data_only=True)["Budget"]
for row in ws.iter_rows(min_row=2, values_only=True):
    print(row)
