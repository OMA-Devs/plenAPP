Lo primero es instalar python3.7. Es IMPORTANTE marcar la opcion "añadir PATH" en la instalación al principio.
Esta opcion se muestra en la parte inferior de la pantalla de instalación.

Antes de utilizar el programa, hay que instalar varios modulos diferentes.
Estos modulos se instalarán desde la carpeta "dependencias" con el programa pip-win1.9.exe

IMPORTANTE marcar la ruta correcta en pip-win1.9. la ruta es
C:\Users\DIAMOND\AppData\Local\Programs\Python\Python37\python.exe

pip install Pillow
pip install openpyxl

Tras esto, se debe instalar Java SDK, localizado en la carpeta "dependencias" también. Despues, utilizando pip-win1.9:

pip install tika

Después, simplemente utilizar plenAPP.py

Es necesario un archivo configuraciones.py. Se provee de un configDEBUG
de prueba que apunta a los lugares y archivos necesarios. Este archivo
no está presente en el repositorio ya que incluye los datos del servidor
corporativo para enviar los correos electrónicos.

Se configuró previamente una cuenta de GMAIL para su uso en debug, pero
requiere modificaciones en el proceso de envío de correos y ha sido eliminada.

La aplicacion plenAPP saca una consola de debug que informa de procesos y errores durante este.
La aplicacion plenAPPw no muestra esa consola de debug
El módulo plenFLUX lee los excel de incidencias y las contabiliza en otro excel diferente llamado "Flujo de clientes". Esta funcionalidad sirve, en su forma más básica, para conocer los puntos de mayor incidencia de clientes. En versiones futuras será mejorada para ofrecer más información. 