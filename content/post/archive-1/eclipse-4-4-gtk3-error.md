---
title: eclipse 4.4 gtk3 error
author: "-"
date: 2014-07-13T07:53:28+00:00
url: /?p=6803
categories:
  - Uncategorized
tags:
  - Java

---
## eclipse 4.4 gtk3 error
A fatal error has been detected by the Java Runtime Environment:
#
# SIGSEGV (0xb) at pc=0x00007f19358e673f, pid=18619, tid=139746828388096
#
# JRE version: Java(TM) SE Runtime Environment (8.0_05-b13) (build 1.8.0_05-b13)
# Java VM: Java HotSpot(TM) 64-Bit Server VM (25.5-b02 mixed mode linux-amd64 compressed oops)
# Problematic frame:
# C [libgdk-x11-2.0.so.0+0x5173f] gdk_display_open+0x3f
#
# Core dump written. Default location: /home/wiloon/apps/eclipse/core or core.18619
#
# An error report file with more information is saved as:
# /home/wiloon/apps/eclipse/hs_err_pid18619.log
#
# If you would like to submit a bug report, please visit:
# http://bugreport.sun.com/bugreport/crash.jsp
# The crash happened outside the Java Virtual Machine in native code.
# See problematic frame for where to report the bug.

edit eclipse.init

add row

--launcher.GTK_version
2