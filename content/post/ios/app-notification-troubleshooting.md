---
title: "iPhone App Notification Troubleshooting 收不到通知排查"
author: "-"
date: 2026-10-08T11:13:27+08:00
lastmod: 2026-10-08T11:13:27+08:00
url: iphone-app-notification-troubleshooting
categories:
  - iOS
tags:
  - ios
  - iphone
  - apns
  - notification
  - remix
  - AI-assisted
---

## 现象

手机是 iPhone 15 Pro，上面装了一个即时通讯 App（下文称「某 App」）。有新消息时，锁屏和横幅都没有提示。打开 App 后，顶部会先显示 "Updating"，更新完才能在 App 里看到新消息。

iOS 系统设置里该 App 的通知配置看起来都没问题：

- Allow Notifications 已开启
- Notification Delivery 是 Immediate Delivery
- Background App Refresh 已开启

## 原因分析

打开 App 时显示 "Updating"，说明消息是 App 启动后自己去服务器拉下来的，在这之前推送没有送到手机。

即时通讯类 App 的通知一般走这条链路：App 的服务器把通知发给 Apple Push Notification service（APNs），APNs 再推给手机，App 本身不需要在后台运行。所以问题一般出在两处：服务器没有发推送，或者推送没能经过 APNs 到达手机。

Background App Refresh 控制的是 App 在后台刷新数据，和远程推送基本无关，开不开都不影响通知。

## 检查清单

按常见程度排序，建议依次检查。

### 1. 是否在电脑端或 Web 端同时在线

不少 IM 服务的逻辑是：用户在桌面客户端或 Web 端在线时，就不再给手机发推送，以免同一条消息在多台设备上重复提醒。

- 关掉电脑上的客户端和浏览器里的 Web 页面，然后用另一个账号给自己发一条消息，看锁屏能不能收到
- 在 App 的设备管理页面（通常叫 Devices 或「登录设备」）查看还有哪些会话在线，不用的可以退出

### 2. App 内部的通知设置

iOS 系统设置之外，App 内部往往还有自己的一套通知开关：

- 私聊、群组、频道的通知是否都已打开
- 是否有「重置所有通知设置」之类的选项（如 Reset All Notifications）。这一操作通常会重新向服务器注册推送 token，经常能修好推送
- 登录多个账号时，是否开启了「显示所有账号的通知」
- 具体的会话是否被静音，或者被归档（有的 App 归档会话默认静音）

### 3. iOS 专注模式与锁屏显示

- 专注模式（Focus）：勿扰、睡眠、工作模式是否开着，有没有设置定时自动开启。需要的话把该 App 加到允许列表
- Settings → Notifications → Scheduled Summary：如果 App 被放进定时推送摘要，通知会攒到固定时间才显示
- Settings → Notifications → 该 App：Lock Screen、Notification Center、Banners 三个位置都要勾上

### 4. 网络与代理是否影响 APNs

如果手机上用了 VPN 或分流规则，规则不当会让 APNs 的长连接断掉，推送就到不了。

判断方法是看其他 App（短信、邮件、其他聊天工具）锁屏时能不能正常收到通知。如果别的 App 也收不到或明显延迟，基本可以确定是 APNs 连接的问题。

处理方法：先关掉 VPN 测试；确认是它的问题后，在规则里让 Apple 推送相关的流量直连：

```text
# Apple push service domains
DOMAIN-SUFFIX,push.apple.com,DIRECT
# Apple-owned IP range used by APNs
IP-CIDR,17.0.0.0/8,DIRECT
```

另外，低电量模式（Low Power Mode）和低数据模式（Low Data Mode）也可能让推送变慢，测试时一并关掉。

### 5. 重新注册推送

以上都检查过还不行时：

1. 在 App 内重置通知设置
1. 退出登录后重新登录
1. 删除 App 重新安装，首次打开时弹出的通知权限请求选 Allow

## 排查顺序

1. 关掉电脑端和 Web 端，用另一个账号给自己发消息，看锁屏能否收到。能收到，就是第 1 项的原因
1. 收不到，就在 App 内重置通知设置，并检查 App 内部的通知开关和静音状态
1. 检查专注模式、定时推送摘要和锁屏显示位置
1. 看其他 App 的推送是否正常，判断是否是网络或 VPN 的问题
1. 最后再尝试重新登录或重装 App

## 当前进度

我已经关掉了一个可能在线的桌面端或 Web 端会话，还需要再测试一次。如果之后仍然收不到通知，再按上面第 2 到第 5 项继续检查。
