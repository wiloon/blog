---
title: modprobe
author: "-"
date: 2011-08-20T20:06:06+00:00
url: modprobe
categories:
  - Linux
tags:
  - reprint
---
## modprobe

modprobe 可载入指定的个别模块，或是载入一组相依的模块。modprobe会根据depmod所产生的相依关系，决定要载入哪些模块。若在载入过程中发生错误，在modprobe会卸载整组的模块

<https://blog.csdn.net/future_fighter/article/details/3862795>

### lsmod

    功能: 列出内核已载入模块的状态
    用法: lsmod
    描述: lsmod 列出/proc/modules的内容。
    输出为: Module(模块名) Size(模块大小) Used by(被...使用)

### command

```bash
modinfo module_name
systool -v -m module_name

modprobe --show-depends

手动加载卸载
控制内核模块载入/移除的命令是kmod 软件包提供的, 要手动装入模块的话，执行:

    modprobe module_name

如果要移除一个模块: 

    modprobe -r module_name

或者:

    rmmod module_name

```

### modinfo 查看内核模块的信息，包括开发人员信息，依赖信息

    modinfo module_name

### load kernel module at boot

    vim /etc/modules-load.d/wireguard.conf

    #load wireguard at boot
    wireguard

---

<https://wiki.archlinux.org/index.php/Kernel_modules_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87>)
