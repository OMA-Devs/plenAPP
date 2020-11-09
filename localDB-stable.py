#Logging
import logging

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
		print("Numero de cuentas OIL: "+str(abCount))
		#for ind,key in enumerate(abonados):
			#print(abonados[key])
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
				#print(a.name+"-"+a.responsable+"-"+a.correo)
				self.estaciones[a.name] = a
	def _rewriteLocal(self):
		self.cursor.execute("DELETE FROM estaciones")
		self.lite.commit()
		for ind, key in enumerate(self.estaciones):
			#print(ind, key, self.estaciones[key])
			sql = "INSERT INTO estaciones (nombre, responsable, correo) VALUES ('"+self.estaciones[key].name+"', '"+self.estaciones[key].responsable+"', '"+self.estaciones[key].correo+"')"
			#print(sql)
			self.cursor.execute(sql)
			self.lite.commit()
	def __init__(self):
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
			print("SQLITE LOCAL ACTUALIZADO, UTILIZANDO LOCAL")
		except pyodbc.InterfaceError:
			print("SQL DRIVER NO ENCONTRADO, FALLBACK TO SQLITE LOCAL")
			self._setEstaciones("lite")
		except pyodbc.OperationalError:
			print("SQL SERVER INALCANZABLE, FALLBACK TO SQLITE LOCAL")
			self._setEstaciones("lite")


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
								#print(self.responsable)
								#print(self.correo)
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
				#print(fullname)
				halfName = fullname.split(" - ")[1]
				self.name = halfName.split(" (")[0]
		#print(self.name)
	def __init__(self, data):
		print("CREANDO ESTACION")
		print("> NOMBRE: "+str(data[0]))
		print("> RESP: "+str(data[1]))
		print("> CORREO: "+str(data[2]))
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
