---
title: ufw
author: "-"
date: 2019-07-28T15:09:46+00:00
url: ufw
categories:
  - Linux
tags:
  - reprint
  - remix
---
## ufw

UFW，即简单防火墙 uncomplicated firewall，是一个 Arch Linux、Debian 或 Ubuntu 中管理防火墙规则的前端。 UFW 通过命令行使用（尽管它有可用的 GUI），它的目的是使防火墙配置简单（即不复杂uncomplicated）。

```Bash
# check ufw status
sudo ufw status
# Status: active
# Status: inactive
```

docker 网络 会忽略  ufw 配置

https://docs.docker.com/engine/network/packet-filtering-firewalls/#docker-and-ufw
