ISO_NAME := Tarea1.iso
ISO_ROOT := /usr/share/initramfs-tools/
INITRD_FILE := /home/kali/Downloads/isoroot/initramfs/init

all: $(ISO_NAME)

$(ISO_NAME):
	mkinitramfs -o $(INITRD_FILE)
	genisoimage -o $(ISO_NAME) -b /home/kali/Downloads/isoroot/isolinux/isolinux.bin -c /home/kali/Downloads/isoroot/isolinux/boot.cat -r -J -no-emul-boot -boot-load-size 4 -boot-info-table -input-charset utf-8 /home/kali/Downloads/isoroot/isolinux
	isohybrid $(ISO_NAME)
   
clean:
	rm -f $(ISO_NAME)
	

