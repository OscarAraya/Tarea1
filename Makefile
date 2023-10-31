ISO_NAME := Tarea1.iso
ISO_ROOT := /usr/share/initramfs-tools/
INITRD_FILE := /home/kali/Downloads/isoroot/initramfs/init

all: $(ISO_NAME)

$(ISO_NAME):
	mkinitramfs -o $(INITRD_FILE)
	xorriso -as mkisofs -o Tarea1.iso -b isolinux/isolinux/bin -c isolinux/boot.cat -r -J -no-emul-boot -boot-load-size 4 -boot-info-table /home/kali/Downloads/isoroot/
	isohybrid @(ISO_NAME)
	
clean:
	rm -f $(ISO_NAME)
	

