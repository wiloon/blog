---
title: System.map、vmlinuz、initrd.img
author: "-"
date: 2012-02-26T13:55:06+00:00
url: /?p=2465
categories:
  - Linux
tags:$
  - reprint
---
## System.map、vmlinuz、initrd.img
### vmlinuz
 1.vmlinuz是可引导的、压缩的内核。"vm"代表"Virtual Memory"。Linux
 支持虚拟内存，不像老的操作系统比如DOS有640KB内存的限制。Linux能够使用硬盘空间作为虚拟内存，因此得名"vm"。vmlinuz是可执行 的Linux内核，它位于/boot/vmlinuz，它一般是一个软链接，比如图中是vmlinuz-2.4.7-10的软链接。
 vmlinuz的建立有两种方式。一是编译内核时通过"make zImage"创建，然后通过:"cp
 /usr/src/linux-2.4/arch/i386/linux/boot/zImage/boot/vmlinuz"产生。zImage适用于
 小内核的情况，它的存在是为了向后的兼容性。 
    
    
          2.是内核编译时通过命令make
 bzImage创建，然后通过:"cp/usr/src/linux-2.4/arch/i386/linux/boot/bzImage
 /boot/vmlinuz"产生。bzImage是压缩的内核映像，需要注意，bzImage不是用bzip2压缩的，bzImage中的bz容易引起误解，bz表示"big zImage"。 bzImage中的b是"big"意思。
    
    
    
      zImage(vmlinuz)和bzImage(vmlinuz)都是用gzip压缩的。它们不仅是一个压缩文件，而且在这两个文件的开头部分内嵌有 gzip解压缩代码。所以你不能用gunzip 或 gzip –dc解包vmlinuz。内核文件中包含一个微型的gzip用于解压缩内核并引导它。两者的不同之处在于，老的zImage解压缩内核到低端内存(第一 个640K)，
 bzImage解压缩内核到高端内存(1M以上)。如果内核比较小，那么可以采用zImage或bzImage之一，两种方式引导的系统运行时是相同的。
    
    
    
      大的内核采用bzImage，不能采用zImage。vmlinux是未压缩的内核，vmlinuz是vmlinux的压缩文件。
 二、initrd-x.x.x.img
 initrd是"initial ramdisk"的简写。initrd一般被用来临时的引导硬件到实际内核vmlinuz能够接管并继续引导的状态。图中的initrd-2.4.7- 10.img主要是用于加载ext3等文件系统及scsi设备的驱动。比如，使用的是scsi硬盘，而内核vmlinuz中并没有这个scsi硬件的驱 动，那么在装入scsi模块之前，内核不能加载根文件系统，但
 scsi模块存储在根文件系统的/lib/modules下。为了解决这个问题，可以引导一个能够读实际内核的initrd内核并用initrd修正 scsi引导问题。initrd-2.6.20-1.img是用gzip压缩的文件，initrd实现加载一些模块和安装文件系统等功能。
    
    
    
      initrd映象文件是使用mkinitrd创建的。mkinitrd实用程序能够创建initrd映象文件。这个命令是RedHat专有的。其它
    
    
    
      Linux发行版或许有相应的命令。这是个很方便的实用程序。具体情况请看帮助:man mkinitrd下面的命令创建initrd映象文件。
    
    
    
      
    
    
    
      initrd是linux在系统引导过程中使用的一个临时的根文件系统，用来支持两阶段的引导过程。
    
    
    
      直白一点，initrd就是一个带有根文件系统的虚拟RAM盘，里面包含了根目录'/'，以及其他的目录，比如: bin，dev，proc，sbin，sys等linux启动时必须的目录，以及在bin目录下加入了一下必须的可执行命令。
    
    
    
PC或者服务器linux内核使用这个initrd来挂载真正的根文件系统，然后将此initrd从内存中 卸掉，这种情况下initrd其实就是一个过渡使用的东西。 在现在的许多简单嵌入式linux中一般是不卸载这个initrd的，而是直接将其作为根文件系统使用，在这之前就需要把所需要的程序，命令还有其它文件 都安装到这个文件系统中。其实现在的大多数嵌入式系统也是有自己的磁盘的，所以，initrd在现在大多数的嵌入式系统中也和一般的linux中的作用一 样只是起过渡使用。
    
    
    
      Initrd的引导过程: '第二阶段引导程序'，常用的是grub将内核解压缩并拷贝到内存中，然后内 核接管了CPU开始执行，然后内核调用init()函数，注意，此init函数并不是后来的init进程！！！然后内核调用函数 initrd_load()来在内存中加载initrd根文件系统。Initrd_load()函数又调用了一些其他的函数来为RAM磁盘分配空间，并计 算CRC等操作。然后对RAM磁盘进行解压，并将其加载到内存中。现在，内存中就有了initrd的映象。
    
    
    
      然后内核会调用mount_root()函数来创建真正的根分区文件系统，然后调用sys_mount()函数来加载真正的根文件系统，然后chdir到这个真正的根文件系统中。
    
    
    
      最后，init函数调用run_init_process函数，利用execve来启动init进程，从而进入init的运行过程。
    
    
    
       
      
      
        三、System.map
      
      
      
        内核符号映射表，顾名思义就是将内核中的符号 (也就是内核中的函数) 和它的地址能联系起来的一个列表。是所有符号及其对应地址的一个列表。之所以这样就使 为了用户编程方便，直接使用函数符号就可以了，而不用去记要使用函数的地址。当你编译一个新内核时，原来的System.map中的符号信息就不正确 了。随着每次内核的编译，就会产生一个新的 System.map文件，并且需要用该文件取代原来的文件
      
      
      
        System.map是一个特定内核的内核符号表。它是你当前运行的内核的System.map的链接。
 内核符号表是怎么创建的呢? System.map是由"nm vmlinux"产生并且不相关的符号被滤出。
      
      
      
        下面是System.map文件的一部分:
 c0100000 A _text
 c0100000 t startup_32
 c01000a5 t checkCPUtype
 c0100133 t is486
 c0100142 t is386
 c010018c t L6
 c010018e t ready
 c010018f t check_x87
 c01001b6 t setup_idt
 c01001d3 t rp_sidt
 c01001e0 T stack_start
 c01001e8 t int_msg
 c01001fc t ignore_int
 c010021e T idt_descr
 c0100224 T cpu_gdt_descr
 c0101000 T swapper_pg_dir
 c0102000 T pg0
 c0103000 T pg1
 c0104000 T empty_zero_page
 c0105000 T _stext
 在进行程序设计时，会命名一些变量名或函数名之类的符号。Linux内核是一个很复杂的代码块，有许许多多的全局符号。
 Linux内核不使用符号名，而是通过变量或函数的地址来识别变量或函数名。比如不是使用size_t BytesRead这样的符号，而是像c0343f20这样引用这个变量。
 对于使用计算机的人来说，更喜欢使用那些像size_t BytesRead这样的名字，而不喜欢像c0343f20这样的名字。内核主要是用c写的，所以编译器/连接器允许我们编码时使用符号名，当内核运行时使用地址。
 然而，在有的情况下，我们需要知道符号的地址，或者需要知道地址对应的符号。这由符号表来完成，符号表是所有符号连同它们的地址的列表。上图就是一个内核符号表，由上图可知变量名checkCPUtype在内核地址c01000a5。
 Linux 符号表使用到2个文件:
 /proc/ksyms
 System.map
      
      
      
        /proc/ksyms是一个"proc file"，在内核引导时创建。实际上，它并不真正的是一个文件，它只不过是内核数据的表示，却给人们是一个磁盘文件的假象，这从它的文件大小是0可以看 出来。然而，System.map是存在于你的文件系统上的实际文件。
 当你编译一个新内核时，各个符号名的地址要发生变化，你的老的System.map具有的是错误的符号信息。每次内核编译时产生一个新的System.map，你应当用新的System.map来取代老的System.map。
 虽然内核本身并不真正使用System.map，但其它程序比如klogd，lsof和ps等软件需要一个正确的System.map。如果你使用错误的 或没有System.map，klogd的输出将是不可靠的，这对于排除程序故障会带来困难。没有System.map，你可能会面临一些令人烦恼的提示 信息。
 另外少数驱动需要System.map来解析符号，没有为你当前运行的特定内核创建的System.map它们就不能正常工作。
 Linux的内核日志守护进程klogd为了执行名称-地址解析，klogd需要使用System.map。System.map应当放在使用它的软件能 够找到它的地方。执行:manklogd可知，如果没有将System.map作为一个变量的位置给klogd，那么它将按照下面的顺序，在三个地方查找 System.map:
 /boot/System.map
 /System.map
 /usr/src/linux/System.map
      
      
      
        System.map也有版本信息，klogd能够智能地查找正确的映象(map)文件。