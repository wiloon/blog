---
title: linux mt4
author: "-"
date: 2012-05-17T23:21:50+00:00
url: /?p=3151
categories:
  - Inbox
tags:
  - MT4

---
## linux mt4
### download mt4

https://cn.nordfx.com/MetaTrader_4.html

### install

```bash
wine mt4.exe
```

MetaTrader 4平台显示的是哪里的时间 ？
  
MT4服务器显示的是欧洲东部时间 (EET) 。欧洲东部夏令时间比格林尼治时间早3个小时 (GMT+3) ，欧洲东部冬令时间比格林尼治时间早2个小时 (GMT+2) 。

欧洲东部时间 (EET) 于3月最后1个星期日切换至夏令时，于10月最后1个星期日切换至冬令时。

夏令时
  
GMT: 0
  
EET: +3
  
冬令时
  
GMT: 0
  
EET: +2
  
How to install Metatrader 4 under Linux!
  
There is a lot of interest out there in running Metatrader 4 on the Linux platform, however until Metaquotes does a native Linux version, the only option if you want
  
to do it is to run it under WINE emulation.

What follows is a step by step guide to installing MT4 in Linux. I have used the
  
excellent Ubuntu distribution for this task.

1) Install WINE if it's not already installed. I used version wine-1.2-rc3 . Please
  
refer to The Ubuntu Wiki for advanced WINE setup instructions.

2) From a valid windows installation, copy over all the fonts into your wine
  
installation. It assumes you told Ubuntu to mount your windows partition in /windows.
  
(You really only need webdings and wingdings if you don't have windows at all. Use
  
google to find them :))

mount your windows partition to /mnt

```bash
  
cp /mnt/WINDOWS/Fonts/* ~/.wine/drive_c/windows/Fonts/
  
```

3) Copy 2 needed mfc4x DLL and msvcp60.dll files from your valid windows installation.
  
(Again use google to find the DLLs for download if you don't have windows)

```bash
  
cp /mnt/WINDOWS/system32/mfc4* ~/.wine/drive_c/windows/system32/
  
```

```bash
  
cp /mnt/WINDOWS/system32/msvcp60.dll ~/.wine/drive_c/windows/system32/
  
```

4) Download mt4setup from FXOpen

5) Change to the folder where you downloaded it and Install MT4.

```bash
  
wine mt4setup.exe
  
```

6) You should now have an icon on your Desktop and a working install of MT4 under Linux!

  * Please note, in order to set a limit/stop order without an invalid parameters error you
  
    need just to remove the expiry(Uncheck the box under the entry price).

http://rebatefx.com/linux-mt4/