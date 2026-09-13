from openpyxl import load_workbook

workbook = load_workbook("sample/template.xlsx")

sheet = workbook.active

value = sheet["A1"].value

print(value)