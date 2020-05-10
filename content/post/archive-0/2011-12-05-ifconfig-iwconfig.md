---
title: ifconfig, iwconfig
author: wiloon
type: post
date: 2011-12-05T13:44:32+00:00
url: /?p=1806
views:
  - 7
bot_views:
  - 4
categories:
  - Linux
  - Network

---
<http://www.linuxquestions.org/questions/linux-wireless-networking-41/ifconfig-vs-iwconfig-268525/>

iwconfig only deals with the wireless elements of a wireless card: the ESSID, WEP keys, etc. All the normal attributes of the network card (IP address, subnet mask etc) are assigned through ifconfig. The two utilities don&#8217;t overlap, and both are required to use the card (unless you&#8217;re using dhclient, in which case you won&#8217;t have to use ifconfig directly).