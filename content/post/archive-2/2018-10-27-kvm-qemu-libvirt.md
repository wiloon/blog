---
title: KVM-Qemu-Libvirt
author: "-"
type: post
date: 2018-10-27T03:36:21+00:00
url: /?p=12820
categories:
  - Uncategorized

---
http://blog.51cto.com/changfei/1672147

KVM-Qemu-Libvirt三者之间的关系

Qemu

Qemu是一个模拟器,它向Guest OS模拟CPU和其他硬件,Guest OS认为自己和硬件直接打交道,其实是同Qemu模拟出来的硬件打交道,Qemu将这些指令转译给真正的硬件。

由于所有的指令都要从Qemu里面过一手,因而性能较差。wKiom1WdDYyjiVZiAAECBtAEQ5E590.jpg

KVM

KVM是linux内核的模块,它需要CPU的支持,采用硬件辅助虚拟化技术Intel-VT,AMD-V,内存的相关如Intel的EPT和AMD的RVI技术,Guest OS的CPU指令不用再经过Qemu转译,直接运行,大大提高了速度,KVM通过/dev/kvm暴露接口,用户态程序可以通过ioctl函数来访问这个接口。见如下伪代码: 

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

KVM内核模块本身只能提供CPU和内存的虚拟化,所以它必须结合QEMU才能构成一个完成的虚拟化技术,这就是下面要说的qemu-kvm。

qemu-kvm

Qemu将KVM整合进来,通过ioctl调用/dev/kvm接口,将有关CPU指令的部分交由内核模块来做。kvm负责cpu虚拟化+内存虚拟化,实现了cpu和内存的虚拟化,但kvm不能模拟其他设备。qemu模拟IO设备（网卡,磁盘等）,kvm加上qemu之后就能实现真正意义上服务器虚拟化。因为用到了上面两个东西,所以称之为qemu-kvm。

Qemu模拟其他的硬件,如Network, Disk,同样会影响这些设备的性能,于是又产生了pass through半虚拟化设备virtio_blk, virtio_net,提高设备性能。

wKiom1WdDc2CEwy6AAGPf4VzQao172.jpg

libvirt

libvirt是目前使用最为广泛的对KVM虚拟机进行管理的工具和API。Libvirtd是一个daemon进程,可以被本地的virsh调用,也可以被远程的virsh调用,Libvirtd调用qemu-kvm操作虚拟机。