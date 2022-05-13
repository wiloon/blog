---
author: "-"
date: "2021-03-29 18:02:06" 
title: "X Server, XServer"
categories:
  - inbox
tags:
  - reprint
---
## "X Server, XServer"

背景

大多数时候我们不希望在服务器上安装图形界面，但有时候有些程序需要图形界面，比如安装Oracle的时候。此时，可以配置让Linux使用远程的X Server进行图形界面显示。

首先要明确的是Linux X Window System的基本原理，X是一个开放的协议规范，当前版本为11，俗称X11。X Window System由客户端和服务端组成，服务端X Server负责图形显示，而客户端库X Client根据系统设置的DISPLAY环境变量，将图形显示请求发送给相应的X Server。

因此，我们只需要在远端开启一个X Server，并在目标机器上相应的设置DISPLAY变量，即可完成图形的远程显示。

### command

```bash
export DISPLAY=192.168.97.183:0
```

~/.xinitrc是X的配置文件，在

/etc/skel/.xinitrc
有它的模板，可以把它copy到用户目录下面:
$ cp /etc/skel/.xinitrc ~

以"."开头的文件，通常是隐藏文件，用普通的"ls"是查看不到的，若想查看，需要用"ls -A"命令。

其次，以"rc"结尾的文件代表它是运行的命令行或者是配置文件。又因为它通常控制着程序的运行，所以也通常叫着"run control"

---

<https://blog.csdn.net/vic_qxz/article/details/79073558>
