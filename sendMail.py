#SQL Lib
import pyodbc

#Libreria para generar los PDF
import reportlab

#Librería SMTP para el envio de los correos.
import smtplib
import base64
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.encoders import encode_base64

#Datos de conexion SQL
server = '192.168.102.202' 
database = '_Datos' 
username = 'david' 
password = 'dgc1991' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
##

'''sendMail
Funcion generica para enviar correos.
Dado que su funcion original es para Plenoil, se mantiene a Marcos y la CRA como copias
en el envio. Eliminar de los sitios correspondientes ambos correos si se va a utilizar
para otra funcion.
STR subject: Asunto del correo.
STR body: Cuerpo del correo.
STR adjunto: PATH absoluto del archivo adjunto. Debe ser un PDF
STR to: Correo del destinatario'''
def sendMail(subject, body, adjunto, to):
    senderCONFIG = {"server": "mailserver01.aspl.es",
				"port": 25,
				"user": "cra@diamondseguridad.com",
				"pass": "912453"}
    message = MIMEMultipart()

    message['Subject'] = subject
    message['From'] = senderCONFIG["user"]
    message['Reply-to'] = senderCONFIG["user"]
    message['To'] = to+","+"marcos.rus@diamondseguridad.com"+","+"cra@diamondseguridad.com"
		
    with open(adjunto, "rb") as opened:
        openedfile = opened.read()
    attachedfile = MIMEApplication(openedfile, _subtype = "pdf", _encoder = encode_base64)
    attachedfile.add_header('content-disposition', 'attachment', filename = name)
    bodyText = MIMEText(body)
    message.attach(bodyText)
    message.attach(attachedfile)
    try:
        server = smtplib.SMTP(senderCONFIG["server"], senderCONFIG["port"])
        print("Conexion con Servidor correcta")
        #server.ehlo()
        server.login(senderCONFIG["user"], senderCONFIG["pass"])
        print("Login en servidor correcto")
        server.sendmail(message['From'], [message['To'],"cra@diamondseguridad.com"], message.as_string())
        print('Email Enviado')			
        server.close()
        print("Conexion con Servidor cerrada")
    except:
        print('Algo ha ocurrido. EMAIL NO ENVIADO')

def genPDF(startDate, endDate):
    pass