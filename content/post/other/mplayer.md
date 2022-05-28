---
title: mplayer
author: "-"
date: 2011-08-27T14:49:28+00:00
url: mplayer
categories:
  - Linux
tags:
  - reprint
---
## mplayer

## 基本播放控制

- → 前进10秒
- ← 后退10秒
- ↑ 前进60秒
- ↓ 后退60秒
- PageUP 前进10分钟
- PageDown 后退10分钟
- Enter 全屏
- Space 暂停
- Esc 退出
- q 退出

## 音量调节

- 9 降低音量
- 0 增大音量
- / 降低音量
- `*` 增大音量
- a 切换声道

### mplayer command monitoraspect

mplayer -monitoraspect 1.25 6.rmvb

全屏 mplayer -aspect 16:9 -fs

### debian 6 smplayer 声音小

Options > preferences > audio > output driver
  
select "alsa"

<http://www.wiloon.com/?p=2850>

### smplayer 中文字幕

option > preference > subtitles > encoding
  
select utf8
  
font : select wqy
  
open subtitle files, change encoding to utf8 , save.
