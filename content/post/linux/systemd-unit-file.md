---
title: systemd script, systemd unit, 启动脚本
author: "-"
date: 2018-02-23T07:17:35+00:00
url: systemd/script
categories:
  - Linux
tags:
  - reprint
  - remix

---
## systemd script, systemd unit, 启动脚本

## service unit 配置文件 template

```Bash
vim /etc/systemd/system/foo.service
```

```Bash
[Unit]
Description=start proxy
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/proxy.sh
RemainAfterExit=true

[Install]
WantedBy=multi-user.target
```

```Bash
[Unit]
# 服务启动时会在 journal 里打印 description0
Description=description0
After=network.target sshd-keygen.service

[Service]
# 脚本路径必须是绝对路径 /bin/sh 为 shell 解释器不能省
ExecStart=/bin/sh /usr/local/bin/shell-script0.sh
Environment="GODEBUG='gctrace=1'"
Environment="ANOTHER_SECRET=JP8YLOc2bsNlrGuD6LVTq7L36obpjzxd"

[Install]
WantedBy=multi-user.target

# 在哪个服务后面启动 (如依赖的服务)
Requires=pulseaudio.service
# 在哪个服务后面启动 (如依赖的服务)
After=pulseaudio.service
```

- [Unit] 启动顺序与依赖关系
  - After 字段: 表示如果 network.target 或 sshd-keygen.service 需要启动, 那么 foo.service 应该在它们之后启动。
  - 相应地,还有一个 Before 字段, 定义 foo.service 应该在哪些服务之前启动。
  - 注意, After 和 Before 字段只涉及启动顺序,不涉及依赖关系。
  - ConditionPathExists, AssertPathExists: 要求给定的绝对路径文件已经存在，否则不做任何事(condition)或进入failed状态(assert)，可在路径前使用!表示条件取反，即不存在时才启动服务。
  - ConditionPathIsDirectory, AssertPathIsDirectory: 如上，路径存在且是目录时启动。
  - StartLimitIntervalSec=400
  - StartLimitBurst=3
- [Service] 区块
  - 用来 Service 的配置，只有 Service 类型的 Unit 才有这个区块。它的主要字段如下
  - Type：定义启动时的进程行为。它有以下几种值。
    - Type=simple：默认值，执行ExecStart指定的命令，启动主进程
    - Type=forking：以 fork 方式从父进程创建子进程，创建后父进程会立即退出
    - Type=oneshot：一次性进程，Systemd 会等当前服务退出，再继续往下执行
    - Type=dbus：当前服务通过D-Bus启动
    - Type=notify：当前服务启动完毕，会通知Systemd，再继续往下执行
    - Type=idle：若有其他任务执行完毕，当前服务才会运行
  - ExecStart：服务启动时要执行的命令
  - ExecStartPre：启动当前服务之前执行的命令
  - ExecStartPost：启动当前服务之后执行的命令
  - ExecReload：重启当前服务时执行的命令
  - ExecStop：停止当前服务时执行的命令
  - ExecStopPost：停止当其服务之后执行的命令
  - RestartSec：自动重启当前服务间隔的秒数
  - Restart：定义何种情况 Systemd 会自动重启当前服务，no, on-success, on-failure, on-abnormal, on-watchdog, on-abort, or always， 默认值: no
  - TimeoutSec：定义 Systemd 停止当前服务之前等待的秒数
  - Environment：指定环境变量
  - EnvironmentFile: 指定文件，可定义多个环境变量，按分行方式存储。
  - WorkingDirectory, 工作目录, 程序启动时的当前目录。如果使用到 workingdirectory，需要先创建该目录
- [Install] 段落相关的指令，它们只在systemctl enable/disable操作时有效。如果期望服务开机自启动，一般只配置一个WantedBy指令，如果不期望服务开机自启动，则Install段落通常省略。主要包含以下内容:
  - WantedBy 本服务设置开机自启动时，在被依赖目标的.wants目录下创建本服务的软链接。例如WantedBy = multi-user.target时，将在/etc/systemd/multi-user.target.wants目录下创建本服务的软链接。
  - RequiredBy	类似WantedBy，但是是在.requires目录下创建软链接。
  - Alias	指定创建软链接时链接至本服务配置文件的别名文件。例如reboot.target中配置了Alias=ctrl-alt-del.target，当执行enable时，将创建/etc/systemd/system/ctrl-alt-del.service软链接并指向reboot.target。
  - DefaultInstance	当是一个模板服务配置文件时(即文件名为Service_Name@.service)，该指令指定该模板的默认实例。例如trojan@.service中配置了DefaultInstall=server时，systemctl enable trojan@.service时将创建名为trojan@server.service的软链接。

可以通过以下两个选项来设置服务启动的频率：

StartLimitIntervalSec=, StartLimitBurst=

设置单元的启动频率限制。  StartLimitIntervalSec= 用于设置时长， 默认值等于 DefaultStartLimitIntervalSec= 的值(默认为10秒)，设为 0 表示不作限制。

StartLimitBurst= 用于设置在一段给定的时长内，最多允许启动多少次， 默认值等于 DefaultStartLimitBurst= 的值(默认为5次)。 虽然此选项通常与 Restart= (参见 systemd.service(5)) 一起使用， 但实际上，此选项作用于任何方式的启动(包括手动启动)， 而不仅仅是由 Restart= 触发的启动。

注意，一旦某个设置了 Restart= 自动重启逻辑的单元触碰到了启动频率限制，那么该单元将再也不会尝试自动重启； 不过，如果该单元后来又被手动重启成功的话，那么该单元的自动重启逻辑将会被再次激活。 注意，systemctl reset-failed 命令能够重置单元的启动频率计数器。 系统管理员在手动启动某个已经触碰到了启动频率限制的单元之前，可以使用这个命令清除启动限制。 注意，因为启动频率限制位于所有单元条件检查之后，所以基于失败条件的启动不会计入启动频率限制的启动次数之中。 注意， slice, target, device, scope 单元不受此选项的影响， 因为这几种单元要么永远不会启动失败、要么只能成功启动一次。

>注意:
>脚本里的命令必须是绝对路径
>ExecStart 命令行参数, ExecStart 执行的命令有参数时, 不要把可执行文件的路径和参数放在双引号里, ExecStart 会把参数 当作路径 的一部分, 然后报错说找不到文件.

设置开机启动

`systemctl enable foo.service`

## Golang binary

Unit File (systemd) for Golang binary

```Bash
vim /etc/systemd/system/foo.service
```

file content

```bash
[Unit]
Description=foo

[Service]
WorkingDirectory=/data/foo
ExecStart=/data/foo/foo -key0=value0
User=root
Group=root
Type=simple
Restart=on-failure
RestartSec=10
LimitNOFILE=100000

[Install]
WantedBy=multi-user.target
```

[https://vincent.bernat.im/en/blog/2017-systemd-golang](https://vincent.bernat.im/en/blog/2017-systemd-golang)

[https://serversforhackers.com/c/process-monitoring-with-systemd](https://serversforhackers.com/c/process-monitoring-with-systemd)

[https://fabianlee.org/2017/05/21/golang-running-a-go-binary-as-a-systemd-service-on-ubuntu-16-04/](https://fabianlee.org/2017/05/21/golang-running-a-go-binary-as-a-systemd-service-on-ubuntu-16-04/)

[http://shanks.leanote.com/post/Go%E5%88%9B%E5%BB%BAdaemon%E7%A8%8B%E5%BA%8F](http://shanks.leanote.com/post/Go%E5%88%9B%E5%BB%BAdaemon%E7%A8%8B%E5%BA%8F)

## java

```Bash
vim /etc/systemd/system/foo.service
```

```bash
[Unit]
Description=description0
After=network.target syslog.target

[Service]
User=root
PrivateTmp=true
Restart=on-failure
RestartSec=10
Type=simple
WorkingDirectory=/home/exc-led/uploader
ExecStart=/usr/java/jre1.8.0_201-amd64/bin/java -Xmx1024m -jar /data/server/service0/service0.jar
ExecStop=/usr/bin/kill -15 $MAINPID

[Install]
WantedBy=multi-user.target
```

[https://xie.infoq.cn/article/2de71d4489a44ae58b6cef4d0](https://xie.infoq.cn/article/2de71d4489a44ae58b6cef4d0)

## systemd service, shell 脚本

```Bash
vim /etc/systemd/system/foo.service
```

内容如下

```bash
[Unit]
Description=description0
AssertPathIsDirectory=/mnt/drive_wiloon
After=docker.service

[Service]
Type=simple
ExecStart=/bin/sh /usr/local/bin/shell-script0.sh
ExecStop=/bin/sh /usr/local/bin/shell-script1.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
Requires=pulseaudio.service
After=pulseaudio.service
```

[http://lxiaogao.lofter.com/post/1cc6a101_62292d3](http://lxiaogao.lofter.com/post/1cc6a101_62292d3)

## systemd service mount rclone drive

```bash
vim /usr/lib/systemd/system/foo.service
```

```bash
[Unit]
Description=description0
AssertPathIsDirectory=/mnt/drive_wiloon
After=docker.service

[Service]
Type=simple
ExecStart=/data/rclone/mount-keepass-db.sh
ExecStop=/bin/fusermount -u /mnt/drive_wiloon
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
```

```bash
vim /usr/lib/systemd/system/foo.service

# ---

# Systemd unit file for default tomcat
#
# To create clones of this service:
# DO NOTHING, use tomcat@.service instead.

[Unit]
Description=Apache Tomcat Web Application Container
After=syslog.target network.target

[Service]
Type=simple
EnvironmentFile=/etc/tomcat/tomcat.conf
Environment="NAME="
EnvironmentFile=-/etc/sysconfig/tomcat
ExecStart=/usr/libexec/tomcat/server start
SuccessExitStatus=143
User=tomcat
Group=tomcat
Restart=always

[Install]
WantedBy=multi-user.target
```

## zookeeper

```bash
[Unit]
Description=zookeeper
After=syslog.target network.target

[Service]
Type=forking
ExecStart=/data/server/zookeeper/zookeeper-3.4.12/bin/zkServer.sh start
ExecStop=/data/server/zookeeper/zookeeper-3.4.12/bin/zkServer.sh stop

[Install]
WantedBy=multi-user.target
```

## The mappings of systemd limits to ulimit

```bash
Directive        ulimit equivalent     Unit
LimitCPU=        ulimit -t             Seconds      
LimitFSIZE=      ulimit -f             Bytes
LimitDATA=       ulimit -d             Bytes
LimitSTACK=      ulimit -s             Bytes
LimitCORE=       ulimit -c             Bytes
LimitRSS=        ulimit -m             Bytes
LimitNOFILE=     ulimit -n             Number of File Descriptors 
LimitAS=         ulimit -v             Bytes
LimitNPROC=      ulimit -u             Number of Processes 
LimitMEMLOCK=    ulimit -l             Bytes
LimitLOCKS=      ulimit -x             Number of Locks 
LimitSIGPENDING= ulimit -i             Number of Queued Signals 
LimitMSGQUEUE=   ulimit -q             Bytes
LimitNICE=       ulimit -e             Nice Level 
LimitRTPRIO=     ulimit -r             Realtime Priority  
LimitRTTIME=     No equivalent
```

编写systemd下服务脚本
  
Red Hat Enterprise Linux 7 (RHEL 7) 已经将服务管理工具从SysVinit和Upstart迁移到了systemd上,相应的服务脚本也需要改变。前面的版本里,所有的启动脚本都是放在/etc/rc.d/init.d/ 目录下。这些脚本都是bash脚本,可以让系统管理员控制这些服务的状态,通常,这些脚本中包含了start,stop,restart这些方法,以提供系统自动调用这些方法。但是在RHEL 7中当中已经完全摒弃了这种方法,而采用了一种叫unit的配置文件来管理服务。

Systemd下的unit文件
  
Unit文件专门用于systemd下控制资源,这些资源包括服务(service)、 socket (socket)、设备(device)、挂载点(mount point)、自动挂载点(automount point)、交换文件或分区(a swap file or partition)…
  
所有的unit文件都应该配置[Unit]或者[Install]段.由于通用的信息在[Unit]和[Install]中描述,每一个unit应该有一个指定类型段,例如[Service]来对应后台服务类型unit.

### unit 类型如下

service : 守护进程的启动、停止、重启和重载是此类 unit 中最为明显的几个类型。
  
socket : 此类 unit 封装系统和互联网中的一个 socket。当下, systemd支持流式,数据报和连续包的 AF_INET,AF_INET6,AF_UNIX socket 也支持传统的 FIFOs 传输模式。每一个 socket unit 都有一个相应的服务 unit 。相应的服务在第一个"连接"进入 socket 或 FIFO 时就会启动 (例如: nscd.socket 在有新连接后便启动 nscd.service)。

device : 此类 unit 封装一个存在于 Linux设备树中的设备。每一个使用 udev 规则标记的设备都将会在 systemd 中作为一个设备 unit 出现。udev 的属性设置可以作为配置设备 unit 依赖关系的配置源。

mount : 此类 unit 封装系统结构层次中的一个挂载点。
  
automount : 此类 unit 封装系统结构层次中的一个自挂载点。每一个自挂载 unit 对应一个已挂载的挂载 unit (需要在自挂载目录可以存取的情况下尽早挂载)。
  
target : 此类 unit 为其他 unit 进行逻辑分组。它们本身实际上并不做什么,只是引用其他 unit 而已。这样便可以对 unit 做一个统一的控制。(例如: multi-user.target 相当于在传统使用 SysV 的系统中运行级别5)；bluetooth.target 只有在蓝牙适配器可用的情况下才调用与蓝牙相关的服务,如: bluetooth 守护进程、obex 守护进程等)

snapshot : 与 targetunit 相似,快照本身不做什么,唯一的目的就是引用其他 unit 。

认识service的unit文件
  
扩展名: .service

路径:

- /etc/systemd/system/*     ――――  供系统管理员和用户使用
- /run/systemd/system/*     ――――  运行时配置文件
- /usr/lib/systemd/system/*   ――――  安装程序使用 (如RPM包安装)

- After    本服务在哪些服务启动之后启动，仅定义启动顺序，不定义服务依赖关系，即使要求先启动的服务启动失败，本服务也依然会启动
- ConditionPathExists, AssertPathExists    要求给定的绝对路径文件已经存在，否则不做任何事(condition)或进入failed状态(assert)，可在路径前使用!表示条件取反，即不存在时才启动服务。
- ConditionPathIsDirectory, AssertPathIsDirectory    如上，路径存在且是目录时启动。

作者: 骏马金龙
链接: [https://www.junmajinlong.com/linux/systemd/service_1/](https://www.junmajinlong.com/linux/systemd/service_1/)
来源: 骏马金龙
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

以下是一段service unit文件的例子,属于/usr/lib/systemd/system/NetworkManager.service文件,它描述的是系统中的网络管理服务。

```Bash
[Unit]

Description=Network Manager

Wants=network.target

Before=network.target network.service

[Service]

Type=dbus

BusName=org.freedesktop.NetworkManager

ExecStart=/usr/sbin/NetworkManager -no-daemon

NM doesn't want systemd to kill its children for it

KillMode=process

[Install]

WantedBy=multi-user.target

Alias=dbus-org.freedesktop.NetworkManager.service

Also=NetworkManager-dispatcher.service
```

整个文件分三个部分

- `[Unit]`: 记录unit文件的通用信息。
- `[Service]`: 记录Service的信息
- `[Install]`: 安装信息。

### Unit 主要包含以下内容

- Description: 对本service的描述。
- Before, After: 定义启动顺序,Before=xxx.service,代表本服务在xxx.service启动之前启动。After=xxx.service,代表本服务在xxx之后启动。
- After, 与 Requires 相似，但会在后面列出的所有模块全部启动完成以后，才会启动当前的服务。After和Before字段只涉及启动顺序，不涉及依赖关系。
- Requires: 这个 unit 启动了, 那么它 "需要(Requires)" 的 unit 也会被启动; 它"需要"的单元被停止了, 它自己也活不了。但是请注意, 这个设定并不能控制某单元与它"需要"的单元的启动顺序 (启动顺序是另外控制的) , 即 Systemd 不是先启动 Requires 再启动本单元, 而是在本单元被激活时, 并行启动两者。
  于是会产生争分夺秒的问题, 如果 Requires 先启动成功,那么皆大欢喜; 如果 Requires 启动得慢,那本单元就会失败 (Systemd 没有自动重试) 。所以为了系统的健壮性,不建议使用这个标记,而建议使用 Wants 标记。可以使用多个 Requires。
- RequiresOverridable: 跟 Requires 很像。但是如果这条服务是由用户手动启动的,那么 RequiresOverridable 后面的服务即使启动不成功也不报错。跟 Requires 比增加了一定容错性,但是你要确定你的服务是有等待功能的。另外,如果不由用户手动启动而是随系统开机启动,那么依然会有 Requires 面临的问题。
- Requisite: 强势版本的 Requires。要是这里需要的服务启动不成功,那本单元文件不管能不能检测等不能等待都立刻就会失败。
- Wants: 推荐使用。本单元启动了,它"想要"的单元也会被启动。但是启动不成功,对本单元没有影响。
- Conflicts: 一个单元的启动会停止与它"冲突"的单元,反之亦然。

### Service 主要包含以下内容

- Type: service的种类,包含下列几种类型:
  - simple 默认,这是最简单的服务类型。意思就是说启动的程序就是主体程序,这个程序要是退出那么一切都退出。Type=simple类型的服务只适合那些在shell下运行在前台的命令。也就是说，当一个命令本身会以daemon模式运行时，将不能使用simple，而应该使用Type=forking。
  - forking 标准 Unix Daemon 使用的启动方式。启动程序后会调用 fork() 函数,把必要的通信频道都设置好之后父进程退出,留下守护精灵的子进程
  - oneshot种服务类型就是启动,完成,没进程了。

notify,idle类型比较少见,不介绍。

- ExecStart: 服务启动时执行的命令,通常此命令就是服务的主体。

------如果你服务的类型不是 oneshot,那么它只可以接受一个命令,参数不限。

------多个命令用分号隔开,多行用 \ 跨行。

- ExecStartPre, ExecStartPost: ExecStart执行前后所调用的命令。
- ExecStop: 定义停止服务时所执行的命令,定义服务退出前所做的处理。如果没有指定,使用systemctl stop xxx命令时,服务将立即被终结而不做处理。如果未设置此选项，那么当此服务被停止时， 该服务的所有进程都将会根据 KillSignal= 的设置被立即全部杀死。
- SuccessExitStatus: 参考ExecStart中返回值,定义何种情况算是启动成功。

eg: SuccessExitStatus=1 2 8 SIGKILL



- Alias: 别名

multi-user.target

systemd有一个默认target，即multi-user.target，Linux系统启动后即处于该默认target的状态。

旧的命令与systemd命令的映射
  
service systemctl Description

service name start --> systemctl start name.service ●Starts a service.

service name stop --> systemctl stopname.service ●Stops a service.

service name restart --> systemctl restartname.service ●Restarts a service.

service name condrestart -->

systemctl try-restart name.service ●Restarts a service only if it is running.

service name reload --> systemctl reloadname.serviceReloads configuration.

service name status --> systemctl status name.service

systemctl is-active name.service

●Checks if a service isrunning.

service -status-all --> systemctl list-units –type service -all

●Displays the status of all services.chkconfig systemctl

chkconfig name on --> systemctl enablename.service ●Enables a service.

chkconfig name off --> systemctl disablename.service ●Disables a service.

chkconfig -list name --> systemctl statusname.service

system ctl is-enabled name.service

●Checks if a service is enabled.

chkconfig -list --> systemctl list-unit-files –type service

●Lists all services and checks if they are enabled.

■创建自己的systemd服务
  
弄清了unit文件的各项意义,我们可以尝试编写自己的服务,与以前用SysV来编写服务相比,整个过程比较简单。unit文件有着简洁的特点,是以前臃肿的脚本所不能比的。

在本例中,尝试写一个命名为my-demo.service的服务,整个服务很简单: 在开机的时候将服务启动时的时间写到一个文件当中。可以通过这个小小的例子来说明整个服务的创建过程。

Step1: 编写属于自己的unit文件,命令为my-demo.service,整个文件如下:

[Unit]

Description=My-demo Service

[Service]

Type=oneshot

ExecStart=/bin/bash /root/test.sh

StandardOutput=syslog

StandardError=inherit

[Install]

WantedBy=multi-user.target

Step2: 将上述的文件拷贝到RHEL 7系统中/usr/lib/systemd/system/*目录下

Step3: 编写unit文件中ExecStart=/bin/bash /root/test.sh所定义的test.sh文件,将其放在定义的目录当中,此文件是服务的执行主体。文件内容如下:

```bash
# !/bin/bash
date >> /tmp/date
```

Step4: 将my-demo.service注册到系统当中执行命令:

```bash
systemctl enable my-demo.service
```

输出: ln -s'/usr/lib/systemd/system/my-demo.service' '/etc/systemd/system/multi-user.target.wants/my-demo.service'

输出表明,注册的过程实际上就是将服务链接到/etc/systemd/system/目录下。

至此服务已经创建完成。重新启动系统,会发现/tmp/date文件已经生成,服务在开机时启动成功。当然本例当中的test.sh文件可以换成任意的可执行文件作为服务的主体,这样就可以实现各种各样的功能。

[http://www.jinbuguo.com/systemd/systemd.service.html](http://www.jinbuguo.com/systemd/systemd.service.html)
  
[https://blog.csdn.net/fu_wayne/article/details/38018825](https://blog.csdn.net/fu_wayne/article/details/38018825)

systemctl开机启动zookeeper
  
[https://www.pocketdigi.com/20180131/1593.html/embed#?secret=rpemgAP8dW](https://www.pocketdigi.com/20180131/1593.html/embed#?secret=rpemgAP8dW)
>[https://www.junmajinlong.com/linux/systemd/service_2/](https://www.junmajinlong.com/linux/systemd/service_2/)

```bash
#!/bin/sh
service_name="foo"
echo "
[Unit]
Description=${service_name}
[Service]
WorkingDirectory=/data/${service_name}
ExecStart=/data/${service_name}/${service_name}
User=root
Type=simple
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
" > /etc/systemd/system/${service_name}.service

systemctl daemon-reload
systemctl enable ${service_name}

echo "commands:
systemctl start ${service_name}
systemctl status ${service_name}
systemctl stop ${service_name}
"
```
