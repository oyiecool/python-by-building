import csv
from pathlib import Path
from docx import Document

def fill(template: Path, values: dict, out: Path) -> None:
    doc = Document(template)
    for para in doc.paragraphs:
        for run in para.runs:
            for key, val in values.items():
                run.text = run.text.replace("{{" + key + "}}", str(val))
    doc.save(out)

Path("letters").mkdir(exist_ok=True)
with open("customers.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):           # columns: name, amount, due
        out = Path("letters") / f"{row['name'].replace(' ', '_')}.docx"
        fill(Path("letter_template.docx"),
             {"NAME": row["name"], "AMOUNT": row["amount"], "DUE": row["due"]}, out)
