---
title: linux tp fancontrol
author: wiloon
type: post
date: 2012-04-15T14:42:08+00:00
url: /?p=2945
categories:
  - Computer Science
  - Hardware
  - Linux

---
<https://github.com/Stanko/ThinkPad-Fan-Control>

OS: Debian 6

<del>/etc/modprobe.d/alsa-base.conf</del>

<del>options thinkpad_acpi fan_control=1</del>

修改配置文件:

/etc/modprobe.d/thinkpad_acpi.conf

options thinkpad\_acpi fan\_control=1 experimental=1

<del>add the following to <tt>/etc/modprobe.d/options</tt></del>

<del><tt></tt><tt>options thinkpad_acpi fan_control=</tt></del>

重新加载模块:

sudo modprobe -r thinkpad\_acpi && sudo modprobe thinkpad\_acpi

然后就可以控制风扇了:

\# (maximum speed)

`echo level 7 | sudo tee /proc/acpi/ibm/fan`

自动控制脚本:

<http://www.thinkwiki.org/wiki/Talk:Code/tp-fancontrol>

第292行报错, 被我改成了

#echo &#8220;watchdog $WATCHDOG\_DELAY&#8221; > $IBM\_ACPI/fan
  
echo watchdog $WATCHDOG\_DELAY | sudo tee $IBM\_ACPI/fan

<https://bugzilla.redhat.com/show_bug.cgi?id=685070>

<http://www.conanblog.me/notes/control-fan-speed-with-thinkpad-acpi/>

<http://ibm-acpi.sourceforge.net/README>

[http://www.thinkwiki.org/wiki/Thermal_Sensors][1]

<http://lm-sensors.org/>

 [1]: http://www.thinkwiki.org/wiki/Thermal_Sensors#ThinkPad_X61