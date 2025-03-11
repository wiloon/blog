---
title: 理解和使用 alsa 配置-默认静音,必须先用amixer解除主音量和pcm音量的静音
author: "-"
date: -001-11-30T00:00:00+00:00
draft: true
url: /?p=6810
categories:
  - Inbox
tags:
  - Linux

---
## 理解和使用 alsa 配置-默认静音,必须先用amixer解除主音量和pcm音量的静音
## 理解和使用alsa配置-默认静音,必须先用amixer解除主音量和pcm音量的静音
http://blog.chinaunix.net/uid-20564848-id-74727.html

ALSA声卡驱动程序的配置
  
对于声卡驱动程序，除了内核自带的驱动程序之外，您还可以使用Advanced Linux Sound Architecture (ALSA，http://www.alsa-project.org/) 提供的驱动程序。它支持一系列主流声卡，同时它和内核 的声音结构互相兼容，在某种程度上，可以说是内核的声卡驱动模块的补充。
  
ALSA的声卡驱动程序的一般命名规则是snd-card-<soundcard>。soundcard代表不同类型的声卡。例如，对于所有 的16位Soundblaster声卡，它们对应的驱动程序模块为snd-card-sb16。
  
若与需要linux内核声音驱动的向后兼容性，您还需要两个模块snd-pcm-oss和snd-mixer-oss。对于amixer设置的多个混音 器，它们都是针对不同的设备的。比如CD通道的设置是针对CD播放器的。而很多应用程序，如象mpg123，xmms，realplayer，都要依赖 PCM通道的设置。MIC代表麦克风。不同的Gain部分对于不同的使用能提供特别的增益。
  
缺省情况下ALSA静音所有的输出。为了获得声音，必须解除主音量和PCM音量的静音。
  
amixer -c 0 sset 'Master',0 100%,100% unmute
  
amixer -c 0 sset 'PCM ',0 100% unmute

选项包括mute，unmute，capture，nocapture，rec，norec，数字或left:right。amixer不带参数运行时， 返回声卡上所有通道的设置情况。
  
为了在每次插入声卡驱动模块时，都打开静音，您可以在/etc/modules.conf加入下列语句: 
  
post-install snd-card-sb16 amixer -c 0 sset 'Master',0 100%,100% unmute && amixer -c 0 sset 'PCM ',0 100% unmute

在成功插入了alsa声卡模块之后，系统会出现/proc/asound目录，这个目录描述了声卡的工作情况，以及创建的设备文件。
  
在您加载snd-pcm-oss设备模块之后，你也能使用与oss兼容的方式存取声卡，这时如下的映射会被完成: 
  
表 5-3
  
ALSA设备 OSS设备 次设备号
  
/dev/snd/pcmC0D0 /dev/audio0 (/dev /audio)  4
  
/dev/snd/pcmC0D0 /dev /dsp0 (/dev/dsp)  3
  
/dev/snd/pcmC0D1 /dev /adsp (/dev/adsp)  12
  
/dev/snd/pcmC1D0 /dev/audio1 20
  
/dev/snd/pcmC1D0 /dev/dsp1 19
  
/dev/snd/pcmC1D1 /dev/adsp1 28
  
/dev/snd/pcmC2D0 /dev/audio2 36
  
/dev/snd/pcmC2D0 /dev/dsp2 35
  
/dev/snd/pcmC2D1 /dev/adsp2 44
  
对于/dev/mixer设备，要加载snd-mixer-oss，可以保证和老的oss混音器的兼容性。如果您插入了上述设备之后，声音系统仍无法正常 工作，您可以运行snddevices命令，建立正确的设备文件。
  
由于为使ALSA正常工作，需要设置大量的设备别名，下面就给出一个/etc/modules.conf的例子，它能够完成ESS Solo1声卡的自动配置工作。其他的ALSA设备的设置也基本与此声卡相同。
  
# 设置ALSA设备的主设备号，它固定为116
  
alias char-major-116 snd

# 设置OSS设备的主设备号，它固定为14，这使得ALSA复用OSS设备
  
alias char-major-14 soundcore

# ALSA设备别名
  
alias sound-card-0 snd-card-es1938

# OSS设备别名
  
alias sound-slot-0 sound-card-0

# 安装不同的声卡服务
  
alias sound-service-0-0 snd-mixer-oss
  
alias sound-service-0-1 snd-seq-oss
  
alias sound-service-0-3 snd-pcm-oss
  
alias sound-service-0-8 snd-seq-oss
  
alias snd-minor-oss-12 snd-pcm-oss

# 运行amixer命令，打开声音输出
  
post-install snd-card-es1938 amixer -c 0 sset 'Master',0 100%,100% unmute && amixer -c 0 sset 'PCM ',0 100% unmute

=================================================
  
http://www.linuxforum.net/forum/printthread.php?Cat=&Board=embedded&main=687530&type=post
  
理解和使用Alsa的配置文件
  
作者: 刘旭晖 Raymond转载请注明出处
  
Email: colorant@163.com
  
BLOG: http://blog.csdn.net/colorant/
  
主页: http://rgbbones.googlepages.com/

最近在做音频相关的驱动，使用到了Alsa。过程中涉及到一些硬件的设置和测试，需要了解Alsa的配置文件的写法，稍微学习了一下，这里把自己 的一些简单理解记录如下。

1 相关说明
  
1.1 网站资源
  
Alsa项目的官方网址: http://www.alsa-project.org/
  
Alsa LIB API Reference: http://www.alsa-project.org/alsa-doc/alsa-lib/
  
配置文件的语法: http://www.alsa-project.org/alsa-doc/alsa-lib/conf.html
  
Asoundrc的官方说明文档: http://www.alsa-project.org/main/index.php/Asoundrc

实际上，如果你仔细看了上述文档，大概也就没必要往下看我的文章了 8 ) 

另: 关于Alsa-Lib的API，网上的是每天自动生成的最新版本的API，如果你不能确认你使用的版本是否和最新版本完全兼容，可以看 Alsa-lib包里自带的那一份文档。可以在src包里执行make doc 自己build出来。
  
1.2 工作环境
  
我测试的软件版本是基于Alsa 1.0.14的版本，当前最新的版本是1.0.16  (2008-7) ，不过配置文件这一部分应该是差不多的，至少从文档上来看是这样。

2 理解配置文件
  
2.1 配置文件的位置
  
配置文件的位置是由Configure阶段的选项来决定的，不过多数时候，Alsa的配置文件位于: /usr/share/alsa目录下，主要 配置文件为/usr/share/alsa/alsa.conf 其它文件是否需要，位置在哪，都是由alsa.conf来决定的。
  
通常会有/usr/share/alsa/card 和/usr/share/alsa/pcm两个子目录，用于设置Card相关的参数，别名以及一些PCM默认设置。
  
此外，在alsa.conf中，通常还会引用 /etc/asound.conf 和 ~/.asoundrc这两个配置文件，这两个文件通常是放置你个人需要特殊设置的相关参数。按照Alsa官方文档的说法，1.0.9版本以后，这两个文 件就不再是必要的，甚至是不应该需要的。至少是不推荐使用吧。不过，对于我来说，在嵌入式系统中使用，为了简单和方便测试，恰恰是需要修改这两个文件 8 ) 
  
2.2 Alsa.conf
  
Alsa.conf中主要的一些内容包括: 用hook读取了/etc/asound.conf 和 ~/.asoundrc这两个配置文件: 
  
@hooks [
  
{
  
func load
  
files [
  
"/etc/asound.conf"
  
"~/.asoundrc"
  
]
  
errors false
  
}
  
]

设置了default pcm的一些默认参数，如，默认使用Card 0 ，Device 0作为音频设备等等。

defaults.ctl.card 0
  
defaults.pcm.card 0
  
defaults.pcm.device 0
  
defaults.pcm.subdevice -1
  
defaults.pcm.nonblock 1
  
defaults.pcm.ipc_key 5678293
  
。。。
  
设置了Alsa 内置的一些plugin的接口参数，例如file: 
  
pcm.file {
  
@args [ FILE FORMAT ]
  
@args.FILE {
  
type string
  
}
  
@args.FORMAT {
  
type string
  
default raw
  
}
  
type file
  
slave.pcm null
  
file $FILE
  
format $FORMAT
  
}

File plugin的作用是将PCM数据流存储到文件中。

此外，通常alsa.conf还会载入cards/aliases.conf ，设置一些声卡的别名等，这个我是不需要了。
  
在aliases.conf 的结尾还有以下一段: 

<confdir:pcm/default.conf>
  
<confdir:pcm/dmix.conf>
  
<confdir:pcm/dsnoop.conf>

用来读入/usr/share/alsa/pcm目录下所列的那3个文件
  
分别设置 默认PCM设备的相关参数，dmix是用来实现播放时软件混音的内建plugin，dsnoop则是用来实现录音时多路分发的内建plugin。

3 一些配置和使用实例

3.1 使用蓝牙设备
  
在/etc/asound.conf中添加下列一项用来使用蓝牙的A2DP设备

# device for bluetooth
  
pcm.bluetooth{
  
type bluetooth
  
device 00:02:5B:00:C1:A0
  
}

然后调用 aplay –D bluetooth sample.wav 播放。

需要注意，为了使用该设备，你需要 /usr/lib/alsa-lib/libasound_module_pcm_bluetooth.so 这一个蓝牙plugin的库文件。这是在Bluez相关的包里，和Alsa本身没有关系。从这里，我们也可以看出alsa的外部plugin和配置文件之 间的名字关系规则:  libasound_module_pcm_####.so 这里的#### 就是你再conf文件中pcm.xxxx 里所写的名字。

3.2 使用非默认的声卡设备通道
  
在我的板子上，Buildin的Audio硬件在Alsa子系统中实现了两个硬件通道，一个是HIFI通道，另一个是语音通道，所以我添加了如下 配置: 

#device for voice channel
  
pcm.voice{
  
type plug
  
slave{
  
pcm "hw:0,1"
  
}
  
}

通过语音通道播放声音的调用的方式:  aplay –D voice sample.wav

这样的写法说明我通过plug这plugin对音频数据进行自动的采样率，通道等调整后，将数据送到我的第0个card的序号为1的device 上。
  
实际上，如果不写上述配置文件，用 aplay -D "plug:SLAVE='hw:0,1'" sample.wav 也可以得到同样的结果。

Hifi通道播放声音直接使用 Aplay sample.wav即可 也就是Aplay –D default sample.wav

3.3 其它
  
混音: 
  
aplay -D plug:dmix sample.wav &
  
你可以通过多次调用上述命令来测试多个音频数据的混音。

Dump音频数据: 
  
aplay -D "plug:'file:FILE=/tmp/dump.bin'" sample.wav