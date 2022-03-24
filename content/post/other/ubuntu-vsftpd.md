---
title: ubuntu vsftpd
author: "-"
date: 2012-05-25T14:59:25+00:00
url: /?p=3216
categories:
  - Linux

tags:
  - reprint
---
## ubuntu vsftpd
sudo apt-get install vsftpd

查看是否打开21端口
  
$ sudo netstat -npltu | grep 21

VSFTPD的菜鸟篇

作者: 龙磊

这是我这个菜鸟学习LINUX所写的第一篇文章，是比较基础的FTP架设的应用，如果我写有什么问题请大家多指教，我后续会陆续出进阶篇把FTP中各种详细的配置跟大家一起进行探讨。

我所用的是LINUX AS+VSFTPD-1.2.0-4的系统架构，在这里说明的是如果对配置文件不是很熟悉，最好做个备份，以免误操作: 

1． 匿名服务器的连接 (独立的服务器) 

在/etc/vsftpd.conf配置文件中添加如下几项: 

Anonymous_enable=yes (允许匿名登陆)

Dirmessage_enable=yes  (切换目录时，显示目录下.message的内容) 

Local_umask=022 (FTP上本地的文件权限，默认是077)

Connect_form_port_20=yes  (启用FTP数据端口的数据连接) *

Xferlog_enable=yes  (激活上传和下传的日志) 

Xferlog_std_format=yes (使用标准的日志格式)

Ftpd_banner=XXXXX  (欢迎信息) 

Pam_service_name=vsftpd  (验证方式) *

Listen=yes  (独立的VSFTPD服务器) *

功能: 只能连接FTP服务器，不能上传和下传

注: 其中所有和日志欢迎信息相关连的都是可选项,打了星号的无论什么帐户都要添加，是属于FTP的基本选项

2． 开启匿名FTP服务器上传权限

在配置文件中添加以下的信息即可: 

Anon_upload_enable=yes (开放上传权限)

Anon_mkdir_write_enable=yes  (可创建目录的同时可以在此目录中上传文件) 

Write_enable=yes (开放本地用户写的权限)

Anon_other_write_enable=yes (匿名帐号可以有删除的权限)

3． 开启匿名服务器下传的权限

在配置文件中添加如下信息即可: 

Anon_world_readable_only=no

注: 要注意文件夹的属性，匿名帐户是其它 (other) 用户要开启它的读写执行的权限

 (R) 读--下传  (W) 写--上传  (X) 执行--如果不开FTP的目录都进不去

4．普通用户FTP服务器的连接 (独立服务器) 

在配置文件中添加如下信息即可: 

Local_enble=yes  (本地帐户能够登陆) 

Write_enable=no  (本地帐户登陆后无权删除和修改文件) 

功能: 可以用本地帐户登陆vsftpd服务器，有下载上传的权限

注: 在禁止匿名登陆的信息后匿名服务器照样可以登陆但不可以上传下传

5． 用户登陆限制进其它的目录，只能进它的主目录

设置所有的本地用户都执行chroot

Chroot_local_user=yes  (本地所有帐户都只能在自家目录) 

设置指定用户执行chroot

Chroot_list_enable=yes  (文件中的名单可以调用) 

Chroot_list_file=/任意指定的路径/vsftpd.chroot_list

注意: vsftpd.chroot_list 是没有创建的需要自己添加，要想控制帐号就直接在文件中加帐号即可

6． 限制本地用户访问FTP

Userlist_enable=yes (用userlistlai 来限制用户访问)

Userlist_deny=no (名单中的人不允许访问)

Userlist_file=/指定文件存放的路径/  (文件放置的路径) 

注: 开启userlist_enable=yes匿名帐号不能登陆

7． 安全选项

Idle_session_timeout=600(秒)  (用户会话空闲后10分钟) 

Data_connection_timeout=120 (秒)   (将数据连接空闲2分钟断) 

Accept_timeout=60 (秒)   (将客户端空闲1分钟后断) 

Connect_timeout=60 (秒)   (中断1分钟后又重新连接) 

Local_max_rate=50000 (bite)   (本地用户传输率50K) 

Anon_max_rate=30000 (bite)   (匿名用户传输率30K) 

Pasv_min_port=50000  (将客户端的数据连接端口改在

Pasv_max_port=60000 50000—60000之间) 

Max_clients=200  (FTP的最大连接数) 

Max_per_ip=4  (每IP的最大连接数) 

Listen_port=5555  (从5555端口进行数据连接) 

8． 查看谁登陆了FTP,并杀死它的进程

ps –xf |grep ftp

kill 进程号

VSFTPD的高手篇

作者: 龙磊

我可不是高手！！！^_^我只不过是个菜鸟，尽我的能力写出了我这个菜鸟觉得的高手篇，所以有什么错误请大家指正哦！！！

环境: linux as 3.0 + vsftpd -1.2.0-4的系统架构，是在独立服务器下的哦！讨厌XINETD^_^

1． 配置本地组访问的FTP

首先创建用户组 test和FTP的主目录

groupadd test

mkdir /tmp/test

然后创建用户

useradd -G test –d /tmp/test –M usr1

注: G: 用户所在的组 d: 表示创建用户的自己目录的位置给予指定

M: 不建立默认的自家目录，也就是说在/home下没有自己的目录

useradd –G test –d /tmp/test –M usr2

接着改变文件夹的属主和权限

chown usr1.test /tmp/test --这表示把/tmp/test的属主定为usr1

chmod 750 /tmp/test --7表示wrx 5表示rx 0表示什么权限都没有

这个实验的目的就是usr1有上传、删除和下载的权限

而usr2只有下载的权限没有上传和删除的权限

当然啦大家别忘了我们的主配置文件vsftpd.conf

要确定local_enable=yes、write_enable=yes、chroot_local_usr=yes这三个选项是有的哦！

2． 配置独立FTP的服务器的非端口标准模式进行数据连接

这个非常容易: 在VSFTPD。CONF中添加

Listen_port=33333

就可以了啦！

好了重头戏来了，这也是我为什么叫高手篇的缘故！^_^ (大家不要扔鸡蛋哦！) 

3． 配置单独的虚拟FTP，使用虚拟FTP用户，并使建立的四个帐户中有不同的权限

 (两个有读目录的权限，一个有浏览、上传、下载的权限，一个有浏览、下载、删除和改文件名的权限) 

A: 配置网卡

第一块网卡地址是10.2.3.4 掩码是255.255.0.0

ifconfig eth0:1 211.131.4.253 netmask 255.255.255.0 up

B: 写入/etc/sysconfig中 (为了重起后IP地址不会丢失) 

cd /etc/sysconfig/network-scripts

cp ifcfg-eth0 ifcfg-eth0:1

vi ifcfg-eth0:1在其中修改内容如下

DEVICE=eth0:1

BROADCAST=211.131.4.255

HWADDR=该网卡的MAC地址

IPADDR=211.131.4.253

NETMASK=255.255.255.0

NETWORK=211.131.4.0

ONBOOT=yes

TYPE=Ethernet

wq推出

C: 进入vsftpd.conf所在的文件夹

cp vsftpd.conf vsftpd2.conf

修改vsftpd.conf添加以下信息

Listen_address=10.2.3.4

修改vsftpd2.conf添加以下信息

Listen_address=211.131.4.253

Ftpd_banner=this is a virtual ftp test

到此虚拟的FTP服务器建立好了

D: 建立logins.txt

vi /tmp/logins.txt

添加入下信息: 

longlei----用户名

longlei----密码

zhangweibo

zhangweibo

jinhui

jinhui

lxp

lxp

格式要按照我的来哦，一个用户名，一个密码啦

F: 建立访问者的口令库文件,然后修改其权限

db_load –T –t hash –f /tmp/logins.txt /etc/vsftpd_login.db

G: 进如/etc/pam.d/中创建ftp.vu

在此文件中添加如下信息

auth required /lib/security/pam_userdb.so db=/etc/vsftpd_login

account required /lib/security/pam_userdb.so db=/etc/vsftpd_login

H: 在/var/ftp/创建目录并改变其属性和它的属主

useradd -d /var/ftp/test qiang

chmod 700 /var/ftp/test

在目录中添加test_file测试文件

I: 进入vsftpd2.conf修改其中的信息 (我加的是) 

Listen_yes

Anonymous_enable=no

Local_enable=yes

Write_enable=no

Anon_upload_enable=no

Anon_mkdir_write_enable=no

Anon_other_write_enable=no

Chroot_local_user=yes

Guest_enable=yes----起用虚拟用户

Guest_username=qiang--将虚拟用户映射为本地用户

Listen_port=5555

Max_client=10

Max_per_ip=1

Ftpd_banner=this is a virtual server and users

Pam_service_name=ftp.vu

注: 在主配置文件中给的权限越低，在后面分用户管理的时候对拥护的权限划分的空间就越大，因为主配置文件最高的限制服务先读主配置文件，然后再读用户的配置文件

重起服务

到此虚拟USER就建好了

J: 在VSFTPD。CONF所在的目录中创建virtaul文件目录

并在文件目录中创建以你用户名命名的配置文件

Longlei zhangweibo jinhui lxp

在longlei中添加: 

Anon_world_readable_only=no

在lxp中添加

Anon_world_readable_only=no

这样此两个用户就有了浏览目录的权限了

在jinhui中添加

Anon_world_readable_only=no

Write_enable=yes

Anon_upload_enable=yes

此用户就有了上传、下载和浏览的权限

在zhangweibo中添加

Anon_world_readable_only=no

Write_enable=yes

Anon_upload_enable=yes

Anon_other_write_enable=yes

此用户就有了上传、下载、删除文件目录、修改文件名和浏览的权限

K: 修改vsftpd2.conf

加入user_config_dir=/vsftpd.conf所在的目录/virtual

重起服务器就搞定了

好了大家别走开，现在隆重推出VSFTPD。CONF中的我所知道的所有配置信息

Anonymous_enable=yes (允许匿名登陆)

Dirmessage_enable=yes  (切换目录时，显示目录下.message的内容) 

Local_umask=022 (FTP上本地的文件权限，默认是077)

Connect_form_port_20=yes  (启用FTP数据端口的数据连接) *

Xferlog_enable=yes  (激活上传和下传的日志) 

Xferlog_std_format=yes (使用标准的日志格式)

Ftpd_banner=XXXXX  (欢迎信息) 

Pam_service_name=vsftpd  (验证方式) *

Listen=yes  (独立的VSFTPD服务器) *

Anon_upload_enable=yes (开放上传权限)

Anon_mkdir_write_enable=yes  (可创建目录的同时可以在此目录中上传文件) 

Write_enable=yes (开放本地用户写的权限)

Anon_other_write_enable=yes (匿名帐号可以有删除的权限)

Anon_world_readable_only=no (放开匿名用户浏览权限)

Ascii_upload_enable=yes (启用上传的ASCII传输方式)

Ascii_download_enable=yes (启用下载的ASCII传输方式)

Banner_file=/var/vsftpd_banner_file (用户连接后欢迎信息使用的是此文件中的相关信息)

Idle_session_timeout=600(秒)  (用户会话空闲后10分钟) 

Data_connection_timeout=120 (秒)   (将数据连接空闲2分钟断) 

Accept_timeout=60 (秒)   (将客户端空闲1分钟后断) 

Connect_timeout=60 (秒)   (中断1分钟后又重新连接) 

Local_max_rate=50000 (bite)   (本地用户传输率50K) 

Anon_max_rate=30000 (bite)   (匿名用户传输率30K) 

Pasv_min_port=50000  (将客户端的数据连接端口改在

Pasv_max_port=60000 50000—60000之间) 

Max_clients=200  (FTP的最大连接数) 

Max_per_ip=4  (每IP的最大连接数) 

Listen_port=5555  (从5555端口进行数据连接) 

Local_enble=yes  (本地帐户能够登陆) 

Write_enable=no  (本地帐户登陆后无权删除和修改文件) 

这是一组

Chroot_local_user=yes  (本地所有帐户都只能在自家目录) 

Chroot_list_enable=yes  (文件中的名单可以调用) 

Chroot_list_file=/任意指定的路径/vsftpd.chroot_list

 (前提是chroot_local_user=no) 

这又是一组

Userlist_enable=yes  (在指定的文件中的用户不可以访问) 

Userlist_deny=yes

Userlist_file=/指定的路径/vsftpd.user_list

又开始单的了

Banner_fail=/路径/文件名  (连接失败时显示文件中的内容) 

Ls_recurse_enable=no

Async_abor_enable=yes

One_process_model=yes

Listen_address=10.2.2.2  (将虚拟服务绑定到某端口) 

Guest_enable=yes (虚拟用户可以登陆)

Guest_username=所设的用户名  (将虚拟用户映射为本地用户) 

User_config_dir=/任意指定的路径/为用户策略自己所建的文件夹

(指定不同虚拟用户配置文件的路径)

又是一组

Chown_uploads=yes  (改变上传文件的所有者为root) 

Chown_username=root

又是一组

Deny_email_enable=yes (是否允许禁止匿名用户使用某些邮件地址)

Banned_email_file=//任意指定的路径/xx/

又是单的

Pasv_enable=yes  ( 服务器端用被动模式) 

User_config_dir=/任意指定的路径//任意文件目录 (指定虚拟用户存放配置文件的路径)

遇到的问题

1. 只允许匿名用户登录

现象: ftp连接过程中，提示输入用户名，输入本机已有用户名angel，得到提示: 530 This FTP server is anonymous only，登录失败。

原因: 安装vsftpd后，其默认为匿名FTP服务器，只允许匿名用户登录。

解决方法: vsftpd有三种服务器方式: 匿名方式、本地方式和虚拟用户方式，此处需要修改vsftpd的配置将其设为本地方式。vsftpd的配置文件位于/etc/目录下，名称为vsftpd.conf。关于该配置文件在网上已经有很多高手做了详细的分析和讲解，并且该文件内部的注释也比较详细，这里就不再一一讲解了。下面只说明几处需要修改的地方: 

将local_enable=YES前的#去掉，使其可用，表示允许本地用户登录；增加listen_port=21配置项，设置监听端口为21；该步骤可选，不允许匿名用户登录，将anonymous_enable=YES的值改为NO，根据实际需要设置。

重启vsftpd服务: service vsftpd restart。启动后，在进行测试，使用本地用户angel及其密码登录，成功。注意: 以上测试是在本机 (或使用SSH登录后) 进行。

500 OOPS: cannot change directory

setsebool -P ftpd_disable_trans 1

service vsftpd restart

setsebool ftpd_disable_trans 1 是停用SELinux 對ftpd 的保護，這樣，ftpd 就可以跟平常一樣的運作了。
  
setsebool 是設定selinux布尔函數的命令，值有0和1。


<http://wiki.ubuntu.org.cn/Vsftpd>

<http://hi.baidu.com/cwg3739/blog/item/3d02a477fc42411fb051b981.html>

<http://doc.linuxpk.com/4233.html>