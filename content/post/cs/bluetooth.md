---
title: 蓝牙配对
author: "-"
date: 2011-12-24T06:24:13+00:00
lastmod: 2026-05-28T09:54:13+08:00
url: bluetooth
categories:
  - cs
tags:
  - bluetooth
  - archlinux
  - remix
  - AI-assisted
---
## Arch Linux 蓝牙连接键盘

### 环境

- 设备：SER8（AMD 小主机）
- 系统：Arch Linux + KDE
- 问题：KDE 系统设置蓝牙页面无法发现蓝牙键盘

### 排查过程

```bash
# 检查蓝牙服务状态
systemctl status bluetooth
# → inactive (dead)，且 disabled

# 检查硬件是否被识别
ls /sys/class/bluetooth/
# → hci0（硬件正常识别）

# 检查软件包
pacman -Q bluez bluedevil
# → bluez 5.86-6 / bluedevil 1:6.6.5-1（已安装）
```

### 根本原因

蓝牙硬件正常、驱动正常、软件包齐全，但 `bluetooth.service` 从未被启用，导致 KDE 蓝牙面板无法扫描任何设备。

### 解决方法

```bash
# 启动蓝牙服务并设置开机自启
sudo systemctl enable --now bluetooth

# 可选：安装命令行调试工具
sudo pacman -S bluez-utils
```

服务启动后，打开 KDE 系统设置 → 蓝牙，将键盘置于配对模式，即可正常发现并配对。

---

## 蓝牙配对
四中配对模式: Numeric Comparison, Just Works, Out of Band and Passkey Entry。

- Numeric Comparison：配对双方都显示一个6位的数字，由用户来核对数字是否一致，一致即可配对。例如手机之间的配对。
- Just Works：用于配对没有显示没有输入的设备，主动发起连接即可配对，用户看不到配对过程。例如连接蓝牙耳机。
- Passkey Entry：要求配对目标输入一个在本地设备上显示的6位数字，输入正确即可配对。例如连接蓝牙键盘。
- Out of Band：两设备的通过别的途径交换配对信息，例如NFC等。例如一些NFC蓝牙音箱。

蓝牙连接需要安全加密，就涉及密钥的生成以及身份认证，通过配对完成这个过程中的交互。

###  Classic
这四种配对方式，除开JUSTWORK外，都可以防止这两种攻击。JUSTWORK由于不涉及人机交互，所以没法防止中间人攻击(MITM)。 
(插一句，传统蓝牙的PIN CODE配对方式就是由于无法防止被动监听攻击 (穷举PIN码）才衍生了这四种SSP简单配对方式。）

BLE中LE配对分为4.0版本中的LE LEGACY配对方式以及在BLE4.2版本开始导入的 BLE Secure Connection 配对方式。 
前者LEGACY中，配对方式三种，JUSTWORK，PASSKEY ENTRY，以及OOB，JUSTWORK依然无法防止MITM，另外由于秘钥生成方式的缺陷，导致LE LEGACY配对方式无法防止被动监听攻击 (OOB可以防止，因为用了非空中的传输交互）正因为此，BLE4.2版本把Secure connection也引入到了BLE中 (为什么说也，是因为CLASSIC模式中也有SECURE CONNECTION方式...），BLE Secure connection和CLASSIC 的SSP采用同样的ECDH加密方式，所以安全性恢复到同样等级，可以防止被动监听攻击了。

BLE SECURE CONNECTION配对又有了四种配对模式，JUSTWORK，PASSKEY ENTRY，NUMERIC COMP.，以及OOB，同样类同于SSP，JUSTWORK防止不了MITM。以上内容，去蓝牙SPEC4.2及其以后版本里头查阅，大概可以弄清楚。总之，用简单的话来说，配对目的就防止两种攻击，被动监听和MITM，防止MITM需要人机交互操作，所以所有的JUSTWORK都没法防止这种攻击。被动监听目前采用非对称加解密方式，即可破解，所以采用EDCH的SSP以及LE SECURE CONNECTION都能防止这种攻击。

作者：城市牧场
链接：https://www.zhihu.com/question/29076831/answer/201659080
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

作者：何新宇
链接：https://www.zhihu.com/question/29076831/answer/43387340
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。



>https://www.zhihu.com/question/29076831