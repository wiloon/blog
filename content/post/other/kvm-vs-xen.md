---
title: KVM Xen
author: "-"
date: 2011-11-26T08:06:57+00:00
url: /?p=1629
categories:
  - Linux
  - VM
tags:
  - reprint
---
## KVM Xen

2002年Xen首次发布时，进过8年的发展，Xen似乎成了曾经受宠的弃儿，当初力撑它的RedHat已经正式转向自家的KVM，而且KVM占有得天独厚的优势，因为它已经成功进入Linux内核。不得不承认虚拟化技术的发展是相当迅速的，如果你没有跟上KVM和Xen的发展速度，在考虑购买哪一种虚拟化平台时，你可能会很困惑。
  
KVM和Xen
  
Xen是一个支持x86、x86_64、安腾和ARM架构的Hypervisor，可以在它支持的处理器架构上运行Linux、Windows、Solaris和部分BSD客户机操作系统，许多公司都支持Xen，当然主要还是思杰 (Citrix) ，Oracle VM其实也是基于Xen包装而成的，当然还有更多的虚拟化解决方案都是以Xen为基础的，Xen可以安装在系统上，也可以直接安装到裸机上。
  
KVM是一个集成到Linux内核的Hypervisor，很明显，宿主操作系统必须是Linux，支持的客户机操作系统包括Linux、Windows、Solaris和BSD，运行在支持虚拟化扩展的x86和x86_64硬件架构上，这意味着KVM不能运行在老式CPU上，新CPU如果不支持虚拟化扩展也不能运行 (如英特尔的Atom处理器) ，在大多数情况下，对于数据中心来说，这些限制都不是问题，因为每个几年硬件都会升级换代，但最近也有些数据中心选择Atom架构，那么注定它们不能使用KVM。
  
如果你想运行Xen宿主主机，你需要有一个支持的内核，Linux默认一般不会提供Xen宿主主机支持，从2.6.23内核开始支持作为客户机运行，如果你的Linux发行版不支持Xen，你必须自己定制内核，或直接选择如Citrix XenServer这样的商业解决方案，但问题是这些解决方案不是完全开源的。

许多人都是自己构建内核，Xen可以运行在很多服务器上，从低成本的虚拟专用服务器 (Virtual Private Server，VPS) 供应商，如Linode，到大型公司，如Amazon的EC2，这些公司都加大了这方面的投入，不会轻易转换到其它技术，即使技术上KVM超越了Xen，也不能一下就取代现有的解决方案，更何况KVM在技术上的优势并不明显，有些地方甚至还未超越Xen，因为Xen的历史比KVM更悠久，它也比KVM更成熟，你会发现Xen中的某些功能在KVM还未实现，因此我们看到KVM项目的Todo List很长，KVM的优势也仅限于它进入了Linux内核。从RHEL 5.4开始，RedHat就支持KVM了，从RHEL 6.0开始RedHat就完全抛弃Xen了。
  
RedHat弃用Xen给克隆REHL的公司带来了麻烦，迫使他们也接受KVM，要么只有自行维护一套包含Xen的分支，但这无疑会增加它们的成本。
  
KVM的发展相当迅速，虽然目前还在追赶Xen，但Xen的领先地位恐怕很快就会丧失，我们不得不担忧Xen的未来出路。
  
只能有一个存活下来吗？
  
选择KVM还是Xen其实就是选择厂商，如果你想使用RHEL，那么KVM无疑是首选，如果你想运行在Amazon EC2上，那么你将使用Xen，主流Linux厂商似乎都站在KVM一边，但它们也为Xen提供了大量的商业支持，Citrix可能不会很快就消失。
  
在IT行业想要成为永久的赢家是不可能的，技术不断地的提高更新，Xen和KVM将在相当长一段时间内共存，市场足够大，需要诸多解决方案，这两种技术背后都有充足的技术支持让它们在未来数年内和平共处

  红帽专家解读: 虚拟化技术KVM和XEN的区别


  出处:CIOAge.com 文: 凌云通

  
    问: 想请问一下KVM的虚拟化技术和原来的XEN虚拟化技术有什么区别，而且在今后redhat是否不会在redhat里在集成XEN的功能，而转向对KVM的支持。
  
  
    答: XEN目前支持Full Virtualization(全虚拟化) 和 Para Virtualization.
  
  
    Full Virtualization的好处在于现有的x86架构的操作系统可以不用修改，直接运行在虚拟机上。 Para Virtualization的好处是性能好，但是虚拟机上运行的操作系统内核要修改。
  
  
    目前主流的厂家的虚拟化重点都是放在Full Virtualization上面。
  
  
    KVM采用的是Full Virtualization，需要CPU支持VT。 如何确认你的CPU是否支持VT,查看cpu flag, intel cpu flag 会有 "vmx" , amd cpu flag 会有 "svm".
  
  
    从架构上讲，xen是自定制的hypervisor，对硬件的资源管理和调度，对虚拟机的生命周期管理等，都是从头开始写的。  KVM全称是Kernel-based Virtual Machine, kernel代表的是Linux kernel。KVM是一个特殊的模块，Linux kernel加载此模块后，可以将Linux kernel 变成hypervisor，因为Linux kernel已经可以很好的实现对硬件资源的调度和管理，KVM只是实现了对虚拟机生命周期管理的相关工作。 KVM的初始版本只有4万行代码，相对于xen的几百万行代码显得非常简洁。
  
  
    更多关于KVM架构的信息，请参考KVM白皮书:
 http://www.linuxinsight.com/files/kvm_whitepaper.pdf
  
  
    红帽在2007年发布RHEL5，采用的是xen来提供虚拟化功能。从红帽RHEL5.4开始，xen和kvm同时存在。 RHEL5上的xen，红帽会支持到2014年。 后续红帽的重点会放在KVM上面。
  
  
  
  
    2008年 RedHat 收购 Qumranet 以后就一直在家搞他的 KVM，没有对 Xen 做任何升级，RHEL/CentOS 5.5 上默认的 Xen 依旧是很老很老的公元2007年发布的 Xen 3.1.2 版本。更糟糕的是 RedHat 在后续的RedHat Enterprise Linux 6 里彻底放弃了 Xen. 如果以后想在新版本的 RHEL/CentOS 上用 Xen 的话就需要使用第三方源或者自己动手编译 Xen 源代码。
  
  
    http://www.vpsee.com/2010/11/upgrade-xen-on-centos-5-5-to-xen-3-4-3/
  

  
    关于KVM和Xen不得不说的事儿
  


  原创作品，允许转载，转载时请务必以超链接形式标明文章 原始出处 、作者信息和本声明。否则将追究法律责任。http://virtualizing.blog.51cto.com/687668/136543
  
    本文选择性的翻译了Xen/KVM的开发者Anthony Liguori的一篇blog。 在KVM刚出现的时候，媒体上有很多关于Xen的FUD。。。。比如Xen is dead啊，KVM进了Linux kernel,而Xen努力了很久也没有进啦等等。这篇文章从技术角度分析了KVM和Xen的差异，当然是站在一个Linux开发者的角度。 Anthony本人也是这两个项目的核心开发者，所以这篇文章就值得一读了。
  
  
    —————————————–
 "…现在围绕着KVM，Xen和Linux虚拟化的言论已经非常的让人感到困惑了。我将尽我最大的努力来澄清这些事情。。。。"
 "我认为我们最终不得不承认我们–Linux 社区, 在Xen上犯了一个非常大的错误。Xen从来就不应该被包含进Linux发行版。我们已经开始考虑这个问题，已经在在密室里面低声谈论这个问题，已经开始尽我们的最大努力避免它。"
 "我这样说，并不是因为Xen不是一个有用的技术，当然也不是因为人们不应该用Xen。Xen是一个而非常有用的项目，能够真正在企业环境里面产生巨大的 影响力。只不过，Xen现在，将来，也不会成为Linux的一部分。因此，把Xen包含进Linux发行版只会使广大的用户对Linux和Xen之间的关 系感到困惑。"
  
  
    "Xen是一个基于Nemesis微内核的hypervisor。当前各Linux发行版包含Xen，默认安装了一个Linux guest(也就是dom0),并尽其最大努力掩盖Xen不是Linux的一部分的真相。他们这一点到做得很棒，以至于大多数的用户根本没有意识到他们正 在运行一个完全不同的OS。这看上去有些荒谬。这就好像Linux发行版自动包含一个NetBSD的kernel，当你想运行LAMP的时候就切换到这个 NetBSD内核。我们不会在发行版中包含一个purpose-build的kernel。我们包含一个kernel,并且确保它对所有的用户都工作正 常。这才是Linux发行版被成为Linux的原因。当你把Linux kernel拿走之后，它就不再是Linux了。"
  
  
    "当个Linux发行版第一次包含Xen的时候，这主要是出于绝望。Virtualization过去是，现在也是一个热门的技术。Linux过去 没有提供任何的native hypervisor的能力。大多数的Linux kernel开发者也对virtualization也知道得不多。因此Xen很容易的使用了一个purpose-build的kernel，并且这个 kernel还有一个相当好的community。我们做了一个龌龊的决定: 包含Xen到发行版中，而不是把Linux变成一个合适的 hypervisor."
  
  
    "这个决定开始让我们感到头疼了，因为它使得大量的用户感到困惑。当人们在谈论Xen没有被合并到Linux，我不认为他们认识到了Xen将来永远 也不会被合并到Linux。Xen将永远是一个独立的，purpose-build kernel。是有一些补丁能让Linux作为一个guest很好的运行在Xen之上。这些补丁很有可能在将来被合并到Linux，但Xen永远不会成为 Linux的一部分。"
 "这并不意味着Xen已经死亡或者不应该鼓励用户从一个开始就使用它。在那个时候，Xen是一个最好的，可行的解决方案。即使在当前这个瞬间，仍然不清楚 是否在所有的情况下，Linux作为一个hypervisor都要好于Xen. 我没有说，所有的用户都应该一股脑的从Xen迁移到Linux。。。"
  
  
    "我是一个Linux开发者，像所有其他尝试着让Linux能很好的运行在所有的平台上，从大型机到DVD播放器，的Linux hacker一样，我将继续工作，让Linux成为一个hypervisor. Linux社区将把Linux变成一个最好的hypervisor. Linux发行版将停止为了virtualization包含一个purpose-build kernel，转而直接依靠Linux来实现它。"
  
  
    "看一看业界其他公司，我很惊奇其他kernel没有走Linux这个方向: 将virtualization直接添加到kernel里面。为什么 Windows不能很好地胜任作为一个hypervisor，以至于不得不重写一个新的kernel(Hyper-V). 为什么Solaris不能很好地胜任作为一个hypervisor，以至于需要SUN包含Xen在xVM中。"
  
