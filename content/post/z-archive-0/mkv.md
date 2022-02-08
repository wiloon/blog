---
title: mkv
author: "-"
date: 2012-04-07T12:24:21+00:00
url: /?p=2847
categories:
  - Uncategorized

tags:
  - reprint
---
## mkv
MKV格式介绍
关键词:  MKV

首先澄清一个误区，mkv不是一种压缩格式，DivX、XviD才是视频压缩格式，mp3、ogg才是音频压缩格式。而mkv是个"组合"和"封装"的格式，换句话说就是一种容器格式。

举个例子的话就比较容易理解了，把只有视频的XviD和只有音频的mp3组合起来，然后以一种多媒体介质的形式出现，最常见的就是avi，其次就是ogm，还有mp4等不太常见的。

avi的出现已经超过了10年，渐渐体现出老态了，除了近年通过VD可以拥有2个音轨，没有其他的改进。

ogm的出现，标志着多音轨格式的出现，可以合成8个以上的音轨，音频上自然也多了ogg这个格式，重要的是可以"内挂"字幕，老外称为"软字幕"，可以任意开关，可以"内挂"8个以上的字幕，美中不足的是仅仅支持srt格式，并且不支持Unicode，对亚洲字符支持严重不足。

还有一个就是Chapter功能，可以自定义段落，播放时就可以选择了。是不是越来越像DVD啦？但是当时的ogm源码是不公开的，就那么几个人在开发，自然进度慢了，前一阵几乎陷入了"死亡"。最近宣布公开源码，加入Open Source行列，重新开始开发。

mkv就是在ogm停滞的那段时间出现的，由俄罗斯的程序员开发的，从一开始就是Open Source，因此得到了很多其他程序员的帮助，开发速度相当快。

ogm有的mkv都有，另外还有很多独特的功能。其中最令人振奋的就是Gabest(开发vobsub的公司)开发的Plugin，不仅开发了专门的播放器Media Player Classic(俗称MPC)， 这个东西的强大相信用过的人都有体会。还开发了很多的MKV用的Mux(合成器)，尤其是Real格式的Mux。 Real的rmvb是封闭格式，官方的Helix根本就不支持多声道所以尽管算法很优秀，但在声效大片的再现上就无能为力了，只能乖乖让位给可以合成AC3和DTS的avi以及ogm了。

但Gabest开发的Realmedia Splitter和mkv Mux可以让rmvb格式的视频和AC3、DTS合成mkv，从根本上克服了rmvb音频上的弱点。不仅如此，还开发了VSFilter.dll和SubtitleSource.ax这2个Plugin，宣布支持ssa和ass的格式软字幕。

总结就是下面几条: 

1.支持多种格式的视频和音频，尤其是Real

2.支持多音轨，多达16条以上

3.支持ssa，ass软字幕，多达16条以上

4.支持段落选取(由制作人决定)

2个插件的下载:

ffdshow 下载最新版的 安装时记得把DIVX3 DIVX4 还有post-processing(后处理)的钩都去掉
matroska splitter

下载页面:http://x264.nl/

插件装好后,通常的播放器都可以播放MKV了

  参考资料: http://newx.blogchina.com/4404315.html
