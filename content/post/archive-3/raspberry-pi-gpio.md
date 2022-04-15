---
title: raspberry pi gpio
author: "-"
date: 2019-07-09T16:04:46+00:00
url: /?p=14659
categories:
  - Raspberry-Pi
tags:
  - reprint
---
## raspberry pi gpio
继电器: 树莓派的GPIO口是3.3V的，你需要把它转化成5V才能进行控制


  
    Raspberry Pi 的GPIO接口电路
  


http://blog.oa25.org/?p=472&embed=true#?secret=57KOUtczxY

https://www.kidscoding8.com/47249.html

```bash
#使GPIO17从内核空间暴露到用户空间中
sudo echo 17 > /sys/class/gpio/export
#设置GPIO17为输出模式
sudo echo out > /sys/class/gpio/gpio17/direction
#向value文件中输入1，GPIO输出高电平，LED点亮
sudo echo 1 > /sys/class/gpio/gpio17/value
#向value文件中输入0，GPIO输出低电平，LED熄灭
sudo echo 0 > /sys/class/gpio/gpio17/value
#注销GPIO17接口
sudo echo 17 > /sys/class/gpio/unexport
```

```bash
sudo vim ledonoff.sh
echo $1 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio$1/direction
echo 1 > /sys/class/gpio/gpio$1/value
sleep 5 #延时5秒
echo 0 > /sys/class/gpio/gpio$1/value
echo $1 > /sys/class/gpio/unexport

sudo ./ledonoff.sh 17
```

https://zhuanlan.zhihu.com/p/40594358
  
https://www.huanxiangke.com/index.php/blog/post/voice-control-to-transform-ordinary-desk-lamp