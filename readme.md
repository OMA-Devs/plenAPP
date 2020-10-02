Lo primero es instalar python3.7. Es IMPORTANTE marcar la opcion "añadir PATH" en la instalación al principio.
Esta opcion se muestra en la parte inferior de la pantalla de instalación.

Antes de utilizar el programa, hay que instalar varios modulos diferentes.
Estos modulos se instalarán desde la carpeta "dependencias" con el programa pip-win1.9.exe

IMPORTANTE marcar la ruta correcta en pip-win1.9. la ruta es
C:\Users\DIAMOND\AppData\Local\Programs\Python\Python37\python.exe

pip3 install Pillow
pip3 install openpyxl

Tras esto, se debe instalar Java SDK, localizado en la carpeta "dependencias" también. Despues, utilizando pip-win1.9:

pip3 install tika

Después, simplemente utilizar plenAPP.py

La aplicacion plenAPP saca una consola de debug que informa de procesos y errores durante este.
La aplicacion plenAPPw no muestra esa consola de debug