---
title: debian, grub2, run level
author: "-"
date: 2012-01-29T11:41:16+00:00
url: /?p=2189
categories:
  - Linux

tags:
  - reprint
---
## debian, grub2, run level
edit /boot/grub/grub.cfg
  
```bash
  
menuentry 'Debian GNU/Linux, with Linux 2.6.32-5-686-bigmem run level 3' -class debian -class gnu-linux -class gnu -class os {
      
insmod part_msdos
      
insmod ext2
      
set root='(hd0,msdos7)'
      
search -no-floppy -fs-uuid -set ca201e81-b7d4-4cb1-9a68-707dab19738a
      
echo 'Loading Linux 2.6.32-5-686-bigmem ...'
      
linux /vmlinuz-2.6.32-5-686-bigmem root=/dev/sda8 ro quiet 3
      
echo 'Loading initial ramdisk ...'
      
initrd /initrd.img-2.6.32-5-686-bigmem
  
}

menuentry 'Debian GNU/Linux, with Linux 2.6.32-5-686-bigmem run level 5' -class debian -class gnu-linux -class gnu -class os {
      
insmod part_msdos
      
insmod ext2
      
set root='(hd0,msdos7)'
      
search -no-floppy -fs-uuid -set ca201e81-b7d4-4cb1-9a68-707dab19738a
      
echo 'Loading Linux 2.6.32-5-686-bigmem ...'
      
linux /vmlinuz-2.6.32-5-686-bigmem root=/dev/sda8 ro quiet 5
      
echo 'Loading initial ramdisk ...'
      
initrd /initrd.img-2.6.32-5-686-bigmem
  
}
  
```