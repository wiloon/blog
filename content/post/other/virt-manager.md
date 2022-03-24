---
title: virt-manager error
author: "-"
date: 2012-03-24T05:41:48+00:00
url: /?p=2614
categories:
  - Linux
  - VM
tags:
  - KVM

---
## virt-manager error
After I finished the install of the "kvm ,qemu-kvm ,libvirt-bin,virtinst,virt-manager". I want to connect to my vms through the virt-manager .But I come to this error:

> Unable to open a connection to the libvirt management daemon.

> Libvirt URI is: qemu:///system

> Verify that:
  
> - The 'libvirtd' daemon has been started

> And more details:

> Unable to open connection to hypervisor URI 'qemu:///system':
  
> unable to connect to '/var/run/libvirt/libvirt-sock', libvirtd may need to be started: Permission denied
  
> Traceback (most recent call last):
  
> File "/usr/share/virt-manager/virtManager/connection.py", line 971, in _try_open
  
> None], flags)
  
> File "/usr/lib/python2.6/dist-packages/libvirt.py", line 111, in openAuth
  
> if ret is None:raise libvirtError('virConnectOpenAuth() failed')
  
> libvirtError: unable to connect to '/var/run/libvirt/libvirt-sock', libvirtd may need to be started: Permission denied

I look into the details of the error ,and finnally I find that I got not enough permission to access the /var/run/libvirt/libvirt-sock.

I changed the permisson ,and finnally I can use it smoothly.