---
title: gitea
author: "-"
date: 2011-08-19T00:19:59+00:00
url: gitea
categories:
  - git
tags:
  - reprint
---
## gitea

Gitea是一款使用Golang编写的可自运营的代码管理工具。

在这个领域，名气最响的应该是Gitlab。但实际使用中Gitlab也有点问题，首先就是资源占用。Gitlab是使用ruby编写的，好几年之前刚出来的时候，一台1G内存的虚拟主机连安装运行都做不到，着实震惊。时至今日都已经发展到了以docker镜像分发，gitlab仍旧会有体积和运行时资源占用的问题。另一点就是功能，对于一般标准团队来说，gitlab的功能太过于丰富，这是往好的地方说，往坏的地方说就是它包含了太多不需要的东西，而这些东西还占用磁盘和运行时资源。

于是着手查看开源的alternative方案，很快就找到了golang研发的gitea。使用golang研发的软件分发都很容易，体积小，安装使用简单，运行时占用资源少。且gitea的功能很完备，某些自身不具备的功能也能通过第三方来解决，比如CI就可以结合同样是golang研发的drone来实施。

https://xenojoshua.com/2019/12/gitea-note/

