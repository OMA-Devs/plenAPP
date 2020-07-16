Antes de utilizar el programa, hay que instalar varios modulos diferentes.

pip install Pillow
pip install openpyxl

Tras esto, se debe instalar Java SDK. Despues:

pip install tika

Después, simplemente utilizar plenAPP.py

Es necesario un archivo configuraciones.py. Se provee de un configDEBUG
de prueba que apunta a los lugares y archivos necesarios. Este archivo
no está presente en el repositorio ya que incluye los datos del servidor
corporativo para enviar los correos electrónicos.

Se configuró previamente una cuenta de GMAIL para su uso en debug, pero
requiere modificaciones en el proceso de envío de correos y ha sido eliminada.
