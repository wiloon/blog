---
title: linux 设置 默认 声卡
author: "-"
date: 2017-01-24T12:39:16+00:00
url: /?p=9682
categories:
  - Uncategorized

tags:
  - reprint
---
## linux 设置 默认 声卡
alsa设置默认声卡
  
2013-11-06 15:43 4650人阅读 评论(0) 收藏 举报
  
分类: 
  
gentoo (47) 
  
版权声明: 本文为博主原创文章,未经博主允许不得转载。
  
首先说一下alsa的配置文件。alsa的配置文件是alsa.conf位于/usr/share/alsa目录下,通常还有/usr/share/alsa/card和/usr/share/alsa/pcm两个子目录用来设置card相关的参数,别名以及一些PCM默认设置。以上配置文件,我等凡夫从不用修改,修改它们是大神的工作。

还有两个配置文件/etc/asound.conf和~/.asoundrc,它俩有效是因为它俩被alsa.conf引用。以下是alsa.conf的原文: 


 view plain copy
  
# pre-load the configuration files

@hooks [
  
{
  
func load
  
files [
  
{
  
@func concat
  
strings [
  
{ @func datadir }
  
"/alsa.conf.d/"
  
]
  
}
  
"/etc/asound.conf"
  
"~/.asoundrc"
  
]
  
errors false
  
}
  
]

然后说我遇到的问题。为了提高本人的台式机的性能,在没有换主板的情况下升级了CPU和显卡。CPU没有造成什么影响,显卡是淘来的微星R6750暴雪1G,芯片为AMD Radeon HD 6750。由于它提供了一个HDMI接口,该接口还支持音频输出,于是麻烦出现了,在gentoo下,声音不走板载的HDA VIA VT82xx集成声卡,不知道走到哪里出去了,反正我的耳机没有声音。

找了好多文档,终于然我弄明白怎么回事了。

首先,如果机器有多于一个声卡,可以用下面的命令显示出来: 


 view plain copy
  
$ cat /proc/asound/cards
  
0 [Generic        ]: HDA-Intel - HD-Audio Generic
  
HD-Audio Generic at 0xfe9bc000 irq 25
  
1 [VT82xx         ]: HDA-Intel - HDA VIA VT82xx
  
HDA VIA VT82xx at 0xfeafc000 irq 17
  
其次,每一个声卡有一个card number和一个device number,可以用下面命令显示出来: 


 view plain copy
  
$ aplay -l
  
*\*\\*\* List of PLAYBACK Hardware Devices \*\***
  
card 0: Generic [HD-Audio Generic], device 3: HDMI 0 [HDMI 0]
  
Subdevices: 1/1
  
Subdevice #0: subdevice #0
  
card 1: VT82xx [HDA VIA VT82xx], device 0: AD1986A Analog [AD1986A Analog]
  
Subdevices: 1/1
  
Subdevice #0: subdevice #0
  
最后,alsa设置了一个defaults设备,音频播放软件默认使用defaults设备输出声音。defaults设备定义在alsa.conf中,内容如下: 


 view plain copy
  
#
  
# defaults
  
#

# show all name hints also for definitions without hint {} section
  
defaults.namehint.showall off
  
# show just basic name hints
  
defaults.namehint.basic on
  
# show extended name hints
  
defaults.namehint.extended off
  
#
  
defaults.ctl.card 0
  
defaults.pcm.card 0
  
defaults.pcm.device 0
  
defaults.pcm.subdevice -1
  
……
  
……
  
……

所以defaults会默认匹配card number和device number比较小的声卡。比如我这里 (看上面aplay -l的输出显示) ,就会匹配到HDMI 0上。

如果要修改,则修改/etc/asound.conf或~/.asoundrc。比如我要把defaults匹配到card 1,device 0上,则添加一下几行: 


 view plain copy
  
$ sudo vim /etc/asound.conf
  
defaults.pcm.card 1
  
defaults.pcm.device 3
  
defaults.ctl.card 1

参考文档: 

[csdn blog]alsa config
  
[csdn blog]理解和使用Alsa的配置文件
  
[arch wiki]设置默认声卡

