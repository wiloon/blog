---
title: git-am
author: "-"
date: 2020-03-17T03:06:27+00:00
url: /?p=15770
categories:
  - Uncategorized

tags:
  - reprint
---
## git-am
https://blog.csdn.net/mliubing2532/article/details/7577905

这篇文章主要介绍一下git-am 和 format-patch 的使用。 因为在git使用当中，会有很多时候别人 (供应商或者其他的开发人员) 发过来一系列的patch，这些patch通常的是类似这样的名字: 

0001-JFFS2-community-fix-with-not-use-OOB.patch
   
0002-Community-patch-for-Fix-mount-error-in.patch
   
0003-partial-low-interrupt-latency-mode-for-ARM113.patch
   
0004-for-the-global-I-cache-invalidation-ARM11.patch
   
0005-1-arm-Add-more-cache-memory-types-macr.patch
   
0006-2-Port-imx-3.3.0-release-to-2.6.28.patch
   
0007-3-Add-MX25-support.patch
   
0008-Move-asm-arch-headers-to-linux-inc-dir.patch
   
0009-1-regulator-allow-search-by-regulator.patch
  
里面包含了提交的日志，作者，日期等信息。你想做的是把这些patch引入到你的代码库中，最好是也可以把日志也引入进来， 方便以后维护用。传统的打patch方式是

patch -p1 < 0001-JFFS2-community-fix-with-not-use-OOB.patch
  
这样来打patch，但是这样会把这些有用的信息丢失。由于这些patch显然是用git format-patch来生成的，所以用git的工具应该就可以很好的做好。git-am 就是作这件事情。

在使用git-am之前， 你要首先git am –abort 一次，来放弃掉以前的am信息，这样才可以进行一次全新的am。
  
不然会遇到这样的错误。
.git/rebase-apply still exists but mbox given.

git-am 可以一次合并一个文件，或者一个目录下所有的patch，或者你的邮箱目录下的patch.

下面举两个例子: 

你现在有一个code base:  small-src, 你的patch文件放在~/patch/0001-trival-patch.patch
  
 

cd small-src
   
git-am ~/patch/0001-trival-patch.patch
  
如果成功patch上去， 你就可以去喝杯茶了。如果失败了， git 会提示错误， 比如: 

error: patch failed: android/mediascanner.cpp:452 error: android/mediascanner.cpp: patch does not apply
  
这样你就需要先看看patch， 然后改改错误的这个文件，让这个patch能够patch上去。

你有一堆patch， 名字是上面提到的那一堆patch， 你把他们放在~/patch-set/目录下 (路径随意) 
  
 

cd opencore
   
git am ~/patch-set/*.patch
  
(这里git就会按照文件名的顺序一次am这些patch) 如果一切顺利， 你所有的patch都OK了， 你又Lucky了。不过不顺利的时候十有八九，如果git am中间遇到了patch,am就会停到打这个patch的地方， 告诉你是哪个patch打不上去。

比如我现在有一个文件file,有两个patch.
  
file 的内容是

the text
   
more text
  
两个patch分别是: 

0001-add-line.patch:

From 8869ccbced494e05738090afa5a54f2a261df0f Mon Sep 1700:00:00 2001
   
From: abc abc@abc-desktop.(none)
   
Date: Thu, 22 Apr 2010 13:04:34 +0800
   
Subject: [PATCH 1/2] add line - file | 2 ++

1 files changed, 2 insertions(+), 0 deletions(-)

diff -git a/file b/file
   
index 067780e..685f0fa 100644
   
- a/file
   
+++ b/file
   
@@ -3,3 +3,5 @@ file:
   
some text more text + +add line - 1.6.3.3
  
0002-change-line.patch:

From f756e1b3a87c216b7e0afea9d15badd033171578 Mon Sep 17 00:00:00 2001
   
From: abc abc@abc-desktop.(none)
   
Date: Thu, 22 Apr 2010 13:05:19 +0800
   
Subject: [PATCH 2/2] change line - file | 2 +-
   
1 files changed, 1 insertions(+), 1 deletions(-) diff -git a/file b/file
   
index 685f0fa..7af7852 100644
   
- a/file
   
file: -some text
   
+Change line text
   
more text
   
- 1.6.3.3
  
运行
  
git am *.patch

来merge这些patch， 报错， Patch failed at 0001 add line这样我们看0001这个patch,原来patch需要的是some text, 而file里面是the text, 所以我们用编辑器把这行改成some text,

vi file
   
git apply 0001-add-line.patch
   
git add file
   
git am -resolved
  
在解决完冲突以后， 比如用git add来让git知道你已经解决完冲突了。

如果你发现这个冲突是无法解决的， 要撤销整个am的东西。 可以运行git am –abort，
  
如果你想只是忽略这一个patch，可以运行git am –skip来跳过这个patch.
  
————————————————
  
版权声明: 本文为CSDN博主「生命不息奋斗不止」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
  
原文链接: https://blog.csdn.net/mliubing2532/article/details/7577905