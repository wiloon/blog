---
title: debian thinkpad 指纹
author: w1100n
type: post
date: 2011-12-15T15:06:41+00:00
url: /?p=1894
categories:
  - Linux

---
添加PPA源

选择Ubuntu Lucid是因为，它的kernel正好也是 2.6.32。看样子这个内核应当是久经考验的，因为Debian Squeeze，Ubuntu Lucid LTS和RHEL 6都是用它作内核。Debian和RHEL(和CentOS)本来就是稳定的象征。安装完之后删掉这个源，我不需要Debian stable之外的其他源。
  
deb http://ppa.launchpad.net/fingerprint/fingerprint-gui/ubuntu/ lucid main
  
安装fingerprint-gui.
  
# sudo apt-get install fingerprint-gui policykit-1-fingerprint-gui
  
注销登录，然后再重新登录（有时可能需要重新启动计算机，以使PolicyKit进程重启）
  
二、设置：
  
安装好后，进入"系统->首选项->Fingerprint GUI"，然后按提示初始化输入你的指纹，建议多输入几个手指的。到此为止，设置就完成了。
  
然后尝试注销再登录，或是在控制台运行sudo命令，应该会有指纹识别的框弹出以验证身份，当然你也还可以通过输入密码的方式验证身份.