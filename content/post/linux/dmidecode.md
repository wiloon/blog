---
title: 'Dmidecode,在 Linux 下获取硬件信息'
author: lcf
date: 2012-09-25T05:35:24+00:00
url: dmidecode
categories:
  - Linux
tags:
  - reprint
---
## 'Dmidecode,在 Linux 下获取硬件信息'

[http://linuxtoy.org/archives/dmidecode.html](http://linuxtoy.org/archives/dmidecode.html)

Dmidecode 应该在主流的 Linux 发行版中都可以找到，因此你只需通过所用发行版的包管理器安装即可，如:

```bash
pacman -S dmidecode # Arch Linux
emerge -av dmidecode # Gentoo
aptitude install dmidecode # Debian/Ubuntu
yum install dmidecode # Fedora
```

不带选项执行 `dmidecode` 通常会输出所有的硬件信息，以下是在笔者机器上执行 dmidecode 后所得到的结果 (部分) :

```bash
# dmidecode 2.10

SMBIOS 2.3 present.
26 structures occupying 1285 bytes.
Table at 0x000FC010.

Handle 0x0000, DMI type 0, 24 bytes
BIOS Information
        Vendor: American Megatrends Inc.
        Version: 080012
        Release Date: 02/06/2007
        Address: 0xF0000
        Runtime Size: 64 kB
        ROM Size: 512 kB
        ...
```

Dmidecode 有个很有用的选项 -t，可以按指定类型输出相关信息，假如要获得处理器方面的信息，则可以执行

```bash
    dmidecode -t processor 
```

输出:

```bash
# dmidecode 2.10

SMBIOS 2.3 present.

Handle 0x0004, DMI type 4, 35 bytes
Processor Information
        Socket Designation: CPU 1
        Type: Central Processor
        Family: Unknown
        Manufacturer: Intel
        ID: F2 06 00 00 FF FB EB BF
        Version: Genuine Intel(R) CPU            2140  @ 1.60GHz
        Voltage: 1.3 V
        External Clock: 200 MHz
        Max Speed: 1600 MHz
        Current Speed: 1600 MHz
        Status: Populated, Enabled
        Upgrade: Other
        L1 Cache Handle: 0x0005
        L2 Cache Handle: 0x0006
        L3 Cache Handle: 0x0007
        Serial Number: To Be Filled By O.E.M.
        Asset Tag: To Be Filled By O.E.M.
        Part Number: To Be Filled By O.E.M.
```

关于 Dmidecode 的更多用法，你可以通过指定 -h 选项查询。

## 查看 内存 个数, list memory slot

```bash
dmidecode|grep -P -A5 "Memory\s+Device"|grep Size|grep -v Range

```

[https://blog.csdn.net/yongqingcloud/article/details/8489710](https://blog.csdn.net/yongqingcloud/article/details/8489710)

[https://blog.csdn.net/BeautyGao/article/details/51538650](https://blog.csdn.net/BeautyGao/article/details/51538650)