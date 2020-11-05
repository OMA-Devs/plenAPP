Lo primero es instalar python3.7. Es IMPORTANTE marcar la opcion "añadir PATH" en la instalación al principio.
Esta opcion se muestra en la parte inferior de la pantalla de instalación.

Antes de utilizar el programa, hay que instalar varios modulos diferentes.
Estos modulos se instalarán desde la carpeta "dependencias"

pip3 install Pillow
pip3 install openpyxl
pip3 install pyodbc

Instalar controlador SQL desde:

https://docs.microsoft.com/es-es/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15#download-for-windows

Tras esto, se debe instalar Java SDK, localizado en la carpeta "dependencias" también:

pip3 install tika

Después, simplemente utilizar plenAPP.py

Es necesario un archivo configuraciones.py.

Se configuró previamente una cuenta de GMAIL para su uso en debug, pero
requiere modificaciones en el proceso de envío de correos y ha sido eliminada.

La aplicacion plenAPP saca una consola de debug que informa de procesos y errores durante este.
La aplicacion plenAPPw no muestra esa consola de debug