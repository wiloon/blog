---
author: "-"
date: "2021-03-27 13:37:15" 
title: "kux"
categories:
  - inbox
tags:
  - reprint
---
## "kux"

### kux 转 mp4

https://zhuanlan.zhihu.com/p/111764932
1. 安装youku客户端
2. 执行脚本 
```bat
@echo off
setlocal enabledelayedexpansion
set ffmpeg="C:\Program Files (x86)\YouKu\YoukuClient\nplayer\ffmpeg.exe"
if exist %ffmpeg% (
    for /r . %%i in (*.kux) do (
        %ffmpeg% -y -i "%%i" -c:a copy -c:v copy -threads 2 "%%~dpni.mp4"
        
    )
) else echo

pause
```