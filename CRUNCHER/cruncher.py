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

class Evento:
	def __init__(self, data):
		self.data = [data]
		self.titulo = ""
		self.observaciones = []
	def checkLOG(self, line):
		##10/11/20 06:39:39.263
		if len(re.findall(r'\d\d/\d\d/\d\d \d\d:\d\d:\d\d.\d\d\d',line)) > 0:
			return True
		else:
			return False
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
	def parseLOG(self): ####EN CONSTRUCCION
		LOG = []
		for ind, obs in enumerate(self.observaciones):
			if self.checkLOG(obs) == True:
				LOG.append(obs)

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
			item.parseLOG()

def colorFormatter(name):
	base  = "<h3 class= 'w3-leftbar w3-border-bottom"
	fmt = ""
	if "RONDA VIRTUAL DE VIDEO" in name or "Test" in name:
		fmt = " w3-border-light-grey"
	elif "EVENTO INTERFONO" in name or "GENERADO" in name:
		fmt = " w3-border-purple"
	elif "401R" in name or "456E" in name: ##ARMADO #cdb796
		fmt = " w3-border-brown"
	elif "401E" in name or "406E" in name: ##DESARMADO  #338cf9
		fmt = " w3-border-indigo"
	elif "130E" in name or "150E" in name: ##Alarma robo #ff80c0
		fmt = " w3-border-pink"
	elif "130R" in name or "150R" in name or "552R" in name: ##Restauraciones #33cccc
		fmt = " w3-border-teal"
	elif "570E" in name: #ANULADO #c0c0c0
		fmt = " w3-border-grey"
	elif "Apertura" in name: #apertura fuera çde horario. #338CF9
		fmt = " w3-border-indigo"
	elif "552E" in name: ##Fallo de comunicacion #00ff80
		fmt = " w3-border-light-green"
	elif "BIDIRECCIONAL" in name: #Perdida de alimentacion. Bidireccional, Fallo de bateria #ffff99
 		fmt = " w3-border-yellow"
	return base+fmt+"'>"

def HTMLwriter(informe):
	f = open(DIR+informe.nombre+".html", "w", encoding="utf-8")
	f.write('''<!doctype html><html lang="en">
		<head>
		<meta charset="utf-8">
		<title></title>
		<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
		</head>
		<body class='w3-content' style='width: 75%'>''')
	f.write("<h1>"+informe.nombre+"</h1>")
	f.write("<h2>"+informe.direccion+"</h2>")
	for item in informe.eventos:
		f.write("<div class='w3-container'>")
		f.write(colorFormatter(item.titulo)+item.titulo+"</h3>")
		if len(item.observaciones) > 0:
			f.write("<div class='w3-container w3-border'>")
			for obs in item.observaciones:
				f.write("<p>"+obs+"</p>")
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
				elif "@cra.es" in line:
					pass
				elif "Scheduler" in line:
					pass
				else:
					informes[-1].data.append(line)

for informe in informes:
	informe.structure()
	HTMLwriter(informe)

'''huercal = None
for informe in informes:
	if "HUERCAL" in informe.nombre:
		huercal = informe

for evento in huercal.eventos:
	print("-------")
	print(evento.titulo)'''

