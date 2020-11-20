#Librería para escribir en los excel.
from openpyxl import load_workbook

import re

import os

print("Cargando Informe completo")
origin = load_workbook("COORDINADORES\\EV.xlsx")
print("Cargando Informe tratado")
target = load_workbook("COORDINADORES\\total.xlsx")

sheet = origin.active
ws = 0
targetSHEET = target.worksheets[ws]

a = sheet["A"]

print("Comenzando el PARSER")
for ind, cell in enumerate(a):
	if cell.value == None:
		pass
	elif type(cell.value) == str:
		if "DM1" in cell.value:
			tienda = re.search(r'T\d\d\d\d',cell.value).group()
			target.create_sheet(tienda)
			ws = ws +1 
			targetSHEET = target[tienda]
			targetSHEET.append([cell.value])
		else:
			targetSHEET.append([cell.value])
			targetSHEET.append(["FECHA Y HORA DEL EVENTO", "EVENTO"])
	else:
		targetSHEET.append([cell.value])

target.save("COORDINADORES\\total.xlsx")