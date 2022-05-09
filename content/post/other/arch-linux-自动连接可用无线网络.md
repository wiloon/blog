---
title: Arch Linux 自动连接可用无线网络
author: "-"
date: 2015-05-02T23:46:55+00:00
url: /?p=7577
categories:
  - Inbox
tags:
  - Arch Linux

---
## Arch Linux 自动连接可用无线网络
本文来自依云's Blog，转载请注明。

Arch Linux 连接网络可以使用其官方开发的 netctl 系列命令行工具。要想在开机 (以及从挂起/休眠状态唤醒) 时自动连接到可用的无线网络，以下是设置步骤。

首先，你得告诉 Arch Linux 你知道哪些无线热点。Arch Linux 不会自动帮你破解别人的 Wi-Fi 密码的。就算 Wi-Fi 热点没有加密，你不说 Arch Linux 怎么知道它应当连接到那个热点呢，也许那是个钓鱼用的热点也说不定哦。

cd 到 /etc/netctl 目录下，可以看到 examples 目录下有一堆示例配置。复制你所需要的配置文件到上一层目录 (/etc/netctl) 。比如绝大多数 Wi-Fi 热点使用的是 WPA 加密，那就复制 examples/wireless-wpa 文件。目标文件名比较随意，起个方便自己的名字就行，比如 work、home 之类的。复制完成之后记得 chmod 600 禁止非 root 用户访问，因为配置文件里会包含你的 Wi-Fi 热点密码。

然后编辑配置文件，修改 ESSID 和 Key 为你的 Wi-Fi 热点 ID 和密码就可以了。之所以要先更改权限再编辑，是因为某些编辑器 (如 Vim) 会生成同权限的备份文件；那里有可能也会包含密码。可以放多份配置文件在这里，netctl-auto 默认会去找一个可用的连接。有多个可用的时候不太清楚它会连上哪一个，可以使用更复杂的配置文件来指定优先级 (参见 examples/wireless-wpa-configsection 示例配置) 。

配置文件写好之后，当然是启动相应的服务啦。Arch Linux 一贯的传统是不启动不必要的服务，除非用户说要启动之。netctl-auto 的 systemd 服务名是 netctl-auto@interface.service (当然 .service 后缀还是可以省略的) 。interface 部分写你的无线网络接口的名字，可以通过 ip link、ifconfig、iwconfig 等命令看到。我禁用了 systemd 的可预测网络接口名称，所以我的无线网络接口名唤 wlan0。我使用如下命令启动服务: 
  
$ sudo systemctl start netctl-auto@wlan0.service
  
如果一切顺利的话一小会儿之后就应该连上网了: 
  
$ systemctl status netctl-auto@wlan0.service
  
● netctl-auto@wlan0.service - Automatic wireless network connection using netctl profiles
  
Loaded: loaded (/usr/lib/systemd/system/netctl-auto@.service; enabled)
  
Active: active (running) since 二 2014-09-02 20:23:31 CST; 2h 45min ago
  
Docs: man:netctl.special(7)
  
Process: 340 ExecStart=/usr/bin/netctl-auto start %I (code=exited, status=0/SUCCESS)
  
CGroup: /system.slice/system-netctl\x2dauto.slice/netctl-auto@wlan0.service
  
├─402 wpa_supplicant -B -P /run/wpa_supplicant_wlan0.pid -i wlan0 -D nl80211,wext -c/run/network/wpa_supplicant_wlan0.conf -W
  
├─404 wpa_actiond -p /run/wpa_supplicant -i wlan0 -P /run/network/wpa_actiond_wlan0.pid -a /usr/lib/network/auto.action
  
└─501 dhcpcd -4 -q -t 30 -K -L wlan0
  
...
  
或者通过 netctl-auto list 命令也可以看到连接上了哪个配置文件里指定的热点。

如果满意的话，就让它开机自启动啦: 
  
$ sudo systemctl enable netctl-auto@wlan0.service
  
参考资料: ArchWiki 上的 netctl 条目。