# Tarea1
Tarea  1 - Sistemas operativos - Evil Maid

Prueba de concepto de un Evil Maid attack en Ubuntu(ubuntu-16.04.6-desktop-i386).

#Creacion de ISO (no test)
Para la creacion del ISO se decide utilizar xorriso(sudo apt-get install xorriso) como alternativa, debido a que genisoimage no esta funcionando de manera correcta.

Para volver a generar el ISO, es necesario modificar el Makefile con la direccion absoluta donde vaya a guardar el directorio "isoroot".
xorriso -as mkisofs -o Tarea1.iso -b /isolinux/isolinux/bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table `/Cambiar/por/directorio/isoroot/`

##Tarea1.py
En caso de probar Tarea1.py es necesario tambien modificar la linea del bash para ingresar la IP y PUERTO a utilizar.

