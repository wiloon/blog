---
title: Archlinux 安装 linux-lts 内核
author: "-"
date: 2022-02-06 01:19:31
url: lts
categories:
  - Linux
tags:
  - remix

---
## Archlinux 安装 linux-lts 内核

在 archlinux 上安装 k8s的时候 pacman -S cri-o, 理论上

- 检查 /boot 目录是否已经挂载
- 挂载 /boot `mount /dev/sda1 /boot`
- 安装 linux-lts `pacman -S linux-lts`
- 把内核注册到 bootloader， `grub-mkconfig -o /boot/grub/grub.cfg`
- 重启 `reboot`
- 重启后 默认选项 "Arch Linux" 对应的内核应该已经是 linux-lts了， 也可以选择 Advanced options for Arch Linux, 能看到具体的内核列表。
- 使用 linux-lts 内核启动
- 确认一下当前使用的内核版本 `uname -r`
- 删除非lts 内核 `pacman -R linux`
- 更新 bootloader `grub-mkconfig -o /boot/grub/grub.cfg`

### LTS

什么是长期支持（LTS）版本？
长期支持（LTS）版本通常与应用程序或操作系统有关，你会在较长的时间内获得安全、维护和（有时有）功能的更新。

LTS 版本被认为是最稳定的版本，它经历了广泛的测试，并且大多包含了多年积累的改进。

需要注意的是，LTS 版本的软件不一定涉及功能更新，除非有一个更新的 LTS 版本。但是，你会在 LTS 版本的更新中得到必要的错误修复和安全修复。

LTS 版本被推荐给生产级的消费者、企业和商家，因为你可以获得多年的软件支持，而且软件更新不会破坏系统。

如果你注意到任何软件的非 LTS 版本，它通常是具有新功能和较短支持时间跨度（例如 6-9 个月）的前沿版本，而 LTS 版本的支持时间为 3-5 年。

为了让大家更清楚的了解 LTS 和非 LTS 版本的区别，我们来看看选择 LTS 版本的一些优缺点。

LTS 版本的优点
软件更新与安全和维护修复的时间很长（Ubuntu 有 5 年支持）
广泛的测试
软件更新不会带来破坏系统的变化
你有足够的时间为下一个 LTS 版本准备系统
LTS 版本的缺点
不提供最新和最强的功能
你可能会错过最新的硬件支持
你也可能会错过最新的应用程序升级
现在，你知道了什么是 LTS 版本及其优缺点，是时候了解一下 Ubuntu 的 LTS 版本了。Ubuntu 是最流行的 Linux 发行版之一，也是少数同时拥有 LTS 和非 LTS 版本的发行版之一。

这就是为什么我决定用一整个章节来介绍它。


- 稳定
新版本内核偶尔会有各种奇怪的问题，比如 5.16.5.arch1-1 `modprobe br_netfilter` 报错找不到模块。

LTS 版本被认为是最稳定的版本，它经历了广泛的测试，并且大多包含了多年积累的改进。

LTS 版本的软件不一定涉及功能更新，除非有一个更新的 LTS 版本。但是，你会在 LTS 版本的更新中得到必要的错误修复和安全修复。

LTS 版本被推荐给生产级的消费者、企业和商家，因为你可以获得多年的软件支持，而且软件更新不会破坏系统。
非 LTS 版本，它通常是具有新功能和较短支持时间跨度(例如 6-9 个月)的前沿版本，而 LTS 版本的支持时间为 3-5 年。

LTS 版本的优点：

软件更新与安全和维护修复的时间很长(Ubuntu 有 5 年支持)

广泛的测试

软件更新不会带来破坏系统的变化

你有足够的时间为下一个 LTS 版本准备系统

LTS 版本的缺点：

不提供最新和最强的功能

你可能会错过最新的硬件支持

你也可能会错过最新的应用程序升级

<https://averagelinuxuser.com/the-lts-kernel-in-arch-linux/>  
<https://blog.csdn.net/weixin_42157556/article/details/116882203>
