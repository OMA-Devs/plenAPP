#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

estaciones = {"humanes":"estefania",
				"vallecas madrid i": "estefania",
				"arganda": "estefania",
				"tres cantos": "estefania",
				"la nucia": "javier",
				"san javier": "alberto",
				"alcala de henares": "estefania",
				"alcantarilla": "alberto",
				"elche i": "javier",
				"rosales madrid ii": "estefania",
				"vera": "alberto",
				"san juan": "javier",
				"san vicente": "javier",
				"fuenlabrada ii": "estefania",
				"santa pola": "javier",
				"aspe": "javier",
				"cuevas de almanzora": "alberto",
				"coslada": "estefania",
				"meco": "estefania",
				"nijar": "alberto",
				"fuenlabrada iii": "estefania",
				"collado villalba": "estefania",
				"bellavista sevilla i": "alberto",
				"olivares": "alberto",
				"san lorenzo": "estefania",
				"villalba": "estefania",
				"hellin": "javier",
				"almeria i": "alberto",
				"tomelloso": "javier",
				"huercal": "alberto",
				"la solana": "javier",
				"patraix valencia i": "javier",
				"javea": "javier",
				"vicar":"alberto",
				"elche ii":"javier",
				"guadarrama":"estefania",
				"villarrobledo":"javier",
				"pirotecnia madrid iii":"estefania",
				"albacete":"javier",
				"guadalajara":"estefania"}
				
llamadas = ["expendedor", "cliente", "CRA", "coordinador"]

incidencias = ["cheque", "mantenimiento",
			"cobro duplicado", "fallo comunicacion",
			"billetero", "fallo iluminacion", "accidente/emergencia",
			"varios"]

incidenciasOLD = ["bloqueo surtidor", "atasco billetero", "impresion ticket/factura",
				"parada de emergencia", "revelado cheque",
				"hoja de reclamaciones", "predeterminado grupo",
				"pruebas domotica", "fallo de comunicaciones", "problemas tecnicos",
				"billete no leido. Incidencia NO localizada",
				"cheque caducado", "otras"]
               
resoluciones = ["apertura manual","toma de datos",
				"cheque revelado","impreso desde cra","responsable/expendedor informado",
				"pasado aviso a servicio tecnico", "estacion rearmada", "cajon abierto", "se realizan pruebas domoticas",
				"NO se realiza apertura","otras"]

bools = ["si","no"]

correos= {"estefania":"estefania.ruiz@plenoil.es",
		"alberto":"alberto.sanchez@plenoil.es",
		"javier":"javier.garcia@plenoil.es"}


copyFECHA = datetime(2020,8,12) ##Fecha para limpiar
copyTOestefania=["bellavista sevilla i","olivares"]
copyTOalberto=[""]
copyTOjavier=["alcantarilla", "san javier", "huercal", "vera", "cuevas de almanzora", "nijar", "almeria i", "vicar"]
		
correoMARCOS = "marcos.rus@diamondseguridad.com"
correoSALA = "cra@diamondseguridad.com"

		
excelSHEETS = {"estefania": 0,
			"javier": 2,
			"alberto": 1}
			

excelNAME = "\\\\192.168.102.5\\t. de noche\\EXCEL PLENOIL\\INCIDENCIAS PLENOIL.xlsx"
		
senderCONFIG = {"server": "mailserver01.aspl.es",
				"port": 25,
				"user": "cra@diamondseguridad.com",
				"pass": "912453"}

'''senderCONFIG = {"server": "smtp.gmail.com",
				"port": 465,
				"user": "diamond.pruebas.plenoil@gmail.com",
				"pass": "cra12345"}'''
