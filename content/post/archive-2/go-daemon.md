---
title: go daemon – systemd
author: "-"
date: 2017-11-10T08:32:33+00:00
url: /?p=11407
categories:
  - Inbox
tags:
  - reprint
---
## go daemon – systemd

build executable file

create systemd unit config file /usr/lib/systemd/system/foo

add following lines

[Unit]
  
Description=foo

[Service]
  
User=root
  
Group=root
  
Restart=on-failure
  
ExecStart=/path/to/execfile/foo

[Install]
  
WantedBy=multi-user.target

<https://vincent.bernat.im/en/blog/2017-systemd-golang>
  
<https://serversforhackers.com/c/process-monitoring-with-systemd>

<https://fabianlee.org/2017/05/21/golang-running-a-go-binary-as-a-systemd-service-on-ubuntu-16-04/>

<http://shanks.leanote.com/post/Go%E5%88%9B%E5%BB%BAdaemon%E7%A8%8B%E5%BA%8F>

    Monit and CentOS - Solving the Error "Could not execute systemctl"
  