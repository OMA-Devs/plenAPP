#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
plenAPP

Aplicación diseñada para hacer de interfaz entre las incidencias generadas
en SoftGuard para el cliente Plenoil. Automatiza tareas de escritura en 
excels de control y el envío de correo de las mencionadas incidencias a
los coordinadores correspondientes.

Esta aplicación está cedida temporalmente a DIAMOND SEGURIDAD S.L.
PROPIEDAD DE D.GOMEZ CALLES
Todos los derechos reservados.'''
#Librería de interfaz
from tkinter import Tk
from tkinter import StringVar
from tkinter import OptionMenu
#from tkinter import *
from tkinter import filedialog
from tkinter.font import Font
from tkinter import messagebox
from tkinter import ttk

#Archivos de configuracion y modulos personalizados.
from configuraciones import *
from localDBstable import DB

#Utilizado solo para mostrar los logos.
from PIL import Image, ImageTk

#Utilizado para extraer fecha y hora automaticamente para las incidencias.
from datetime import datetime

#Librería para escribir en los excel.
from openpyxl import load_workbook

#Librería SMTP para el envio de los correos.
import smtplib
import base64
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.encoders import encode_base64

##Librerías necesarias para extraer datos del PDF
from tika import parser
import re

#Logging
import logging

estaciones = DB().estaciones

class Aplicacion():
	''' Clase monolitica que encapsula la interfaz y las funciones necesarias para su
	correcto desarrollo.'''
	def __init__(self):
		''' Creación de la interfaz y todas sus variables asociadas'''
		self.raiz = Tk()
		self.raiz.geometry('') 		#La línea de geometría sin definir ningún tamaño hace que la interfaz sea autoadaptable.
		self.fontTITLE = Font(size = 30)
		self.font = Font(size = 16)
		buttStyle = ttk.Style()
		buttStyle.configure("size.TButton", font = ("Helvetica",16))
		self.raiz.configure(bg = 'white')
		self.raiz.title('Incidencias plenoil')
		self.status = None	#Esta variable sirve para determinar si se ha elegido SI o NO en llamada, para evitar que los operadores la lien.
		self.stationName = "" #Variable necesaria al automatizar la eleccion de estación.
		self.adjunto = None #Variable que almacena el archivo adjunto
		##################
		##LOGOS y TITULO##
		##################
		diamondLOGO = ImageTk.PhotoImage(Image.open("logodiamond.png").resize((120,120)))
		plenoilLOGO = ImageTk.PhotoImage(Image.open("logoplenoil.png").resize((120,120)))
		self.diamondLOGO = ttk.Label(self.raiz, image = diamondLOGO)
		self.diamondLOGO.grid(column=5, row = 0, columnspan = 2)
		self.plenoilLOGO = ttk.Label(self.raiz, image = plenoilLOGO)
		self.plenoilLOGO.grid(column=0, row = 0, columnspan = 2)
		self.titleLABEL = ttk.Label(self.raiz, text= "INCIDENCIAS PLENOIL", font = self.fontTITLE)
		self.titleLABEL.grid(column = 2, row = 0, columnspan = 3)
		##############################
		##BOTONES DE LLAMADA Y ENVIO##
		##############################
		self.callLABEL = ttk.Label(self.raiz, text= "¿HAY LLAMADA?", font = self.font)
		self.yesBUTTON = ttk.Button(self.raiz, text="SI",
									command=self.showCALL, style = "size.TButton")
		self.noBUTTON = ttk.Button(self.raiz, text="NO",
								   command=self.showNOCALL, style = "size.TButton")
		self.sendBUTTON = ttk.Button(self.raiz, text="ENVIAR",
										command=self.sendIncidencia, style = "size.TButton")
		self.adjBUTTON = ttk.Button(self.raiz, text="ADJUNTAR",
										command=self.adjuntar, style = "size.TButton")
		self.incNAME = ttk.Label(self.raiz, text="", font = self.font)
		########################
		##SECCION "LLAMADA DE"##
		########################
		self.DEllamadaLABEL = ttk.Label(self.raiz, text="LLAMADA DE", font = self.font)
		self.DEllamadaVAR = StringVar(self.raiz)
		self.DEllamadaVAR.set("cliente")
		self.DEllamadaMENU = OptionMenu(self.raiz, self.DEllamadaVAR, *llamadas)        
		self.DEllamadaMENU.config(font = self.font) 
		########################       
		##SECCCION "INCIDENCIA##
		########################
		self.incidenciaLABEL = ttk.Label(self.raiz, text="INCIDENCIA", font = self.font)
		self.incidenciaVAR = StringVar(self.raiz)
		self.incidenciaVAR.set("cheque")
		self.incidenciaMENU = OptionMenu(self.raiz, self.incidenciaVAR, *incidencias)
		self.incidenciaMENU.config(font = self.font)
		########################
		##SECCION "RESOLUCION"##
		########################
		self.resolucionLABEL = ttk.Label(self.raiz, text="RESOLUCION", font = self.font)
		self.resolucionVAR = StringVar(self.raiz)
		self.resolucionVAR.set("apertura manual")
		self.resolucionMENU = OptionMenu(self.raiz, self.resolucionVAR, *resoluciones)
		self.resolucionMENU.config(font = self.font)    
		#########################
		##SECCION "SOLUCIONADO"##
		#########################
		self.solucionLABEL = ttk.Label(self.raiz, text="SOLUCIONADO", font = self.font)
		self.solucionVAR = StringVar(self.raiz)
		self.solucionVAR.set("si")
		self.solucionMENU = OptionMenu(self.raiz, self.solucionVAR, *bools)       
		self.solucionMENU.config(font = self.font)      
		#################################
		##SECCION "TELEFONO DE GUARDIA"##
		#################################
		self.tlfLABEL = ttk.Label(self.raiz, text="TELEFONO GUARDIA", font = self.font)
		self.tlfVAR = StringVar(self.raiz)
		self.tlfVAR.set("no")
		self.tlfMENU = OptionMenu(self.raiz, self.tlfVAR, *bools) 
		self.tlfMENU.config(font = self.font)
		###########################
		##SECCION "OBSERVACIONES"##
		###########################
		self.obsLABEL = ttk.Label(self.raiz, text="OBSERVACIONES", font = self.font)
		self.obsVAR = ttk.Entry(self.raiz)
		##################################
		##SECCION "TIEMPO DE RESOLUCION"##
		##################################
		self.tiempoLABEL = ttk.Label(self.raiz, text="TIEMPO DE RESOLUCION", font = self.font)
		self.tiempoVAR = ttk.Entry(self.raiz)
		self.tiempoAPROX = ttk.Label(self.raiz, text="", font = self.font)
		####################################
		##DISPOSICION INTERFAZ BASICA FIJA##
		####################################
		self.callLABEL.grid(column = 2, row = 1, columnspan = 3)
		self.yesBUTTON.grid(column = 2, row = 2, pady = 20)
		self.noBUTTON.grid(column = 4, row = 2, pady = 20)
		self.adjBUTTON.grid(column=1, row = 11, columnspan = 3, pady = 20)
		self.sendBUTTON.grid(column=3, row = 11, columnspan = 3, pady = 20)
		self.incNAME.grid(column = 2, row = 12, columnspan = 3, pady = 20)
		##INICIO DEL BUCLE PRINCIPAL##
		#configActions.checkCopyFECHA()
		self.raiz.mainloop()
	def showCALL(self):
		'''Esta función crea la interfaz necesaria para rellenar una incidencia en excel'''
		##DISPOSICION "LLAMADA DE"
		self.DEllamadaLABEL.grid(column = 2, row = 3, columnspan = 3, pady = 20)
		self.DEllamadaMENU.grid(column = 2, row = 4, columnspan = 3)
		##DISPOSICION "INCIDENCIA"
		self.incidenciaLABEL.grid(column = 0, row = 3, columnspan = 2, pady = 20)
		self.incidenciaMENU.grid(column = 0, row = 4, columnspan = 2)
		##DISPOSICION "RESOLUCION"
		self.resolucionLABEL.grid(column = 5, row = 3, columnspan = 2, pady = 20)
		self.resolucionMENU.grid(column = 5, row = 4, columnspan = 2)
		##DISPOSICION "SOLUCION"
		self.solucionLABEL.grid(column = 0, row = 6, columnspan = 2, pady = 20)
		self.solucionMENU.grid(column = 0, row = 7, columnspan = 2)
		##DISPOSICION "TELEFONO DE GUARDIA"
		self.tlfLABEL.grid(column = 5, row = 6, columnspan = 2, pady = 20)
		self.tlfMENU.grid(column = 5, row = 7, columnspan = 2)
		##DISPOSICION "OBSERVACIONES"
		self.obsLABEL.grid(column = 2, row = 6, columnspan = 3)
		self.obsVAR.grid(column = 2, row = 7, columnspan = 3 )
		##DISPOSICION "TIEMPO DE RESOLUCION"
		self.tiempoLABEL.grid(column = 2, row = 8, columnspan = 3)
		self.tiempoVAR.grid(column = 2, row = 10, columnspan = 3)
		self.tiempoAPROX.grid(column = 2, row = 9, columnspan = 3)
		##Determinación de la variable STATUS
		self.status = True
	def showNOCALL(self):
		'''Esta función elimina todos los elementos no necesarios al no haber
		llamada. Para no confundirse con la interfaz básica de inicio, también
		muestra un mensaje de información sobre lo que el operador tiene que hacer'''
		self.DEllamadaLABEL.grid_forget()
		self.DEllamadaMENU.grid_forget()
		self.incidenciaLABEL.grid_forget()
		self.incidenciaMENU.grid_forget()
		self.resolucionLABEL.grid_forget()
		self.resolucionMENU.grid_forget()
		self.solucionLABEL.grid_forget()
		self.solucionMENU.grid_forget()
		self.tlfLABEL.grid_forget()
		self.tlfMENU.grid_forget()
		self.obsLABEL.grid_forget()
		self.obsVAR.grid_forget()
		self.tiempoLABEL.grid_forget()
		self.tiempoVAR.grid_forget()
		##IMPORTANTE, determinacion de la variable STATUS.
		self.status = False
		messagebox.showinfo("NO HAY LLAMADA","PULSA ADJUNTAR Y ENVIAR")
	def checkEstacionNAME(self):
		'''Función de control. Extrae el nombre del archivo adjunto y lo 
		compara con la lista de estaciones definida en "configuraciones.py".'''
		## Se localiza el nombre en la ruta del archivo
		indName = self.adjunto.name.split("PLENOIL ")
		realNAME = indName[-1][0:-4]
		self.stationName = realNAME
		print("Nombre extraido: "+realNAME)
		## Se comparan el nombre de la entrada y la incidencia.
		try:
			estaciones[realNAME]#Importante convertir a minusculas
			print("Estación en el listado")
			if self.stationName in copyTOestefania:
				print("Mensaje en copia a ESTEFANIA")
			elif self.stationName in copyTOalberto:
				print("Mensaje en copia a ALBERTO")
			elif self.stationName in copyTOjavier:
				print("Mensaje en copia a JAVIER")
			elif self.stationName in copyTOpatricia:
				print("Mensaje en copia a PATRICIA")
			else:
				print("Mensaje SIN copia")
			return True
		except KeyError:
			print("Estación no esta en el listado")
			return False
	def calculateTIME(self):
		file_data = parser.from_file(self.adjunto.name)
		text = file_data['content']
		tPrint = ""
		dPrint = ""
		datetimeArray = []
		for line in text.split("\n"):
			if line is not "":
				if tPrint == "":
					hora = re.search(r'\d\d:\d\d:\d\d',line)
					try:
						tPrint = hora.group()[:-3]
					except AttributeError:
						pass
				if dPrint == "":
					fecha = re.search(r'\d\d/\d\d/\d\d\d\d',line)
					try:
						dPrint = fecha.group()
					except AttributeError:
						pass
				if line[0] == "[":
					fecha = line[1:11].split("/")
					#print(fecha)
					hora = line[12:17].split(":")
					#print(hora)
					for i in range(len(fecha)):
						fecha[i] = int(fecha[i])
					for i in range(len(hora)):
						hora[i] = int(hora[i])
					dat = datetime(fecha[2],fecha[1],fecha[0],hora[0],hora[1])
					datetimeArray.append(dat)
		startD = dPrint.split("/")
		startT = tPrint.split(":")
		##ESTE BLOQUE AVISA LA INSERCION DE UN PDF EN EL QUE NO SE PUEDE EXTRAER LA HORA/FECHA
		##ADEMAS DEJARA EL MENSAJE EN LA INTERFAZ.
		try:
			for i in range(len(startD)):
				startD[i] = int(startD[i])
			for i in range(len(startT)):
				startT[i] = int(startT[i])
			startDATE = datetime(startD[2],startD[1],startD[0],startT[0],startT[1])
			endDATE = datetimeArray[-1]
			elapsed = endDATE-startDATE
			return "Calculado: "+str(elapsed.seconds//60)
		except ValueError or IndexError:
			messagebox.showwarning("CUIDADO", "NO SE HA PODIDO LOCALIZAR LA HORA/FECHA. VERIFICAR PDF Y EXCEL")
			return "NO HAY FECHA/HORA. COMPROBAR EXCEL/PDF"
	def printIncidencia(self):
		'''Genera la cadena de incidencia que será impresa en el excel.
		Efectua esta operación leyendo el pdf y buscando la hora de creacion
		del evento.
		También coge los valores de las variables de interfaz y luego lo 
		ordena todo en el formato requerido por el excel.'''
		##Procesado de fecha y hora
		file_data = parser.from_file(self.adjunto.name)
		text = file_data['content']
		tPrint = ""
		dPrint = ""
		for line in text.split("\n"):
			if line is not "":
				if tPrint == "":
					hora = re.search(r'\d\d:\d\d:\d\d',line)
					try:
						tPrint = hora.group()[:-3]
					except AttributeError:
						pass
				if dPrint == "":
					fecha = re.search(r'\d\d/\d\d/\d\d\d\d',line)
					try:
						dPrint = fecha.group()
					except AttributeError:
						pass
		##Procesado de posibles incidencias y resoluciones OTRO
		inci = self.incidenciaVAR.get().upper()
		reso = self.resolucionVAR.get().upper()
		##Añadido de la parte cheque
		anulado = ""
		numCHEQUE = ""
		if reso.lower() == "apertura manual" and inci.lower() == "cheque":
			anulado = "NO"
			numCHEQUE = "-"
		##Devolucion de la incidencia
		return[self.stationName.upper(),dPrint,tPrint
			,self.DEllamadaVAR.get().upper(),inci, reso,self.solucionVAR.get().upper()
			,self.tlfVAR.get().upper(),self.obsVAR.get().upper(),anulado,numCHEQUE
			,self.tiempoVAR.get()]
	def sendMail(self):
		'''Proceso para enviar el correo con la incidencia a los coordinadores
		correspondientes. Genera el correo electrónico y adjunta el archivo
		elegido.'''
		nameIND = self.adjunto.name.rfind("/")
		name = self.adjunto.name[nameIND+1: -4]
		#subject = name
		message = MIMEMultipart()

		message['Subject'] = name
		message['From'] = senderCONFIG["user"]
		message['Reply-to'] = senderCONFIG["user"]
		
		if self.stationName in copyTOestefania:
			message['To'] = estaciones[self.stationName].correo+","+correoSALA+","+"estefania.ruiz@plenoil.es"
			print("Mensaje en copia a ESTEFANIA")
		elif self.stationName in copyTOalberto:
			message['To'] = estaciones[self.stationName].correo+","+correoSALA+","+"alberto.sanchez@plenoil.es"
			print("Mensaje en copia a ESTEFANIA")
		elif self.stationName in copyTOjavier:
			message['To'] = estaciones[self.stationName].correo+","+correoSALA+","+"javier.garcia@plenoil.es"
			print("Mensaje en copia a ESTEFANIA")
		elif self.stationName in copyTOpatricia:
			message['To'] = estaciones[self.stationName].correo+","+correoSALA+","+"patricia.ferreiro@plenoil.es"
			print("Mensaje en copia a PATRICIA")
		else:
			message['To'] = estaciones[self.stationName].correo+","+correoSALA
			print("Mensaje SIN copia")

		text = MIMEText(name)
		
		with open(self.adjunto.name, "rb") as opened:
			openedfile = opened.read()
		attachedfile = MIMEApplication(openedfile, _subtype = "pdf", _encoder = encode_base64)
		attachedfile.add_header('content-disposition', 'attachment', filename = name)
		#body = name
		message.attach(text)
		message.attach(attachedfile)
		try:
			server = smtplib.SMTP(senderCONFIG["server"], senderCONFIG["port"])
			print("Conexion con Servidor correcta")
			#server.ehlo()
			server.login(senderCONFIG["user"], senderCONFIG["pass"])
			print("Login en servidor correcto")
			if self.stationName in copyTOestefania:
				server.sendmail(message['From'], [message['To'],correoSALA,"estefania.ruiz@plenoil.es"], message.as_string())
			elif self.stationName in copyTOalberto:
				server.sendmail(message['From'], [message['To'],correoSALA,"alberto.sanchez@plenoil.es"], message.as_string())
			elif self.stationName in copyTOjavier:
				server.sendmail(message['From'], [message['To'],correoSALA,"javier.garcia@plenoil.es"], message.as_string())
			elif self.stationName in copyTOpatricia:
				server.sendmail(message['From'], [message['To'],correoSALA,"patricia.ferreiro@plenoil.es"], message.as_string())
			else:
				server.sendmail(message['From'], [message['To'],correoSALA], message.as_string())
			print('Email Enviado')			
			server.close()
			print("Conexion con Servidor cerrada")
		except:
			print('Algo ha ocurrido. EMAIL NO ENVIADO')
			messagebox.showerror("ERROR","NO SE HA ENVIADO EL EMAIL")
	def adjuntar(self):
		'''Proceso básico que une todas las funciones anteriores. Hace todas
		las comprobaciones necesarias para asegurar que la incidencia se
		escribe donde corresponde y se envia a quien corresponde.'''
		self.adjunto = filedialog.askopenfile(initialdir="\\\\192.168.102.5\\t. de noche\\PLENOIL INCIDENCIA", parent=self.raiz,mode='rb',title='Examinar...')
		self.incNAME["text"] = self.adjunto.name.split("/")[-1]
		self.tiempoAPROX["text"] = self.calculateTIME()
		self.checkEstacionNAME()
	def sendIncidencia(self):
		if self.adjunto == None:
			messagebox.showerror("ERROR","NO HAY INCIDENCIA ADJUNTA")
		else:
			#print(adjunto.name)
			if self.status == True:
				if self.checkEstacionNAME() == True:
					print(self.printIncidencia())
					print("Incidencia Coincide con Estaciones")
					row = self.printIncidencia()
					coord = estaciones[self.stationName].responsable.lower()
					worksheet = excelSHEETS[coord]
					try:
						wb = load_workbook(excelNAME)
						ws = wb.worksheets[worksheet]
						ws.append(row)
						wb.save(excelNAME)
						self.sendMail()
						if self.stationName in copyTOestefania:
							messagebox.showinfo("INCIDENCIA CORRECTA","AÑADIDO AL REGISTRO. ENVIADO A "
												+estaciones[self.stationName].correo+ ",estefania.ruiz@plenoil.es, "+correoMARCOS+" Y "+correoSALA)
						elif self.stationName in copyTOalberto:
							messagebox.showinfo("INCIDENCIA CORRECTA","AÑADIDO AL REGISTRO. ENVIADO A "
												+estaciones[self.stationName].correo+ ",alberto.sanchez@plenoil.es, "+correoMARCOS+" Y "+correoSALA)
						elif self.stationName in copyTOjavier:
							messagebox.showinfo("INCIDENCIA CORRECTA","AÑADIDO AL REGISTRO. ENVIADO A "
												+estaciones[self.stationName].correo+ ",javier.garcia@plenoil.es, "+correoMARCOS+" Y "+correoSALA)
						elif self.stationName in copyTOpatricia:
							messagebox.showinfo("INCIDENCIA CORRECTA","AÑADIDO AL REGISTRO. ENVIADO A "
												+estaciones[self.stationName].correo+ ",patricia.ferreiro@plenoil.es, "+correoMARCOS+" Y "+correoSALA)
						else:
							messagebox.showinfo("INCIDENCIA CORRECTA","AÑADIDO AL REGISTRO. ENVIADO A "
												+estaciones[self.stationName].correo+", "+correoMARCOS+" Y "+correoSALA)
					except PermissionError:
						messagebox.showerror("ERROR","EXCEL ABIERTO. CIERRA EXCEL Y REINICIA LA APLICACION")
				else:
					messagebox.showerror("ERROR","NOMBRE DE LA ESTACION NO ESTA EN LISTA")
			elif self.status == False:
				if self.checkEstacionNAME() == True:
					self.sendMail()
					coord = estaciones[self.stationName].responsable.lower()
					if self.stationName in copyTOestefania:
						messagebox.showinfo("INCIDENCIA CORRECTA","AÑADIDO AL REGISTRO. ENVIADO A "
											+estaciones[self.stationName].correo+ ",estefania.ruiz@plenoil.es, "+correoMARCOS+" Y "+correoSALA)
					elif self.stationName in copyTOalberto:
						messagebox.showinfo("INCIDENCIA CORRECTA","AÑADIDO AL REGISTRO. ENVIADO A "
											+estaciones[self.stationName].correo+ ",alberto.sanchez@plenoil.es, "+correoMARCOS+" Y "+correoSALA)
					elif self.stationName in copyTOjavier:
						messagebox.showinfo("INCIDENCIA CORRECTA","AÑADIDO AL REGISTRO. ENVIADO A "
											+estaciones[self.stationName].correo+ ",javier.garcia@plenoil.es, "+correoMARCOS+" Y "+correoSALA)
					elif self.stationName in copyTOpatricia:
						messagebox.showinfo("INCIDENCIA CORRECTA","AÑADIDO AL REGISTRO. ENVIADO A "
											+estaciones[self.stationName].correo+ ",patricia.ferreiro@plenoil.es, "+correoMARCOS+" Y "+correoSALA)
					else:
						messagebox.showinfo("INCIDENCIA CORRECTA","AÑADIDO AL REGISTRO. ENVIADO A "
											+estaciones[self.stationName].correo+", "+correoMARCOS+" Y "+correoSALA)
				else:
					messagebox.showerror("ERROR","NOMBRE DE LA ESTACION NO ESTA EN LISTA")
		


def main():
	Aplicacion()
	return 0


if __name__ == '__main__':
	main()
