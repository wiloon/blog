---
title: windows默认共享的打开和关闭？
author: "-"
date: 2013-05-16T10:48:32+00:00
url: /?p=5475
categories:
  - Windows
tags:$
  - reprint
---
## windows默认共享的打开和关闭？
<http://www.cnblogs.com/Fooo/archive/2007/06/04/771021.html>

Windows启动时都会默认打开admin$ ipc$ 和每个盘符的共享，对于不必要的默认共享，一般都会把它取消掉，可当又需要打开此默认共享时，又该从哪里设置呢，一般来说有两个地方，MSDOS命令和计算机管理共享文件夹，下面主要从DOS命令来设置，因为比较简单，也可进行批处理。

一、因为Windows是默认打开默认共享的，还是先从删除默认共享开始吧: 

首先从注册表里永久禁止打开默认共享: 

如果要禁止C$、D$、E$一类的共享，可以单击"开始→运行"命令，在运行窗口键入"Regedit"后回车，打开注册表编辑器。依次展开[HKEY_LOCAL_MACHINESYSTEMCurrentControlSetServiceslanmanserverparameters ]分支，将右侧窗口中的DOWRD值"AutoShareServer"设置为"0"即可。
  
如果要禁止ADMIN$共享，可以在同样的分支下，将右侧窗口中的DOWRD值"AutoShareWKs" 设置为"0"即可。
  
如果要禁止IPC$共享，可以在注册表编辑器中依次展开[HKEY_LOCAL_MACHINESYSTEMCurrentControlSetControlLsa]分支，将右侧窗口中的DOWRD值"restrictanonymous"设置值为"1"即可。

当不想改动注册表，或只是临时删除这些共享时，可以使用 net share 命令: 

输入net share 命令时可以查看当前所有的共享

**net share c$ /del
  
net share d$ /del
  
net share ipc$ /del
  
net share admin$ /del**

想每次开机后自动删除默认共享，只需把上面的命令保存为.bat文件，开机自动运行就可以了

二、打开默认共享: 

先在控制面板的"服务"，看SERVER服务是否启动，如果没有启动，则将设置为自动或者手动，然后再选择启动。
  
开启系统的默认共享的方法
  
1.检查AutoShareServer和AutoShareWks注册表值是否为0。
  
2.找到注册表中的HKEY_LOCAL_MACHINESystemCurrentControlSetServicesLanmanServerParameters。
  
3.将下面子项中的AutoShareServer和AutoShareWks DWORD值改为1。
  
4.重启。通常Win2003、Win2000XP会在启动时自动创建。
  
5.启动后，可以通过运行CMD命令进入命令行模式，再运行net share，再共享列表中会看到Admin$、C$IPC$等默认共享。
  
注意: 如果按以上方法仍无效。可能是病毒或恶意程序破坏了系统，这时因先杀毒和恢复系统。
  
此外关闭Server服务、在网卡上去掉Microsoft客户端驱以及在网卡上去掉"文件和打印共享"等都会关闭默认共享。此时要将相应项恢复设置。

也可以在开始菜单的运行中输入CMD，然后输入以下的命令
  
**net share c$=c:
  
net share d$=d:
  
net share ipc$
  
net share admin$**

在计算机管理中的共享文件中也可以对所有的共享目录进行设置，右键"我的电脑"->"管理"->"共享文件"，由于是图形界面比较简单，这里就不在详细说明。