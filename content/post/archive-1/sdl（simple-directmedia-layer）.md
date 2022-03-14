---
title: SDL (Simple DirectMedia Layer) 
author: "-"
date: 2013-11-10T08:04:58+00:00
url: /?p=5938
categories:
  - Uncategorized
tags:
  - KVM
  - linux

---
## SDL (Simple DirectMedia Layer)

**SDL** (Simple DirectMedia Layer) 是一个用C语言编写的、跨平台的、免费和开源的多媒体程序库，它提供了一个简单的接口用于操作硬件平台的图形显示、声音、输入设备等。SDL库被广泛应用于各种操作系统 (如Linux、FreeBSD、Windows、Mac OS、iOS、Android等) 上的游戏开发、多媒体播放器、模拟器 (如QEMU) 等众多应用程序之中。尽管SDL是用C语言编写的，但是其他很多流行的编程语言 (如C++、C#、Java、Objective C、Lisp、Erlang、Pascal、Perl、Python、PHP、Ruby等等) 都提供了SDL库的绑定，在这些编程语言中都可以很方便的调用SDL的功能。

在QEMU模拟器中的图形显示默认就是使用SDL的。当然，需要在编译qemu-kvm时需要配置SDL的支持，之后才能编译SDL功能到QEMU的命令行工具中，最后才能启动客户机时使用SDL的功能。在编译qemu-kvm的系统中，需要有SDL的开发包的支持，在RHEL6.3系统中需要安装SDL-devel这个RPM包。如果有SDL-devel软件包，在3.4.2节中配置QEMU时默认就会配置为提供SDL的支持，通过运行configure程序，在其输出信息中可以看到"SDL support   yes"即表明SDL支持将会被编译进去。当然，如果不想将SDL的支持编译进去，在配置qemu-kvm时加上"–disable-sdl"的参数即可，configure输出信息中会显示提示"SDL support   no"。


debian install sdl

open synaptic..... install libsdl1.2-dev