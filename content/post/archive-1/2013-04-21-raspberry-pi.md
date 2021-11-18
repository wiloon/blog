---
title: raspberry pi omxplayer mplayer
author: "-"
date: 2013-04-21T02:46:47+00:00
url: /?p=5417
categories:
  - Raspberry Pi
tags:
  - Raspberry Pi

---
## raspberry pi omxplayer mplayer
```bash
sudo apt-get install omxplayer
sudo apt-get install fonts-wqy-zenhei
sudo apt-get install ttf-freefont

omxplayer --subtitles The.Legend.of.1900.1998.BDRip.X264-BMDruCHinYaN.chs.srt \
--font /usr/share/fonts/truetype/wqy/wqy-zenhei.ttc \
La.Leggenda.Del.Pianista.Sull.Oceano.1998.BluRay.1080p.2Audio.DTS-HD.MA.5.1.x264-beAst.mkv

omxplayer -r -o hdmi --subtitles The.Legend.of.1900.1998.BDRip.X264-BMDruCHinYaN.chs.srt \
--font /usr/share/fonts/truetype/wqy/wqy-zenhei.ttc \
La.Leggenda.Del.Pianista.Sull.Oceano.1998.BluRay.1080p.2Audio.DTS-HD.MA.5.1.x264-beAst.mkv
```

#-r 全屏播放
  
#-o hdmi 输出音频到hdmi
  
#-subtitles 字幕
  
#-font 字体文件
  
omxplayer中文乱码可以直接在omxplayer中指定字体,直接使用wqy字体即可: 
  
$omxplayer -t 1 -p -r -font /usr/share/fonts/truetype/wqy/wqy-zenhei.ttc -align center -o hdmi test.avi
  
omxplayer不支持外置字幕目前新版本omxplayer已经支持外置字幕,可以去网站上下载5,不过目前好像只支持utf-8,不行只能通过enca转码。

标准Raspbian版本中支持树莓派的GPU的播放器好像只有omxplayer,是个命令行程序,没有界面的,也不能拖动。它有很多参数,最常用的是-o,选项有local和hdmi,表示声音输出到audio out还是hdmi,omxplayer后面跟着要播放的文件名称,不支持wmv,不支持外置字幕。打开终端窗口,出现提示符后输入: 

omxplayer -o hdmi 文件名

OMXplayer支持硬解码,因此是一个非常不错的选择。
  
支持格式目前知道的有: MKV、AVI、FLV、MP4

如果想用全屏播放,参数是: -r

如果想用HDMI输出声音,参数是: -o hdmi,并且有个前提: /boot/config.txt 里面设置HDMI_DRIVER=2

$ omxplayer –help
  
Usage: omxplayer [OPTIONS] [FILE]
  
Options :
  
-h / –help print this help
  
-a / –alang language audio language : e.g. ger
  
-n / –aidx index audio stream index : e.g. 1
  
-o / –adev device audio out device : e.g. hdmi/local
  
-i / –info dump stream format and exit
  
-s / –stats pts and buffer stats
  
-p / –passthrough audio passthrough
  
-d / –deinterlace deinterlacing
  
-w / –hw hw audio decoding
  
-3 / –3d switch tv into 3d mode
  
-y / –hdmiclocksync adjust display refresh rate to match video
  
-t / –sid index show subtitle with index
  
-r / –refresh adjust framerate/resolution to video

快捷键

– Decrease Volume
  
= Increase Volume

Left Arrow Seek -30 s
  
Right Arrow Seek +30 s
  
Down Arrow Seek -600 s
  
Up Arrow Seek +600 s

z Show Info
  
1 Decrease Speed
  
2 Increase Speed
  
j Previous Audio stream
  
k Next Audio stream
  
i Previous Chapter
  
o Next Chapter
  
n Previous Subtitle stream
  
m Next Subtitle stream
  
s Toggle subtitles
  
d Subtitle delay -250 ms
  
f Subtitle delay +250 ms
  
q Exit OMXPlayer
  
Space or p Pause/Resume

#compile from source
  
git clone https://github.com/popcornmix/omxplayer.git
  
http://tacy.github.io/blog/2013/02/10/raspberry-pi-notes/

http://www.xieaoran.tk/post/2015/01/15/raspberry-pi-hw-decode

https://github.com/popcornmix/omxplayer
  
https://archlinuxarm.org/forum/viewtopic.php?f=59&t=6637