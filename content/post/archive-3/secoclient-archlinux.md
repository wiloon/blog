---
title: huawei vpn, sslvpn, secoclient in archlinux, 华为SSLVPN客户端
author: "-"
date: 2020-02-01T03:59:45+00:00
url: secoclient
categories:
  - VPN

tags:
  - reprint
---
## huawei vpn, sslvpn, secoclient in archlinux, 华为SSLVPN客户端

### 下载安装包

<http://www.corem.com.cn/index.php/service/tools/secoclient>

官方只提供了ubuntu版本，用以下方式可以在 archlinux 上使用。

```bash
sudo -i

# seco client 依赖 ubuntu 的 arch 命令， 模拟 arch 命令返回 x86_64
echo "echo x86_64" > /usr/bin/arch
chmod u+x /usr/bin/arch

# install seco client
./secoclient-linux-64-6.0.2.run

# 启动后台服务
cd /usr/local/SecoClient/promote
./SecoClientPromoteService -d

# 启动secoclient UI
cd /usr/local/SecoClient/
./SecoClient
```

### 启动脚本

把 server_address 替换成服务端IP

```bash
#!/bin/bash                 
sudo ip route del <server_address>
count=`ps -ef |grep SecoClientPromoteService |grep -v "grep" |wc -l`
      echo $count
      if [ 0 == $count ];then
              cd /usr/local/SecoClient/promote
              sudo       ./SecoClientPromoteService -d
      fi
count=`ps -ef |grep SecoClient |grep -v "grep" |wc -l`
      echo $count
      if [ 1 == $count ];then
            cd /usr/local/SecoClient/
           sudo ./SecoClient
      fi
```

### crostini

```bash
# in crostini
export WAYLAND_DISPLAY=wayland-0
# user id 使用非0数字(非root的已有用户id,如1000,填0 时，secoclient无法启动)
export XDG_RUNTIME_DIR=/run/user/<user id>
/opt/google/cros-containers/bin/sommelier -X ./SecoClient
```
