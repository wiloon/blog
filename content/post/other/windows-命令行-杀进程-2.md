---
title: windows 命令行 杀进程
author: "-"
date: 2014-12-30T02:30:45+00:00
url: /?p=7143
categories:
  - Inbox
tags:
  - Windows

---
## windows 命令行 杀进程

列出进程:

tasklist|findstr task

TASKKILL /IM taskmgr.exe

TASKKILL.exe

TASKKILL命令是Microsoft Windows内置的一款命令,可以用来终止进程,具体的命令规则如下:

TASKKILL [/S system [/U username [/P [password]]]] { [/FI filter] [/PID processid | /IM imagename] } [/F] [/T]

参数列表:

/S system 指定要连接到的远程系统。
/U [domain]user 指定应该在哪个用户上下文 执行这个命令。
/P [password] 为提供的用户上下文指定密码。如果忽略,提示输入。
/F 指定要强行终止的进程。
/FI filter 指定筛选进或筛选出查询的的任务。
/PID process id 指定要终止的进程的PID。
/IM image name 指定要终止的进程的图像名。通配符 '*'可用来指定所有图像名。
/T Tree kill: 终止指定的进程和任何由此启动的子进程。
/? 显示帮助/用法。

示例

TASKKILL /S system /F /IM notepad.exe /T TASKKILL /PID 1230 /PID 1241 /PID 1253 /T TASKKILL /F /IM QQ.exe

<http://netsecurity.51cto.com/art/201309/411766.htm>

## ntsd

ntsd -c q -p PID

win7 需要 安装  win sdk for win7
