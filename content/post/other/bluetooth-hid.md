---
title: 蓝牙 HID
author: "-"
date: 2011-08-18T02:19:41+00:00
url: /?p=422
categories:
  - Linux
tags:$
  - reprint
---
## 蓝牙 HID
 The Human Interface Device (HID)定义了蓝牙在人机接口设备中的协议、特征和使用规程。典型的应用包括蓝牙鼠标、蓝牙键盘、蓝牙游戏手柄等。该协议改编自USB HID Protocol。
    
2.一些概念
(1)HID Reports:Bluetooth HID devices支持三种Report：Input, Output, and Feature。
(2)HID建立Control Channel和Interrupt Channel两个通道，report可以在这两条channel上传输，在Control channel上传输的report称为synchronous reports ；在Interrupt channel上传输的report称为asynchronous reports。
(3)Feature reports are always transferred synchronously using GET_REPORT or SET_REPORT requests。
(4)Report Protocol Mode和Boot Protocol Mode。Bluetooth HID Hosts至少支持一种，Bluetooth HID Device则需要支持Report Protocol Mode，并且Report Protocol Mode是Bluetooth HID Device的默认Mode。 


HOG  (HID OVER GATT）
蓝牙4.0的BLE (bluetooth low en）技术

>https://www.zhihu.com/question/23785524
>https://developer.aliyun.com/article/376006