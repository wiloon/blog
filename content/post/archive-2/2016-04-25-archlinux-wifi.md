---
title: archlinux netctl wifi
author: wiloon
type: post
date: 2016-04-25T06:39:09+00:00
url: /?p=8945
categories:
  - Uncategorized

---
<div class="article_title">
</div>

<div class="article_manage clearfix">
</div>

<div id="article_content" class="article_content">
  <p>
    # Essay Address: http://blog.csdn.net/sunnypotter/article/details/23201339
  </p>
  
  <p>
    
  </p>
  
  <p>
    # 如果之前systemctl enable dhcpcd.service<br /> systemctl dhcpcd.service<br /> systemctl disable dhcpcd.service<br /> # 然后<br /> cd /etc/netctl<br /> cp examples/wireless-wpa .    # A simple WPA encrypted wireless connection<br /> vim wireless-wpa    # Modify<br /> + Interface=wlp8s0 # iw dev查看, 或ip link 或ifconfig<br /> + Connection=wireless<br /> + Security=wpa<br /> +<br /> + IP=dhcp<br /> + ESSID=&#8217;wifi-name&#8217;<br /> + Key=&#8217;wifi-passwd&#8217;<br /> # 注意，必须先完成以上才能进行一下，否则有一系列问题<br /> netctl enable wireless-wpa<br /> netctl start wireless-wpa<br /> reboot<br /> (<br /> 相关文件夹: /etc/netctl # 网络配置文件夹,假如配置名字叫 wireless-wpa<br /> /etc/systemd/system #<br /> /etc/systemd/system  # netctl@wireless-wpa.service<br /> /etc/systemd/system/multi-user.target.wants # netctl@wireless-wpa.service<br /> 相关命令:<br /> journalctl -xn<br /> systemctl &#8211;failed<br /> systemctl list-unit-files<br /> systemctl daemon-reload
  </p>
  
  <p>
    ip link<br /> ifconfig wlp8s0 up  # start wireless adapter<br /> ifconfig eno1 up # start wire adapter
  </p>
  
  <p>
    # dhcpcd network-adapter 动态分配IP<br /> dhcpcd eno1<br /> dhcpcd wlp8s0<br /> )
  </p>
</div>