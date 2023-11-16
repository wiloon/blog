---
title: vmpk
author: "-"
date: 2013-11-09T15:58:59+00:00
url: /?p=5919
categories:
  - Inbox
tags:
  - reprint
---
## vmpk

Virtual MIDI Piano Keyboard is a MIDI events generator and receiver. It doesn't produce any sound by itself, but can be used to drive a MIDI synthesizer (either hardware or software, internal or external). You can use the computer's keyboard to play MIDI notes, and also the mouse. You can use the Virtual MIDI Piano Keyboard to display the played MIDI notes from another instrument or MIDI file player. To do so, connect the other MIDI port to the input port of VMPK. ([http://vmpk.sourceforge.net/](http://vmpk.sourceforge.net/))
  
安装方法:
  
sudo apt-get install vmpk

直接使用应该不会有声音，因为这个软件没有输出，要安装另外一个软件才行。
  
安装方法:
  
sudo apt-get install timidity

然后在VMPK菜单中的连接中选择timidity中的任一款作为VMPK的输出就可以。
  
感觉VMPK中的键位设置不是很理想，还好可以自己调整。 (ubuntu论坛)
