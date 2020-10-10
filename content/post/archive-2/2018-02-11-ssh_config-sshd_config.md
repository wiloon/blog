---
title: ssh_config, sshd_config
author: wiloon
type: post
date: 2018-02-11T15:40:49+00:00
url: /?p=11872
categories:
  - Uncategorized

---
https://segmentfault.com/a/1190000014822400

sshd_config
  
MaxAuthTries 20

http://matt-u.iteye.com/blog/851158

linux ssh\_config和sshd\_config配置文件
  
转载190019892011-08-22 09:34:11评论(1)63053人阅读
   
现在远程管理linux系统基本上都要使用到ssh，原因很简单：telnet、FTP等传输方式是&#x200d;以明文传送用户认证信息，本质上是不安全的，存在被网络窃听的危险。SSH（Secure Shell）目前较可靠，是专为远程登录会话和其他网络服务提供安全性的协议。利用SSH协议可以有效防止远程管理过程中的信息泄露问题，透过SSH可以对所有传输的数据进行加密，也能够防止DNS欺骗和IP欺骗。

ssh\_config和sshd\_config都是ssh服务器的配置文件，二者区别在于，前者是针对客户端的配置文件，后者则是针对服务端的配置文件。两个配置文件都允许你通过设置不同的选项来改变客户端程序的运行方式。下面列出来的是两个配置文件中最重要的一些关键词，每一行为"关键词&值"的形式，其中"关键词"是忽略大小写的。
  
&#x200d;&#x200d;1、编辑 /etc/ssh/ssh_config 文件

# Site-wide defaults for various options

Host *
          
ForwardAgent no
          
ForwardX11 no
          
RhostsAuthentication no
          
RhostsRSAAuthentication no
      
&#x200d; RSAAuthentication yes
          
PasswordAuthentication yes
          
FallBackToRsh no
          
UseRsh no
          
BatchMode no
          
CheckHostIP yes
          
StrictHostKeyChecking no
          
IdentityFile ~/.ssh/identity
          
Port 22
          
Cipher blowfish
          
EscapeChar ~
  
下面对上述选项参数逐进行解释：

# Site-wide defaults for various options

带"#"表示该句为注释不起作，该句不属于配置文件原文，意在说明下面选项均为系统初始默认的选项。说明一下，实际配置文件中也有很多选项前面加有"#"注释，虽然表示不起作用，其实是说明此为系统默认的初始化设置。
  
Host *
  
"Host"只对匹配后面字串的计算机有效，"_"表示所有的计算机。从该项格式前置一些可以看出，这是一个类似于全局的选项，表示下面缩进的选项都适用于该设置，可以指定某计算机替换_号使下面选项只针对该算机器生效。
  
ForwardAgent no
  
"ForwardAgent"设置连接是否经过验证代理（如果存在）转发给远程计算机。
  
ForwardX11 no
  
"ForwardX11"设置X11连接是否被自动重定向到安全的通道和显示集（DISPLAY set）。
  
RhostsAuthentication no
  
"RhostsAuthentication"设置是否使用基于rhosts的安全验证。
  
RhostsRSAAuthentication no
  
"RhostsRSAAuthentication"设置是否使用用RSA算法的基于rhosts的安全验证。
  
RSAAuthentication yes
  
"RSAAuthentication"设置是否使用RSA算法进行安全验证。
  
PasswordAuthentication yes
  
"PasswordAuthentication"设置是否使用口令验证。
  
FallBackToRsh no
  
"FallBackToRsh"设置如果用ssh连接出现错误是否自动使用rsh，由于rsh并不安全，所以此选项应当设置为"no"。
  
UseRsh no
  
"UseRsh"设置是否在这台计算机上使用"rlogin/rsh"，原因同上，设为"no"。
  
BatchMode no
  
"BatchMode"：批处理模式，一般设为"no"；如果设为"yes"，交互式输入口令的提示将被禁止，这个选项对脚本文件和批处理任务十分有用。
  
CheckHostIP yes
  
"CheckHostIP"设置ssh是否查看连接到服务器的主机的IP地址以防止DNS欺骗。建议设置为"yes"。
  
StrictHostKeyChecking no
  
"StrictHostKeyChecking"如果设为"yes"，ssh将不会自动把计算机的密匙加入"$HOME/.ssh/known_hosts"文件，且一旦计算机的密匙发生了变化，就拒绝连接。
  
IdentityFile ~/.ssh/identity
  
"IdentityFile"设置读取用户的RSA安全验证标识。
  
Port 22
  
"Port"设置连接到远程主机的端口，ssh默认端口为22。
  
Cipher blowfish
  
"Cipher"设置加密用的密钥，blowfish可以自己随意设置。
  
EscapeChar ~
  
"EscapeChar"设置escape字符。
  
2、编辑 /etc/ssh/sshd_config 文件：&#x200d;

# This is ssh server systemwide configuration file.

          Port 22
          ListenAddress 192.168.1.1
          HostKey /etc/ssh/ssh_host_key
          ServerKeyBits 1024
          LoginGraceTime 600
          KeyRegenerationInterval 3600
          PermitRootLogin no
          IgnoreRhosts yes
          IgnoreUserKnownHosts yes
          StrictModes yes
          X11Forwarding no
          PrintMotd yes
          SyslogFacility AUTH
          LogLevel INFO
          RhostsAuthentication no
          RhostsRSAAuthentication no
          RSAAuthentication yes
          PasswordAuthentication yes
          PermitEmptyPasswords no
          AllowUsers admin
    

&#x200d;下面逐行说明上面的选项设置：
  
Port 22
  
"Port"设置sshd监听的端口号。
  
ListenAddress 192.168.1.1
  
"ListenAddress"设置sshd服务器绑定的IP地址。
  
HostKey /etc/ssh/ssh\_host\_key
  
"HostKey"设置包含计算机私人密匙的文件。
  
ServerKeyBits 1024
  
"ServerKeyBits"定义服务器密匙的位数。
  
LoginGraceTime 600
  
"LoginGraceTime"设置如果用户不能成功登录，在切断连接之前服务器需要等待的时间（以秒为单位）。
  
KeyRegenerationInterval 3600
  
"KeyRegenerationInterval"设置在多少秒之后自动重新生成服务器的密匙（如果使用密匙）。重新生成密匙是为了防止用盗用的密匙解密被截获的信息。
  
PermitRootLogin no
  
"PermitRootLogin"设置是否允许root通过ssh登录。这个选项从安全角度来讲应设成"no"。
  
IgnoreRhosts yes
  
"IgnoreRhosts"设置验证的时候是否使用"rhosts"和"shosts"文件。
  
IgnoreUserKnownHosts yes
  
"IgnoreUserKnownHosts"设置ssh daemon是否在进行RhostsRSAAuthentication安全验证的时候忽略用户的"$HOME/.ssh/known_hosts"
  
StrictModes yes
  
"StrictModes"设置ssh在接收登录请求之前是否检查用户家目录和rhosts文件的权限和所有权。这通常是必要的，因为新手经常会把自己的目录和文件设成任何人都有写权限。
  
X11Forwarding no
  
"X11Forwarding"设置是否允许X11转发。
  
PrintMotd yes
  
"PrintMotd"设置sshd是否在用户登录的时候显示"/etc/motd"中的信息。
  
SyslogFacility AUTH
  
"SyslogFacility"设置在记录来自sshd的消息的时候，是否给出"facility code"。
  
LogLevel INFO
  
"LogLevel"设置记录sshd日志消息的层次。INFO是一个好的选择。查看sshd的man帮助页，已获取更多的信息。
  
RhostsAuthentication no
  
"RhostsAuthentication"设置只用rhosts或"/etc/hosts.equiv"进行安全验证是否已经足够了。
  
RhostsRSAAuthentication no
  
"RhostsRSA"设置是否允许用rhosts或"/etc/hosts.equiv"加上RSA进行安全验证。
  
RSAAuthentication yes
  
"RSAAuthentication"设置是否允许只有RSA安全验证。
  
PasswordAuthentication yes
  
"PasswordAuthentication"设置是否允许口令验证。
  
PermitEmptyPasswords no
  
"PermitEmptyPasswords"设置是否允许用口令为空的帐号登录。
  
AllowUsers admin
  
"AllowUsers"的后面可以跟任意的数量的用户名的匹配串，这些字符串用空格隔开。主机名可以是域名或IP地址。