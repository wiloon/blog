---
title: Linux系统日志–syslog
author: "-"
date: 2011-12-30T15:41:45+00:00
url: /?p=2057
categories:
  - Linux
tags:
  - reprint
---
## Linux系统日志–syslog
我们可以借助syslog函数将消息写入到/var/log/messages文件或其他配置好的文章。syslogd (系统日志守护进程) 会监控程序提交的消息并对其进行处理。klogd (内核日志守护进程) 负责监控内核提交的消息，并将内核消息记录到/var/log/messages。二者协作记录日志消息。每次启动linux时，这两个守护进程都会由/etc/rc.d/init.d中的初始化脚本启动。
  
    #vi /etc/syslog.conf 
    
    
      daemon.info    /var/log/messages
  

syslog.conf文件中每一行包括以下内容: 

l       选择器， 用于表明应该记录哪些消息的一组单词。包括设备 (用于指定选择哪种类型程序的代码，即生成该消息的程序类别) 和优先级 (又能够于指定选择记录的消息类型，更确切的说是表明该消息所代表事件的严重程度) 。

l       动作，用于指定sysogd接收到与选择标准相匹配的消息时应该执行的动作，通常可以使消息要写入的文件名，或应该显示该消息的机器的用户名。

设备


  
    
               设备描述
    
    
    
               设备名
    
  
  
  
    
      来自login等用户身份验证类程序的消息
    
    
    
        auth
    
  
  
  
    
      特殊目的 (私有) 用户身份验证消息
    
    
    
        auth-priv
    
  
  
  
    
      来自cron程序的消息 (用于控制自动化得，调度后的任务) 
    
    
    
        cron
    
  
  
  
    
      来自未在此处列出的所有标准守护进程或服务器的消息
    
    
    
        deamon
    
  
  
  
    
      内核消息 (由klogd捕捉) 
    
    
    
        kern
    
  
  
  
    
      打印服务器消息
    
    
    
        lpr
    
  
  
  
    
      邮件服务器消息 (来自mail transfer agent) 
    
    
    
        mail
    
  
  
  
    
      新闻服务器消息
    
    
    
        news
    
  
  
  
    
      关于系统登录进程本身的消息
    
    
    
        syslog
    
  
  
  
    
      来自终端用户所启动程序的消息
    
    
    
        user
    
  
  
  
    
      来自uucp程序的消息
    
    
    
        uucp
    
  
  
  
    
      八个特定用途的类别信息，linux销售商和编程人员可能需要使用这些消息来定义通常类别信息之外的特定需求
    
    
    
        local0到local7
    
  


优先级


  
    
               优先级描述
    
    
    
            优先级名
    
  
  
  
    
      无优先级
    
    
    
        none
    
  
  
  
    
      调试信息
    
    
    
        debug
    
  
  
  
    
      关于程序当前状态的报告消息
    
    
    
        info
    
  
  
  
    
      程序运行中产生了值得注意的事件
    
    
    
        notice
    
  
  
  
    
      程序中存在潜在问题的警告信息
    
    
    
        waring
    
  
  
  
    
      程序存在错误的通告
    
    
    
        err
    
  
  
  
    
      错误消息，可能会导致程序关闭的事件
    
    
    
        crit
    
  
  
  
    
      严重错误消息，会导致程序关闭并可能影响其他程序
    
    
    
        alert
    
  
  
  
    
      发生严重事件，并有导致系统崩溃的潜在危险
    
    
    
        emerg
    
  


简单动作大概如下: 

将消息写入某终端，该终端可以为从/dev/tty1到/dev/tty6的标准终端名，也可以为控制台设备，比如/dev/console。

将消息写入到指定用户列表中当前已登录用户的计算机屏幕。

将消息写入远程系统上的日志文件，这是通过在动作中使用符号@实现的。

下面给出一些例子: 
  
    #vi /etc/syslog.conf 
    
    
      authpriv.*                                      /var/log/secure
  

将私有用户验证的消息对于任何优先级写入/var/log/messages.
  
    *.info ;main.none ;authpriv.none                    /var/log/messages
  

匹配来自任何设备并且优先级为info (或更高) 的消息，但来自mail的所有消息都被排除。

最后，在对syslog.conf修改完成后，记得通知syslogd和klogd重新读取该配置文件。
  
    #service syslog restart
  
  
    不同发行版的进程名, 配置文件名称可能不同, Debian 6 的配置文件是/etc/rsyslog.conf, 进程名是rsyslogd.
  
