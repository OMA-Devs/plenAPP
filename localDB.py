#Logging
import logging

#Datetime
from datetime import datetime

#SQLITE FALLBACK
import sqlite3

#SQL Lib and config
import pyodbc


class DB:
	'''Obtener el listado de estaciones del servidor
	arg curs: instancia de cursor SQL
	return abonados: diccionario compuesto de listas.
    Clave: cue_iid (convertida a STR)
    Contenido = lista con todos los datos del abonado'''
	def _getEstacionesSQL(self, curs):
		abonados = {}
		abCount = 0

		curs.execute("SELECT * FROM [m_cuentas] where cue_clinea = 'OIL'") 
		row = curs.fetchone() 
		while row:
			abonados[str(row[0])] = row 
			row = curs.fetchone()
			abCount = abCount +1
		self.log.info("_getEstacionesSQL.- Numero de cuentas OIL: "+str(abCount))
		return abonados
	def _setEstaciones(self, dbType):
		if dbType == "sql":
			for key,item in enumerate(self.SQLdata):
				ab = Estacion(self.SQLdata[item])
				self.estaciones[ab.name] = ab
		if dbType == "lite":
			self.cursor.execute("SELECT * FROM estaciones")
			abonados = self.cursor.fetchall()
			for ab in abonados:
				a = Estacion(ab)
				self.estaciones[a.name] = a
	def _rewriteLocal(self):
		self.cursor.execute("DELETE FROM estaciones")
		self.lite.commit()
		for ind, key in enumerate(self.estaciones):
			sql = "INSERT INTO estaciones (nombre, responsable, correo) VALUES ('"+self.estaciones[key].name+"', '"+self.estaciones[key].responsable+"', '"+self.estaciones[key].correo+"')"
			self.cursor.execute(sql)
			self.lite.commit()
	def __init__(self):
		'''LOGGER'''
		self.log = logging.getLogger("DB")
		self.fh = logging.FileHandler("app.log")
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		self.fh.setFormatter(formatter)
		self.log.setLevel(logging.ERROR)
		self.log.addHandler(self.fh)
		##
		self.estaciones = {}
		self.lite = sqlite3.connect("DB.db")
		self.cursor = self.lite.cursor()
		try:
			server = '192.168.102.202' 
			database = '_Datos' 
			username = 'david' 
			password = 'dgc1991' 
			cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password, timeout=1)
			cursor = cnxn.cursor()
			self.SQLdata = self._getEstacionesSQL(cursor)
			self._setEstaciones("sql")
			self._rewriteLocal()
			self.log.info("SQLITE LOCAL ACTUALIZADO, UTILIZANDO LOCAL")
		except pyodbc.InterfaceError:
			self.log.error("SQL DRIVER NO ENCONTRADO, FALLBACK TO SQLITE LOCAL")
			self._setEstaciones("lite")
		except pyodbc.OperationalError:
			self.log.error("SQL SERVER INALCANZABLE, FALLBACK TO SQLITE LOCAL")
			self._setEstaciones("lite")

class incDB:
	def __init__(self):
		'''LOGGER'''
		self.log = logging.getLogger("incDB")
		self.fh = logging.FileHandler("app.log")
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		self.fh.setFormatter(formatter)
		self.log.setLevel(logging.ERROR)
		self.log.addHandler(self.fh)
		##
		self.month = datetime.now().month
		self.lite = sqlite3.connect("INCIDENCIAS.db")
		self.cursor = self.lite.cursor()
	def insertINC(self, task):
		sql = ''' INSERT INTO "'''+str(self.month)+'''"(estacion,fecha,hora,llamadaDe,incidencia,resolucion,solucionado,telefonoGuardia,diamond,anulado,nCheque,tiempoResolucion)
			VALUES(?,?,?,?,?,?,?,?,?,?,?,?) '''
		self.cursor.execute(sql, task)
		self.lite.commit()

class Incidencia:
	pass

class Estacion:
	def setResponsableMail(self):
		if len(self.data) == 3:
			self.responsable = self.data[1]
			self.correo = self.data[2]
		else:
			for i in self.data:
				try:
					if type(i) == str:
						splitted = i.split("\n")
						for line in splitted:
							if "RESPONSABLE" in line:
								splitLine = line.split(": ")
								halfLine = splitLine[1].split(" (")
								self.responsable = halfLine[0].split(" ")[0]
								self.correo = halfLine[1].split(") ")[0].lower()
				except AttributeError:
					pass
			
	def setName(self):
		if len(self.data) == 3:
			self.name = self.data[0]
		else:
			fullname = self.data[3]
			if "9999" in fullname or "3709" in fullname or "INSTALANDO" in fullname:
				self.name = fullname
			else:
				halfName = fullname.split(" - ")[1]
				self.name = halfName.split(" (")[0]
	def __init__(self, data):
		self.data = data
		self.name = ""
		self.responsable = "NO"
		self.correo = "NO"
		self.setName()
		self.setResponsableMail()

if __name__ == "__main__":
	db = DB()
	print("---PRINTING---")
	#print(db.estaciones)
	for ind, key in enumerate(db.estaciones):
		print(db.estaciones[key].name+"-"+db.estaciones[key].responsable+"-"+db.estaciones[key].correo)
	inc = incDB()
	sqlPRUEBA = ("ELCHE","11/11/11","00:00:00","expendedor","cheque no impreso","apertura manual","si","no","OBSERVACION","-",0,5)
	inc.insertINC(sqlPRUEBA)
