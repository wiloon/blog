---
title: openwrt mirror
author: w1100n
type: post
date: 2018-10-28T15:48:43+00:00
url: /?p=12831
categories:
  - Uncategorized

---
edit /etc/opkg/distfeeds.conf

```bash
  
src/gz openwrt_core http://openwrt.proxy.ustclug.org/releases/18.06.1/targets/ipq806x/generic/packages
  
src/gz openwrt\_base http://openwrt.proxy.ustclug.org/releases/18.06.1/packages/arm\_cortex-a15_neon-vfpv4/base
  
src/gz openwrt\_packages http://openwrt.proxy.ustclug.org/releases/18.06.1/packages/arm\_cortex-a15_neon-vfpv4/packages
  
src/gz openwrt\_routing http://openwrt.proxy.ustclug.org/releases/18.06.1/packages/arm\_cortex-a15_neon-vfpv4/routing
  
src/gz openwrt\_telephony http://openwrt.proxy.ustclug.org/releases/18.06.1/packages/arm\_cortex-a15_neon-vfpv4/telephony
  
```

```bash
  
\# backup
  
src/gz openwrt_core http://downloads.openwrt.org/releases/18.06.1/targets/ipq806x/generic/packages
  
src/gz openwrt\_base http://downloads.openwrt.org/releases/18.06.1/packages/arm\_cortex-a15_neon-vfpv4/base
  
src/gz openwrt\_packages http://downloads.openwrt.org/releases/18.06.1/packages/arm\_cortex-a15_neon-vfpv4/packages
  
src/gz openwrt\_routing http://downloads.openwrt.org/releases/18.06.1/packages/arm\_cortex-a15_neon-vfpv4/routing
  
src/gz openwrt\_telephony http://downloads.openwrt.org/releases/18.06.1/packages/arm\_cortex-a15_neon-vfpv4/telephony
  
```

https://openwrt.proxy.ustclug.org/

https://mirrors.ustc.edu.cn/help/lede.html