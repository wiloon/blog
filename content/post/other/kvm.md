---
title: 虚拟化, KVM
author: "-"
date: 2011-11-26T07:28:57+00:00
url: /?p=1619
categories:
  - Linux
  - VM

tags:
  - reprint
---
## 虚拟化, KVM
### intel 虚拟化 VT-d VT-x VT-c
简单描述理解 VT-d VT-x VT-c

VT-d 英文全程为 Virtualization Technology for Directed I/O

其中 VT 是 Virtualization Technology 的缩写，d代表Directed

VT-d 的 Intel 官方中文名称是 定向 I/O 虚拟化技术 ，这个技术就是俗称的虚拟化直通技术，就是允许宿主机将某些硬件资源 (比如硬盘、显卡、网卡) 的管辖权直接移交给虚拟机，此时宿主机将不能再使用此硬件，虚拟机会以直通独占的方式使用它们，这种直通的技术带来的好处就是，虚拟机中使用该硬件的性能损耗是极小的, 改善了 I/O 设备在虚拟化环境中的性能并且隔离更加彻底提高了系统的安全性

VT-x 其实就是 Intel Virtualization Technology

至于为什么后边有个 x 呢？

是因为英特尔在起名字的时候，将x86平台上的VT技术，称之为VT-x；在Itanium平台上的VT技术，称之为VT-i。

VT-x 是 Intel CPU 的硬件虚拟化技术，提供内存以及虚拟机的硬件隔离，这也是平常我们想在 intel 平台上做虚拟化最基本需要支持的技术。

VT-x不仅需要处理器的支持，也需要主板、BOIS的支持

VT-c 英文全程为 Virtualization Technology for Connectivity

VT-c 主要是针对提高网络 I/O 提供的虚拟化技术，它可以在一个物理网卡上，建立针对虚拟机的设备队列，最大限度的提高 I/O 吞吐率。

我看网上文章千篇一律的都只是官方的介绍一下 VMDq 和 VMDc ，甚至搞不清 VT-d 和 VT-c 到底有什么区别

其实这个很简单

一个数据包的处理，传统方式是由虚拟机管理系统(CPU处理)来分配这个数据包到底给到哪台虚拟机，现在是由网卡的硬件直接来处理，所以减少了处理延迟，提高了效率

和 VT-d 有什么区别？

VT-d 是可以将一个物理网卡直通给一个虚拟机。现在的 VT-c 就很厉害了，可以将一个物理网卡分成十份，分别直通给10个虚拟机，并且这十份都是隔离互不影响的，注意，这里我用了直通两个字，也就是分割成十份这个操作是不经过虚拟机管理系统的 (也就是不经过CPU) ，所以 I/O 性能很高，并且减少CPU的负载

作者: Feng

转载请尽量注明来源 : www.d3tt.com

KVM:Kernel-based Virtual Machine的简写，是rhel5.4推出的最新虚拟化技术，目前红帽只支持在64位的rhel5.4上运行kvm,同时硬件需要支持VT技术，使用kvm虚拟机的时候需要关闭SELinux;

Red Hat从2009年6月中旬开始在部分企业级用户那里开始了对Red Hat Enterprise Virtualization(RHRV)的beta测试。RHEV是Red Hat去年收购虚拟化厂商Qumranet获得的一项hypervisor技术。Citrix通过收购获得的Xen就是因为Linux hypervisor而被人们所熟知。不过Red Hat的KVM被认为是将成为未来Linux hypervisor的主流。Red Hat产品和技术总裁Paul Cormier表示: "KVM最大的好处就在于它是与Linux内核集成的。未来几年人们的关注焦点仍然集中在hypervisor上。hypervisor是**操作系统**的一项功能，自然能够被用户所接受。

从Linux 2.6.20开始内核中已经开始集成KVM。因此，由Fedora社区开发的Fedora也开始支持KVM。Linux 2.6.20之后的Linux发行版本的内核中也都将KVM作为基本的hypervisor。

Red Hat从进行beta测试的Red Hat Enterprise Linux(RHEL)5.4也开始装载了KVM。Red Hat日本营销本部部长中井雅也先生解释说: "为了确保企业用户的稳定性，我们进行了严格的beta测试。这对与**开源**社区合作的Red Hat来说是很不寻常的。由此看来，这表明Red Hat非常重视KVM基本的虚拟化性能。"

KVM是进入Linux内核的虚拟化项目，它刚刚起步，还不为众人所熟知。但随着RedHat下一步推广KVM力度的加大，相信不久的将来KVM会逐渐占据市场的主要位置。
 现在所说的虚拟化，一般都是指在CPU硬件支持基础之上的虚拟化技术。KVM也同hyper-V、Xen一样依赖此项技术。没有CPU硬件虚拟化的支持，KVM是无法工作的。
 准确来说，KVM是Linux的一个模块。可以用modprobe去加载KVM模块。加载了模块后，才能进一步通过其他工具创建虚拟机。但仅有KVM模块是远远不够的，因为用户无法直接控制内核模块去作事情: 还必须有一个用户空间的工具才行。这个用户空间的工具，开发者选择了已经成型的开源虚拟化软件QEMU。说起来QEMU也是一个虚拟化软件。它的特点是可虚拟不同的CPU。比如说在x86的CPU上可虚拟一个Power的CPU，并可利用它编译出可运行在Power上的程序。KVM使用了QEMU的一部分，并稍加改造，就成了可控制KVM的用户空间工具了。所以你会看到，官方提供的KVM下载有两大部分三个文件，分别是KVM模块、QEMU工具以及二者的合集。也就是说，你可以只升级KVM模块，也可以只升级QEMU工具。这就是KVM和QEMU的关系。  至此，你已经可以使用QEMU工具创建虚拟机了。但我们会发现RedHat的虚拟化并非如此简单。与之相关的还有libvirt、VMM等。原因就是因为QEMU工具效率不高，不易于使用。libvirt是一套C语言的API，现在也有其他语言的了。它负责将不同类型的虚拟化工具的差异完全屏蔽掉。例如Xen的管理命令是xm，而KVM则是qemu-kvm。使用libvirt，你只需要通过libvirt提供的函数连接到Xen或者KVM宿主机，便可以用同样的命令指挥不同的虚拟机了。libvirt不仅提供了API，还自带了一套管理虚拟机的命令——virsh。你可以通过使用virsh命令来进一步了解libvirt。但最终用户更渴望的是图形用户界面，这就是VMM的事情了。VMM是一套用python写的虚拟机管理图形界面，用户可以通过它直观地操作不同的虚拟机。VMM就是利用了libvirt的API参数实现的。

以上这些就是RedHat虚拟化技术的大致架构了，RedHat还有一套用于大规模管理KVM虚拟机的工具，叫oVirt，现正处于开发过程中。有兴趣的朋友可以去看看。上述软件的官方链接在本网站首页上均有。
  


>https://mp.weixin.qq.com/s?__biz=MzAxNzU3NjcxOA==&mid=2650731258&idx=1&sn=f0293a563851bdbb52cc5a9cedd14dd6&exportkey=AXdGcrSfdrF0r17rzGstEiE%3D&acctmode=0&pass_ticket=1LNuuzGLwdjHEXOvMPmVeAPvrgBB0fE9mx4esSgeYM06PZpYntpXVI9i%2FbGqHZbq&wx_header=0