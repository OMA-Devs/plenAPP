#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
	
llamadas = ["expendedor", "cliente", "CRA", "coordinador"]

incidencias = ["cheque", "mantenimiento", "surtidor equivocado",
			"cobro duplicado", "fallo comunicacion",
			"billetero", "fallo iluminacion", "accidente/emergencia",
			"varios"]

               
resoluciones = ["apertura manual","toma de datos",
				"cheque revelado","impreso desde cra","responsable/expendedor informado",
				"pasado aviso a servicio tecnico", "estacion rearmada", "cajon abierto", "se realizan pruebas domoticas",
				"NO se realiza apertura","otras"]

bools = ["si","no"]

#copyFECHA = datetime(2020,9,25) ##Fecha para limpiar
copyTOestefania=[]
copyTOalberto=[]
copyTOjavier=[]
copyTOpatricia=[]
		
correoMARCOS = "marcos.rus@diamondseguridad.com"
correoSALA = "cra@diamondseguridad.com"

		
excelSHEETS = {"estefania": 0,
			"javier": 2,
			"alberto": 1,
			"patricia": 3}
			

excelNAME = "\\\\192.168.102.5\\t. de noche\\EXCEL PLENOIL\\INCIDENCIAS PLENOIL.xlsx"
		
senderCONFIG = {"server": "mailserver01.aspl.es",
				"port": 25,
				"user": "cra@diamondseguridad.com",
				"pass": "d1am0nd%2453"}

'''senderCONFIG = {"server": "smtp.gmail.com",
				"port": 465,
				"user": "diamond.pruebas.plenoil@gmail.com",
				"pass": "cra12345"}'''
