---
title: ssh 跳板(Jump Host)的使用
author: "-"
date: 2014-08-08T07:35:43+00:00
url: /?p=6912
categories:
  - Inbox
tags:
  - reprint
---
## ssh 跳板(Jump Host)的使用

```bash
# jump0:跳板机
# server0: 目标服务器
host jump0
  HostName 192.168.0.1
  User user0

Host server0
  HostName 192.168.0.2
  User user0
  ProxyCommand ssh -q -W %h:%p jump0
# %h: ~/.ssh/config 的语法, 代表主机名, 执行的时候会用 HostName 的值替换
# %p: 端口
# https://linux.die.net/man/5/ssh_config
```

这里说的 ssh 跳板，是指我们通过一个中继服务器其访问另一台内网服务器。典型的应用场景是在 VPN 网络中，我们进入了 VPN 服务器之后再访问另一个网段的内网服务器。

1 动态跳板列表
最简单的方法是在 ssh 命令中使用 -J 选项来指明跳板列表。这里称「列表」，意味着你可以给出一长串的服务器，ssh 会顺序经过所有的跳板然后到达最终的远程服务器。命令的形式如下：

1
ssh -J username@host1:port username@host2:port
跳板序列的形式如下：

1
ssh -J username@host1:port,username@host2:port username@host3:port
2 静态列表配置
ssh 中 host 别名可以在 ~/.ssh/config 文件中进行设置。如按照如下设置

1
2
3
4
5
6
7
8

### First jumphost. Directly reachable

Host vps1
  HostName vps1.example.org

### Host to jump to via jumphost1.example.org

Host contabo
  HostName contabo.example.org
  ProxyJump contabo
我们可以简化 ssh 命令：

1
ssh -J vps1 contabo
另外，如果某个远端服务器总是需要经过一个固定的跳板服务器，我们可以通过配置文件固定下来。如：

1
2
3
4
5
6
7
8
9
10
11
Host vps1
    HostName vps1.example.org
    IdentityFile ~/.ssh/vps1.pem
    User ec2-user

Host contabo
    HostName contabo.example.org
    IdentityFile ~/.ssh/contabovps
    Port 22
    User admin
    ProxyCommand ssh -q -W %h:%p vps1
其中关键的配置是 ProxyCommand，其中-q表示代理命令工作在静默模式下，而 -W 则表示 stdio 转发。

然后我们就可以通过下面的命令访问 contabo 了

1
ssh contabo
这里说一个让 ssh 在空闲是保持连接的方法：在 ~/.ssh/config 文件中加入：

1
2
Host *
    ServerAliveInterval 10

>[https://www.codewoody.com/posts/11038/](https://www.codewoody.com/posts/11038/)
