---
title: OverlayFS
author: wiloon
type: post
date: 2018-04-05T10:26:43+00:00
url: /?p=12109
categories:
  - Uncategorized

---
https://blog.csdn.net/styshoo/article/details/60715942

Docker存储驱动之OverlayFS简介

简介
  
　　OverlayFS是一种和AUFS很类似的文件系统，与AUFS相比，OverlayFS有以下特性：
  
　　　1) 更简单地设计；
  
　　　2) 从3.18开始，就进入了Linux内核主线；
  
　　　3) 可能更快一些。
  
　　因此，OverlayFS在Docker社区关注度提高很快，被很多人认为是AUFS的继承者。就像宣称的一样，OverlayFS还很年轻。所以，在生成环境使用它时，还是需要更加当心。
  
　　Docker的overlay存储驱动利用了很多OverlayFS特性来构建和管理镜像与容器的磁盘结构。
  
　　自从Docker1.12起，Docker也支持overlay2存储驱动，相比于overlay来说，overlay2在inode优化上更加高效。但overlay2驱动只兼容Linux kernel4.0以上的版本。
  
　　注意：自从OverlayFS加入kernel主线后，它在kernel模块中的名称就被从overlayfs改为overlay了。但是为了在本文中区别，我们使用OverlayFS代表整个文件系统，而overlay/overlay2表示Docker的存储驱动。

overlay和overlay2
  
OverlayFS（overlay）的镜像分层与共享
  
　　OverlayFS使用两个目录，把一个目录置放于另一个之上，并且对外提供单个统一的视角。这两个目录通常被称作层，这个分层的技术被称作union mount。术语上，下层的目录叫做lowerdir，上层的叫做upperdir。对外展示的统一视图称作merged。
  
　　下图展示了Docker镜像和Docker容器是如何分层的。镜像层就是lowerdir，容器层是upperdir。暴露在外的统一视图就是所谓的merged。