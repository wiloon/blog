---
title: chrome os, chromeos basic
author: "-"
date: 2018-11-03T15:08:31+00:00
url: /?p=12855
categories:
  - chrome
tags:
  - reprint
---
## chrome os, chromeos basic

### chrome os 多桌面

[https://support.google.com/chromebook/answer/9594869?hl=en](https://support.google.com/chromebook/answer/9594869?hl=en)

Drag windows and apps to your preferred desk.
Or use shortcuts:
Move a window to a new desk: Right-click the top of a window then, select Move window to another desk.
Make a window or app available across all desks: Right-click the top of a window, then select Show in all desks.

### crosh

Crosh stands for “Chrome Shell,” and it lets you run commands that usually don’t have graphical tools. You can do things like installing Crouton for a full Linux OS on your Chromebook or checking the device’s battery health—more “advanced” stuff, to put it crudely. If you’ve ever used the Command Prompt or PowerShell on Windows, Crosh is Chrome OS’ version of that tool.

#### 进入crosh环境

```bash
    ctrl+t
```

#### 管理 linux 虚拟机

```bash
vmc list
vmc start termina
vmc stop termina
```

#### crosh 命令

- top
- ping
shell: 打开一个完整的bash shell。
systrace: 启动系统跟踪。
packet_capture: 捕获并记录数据包。
network_diag
tracepath
help
exit

### cpu mem monitor

    chrome://sys-internals/

### openvpn

[https://docs.google.com/document/d/18TU22gueH5OKYHZVJ5nXuqHnk2GN6nDvfu2Hbrb4YLE/pub#h.bta4pj6t7nhs](https://docs.google.com/document/d/18TU22gueH5OKYHZVJ5nXuqHnk2GN6nDvfu2Hbrb4YLE/pub#h.bta4pj6t7nhs)

your profile can not be used... ...

rm -rf /home/wiloon/.config/google-chrome/Default

### STATUS_INVALID_IMAGE_HASH

Google 在79版本 (2019年12月20号左右) 的更新中又重新启用了Renderer Code Integrity Protection (渲染器代码完整性保护) ,会阻止签名不是谷歌和微软的模块加载浏览器。目前更新的谷歌浏览器版本仍未对该问题进行修复,希望后续更新的版本能解决这个问题。

解决方法: 禁用谷歌chrome的这项功能

修改注册表

    Windows Registry Editor Version 5.00

    [HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Google\Chrome]
    "RendererCodeIntegrityEnabled"=dword:00000000

### 快捷键

    https://support.google.com/chromebook/answer/183101

---

[https://zhuanlan.zhihu.com/p/133243870](https://zhuanlan.zhihu.com/p/133243870)

[https://www.pcpc.me/tech/terminal-commands-chromebook](https://www.pcpc.me/tech/terminal-commands-chromebook)

[https://zh.omatomeloanhikaku.com/how-is-crosh-different-than-the-linux-terminal-on-a-chromebook-935](https://zh.omatomeloanhikaku.com/how-is-crosh-different-than-the-linux-terminal-on-a-chromebook-935)
