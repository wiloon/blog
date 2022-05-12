---
title: Regsvr32
author: "-"
date: 2013-02-18T03:09:42+00:00
url: /?p=5182
categories:
  - Windows
tags:
  - reprint
---
## Regsvr32

Regsvr32命令的作用是将动态链接库文件注册为注册表中的命令组成。WInXP系统的regsvr32.exe在windowssystem32文件夹下；2000系统的regsvr32.exe在winntsystem32文件夹下。

Regsvr 32命令是Windows中控件文件(如扩展名为DLL、OCX、CPL的文件)的注册和反注册工具。命令格式

Regsvr32 [/s] [/n] [/i[:cmdline]] dllname

/u 卸载安装的控件，卸载服务器注册；

/s 注册成功后不显示操作成功信息框；

/i 调用DllInstall函数并把可选参数[cmdline]传给它，当使用/u时用来卸载DLL；

/n 不调用DllRegisterServer，该参数必须和/i一起使用。

简单实例

要手工注册"E:\CPCW.dll"，只需在"开始→运行"中键入"Regsvr32 E:\CPCW.dll"，单击"确定"按钮后会弹出提示信息"DllRegisterServer in CPCW.dll succeeded"，说明组件注册成功；如果要卸载此组件，在"开始→运行"中键入"Regsvr32 /u E:\CPCW.dll"即可。

格式: regsvr32 [/s] [/n] [/i[:cmdline]] DLLname

使用参数---解除服务器注册

使用参数[/s]---无声；不显示消息框

使用参数---调用DllInstall，给其传递一个可选[cmdline];跟/u参数一起使用时卸载DLL。

使用参数[/n]---不用调用DLLRegisterServer。这个参数必须跟/i一起使用。

实例1: IE无法打开新窗口

regsvr32 actxprxy.dll

regsvr32 shdocvw.dll

重启后如果还不能解决

regsvr32 mshtml.dll

regsvr32 urlmon.dll

regsvr32 msjava.dll

regsvr32 browseui.dll

regsvr32 oleaut32.dll

regsvr32 shell32.dll

实例2: IE无法保存HTML格式文件

regsvr32 inetcomm.dll

实例3: MSN无法登陆

regsvr32 softpub.dll

实例4: windows默认的文件关联混乱

regsvr32 /i shdocvw.dll

regsvr32 /i shell.dll

regsvr32 /i shdoc401.dll

实例5: Window server 2003中无法播放MP3

regsvr32 i3codeca.acm

regsvr32 i3codecx.ax

实例6: Windows添加/删除程序无法启动

regsvr32 mshtml.dll

regsvr32 /i shdocvw.dll

regsvr32 /i shell.dll

实例7 Windows搜索功能故障

regsvr32 urlmon.dll

实例8: 禁止系统对媒体文件进行预览

regsvr32 /u shmedia.dll 恢复可用 regsvr32 shmedia.dll

实例9: 卸载Win XP自带的zip功能

regsvr32 /u zipfldr.dll

实例10: 禁用FSO对象

regsvr32 /u scrrun.dll

实例11:用户帐户打开后看不到里面的内容

regsvr32 nusrmgr.cpl     是用户账户的运行文件
  
regsvr32 mshtml.dll       是HTML解释器相关模块
  
regsvr32 jscript.dll       是Microsoft javascript脚本支持相关文件
  
regsvr32 /i shdocvw.dll   是为Windows应用程序添加基础文件和网络操作相关模块

用户帐户打开空白一般可能模块会出现问题，有的会出现比如模块找不到等

管理員無法打開或設置用戶權限解決方法:
  
執行:regsvr32 uscript.dll
  
regsvr32 mshtml.dll

切换用户出现警示提示，"高级INF安装程序"
  
"错误: 无法定位INF文件C:WINDOWSINFicw.inf

<http://carywu.blog.51cto.com/13185/9536>
