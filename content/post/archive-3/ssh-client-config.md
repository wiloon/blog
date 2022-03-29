---
title: ssh client config
author: "-"
date: 2020-04-18T12:36:57+00:00
url: ssh/config
categories:
  - linux
tags:
  - reprint
---
## ssh config
>https://daemon369.github.io/ssh/2015/03/21/using-ssh-config-file

```bash
vim ~/.ssh/config
#---
Host *
    ControlMaster auto # ssh multiplexing
    ControlPath   ~/.ssh/master-%r@%h:%p
    ControlPersist 10m
    ForwardAgent yes # ssh agent forward
    User root # 默认用户
```

## ssh client config, 保持连接

避免SSH连接因超时闲置断开

## ssh 客户端保持连接

```bash
vim ~/.ssh/config

Host 192.168.*
    ServerAliveInterval 120
    User root

```

用 SSH 过程连接电脑时，经常遇到长时间不操作而被服务器踢出的情况，常见的提示如:

    Write failed: Broken pipe

这是因为如果有一段时间在SSH连接上无数据传输，连接就会断开。解决此问题有两种方法。[1]

## 方案一: 在客户端设置

方法很简单，只需在客户端电脑上编辑 (需要root权限) /etc/ssh/ssh_config，并添加如下一行:
  
  ServerAliveInterval 60
  
此后该系统里的用户连接SSH时，每60秒会发一个KeepAlive请求，避免被踢。
  
## 方案二: 在服务器端设置
  
如果有相应的权限，也可以在服务器端设置，即编辑/etc/ssh/sshd_config，并添加:
  
  ClientAliveInterval 60
  
重启SSH服务器后该项设置会生效。每一个连接到此服务器上的客户端都会受其影响。应注意启用该功能后，安全性会有一定下降 (比如忘记登出时……)

```bash
vim /etc/ssh/sshd_config
#添加
# ClientAliveInterval指定了服务器端向客户端请求消息的时间间隔, 默认是0，不发送。而ClientAliveInterval 60表示每分钟发送一次，然后客户端响应，这样就保持长连接了。
ClientAliveInterval 30
# ClientAliveCountMax表示服务器发出请求后客户端没有响应的次数达到一定值，就自动断开
ClientAliveCountMax 3
```

#### 使用通配符 (wildcard)

```bash
vim .ssh/config

host 192.168.*
    user root

host name0
    hostname 192.168.1.1
    user root
```


#### Session Multiplexing
<https://blog.wiloon.com/?p=16030>



### ssh agent forward
<https://blog.wiloon.com/?p=16034>

### 指定源端口

```bash
ssh -o 'ProxyCommand nc -p 2345 %h %p' $MY_SERVER
```

### 查看ssh上已经连接的用户、session

who or w. who -a
  
netstat -tnpa | grep 'ESTABLISHED.*sshd'
  
ps auxwww | grep sshd:
  
ps ax | grep sshd

### sshd, vim /etc/ssh/sshd_config

maxstartup
  
这个是限制处于联机页面的连接数，默认值10。联机页面就是当你登录ssh时，还没输入密码的页面。

三元组形式
  
10:30:60
  
10: 当连接数达到10时就开始拒绝连接，不过不是全部拒绝，我们继续往下看
  
30: 当连接数到达10时，之后的连接有30的概率被拒绝掉
  
60: 当连接数达到60时，之后的连接就全部拒绝了
  
一个数字的形式
  
我们可以直接 写个60，这样言简意赅，连接数达到60之前敞开玩，达到60后就不能玩了。

maxsessions

同一地址的最大连接数,也就是同一个IP地址最大可以保持多少个链接

https://blog.csdn.net/u014686399/java/article/details/84778292



SSH 参数配置有3个层次: 

命令行参数，如-p 10086, -i /path/to/identity_file 等选项来设置SSH的端口号或认证证书位置
  
针对某个用户的配置文件，所在路径为~/.ssh/config，默认是不存在的，需要手动创建
  
针对系统所有用户的配置文件，，所在路径为/etc/ssh/ssh_config
  
参数重要性的顺序也是1>2>3，即越近的配置重要性越高。

用户配置文件在 ~/.ssh/config, 没有的话新建一个
  
Host 名称(自己决定，方便输入记忆的)
      
HostName 主机名
      
Port 22
      
User 登录的用户名
      
IdentityFile 证书文件路径

Host
  
Host配置项标识了一个配置区段。
  
ssh配置项参数值可以使用通配符: *代表0～n个非空白字符，?代表一个非空白字符，!表示例外通配。
  
我们可以在系统配置文件中看到一个匹配所有host的默认配置区段: 

```bash
$ cat /etc/ssh/ssh_config | grep '^Host'
```

Host *
  
这里有一些默认配置项，我们可以在用户配置文件中覆盖这些默认配置。

```bash
host router
     HostName 192.168.1.1
     Port 22
     User root
     IdentityFile ~/.ssh/id_rsa
```

使用ssh的配置文件可以在很大程度上方便各种操作，特别适应于有多个ssh帐号、使用非标准端口或者写脚本等情况。

man ssh_config
  
可以查看手册

如果之前是用密码方式来登录ssh，需要先改用证书方式。可以看最后面生成SSH证书

两个SSH帐号，一个是github的，一个是其他服务器的，证书文件正如其名，那么可以这样写

Host github.com
      
HostName github.com
      
User git
      
IdentityFile ~/.ssh/github

注意，github的Host必须写成"github.com"。你可以会有其他要求，比如指定端口号、绑定本地端口，这些都可以通过man来查询，比如

Port 端口号
  
DynamicForward 本地端口号
  
如果服务器同时有ipv4/ipv6地址，HostName使用域名会比较方便

使用

有了这些配置，很多操作就非常简化了。比如登录服务器

ssh server
  
传输文件

scp server:~/test .
  
如果使用Putty等工具，可能需要一些其他操作(转换私钥格式，貌似)，自行搜索吧

生成SSH证书

登入服务器端，生成密钥(你使用哪个用户名登录，就在哪个用户名下生成)

ssh-keygen -t rsa
  
会询问将密钥放在何处，默认即可。然后是输入密码，留空(否则你登录不仅需要私钥还要输入密码)。

完成后在~/.ssh目录下会生成另个文件id_rsa、id_rsa.pub，一个私钥一个公钥。接着执行

cd ~/.ssh
  
cat id_rsa.pub >> authorized_keys
  
chmod 600 authorized_keys
  
再将id_rsa取回本地，放入~/.ssh并将权限设为400。

服务器端，删掉这两个文件，并修改sshd配置。编辑/etc/ssh/sshd_config如下

PubkeyAuthentication yes
  
### PasswordAuthentication
是否允许使用基于密码的认证。默认为"yes"。
  
之后重启sshd服务
  
https://vra.github.io/2017/07/09/ssh-config/
  
http://www.lainme.com/doku.php/blog/2011/01/%E4%BD%BF%E7%94%A8ssh_config