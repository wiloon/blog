---
title: compile the kernel – Debian squeeze
author: w1100n
type: post
date: 2012-02-26T13:46:00+00:00
url: /?p=2443
categories:
  - Linux

---
下载源代码, 编译软件准备
  
下载内核源代码：<http://www.kernel.org/>

apt-get update

apt-get install kernel-package libncurses5-dev fakeroot axel bzip2 build-essential gcc make

#kernel-package (debian 特有，也是这个方法的关键),用 debian 的独特方法编译 linux 的内核，会用到 debian 提供的工具。这样做不适用于其他的发行版，但好处是比较简单，而且可以直接产生 .deb 包，可以和其它 debian 软件一样管理和安装。

下载源代码
  
axel http://www.kernel.org/pub/linux/kernel/v2.6/linux-2.6.32.5.tar.xz

注意，很多教程上说应该解压到 /usr/src, 但是实际上解压到任何目录上都可以。
  
/usr/src下面需要root权限反而容易出问题.

unpak...

$xz -d \***.**tar.xz**

$tar -xvf  \***.tar

ln -s linux-2.6.21.3 linux
  
cd /usr/src/linux

清理以前编译时留下的临时文件，如果是刚刚解开的包，据我的实践，不需要执行这步。执行与否，自己考虑。
  
相关命令如下：

make mrproper

很多教程上说把现在使用的内核的config拷贝过来参考，据我的实践，也不需要，ubuntu还有debian会自动做这步。

cp /boot/config-\`uname -r\` ./.config
  
不过ubntu的config存在很多问题, 建议改用附件中arch的2.6.23的config

开始配置内核选项。从linux-2.6.32开始可以使用make localmodconfig自动精简内核, 菜鸟也能轻松精简内核到十几MB(也可以完全手动配置....直接跳到make menuconfig)
  
自动精简内核模块
  
注意: 该方法会自动去掉一些从开机到当前没用使用的模块(主要是驱动模块),
  
所以你可以使用一下你的摄像头, 挂载一下iso文件.....
  
以保证需要的模块不会被精简掉, 否则使用新内核时会发现不能挂载iso文件, 不能使用某些外设等等.
  
命令如下:

  make localmodconfig

然后就可以直接进行编译了.(fakeroot......)

也可以再使用menuconfig检查一下

make menuconfig(2.6.35以上支持make nconfig)

sudo make-kpkg clean #这条命令好像不要超级权限，很多资料上说要，不过这不是原则问题。
  
fakeroot make-kpkg -initrd -append-to-version=ylxy1.0 kernel_image

-

which brings up the kernel configuration menu. Go to Load an Alternate Configuration File and choose .config (which contains the configuration of your current working kernel) as the configuration file:

Then browse through the kernel configuration menu and make your choices. When you are finished and select Exit, answer the following question (Do you wish to save your new kernel configuration?) with Yes:

After -append-to-version= you can write any string that helps you identify the kernel, but it must begin with a minus (-) and must not contain whitespace.

Now be patient, the kernel compilation can take some hours, depending on your kernel configuration and your processor speed.

sudo aptitude install hardinfo

<http://www.kernel.org/>

[http://www.howtoforge.com/kernel_compilation_debian_etch][1]

<http://forum.ubuntu.org.cn/viewtopic.php?t=110461>

 [1]: http://www.howtoforge.com/kernel_compilation_debian_etch