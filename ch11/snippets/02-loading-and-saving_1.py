df = pd.read_csv("expenses.csv")                       # from Chapter 7
df = pd.read_csv("data.csv", sep=";", encoding="utf-8-sig", parse_dates=["date"])
df = pd.read_excel("report.xlsx", sheet_name="Q1")
df = pd.read_json("items.json")

sales.to_csv("sales_out.csv", index=False)
sales.to_excel("sales_out.xlsx", index=False, sheet_name="Sales")
