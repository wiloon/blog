---
title: 'Linux  双显示器/多屏/扩展屏幕/xrandr'
author: "-"
date: 2012-11-11T11:21:57+00:00
url: /?p=4647
categories:
  - Linux
tags:
  - reprint
---
## 'Linux  双显示器/多屏/扩展屏幕/xrandr'

```bash

xrandr -verbose

xrandr -output DVI-0 -left-of VGA-0 -auto
  
```

不带参数执行xrandr能够列出当前的显示设备和每个设备支持的模式。 edit xorg.conf add line Virtual 2560 1024

```bash
  
wiloon@debian:~$ xrandr
  
Screen 0: minimum 320 x 200, current 1680 x 1050, maximum 16384 x 16384
  
DFP1 connected 1680x1050+0+0 (normal left inverted right x axis y axis) 518mm x 324mm
   
1920x1200 60.0 +
   
1920x1080 60.0
   
1600x1200 60.0
   
1680x1050 60.0*
   
1400x1050 60.0
   
1600x900 60.0
   
1360x1024 60.0
   
1280x1024 60.0
   
1440x900 60.0
   
1280x960 60.0
   
1280x800 60.0
   
1280x768 60.0
   
1280x720 60.0
   
1024x768 60.0
   
800x600 60.3
   
640x480 59.9
  
DFP2 disconnected (normal left inverted right x axis y axis)
  
DFP3 disconnected (normal left inverted right x axis y axis)
  
DFP4 disconnected (normal left inverted right x axis y axis)
  
DFP5 connected 1680x1050+0+0 (normal left inverted right x axis y axis) 408mm x 255mm
   
1680x1050 60.0*+
   
1600x1200 60.0
   
1400x1050 60.0
   
1600x900 60.0
   
1360x1024 60.0
   
1280x1024 75.0 60.0
   
1440x900 59.9
   
1280x960 60.0
   
1280x800 60.0
   
1152x864 60.0 75.0
   
1280x768 60.0
   
1280x720 60.0
   
1024x768 75.0 70.1 60.0
   
800x600 72.2 75.0 60.3 56.2
   
640x480 75.0 72.8 66.6 59.9
  
CRT1 disconnected (normal left inverted right x axis y axis)
  
```

```bash
  
wiloon@debian:~$ xrandr -output DFP1 -auto -left-of DFP5
  
xrandr -output DFP1 -mode 1920x1200 -left-of CRT2 -mode 1680x1050
  
```

```bash

wiloon@debian:~$ cvt 1680 1050
  
# 1680x1050 59.95 Hz (CVT 1.76MA) hsync: 65.29 kHz; pclk: 146.25 MHz
  
Modeline "1680x1050_60.00" 146.25 1680 1784 1960 2240 1050 1053 1059 1089 -hsync +vsync
  
wiloon@debian:~$ xrandr -newmode "1680x1050" 146.25 1680 1784 1960 2240 1050 1053 1059 1089 -hsync +vsync
  
wiloon@debian:~$ xrandr -addmode VGA1 "1680x1050"
  
wiloon@debian:~$ xrandr -output VGA1 -mode 1680x1050

```

1. 设置显示分辨率及 xrandr 介绍 X Windows 中有一个显示分辨率的概念，在默认情况下，这个显示分辨率为 max\*max ，max等于你的所有连接上的显示器中最大分辨率中的最大值。例如我的笔记本液晶屏最大分辨率为 1024\*768，外接显示器最大分辨率为 1280\*1024，则默认的显示分辨率为 1280\*1280。如果我设置左右双屏且使用最大分辨率，那么总显示分辨率就会达到2304*1024，达到超出系统默认的大小。在这种情况下强行设置双屏幕，就会导致 X 进入超低分辨率，结果不得不手工重设 xrog.conf 来恢复。 为了更好检测这个问题，我们需要用到xrandr 这个软件，xrandr系统已经自带，如果没有请安装x11-xserver-utils: sudo apt-get install x11-xserver-utils 。

不带参数执行xrandr能够列出当前的显示设备和每个设备支持的模式。Screen代表了总显示区域，VGA代表显示器，LVDS代表笔记本液晶屏。

Screen 0: minimum 320 x 200, current 1280 x 768, maximum 1280 x 1280 VGA connected (normal left inverted right x axis y axis) 1280x1024      75.0 +   69.8     59.9 1024x768       75.1     70.1     60.0 800x600        72.2     75.0     60.3 640x480        75.0     72.8     65.4     60.0 720x400        70.1 LVDS connected 1024x768+0+0 (normal left inverted right x axis y axis) 246mm x 184mm 1024x768       50.0*+   60.0     40.0 800x600        60.3 640x480        60.0     59.9

系统默认显示分辨率为 1280x1280，而在左右扩展双屏情况下VGA和LVDS支持的最小分辨率加在一起都超过这个数字，当然会导致 X 进入超低分辨率了。如果感兴趣，可以用以下命令尝试把外接显示器打开并设置为右侧扩展屏幕 (不用sudo) 来验证一下:

xrandr -output VGA -auto -right-of LVDS 系统会出错，提升说屏幕大小超出限制。

解决方法: 手工修改xorg.conf，在Section "Screen"中添加一行 Virtual 2304 1024 Section "Screen" Identifier "Default Screen" Monitor "Configured Monitor" Device "Configured Video Device" SubSection "Display" Virtual 2304 1024 EndSubSection EndSection 注意: Ubuntu 8.04中的xorg.conf已经非常精简，Subsection "Display" 可能要自己添加，别忘记 EndSubSection 我设置好以后的xrandr命令输入如下:  $ xrandr Screen 0: minimum 320 x 200, current 1024 x 768, maximum 2304 x 1024 VGA connected (normal left inverted right x axis y axis) .... LVDS connected 1024x768+0+0 (normal left inverted right x axis y axis) 246mm x 184mm .... 现在应该没问题了，用刚才的命令打开双屏后， $ xrandr Screen 0: minimum 320 x 200, current 2304 x 1024, maximum 2304 x 1024 VGA connected 1280x1024+1024+0 (normal left inverted right x axis y axis) 340mm x 270mm ... LVDS connected 1024x768+0+0 (normal left inverted right x axis y axis) 246mm x 184mm ... 其实这个显示分辨率完全可以设置高一些，比如我就设置成4000 x 2000，如果连接到最大分辨率为1920x1200的外接显示器，也不用重新设置 xorg.conf 了。

xrandr 命令行可以很方便地切换双屏，常用方式如下，其他的可以自己探索:

xrandr -output VGA -same-as LVDS -auto 打开外接显示器(最高分辨率)，与笔记本液晶屏幕显示同样内容 (克隆)

xrandr -output VGA -same-as LVDS -mode 1024x768 打开外接显示器(分辨率为1024x768)，与笔记本液晶屏幕显示同样内容 (克隆)

xrandr -output VGA -right-of LVDS -auto 打开外接显示器(最高分辨率)，设置为右侧扩展屏幕

xrandr -output VGA -off 关闭外接显示器

xrandr -output VGA -auto -output LVDS -off 打开外接显示器，同时关闭笔记本液晶屏幕 (只用外接显示器工作)

xrandr -output VGA -off -output LVDS -auto 关闭外接显示器，同时打开笔记本液晶屏幕 (只用笔记本液晶屏)

 (最后两种情况请小心操作，不要误把两个屏幕都关掉了。。。。)

## Adding undetected resolutions {#Adding_undetected_resolutions}

Due to buggy hardware or drivers, your monitor's correct resolutions may not always be detected. For example, the EDID data block queried from your monitor may be incorrect. If the mode already exists, but just isn't associated for the particular output, you can add it like this:

$ xrandr -addmode S-video 800x600

If the mode doesn't yet exist, you'll need to **create it first** by specifying a modeline:

$ xrandr -newmode <Mode"Line>

You may create a modeline using the gtf or cvt utility. For example, if you want to add a mode with resolution 800x600 at 60 Hz, you can enter the following command: (The output is shown following.)

$ cvt 1680 1050 60

# 1680x1050 59.95 Hz (CVT 1.76MA) hsync: 65.29 kHz; pclk: 146.25 MHz
  
Modeline "1680x1050_60.00" 146.25 1680 1784 1960 2240 1050 1053 1059 1089 -hsync +vsync

Then copy the information after the word "Modeline" into the xrandr command:

$ xrandr -newmode "1680x1050_60.00"  146.25  1680 1784 1960 2240  1050 1053 1059 1089 -hsync +vsync

After the mode is entered, it needs to be added to the output using the -addmode command as explained above.

addnewmode

xrandr -addmode "1680x1050_60.00"

[https://wiki.archlinux.org/index.php/Xrandr](https://wiki.archlinux.org/index.php/Xrandr)
