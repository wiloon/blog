---
title: modprobe, `lsmod`
author: "-"
date: 2011-08-20T20:06:06+00:00
url: modprobe
categories:
  - Linux
tags:
  - reprint
---
## modprobe, `lsmod`

modprobe 可载入指定的个别模块，或是载入一组相依的模块。modprobe 会根据 `depmod` 所产生的相依关系，决定要载入哪些模块。
若在载入过程中发生错误，在 modprobe 会卸载整组的模块

[https://blog.csdn.net/future_fighter/article/details/3862795](https://blog.csdn.net/future_fighter/article/details/3862795)

### `lsmod`

- 功能: 列出内核已载入模块的状态
- 用法: `lsmod`
- 描述: `lsmod` 列出 `/proc/modules` 的内容。
- 输出为: Module(模块名) Size(模块大小) Used by(被...使用)

```Bash
# 查看某一个模块是否已经被加载
lsmod|grep wireguard
```

### 手动加载卸载
控制内核模块载入/移除的命令是 `kmod` 软件包提供的

```Bash
# 手动加载内核模块
sudo modprobe wireguard

# 手动卸载内核模块
modprobe -r wireguard

# 或者
rmmod wireguard
```

### load kernel module at boot

```bash
vim /etc/modules-load.d/wireguard.conf

# load wireguard module at boot
wireguard
```

## command

```bash
systool -v -m module_name

modprobe --show-depends
```

### `modinfo` 查看内核模块的信息，包括开发人员信息，依赖信息

```bash
modinfo module_name
```

[https://wiki.archlinux.org/index.php/Kernel_modules_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87](https://wiki.archlinux.org/index.php/Kernel_modules_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87))
