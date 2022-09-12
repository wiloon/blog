---
title: systemd, systemctl basic, command
author: "-"
date: 2015-05-04T00:34:26+00:00
url: systemd
categories:
  - Linux
tags:
  - reprint
---
## systemd, systemctl basic, command

Systemd 是 Linux 系统中最新的初始化系统 (init），它主要的设计目标是克服 sysvinit 固有的缺点，提高系统的启动速度

## --now

```bash
# enable and start service0
systemctl --now enable service0

```

### Systemd 新特性

- 系统引导时实现服务并行启动
- 按需启动守护进程
- 自动化的服务依赖关系管理
- 同时采用socket式与D-Bus总线式激活服务
- 系统状态快照

### 查看配置文件位置

```bash
systemctl status service0
```

配置文件主要放在 /usr/lib/systemd/system 目录, 也可能在/etc/systemd/system 目录

- /lib/systemd/system：系统默认的单元文件
- /etc/systemd/system：用户安装的软件的单元文件
- /usr/lib/systemd/system：用户自己定义的单元文件

### 配置文件

#### [Unit]: 启动顺序与依赖关系

After字段: 表示如果network.target或sshd-keygen.service需要启动,那么sshd.service应该在它们之后启动。

相应地,还有一个Before字段,定义sshd.service应该在哪些服务之前启动。

注意,After和Before字段只涉及启动顺序,不涉及依赖关系。

## [Service]区块

用来 Service 的配置，只有 Service 类型的 Unit 才有这个区块。它的主要字段如下

Type：定义启动时的进程行为。它有以下几种值。
Type=simple：默认值，执行ExecStart指定的命令，启动主进程
Type=forking：以 fork 方式从父进程创建子进程，创建后父进程会立即退出
Type=oneshot：一次性进程，Systemd 会等当前服务退出，再继续往下执行
Type=dbus：当前服务通过D-Bus启动
Type=notify：当前服务启动完毕，会通知Systemd，再继续往下执行
Type=idle：若有其他任务执行完毕，当前服务才会运行
ExecStart：启动当前服务的命令
ExecStartPre：启动当前服务之前执行的命令
ExecStartPost：启动当前服务之后执行的命令
ExecReload：重启当前服务时执行的命令
ExecStop：停止当前服务时执行的命令
ExecStopPost：停止当其服务之后执行的命令
RestartSec：自动重启当前服务间隔的秒数
Restart：定义何种情况 Systemd 会自动重启当前服务，可能的值包括always（总是重启）、on-success、on-failure、on-abnormal、on-abort、on-watchdog
TimeoutSec：定义 Systemd 停止当前服务之前等待的秒数
Environment：指定环境变量
EnvironmentFile: 指定文件，可定义多个环境变量，按分行方式存储。
————————————————
版权声明：本文为CSDN博主「Golden_Chen」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：<https://blog.csdn.net/Golden_Chen/article/details/114689804>

### Environment, 环境变量

```f
[Service]
Environment="GODEBUG='gctrace=1'"
Environment="ANOTHER_SECRET=JP8YLOc2bsNlrGuD6LVTq7L36obpjzxd"
```

### systemd-analyze

查看启动耗时

```bash
    $ systemd-analyze
    
    # 查看每个服务的启动耗时
    systemd-analyze blame

    # 显示瀑布状的启动过程流
    $ systemd-analyze critical-chain

    # 显示指定服务的启动流
    $ systemd-analyze critical-chain atd.service
```

## systemd 版本/version

```bash
    systemctl --version

    # 生成一张启动详细信息矢量图, .svg可以用chrome打开
    sudo systemd-analyze plot > /home/wiloon/tmp/boot3.svg
```

### timedatectl

```bash
# 查看当前时区设置
$ timedatectl

# 显示所有可用的时区
$ timedatectl list-timezones                                                                                  
# 设置当前时区
$ sudo timedatectl set-timezone America/New_York
$ sudo timedatectl set-time YYYY-MM-DD
$ sudo timedatectl set-time HH:MM:SS
## timedatectl ntp
timedatectl set-ntp true
```

### loginctl

```bash
    # 列出当前session
    $ loginctl list-sessions

    # 列出当前登录用户
    $ loginctl list-users

    # 列出显示指定用户的信息
    $ loginctl show-user ruanyf

    ## 查看 session 类型, x or wayland
    loginctl show-session <SESSION_ID> -p Type
```

### cat

```bash
    systemctl cat bluetooth|grep Condition
```

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

# 查看是否启用
systemctl is-enabled service0

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
# 混合休眠模式 (同时休眠到硬盘并待机) : 
systemctl hybrid-sleep

# list all service
systemctl
systemctl list-unit-files | grep enabled

# 查看所有单元
$ systemctl list-unit-files

# 查看所有 Service 单元
$ systemctl list-unit-files --type service

# 查看所有 Timer 单元
$ systemctl list-unit-files --type timer

显示所有已启动的服务
systemctl list-units --type=service

systemctl is-active httpd.service  (仅显示是否 Active)

systemctl daemon-reload

# check service enabled
systemctl list-unit-files |grep enabled
# 查看服务是否开机启动
systemctl is-enabled foo.service
# 禁止 foo.service 开机启动
systemctl disable foo.service
# 禁止 foo.service 开机启动， 同时停掉服务
systemctl --now disable foo.service

journalctl -f
systemd-analyze blame

systemctl --type=service
systemctl status xxx
```

### systemctl status

```bash
    Loaded行: 配置文件的位置,是否设为开机启动
    Active行: 表示正在运行
    Main PID行: 主进程ID
    Status行: 由应用本身 (这里是 httpd ) 提供的软件当前状态
    CGroup块: 应用的所有子进程
    日志块: 应用的日志
```

```bash
# 打印完整的控制台日志, 不加 -l 的话, 默认会截断.
systemctl status service0 -l

```

<http://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-commands.html>

### Unit

Systemd 可以管理所有系统资源。不同的资源统称为 Unit (单位) 。
Unit 一共分成12种。

```bash
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
```

### systemctl list-units

```bash
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
```

### Unit 管理

```bash
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
```

### 依赖关系

 systemctl list-dependencies nginx.service
 systemctl list-dependencies --all nginx.service

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
这个命令会在/etc/systemd/system/目录下创建需要的符号链接，表示服务需要进行启动。通过 stdout 输出的信息可以看到，软连接实际指向的文件为/usr/lib/systemd/system/目录中的文件，实际起作用的也是这个目录中的文件。
systemctl disable xxx的作用
执行systemctl disable xxx后，会禁用这个服务。它实现的方法是将服务对应的软连接从/etc/systemd/system中删除。命令执行情况一般类似如下：
[root@NameNode01 system]# systemctl disable NetworkManager
Removed symlink /etc/systemd/system/multi-user.target.wants/NetworkManager.service.
Removed symlink /etc/systemd/system/dbus-org.freedesktop.NetworkManager.service.
Removed symlink /etc/systemd/system/dbus-org.freedesktop.nm-dispatcher.service.
Removed symlink /etc/systemd/system/network-online.target.wants/NetworkManager-wait-online.service.
在执行systemctl disable xxx的时候，实际只是删除了软连接，并不会产生其他影响。
systemctl mask xxx的作用
执行 systemctl mask xxx会屏蔽这个服务。它和systemctl disable xxx的区别在于，前者只是删除了符号链接，后者会建立一个指向/dev/null的符号链接，这样，即使有其他服务要启动被mask的服务，仍然无法执行成功。执行该命令的效果一般类似如下：
[root@NameNode01 system]# systemctl mask NetworkManager
Created symlink from /etc/systemd/system/NetworkManager.service to /dev/null.
systemctl mask xxx和systemctl disable xxx的区别
在执行过mask后，如果想要启动服务，那么会报类似如下错误：
[root@NameNode01 system]# systemctl start NetworkManager
Failed to start NetworkManager.service: Unit is masked.
如果使用disable的话，可以正常启动服务。总体来看，disable和enable是一对操作，是用来启动、停止服务。
使用systemctl unmask xxx取消屏蔽
如果使用了mask，要想重新启动服务，必须先执行unmask将服务取消屏蔽。mask和unmask是一对操作，用来屏蔽和取消屏蔽服务。
————————————————
版权声明：本文为CSDN博主「stpice」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：<https://blog.csdn.net/stpice/article/details/104569146>

---

<https://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-part-two.html>

<https://www.cnblogs.com/xingmuxin/p/11413784.html>

<https://blog.csdn.net/stpice/article/details/104569146>

### systemd 配置文件

1. 系统配置文件： /etc/systemd/system.conf
2. 用户配置文件： /etc/systemd/user.conf

systemd 用户实例不会继承类似 .bashrc 中定义的环境变量。systemd 用户实例有三种设置环境变量的方式：

对于有 $HOME 目录的用户，可以在 ~/.config/systemd/user.conf 文件中使用 DefaultEnvironment 选项，这些设置只对当前用户的用户单元有效。
在 /etc/systemd/user.conf 文件中使用 DefaultEnvironment 选项。这个配置在所有的用户单元中可见。
在 /etc/systemd/system/user@.service.d/ 下增加配置文件设置。 这个配置在所有的用户单元中可见。
在任何时候， 使用 systemctl --user set-environment 或 systemctl --user import-environment. 对设置之后启动的所有用户单元有效，但已经启动的用户单元不会生效。
提示： 如果想一次设置多个环境变量，可以写一个配置文件，文件里面每一行定义一个环境变量，用 "key=value" 的键值对表示，然后在你的启动脚本里添加xargs systemctl --user set-environment < /path/to/file.conf。
————————————————
版权声明：本文为CSDN博主「Golden_Chen」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：<https://blog.csdn.net/Golden_Chen/article/details/114689804>

## systemd资源控制

><https://www.cnblogs.com/jimbo17/p/9107052.html>
><https://documentation.suse.com/zh-cn/sles/15-SP2/html/SLES-all/cha-tuning-cgroups.html>

```bash
systemctl set-property user.slice MemoryAccounting=yes

```
