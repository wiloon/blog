---
title: systemd, systemctl basic, command
author: "-"
date: 2015-05-04T00:34:26+00:00
url: systemd

---
## systemd, systemctl basic, command
Systemd 是 Linux 系统中最新的初始化系统（init），它主要的设计目标是克服 sysvinit 固有的缺点，提高系统的启动速度
### Systemd新特性：
- 系统引导时实现服务并行启动
- 按需启动守护进程
- 自动化的服务依赖关系管理
- 同时采用socket式与D-Bus总线式激活服务
- 系统状态快照  
### 查看配置文件位置
    systemctl status service0

配置文件主要放在/usr/lib/systemd/system 目录,也可能在/etc/systemd/system目录

### 配置文件
####  [Unit] 区块: 启动顺序与依赖关系。
After字段: 表示如果network.target或sshd-keygen.service需要启动,那么sshd.service应该在它们之后启动。

相应地,还有一个Before字段,定义sshd.service应该在哪些服务之前启动。

注意,After和Before字段只涉及启动顺序,不涉及依赖关系。

### systemd-analyze
# 查看启动耗时
    $ systemd-analyze
    
    # 查看每个服务的启动耗时
    systemd-analyze blame

    # 显示瀑布状的启动过程流
    $ systemd-analyze critical-chain

    # 显示指定服务的启动流
    $ systemd-analyze critical-chain atd.service

    systemctl --version
    # 生成一张启动详细信息矢量图, .svg可以用chrome打开
    sudo systemd-analyze plot > /home/wiloon/tmp/boot3.svg

### hostnamectl
    # 显示当前主机的信息
    $ hostnamectl

    # 设置主机名。
    $ sudo hostnamectl set-hostname rhel7

### timedatectl
    # 查看当前时区设置
    $ timedatectl

    # 显示所有可用的时区
    $ timedatectl list-timezones                                                                                  
    # 设置当前时区
    $ sudo timedatectl set-timezone America/New_York
    $ sudo timedatectl set-time YYYY-MM-DD
    $ sudo timedatectl set-time HH:MM:SS

### loginctl
    # 列出当前session
    $ loginctl list-sessions

    # 列出当前登录用户
    $ loginctl list-users

    # 列出显示指定用户的信息
    $ loginctl show-user ruanyf

### cat
    systemctl cat bluetooth|grep Condition

### mask
```bash
systemctl mask service0
systemctl unmask service0
```

### check the boot performance
```bash
systemd-analyze blame
systemctl list-timers --all
```

```bash
# to see which units have failed.
systemctl --failed

# 退出系统并关闭电源: 
systemctl poweroff
systemctl reboot
# CPU停止工作
$ sudo systemctl halt
# 待机: 
systemctl suspend
systemctl hibernate
# 混合休眠模式（同时休眠到硬盘并待机) : 
systemctl hybrid-sleep

# list all service
systemctl
systemctl list-unit-files | grep enabled

systemctl is-enabled SERVICE

显示所有已启动的服务
systemctl list-units --type=service

systemctl is-active httpd.service （仅显示是否 Active)

systemctl daemon-reload

# check service enabled
systemctl list-unit-files |grep enabled
查看服务是否开机启动: systemctl is-enabled service0.service
在开机时禁用一个服务: systemctl disable service0.service

journalctl -f
systemd-analyze blame

systemctl --type=service
systemctl status xxx
```

### systemctl status
    Loaded行: 配置文件的位置,是否设为开机启动
    Active行: 表示正在运行
    Main PID行: 主进程ID
    Status行: 由应用本身（这里是 httpd ) 提供的软件当前状态
    CGroup块: 应用的所有子进程
    日志块: 应用的日志

http://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-commands.html

### Unit
Systemd 可以管理所有系统资源。不同的资源统称为 Unit（单位) 。
Unit 一共分成12种。

    Service unit: 系统服务
    Target unit: 多个 Unit 构成的一个组
    Device Unit: 硬件设备
    Mount Unit: 文件系统的挂载点
    Automount Unit: 自动挂载点
    Path Unit: 文件或路径
    Scope Unit: 不是由 Systemd 启动的外部进程
    Slice Unit: 进程组
    Snapshot Unit: Systemd 快照,可以切回某个快照
    Socket Unit: 进程间通信的 socket
    Swap Unit: swap 文件
    Timer Unit: 定时器

### systemctl list-units
    # 列出正在运行的 Unit
    $ systemctl list-units

    # 列出所有Unit,包括没有找到配置文件的或者启动失败的
    $ systemctl list-units --all

    # 列出所有没有运行的 Unit
    $ systemctl list-units --all --state=inactive

    # 列出所有加载失败的 Unit
    $ systemctl list-units --failed

    # 列出所有正在运行的、类型为 service 的 Unit
    $ systemctl list-units --type=service

### Unit 管理

    # 立即启动一个服务
    $ sudo systemctl start apache.service

    # 立即停止一个服务
    $ sudo systemctl stop apache.service

    # 重启一个服务
    $ sudo systemctl restart apache.service

    # 杀死一个服务的所有子进程
    $ sudo systemctl kill apache.service

    # 重新加载一个服务的配置文件
    $ sudo systemctl reload apache.service

    # 重载所有修改过的配置文件
    $ sudo systemctl daemon-reload

    # 显示某个 Unit 的所有底层参数
    $ systemctl show httpd.service

    # 显示某个 Unit 的指定属性的值
    $ systemctl show -p CPUShares httpd.service

    # 设置某个 Unit 的指定属性
    $ sudo systemctl set-property httpd.service CPUShares=500

### 依赖关系
 systemctl list-dependencies nginx.service
 systemctl list-dependencies --all nginx.service

 ### 
 /etc/systemd/system/
 /usr/lib/systemd/system/
 /etc/systemd/system/multi-user.target.wants/v2ray.service

### systemctl mask和systemctl disable
systemctl mask和systemctl disable的区别一般很难注意到，因为我大部分时候只会使用systemctl disable，并不会用到systemctl mask。在一次遇到问题的时候，需要使用systemctl mask来禁用服务，下边具体说明。

systemctl enable的作用
我们知道，在系统中安装了某个服务以后，需要将该服务设置为开机自启，那么一般会执行systemctl enable xxx，这个时候会发现shell中会输出两行提示，一般类似如下：
[root@NameNode01 system]# systemctl enable NetworkManager 
Created symlink from /etc/systemd/system/multi-user.target.wants/NetworkManager.service to /usr/lib/systemd/system/NetworkManager.service.
Created symlink from /etc/systemd/system/dbus-org.freedesktop.nm-dispatcher.service to /usr/lib/systemd/system/NetworkManager-dispatcher.service.
Created symlink from /etc/systemd/system/network-online.target.wants/NetworkManager-wait-online.service to /usr/lib/systemd/system/NetworkManager-wait-online.service.
1
2
3
4
这个命令会在/etc/systemd/system/目录下创建需要的符号链接，表示服务需要进行启动。通过stdout输出的信息可以看到，软连接实际指向的文件为/usr/lib/systemd/system/目录中的文件，实际起作用的也是这个目录中的文件。
systemctl disable xxx的作用
执行systemctl disable xxx后，会禁用这个服务。它实现的方法是将服务对应的软连接从/etc/systemd/system中删除。命令执行情况一般类似如下：
[root@NameNode01 system]# systemctl disable NetworkManager
Removed symlink /etc/systemd/system/multi-user.target.wants/NetworkManager.service.
Removed symlink /etc/systemd/system/dbus-org.freedesktop.NetworkManager.service.
Removed symlink /etc/systemd/system/dbus-org.freedesktop.nm-dispatcher.service.
Removed symlink /etc/systemd/system/network-online.target.wants/NetworkManager-wait-online.service.
1
2
3
4
5
在执行systemctl disable xxx的时候，实际只是删除了软连接，并不会产生其他影响。
systemctl mask xxx的作用
执行 systemctl mask xxx会屏蔽这个服务。它和systemctl disable xxx的区别在于，前者只是删除了符号链接，后者会建立一个指向/dev/null的符号链接，这样，即使有其他服务要启动被mask的服务，仍然无法执行成功。执行该命令的效果一般类似如下：
[root@NameNode01 system]# systemctl mask NetworkManager 
Created symlink from /etc/systemd/system/NetworkManager.service to /dev/null.
1
2
systemctl mask xxx和systemctl disable xxx的区别
在执行过mask后，如果想要启动服务，那么会报类似如下错误：
[root@NameNode01 system]# systemctl start NetworkManager
Failed to start NetworkManager.service: Unit is masked.
1
2
如果使用disable的话，可以正常启动服务。总体来看，disable和enable是一对操作，是用来启动、停止服务。
使用systemctl unmask xxx取消屏蔽
如果使用了mask，要想重新启动服务，必须先执行unmask将服务取消屏蔽。mask和unmask是一对操作，用来屏蔽和取消屏蔽服务。
————————————————
版权声明：本文为CSDN博主「stpice」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/stpice/article/details/104569146

---

https://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-part-two.html
https://www.cnblogs.com/xingmuxin/p/11413784.html
>https://blog.csdn.net/stpice/article/details/104569146