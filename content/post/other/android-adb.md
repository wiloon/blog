---
title: android adb
author: "-"
date: 2012-06-23T01:32:36+00:00
url: /?p=3623
categories:
  - Linux
tags:$
  - reprint
---
## android adb

<http://blog.sina.com.cn/s/blog_51335a000101j59n.html>

启动adb服务, 该服务用来为模拟器或通过USB数据线连接的真机服务, 需要以root权限启动, 否则adb devices会提示no permissions.

```bash
  
adb kill-server
  
adb start-server
  
```

列出已连接的android设备

```bash
  
adb devices
  
```

安装apk

```bash
  
adb install xxx/xxx.apk
  
```

```bash
  
adb shell
  
```

  在SDK的Tools文件夹下包含着Android模拟器操作的重要命令ADB，ADB的全称为Android Debug Bridge，就是调试桥的作用，借助这个工具，我们可以管理设备或手机模拟器的状态 ，还可以进行以下的操作:

   (1) 快速更新设备或手机模拟器中的代码，如应用或Android系统升级；
  (2) 在设备上运行Shell命令；
  (3) 管理设备或手机模拟器上的预定端口；

   (4) 在设备或手机模拟器上复制或粘贴文件。

  ADB的工作方式比较特殊采用监听Socket TCP 5554等端口的方式让IDE和Qemu通信，默认情况下ADB会daemon相关的网络端口，所以当我们运行Eclipse时ADB进程就会自动运行，在Eclipse中通过DDMS来调试Android程序；也可以通过手动方式调用，以下为一些常用的操作供参考。

  1.版本信息

  D:\unsetup\android-sdk-windows-1.0_r1\tools>adb version

  Android Debug Bridge version 1.0.20

  2.安装应用到模拟器
 adb install [-l] [-r] <file>。

  其中file是需要安装的apk文件的决定路径。

  3.卸载已经安装的应用

   (1) 方法1:

       adb uninstall [-k] <package>。

  其中package表示需要卸载的应用的包的名字，k表示是否保留应用的配置信息和cache数据。

   (2) 手动删除。
 adb shell
 cd /data/app
 rm app.apk

  4.进入设备或模拟器的Shell
 adb shell
 通过上面的命令，就可以进入设备或模拟器的Shell环境中，在这个Linux Shell中，可以执行各种Linux 的命令，另外如果只想执行一条Shell命令，可以采用以下的方式:
 adb shell [command]
 如:

  D:\unsetup\android-sdk-windows-1.0_r1\tools>adb shell df

  /dev: 49564K total, 0K used, 49564K available (block size 4096)

  /sqlite_stmt_journals: 4096K total, 0K used, 4096K available (block size 4096)

  /system: 69120K total, 65508K used, 3612K available (block size 4096)

  /data: 76544K total, 63684K used, 12860K available (block size 4096)

  /cache: 69120K total, 1244K used, 67876K available (block size 4096)

  5.转发端口

  可以使用 forward 命令进行任意端口的转发—一个模拟器/设备实例的某一特定主机端口向另一不同端口的转发请求。下面演示了如何建立从主机端口7100到模拟器/设备端口8100的转发。

  adb forward tcp:7100 tcp:8100

  同样地，可以使用ADB来建立命名为抽象的UNIX域 socket ，上述过程如下所示:

  adb forward tcp:7100 local:logd

  6.复制文件

  可以使用adb pull ,push 命令将文件复制到一个模拟器/设备实例的数据文件或是从数据文件中复制。install 命令只将一个apk文件复制到一个特定的位置，与其不同的是，pull 和 push 命令可让用户复制任意的目录和文件到一个模拟器/设备实例的任何位置。

  从模拟器或者设备中复制文件或目录，使用如下命:

  adb pull <remote> <local>

  将文件或目录复制到模拟器或者设备，使用如下命令:

  adb push <local> <remote>

  在这些命令中， <local> 和<remote> 分别指通向自己的发展机 (本地) 和模拟器/设备实例 (远程) 上的目标文件/目录的路径。

  下面是一个例子: :

  adb push foo.txt /sdcard/foo.txt

  7.搜索模拟器/设备的实例
 取得当前运行的模拟器/设备的实例的列表及每个实例的状态，如:

  D:\unsetup\android-sdk-windows-1.0_r1\tools>adb devices

  List of devices attached

  HT843GZ03305    device

  8.查看bug报告

  D:\unsetup\android-sdk-windows-1.0_r1\tools>adb bugreport

  ========================================================

  == dumpstate

  ========================================================

  -- SYSTEM LOG --

  04-12 16:59:46.521 D/ShowTrack(23968): MyOverlay::darw..mDefCaption=I'm Here.

  04-12 16:59:46.531 D/ShowTrack(23968): MyOverlay::darw..mDefCaption=I'm Here.

  04-12 16:59:46.531 D/ShowTrack(23968): MyOverlay::darw..mDefCaption=I'm Here.

  04-12 16:59:46.541 D/ShowTrack(23968): MyOverlay::darw..mDefCaption=I'm Here.

  04-12 16:59:47.391 I/ActivityManager(   55): Starting activity: Intent { comp={com.iceskysl.iTracks/com.iceskysl.iTracks.iTracks} }

  04-12 16:59:47.641 D/iTracks (23968): renderListView.

  04-12 16:59:47.671 D/ShowTrack(23968): MyOverlay::darw..mDefCaption=I'm Here.

  04-12 16:59:47.681 D/ShowTrack(23968): MyOverlay::darw..mDefCaption=I'm Here.

  9.记录无线通讯日志
 一般来说，无线通讯的日志非常多，在运行时没必要去记录，但我们还是可以通过命令，设置记录:

  D:\unsetup\android-sdk-windows-1.0_r1\tools>adb shell

# logcat -b radio

  logcat -b radio

  D/HTC_RIL (   30): (t=1239390296)<< 0

  D/HTC_RIL (   30): (t=1239390296)>> AT@HTCPDPFD=0

  D/HTC_RIL (   30): (t=1239390296)<< 0

  D/HTC_RIL (   30): (t=1239390296)>> AT+CSQ

  D/HTC_RIL (   30): (t=1239390296)<< +CSQ: 29,99

  D/HTC_RIL (   30): 0

  D/HTC_RIL (   30): (t=1239390296)>> AT+CREG?

  D/HTC_RIL (   30): (t=1239390296)<< +CREG: 2,3

  D/HTC_RIL (   30): 0

  10.获取设备的ID和序列号
 adb get-product

  D:\unsetup\android-sdk-windows-1.0_r1\tools>adb get-serialno

  HT843GZ03305

  11.通过远程Shell端运行AQLite3连接数据库

  通过ADB远程Shell端，可以通过Android的软AQLite 3 命令程序来管理数据库。SQLite 3 工具包含了许多使用命令，例如，.dump 显示表的内容，.schema 可以显示出已经存在的表空间的SQL CREATE结果集。SQLite3还允许远程执行sql命令。

  通过SQLite 3 , 按照前面的方法登录模拟器的远程Shell端，然后启动工具就可以使用SQLite 3 命令。当SQLite 3 启动以后，还可以指定想查看的数据库的完整路径。模拟器/设备实例会在文件夹中保存SQLite3数据库/data/data/<package_name> /databases /。

  示例如下:

  $ adb  shell

# sqlite3 /data/data/com.example.google.rss.rssexample/databases/rssitems.db

  SQLite version 3.3.12

  Enter ".help" for instructions

  .... enter commands, then quit...

  sqlite> .exit

  当启动SQLite 3的时候，就可以通过Shell端发送SQLite 3,命令了。用exit 或<Ctrl+D>组合键退出ADB远程Shell端。

  12.ADB命令列表

  下列表格列出了adb支持的所有命令,并对它们的意义和使用方法做了说明.

        Category
      
    
    
    
      
        Command
      
    
    
    
      
        Description
      
    
    
    
      
        Comments
      
    
  
  
  
    
      
        Options
      
    
    
    
      
        -d
      
    
    
    
      
        仅仅通过USB接口来管理abd
      
    
    
    
      
        如果不只是用USB接口来管理则返回错误
      
    
  
  
  
    
      
        -e
      
    
    
    
      
        仅仅通过模拟器实例来管理adb
      
    
    
    
      
        如果不是仅仅通过模拟器实例管理则返回错误
      
    
  
  
  
    
      
        -s <serialNumber>
      
    
    
    
      
        通过模拟器/设备的允许命令号码来发送命令来管理adb (如 "emulator-5556″)
      
    
    
    
      
        如果没有指定号码，则会报错
      
    
  
  
  
    
      
        General
      
    
    
    
      
        devices
      
    
    
    
      
        查看所有连接模拟器/设备的设施的清单
      
    
    
    
      
        查看 Querying for Emulator/Device Instances 获取更多相关信息
      
    
  
  
  
    
      
        help
      
    
    
    
      
        查看adb所支持的所有命令
      
    
    
    
    
  
  
  
    
      
        version
      
    
    
    
      
        查看adb的版本序列号
      
    
    
    
    
  
  
  
    
      
        Debug
      
    
    
    
      
        logcat [<option>] [<filter-specs>]
      
    
    
    
      
        将日志数据输出到屏幕上
      
    
    
    
    
  
  
  
    
      
        bugreport
      
    
    
    
      
        查看bug的报告，如dumpsys ,dumpstate ,和logcat 信息
      
    
    
    
    
  
  
  
    
      
        jdwp
      
    
    
    
      
        查看指定设施的可用的JDWP信息
      
    
    
    
      
        可以用 forward jdwp:<pid> 端口映射信息来连接指定的JDWP进程，例如: 
 adb forward tcp:8000 jdwp:472
 jdb -attach localhost:8000

        Data
      
    
    
    
      
        install <path-to-apk>
      
    
    
    
      
        安装Android为 (可以模拟器/设施的数据文件.apk指定完整的路径) 
      
    
    
    
    
  
  
  
    
      
        pull <remote> <local>
      
    
    
    
      
        将指定的文件从模拟器/设施拷贝到计算机上
      
    
    
    
    
  
  
  
    
      
        push <local> <remote>
      
    
    
    
      
        将指定的文件从计算机上拷贝到模拟器/设备中
      
    
    
    
    
  
  
  
    
      
        Ports and Networking
      
    
    
    
      
        forward <local> <remote>
      
    
    
    
      
        用本地指定的端口通过Socket方法远程连接模拟器/设施
      
    
    
    
      
        端口需要描述下列信息:
      
      
      
        
          tcp:<portnum>
        
        
          local:<UNIX domain socket name>
        
        
          dev:<character device name>
        
        
          jdwp:<pid>
        
      
    
  
  
  
    
      
        ppp <tty> [parm]…
      
    
    
    
      
        通过USB运行ppp: 
      
      
      
        
          <tty> — the tty for PPP stream. For exampledev:/dev/omap_csmi_ttyl.
        
        
          [parm]… &mdash zero or more PPP/PPPD options, such as defaultroute ,local , notty , etc.
        
      
      
      
        需要提醒的不能自动启动PDP连接
      
    
    
    
    
  
  
  
    
      
        Scripting
      
    
    
    
      
        get-serialno
      
    
    
    
      
        查看adb实例的序列号
      
    
    
    
      
        查看 Querying for Emulator/Device Instances 可以获得更多信息
      
    
  
  
  
    
      
        get-state
      
    
    
    
      
        查看模拟器/设施的当前状态
      
    
  
  
  
    
      
        wait-for-device
      
    
    
    
      
        如果设备不联机就不让执行,也就是实例状态是 device 时
      
    
    
    
      
        可以提前把命令转载在adb的命令器中,在命令器中的命令在模拟器/设备连接之前是不会执行其他命令的，示例如下:
      
      
      
        adb wait-for-device shell getprop
      
      
      
        需要提醒的是，这些命令在所有的系统启动起来之前是不会启动adb的，所以在所有的系统启动起来之前也不能执行其他的命令，例如，运用install 的时候就需要Android包，这些包需要系统完全启动，例如: 
      
      
      
        adb wait-for-device install .apk
      
      
      
        上面的命令只有连接上了模拟器/设备连接上了adb服务才会被执行，而在Android系统完全启动前执行就会有错误发生
      
    
  
  
  
    
      
        Server
      
    
    
    
      
        start-server
      
    
    
    
      
        选择服务是否启动adb服务进程
      
    
    
    
    
  
  
  
    
      
        kill-server
      
    
    
    
      
        终止adb服务进程
      
    
    
    
    
  
  
  
    
      
        Shell
      
    
    
    
      
        shell
      
    
    
    
      
        通过远程Shell命令来控制模拟器/设备实例
      
    
    
    
      
        查看获取更多信息 for more information
      
    
  
  
  
    
      
        shell [<shellCommand>]
      
    
    
    
      
        连接模拟器/设施执行Shell命令，执行完毕后退出远程Shell端l
