#!/usr/bin/env python
# -*- coding: utf-8 -*-

##Librerías necesarias para extraer datos del PDF
from tika import parser
import re

import os

DIR = "CRUNCHER\\"

file_data = parser.from_file("CRUNCHER\\ALL.pdf")
text = file_data['content']
textARR = text.split("\n")

def checkLOG(line):
	##10/11/20 06:39:39.263
	if len(re.findall(r'\d\d/\d\d/\d\d \d\d:\d\d:\d\d.\d\d\d',line)) > 0:
		return True
	else:
		return False

class Evento:
	def __init__(self, data):
		self.data = [data]
		self.titulo = ""
		self.observaciones = []
	def checkOBS(self, line):
		if len(line) > 0:
			if line[0] == "[":
				return True
			else:
				return False
	def _setATT(self):
		self.titulo = self.data[0]
		self.data.pop(0)
		try:
			if self.checkOBS(self.data[0]) == False:
				self.titulo = self.titulo + " "+self.data[0]
				self.data.pop(0)
		except IndexError:
			pass
	def parseOBS(self):
		OBS = ""
		for ind, line in enumerate(self.data):
			if self.checkOBS(line) == True:
				OBS = line
			else:
				OBS = OBS+line
			try:
				if self.checkOBS(self.data[ind+1]) == True:
					self.observaciones.append(OBS)
					OBS = ""
			except IndexError:
				self.observaciones.append(OBS)
				OBS = ""
		

class Informe:
	def __init__(self, data):
		self.data = [data]
		self.nombre = ""
		self.direccion = ""
		self.eventos = []
	def _setATT(self):
		self.nombre = self.data[0]
		self.direccion = self.data[1]
		self.data.pop(0)
		self.data.pop(0)
	def checkEVENTO(self, line):
		if len(re.findall(r'\d\d/\d\d/\d\d\d\d \d\d:\d\d:\d\d',line[0:19])) > 0:
			return True
		else:
			return False
	def parseEVENTS(self):
		ev = ""
		for ind, line in enumerate(self.data):
			if self.checkEVENTO(line) == True:
				ev = Evento(line)
			else:
				ev.data.append(line)
			try:
				if self.checkEVENTO(self.data[ind+1]) == True:
					self.eventos.append(ev)
					ev = ""
			except IndexError:
				self.eventos.append(ev)
				ev = ""
		self.data = []
	def structure(self):
		self._setATT()
		self.parseEVENTS()
		for item in self.eventos:
			item._setATT()
			item.parseOBS()

def HTMLwriter(informe):
	f = open(DIR+informe.nombre+".html", "w", encoding="utf-8")
	f.write('''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">

  <title></title>

  <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">

</head>

<body>''')
	f.write("<h1>"+informe.nombre+"</h1>")
	f.write("<h2>"+informe.direccion+"</h2>")
	for item in informe.eventos:
		f.write("<div class='w3-container w3-border'>")
		f.write(item.titulo)
		if len(item.observaciones) > 0:
			f.write("<div class='w3-container w3-border'>")
			for obs in item.observaciones:
				f.write(obs)
			f.write("</div>")
		f.write("</div>")
	f.write("</body></html>")
	f.close()

	
informes = []

for ind, line in enumerate(textARR):
	if line is not "":
		if line[0:3] == "OIL":
			informes.append(Informe(line))
		else:
			if len(informes) > 0:
				##Criterios para añadir o no una linea
				if line == "Fecha Cuenta Evento Usuario Zona":
					pass
				elif "Observación" in line:
					pass
				elif "andres@cra.es" in line:
					pass
				elif "Scheduler" in line:
					pass
				else:
					informes[-1].data.append(line)

for informe in informes:
	informe.structure()
	HTMLwriter(informe)

