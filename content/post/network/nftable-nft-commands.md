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

## 表

```Bash
# 列出所有表
nft list tables
# 列出某一个族的表
# 列出 inet 族的表
nft list tables inet
# 列出 ip 族的表
nft list tables ip

# 列出 table0 表的内容
nft list table ip table0
nft list table table0 

# 列出 handle
nft -a list table filter

# 增加表, Adding tables

命令行

```bash
# nft add table [family] <name>
nft add table ip foo

# 默认簇: ip
nft add table table0

# 删除 ip 族的 foo 表
nft delete table ip foo
# 默认 ip 族
nft delete table foo
```

## 链

```Bash
# 创建链
nft add chain [<family>]  <chain-name> { type <type> hook <hook> priority <value> \; [policy <policy>] }
nft add chain filter input { type filter hook input priority 0 \; } # 要和hook (钩子) 相关连

# 创建一个常规链
# 将名为 chain0 的常规链添加到 ip 簇(默认) 中名为 mytable 的表中
nft add chain table0 chain0

# 创建一个基本链
nft add chain ip table0 chain1 { type filter hook input priority 0\; }
nft add chain table0 chain1 { type filter hook input priority 0\; }
nft add chain table0 chain2 { type filter hook output priority 0\; }

# 将默认表中的 input 链策略从 accept 更改为 drop
nft chain ip table0 input { policy drop \; }
```


## 规则 

```Bash
nft add rule [<family>] <table> <chain> <matches> <statements>
nft add rule inet mytable input tcp dport ssh accept

# family = ip
# table = table0
# chain = chain1
# matches = tcp dport ssh accept
nft add rule table0 chain1 tcp sport 1035 drop


nft replace rule [<family>] <table> <chain> [handle <handle>] <matches> <statements>
nft replace rule ip table0 chain1 tcp sport 1025 drop
nft replace rule table0 chain1 handle 4 tcp sport 1025 drop

# nft delete rule [<family>] <table> <chain> [handle <handle>]
nft delete rule ip table0 chain1 handle 7

```

### 查

```bash
nft list ruleset # 列出所有规则 
# 列出 ip 族 foo 表的内容
nft list table ip foo # 列出 foo 表的内容

nft list chain filter input # 列出 filter 表 input 链


```

### 增

#### 增加表, Adding tables

命令行

```bash
# nft add table [family] <name>
nft add table ip foo

# 默认簇: ip
nft add table foo

```

原生语法的脚本

```Bash
table <table_address_family> <table_name> {
}
```

family 参数是可选的, 如果不指定 family, 默认是 IPv4

#### 增加链, add chain

```bash


```

#### 增加规则, add rule

```bash
nft add rule  <chain-name> ip daddr 8.8.8.8 counter
nft add rule filter input tcp dport 22 accept

nft insert rule nat post ip protocol icmp icmp type echo-request accept
```

### 删

```bash
# 清空整个规则集
nft flush ruleset
# 删除表中所有的规则
# 删除 ip 族 foo 表的内容
nft flush table ip foo



# 按 handle 删除
nft delete rule table0 chain0 handle 4

# 删除指定的链，这里为 input
nft delete chain inet mytable input

```

### 改

更改链名用 rename  
更改规则用 replace
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
