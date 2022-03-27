---
title: nftable, nft  basic, commands
author: "-"
date: 2018-10-05T06:43:04+00:00
url: nft
categories:
  - network

tags:
  - reprint
---
## nftable, nft  basic, commands

### 安装 nftables

#### archlinux
```bash
sudo pacman -S nftables
sudo systemctl start nftables
sudo systemctl enable nftables
```

#### centos 8
```bash
systemctl disable --now firewalld

```


### 查
```bash
nft list ruleset # 列出所有规则
nft list tables  # 列出所有表
# 列出每个族的表
nft list tables ip
nft list table ip foo # 列出foo表的内容

nft list chain filter input # 列出filter表input链

# 列出handle
nft -a list table filter
```

### 增
#### 增加表, Adding tables: 
```bash
nft add table [<family>] <name>
nft add table ip foo
```

family 参数是可选的,如果不指定 family,默认是 IPv4

#### 增加链,add chain: 
```bash
nft add chain [<family>]  <chain-name> { type <type> hook <hook> priority <value> \; [policy <policy>] }
nft add chain filter input { type filter hook input priority 0 \; } # 要和hook (钩子) 相关连
```

#### 增加规则, add rule:
```bash
nft add rule  <chain-name> ip daddr 8.8.8.8 counter
nft add rule filter input tcp dport 22 accept

nft insert rule nat post ip protocol icmp icmp type echo-request accept
```

### 删
```bash
#清空整个规则集
nft flush ruleset
# 删除表中所有的规则
nft flush table ip foo

nft delete table ip foo

# 按 handle 删除
nft delete rule table0 chain0 handle 4
```

### 改
更改链名用rename  
更改规则用replace  
-n  
-nn 以上命令后面也可以加 -nn 用于不解析ip地址和端口  
-a 加 -a 用于显示 handles  

### 保存规则到文件
nftables.service 启动时自动加载 /etc/nftables.conf

```bash
nft list ruleset> /etc/nftables.conf
```

### 从文件加载规则

```bash
nft -f /etc/nftables.conf
```