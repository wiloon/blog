---
title: android adb
author: wiloon
type: post
date: 2012-06-23T01:32:36+00:00
url: /?p=3623
categories:
  - Linux

---
http://blog.sina.com.cn/s/blog_51335a000101j59n.html

启动adb服务, 该服务用来为模拟器或通过USB数据线连接的真机服务, 需要以root权限启动, 否则adb devices会提示no permissions.

[shell]
  
adb kill-server
  
sudo adb start-server
  
[/shell]

列出已连接的android设备

[shell]
  
adb devices
  
[/shell]

安装apk

[shell]
  
adb install xxx/xxx.apk
  
[/shell]

[shell]
  
adb shell
  
[/shell]

<p style="color: #4b4b4b;">
  在SDK的Tools文件夹下包含着Android模拟器操作的重要命令ADB，ADB的全称为Android Debug Bridge，就是调试桥的作用，借助这个工具，我们可以管理设备或手机模拟器的状态 ，还可以进行以下的操作：
</p>

<p style="color: #4b4b4b;">
  （1）快速更新设备或手机模拟器中的代码，如应用或Android系统升级；<br /> （2）在设备上运行Shell命令；<br /> （3）管理设备或手机模拟器上的预定端口；
</p>

<p style="color: #4b4b4b;">
  （4）在设备或手机模拟器上复制或粘贴文件。
</p>

<p style="color: #4b4b4b;">
  ADB的工作方式比较特殊采用监听Socket TCP 5554等端口的方式让IDE和Qemu通信，默认情况下ADB会daemon相关的网络端口，所以当我们运行Eclipse时ADB进程就会自动运行，在Eclipse中通过DDMS来调试Android程序；也可以通过手动方式调用，以下为一些常用的操作供参考。
</p>

<p style="color: #4b4b4b;">
  <strong>1.</strong><strong>版本信息</strong>
</p>

<p style="color: #4b4b4b;">
  D:\unsetup\android-sdk-windows-1.0_r1\tools>adb version
</p>

<p style="color: #4b4b4b;">
  Android Debug Bridge version 1.0.20
</p>

<p style="color: #4b4b4b;">
  2.<strong>安装应用到模拟器</strong><br /> adb install [-l] [-r] <file>。
</p>

<p style="color: #4b4b4b;">
  其中file是需要安装的apk文件的决定路径。
</p>

<p style="color: #4b4b4b;">
  <strong>3.</strong><strong>卸载已经安装的应用</strong>
</p>

<p style="color: #4b4b4b;">
  （1）方法1：
</p>

<p style="color: #4b4b4b;">
       adb uninstall [-k] <package>。
</p>

<p style="color: #4b4b4b;">
  其中package表示需要卸载的应用的包的名字，k表示是否保留应用的配置信息和cache数据。
</p>

<p style="color: #4b4b4b;">
  （2）手动删除。<br /> adb shell<br /> cd /data/app<br /> rm app.apk
</p>

<p style="color: #4b4b4b;">
  4.<strong>进入设备或模拟器的</strong><strong>S</strong><strong>hell</strong><br /> adb shell<br /> 通过上面的命令，就可以进入设备或模拟器的Shell环境中，在这个Linux Shell中，可以执行各种Linux 的命令，另外如果只想执行一条Shell命令，可以采用以下的方式：<br /> adb shell [command]<br /> 如：
</p>

<p style="color: #4b4b4b;">
  D:\unsetup\android-sdk-windows-1.0_r1\tools>adb shell df
</p>

<p style="color: #4b4b4b;">
  /dev: 49564K total, 0K used, 49564K available (block size 4096)
</p>

<p style="color: #4b4b4b;">
  /sqlite_stmt_journals: 4096K total, 0K used, 4096K available (block size 4096)
</p>

<p style="color: #4b4b4b;">
  /system: 69120K total, 65508K used, 3612K available (block size 4096)
</p>

<p style="color: #4b4b4b;">
  /data: 76544K total, 63684K used, 12860K available (block size 4096)
</p>

<p style="color: #4b4b4b;">
  /cache: 69120K total, 1244K used, 67876K available (block size 4096)
</p>

<p style="color: #4b4b4b;">
  <strong>5.</strong><strong>转发端口</strong>
</p>

<p style="color: #4b4b4b;">
  可以使用 forward 命令进行任意端口的转发—一个模拟器/设备实例的某一特定主机端口向另一不同端口的转发请求。下面演示了如何建立从主机端口7100到模拟器/设备端口8100的转发。
</p>

<p class="PreformattedText" style="color: #4b4b4b;">
  adb forward tcp:7100 tcp:8100
</p>

<p style="color: #4b4b4b;">
  同样地，可以使用ADB来建立命名为抽象的UNIX域套接口，上述过程如下所示:
</p>

<p class="PreformattedText" style="color: #4b4b4b;">
  adb forward tcp:7100 local:logd
</p>

<p style="color: #4b4b4b;">
  6.<strong>复制文件</strong>
</p>

<p style="color: #4b4b4b;">
  可以使用adb pull ,push 命令将文件复制到一个模拟器/设备实例的数据文件或是从数据文件中复制。install 命令只将一个apk文件复制到一个特定的位置，与其不同的是，pull 和 push 命令可让用户复制任意的目录和文件到一个模拟器/设备实例的任何位置。
</p>

<p style="color: #4b4b4b;">
  从模拟器或者设备中复制文件或目录，使用如下命:
</p>

<p class="PreformattedText" style="color: #4b4b4b;">
  adb pull <remote> <local>
</p>

<p style="color: #4b4b4b;">
  将文件或目录复制到模拟器或者设备，使用如下命令：
</p>

<p class="PreformattedText" style="color: #4b4b4b;">
  adb push <local> <remote>
</p>

<p style="color: #4b4b4b;">
  在这些命令中， <local> 和<remote> 分别指通向自己的发展机（本地）和模拟器/设备实例（远程）上的目标文件/目录的路径<strong>。</strong>
</p>

<p style="color: #4b4b4b;">
  下面是一个例子：:
</p>

<p class="PreformattedText" style="color: #4b4b4b;">
  adb push foo.txt /sdcard/foo.txt
</p>

<p style="color: #4b4b4b;">
  7.<strong>搜索模拟器</strong><strong>/</strong><strong>设备的实例</strong><br /> 取得当前运行的模拟器/设备的实例的列表及每个实例的状态，如：
</p>

<p style="color: #4b4b4b;">
  D:\unsetup\android-sdk-windows-1.0_r1\tools>adb devices
</p>

<p style="color: #4b4b4b;">
  List of devices attached
</p>

<p style="color: #4b4b4b;">
  HT843GZ03305    device
</p>

<p style="color: #4b4b4b;">
  8.<strong>查看</strong><strong>bug</strong><strong>报告</strong>
</p>

<p style="color: #4b4b4b;">
  D:\unsetup\android-sdk-windows-1.0_r1\tools>adb bugreport
</p>

<p style="color: #4b4b4b;">
  ========================================================
</p>

<p style="color: #4b4b4b;">
  == dumpstate
</p>

<p style="color: #4b4b4b;">
  ========================================================
</p>

<p style="color: #4b4b4b;">
  &#8212;&#8212; SYSTEM LOG &#8212;&#8212;
</p>

<p style="color: #4b4b4b;">
  04-12 16:59:46.521 D/ShowTrack(23968): MyOverlay::darw..mDefCaption=I&#8217;m Here.
</p>

<p style="color: #4b4b4b;">
  04-12 16:59:46.531 D/ShowTrack(23968): MyOverlay::darw..mDefCaption=I&#8217;m Here.
</p>

<p style="color: #4b4b4b;">
  04-12 16:59:46.531 D/ShowTrack(23968): MyOverlay::darw..mDefCaption=I&#8217;m Here.
</p>

<p style="color: #4b4b4b;">
  04-12 16:59:46.541 D/ShowTrack(23968): MyOverlay::darw..mDefCaption=I&#8217;m Here.
</p>

<p style="color: #4b4b4b;">
  04-12 16:59:47.391 I/ActivityManager(   55): Starting activity: Intent { comp={com.iceskysl.iTracks/com.iceskysl.iTracks.iTracks} }
</p>

<p style="color: #4b4b4b;">
  04-12 16:59:47.641 D/iTracks (23968): renderListView.
</p>

<p style="color: #4b4b4b;">
  04-12 16:59:47.671 D/ShowTrack(23968): MyOverlay::darw..mDefCaption=I&#8217;m Here.
</p>

<p style="color: #4b4b4b;">
  04-12 16:59:47.681 D/ShowTrack(23968): MyOverlay::darw..mDefCaption=I&#8217;m Here.
</p>

<p style="color: #4b4b4b;">
  9.<strong>记录无线通讯日志</strong><br /> 一般来说，无线通讯的日志非常多，在运行时没必要去记录，但我们还是可以通过命令，设置记录：
</p>

<p style="color: #4b4b4b;">
  D:\unsetup\android-sdk-windows-1.0_r1\tools>adb shell
</p>

<p style="color: #4b4b4b;">
  # logcat -b radio
</p>

<p style="color: #4b4b4b;">
  logcat -b radio
</p>

<p style="color: #4b4b4b;">
  D/HTC_RIL (   30): (t=1239390296)<< 0
</p>

<p style="color: #4b4b4b;">
  D/HTC_RIL (   30): (t=1239390296)>> AT@HTCPDPFD=0
</p>

<p style="color: #4b4b4b;">
  D/HTC_RIL (   30): (t=1239390296)<< 0
</p>

<p style="color: #4b4b4b;">
  D/HTC_RIL (   30): (t=1239390296)>> AT+CSQ
</p>

<p style="color: #4b4b4b;">
  D/HTC_RIL (   30): (t=1239390296)<< +CSQ: 29,99
</p>

<p style="color: #4b4b4b;">
  D/HTC_RIL (   30): 0
</p>

<p style="color: #4b4b4b;">
  D/HTC_RIL (   30): (t=1239390296)>> AT+CREG?
</p>

<p style="color: #4b4b4b;">
  D/HTC_RIL (   30): (t=1239390296)<< +CREG: 2,3
</p>

<p style="color: #4b4b4b;">
  D/HTC_RIL (   30): 0
</p>

<p style="color: #4b4b4b;">
  10.<strong>获取设备的</strong><strong>ID</strong><strong>和序列号</strong><br /> adb get-product
</p>

<p style="color: #4b4b4b;">
  D:\unsetup\android-sdk-windows-1.0_r1\tools>adb get-serialno
</p>

<p style="color: #4b4b4b;">
  HT843GZ03305
</p>

<p style="color: #4b4b4b;">
  <strong>11.通过远程</strong><strong>Shell端运行</strong><strong>AQLite3连接数据库</strong>
</p>

<p style="color: #4b4b4b;">
  通过ADB远程Shell端，可以通过Android的软AQLite 3 命令程序来管理数据库。SQLite 3 工具包含了许多使用命令，例如，.dump 显示表的内容，.schema 可以显示出已经存在的表空间的SQL CREATE结果集。SQLite3还允许远程执行sql命令。
</p>

<p style="color: #4b4b4b;">
  通过SQLite 3 , 按照前面的方法登录模拟器的远程Shell端，然后启动工具就可以使用SQLite 3 命令。当SQLite 3 启动以后，还可以指定想查看的数据库的完整路径。模拟器/设备实例会在文件夹中保存SQLite3数据库/data/data/<package_name> /databases /。
</p>

<p style="color: #4b4b4b;">
  示例如下:
</p>

<p style="color: #4b4b4b;">
  $ adb  shell
</p>

<p style="color: #4b4b4b;">
  # sqlite3 /data/data/com.example.google.rss.rssexample/databases/rssitems.db
</p>

<p style="color: #4b4b4b;">
  SQLite version 3.3.12
</p>

<p style="color: #4b4b4b;">
  Enter &#8220;.help&#8221; for instructions
</p>

<p style="color: #4b4b4b;">
  &#8230;. enter commands, then quit&#8230;
</p>

<p style="color: #4b4b4b;">
  sqlite> .exit
</p>

<p style="color: #4b4b4b;">
  当启动SQLite 3的时候，就可以通过Shell端发送SQLite 3,命令了。用exit 或<Ctrl+D>组合键退出ADB远程Shell端。
</p>

<p style="color: #4b4b4b;">
  <strong>12.ADB</strong><strong>命令列表</strong>
</p>

<p style="color: #4b4b4b;">
  下列表格列出了adb支持的所有命令,并对它们的意义和使用方法做了说明.
</p>

<table style="color: #4b4b4b;" border="1" cellspacing="0" cellpadding="0">
  <tr>
    <td style="color: #454545;">
      <p class="TableHeading">
        Category
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableHeading">
        Command
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableHeading">
        Description
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableHeading">
        Comments
      </p>
    </td>
  </tr>
  
  <tr>
    <td style="color: #454545;" rowspan="3">
      <p class="TableContents">
        Options
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        -d
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        仅仅通过USB接口来管理abd
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        如果不只是用USB接口来管理则返回错误
      </p>
    </td>
  </tr>
  
  <tr>
    <td style="color: #454545;">
      <p class="TableContents">
        -e
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        仅仅通过模拟器实例来管理adb
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        如果不是仅仅通过模拟器实例管理则返回错误
      </p>
    </td>
  </tr>
  
  <tr>
    <td style="color: #454545;">
      <p class="TableContents">
        -s <serialNumber>
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        通过模拟器/设备的允许命令号码来发送命令来管理adb (如 “emulator-5556″)
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        如果没有指定号码，则会报错
      </p>
    </td>
  </tr>
  
  <tr>
    <td style="color: #454545;" rowspan="3">
      <p class="TableContents">
        General
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        devices
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        查看所有连接模拟器/设备的设施的清单
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        查看 Querying for Emulator/Device Instances 获取更多相关信息
      </p>
    </td>
  </tr>
  
  <tr>
    <td style="color: #454545;">
      <p class="TableContents">
        help
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        查看adb所支持的所有命令
      </p>
    </td>
    
    <td style="color: #454545;">
    </td>
  </tr>
  
  <tr>
    <td style="color: #454545;">
      <p class="TableContents">
        version
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        查看adb的版本序列号
      </p>
    </td>
    
    <td style="color: #454545;">
    </td>
  </tr>
  
  <tr>
    <td style="color: #454545;" rowspan="3">
      <p class="TableContents">
        Debug
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        logcat [<option>] [<filter-specs>]
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        将日志数据输出到屏幕上
      </p>
    </td>
    
    <td style="color: #454545;">
    </td>
  </tr>
  
  <tr>
    <td style="color: #454545;">
      <p class="TableContents">
        bugreport
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        查看bug的报告，如dumpsys ,dumpstate ,和logcat 信息
      </p>
    </td>
    
    <td style="color: #454545;">
    </td>
  </tr>
  
  <tr>
    <td style="color: #454545;">
      <p class="TableContents">
        jdwp
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        查看指定设施的可用的JDWP信息
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        可以用 forward jdwp:<pid>端口映射信息来连接指定的JDWP进程，例如：<br /> adb forward tcp:8000 jdwp:472<br /> jdb -attach localhost:8000
      </p>
    </td>
  </tr>
  
  <tr>
    <td style="color: #454545;" rowspan="3">
      <p class="TableContents">
        Data
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        install <path-to-apk>
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        安装Android为（可以模拟器/设施的数据文件.apk指定完整的路径）
      </p>
    </td>
    
    <td style="color: #454545;">
    </td>
  </tr>
  
  <tr>
    <td style="color: #454545;">
      <p class="TableContents">
        pull <remote> <local>
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        将指定的文件从模拟器/设施拷贝到计算机上
      </p>
    </td>
    
    <td style="color: #454545;">
    </td>
  </tr>
  
  <tr>
    <td style="color: #454545;">
      <p class="TableContents">
        push <local> <remote>
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        将指定的文件从计算机上拷贝到模拟器/设备中
      </p>
    </td>
    
    <td style="color: #454545;">
    </td>
  </tr>
  
  <tr>
    <td style="color: #454545;" rowspan="2">
      <p class="TableContents">
        Ports and Networking
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        forward <local> <remote>
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        用本地指定的端口通过Socket方法远程连接模拟器/设施
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        端口需要描述下列信息:
      </p>
      
      <ul>
        <li>
          tcp:<portnum>
        </li>
        <li>
          local:<UNIX domain socket name>
        </li>
        <li>
          dev:<character device name>
        </li>
        <li>
          jdwp:<pid>
        </li>
      </ul>
    </td>
  </tr>
  
  <tr>
    <td style="color: #454545;">
      <p class="TableContents">
        ppp <tty> [parm]…
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        通过USB运行ppp：
      </p>
      
      <ul>
        <li>
          <tty> — the tty for PPP stream. For exampledev:/dev/omap_csmi_ttyl.
        </li>
        <li>
          [parm]… &mdash zero or more PPP/PPPD options, such as defaultroute ,local , notty , etc.
        </li>
      </ul>
      
      <p class="TableContents">
        需要提醒的不能自动启动PDP连接
      </p>
    </td>
    
    <td style="color: #454545;">
    </td>
  </tr>
  
  <tr>
    <td style="color: #454545;" rowspan="3">
      <p class="TableContents">
        Scripting
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        get-serialno
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        查看adb实例的序列号
      </p>
    </td>
    
    <td style="color: #454545;" rowspan="2">
      <p class="TableContents">
        查看 Querying for Emulator/Device Instances 可以获得更多信息
      </p>
    </td>
  </tr>
  
  <tr>
    <td style="color: #454545;">
      <p class="TableContents">
        get-state
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        查看模拟器/设施的当前状态
      </p>
    </td>
  </tr>
  
  <tr>
    <td style="color: #454545;">
      <p class="TableContents">
        wait-for-device
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        如果设备不联机就不让执行,也就是实例状态是 device 时
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        可以提前把命令转载在adb的命令器中,在命令器中的命令在模拟器/设备连接之前是不会执行其他命令的，示例如下:
      </p>
      
      <p class="PreformattedText">
        adb wait-for-device shell getprop
      </p>
      
      <p class="TableContents">
        需要提醒的是，这些命令在所有的系统启动起来之前是不会启动adb的，所以在所有的系统启动起来之前也不能执行其他的命令，例如，运用install 的时候就需要Android包，这些包需要系统完全启动，例如：
      </p>
      
      <p class="PreformattedText">
        adb wait-for-device install <app>.apk
      </p>
      
      <p class="TableContents">
        上面的命令只有连接上了模拟器/设备连接上了adb服务才会被执行，而在Android系统完全启动前执行就会有错误发生
      </p>
    </td>
  </tr>
  
  <tr>
    <td style="color: #454545;" rowspan="2">
      <p class="TableContents">
        Server
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        start-server
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        选择服务是否启动adb服务进程
      </p>
    </td>
    
    <td style="color: #454545;">
    </td>
  </tr>
  
  <tr>
    <td style="color: #454545;">
      <p class="TableContents">
        kill-server
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        终止adb服务进程
      </p>
    </td>
    
    <td style="color: #454545;">
    </td>
  </tr>
  
  <tr>
    <td style="color: #454545;" rowspan="2">
      <p class="TableContents">
        Shell
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        shell
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        通过远程Shell命令来控制模拟器/设备实例
      </p>
    </td>
    
    <td style="color: #454545;" rowspan="2">
      <p class="TableContents">
        查看获取更多信息 for more information
      </p>
    </td>
  </tr>
  
  <tr>
    <td style="color: #454545;">
      <p class="TableContents">
        shell [<shellCommand>]
      </p>
    </td>
    
    <td style="color: #454545;">
      <p class="TableContents">
        连接模拟器/设施执行Shell命令，执行完毕后退出远程Shell端l
      </p>
    </td>
  </tr>
</table>