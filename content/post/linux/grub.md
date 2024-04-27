---
title: grub
author: "-"
date: 2011-11-26T08:29:54+00:00
url: grub
categories:
  - Linux
tags:
  - reprint
  - remix
---
## grub

https://www.gnu.org/software/grub/manual/grub/grub.html#Simple-configuration

GRUB 来自 GRand Unified Bootloader 的缩写。它的功能是在启动时从 BIOS 接管掌控、加载自身、加载 Linux 内核到内存，然后再把执行权交给内核。一旦内核开始掌控，GRUB 就完成了它的任务，也就不再需要了。

GRUB 支持多种 Linux 内核，并允许用户在启动时通过菜单在其中选择。

GRUB 菜单提供了一个 “救援rescue” 内核，用于故障排除或者由于某些原因导致的常规内核不能完成启动过程。

grub.cfg 文件是 GRUB 配置文件。它由 grub2-mkconfig 程序根据用户的配置使用一组主配置文件以及 grub 默认文件而生成。/boot/grub2/grub.cfg 文件在 Linux 安装时会初次生成，安装新内核时又会重新生成。

grub.cfg 文件包括了类似 Bash 脚本的代码以及一个按照安装顺序排序的已安装内核列表。

grub.cfg 的主要配置文件都在 /etc/grub.d 目录。该目录中的每个文件都包含了最终会整合到 grub.cfg 文件中的 GRUB 代码。这些配置文件的命名模式以排序方式设计，这使得最终的 grub.cfg 文件可以按正确的顺序整合而成。每个文件都有注释表明该部分的开始和结束，这些注释也是最终的 grub.cfg 文件的一部分，从而可以看出每个部分是由哪个文件生成。

## grub config file path

## check grub version

```Bash
grub2-install --version
```

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

## menuentry

定义 GRUB 的菜单项。当选中菜单项时，GRUB 将执行括号内的命令。如果最后的命令返回成功，并且内核被加载时，将自动执行 boot 命令。

https://www.cnblogs.com/fluidog/p/15176726.html

## 设置环境变量

set variable=value 设置变量的值

## search

搜索符合条件的分区

查找设备。语法格式如下：

search [-f, --file|--label|--fs-uuid] [--set [<var>]] [--no-floppy] <name>
注解：

[--file|--label|--fs-uuid]

分别表示按文件、文件系统标志、文件系统 UUID 查找设备。

[--set [<var>]]

第一个找到的设备会被设置为环境变量 var 的值。默认变量是 root。

[--no-floppy]

防止搜索软盘。