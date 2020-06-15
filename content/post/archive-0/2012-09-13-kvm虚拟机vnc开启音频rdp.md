---
title: kvm虚拟机vnc开启音频+rdp
author: wiloon
type: post
date: 2012-09-13T13:35:41+00:00
url: /?p=4031
categories:
  - Linux

---
# 

<div>
  <p>
    为了方便使用virt-manager来创建和管理kvm的虚拟机。默认创建好的windows xp虚拟机，用vnc连接的时候会没有声音，用rdesktop连接的时候声音是正常的。
  </p>
  
  <div>
    查了一些发行版的bugzilla，发现相关的bug还真有不少，在fedora的wiki上找到了解决方法（原始链接在<a href="https://fedoraproject.org/wiki/How_to_debug_Virtualization_problems#Audio_output">这里</a>）：
  </div>
  
  <div>
    修改/etc/libvirt/qemu.conf文件中的vnc_allow_host_audio为1，然后重启libvirtd服务，就OK了。不过这样设置以后，即使不打开virt-manager的vnc客户端，也能够听到虚拟机中发出的声音。
  </div>
</div>

If you have a Linux computer and sound is working on it, then you will be able to get sound through rdesktop. But it&#8217;s not necessary easy, unless you are aware that there is a bug that prevents it. Good news is that there is a really simple work-around to make sound work.

To get sound to work through rdesktop, first make sure Windows is configured to pass sound through Remote Desktop. Open up "Control Panel&#8221; -> "Sounds and Audio Devices&#8221;. You should see "Microsoft RDP Audio Driver&#8221;. Next, if the "Device volume&#8221; is set to "Low&#8221;, it is either because: 1) sound pass-through is not enabled; or 2) you reduced the volume to "Low&#8221;. Try fixing #2 by moving the slider to "High&#8221;, then click the "Apply&#8221; button. If the slider stays at "High&#8221;, then it&#8217;s #2 and you should now have sound. If the slider jumps back to "Low&#8221; then it&#8217;s #1 (continue to next paragraph).

If the sound pass-through is diabled, then the volume slider will not stick. You&#8217;ll have to enable it in rdesktop with the "-r sound&#8221; flag. But that feature is bugged. Luckily the work around is to use the "-r sound&#8221; flag twice. (My version of rdesktop is 1.3.1.) For example:



<pre>rdesktop -r sound -r sound host.domain.com</pre>



Easy, eh? Once you have the sound pass-through enabled, you can test with the slider to see that it sticks after clicking the "Apply&#8221; button. Now you have sound forwarded to your Linux box.

<p align="right">
  Chieh Cheng
 Mon, 19 Apr 2010 23:02:45 +0000
</p>

Note that the Windows volume control on the task bar will still show maximum sound volume even if sound is disabled through rdesktop.

<p align="right">
  Chieh Cheng
 Mon, 26 Apr 2010 17:18:41 +0000
</p>

That did it for me THANKS a million!!!

<p align="right">
  <a href="mailto:ff@member.org">ff</a>
 Tue, 22 Feb 2011 15:21:06 +0000
</p>

It&#8217;s not a bug.
  
It will work correct if you use it like this:

rdesktop -r sound:local:alsa host.domain.com

<p align="right">
  yong
 Fri, 17 Jun 2011 07:31:25 +0000
</p>

<p align="right">
  <p align="right">
    <p align="right">
      <a href="http://coolex.info/blog/121.html">http://coolex.info/blog/121.html</a>
    </p>
    
    <h2>
      <a href="http://www.gearhack.com/Forums/DisplayComments.php?file=Computer/Linux/Getting_Sound_Through_rdesktop">http://www.gearhack.com/Forums/DisplayComments.php?file=Computer/Linux/Getting_Sound_Through_rdesktop</a>
    </h2>