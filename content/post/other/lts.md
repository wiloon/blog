---
title: Archlinux 安装 linux-lts 内核
author: "w1100n"
date: 2022-08-21 08:22:16
url: lts
categories:
  - Linux
tags:
  - remix

---
## Archlinux 安装 linux-lts 内核

Archlinux 如果做服务器用的话, 最好安装 LTS 内核, 否则...说不定哪次更新之后, 服务就起不来了, 比如最近遇到的 linux 5.19.1 和 netavark 的兼容问题.

折腾 k8s, 尝试安装 cri-o 的时候习惯性的先执行了 `pacman -Syu`  (操作系统用的 archlinux ），然后再安装 cri-o, `pacman -S cri-o`, 理论上 cri-o 会默认在 sysctl 里配置 `bridge-nf-call-iptables = 1`，但是重启后发现 `bridge-nf-call-iptables = 1` 没生效，手动配置之后也不行，提示 br_netfilter 内核模块没加载， 手动加载 `modprobe br_netfilter` 又报错说找不到模块，看上去是前面更新系统的时候升级了内核，从 5.16.4.arch1-1 升到了 5.16.5.arch1-1，modprobe 还是到旧内核的目录找 br_netfilter 模块，简单Google了一下看到有人解决 modprobe 的问题建议用 LTS 的内核，又Google了一下 archlinux 换 LTS 内核，然后再 `pacman -S cri-o` 重启之后 sysctl 的配置果然没有问题了， 更换内核的过程记录如下。

- 检查 /boot 目录是否已经挂载 `mount |grep boot`

用 archinstall, [https://github.com/archlinux/archinstall](https://github.com/archlinux/archinstall) 安装的 archlinux 启动之后默认不挂载 /boot 目录，需要手动挂载，再更换内核。  
当然....如果 /boot 不是独立的分区, 可以跳过挂载, 直接安装 linux-lts.  

- 挂载 /boot `mount /dev/sda1 /boot`
- 安装 linux-lts `pacman -S linux-lts`
- 把内核注册到 bootloader， `grub-mkconfig -o /boot/grub/grub.cfg`
- 重启 `reboot`
- 重启后 默认选项 "Arch Linux" 对应的内核应该已经是 linux-lts 了， 也可以选择 Advanced options for Arch Linux, 能看到具体的内核列表。
- 使用 linux-lts 内核启动
- 确认一下当前使用的内核版本 `uname -r`, 比如我的是 `5.15.61-1-lts`
- `/boot` 没挂载的话，记得再挂载一次, 准备删除非 LTS 内核
- 删除非 LTS 内核 `pacman -R linux`
- 更新 bootloader `grub-mkconfig -o /boot/grub/grub.cfg`
- 可以再重启一下 `reboot`

>以下内容为转载

### 长期支持, LTS, Long Term Support

- 长期支持版本通常与应用程序或操作系统有关，LTS 会在较长的时间内获得安全、维护和 (有时有）功能的更新。
- LTS 版本被认为是稳定的版本，它经历了广泛的测试，并且大多包含了多年积累的改进。
- 需要注意的是，LTS 版本的软件不一定涉及功能更新，除非有一个更新的 LTS 版本。但是，LTS 版本的更新中会有必要的错误修复和安全修复。
- LTS 版本被推荐给生产级的消费者、企业和商家，因为你可以获得多年的软件支持，而且软件更新不会破坏系统。

如果你注意到任何软件的非 LTS 版本，它通常是具有新功能和较短支持时间跨度 (例如 6-9 个月）的前沿版本，而 LTS 版本的支持时间为 3-5 年。

#### LTS 的优点

- 软件更新与安全和维护修复的时间很长
- 广泛的测试
- 软件更新不会带来破坏系统的变化
- 你有足够的时间为下一个 LTS 版本准备系统

#### LTS 的缺点

- 不提供最新和最强的功能
- 可能会错过最新的硬件支持
- 也可能会错过最新的应用程序升级

### 引用

[https://linux.cn/article-12618-1.html](https://linux.cn/article-12618-1.html)

[https://averagelinuxuser.com/the-lts-kernel-in-arch-linux/](https://averagelinuxuser.com/the-lts-kernel-in-arch-linux/)

[https://blog.csdn.net/weixin_42157556/article/details/116882203](https://blog.csdn.net/weixin_42157556/article/details/116882203)
