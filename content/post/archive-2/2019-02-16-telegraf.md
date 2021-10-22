---
title: telegraf
author: "-"
date: 2019-02-16T11:08:43+00:00
url: telegraf

---
## telegraf
### archlinux install telegraf
```bash
yay -S telegraf-bin
```

### binary
    https://portal.influxdata.com/downloads/

### 配置文件 vim /etc/telegraf/telegraf.conf
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
  hostname = ""
  omit_hostname = false
[[outputs.influxdb]]
  urls = ["http://influxdb.wiloon.com:8086"]
  database = "db0"

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
```

### hsperfdata
https://github.com/njwhite/telegraf/tree/master/plugins/inputs/hsperfdata

### windows
    choco install telegraf
#### 配置文件 
    C:\Program Files\telegraf\telegraf.conf
    
#### install as windows serivce, choco安装的telegraf默认安装成service了
https://docs.influxdata.com/telegraf/v1.14/administration/windows_service/

    C:\"Program Files"\Telegraf\telegraf.exe --service install
    net start telegraf

### telegraf influxdb_listener
```
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
https://github.com/influxdata/telegraf/blob/release-1.10/plugins/inputs/ping/README.md

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


### openwrt
#### telegraf, 下载 static 版本
https://github.com/influxdata/telegraf/releases/tag/v1.19.0  
https://dl.influxdata.com/telegraf/releases/telegraf-1.19.0_static_linux_amd64.tar.gz

mv telegraf-1.19.0/usr/bin/telegraf /usr/bin/
mv telegraf-1.19.0/usr/lib/telegraf /usr/lib
mv telegraf-1.19.0/var/log/* /var/log
mv telegraf-1.19.0/etc/* /etc

#### 配置开机启动
登录到openwrt web 管理页面, 点击菜单 System > Startup > Local Startup, 在exit0 上面插入一行, 填写以下命令

    /usr/bin/telegraf --config /etc/telegraf/telegraf.conf

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

运行在容器里的telegraf监控宿主机资源
https://www.jacobtomlinson.co.uk/monitoring/2016/06/23/running-telegraf-inside-a-container/


### wireguard
    https://github.com/influxdata/telegraf/blob/master/plugins/inputs/wireguard/README.md
      