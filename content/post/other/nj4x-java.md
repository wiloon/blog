---
title: nj4x java config
author: "-"
date: 2015-05-31T14:47:40+00:00
url: /?p=7734
categories:
  - Uncategorized
tags:
  - MT4

---
## nj4x java config
nj4x requires jdk 1.7 !!!

download jfx-2.3.8.7z from http://www.nj4x.com/downloads

unpack

clear the config file folder under C:\Users\user0\jfx_term

# terminal server找不到配置文件时会提示指定mt4.exe

open nj4x_home/bin/run_terminal_server.exe ( if errordownload and install vcredist_x86.ext )

select/config mt4_home path

run java code

----- end -----

copy nj4x-2.3.8/examples/experts/ into mt4 foolder C:\Program Files\MetaTrader 4\MQL4\Experts

If you are using Windows XP, you have to rename mt45if_xp.dll to mt45if.dll

open mt4 terminal.exe

click menu view>strategy tester

select jfx.ex4 for export advisor, open export properties

symbol:eurusd

