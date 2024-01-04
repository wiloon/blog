---
title: 使用 arpalert 来做被动式arp防火墙
author: "-"
date: 2012-09-19T23:55:18+00:00
url: /?p=4111
categories:
  - Linux
  - Network
tags:
  - reprint
---
## 使用 arpalert 来做被动式arp防火墙
[http://forum.ubuntu.org.cn/viewtopic.php?f=116&t=110347&sid=ae4c75fe6a8b5aa1672e8a05bc6f7d85](http://forum.ubuntu.org.cn/viewtopic.php?f=116&t=110347&sid=ae4c75fe6a8b5aa1672e8a05bc6f7d85)

我说的被动式是指在探测到欺骗时做出防护动作

在局域网环境中 arp 欺骗是个很头疼的问题, 尤其是网关不是自己控制的时候. 虽然自己可以绑定网关, 但是网关就没办法了. 结果导致网关的东西传不回来, 无法上网.

原理:
  
arpalert 监听网卡收到的 arp 包, 并根据规则(黑白名单等)调用一个防护脚本.

安装:
  
安装以下包:
  
libnet-arp-perl arpalert(建议用最新的 2.0.11 版, 2.0.10 前的版本处理名单时有问题)
  
另外将以下文本存为 /usr/local/sbin/arpdef.pl
  
加上可执行权限(755)

[perl]
  
#!/usr/bin/perl -w

use strict;
  
if ( $< ) {
  
print "$0n";
  
system("sudo",($0,@ARGV));
  
exit;
  
}

my $mac = $ARGV[0];
  
my $ip = $ARGV[1];

my ($gateip,$gatemac) = ("192.168.6.1","00:04:80:FA:3C:00");
  
exit 0 if (("U$mac" eq "U$gatemac") && ($ip eq $gateip));

#logging ..
  
my $date=\`date +"%F %T"\`;
  
chomp $date;
  
open (LOGFILE,">>/home/autumncat/log/arpdef.log");
  
if ( 4 <= $#ARGV ) {
  
printf LOGFILE "%s    %s %15s %15s %6s %d (%s)n",($date,@ARGV,"Null");
  
} else {
  
printf LOGFILE "%s    manual executing.n",$date;
  
}
  
close LOGFILE;

#correct gateway
  
# if (("U$ip" eq $gateip)&&("U$mac" ne $gatemac)) {
  
# send arp
  
use Net::ARP;
  
use Time::HiRes qw( usleep );
  
my $ival = 40000;
  
my $time = 60 * 1000000; #total time = 30sec
  
for (my $i=0;$i<$time;$i+=$ival) {
  
Net::ARP::send_packet(
  
'eth0',
  
"192.168.6.28", #my ip
  
$gateip,
  
"00:1A:4D:93:3D:44", # my mac
  
$gatemac,
  
'reply');
  
usleep($ival);
  
}
  
# }
  
[/perl]

设置
  
修改 /etc/arpalert/arpalert.conf
  
(调整了一下)

```bash
  
#
  
# Copyright (c) 2005-2010 Thierry FOURNIER
  
# $Id: arpalert.conf.in 690 2008-03-31 18:36:43Z  $
  
#
  
# Default config file
  
#

# white list
  
maclist file = "/etc/arpalert/maclist.allow"

# black list
  
maclist alert file = "/etc/arpalert/maclist.deny"

# dump file
  
maclist leases file = "/var/lib/arpalert/arpalert.leases"

# list of authorized request
  
#auth request file = /etc/arpalert/authrq.conf

# log file
  
log file = "/var/log/arpalert.log"

# pid file
  
lock file = "/var/run/arpalert.pid"

# log level
  
use syslog = false

# log level
  
log level = 6

# user for privilege separation
  
user = arpalert

# rights for file creation
  
umask = 177

# only for debugging: this dump paquet received on standard output
  
dump packet = false

# run the program as daemon ?
  
daemon = false

# minimun time to wait between two leases dump
  
dump inter = 5

#Configure the network for catch only arp request.
  
#The detection type "new_mac" is desactived.
  
#This mode is used for CPU saving if Arpalert is running on a router
  
catch only arp = true

# comma separated interfaces to lesson
  
# if not precised, the soft select the first interface.
  
# by default select the first interface encontered
  
interface = eth0

# script launched on each detection
  
# parameters are:
  
#  - "mac adress of requestor"
  
#  - "ip of requestor"
  
#  - "supp. parm."
  
#  - "ethernet device listening on"
  
#  - "type of alert"
  
#  - optional : "ethernet vendor"
  
# type of alert:
  
# 0: ip change
  
# 1: mac address only detected but not in whithe list
  
# 2: mac address in black list
  
# 3: new mac address
  
# 4: unauthorized arp request
  
# 5: abusive number of arp request detected
  
# 6: ethernet mac address different from arp mac address
  
# 7: global flood detection
  
# 8: new mac adress without ip
  
# 9: mac change
  
action on detect = "/usr/local/sbin/arpdef.pl"

# module launched on each detection
  
mod on detect = ""
  
# this chain is transfered to the init function of module loaded
  
mod config = ""

# script execution timeout (seconds)
  
execution timeout = 10

# maximun simultaneous lanched script
  
max alert = 8

# what data are dumped in leases file
  
dump black list = false
  
dump white list = false
  
dump new address = true

# after this time a mac adress is removed from memory (seconds) (default 1 month)
  
mac timeout = 259200

# after this limit the memory hash is cleaned (protect to arp flood)
  
max entry = 1000000

# this permit to send only one mismatch alert in this time (in seconds)
  
anti flood interval = 0

# if the number of arp request in seconds exceed this value, all alerts are ignored for
  
# "anti flood interval" time
  
anti flood global = 50

# vendor name
  
# add the mac vendor field in logs, alerts script and/or module execution
  
mac vendor file = "/etc/arpalert/oui.txt"
  
log mac vendor = true
  
alert mac vendor = true
  
mod mac vendor = true

# log if the adress is referenced in hash but is not in white list
  
log referenced address = false
  
alert on referenced address = false
  
mod on referenced address = false

# log if the mac adress is in black list
  
log deny address = true
  
alert on deny address = true
  
mod on deny address = true

# log if the adress isn't referenced
  
log new address = true
  
alert on new address = true
  
mod on new address = true

# log if the adress isn't referenced (for mac adress only)
  
log new mac address = true
  
alert on new mac address = true
  
mod on new mac address = true

# log if the ip adress id different from the last arp request with the same mac adress
  
log ip change = true
  
alert on ip change = true
  
mod on ip change = true

# log if the ip adress id different from the last arp request with the same mac adress
  
log mac change = true
  
alert on mac change = true
  
mod on mac change = true

# unauthorized arp request:
  
# log all the request not authorized in auth file
  
log unauth request = false
  
alert on unauth request = false
  
mod on unauth request = false
  
# dont analyse arp request for unknow hosts (not in white list)
  
ignore unknown sender = false
  
# ignore arp request with mac adresse of the lessoned interfaces for the authorizations checks
  
ignore me = true
  
# ignore windows self test
  
ignore self test = false
  
# suspend time method:
  
# 1: ignore all unauth alerts during "anti flood interval" time
  
# 2: ignore only tuple (mac address, ip address) during "anti flood interval" time
  
unauth ignore time method = 2

# log if the number of request per seconds are > "max request"
  
log request abus = true
  
alert on request abus = true
  
mod on request abus = true
  
# maximun request authorized by second
  
max request = 1000000

# log if the ethernet mac address are different than the arp amc address (only for requestor)
  
log mac error = true
  
alert on mac error = true
  
mod on mac error = true

# log if have too many arp request per seconds
  
log flood = false
  
alert on flood   = false
  
mod on flood = true
  
```

sudo visudo
  
加上一行

  代码:


```bash
arpalert ALL=NOPASSWD: /usr/local/sbin/arpdef.pl *
```
