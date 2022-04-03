---
title: Flatpak
author: "-"
date: 2011-07-29T13:27:07+00:00
url: wording
categories:
  - linux

tags:
  - reprint
---
## Flatpak

Flatpak由红帽员工亚历山大·拉尔森(Alexander Larsson)开发，并于2015年正式发布。它是用C编程开发的，提供了在Linux发行版上安装应用程序的一种快速和直接的方法。

Flatpak的工作原理是将一个应用程序组合并编译成一个包。此前，Flatpak被称为xdg-app。这个特定的框架使用了在沙箱环境中运行应用程序而不需要根特权的概念。因此，一些flatpak应用程序不能访问和利用系统的全部资源。

Flatpak应用程序主要针对三种桌面环境——FreeDesktop、KDE和GNOME。不幸的是，Flatpak不支持任何后端工具，因为它只生成在Desktop环境中运行的应用程序。这是这个包管理器的一个主要缺点，因为它不支持服务器，除非您安装像GNOME这样的桌面环境(DE)。

与Snap类似，Flatpak有一个名为Flathub的在线商店，用户可以在那里找到并下载他们想要的应用程序。Flathub首次发布时，只允许开发者发布免费和开源的应用程序。然而，在更新了他们的条款和条件之后，开发人员现在甚至可以发布专有包。

>https://blog.csdn.net/weixin_39636364/article/details/120424180

```bash
pacan -S flatpak 

flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak search Spotify
flatpak install flathub Spotify
flatpak list
flatpak run com.spotify.Client
flatpak uninstall name
```