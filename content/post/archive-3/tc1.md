---
title: TC1
author: "-"
date: 2019-11-02T14:31:04+00:00
url: /?p=15104
categories:
  - Inbox
tags:
  - reprint
---
## TC1
<https://ljr.im/articles/streamline-the-fibonacci-tc1-firmware/>

docker pull python:2-slim-stretch

docker run -it -name mico -v /home/wiloon/tmp/mico:/workdir python:2-slim-stretch bash

apt update && apt install git wget lib32ncurses5

ln -s /usr/local/bin/python /usr/bin/python

# 容器bash
  
pip install mico-cube && \
  
cd /workdir && \
  
wget <http://firmware.mxchip.com/MiCoder_v1.1.Linux.tar.gz> && \
  
tar -zxf MiCoder_v1.1.Linux.tar.gz && \
  
rm MiCoder_v1.1.Linux.tar.gz && \
  
mico config -global MICODER /workdir/MiCoder

# 容器bash
  
cd /workdir && \
  
mico new TC1 -create-only

# 容器bash
  
cd /workdir/TC1 && \
  
mico add <https://code.aliyun.com/mico/mico-os.git/#6c465211d3ff8797cd835e400ec54a06530dd476>

# 容器bash
  
git clone <https://github.com/cnk700i/tc1_mqtt.git> && \
  
mv tc1_mqtt/TC1 . && \
  
rm tc1_mqtt -r

//自定义
  
# define ZTC_NAME "tc1_%s" //设备名称模板，默认生成的设备名称为tc1_{{MAC地址}}，PS: 如修改要保留%s，将填充MAC地址
  
# define CONFIG_SSID "wifi_ssid" //WiFi名称
  
# define CONFIG_USER_KEY "wifi_password" //WiFi密码
  
# define CONFIG_MQTT_IP "mqtt_ip" //MQTT服务器IP
  
# define CONFIG_MQTT_PORT 1883 //MQTT服务器端口
  
# define CONFIG_MQTT_USER "mqtt_user" //MQTT用户名
  
# define CONFIG_MQTT_PASSWORD "mqtt_password" //MQTT密码
  
# define STATE_UPDATE_INTERVAL 10000 //功率上报间隔，单位ms
  
# define MQTT_CLIENT_SUB_TOPIC "cmnd/%s" //命令控制接收topic，%s取ZTC_NAME (默认tc1_{{MAC地址}}) ，PS: 请勿修改此处，可修改ZTC_NAME
  
# define MQTT_CLIENT_PUB_TOPIC "stat/%s" //状态信息topic，%s取ZTC_NAME (默认tc1_{{MAC地址}}) ，PS: 请勿修改此处，可修改ZTC_NAME
  
# define USER_CONFIG_VERSION 3 //修改为与上次固件不同，触发重新加载信息 (线刷可忽略)

# 容器bash
  
# /workdir/TC1
  
mico make TC1@MK3031@moc

编译成功后的固件文件
  
/workdir/TC1/build/TC1@MK3031@moc/binary/TC1@MK3031@moc.all.bin，用于线刷
  
/workdir/TC1/build/TC1@MK3031@moc/binary/TC1@MK3031@moc.ota.bin，用于OTA

```bash
docker run -d \
--name mqtt \
-p 1883:1883 \
-p 9001:9001 \
-v mosquitto-conf:/mosquitto/config \
-v /mosquitto/data \
-v /mosquitto/log  \
eclipse-mosquitto
```

```bash
docker run -d \
--name=ha \
--net=host \
-v ha-config:/config \
-v /etc/localtime:/etc/localtime:ro \
homeassistant/home-assistant
```

---

### 米家 + iphone

```bash
podman run -d --name=ha -p 5353:5353/udp -p 8123:8123 -p 51827:51827 -v ha-conf:/config -v /etc/localtime:/etc/localtime:ro homeassistant/home-assistant
```

    5353/udp是homekit用的
    就是苹果那套
    小米的是
    xiaomi_miio

    switch:

- platform: xiaomi_miio
    name: 'xiaomi_1'
    host: 192.168.xx.xx
    token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

    homeassistant:
      customize:
        switch.xiaomi_1:
          friendly_name: 客厅开关

    homekit:
    port: 51800
    filter:
        include_domains:
            - alarm_control_panel
            - light
            - switch

    homeki
