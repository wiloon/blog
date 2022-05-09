---
title: openstack
author: "-"
date: 2018-03-29T08:57:23+00:00
url: /?p=12087
categories:
  - Inbox
tags:
  - reprint
---
## openstack
https://www.cnblogs.com/wangle1001986/p/5320752.html
  
https://www.zhihu.com/question/54447067

openstack是云管理平台,其本身并不提供虚拟化功能,真正的虚拟化能力是由底层的hypervisor (如KVM、Qemu、Xen等) 提供。所谓管理平台,就是为了方便使用而已。打一个不恰当的比方,订单管理平台之类的产品,其实就是整合了一系列的sql调用而已。类似的,如果没有openstack,一样可以通过virsh、virt-manager来实现创建虚拟机的操作,只不过敲命令行的方式需要一定的学习成本,对于普通用户不是很友好。

作者: Zongrong Zheng
  
链接: https://www.zhihu.com/question/54447067/answer/292892408
  
来源: 知乎
  
著作权归作者所有。商业转载请联系作者获得授权,非商业转载请注明出处。

OpenStack与KVM的区别与联系
  
转: https://www.aliyun.com/zixun/content/2_6_280418.html

OpenStack与KVM都是目前IT界比较热门的两个词汇。它们都是开源的,都与Linux有着千丝万缕的关系。但这两者还是有很大的差别呢。

OpenStack: 开源管理项目

OpenStack是一个旨在为公共及私有云的建设与管理提供软件的开源项目。它不是一个软件,而是由几个主要的组件组合起来完成一些具体的工作。OpenStack由以下五个相对独立的组件构成: 

lOpenStack Compute(Nova)是一套控制器,用于虚拟机计算或使用群组启动虚拟机实例；

lOpenStack镜像服务(Glance)是一套虚拟机镜像查找及检索系统,实现虚拟机镜像管理；

lOpenStack对象存储(Swift)是一套用于在大规模可扩展系统中通过内置冗余及容错机制,以对象为单位的存储系统,类似于Amazon S3；

lOpenStack Keystone,用于用户身份服务与资源管理以及

lOpenStack Horizon,基于Django的仪表板接口,是个图形化管理前端。

这个起初由美国国家航空航天局和Rackspace在2010年末合作研发的开源项目,旨在打造易于部署、功能丰富且易于扩展的云计算平台。OpenStack项目的首要任务是简化云的部署过程并为其带来良好的可扩展性,企图成为数据中心的操作系统,即云操作系统。

KVM: 开放虚拟化技术

KVM (Kernel-based Virtual Machine) 是一个开源的系统虚拟化模块,它需要硬件支持,如Intel VT技术或者AMD V技术,是基于硬件的完全虚拟化,完全内置于Linux。

2008年,红帽收购Qumranet获得了KVM技术,并将其作为虚拟化战略的一部分大力推广,在2011年发布RHEL6时支持KVM作为唯一的hypervisor。KVM主打的就是高性能、扩展性、高安全,以及低成本。

与Linux的缘分

一个被某些热心支持者成为云时代的Linux,是公有云与私有云的开源操作系统。一个则是Linux内核的一部分,将Linux转换成一个Type-1 hypervisor,无需任何变更就能享受现有的Linux内核调度、内存管理和设备支持。

OpenStack炙手可热,它如同Linux一样,旨在构建一个内核,所有的软件厂商都围绕着它进行工作。OpenStack的许多子项目,对云计算平台中的各种资源 (如计算能力、存储、网络) 提供敏捷管理。此外,OpenStack也提供对虚拟化技术的支持。

KVM集成在Linux的各个主要发行版本中,使用Linux自身的调度器进行管理。KVM专注于成为最好的虚拟机监控器,是使用Linux企业的不二选择,加上它还支持Windows平台,所以也是异构环境的最佳选择。

OpenStack与KVM都发展迅猛

OpenStack是一个拥有众多支持者的大项目。时至今日,已经有超过180家企业和400多位开发人员对这一项目积极地做着贡献,而其生态系统甚至更为庞大,已经超过了5600人和850家机构。在今年9月,OpenStack基会正式成立。白金会员有红帽、IBM与惠普等,黄金会员包括思科、戴尔与英特尔等。

OpenStack基本上是一个软件项目,有近55万行代码。分解成核心项目、孵化项目,以及支持项目和相关项目。除了以上提及的五大组成,与虚拟网络有关的Quantum首次被列为核心项目。

KVM是一个脱颖而出的开放虚拟化技术。它是由一个大型的、活跃的开放社区共同开发的,红帽、IBM、SUSE等都是其成员。2011年,IBM、红帽、英特尔与惠普等建立开放虚拟化联盟 (OVA) ,帮助构建KVM生态系统,提升KVM采用率。如今,OVA已经拥有超过250名成员公司,其中,IBM有60多位程序员专门工作于KVM开源社区。

OpenStack与KVM的解决方案

在去年9月22日发布Diablo之后,OpenStack社区随即开始着手新版本的设计和开发,新版本开发代号为Essex。此前发布有四个版本: Austin、Bexar、Cactus与Diablo。新版本发布包含云计算控制中心Nova、镜像服务Glance、认证服务Keystone和Dashboard项目Horizon,也包括对象存储项目Swift。

由此可以看出,OpenStack是一个框架,一个可以建立公有云和私有云的基础架构。它并不是一个现成的产品,要想开展基础架构方面的工作,企业需要顾问和开发人员。很多时候还需要第三方的集成工具。

KVM可通过购买Linux版本获得,或作为独立hypervisor单独购买。最近,IBM KVM (北京) 卓越中心落户北京,展示IBM及合作伙伴基于KVM的产品,包括IBM SmartCloud Entry、IBM System Director VMControl、Red Hat Enterprise Virtualization及SUSE云。

OpenStack与KVM相互辉映

OpenStack几乎支持所有的虚拟化管理程序,不论是开源的 (Xen与KVM) 还是厂商的 (Hyper-V与VMware) 。但在以前,OpenStack是基于KVM开发的,KVM常常成为默认的虚拟机管理程序。两者都使用相同的开放源理念与开发方法。

如今,多数企业用户在IT环境中使用了超过一种的虚拟化软件,有一半的用户选择将开源产品作为性价比更高的虚拟化替代方案。IDC报道中指出,OpenStack是KVM增长的一个巨大机会。OpenStack是一个具有巨大的行业发展动力,并拥有一个充满活力的社区的云计算平台,有95%的OpenStack平台由KVM驱动。因此,随着OpenStack的增长,KVM也会相应增长。

小结

虽然OpenStack与KVM在IT界比较受关注,但是它们都存在一些劣势。比如OpenStack引发了厂商之间的利益冲突,在兼容性方面有待提供,开发成本也较高,服务支持也有点滞后。KVM市场占有率很低,成熟度不够。但是,两者都有强大的发展动力,也有各大IT厂商的持续支持。开源终究还是会胜出呢,这个趋势不可避免。