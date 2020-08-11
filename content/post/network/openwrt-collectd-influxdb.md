+++
author = "w1100n"
date = "2020-08-09 18:45:31" 
title = "openwrt collectd influxdb grafana"

+++

### install
    opkg install luci-app-statistics collectd collectd-mod-cpu \
    collectd-mod-interface collectd-mod-iwinfo \
    collectd-mod-load collectd-mod-memory collectd-mod-network collectd-mod-uptime

### enable service
    /etc/init.d/luci_statistics enable
    /etc/init.d/collectd enable

重启openwrt 在菜单 里会多出一项