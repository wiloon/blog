---
title: KVM与Xen和VMware的PK
author: "-"
date: 2011-11-26T07:53:04+00:00
url: /?p=1625
categories:
  - Linux
  - VM
tags:$
  - reprint
---
## KVM与Xen和VMware的PK
  
    KVM与Xen和VMware的PK
  


  原创作品，允许转载，转载时请务必以超链接形式标明文章 原始出处 、作者信息和本声明。否则将追究法律责任。http://virtualizing.blog.51cto.com/687668/136544
  
    【sudison】这篇文章翻译至KVM的maintainer Avi Kivity的一篇文章. 文中提到了KVM比ESX和Xen优越的一个地方: 既能获得很好的performance,又能解决设备驱动的维护问题。还是有一定的道理。
  
  
    ——————
 I/O的性能对一个hypervisor而言至关重要。同时，I/O也是一个很大的维护负担，因为有大量需要被支持的硬件设备，大量的I/O协议，高可用性，以及对这些设备的管理。
  
  
    VMware选择性能，但是把I/O协议栈放到了hypervisor里面。不幸的是，VMware kernel是专有的，那就意味着VMware不得不开发和维护整个协议栈。那将意味着开发速度会减慢，你的硬件可能要等一段时间才会得到VMware的支持。
  
  
    Xen选择了可维护这条道路，它将所有的I/O操作放到了Linux guest里面，也就是所谓的domain-0里面。重用Linux来做I/O, Xen的维护者就不用重写整个I/O协议栈了。但不幸的是，这样就牺牲了性能: 每一个中断都必需经过Xen的调度，才能切换到domain 0, 并且所有的东西都不得不经过一个附加层的映射。
  
  
    并不是说Xen已经完全解决了可维护性这个问题: Xen domain 0 kernel仍然是古老的Linux 2.6.18 (尽管2.6.25也已经可用了。【sudison注: 】现在Xen已经在通过domain 0 pv_ops在解决这个问题了) 
  
  
    那KVM是怎么处理的呢？像VMware一样，I/O是被放到hypervisor的上下文来执行的，所以性能上不会有损害。像Xen一样，KVM重用了整个Linux I/O协议栈，所以KVM的用户就自然就获得了最新的驱动和I/O协议栈的改进。
  
