#!/usr/bin/env python
# -*- coding: utf-8 -*-

estaciones = {"humanes":"estefania",
				"vallecas": "estefania",
				"arganda": "estefania",
				"tres cantos": "estefania",
				"la nucia": "javier",
				"san javier": "alberto",
				"alcala de henares": "estefania",
				"alcantarilla": "alberto",
				"elche": "javier",
				"rosales": "estefania",
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
				"bellavista": "alberto",
				"olivares": "alberto",
				"san lorenzo": "estefania",
				"villalba": "estefania",
				"hellin": "javier",
				"almeria 1": "alberto",
				"tomelloso": "javier",
				"huercal": "alberto",
				"la solana": "javier",
				"patraix": "javier",
				"javea": "javier",
				"vicar":"alberto",
				"elche ii":"javier",
				"guadarrama":"estefania",
				"villarrobledo":"javier",
				"pirotecnia":"estefania"}
				
llamadas = {"expendedor", "cliente", "CRA", "coordinador"}

incidencias = {"bloqueo surtidor", "atasco billetero", "impresion ticket/factura",
				"parada de emergencia", "repostaje incompleto", "revelado cheque",
				"hoja de reclamaciones", "predeterminado grupo", "pruebas cronometradas",
				"pruebas domotica", "fallo de comunicaciones", "problemas tecnicos",
				"billete no leido. Incidencia localizada en el log", "billete no leido. Incidencia NO localizada",
				"cheque caducado",
               "otra incidencia"}
               
resoluciones = {"apertura manual","toma de datos",
				"cheque revelado","impreso desde cra","responsable/expendedor informado",
				"pasado aviso a servicio tecnico", "estacion rearmada",
				"otra resolucion"}

bools = {"si","no"}

correos= {"estefania":"diamond.pruebas.plenoil@gmail.com",
		"alberto":"diamond.pruebas.plenoil@gmail.com",
		"javier":"diamond.pruebas.plenoil@gmail.com"}
		
correoSALA = "diamond.pruebas.plenoil@gmail.com"

		
excelSHEETS = {"estefania": 0,
			"javier": 2,
			"alberto": 1}
			
excelNAME = "Incidencias Plenoil.xlsx"
		
senderCONFIG = {"server": "mailserver01.aspl.es",
				"port": 25,
				"user": "cra@diamondseguridad.com",
				"pass": "912453"}

'''senderCONFIG = {"server": "smtp.gmail.com",
				"port": 465,
				"user": "diamond.pruebas.plenoil@gmail.com",
				"pass": "cra12345"}'''
