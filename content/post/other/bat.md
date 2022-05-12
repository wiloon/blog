---
title: windows bat, 批处理获取当前时间
author: "-"
date: 2013-02-20T11:31:47+00:00
url: /?p=5211
categories:
  - Windows
tags:$
  - reprint
  - bat
---
## 批处理获取当前时间

  rem CODE BY t0nsha
 rem 关于提取date,time输出结果的一个批处理
 rem ":" (冒号) 和"~"波浪号必不可少！
 rem "~"后的数字: 为正数表示舍弃输出结果的前几位；直接跟负数表示取到输出结果的后第几位。
 rem ","后的数字: 为正数表示取到输出结果的前第几位；为负数表示舍弃输出结果的后几位。
 echo %date%
 echo %date:~4%
 ::下行表示舍弃前0位,取到第10位 (即取输出结果的前10位) 
 echo %date:~0,10%
 echo %date:~4,-5%
 pause
 echo %time%
 echo %time:~-3%
 echo %time:~2,-3%
 pause
 echo %date:~4% %time:~0,-3%
 pause 
  
    BTW
  
  
    使用批处理产生日期 (时间) 文件、文件夹 帮别人整Sql     server自动备份
 发现无法使用网络映射驱动器作为备份文件存放路径
 而本机磁盘空间实在是不够
 于是决定在本机只备份最新2天数据
 再写个批处理,做成系统调度
 每周将备份数据复制到网络驱动器上存档
  
  
    从网上搜到批处理产生日期文件的办法
 下面是实现的比较好的
  
  
    批处理文件: 
 @echo off
 set aFile=bak-%DATE:~4,4%%DATE:~9,2%%DATE:~12,2%
 set bFile=bak-%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%
 set cFile=bak-%DATE%
 echo Afile=%aFile%
 echo Bfile=%bFile%
 echo Cfile=%cFile%
  
  
    输出:
 Afile=bak-20061219
 Bfile=bak-113202
 Cfile=bak-星期二 2006-12-19
  
  
    于是备份bat就好写了
 @echo off
 echo 正在备份数据到网络驱动器。。。
 set folder=%DATE%
 md "y:%folder%"
 copy d:DataBak*.BAK "y:%folder%"
 echo 备份完毕。
  
  
    ----------------------------------
 @echo off
 set AFile=bak-%DATE:~4,4%%DATE:~9,2%%DATE:~12,2%
 set BFile=bak-%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%
 echo AFile=%AFile%.rar
 echo BFile=%BFile%.rar
  
  
    运行此批处理的结果: 
 AFile=bak-20060109.rar --- 年月日 - 8位
 BFile=bak-140650.rar ---- 时分秒 - 6位
  
  
    另: 如果小时数只有一位数字,造成中间有空格而出错的问题,请使用如下方法补0
 set hh=%time:~0,2%
 if /i %hh% LSS 10 (set hh=0%time:~1,1%)
  
  
    来自: http://www.5jia6.cn/blog/article.asp?id=173
  
