---
title: mplayer output driver
author: "-"
date: 2012-04-07T12:40:58+00:00
url: /?p=2850
categories:
  - Linux
tags:
  - reprint
---
## mplayer output driver
Output drivers (directx, xv, x11, gl, alsa, oss...) what are they? Which one is the best?

MPlayer has several output drivers, for video and sound. SMPlayer allows you to select the one you want among all of them (Preferences -> General -> Video/Audio).

For video it's recommended that you use xv (linux) or directx (windows). They use hardware acceleration and give the best performance. The inconvenience about directx for Windows Vista users is that it disables Aero.

x11 and directx:noaccel are drivers without hardware acceleration. They give the worst performance. Moreover directx:noaccel gives a bad quality in fullscreen mode.

gl and gl2 will use 3D acceleration from the graphic card. They will give better performance than directx:noaccel and x11 but no so much as directx or xv. gl/gl2 can be useful for Windows Vista users.

For sound, you should usually use oss or alsa in linux. I don't like esd or arts, they use to use more CPU.

In windows the sound drivers are dsound and win32. I read that dsound can cause sometimes audio-video sync problems. If you notice that problem try win32 instead.

Other drivers allows you to save the video as image files or write the sound to the disk. These drivers are not officially supported by SMPlayer. Use them only if you know what you're doing.