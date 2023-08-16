---
title: android 自动充电
author: "-"
date: 2022-06-22 12:19:23
url: android/auto/charge
categories:
  - Inbox
tags:
  - reprint
---
## android 自动充电

## Chanify 消息推送工具

<https://github.com/chanify/chanify-ios/blob/main/README-zh_CN.md>

```bash
# sample
podman run -it \
-v /my/data:/root/.chanify \
wizjin/chanify:latest \
serve --name=<node name> --endpoint=http://<address>:<port>

# podman
podman run -it \
-d --name chanify \
-p 30080:80 \
-v chanify-data:/root/.chanify \
wizjin/chanify:latest \
serve --name=chanify0 --endpoint=https://chanify.wiloon.com

# docker
docker run -it -d \
--name chanify \
--restart=always \
-p 30080:80 \
-v chanify-data:/root/.chanify \
wizjin/chanify:latest \
serve --name=chanify0 --endpoint=https://chanify.wiloon.com
```

启动服务配置好 nginx 之后, 在浏览器访问 `https://chanify.wiloon.com`, 能看到 endpoint 的二维码, 用 iOS chanify 客户端扫二维码添加节点. 切换到频道, 在频道上左滑查看 token

## 用自建的服务器发消息

```bash
curl --form-string "text=hello" "http://chanify.wiloon.com/v1/sender/<token>"
curl "http://chanify.wiloon.com/v1/sender/<token>/msg0"
```

## 礼信通4芯数据传输 USB 定时开关遥控制器延长线智能 WIFI 电源数据

<https://item.taobao.com/item.htm?spm=a1z09.2.0.0.3b462e8dwgAuy1&id=675291964059&_u=m2lc6g03a41>

### 查看控制指令 URL

用微信扫二维码, 操作开关之后, 点击页面上的绿色图标, URL会被复制到剪贴板, 格式是这样的  `http://saygift.qlkkj.net/oder?Qd=<key>&sw=1&od=op`, od=op: 开, od=cs: 关

用 curl 测试一下

```bash
# 开
curl -v "http://saygift.qlkkj.net/oder?Qd=<key>&sw=1&od=op"
# 关
curl -v "http://saygift.qlkkj.net/oder?Qd=<key>&sw=1&od=cs"
```

## MacroDroid

<https://www.macrodroid.com/>

android 机 安装 MacroDroid, 配置规则电池电量低于 30%

1. 发消息到 chanify `https://chanify.wiloon.com/v1/sender/<token>/foo`
2. 发http请求 `http://saygift.qlkkj.net/oder?Qd=<key>=1&od=op` 开始充电

## scrcpy, 显示并控制通过 USB (或 TCP/IP) 连接的安卓设备

<https://github.com/Genymobile/scrcpy/blob/master/README.zh-Hans.md>

## iPhone 自动充电

```bash
sudo pacman -S python-setuptools
sudo pacman -S python-packaging
sudo pacman -S python-ordered-set
python-more-itertools
python-jaraco.functools
python-jaraco.text
python-jaraco.context
python-six
python-jinja
python-markupsafe
python-cryptography
openssl
yay -S python-miio
```

<https://www.leavesongs.com/THINK/iOS-with-chuangmiplug-smart-plug2.html>
