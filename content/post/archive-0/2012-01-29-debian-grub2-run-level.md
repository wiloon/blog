---
title: debian, grub2, run level
author: wiloon
type: post
date: 2012-01-29T11:41:16+00:00
url: /?p=2189
categories:
  - Linux

---
edit /boot/grub/grub.cfg
  
[shell]
  
menuentry &#8216;Debian GNU/Linux, with Linux 2.6.32-5-686-bigmem run level 3&#8242; &#8211;class debian &#8211;class gnu-linux &#8211;class gnu &#8211;class os {
	  
insmod part_msdos
	  
insmod ext2
	  
set root='(hd0,msdos7)&#8217;
	  
search &#8211;no-floppy &#8211;fs-uuid &#8211;set ca201e81-b7d4-4cb1-9a68-707dab19738a
	  
echo &#8216;Loading Linux 2.6.32-5-686-bigmem &#8230;&#8217;
	  
linux /vmlinuz-2.6.32-5-686-bigmem root=/dev/sda8 ro quiet 3
	  
echo &#8216;Loading initial ramdisk &#8230;&#8217;
	  
initrd /initrd.img-2.6.32-5-686-bigmem
  
}

menuentry &#8216;Debian GNU/Linux, with Linux 2.6.32-5-686-bigmem run level 5&#8242; &#8211;class debian &#8211;class gnu-linux &#8211;class gnu &#8211;class os {
	  
insmod part_msdos
	  
insmod ext2
	  
set root='(hd0,msdos7)&#8217;
	  
search &#8211;no-floppy &#8211;fs-uuid &#8211;set ca201e81-b7d4-4cb1-9a68-707dab19738a
	  
echo &#8216;Loading Linux 2.6.32-5-686-bigmem &#8230;&#8217;
	  
linux /vmlinuz-2.6.32-5-686-bigmem root=/dev/sda8 ro quiet 5
	  
echo &#8216;Loading initial ramdisk &#8230;&#8217;
	  
initrd /initrd.img-2.6.32-5-686-bigmem
  
}
  
[/shell]