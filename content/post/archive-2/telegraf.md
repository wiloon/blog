---
title: telegraf
author: "-"
date: 2019-02-16T11:08:43+00:00
url: telegraf
categories:
  - devops
tags:
  - reprint
  - remix
---
## telegraf

### archlinux, telegraf

```bash
yay -S telegraf-bin
```

### ubuntu && debian

```bash
# influxdb.key GPG Fingerprint: 05CE15085FC09D18E99EFB22684A14CF2582E0C5
wget -q https://repos.influxdata.com/influxdb.key
echo '23a1c8836f0afc5ed24e0486339d7cc8f6790b83886c4c96995b88a061c5bb5d influxdb.key' | sha256sum -c && cat influxdb.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/influxdb.gpg > /dev/null
echo 'deb [signed-by=/etc/apt/trusted.gpg.d/influxdb.gpg] https://repos.influxdata.com/debian stable main' | sudo tee /etc/apt/sources.list.d/influxdata.list
sudo apt-get update && sudo apt-get install telegraf
```

### binary

[https://portal.influxdata.com/downloads/](https://portal.influxdata.com/downloads/)

> vim /etc/telegraf/telegraf.conf

```bash
[global_tags]
[agent]
  interval = "10s"
  round_interval = true
  metric_batch_size = 1000
  metric_buffer_limit = 10000
  collection_jitter = "0s"
  flush_interval = "10s"
  flush_jitter = "0s"
  precision = ""
# 修改主机名
  hostname = "foo"
  omit_hostname = false
[[outputs.influxdb]]
  urls = ["http://influxdb.wiloon.com:32086"]
# 注意修改 database
  database = "monitor"

[[inputs.cpu]]
  percpu = true
  totalcpu = true
  collect_cpu_time = false
  report_active = false
[[inputs.disk]]
  ignore_fs = ["tmpfs", "devtmpfs", "devfs", "iso9660", "overlay", "aufs", "squashfs"]

[[inputs.diskio]]
[[inputs.kernel]]
[[inputs.mem]]
[[inputs.processes]]
[[inputs.swap]]
[[inputs.system]]
[[inputs.net]]
[[inputs.netstat]]
[[inputs.linux_sysctl_fs]]
```

#### inputs.linux_sysctl_fs

>[https://www.kernel.org/doc/Documentation/sysctl/fs.txt](https://www.kernel.org/doc/Documentation/sysctl/fs.txt)

### hsperfdata

[https://github.com/njwhite/telegraf/tree/master/plugins/inputs/hsperfdata](https://github.com/njwhite/telegraf/tree/master/plugins/inputs/hsperfdata)

### windows

```bash
    choco install telegraf
```

#### 配置文件

```bash
    C:\Program Files\telegraf\telegraf.conf
```

#### install as windows serivce, choco 安装的 telegraf 默认会安装成 service

[https://docs.influxdata.com/telegraf/v1.14/administration/windows_service/](https://docs.influxdata.com/telegraf/v1.14/administration/windows_service/)

```bash
    C:\"Program Files"\Telegraf\telegraf.exe --service install
    net start telegraf
```

### telegraf influxdb_listener

```bash
vim  /etc/telegraf/telegraf.conf
[[outputs.influxdb]]
  urls = ["http://influxdb.wiloon.com"]
  database = "database0"

[[inputs.influxdb_listener]]
  service_address = ":8086"
  read_timeout = "10s"
  write_timeout = "10s"
  max_body_size = 0
```

### ping plugin

[https://github.com/influxdata/telegraf/blob/release-1.10/plugins/inputs/ping/README.md](https://github.com/influxdata/telegraf/blob/release-1.10/plugins/inputs/ping/README.md)

```bash
[[inputs.ping]]
  ## List of urls to ping
  urls = ["example.org"]

  ## Number of pings to send per collection (ping -c <COUNT>)
  # count = 1

  ## Interval, in s, at which to ping. 0 == default (ping -i <PING_INTERVAL>)
  ## Not available in Windows.
  # ping_interval = 1.0

  ## Per-ping timeout, in s. 0 == no timeout (ping -W <TIMEOUT>)
  # timeout = 1.0

  ## Total-ping deadline, in s. 0 == no deadline (ping -w <DEADLINE>)
  # deadline = 10

  ## Interface or source address to send ping from (ping -I <INTERFACE/SRC_ADDR>)
  ## on Darwin and Freebsd only source address possible: (ping -S <SRC_ADDR>)
  # interface = ""

  ## Specify the ping executable binary, default is "ping"
  # binary = "ping"

  ## Arguments for ping command
  ## when arguments is not empty, other options (ping_interval, timeout, etc) will be ignored
  # arguments = ["-c", "3"]
```

### openwrt

#### telegraf, 下载 static 版本

[https://github.com/influxdata/telegraf/releases/tag/v1.19.0](https://github.com/influxdata/telegraf/releases/tag/v1.19.0)  
[https://dl.influxdata.com/telegraf/releases/telegraf-1.19.0_static_linux_amd64.tar.gz](https://dl.influxdata.com/telegraf/releases/telegraf-1.19.0_static_linux_amd64.tar.gz)

mv telegraf-1.19.0/usr/bin/telegraf /usr/bin/
mv telegraf-1.19.0/usr/lib/telegraf /usr/lib
mv telegraf-1.19.0/var/log/*/var/log
mv telegraf-1.19.0/etc/* /etc

#### 配置开机启动

登录到 openwrt web 管理页面, 点击菜单 System > Startup > Local Startup, 在exit0 上面插入一行, 填写以下命令

```bash
    /usr/bin/telegraf --config /etc/telegraf/telegraf.conf
```

### docker

```bash
podman run --rm telegraf telegraf config > telegraf.conf
podman volume create telegraf-config

podman run --name telegraf -d \
    -v telegraf-config:/etc/telegraf:ro \
    -v /etc/localtime:/etc/localtime:ro \
    -p 38080:38080 \
    -p 38186:38186 \
    telegraf

podman run --name telegraf -d \
    -v /:/hostfs:ro \
    -v /etc:/hostfs/etc:ro \
    -v /proc:/hostfs/proc:ro \
    -v /sys:/hostfs/sys:ro \
    -v /var/run/utmp:/var/run/utmp:ro \
    -v telegraf-config:/etc/telegraf:ro \
    -v /etc/localtime:/etc/localtime:ro \
    -e HOST_ETC=/hostfs/etc \
    -e HOST_PROC=/hostfs/proc \
    -e HOST_SYS=/hostfs/sys \
    -e HOST_MOUNT_PREFIX=/hostfs \
    --net=host \
    --restart=always \
    telegraf
```

运行在容器里的 telegraf 监控宿主机资源
[https://www.jacobtomlinson.co.uk/monitoring/2016/06/23/running-telegraf-inside-a-container/](https://www.jacobtomlinson.co.uk/monitoring/2016/06/23/running-telegraf-inside-a-container/)

### wireguard, telegraf

[https://github.com/influxdata/telegraf/blob/master/plugins/inputs/wireguard/README.md](https://github.com/influxdata/telegraf/blob/master/plugins/inputs/wireguard/README.md)

### exec, 执行 shell 脚本

```bash
[[inputs.exec]]
  ## Commands array
  commands = [
    "/data/blog/count.sh"
  ]

  ## Timeout for each command to complete.
  timeout = "60s"

  ## measurement name suffix (for separating different commands)
  name_suffix = "_collector"

  ## Data format to consume.
  ## Each data format has its own unique set of configuration options, read
  ## more about them here:
  # https://github.com/influxdata/telegraf/blob/master/docs/DATA_FORMATS_INPUT.md
  data_format = "influx"
```

#### count.sh

```bash
#!/bin/sh
cd /data/blog/wiloon.com
git pull>/dev/null
post_count=$(ls -lR content/post |grep '\.md'|wc -l)
word_count=$(ls -lR content/post |grep '\.md'|wc -m)

echo 'blog,domain=wiloon post_count='''$post_count'''i,word_count='''$word_count'''i'
```

telegraf 默认用 tellegraf 用户启动, 所以... 记得给脚本加执行权限.

[https://github.com/influxdata/telegraf/blob/release-1.21/plugins/inputs/exec/README.md](https://github.com/influxdata/telegraf/blob/release-1.21/plugins/inputs/exec/README.md)
