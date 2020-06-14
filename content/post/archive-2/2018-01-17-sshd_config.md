---
title: sshd config
author: wiloon
type: post
date: 2018-01-17T08:50:28+00:00
url: /?p=11742
categories:
  - Uncategorized

---
.ssh/authorized_keys

ClientAliveInterval
  
Port 22  
port用来设置sshd监听的端口，为了安全起见，建议更改默认的22端口为5位以上陌生端口

AddressFamily
指定 sshd(8) 应当使用哪种地址族。取值范围是：&#8221;any&#8221;(默认)、&#8221;inet&#8221;(仅IPv4)、&#8221;inet6"(仅IPv6)。
  
#ListenAddress 0.0.0.0
  
#ListenAddress用来设置sshd服务器绑定的IP地址
  
Protocol
               
指定 sshd(8) 支持的SSH协议的版本号。
               
&#8216;1&#8217;和&#8217;2&#8217;表示仅仅支持SSH-1和SSH-2协议。&#8221;2,1"表示同时支持SSH-1和SSH-2协议。

HostKey
               
主机私钥文件的位置。如果权限不对，sshd(8) 可能会拒绝启动。
               
SSH-1默认是 /etc/ssh/ssh\_host\_key 。
               
SSH-2默认是 /etc/ssh/ssh\_host\_rsa\_key 和 /etc/ssh/ssh\_host\_dsa\_key 。
               
一台主机可以拥有多个不同的私钥。&#8221;rsa1"仅用于SSH-1，&#8221;dsa&#8221;和&#8221;rsa&#8221;仅用于SSH-2。

PermitRootLogin
  
是否允许 root 登录。可用值如下：
  
"yes&#8221;(默认) 表示允许。&#8221;no&#8221;表示禁止。
  
"without-password&#8221;表示禁止使用密码认证登录。
  
"forced-commands-only&#8221;表示只有在指定了 command 选项的情况下才允许使用公钥认证登录。同时其它认证方法全部被禁止。这个值常用于做远程备份之类的事情。

AuthorizedKeysFile
  
存放该用户可以用来登录的 RSA/DSA 公钥。
  
该指令中可以使用下列根据连接时的实际情况进行展开的符号：
  
%% 表示&#8217;%&#8217;、%h 表示用户的主目录、%u 表示该用户的用户名。
  
经过扩展之后的值必须要么是绝对路径，要么是相对于用户主目录的相对路径。
  
默认值是&#8221;.ssh/authorized_keys&#8221;。

PasswordAuthentication
  
是否允许使用基于密码的认证。默认为&#8221;yes&#8221;。

UsePrivilegeSeparation
  
是否让 sshd(8) 通过创建非特权子进程处理接入请求的方法来进行权限分离。默认值是&#8221;yes&#8221;。
               
认证成功后，将以该认证用户的身份创建另一个子进程。
               
这样做的目的是为了防止通过有缺陷的子进程提升权限，从而使系统更加安全。

PermitUserEnvironment
               
指定是否允许 sshd(8) 处理 ~/.ssh/environment 以及 ~/.ssh/authorized_keys 中的 environment= 选项。
               
默认值是&#8221;no&#8221;。如果设为&#8221;yes&#8221;可能会导致用户有机会使用某些机制(比如 LD_PRELOAD)绕过访问控制，造成安全漏洞。

AllowUsers
               
这个指令后面跟着一串用空格分隔的用户名列表(其中可以使用&#8221;*&#8221;和&#8221;?&#8221;通配符)。默认允许所有用户登录。
               
如果使用了这个指令，那么将仅允许这些用户登录，而拒绝其它所有用户。
               
如果指定了 USER@HOST 模式的用户，那么 USER 和 HOST 将同时被检查。
               
这里只允许使用用户的名字而不允许使用UID。相关的 allow/deny 指令按照下列顺序处理：
               
DenyUsers, AllowUsers, DenyGroups, AllowGroups

Ciphers
               
指定SSH-2允许使用的加密算法。多个算法之间使用逗号分隔
               
Ciphers aes256-ctr,aes192-ctr,aes128-ctr
  
https://blog.csdn.net/zhu_xun/article/details/18304441
  
http://www.jinbuguo.com/openssh/sshd_config.html
  
http://daemon369.github.io/ssh/2015/03/21/using-ssh-config-file