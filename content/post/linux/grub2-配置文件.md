---
title: grub2 配置文件
author: "-"
date: 2011-11-26T08:29:54+00:00
url: /?p=1633
categories:
  - Linux
tags:
  - reprint
---
## grub2 配置文件

## grub config file path

## check grub version

    grub2-install --version

GRUB1.配置文件: /boot/grub/menu.lst
  
GRUB2.配置文件: /boot/grub/grub.cfg，/etc/grub.d/下是生成配置文件的模板，/etc/default/grub是生成配置文件的参数

If you change this file, run 'update-grub' afterward to update
  
/boot/grub/grub.cfg.
  
GRUB_DEFAULT=0 ->设置默认启动项，按menuentry顺序。比如要默认从第四个菜单项启动，数字改为3，若改为 saved，则默认为上次启动项。
  
GRUB_HIDDEN_TIMEOUT=0
  
GRUB_HIDDEN_TIMEOUT_QUIET=true ->隐藏菜单，grub2不再使用，不管
  
GRUB_TIMEOUT="3" ->设置进入默认启动项的等候时间，默认值10秒，按自己需要修改
  
GRUB_DISTRIBUTOR=\`lsb_release -i -s 2> /dev/null || echo Debian\`
  
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash" ->添加内核启动参数，这个为默认
  
GRUB_CMDLINE_LINUX="noresume" ->手动添加内核启动参数，比如 acpi=off noapic等可在这里添加
  
# Uncomment to disable graphical terminal (grub-pc only)
  
#GRUB_TERMINAL=console ->设置是否使用图形介面。去除前面#，仅使用控制台终端，不使用图形介面
  
# The resolution used on graphical terminal
  
# note that you can use only modes which your graphic card supports via VBE
  
# you can see them in real GRUB with the command \`vbeinfo'
  
#GRUB_GFXMODE=640x480 设定图形介面分辨率，如不使用默认，把前面#去掉，把分辨率改为800x600或1024x768
  
# Uncomment if you don't want GRUB to pass "root=UUID=xxx" parameter to Linux
  
#GRUB_DISABLE_LINUX_UUID=true ->设置grub命令是否使用UUID，去掉#，使用root=/dev/sdax而不用root=UUDI=xxx
  
# Uncomment to disable generation of recovery mode menu entrys
  
#GRUB_DISABLE_LINUX_RECOVERY="true" ->设定是否创建修复模式菜单项

### menuentry

    vim /etc/grub.d/40_custom

```bash
menuentry "arch iso" {
   set isofile="/root/archlinux-2022.02.01-x86_64.iso"
   # or set isofile="/<username>/Downloads/ubuntu-20.04-desktop-amd64.iso"
   # if you use a single partition for your $HOME
   rmmod tpm
   search --no-floppy --fs-uuid --set=root 6c40ac7b-4a98-47c2-94ac-9e0a20f4a3c1 
   loopback loop ($root)$isofile
   linux (loop)/casper/vmlinuz boot=casper iso-scan/filename=$isofile noprompt noeject
   initrd (loop)/casper/initrd
}

menuentry "arch iso" {
   set isofile="/root/archlinux-2022.02.01-x86_64.iso"
   loopback loop (hd0,0)$isofile
   linux (loop)/casper/vmlinuz boot=casper iso-scan/filename=$isofile noprompt noeject
   initrd (loop)/casper/initrd.lz
}

menuentry "arch iso" {
  loopback loop /root/archlinux-2022.02.01-x86_64.iso
  linux (loop)/boot/bzImage --
  initrd (loop)/boot/tinycore.gz
}

```

    grub2-mkconfig -o /boot/grub2/grub.cfg

### Linux GRUB磁盘分区表示法

    第一个主分区    /dev/sda1    hd(0,0)
