# plenAPP
Este programa surge de la necesidad de integrar los protocolos de actuación y necesidades de comunicación del cliente Plenoil y la Central Receptora de Alarmas Diamond Seguridad. Es un programa que integra en el programa [softGuard](https://softguard.com/) ya funcional en la CRA las necesidades específicas de este cliente.

## Funcionamiento
1. El programa extrae la lista de clientes de la plataforma SoftGuard, así como los responsables correspondientes y sus datos de contacto.
2. Lee los informes generados manualmente en PDF por los operadores.
3. Identifica la instalación y responsable a la que pertenece el informe.
4. Genera las entradas necesarias en un Excel de control solicitado por el cliente.
5. Envía los correos electrónicos correspondientes de la manera adecuada.

Todo este proceso ha ayudado a la CRA a reducir los tiempos de trámites y la tasa de error humano rápidamente. La aplicación sigue actualizandose en este momento, ajustándose a las necesidades del cliente.

# INSTALACION
## Solo WINDOWS
1. Instalar python3.7 o superior.
	1. Es IMPORTANTE marcar la opcion "añadir PATH" en la instalación al principio. Esta opcion se muestra en la parte inferior de la pantalla de instalación.
2. Instalar [Java SDK](https://www.oracle.com/java/technologies/javase-downloads.html)
3. Instalar [odbc Driver](https://www.microsoft.com/en-us/download/details.aspx?id=56567)

## Solo LINUX (debian Based)
1. Instalar java SDK.
	2. sudo apt-get install default-jdk

## Pasos de instalación genéricos
1. pip3 install Pillow
2. pip3 install openpyxl
3. pip3 install tika
	1. Tika no va a funcionar si el SDK de Java no está instalado. Mucho cuidado.
4. pip3 install pyodbc

# Usuarios de Diamond
La ruta del ejecutable de python es:
> C:\Users\DIAMOND\AppData\Local\Programs\Python\Python37\python.exe

# USO
1. Ejecutar plenAPP.py o plenAPP.pyw
	1. plenAPP.py: Ejecuta el programa con una consola de Debug.
	2. plenAPP.pyw: Ejecuta exactamente el mismo programa pero SOLO la interfaz gráfica.
2. Pulsar botón SI o NO respondiendo a la pregunta en pantalla.
3. Adjuntar archivo PDF generado por softguard
4. Rellenar el formulario de opciones.
5. Pulsar enviar.

## Errores conocidos
1. La aplicación no permite escribir en el excel correspondiente si este está abierto.
2. Algunas veces, la conexión con el servidor TIKA no se establece correctamente y la aplicación se cuelga.
3. Los errores de dicción o escritura en la base de datos de SoftGuard pueden llevar a problemas inesperados con la aplicación. 