---
title: chromeos basic
author: w1100n
type: post
date: 2018-11-03T15:08:31+00:00
url: /?p=12855
categories:
  - Uncategorized

---
### cpu mem monitor
    chrome://sys-internals/
### openvpn
https://docs.google.com/document/d/18TU22gueH5OKYHZVJ5nXuqHnk2GN6nDvfu2Hbrb4YLE/pub#h.bta4pj6t7nhs


your profile can not be used... ...

rm -rf /home/wiloon/.config/google-chrome/Default

### STATUS_INVALID_IMAGE_HASH

Google 在79版本（2019年12月20号左右）的更新中又重新启用了Renderer Code Integrity Protection（渲染器代码完整性保护），会阻止签名不是谷歌和微软的模块加载浏览器。目前更新的谷歌浏览器版本仍未对该问题进行修复，希望后续更新的版本能解决这个问题。

解决方法：禁用谷歌chrome的这项功能

修改注册表

    Windows Registry Editor Version 5.00

    [HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Google\Chrome]
    "RendererCodeIntegrityEnabled"=dword:00000000


---

https://zhuanlan.zhihu.com/p/133243870