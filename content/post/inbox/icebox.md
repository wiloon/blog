---
title: "icebox"
author: "-"
date: ""
url: ""
categories:
  - inbox
tags:
  - inbox
---
## "icebox"

先用adb安装 
# 谷歌版冰箱激活

Root方法:
把冰箱apk放到 /data/local/tmp/
文件夹中，然后为方便起见重命名为icebox.apk
然后打开终端，su后输入

pm install -i "com.android.vending" -r /data/local/tmp/icebox.apk

搞定[受虐滑稽]

adb方法: 
手机接上电脑，
执行

adb push [冰箱apk位置] /data/local/tmp/icebox.apk

adb shell pm install -i "com.android.vending" -r /data/local/tmp/icebox.apk

adb shell rm /data/local/tmp/icebox.apk

同样搞定[受虐滑稽][受虐滑稽]

然后你就可以连上谷歌验证购买了
参考: 
https://medium.com/@pixplicity/setting-the-install-vendor-of-an-app-7d7deacb01ee 


### 冰箱免 Root (设备管理员模式) 手动配置
https://github.com/heruoxin/Ice-Box-Docs/blob/master/Device%20Owner%20%EF%BC%88%E5%85%8D%20root%EF%BC%89%E6%A8%A1%E5%BC%8F%E8%AE%BE%E7%BD%AE.md
    adb shell dpm set-device-owner com.catchingnow.icebox/.receiver.DPMReceiver
