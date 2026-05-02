---
title: archlinux packages
author: "-"
date: "2026-05-02T20:02:02+08:00"
url: archlinux-packages
categories:
  - Linux
tags:
  - archlinux
  - remix
  - AI-assisted
---
## archlinux packages

本文逐步记录我的 Arch Linux 系统中安装的软件包，目标是了解每个包在当前系统中的用途，以及它是否是必要的依赖（能否安全删除）。

- `aalib`: ASCII art graphic library
- `aardvark-dns`: Authoritative DNS server for A/AAAA container records
- `abseil-cpp`: Collection of C++ library code designed to augment the C++ standard library
- `adwaita-fonts`: GNOME Adwaita 字体，被 wechat 等应用依赖
- `ansible`: IT automation tool
- `ansible-core`: Ansible core engine
- `aom`: Alliance for Open Media video codec
- `appstream`: Provides a standard for creating app stores across distributions
- `archlinux-appstream-data`: Arch Linux application database for AppStream-based software centers
- `at-spi2-core`: Protocol definitions and daemon for D-Bus at-spi
- `audit`: Userspace components of the audit framework
- `avahi`: Service Discovery for Linux using mDNS/DNS-SD (compatible with Bonjour)
- `baloo-widgets`: KDE Baloo 搜索框架集成小部件
- `bluez-libs`: Deprecated libraries for the bluetooth protocol stack
- `boost-libs`: Boost C++ 通用库运行时动态库，详见 [boost-libs](#boost-libs)
- `botan`: Crypto library written in C++
- `bubblewrap`: 非特权沙箱工具，详见 [bubblewrap](#bubblewrap)
- `btrfs-progs`: Userspace utilities to manage btrfs filesystems
- `c-ares`: 异步 DNS 解析 C 库，被 curl、Node.js 等广泛使用
- `ca-certificates-mozilla`: Mozilla's set of trusted CA certificates
- `cfitsio`: C/Fortran library for reading and writing FITS data format files
- `chrony`: Lightweight NTP client and server
- `conmon`: OCI container runtime monitor
- `cryptsetup`: Userspace setup tool for transparent encryption of block devices using dm-crypt
- `dav1d`: AV1 cross-platform decoder focused on speed and correctness
- `expat`: C 语言实现的流式 XML 解析库（libexpat），详见 [expat](#expat)
- `fftw`: A library for computing the discrete Fourier transform (DFT)
- `fzf`: General-purpose command-line fuzzy finder
- `gcr`: A library for bits of crypto UI and parsing
- `glslang`: OpenGL Shading Language 编译器和验证器，详见 [glslang](#glslang)
- `gnutls`: A library which provides a secure layer over a reliable transport layer
- `gtk-update-icon-cache`: GTK icon cache updater
- `hwdata`: Hardware identification databases
- `iproute2`: IP routing utilities
- `libavif`: Library for encoding and decoding .avif files
- `libplist`: Library to handle Apple Property List files
- `libx11`: X11 client-side library

### expat

C 语言实现的流式 XML 解析库（libexpat），采用 SAX（事件驱动）解析模型，适合处理大型 XML 文档。当前系统被以下包依赖：`antigravity`（Google 的 AI 辅助 IDE 工具）、`avahi`（mDNS/DNS-SD 零配置网络服务）、`cmake`（跨平台构建系统）、`dbus`（进程间通信总线）、`dbus-broker`（D-Bus 的替代实现）、`exiv2`（图片元数据读写库）、`fontconfig`（字体配置库）、`gdb`（GNU 调试器）、`git`（版本控制工具）、`mesa`（OpenGL/Vulkan 图形驱动实现）、`neon`（HTTP/WebDAV 客户端库）、`polkit`（权限授权框架）、`python`（Python 解释器）、`qt6-webengine`（Qt6 网页渲染引擎）、`vtk`（3D 可视化工具库）、`wayland`（显示服务协议库）、`webkit2gtk-4.1`（WebKit 网页渲染引擎）、`wechat-bin`（微信桌面客户端）。

### boost-libs

Boost C++ 通用库集合的运行时组件，包含需要单独编译的动态链接库（非 header-only 部分），涵盖 Filesystem（文件系统）、Regex（正则）、Thread（多线程）、Serialization（序列化）、Asio（异步 I/O）等模块。当前系统被以下包依赖：`kig`（KDE 几何软件）、`libime`（fcitx5 输入法核心）、`libkolabxml`（Kolab 数据格式库）、`maeparser`（化学结构解析）、`source-highlight`（代码高亮）。其中 `libime` 是 fcitx5 输入法的关键依赖。

### bubblewrap

非特权沙箱工具，利用 Linux namespaces 和 seccomp 技术隔离进程运行环境，无需 root 权限。当前系统被以下包依赖：`flatpak`（应用沙箱运行时）、`glycin`（图像加载库，用于 GNOME）、`portable`（可移植应用框架）、`webkit2gtk-4.1`（WebKit 渲染引擎，GTK 版本）。其中 `flatpak` 和 `webkit2gtk-4.1` 是桌面应用生态的关键依赖。

### glslang

GLSL（OpenGL Shading Language）编译器和验证器，也称作 GLslang，是一个以 C 语言为基础的高阶着色语言。由 OpenGL ARB 建立，提供开发者对绘图管线更多的直接控制，而无需使用汇编语言或硬件规格语言。

### akonadi

`Akonadi` 框架为应用程序提供中心数据库来统一保存、索引和获取用户的个人信息。这包括邮件、联系人、日历、事件、日志、闹钟和笔记等。在 SC 4.4 中，KAddressBook 成为首个使用 `Akonadi` 框架的程序。在 SC 4.7 中，KMail、KOrganizer、KJots 等也开始更新使用 `Akonadi`。此外，一些等离子部件也使用 `Akonadi` 保存和获取日历事件、笔记等。

### akonadi-search

`akonadi-search` 为 Akonadi 提供全文搜索功能，基于 `xapian-core` 搜索引擎，提供在 Akonadi 数据库中搜索邮件、联系人、日历等个人信息数据的库和守护进程。当前系统被以下包依赖：`akonadiconsole`（Akonadi 管理与调试控制台）、`kaddressbook`（KDE 联系人管理器）、`kmail`（KDE 邮件客户端）、`merkuro`（KDE 邮件、日历、联系人和任务套件）、`messagelib`（KDE PIM 消息库）、`pimcommon`（KDE PIM 公共库）。

### iana-etc

提供 `/etc/protocols` 和 `/etc/services` 两个文件。

`/etc/protocols`：描述 TCP/IP 子系统中可用的多种 DARPA 网络协议，记录了 TCP/IP 协议族的所有协议类型。

`/etc/services`：提供友好文本名称与端口号、协议类型之间的映射。由互联网号码分配局（IANA，Internet Assigned Numbers Authority）维护。

## linux-firmware

在 Linux Kernel 中，Driver 和 Firmware 是有明确含义的。Driver 是控制被操作系统管理的外部设备的代码段，通过 `driver_register()` 注册到总线上。当设备被注册到同一总线时，总线驱动进行 binding，成功后调用 driver 的 `probe()` 函数初始化设备，并将控制接口注册到 Linux 其他子系统（如字符设备、v4l2 等）。

Firmware 是运行在非"控制处理器"（如外设中的处理器）中的程序，通常使用与主处理器不同的指令集。这些程序以二进制形式存在，拷贝在 `/lib/firmware` 目录下。Driver 在初始化时通过 `request_firmware()` 等接口将指定 firmware 加载到内存，再传输到设备上。

Driver 和 firmware 没有直接关系，firmware 通常由驱动去加载。OS 一般不需要理解 firmware 是什么，只把它当做数据——具体含义只有使用它的设备才知道。

## cmake

一个跨平台的编译（Build）工具。

## gst-plugins-base

GStreamer 流媒体框架的基础插件集合。
