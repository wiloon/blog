---
title: 虚拟机硬盘格式的选择 qcow2, raw
author: "-"
date: 2011-12-03T06:33:33+00:00
url: /?p=1678
categories:
  - Linux
  - VM
tags:
  - reprint
---
## 虚拟机硬盘格式的选择 qcow2, raw

结论： 建议用 raw

曾经有过一段时间，徘徊于对虚拟机硬盘格式的迷惑中，2009年，终于得出了一些结论 (下面的思路基本通用于其他虚拟机)
搜了下，发现大部分用 qemu 或者 kvm 的，都默认使用 qcow2 来作为虚拟硬盘，但 qemu 官方默认是用 raw。
下面是 qemu wiki 对两种格式的描述:

## raw

Raw disk image format (default). This format has the advantage of being simple and easily exportable to all other emulators. 
If your file system supports holes (for example in ext2 or ext3 on Linux or NTFS on Windows), then only the written sectors will reserve space. 
Use qemu-img info to know the real size used by the image or ls -ls on Unix/Linux.

## qcow2

QEMU image format, the most versatile format. Use it to have smaller images (useful if your filesystem does not supports holes, for example on Windows), 
optional AES encryption, zlib based compression and support of multiple VM snapshots.

## raw 的优势 (能找到的相关资料太少，不知道是不是理解有误)

1、简单，并能够导出为其他虚拟机的虚拟硬盘格式
2、根据实际使用量来占用空间使用量，而非原先设定的最大值 (比如设定最高20G，而实际只使用3G) 。——需要宿主分区支持hole (比如ext2 ext3 ext4 ntfs 等)
3、以后能够改变空间最大值 (把最高值20G提高到200G，qcow2也可以，不过要转为raw)
4、能够直接被宿主机挂载，不用开虚拟机即可在宿主和虚拟机间进行数据传输 (注意，此时虚拟机不要开)

## 而qcow2的优势

1、更小的虚拟硬盘空间 (尤其是宿主分区不支持hole的情况下)
2、optional AES encryption, zlib based compression and support of multiple VM snapshots.

另外，根据fedora12的wiki，说测试结果是raw比qcow2性能更好，即使是新版的qcow2。[http://fedoraproject.org/wiki/Featur...w2_Performance](http://fedoraproject.org/wiki/Featur...w2_Performance)

如果单纯靠这些信息，那么raw好像更有优势，而且更方便。 (raw支持快照否？？？)

那么，为什么大家都默认使用qcow2呢？为什么？

同样的，还有vmdk vdi等虚拟机硬盘格式的优劣表现在哪方面呢？
又看到一个资料，说raw 格式是一种"直读直写"的格式,不具备特殊的特性。也就是说，qcow2具备的这两个AES encryption, zlib based compression，raw就没有。
kqemu是qemu的内核加速模块，不是kvm。wiki里qemu部分有写，和kvm是分为两部分的，是两种不同的内核加速模块。
qemu跑98、me、xp是很慢的，但跑win95，win2000，是飞速的，尤其是win2000 (nnd，win2000好像在普通电脑里相比那几个好像是最慢的) 。98、me要快，可以用定制版的windows，好像叫lite的。
  
更进一步认识，并修正上面的看法
  
但今天 (2010年) 再回过头来看，发现其实 raw 更好:
  
raw 相比 qcow2 就缺乏的四个功能，但都能通过别的方式解决: 

1、加密功能: 把raw本身就当普通文件加密之搞定
2、快照功能: 把raw加入版本管理目录中，具体需要的设置可能稍微有点多。
3、宿主机不支持按需打孔模式 (hole) : 这个可以自己根据使用情况来扩展raw的最大值
4、硬盘压缩: 就当普通电脑文件压缩之即可而raw有qcow2所无法媲美的功能:
1、效率高于qcow2
2、直接读写虚拟机硬盘里面的文件，这比较"暴力"，但既然可以这么暴力，那么也就不怕虚拟机出任何问题了。
3、通用性好，是转为其他虚拟机的格式的通用中间格式，这样就不用担心转换虚拟机系统了。

==================================================================

补充一:

如何让KVM等各种虚拟系统能够拿到本地硬件的原始级别图形加速功能:

在linuxsir上playfish提到: 可以让kvm拿到native级别的图形加速性能。目前我对spice仍然不熟，感觉就是一个虚拟机统一后端/前端图形界面，但这个用远程桌面不也可以实现？ (已经被我下面的否定了，两者不一样，spice应该是: 远程桌面+远程资源本地映射) 刚刚看了其英文介绍，简要翻译下:
硬件加速方面:
1、"客户端"2D使用通用的Cairo渲染
2、"客户端"windows下使用GDI，linux下使用Opengl
3、使用"客户端"的GPU来替换CPU渲染: 可因此获得高效的渲染，并改善虚拟机的CPU使用率
4、"服务端"使用Opengl来渲染
  
  
ps: 这很好玩，不管虚拟的机子是什么类型，都可以根据自己电脑的配置，来使用本地的硬件，那这样的话，同样的一个虚拟机，在不同的电脑上显示效果可就不一样了。
  
==============================================================
补充二:

虚拟硬盘所在的宿主机分区该使用何种分区方式？
 问题的关键可能是虚拟机的虚拟硬盘到底保留了多少宿主机的分区格式特点了。比如宿主用ext3,而虚拟机里用ext4,那么虚拟机里面的性能如何？是 ext3的性能还是ext4的性能？——我想可能ext3的性能应该是该虚拟机的最高上限了，而不会有ext4提升的那部分。硬盘的最大性能>特定分区格式和系统所能利用的最大性能>虚拟机虚拟硬盘所能利用的最大性能>虚拟机中的操作系统和分区格式所能利用的 最大性能
 经过这么多层的削弱，估计确实非常有必要有一种专门为虚拟机设计的分区格式，比如lvm之类的，来获得更高的性能。虚拟机中，linux的swap还是要开的，因为你无法确定某一天你会大量使用内存 (尤其是用于服务器方面的) ，以至你原来给的内存不够用，所以需要预留这些空间，有了这点缓冲时间，估计够在线解决问题了。
 但挂了swap之后慢，可能和我上面说的: 虚拟机的硬盘性能最大只能达到宿主的硬盘性能上限，而不会超过它，所以导致的。

  ========================================================

  补充三:

  raw在生产环境下也这么好？
  并非如此，因为我所上面列举的4个raw可以通过别的方式搞定的功能，实际上有个前提: 能够随时关机。 (不关机也可以，但因为这方面并没有经过多少验证，安全性稳定性如何存疑。)

而raw的很多优势，也是基于关机状态才具备的优势，比如: 直接挂载。
而这些都是生产环境下所无法具备的条件，生产环境大都需要的是: 在线方式实现/不关机就可搞定 (即使是硬盘分区之类底层操作，所以才会发展出lvm之类的东西) 。

也就是说，如果要在线具备更高级的硬盘特性/稳

  转自: [http://jobinson99.blog.163.com/blog/static/2591478201051194046840/](http://jobinson99.blog.163.com/blog/static/2591478201051194046840/)
