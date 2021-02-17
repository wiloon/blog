+++
author = "w1100n"
date = "2021-02-17 13:32:57" 
title = "network"

+++

### 策略路由
    iptables -t mangle -N XRAY
    iptables -t mangle -A XRAY -p tcp -j TPROXY --on-port 12345 --tproxy-mark 1
    iptables -t mangle -A XRAY -p udp -j TPROXY --on-port 12345 --tproxy-mark 1
    iptables -t mangle -A PREROUTING -j XRAY
    
    ip rule add fwmark 1 table 100
    ip route add local 0.0.0.0/0 dev lo table 100
