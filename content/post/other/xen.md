---
title: Xen
author: "-"
date: 2011-11-26T07:02:20+00:00
url: /?p=1613
categories:
  - Linux

tags:
  - reprint
---
## Xen

  
    
      
        Xen 是一个开放源代码虚拟机监视器，由剑桥大学开发。它打算在单个计算机上运行多达100个满特征的操作系统。操作系统必须进行显式地修改 ("移植") 以在Xen上运行 (但是提供对用户应用的兼容性) 。这使得Xen无需特殊硬件支持，就能达到高性能的虚拟化.
      
      
      
        IBM经常在其主机和服务器上使用虚拟机来尽可能发挥其性能，并类似chroot监禁那样将程序置于隔离的虚拟OS中以增强安全性。除此之外，它还能使不同和不兼容的OS运行在同一台计算机上。Xen对虚拟机活跃迁移的支持允许工荷平衡和避免停时。
      
  


  
    
  
  
  
    与其它虚拟机的比较
  
  
    Denali使用准虚拟化技术来提高x86电脑上虚拟机的性能。Denali的虚拟机为因特网服务专门支持了最小化的操作系统。系统可以运行上千个虚拟机。Xen与Denali不同，因为它试图运行适当数量的完整操作系统，而非大量轻量级操作系统。
  
  
    VMware为x86提供虚拟机，这些虚拟机可以运行未修改的PC操作系统。所涉及的技术极为复杂，也导致了性能的 (有时相当显著) 下降。Xen牺牲了完全的二进制兼容，换取相对的简易性和改善的性能。
  
  
  
  
  
    Xen的准虚拟化
  
  
    Xen通过一种叫做准虚拟化的技术获得高性能，甚至在某些与传统虚拟技术极度不友好的架构上 (x86) ，Xen也有上佳的表现。与那些传统通过软件模拟实现硬件的虚拟机不同，在Intel VT-X支持下3.0版本之前的Xen需要系统的来宾权限，用来和Xen API进行连接。到目前为止，这种技术已经可以运用在NetBSD, GNU/Linux, FreeBSD和Plan 9系统上。在Brainshare 2005会议上，Novell展示了NetWare与 Xen的连通。与Windows XP连通的技术曾在Xen开发初期进行，但微软的协议未能允许它发布。Sun公司也正在积极地将Solaris移植到Xen平台之上。
  
  
    Xen的半虚拟化
  
  
    Xen通过一种叫做半虚拟化的技术获得高效能的表现(较少的效能损失, 典型的情况下大约损失 2%, 在最糟的情况下会有 8% 的效能耗损; 与其它使用完全的虚拟化却造成最高到 20% 损耗的其他解决方案形成一个明显的对比)，甚至在某些与传统虚拟技术极度不友好的架构上 (x86) ，Xen也有极佳的表现。与那些传统通过软件模拟实现硬件的虚拟机不同，在3.0版本及在Intel VT-X支援前的Xen需要让客户操作系统 (guest operating systems) 与Xen API进行连接。到目前为止，这样连结已经可以运用在NetBSD, GNU/Linux, FreeBSD和贝尔实验室的Plan 9系统上。在Brainshare 2005会议上，Novell展示了NetWare与 Xen的连通。与Windows XP连通的技术曾在Xen开发初期进行，但微软的协议未能允许它发布。Sun微系统公司也正积极研究Solaris与Xen的连结，使其能在Xen平台上运作。
  
  
    Xen的完全虚拟化
  
  
    Intel对Xen贡献修改以支持其VT-X Vanderpool架构扩展。如果主系统支持Vanderpool或者Pacifica扩展 (Intel和AMD对本地支持虚拟化的扩展) ，这项技术将允许未修改的客作业系统运行在Xen虚拟机中。事实上，那意味著性能的提升，并且你可以在没有进行任何协议不允许的修改的情况下对Windows进行虚拟。
  
  
    虚拟机的迁移
  
  
    Xen虚拟机可以在不停止的情况下在局域网内多个物理主机之间实时迁移。在操作过程中，虚拟机在没有停止工作的情况下内存被反复的复制到目标机器。虚拟机在最终目的地开始执行之前，会有一次60-300毫秒秒的非常短暂的暂停以执行最终的同步化，给人无缝迁移的感觉。类似的技术被用来暂停一台正在运行的虚拟机到磁盘，并切换到另外一台，第一台虚拟机在以后可以恢复。
  
  
    
  
  
  
    平台支持
  
  
    Xen目前可以运行在x86系统上，并正在向x86_64、IA64、PPC移植。移植到其他平台从技术上是可行的，未来有可能会实现。
  