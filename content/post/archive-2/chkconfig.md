---
title: chkconfig
author: "-"
date: 2018-01-10T07:27:25+00:00
url: /?p=11696
categories:
  - Uncategorized

tags:
  - reprint
---
## chkconfig
```bash
chkconfig --list

# 如果这个服务尚未被添加到 chkconfig 列表中,则现需要使用 –-add 参数将其添加进去
chkconfig –-add postfix

# 比如要将MySQLd设置为开机自动启动
chkconfig MySQLd on

# 取消 postfix 的自动启动
chkconfig postfix off
```

https://www.cnblogs.com/panjun-Donet/archive/2010/08/10/1796873.html

chkconfig命令主要用来更新 (启动或停止) 和查询系统服务的运行级信息。谨记chkconfig不是立即自动禁止或激活一个服务,它只是简单的改变了符号连接。

使用语法: 
  
chkconfig [-add][-del][-list][系统服务] 或 chkconfig [-level <等级代号>][系统服务][on/off/reset]

chkconfig在没有参数运行时,显示用法。如果加上服务名,那么就检查这个服务是否在当前运行级启动。如果是,返回true,否则返回false。如果在服务名后面指定了on,off或者reset,那么chkconfi 会改变指定服务的启动信息。on和off分别指服务被启动和停止,reset指重置服务的启动信息,无论有问题的初始化脚本指定了什么。on和off开关,系统默认只对运行级3,4,5有效,但是reset可以对所有运行级有效。

参数用法: 
     
-add 增加所指定的系统服务,让chkconfig指令得以管理它,并同时在系统启动的叙述文件内增加相关数据。
     
-del 删除所指定的系统服务,不再由chkconfig指令管理,并同时在系统启动的叙述文件内删除相关数据。
     
-level<等级代号> 指定读系统服务要在哪一个执行等级中开启或关毕。
        
等级0表示: 表示关机
        
等级1表示: 单用户模式
        
等级2表示: 无网络连接的多用户命令行模式
        
等级3表示: 有网络连接的多用户命令行模式
        
等级4表示: 不可用
        
等级5表示: 带图形界面的多用户模式
        
等级6表示: 重新启动
        
需要说明的是,level选项可以指定要查看的运行级而不一定是当前运行级。对于每个运行级,只能有一个启动脚本或者停止脚本。当切换运行级时,init不会重新启动已经启动的服务,也不会再次去停止已经停止的服务。

    chkconfig --list [name]: 显示所有运行级系统服务的运行状态信息 (on或off) 。如果指定了name,那么只显示指定的服务在不同运行级的状态。
    chkconfig --add name: 增加一项新的服务。chkconfig确保每个运行级有一项启动(S)或者杀死(K)入口。如有缺少,则会从缺省的init脚本自动建立。
    chkconfig --del name: 删除服务,并把相关符号连接从/etc/rc[0-6].d删除。
    chkconfig [--level levels] name: 设置某一服务在指定的运行级是被启动,停止还是重置。
    

http://www.edbiji.com/doccenter/showdoc/78/nav/994.html