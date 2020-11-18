#!/usr/bin/env python
# -*- coding: utf-8 -*-

##Librerías necesarias para extraer datos del PDF
from tika import parser
import re

import os

DIR = "FACTURAS\\"

file_data = parser.from_file("FACTURAS\\FACT.pdf")
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
		self.facturas = 0
		self.ticket = 0
	def _setATT(self):
		self.nombre = self.data[0]
		self.direccion = self.data[1]
		self.data.pop(0)
		self.data.pop(0)
	def checkEVENTO(self, line):
		if len(re.findall(r'\d\d/\d\d/\d\d\d\d \d\d:\d\d:\d\d',line)) > 0:
			return True
		else:
			##print(line)
			return False
	def parseEVENTS(self):
		ev = ""
		for ind, line in enumerate(self.data):
			#print(line)
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
	def lookFOR(self, word, event):
		for obs in event.observaciones:
			if word in obs:
				return True
			else:
				return False
	def structure(self):
		self._setATT()
		self.parseEVENTS()
		for item in self.eventos:
			item._setATT()
			item.parseOBS()
			item.parseLOG()
		for item in self.eventos:
			if self.lookFOR("FACTURA", item) == True:
				self.facturas = self.facturas +1
			if self.lookFOR("TICKET", item) == True:
				self.ticket = self.ticket +1

	
informes = []
facts = 0

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
	facts = facts + informe.facturas
	''''if "MONFORTE" in informe.nombre:
		for item in informe.eventos:
			print("-----------------")
			print(item.titulo)
			for ob in item.observaciones:
				print(ob)'''
	''''print(informe.nombre)
	print("--FACTURAS: "+ str(informe.facturas))
	print("--TICKETS: "+ str(informe.ticket))'''

print(facts)

