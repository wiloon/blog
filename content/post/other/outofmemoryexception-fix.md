---
title: OutOfMemoryException Fix
author: "-"
date: 2013-09-04T08:38:07+00:00
url: /?p=5790
categories:
  - Inbox
tags:
  - reprint
---
## OutOfMemoryException Fix

OutOfMemory exceptions are often caused by address space fragmentation in Visual Studio process. For users experiencing excessive OutOfMemory exceptions we provide a tool which overrides Visual Studio's memory allocation policy to ensure more continuous address space for Common Language Runtime.

To use the tool download [wrappers.zip][1] file, unpack it and run devenv2005_wrap, devenv2008_wrap and devenv2010_wrap instead of devenv.exe for Visual Studio 2005, 2008 and 2010 correspondingly.

In some cases Visual Studio fails to start under wrappers. Check AppInit_DLLs. Rogue DLLs activated from there can interfere with wrappers. Example: wxvault.dll preinstalled with Dell laptops.

Sometimes wrappers won't help (because it's simply not enough memory), see <http://stevenharman.net/blog/archive/2008/04/29/hacking-visual-studio-to-use-more-than-2gigabytes-of-memory.aspx> for other solutions and explanations.

 [1]: http://confluence.jetbrains.com/download/attachments/37364/wrappers.zip?version=1&modificationDate=1340040619000
