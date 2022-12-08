---
title: linux 时区，时间
author: lcf
date: 2012-09-24T08:38:55+00:00
url: /?p=4224
categories:
  - Linux
tags:
  - reprint
---
## linux 时区，时间

```bash
#把硬件时间设置成系统时间
hwclock --hctosys

#把系统时间设置成硬件
hwclock --systohc

#设置硬件时间
hwclock --set --date="mm/dd/yy hh:mm:ss"

#修改系统时间
date -s "dd/mm/yyyy hh:mm:ss"
```

### CentOS 7 时区设置

在 CentOS 7 中, 引入了一个叫 timedatectl 的设置设置程序.

```bash
# 查看系统时间方面的各种状态
timedatectl status
# 列出所有时区
timedatectl list-timezones
# 设置系统时区为上海
timedatectl set-timezone Asia/Shanghai 
```

timedatectl set-local-rtc 1 # 将硬件时钟调整为与本地时钟一致, 0 为设置为 UTC 时间

其实不考虑各个发行版的差异化, 从更底层出发的话, 修改时间时区比想象中要简单:

cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

Linux时钟分为系统时钟 (System Clock) 和硬件 (Real Time Clock，简称RTC) 时钟。系统时钟是指当前Linux Kernel中的时钟，而硬件时钟则是主板上由电池供电的时钟，这个硬件时钟可以在BIOS中进行设置。当Linux启动时，硬件时钟会去读取系统时钟的设置，然后系统时钟就会独立于硬件运作。

Linux中的所有命令 (包括函数) 都是采用的系统时钟设置。在Linux中，用于时钟查看和设置的命令主要有date、hwclock和clock。其中，clock和hwclock用法相近，只用一个就行，只不过clock命令除了支持x86硬件体系外，还支持Alpha硬件体系。

1. date

查看系统时间

date

设置系统时间
  
```bash
  
sudo date -set "09/12/2012 10:19"  (月/日/年时:分:秒) 
  
sudo date -set "08/31/2012 10:19"
  
```
  
1. hwclock/clock

查看硬件时间

hwclock -show

或者# clock -show

设置硬件时间

hwclock -set -date="07/07/06 10:19"  (月/日/年 时:分:秒)

或者# clock -set -date="07/07/06 10:19"  (月/日/年 时:分:秒)

1. 硬件时间和系统时间的同步

按照前面的说法，重新启动系统，硬件时间会读取系统时间，实现同步，但是在不重新启动的时候，需要用hwclock或clock命令实现同步。

硬件时钟与系统时钟同步: # hwclock -hctosys (hc代表硬件时间，sys代表系统时间) 或者# clock -hctosys

系统时钟和硬件时钟同步: # hwclock -systohc或者# clock -systohc

时区的设置

tzselect

Please identify a location so that time zone rules can be set correctly.Please select a continent or ocean. 1) Africa 2) Americas 3) Antarctica 4) Arctic Ocean 5) Asia 6) Atlantic Ocean 7) Australia 8) Europe 9) Indian Ocean10) Pacific Ocean11) none - I want to specify the time zone using the Posix TZ format.#? 输入5，亚洲

Please select a country. 1) Afghanistan 18) Israel 35) Palestine 2) Armenia 19) Japan 36) Philippines 3) Azerbaijan 20) Jordan 37) Qatar 4) Bahrain 21) Kazakhstan 38) Russia 5) Bangladesh 22) Korea (North) 39) Saudi Arabia 6) Bhutan 23) Korea (South) 40) Singapore 7) Brunei 24) Kuwait 41) Sri Lanka 8) Cambodia 25) Kyrgyzstan 42) Syria 9) China 26) Laos 43) Taiwan10) Cyprus 27) Lebanon 44) Tajikistan11) East Timor 28) Macau 45) Thailand12) Georgia 29) Malaysia 46) Turkmenistan13) Hong Kong 30) Mongolia 47) United Arab Emirates14) India 31) Myanmar (Burma) 48) Uzbekistan15) Indonesia 32) Nepal 49) Vietnam16) Iran 33) Oman 50) Yemen17) Iraq 34) Pakistan#? 输入9，中国

Please select one of the following time zone regions.1) east China - Beijing, Guangdong, Shanghai, etc.2) Heilongjiang3) central China - Gansu, Guizhou, Sichuan, Yunnan, etc.4) Tibet & most of Xinjiang Uyghur5) southwest Xinjiang Uyghur#? 输入1，北京时间

The following information has been given:

China east China - Beijing, Guangdong, Shanghai, etc.

Therefore TZ="Asia/Shanghai" will be used.Local time is now: Fri Jul 7 10:32:18 CST 2006.Universal Time is now: Fri Jul 7 02:32:18 UTC 2006.Is the above information OK?1) Yes2) No#? 输入1，确认

如果不用tzselect命令，可以修改文件变更时区。

vi /etc/sysconfig/clock ZONE=Asia/Shanghai (查/usr/share/zoneinfo下面的文件)  UTC=false ARC=false

rm /etc/localtime

ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

重新启动即可。

<http://www.cnblogs.com/zhangeamon/p/5500744.html>
