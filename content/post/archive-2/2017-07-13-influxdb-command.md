---
title: 'influxdb install & config'
author: wiloon
type: post
date: 2017-07-13T08:21:48+00:00
url: /?p=10830
categories:
  - Uncategorized

---
### dnf

```bash
sudo tee  /etc/yum.repos.d/influxdb.repo<<EOF
[influxdb]
name = InfluxDB Repository
baseurl = https://repos.influxdata.com/rhel/7/x86_64/stable/
enabled = 1
gpgcheck = 1
gpgkey = https://repos.influxdata.com/influxdb.key
EOF
dnf install influxdb
vim /etc/influxdb/influxdb.conf
systemctl enable influxdb

```

```bash
# install
# archlinux
yaourt -S influxdb

# centos
# https://www.influxdata.com/blog/package-repository-for-linux/
sudo yum install influxdb
sudo yum localinstall influxdb-1.2.4.x86_64.rpm

# for Linux Binaries (64-bit)
tar xvfz influxdb-1.3.1_linux_amd64.tar.gz
rsync -r /path/to/influxdb-1.2.4-1/ /

#edit config file
emacs /etc/influxdb/influxdb.conf
```

#reporting-disabled = false

[meta]
  
dir = "/var/lib/influxdb/meta&#8221;
  
#retention-autocreate = true

[data]
  
dir = "/var/lib/influxdb/data&#8221;
  
wal-dir = "/var/lib/influxdb/wal&#8221;
  
wal-fsync-delay = "0s&#8221;

# index-version = "inmem&#8221;

index-version = "tsi1&#8221;

trace-logging-enabled = false
  
query-log-enabled = true
  
cache-max-memory-size = "512m&#8221;
  
cache-snapshot-memory-size = "32m&#8221;

# 超过10分钟没有写入, 把cache写到新的TSM文件

cache-snapshot-write-cold-duration = "10m&#8221;

[coordinator]
  
#慢查询
  
log-queries-after = "10s&#8221;

[retention]

#edit file /etc/default/influxdb
  
STDERR=/data/logs/influxdb/influxdb.log

#edit logrotate config, modify log path
  
/etc/logrotate.d/influxdb

```bash
# chown
chown influxdb:influxdb /data/influxdb/
chown influxdb:influxdb /data/logs/influxdb/

#start
systemctl start influxdb
#or
sudo influxd

#connect via cli, rfc3339：日期格式YYYY-MM-DDTHH:MM:SS.nnnnnnnnnZ
influx -precision rfc3339



```