from openpyxl import load_workbook

workbook = load_workbook("sample/template.xlsx")

sheet = workbook.active

sheet["B2"].value = "何か"

workbook.save("sample/template.xlsx")

cell_value = sheet["B2"].value

print(cell_value)

