---
title: windows command
author: wiloon
type: post
date: 2015-04-11T01:03:59+00:00
url: /?p=7451
categories:
  - Uncategorized
tags:
  - Windows

---
tasklist



1、查看进程对应哪服务 tasklist -svc
  
2、查看进程调用哪些DLL tasklist -m
  
3、查看调用某一Dll的所有进程 tasklist -m MSVCP60.DLL，有时候不得以需要删除文件夹，老是提示dll文件受保护，不能删除文件夹，找到进程结束掉，regsvr32 -u *.dll注销dll文件，删除。这样应该可以了。
  
4、查看进程详细信息 tasklist -v：&#8221;进程名&#8221;,&#8221;PID&#8221;,&#8221;会话名 ",&#8221;会话#&#8221;,&#8221;内存使用 ",&#8221;状态  ",&#8221;用户名&#8221;,&#8221;CPU 时间&#8221;,&#8221;窗口标题 &#8221;
  
5、筛选器查找进程

<div>
  EQ:　等于
</div>

<div>
  NE:　不等于
</div>

<div>
  LT:　小于
</div>

<div>
  LE:　小于等于
</div>

<div>
  GT:　大于
</div>

<div>
  GE:　大于等于
</div>

<div>
  tasklist -fi "username ne NT authority\system&#8221; -fi "status eq running&#8221; 列出系统中正在运行的非SYSTEM状态的所有进程
</div>

<div>
</div>

<div>
  <div>
    tasklist -fi "username ne NT authority\system&#8221; -fi "status eq running&#8221; 列出系统中正在运行的非SYSTEM状态的所有进程
  </div>
  
  <div>
    tasklist -fi "pid eq 2860&#8221; -svc列出pid是2860的这个进程中的服务 （有问题的进程调用哪些服务）
  </div>
  
  <div>
    tasklist -fi "pid eq 2860&#8221; -m列出pid是2860的这个进程加载的dll模块（有问题的进程调用哪些DLL文件）
  </div>
  
  <div>
    tasklist -fi "pid eq 2860&#8221; -v列出pid是2860的这个进程的详细信息
  </div>
  
  <div>
    tasklist -fi "servicers eq spooler&#8221;列出对应服务是spooler的进程（哪些进程在使用这个有问题的服务）
  </div>
  
  <div>
    tasklist -fi "modules eq MSVCP60.DLL&#8221;列出调用MSVCP60.DLL的进程（哪些进程在使用这个有问题的DLL）
  </div>
</div>

<div>
</div>

<div>
  <div>
    Taskkill -pid 2860/Taskkill -im qq.exe 关掉进程
  </div>
  
  <div>
    系统debug级的ntsd，很多进程Tasklist是杀不了的，但是用ntsd就可以，基本上除了WINDOWS系统自己的管理进程,ntsd都可以杀掉，不过有些rootkit级别的超级木马就无能为力了，不过幸好这类木马还是很少的。
  </div>
  
  <div>
  </div>
  
  <div>
    ntsd
  </div>
  
  <div>
    系统debug级的ntsd，很多进程Tasklist是杀不了的，但是用ntsd就可以，基本上除了WINDOWS系统自己的管理进程,ntsd都可以杀掉，不过有些rootkit级别的超级木马就无能为力了，不过幸好这类木马还是很少的。
  </div>
  
  <div>
    1、利用进程的PID结束进程
  </div>
  
  <div>
    　　命令格式：ntsd -c q -p pid
  </div>
  
  <div>
    　　命令范例： ntsd -c q -p 1332 （结束explorer.exe进程）
  </div>
  
  <div>
    2、利用进程名结束进程
  </div>
  
  <div>
    　　命令格式：ntsd -c q -pn ***.exe （***.exe 为进程名,exe不能省）
  </div>
  
  <div>
    　　命令范例：ntsd -c q -pn explorer.exe
  </div>
</div>

<div>
  大家有补充的，请留言
</div>

本文出自 “[Colt-&#8216;s-Cyberspace][1]” 博客，请务必保留此出处<http://coltiam.blog.51cto.com/1364465/394060>

 [1]: http://coltiam.blog.51cto.com/