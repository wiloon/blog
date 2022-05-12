---
title: 'com4j.ComException,80040154 CoCreateInstance failed,Class not registered'
author: "-"
date: 2013-02-18T07:02:11+00:00
url: /?p=5187
categories:
  - Windows
tags:$
  - reprint
---
## 'com4j.ComException,80040154 CoCreateInstance failed,Class not registered'

http://jenkins.361315.n4.nabble.com/VSS-Plugin-com4j-ComException-while-extraction-td374921.html

I had the same issue. The problem is with the VSS installation. If vss client is copied and not installed then the VSS dlls do not get registered. Try registering {Vss client installation folder}win32SSAPI.dll on command prompt as regsvr32 {Vss client installation folder}win32SSAPI.dll