---
title: KVM-Qemu-Libvirt
author: "-"
date: 2018-10-27T03:36:21+00:00
url: /?p=12820
categories:
  - Uncategorized

tags:
  - reprint
---
## KVM-Qemu-Libvirt
http://blog.51cto.com/changfei/1672147

KVM-Qemu-Libvirt三者之间的关系

## Qemu

Qemu是一个模拟器,它向Guest OS模拟CPU和其他硬件, Guest OS认为自己和硬件直接打交道,其实是同Qemu模拟出来的硬件打交道,Qemu将这些指令转译给真正的硬件。

由于所有的指令都要从Qemu里面过一手,因而性能较差。wKiom1WdDYyjiVZiAAECBtAEQ5E590.jpg

## KVM

KVM是linux内核的模块,它需要 CPU 的支持, 采用硬件辅助虚拟化技术Intel-VT,AMD-V,内存的相关如Intel的EPT和AMD的RVI技术,Guest OS的CPU指令不用再经过Qemu转译,直接运行,大大提高了速度,KVM通过 /dev/kvm暴露接口,用户态程序可以通过 ioctl函数来访问这个接口。见如下伪代码: 

open("/dev/kvm")
  
ioctl(KVM_CREATE_VM)
  
ioctl(KVM_CREATE_VCPU)
  
for (;;) {
      
ioctl(KVM_RUN)
          
switch (exit_reason) {
          
case KVM_EXIT_IO:
          
case KVM_EXIT_HLT:
      
}
  
}

KVM 内核模块本身只能提供CPU和内存的虚拟化, 所以它必须结合QEMU才能构成一个完成的虚拟化技术, 这就是下面要说的 qemu-kvm。

## qemu-kvm

Qemu将KVM整合进来,通过ioctl调用 /dev/kvm接口,将有关CPU指令的部分交由内核模块来做。kvm 负责cpu虚拟化+内存虚拟化, 实现了cpu和内存的虚拟化, 但kvm不能模拟其他设备。qemu模拟IO设备 (网卡,磁盘等) , kvm加上qemu之后就能实现真正意义上服务器虚拟化。因为用到了上面两个东西,所以称之为qemu-kvm。

Qemu 模拟其他的硬件,如Network, Disk,同样会影响这些设备的性能,于是又产生了pass through半虚拟化设备virtio_blk, virtio_net,提高设备性能。

## libvirt

libvirt是目前使用最为广泛的对KVM虚拟机进行管理的工具和API。Libvirtd是一个daemon进程,可以被本地的 virsh 调用,也可以被远程的virsh调用,Libvirtd调用qemu-kvm操作虚拟机。

## libvirt、virsh、virt-manager
https://blog.csdn.net/wanglei_storage/article/details/51107648

libvirt、virsh、virt-manager 介绍
  
kvm 虚拟化中 libvirt 是目前使用最为广泛的对 kvm 虚拟机进行管理的工具和应用程序接口,而且一些常用的虚拟机管理工具 (virsh、virt-install、virt-manager等) 和云计算框架平台都在底层使用libvirt的应用程序接口。

## virsh
virsh 是用于管理虚拟化环境中的客户机和 Hypervisor 的命令行工具, 与 virt-manager 等工具类似, 它也是通过 libvirt API 来实现虚拟化的管理。virsh 是完全在命令行文本模式下运行的用户态工具, 它是系统管理员通过脚本程序实现虚拟化自动部署和管理的理想工具之一。

virt-manager 是虚拟机管理器 (Virtual Machine Manager)  这个应用程序的缩写,也是管理工具的软件包名称。virt-manager 是用于管理虚拟机的图形化的桌面用户接口。

 
**libvirt，virt-manager,virsh**: 由于qemu-kvm的效率及通用性问题，有组织开发了 libvirt 用于虚拟机的管理，带有一套基于文本的虚拟机的管理工具 virsh，以及一套用户渴望的图形界面管理工具 virt-manager。libvirt 是用 python 语言写的通用的API，不仅可以管理 KVM， 也可用于管理XEN

### 内核版本是 2.6.22 或更新版本内建 KVM 模块，可以使用下面命令来检查你的内核版本是否支持KVM :

modprobe -l kvm*

另外，KVM还需要修改过的QEMU(EXTRA仓库中的qemu-kvm)来启动和管理虚拟机。 此时，有两个选择 (根据你需要，选一个即可，比如你不仅使用kvm还需要使用qemu，则选2,否则，一般选1就够用了。直观的区别就是qemu软件包很大，而qemu-kvm很小，qemu-kvm相当于qemu中的qemu-system-x86_64的一个定制版) : 

1. 安装qemu-kvm，以后要运行kvm的时候，就输入qemu-kvm -enable-kvm这个命令

pacman -S kernel26 qemu-kvm

2. 安装qemu >= 0.9.0，和qemu-kvm包冲突，现在也附带了一个可以使用qemu-kvm的，以后要运行kvm的时候就是输入: qemu -enable-kvm。

pacman -S kernel26 qemu

http://blog.sina.com.cn/s/blog_6b1c9ed50100w9jj.html
http://changfei.blog.51cto.com/4848258/1672147
