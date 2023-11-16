---
title: kvm 虚拟机 vnc 开启音频 +rdp
author: "-"
date: 2012-09-13T13:35:41+00:00
url: /?p=4031
categories:
  - Linux
tags:
  - reprint

---
## kvm虚拟机vnc开启音频+rdp
  
为了方便使用virt-manager来创建和管理kvm的虚拟机。默认创建好的windows xp虚拟机，用vnc连接的时候会没有声音，用rdesktop连接的时候声音是正常的。

查了一些发行版的bugzilla，发现相关的bug还真有不少，在fedora的wiki上找到了解决方法 (原始链接在这里) :

修改/etc/libvirt/qemu.conf文件中的vnc_allow_host_audio为1，然后重启libvirtd服务，就OK了。不过这样设置以后，即使不打开virt-manager的vnc客户端，也能够听到虚拟机中发出的声音。

If you have a Linux computer and sound is working on it, then you will be able to get sound through rdesktop. But it's not necessary easy, unless you are aware that there is a bug that prevents it. Good news is that there is a really simple work-around to make sound work.

To get sound to work through rdesktop, first make sure Windows is configured to pass sound through Remote Desktop. Open up "Control Panel" -> "Sounds and Audio Devices". You should see "Microsoft RDP Audio Driver". Next, if the "Device volume" is set to "Low", it is either because: 1) sound pass-through is not enabled; or 2) you reduced the volume to "Low". Try fixing #2 by moving the slider to "High", then click the "Apply" button. If the slider stays at "High", then it's #2 and you should now have sound. If the slider jumps back to "Low" then it's #1 (continue to next paragraph).

If the sound pass-through is diabled, then the volume slider will not stick. You'll have to enable it in rdesktop with the "-r sound" flag. But that feature is bugged. Luckily the work around is to use the "-r sound" flag twice. (My version of rdesktop is 1.3.1.) For example:

rdesktop -r sound -r sound host.domain.com

Easy, eh? Once you have the sound pass-through enabled, you can test with the slider to see that it sticks after clicking the "Apply" button. Now you have sound forwarded to your Linux box.

Chieh Cheng
Mon, 19 Apr 2010 23:02:45 +0000

Note that the Windows volume control on the task bar will still show maximum sound volume even if sound is disabled through rdesktop.

Chieh Cheng
Mon, 26 Apr 2010 17:18:41 +0000

That did it for me THANKS a million!!!

ff
Tue, 22 Feb 2011 15:21:06 +0000

It's not a bug.
  
It will work correct if you use it like this:

rdesktop -r sound:local:alsa host.domain.com

yong
 Fri, 17 Jun 2011 07:31:25 +0000

[http://coolex.info/blog/121.html](http://coolex.info/blog/121.html)

[http://www.gearhack.com/Forums/DisplayComments.php?file=Computer/Linux/Getting_Sound_Through_rdesktop](http://www.gearhack.com/Forums/DisplayComments.php?file=Computer/Linux/Getting_Sound_Through_rdesktop)
