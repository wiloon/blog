---
title: "embedded basic"
author: "-"
date: ""
url: ""
categories:
  - inbox
tags:
  - inbox
---
## "embedded basic"

### MCU

微控制单元MCU (Microcontroller Unit) 又叫单片机、微处理器，是集成电路的一种。MCU类似于CPU，是可以执行嵌入式程序的一种集成电路。  
MCU执行的程序叫嵌入式程序。嵌入式程序可以存储在MCU上，也可以存储在外面的存储器上。比如Flash就是存储器的一种。  
模组: 芯片必须配合一些外围设备才能工作。为了方便厂家使用，模组厂家会集成一些外围部件，并写入嵌入式程序，整体打包后作为一个解决方案，给设备厂家使用。
MCU可以算是CPU+RAM+ROM+UART+TIMER+RTC等简单外设。  

SoC (System on Chip) ，中文名是片上系统。SoC含义很多，有一种定义是一个有专用目标的集成电路，是一个包含嵌入式软件的完整系统。SoC方案中，对设备所有智能化操作都是通过模组来实现的，设备无需另外增加MCU。此类控制通常而言比较简单，例如开关，灯之类的产品，只需要几个IO口，就可以控制产品。

### JTAG

JTAG (Joint Test Action Group，联合测试行动小组) 是一种国际标准测试协议 (IEEE 1149.1兼容) ，主要用于芯片内部测试。现在多数的高级器件都支持JTAG协议，如ARM、DSP、FPGA器件等。标准的JTAG接口是4线: TMS、 TCK、TDI、TDO，分别为模式选择、时钟、数据输入和数据输出线。 相关JTAG引脚的定义为:

    TMS: 测试模式选择，TMS用来设置JTAG接口处于某种特定的测试模式；
    TCK: 测试时钟输入；
    TDI: 测试数据输入，数据通过TDI引脚输入JTAG接口；
    TDO: 测试数据输出，数据通过TDO引 脚从JTAG接口输出；

### SWD接口

串行调试 (Serial Wire Debug) ，应该可以算是一种和JTAG不同的调试模式，使用的调试协议也应该不一样，所以最直接的体现在调试接口上，与JTAG的20个引脚相比，SWD只需要4个 (或者5个) 引脚，结构简单，但是使用范围没有JTAG广泛，主流调试器上也是后来才加的SWD调试模式。

SWD和传统的调试方式区别:

SWD模式比JTAG在高速模式下面更加可靠。在大数据量的情况下面JTAG下载程序会失败，但是SWD发生的几率会小很多。基本使用JTAG仿真模式的情况下是可以直接使用SWD模式的，只要你的仿真器支持，所以推荐大家使用这个模式。
在大家GPIO刚好缺一个的时候，可以使用SWD仿真，这种模式支持更少的引脚。
在大家板子的体积有限的时候推荐使用SWD模式，它需要的引脚少，当然需要的PCB空间就小啦！比如你可以选择一个很小的2.54间距的5芯端子做仿真接口。

### RDI 接口

远程调试接口 (Remote Debug Interface) ，是ARM公司提出的标准调试接口，主要用于ARM芯片的仿真，由于各个IDE厂商使用的调试接口各自独立，硬件无法进行跨平台的调试。现在众多的IDE厂家都逐步采用标准RDI作为ARM仿真器的调试接口，因此使跨平台的硬件调试成为可能。EasyJTAG由于使用标准RDI调试接口，因此在任何使用标准RDI接口的IDE调试环境中都可以使用，例如ARM公司的ADS1.2/IAR公司的EWARM 3.30 。

### J-Link

J-Link是最著名的ARM开发调试工具，J-Link由SEGGER公司生产。提供对市面上几乎所有ARM内核芯片的支持。目前最新版本的J-Link产品为V8，支持JTAG和SWD模式。并且对主要的IDE环境如KEIL、IAR都有良好的支持。优点很多，因此也是首选的调试工具。

所以JLINK就是怎么个作用呢？ 起到一个中间转换桥梁，芯片测试用的是JTAG，而JTAG另一端在早起是并口，而现在大多都是USB口，中间过度的重担就交给了Jlink。

### ULink仿真器

ULINK是ARM/KEIL公司推出的仿真器，目前网上可找到的是其升级版本，ULINK2和ULINK Pro仿真器。ULINK/ULINK2可以配合Keil软件实现仿真功能，并且仅可以在Keil软件上使用，增加了串行调试 (SWD) 支持，返回时钟支持和实时代理等功能。开发工程师通过结合使用RealView MDK的调试器和ULINK2，可以方便的在目标硬件上进行片上调试 (使用on-chip JTAG，SWD和OCDS) 、Flash编程。

但是要注意的是，ULINK是KEIL公司开发的仿真器，专用于KEIL平台下使用，ADS、IAR下不能使用。

### ST-Link仿真器

ST-LINK是专门针对意法半导体STM8和STM32系列芯片的仿真器。ST-LINK /V2指定的SWIM标准接口和JTAG / SWD标准接口，其主要功能有:

编程功能: 可烧写FLASH ROM、EEPROM、AFR等；
仿真功能: 支持全速运行、单步调试、断点调试等各种调试方法，可查看IO状态，变量数据等；
仿真性能: 采用USB2.0接口进行仿真调试，单步调试，断点调试，反应速度快；
编程性能: 采用USB2.0接口，进行SWIM / JTAG / SWD下载，下载速度快；

### OpenJTAG

OpenJTAG为开源的JTAG调试工具，功能强大，并且配合其他的开源软件工具可用於在Linux对ARM芯片进行调试，因此在一些社群中使用较多。因为采用FTDI+FPGA双芯片的架构，成本相对较高。

### J-link ARM-OB

因为SEGGER版本众多。其中有一些定制的版本，不带J-link模式而仅支持SWD模式。J-linkARM-OB最初是SEGGER给某个厂家的特殊版本。被破解后目前可以自制，成本约￥20。
ARM-OB因为不支持JTAG模式，而仅支持SWD模式，因此有些较早的ARM7内核MCU，并且不支持SWD模式的芯片，是不能够调试的。

## IDE 说明 Keil、RVDS、ADS、DS-5、MDK

#### Software Development Toolkit (SDT)

ARM公司最早推出的开发工具，最终版本是2.5.2，但从版本2.5.1开始，ARM公司宣布推出一套新的集成开发工具 ADS1.0，用来取代SDT。主要特点如下:

IDE:  CodeWarrior集成环境
编译器:  ARM C compiler
调试器:  armsdARM和THUMB的符号调试器

#### ARM Developer Suite(ADS )

ARM公司大约在1999年推出的，用来代替SDT的集成开发环境，其最终版为1.2.1。主要特点如下:

IDE:  CodeWarrior集成环境
编译器:  ARM C compiler for ADS
调试器:  ARM Extention Degugger(AXD)
仿真器:  ARMulator
硬件调试单元:  Multi-ICE/wiggler
支持调试协议:  RDI
目前，可以从官网[https://developer.arm.com/products/software-development-tools/legacy-tools](https://developer.arm.com/products/software-development-tools/legacy-tools)下载。

#### The RealView Development Suite (RVDS)

RVDS: RealView Development Suite, 包括以前 MMP 平台上用到的 RVCT 编译器，是 ADS  (ARM Development Suite) 的升级产品。
继ADS之后ARM公司在大约2002年推出的集成开发环境，简称RVDS。其编译器也顺便改名叫RVCT，统一使用品牌RealView(RV)。RVDS的集成环境换成了开源的Eclipse，更新到4.1.2版本就停止了。
RVDS分为标准版和专业版两个不同的版本，需要单独下载安装。专业版的主要特点如下 (标准版对某些功能有限制)

支持内核:  全部
IDE:  ARM Workbench IDE (Eclipse 3.3 IDE 的集成开发环境) / CodeWarrior可供选择
编译器:  RVCT (仅仅是改了个名，本质还是ARM C/C++ Compiler)
调试器:  REALVIEW Degugger(RVD)
仿真器:  REALVIEW ISS
硬件调试单元:  Realview ICE(RVI)/ Multi-ICE (3.1版本后不支持Multi-ICE)
支持调试协议:  RDDI/RDI (3.1版本后不支持RDI)
目前，4.0版本的可以从官网[https://developer.arm.com/products/software-development-tools/legacy-tools下载。4.1版本在ARM](https://developer.arm.com/products/software-development-tools/legacy-tools下载。4.1版本在ARM)官网找不到！

插曲
2005年Keil被ARM公司收购。Keil在被收购之前，曾经使用gcc编译器和自己开发的编译器，被收购之后便放弃了自己的编译器和gcc，转而用的是ARM的编译器。不过限制了对高端内核如arm11和a8的支持。收购keil后，keil针对Cortex m3/m0的工具最初叫 RealView mdk。ARM自己的工具叫realview development studio(rvds)。自此，分为两大分支:

MDK系列，MDK-ARM是ARM 公司推荐的针对微控制器的工具链，或者基于单核ARMTDMI，Cortex-M或者Cortex-R处理器的目录芯片组。总结来说，KEIL公司目前有四款独立的嵌入式软件开发工具，即MDK、KEIL C51、KEIL C166、KEIL C251，它们都是KEIL公司品牌下的产品，都基于uVision集成开发环境，其中MDK是RealView系列中的一员。
RVDS (后升级DS-5) 包含全部功能，支持所有ARM内核。

#### Microcontroller Development Kit (MDK)

原名RealView MDK，也称MDK-ARM、KEIL MDK、KEIL For ARM，都是同一个东西。ARM公司现在统一使用MDK-ARM的称呼，MDK的设备数据库中有很多厂商的芯片，是专为微控制器开发的工具，为满足基于MCU进行嵌入式软件开发的工程师需求而设计。主要特点如下

支持内核:  ARM7，ARM9，Cortex-M4/M3/M1，Cortex-R0/R3/R4等ARM微控制器内核。后续可能变化。
IDE:  uVision IDE
编译器:  ARM Compiler 6 (限制在以上内核的编译) 、ARM Compiler 5 (限制在以上内核的编译) 、可配置Gcc
调试器:  μVision Debugger，仅可连接到KEIL设备库中的芯片组 (www.keil.com/dd)
仿真器:  uVision CPU & Peripheral Simulation
硬件调试单元:  uLink /jlink
该工具可以在Keil的官网直接进行下载，不过下载时需要填写一堆信息！

#### ARM Development Studio 5 (DS-5)

DS-5:  ARM Development Studio 5，是 替代 RVDS 的工具。
ARM最新的开发套件。也是目前ARM推出的功能最强大、全面的开发环境。主要特点如下:

支持内核:  全部
IDE:  定制的 Eclipse IDE
编译器:  ARM Compiler 6、ARM Compiler 5、gcc (Linaro GNU GCC Compiler for Linux)
调试器:  DS-5调试器支持ETM 指令和数据跟踪、PTM程序跟踪
仿真器:  DS-5支持ULINK2、ULINKpro和DSTREAM仿真器
Streamline:  性能分析器
模拟器:  RTSM ，支持Cortex-A8 固定虚拟平台 (FVP) 、多核 Cortex-A9 实时模拟器、ARMv8 固定虚拟平台 (FVP)
该工具可以在ARM的官网的[https://developer.arm.com/products/software-development-tools](https://developer.arm.com/products/software-development-tools)直接免费下载，且不需要登陆！

ARM编译套件
ARM公司除了提供了以上各种IDE外，从4.x开始，其也提供了可独立下载使用 (命令行工具) 的编译套件！交旧版本的没有独立提供，但是可以很方便的进行提取从而独立使用！
其中，最新版的独立编译套件可以从[https://developer.arm.com/products/software-development-tools/compilers/arm-compiler/downloads下载，旧点版本的可以通过以下地址下载https://developer.arm.com/products/software-development-tools/compilers/legacy-compiler-releases](https://developer.arm.com/products/software-development-tools/compilers/arm-compiler/downloads下载，旧点版本的可以通过以下地址下载https://developer.arm.com/products/software-development-tools/compilers/legacy-compiler-releases)。再旧的就只能自己搞了。

### segger embedded studio for arm v5.1.0b

#### package manager

- cmsis-core support package

### 天线, 陶瓷天线和PCB天线以及IPEX天线

陶瓷天线是一种适合于蓝牙装置使用的小型化天线。下面云里物里给大家介绍下这三种天线有什么区别。

陶瓷天线又分为块状陶瓷天线和多层陶瓷天线。

块状天线是使用高温将整块陶瓷体一次烧结完成后再将天线的金属部分印在陶瓷块的表面上。而多层天线烧制采用低温共烧的方式讲多层陶瓷迭压对位后再以高温烧结，所以天线的金属导体可以根据设计需要印在每一层陶瓷介质层上，如此一来可以有效缩小天线尺寸，并能达到隐藏天线目的。由于陶瓷本身介电常数比pcb电路板的要高，所以使用陶瓷天线能有效缩小天线尺寸。

PCB天线是指无线接收和发射用的PCB上的部分。

发射时，它把发射机的高频电流转换为空间电磁波；接收时，它又把从空间获取的电磁波变换成高频电流输入接收机。它的优点是: 空间占用较少，成本低廉，不需单独组装天线，不易触碰损坏，整机组装方便，但有代价---牺牲性能。

缺点是: 单个天线场型很难做到圆整，插损高，效率相对低下，容易遭到主板上的干扰。

IPEX天线是一种作为射频电路和天线的接口，被广泛应用于无线局域网 (WLAN) 相关产品单板上。

它的优点是: 场型能控制更好，插损低，信号的方向指向性好，效率高，抗干扰能力强，能减少受到主板上的干扰，而且不用太多的调试匹配，作为终端制造者，只需要外面接一个IPEX的天线即可；

当然也有弊端: 成本叫高，组装起来比较麻烦。

版权声明: 进步始于交流，收获源于分享！转载请保留原文出处，谢谢！
[https://blog.csdn.net/ZCShouCSDN/article/details/81836601](https://blog.csdn.net/ZCShouCSDN/article/details/81836601)  

### linux jlink

[https://boseji.com/posts/segger-jlink-in-manjaro-linux/](https://boseji.com/posts/segger-jlink-in-manjaro-linux/)

### micro python

[https://gitee.com/WeAct-TC/MiniF4-STM32F4x1](https://gitee.com/WeAct-TC/MiniF4-STM32F4x1)
