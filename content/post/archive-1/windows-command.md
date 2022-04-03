---
title: windows command
author: "-"
date: 2015-04-11T01:03:59+00:00
url: /?p=7451
categories:
  - Uncategorized
tags:
  - Windows

---
## windows command
tasklist


1. 查看进程对应哪服务 tasklist -svc
  
2. 查看进程调用哪些DLL tasklist -m
  
3. 查看调用某一Dll的所有进程 tasklist -m MSVCP60.DLL，有时候不得以需要删除文件夹，老是提示dll文件受保护，不能删除文件夹，找到进程结束掉，regsvr32 -u *.dll注销dll文件，删除。这样应该可以了。
  
4. 查看进程详细信息 tasklist -v: "进程名","PID","会话名 ","会话#","内存使用 ","状态  ","用户名","CPU 时间","窗口标题 "
  
5. 筛选器查找进程

  EQ:等于


  NE:不等于


  LT:小于


  LE:小于等于


  GT:大于


  GE:大于等于


  tasklist -fi "username ne NT authority\system" -fi "status eq running" 列出系统中正在运行的非SYSTEM状态的所有进程
  
    tasklist -fi "username ne NT authority\system" -fi "status eq running" 列出系统中正在运行的非SYSTEM状态的所有进程
  
  
    tasklist -fi "pid eq 2860" -svc列出pid是2860的这个进程中的服务  (有问题的进程调用哪些服务) 
  
  
    tasklist -fi "pid eq 2860" -m列出pid是2860的这个进程加载的dll模块 (有问题的进程调用哪些DLL文件) 
  
  
    tasklist -fi "pid eq 2860" -v列出pid是2860的这个进程的详细信息
  
  
    tasklist -fi "servicers eq spooler"列出对应服务是spooler的进程 (哪些进程在使用这个有问题的服务) 
  
  
    tasklist -fi "modules eq MSVCP60.DLL"列出调用MSVCP60.DLL的进程 (哪些进程在使用这个有问题的DLL) 
  
  
    Taskkill -pid 2860/Taskkill -im qq.exe 关掉进程
  
  
    系统debug级的ntsd，很多进程Tasklist是杀不了的，但是用ntsd就可以，基本上除了WINDOWS系统自己的管理进程,ntsd都可以杀掉，不过有些rootkit级别的超级木马就无能为力了，不过幸好这类木马还是很少的。
  
  
  
    ntsd
  
  
    系统debug级的ntsd，很多进程Tasklist是杀不了的，但是用ntsd就可以，基本上除了WINDOWS系统自己的管理进程,ntsd都可以杀掉，不过有些rootkit级别的超级木马就无能为力了，不过幸好这类木马还是很少的。
  
  
    1、利用进程的PID结束进程
  
  
    命令格式: ntsd -c q -p pid
  
  
    命令范例:  ntsd -c q -p 1332  (结束explorer.exe进程) 
  
  
    2、利用进程名结束进程
  
  
    命令格式: ntsd -c q -pn ***.exe  (***.exe 为进程名,exe不能省) 
  
  
    命令范例: ntsd -c q -pn explorer.exe
  


  大家有补充的，请留言

本文出自 "[Colt-'s-Cyberspace][1]" 博客，请务必保留此出处<http://coltiam.blog.51cto.com/1364465/394060>

 [1]: http://coltiam.blog.51cto.com/