---
title: eclipse.ini
author: "-"
date: 2013-05-17T03:18:45+00:00
url: /?p=5478
categories:
  - Java
tags:
  - reprint
---
## eclipse.ini

[http://www.cnblogs.com/yan5lang/archive/2011/05/24/2055867.html](http://www.cnblogs.com/yan5lang/archive/2011/05/24/2055867.html)

Eclipse的启动由$ECLIPSE_HOME/eclipse.ini控制，如果$ECLIPSE_HOME 没有被定义，则Eclipse安装目录下的默认eclipse.ini会生效。

eclipse.ini是一个文本文件，其内容相当于在Eclipse运行时添加到 Eclipse.exe之后的命令行参数。

其格式要求:

1: 所有的选项及其相关的参数必须在单独的一行之内

2: 所有在-vmargs之后的参数将会被传输给JVM，所有如果所有对Eclipse 设置的参数必须写在-vmargs之前 (就如同你在命令行上使用这些参数一样)
  
默认情况下，eclipse.ini的内容如下:

-showsplash
  
org.eclipse.platform
  
-launcher.XXMaxPermSize
  
256m
  
-vmargs
  
-Xms40m
  
-Xmx256m

上面的配置表示堆空间初始大小为40M，最大为256M，PermGen最大为256M。

指定虚拟机

建议你使用eclipse.ini来指定一个确定的JVM，而不是使用默认的情况，因为很多情况下你无法确认你的Eclipse到底使用的你机器上安装的哪个JVM，使用eclipse.ini来指定使得你能指定并确认之。

下面的例子将展示如何正确的使用 -vm选项

注意-vm选项的格式有严格的要求:
  
1: -vm选项和它的值 (路径) 必须在单独的一行
  
2: 其值必须严格地指向Java可执行文件，而不仅仅只是Java home目录。
  
3: -vm选项必须在-vmargs选项之前，之前已经说过，所有在-vmargs之后的选项将会直接被传递给JVM

Windows Example

-showsplash
  
org.eclipse.platform
  
-launcher.XXMaxPermSize
  
256m
  
-vm
  
C:\Java\JDK\1.5\bin\javaw.exe
  
-vmargs
  
-Xms40m
  
-Xmx512m

Linux Example

在Linux操作系统中，格式和Windows中很类似

-showsplash
  
org.eclipse.platform
  
-launcher.XXMaxPermSize
  
256m
  
-vm
  
/opt/sun-jdk-1.6.0.02/bin/java
  
-vmargs
  
-Xms40m
  
-Xmx512m

Mac OS X Example

指定Java 6:

-showsplash
  
org.eclipse.platform
  
-launcher.XXMaxPermSize
  
256m
  
-vm
  
/System/Library/Frameworks/JavaVM.framework/Versions/1.6.0/Home/bin/java
  
-vmargs
  
-Xms40m
  
-Xmx512m

堆(Heap)和非堆(Non-heap)内存
  
按照官方的说法: "Java虚拟机具有一个堆，堆是运行时数据区域，所有类实例和数组的内存均从此处分配。堆是在 Java
  
虚拟机启动时创建的。""在JVM中堆之外的内存称为非堆内存(Non-heap memory)"。可以看出JVM主要管理两种类型的内存: 堆和非堆。
  
简单来说堆就是Java代码可及的内存，是留给开发人员使用的；
  
非堆就是JVM留给自己用的，所以方法区、JVM内部处理或优化所需的内存(如JIT编译后的代码缓存)、每个类结构(如运行时常数池、字段和方法数据)以及方法和构造方法
  
的代码都在非堆内存中。
  
堆内存分配:
  
JVM初始分配的内存由-Xms指定，默认是物理内存的1/64；
  
JVM最大分配的内存由-Xmx指定，默认是物理内存的1/4。
  
默认空余堆内存小于40%时，JVM就会增大堆直到-Xmx的最大限制；
  
空余堆内存大于70%时，JVM会减少堆直到-Xms的最小限制。
  
因此服务器一般设置-Xms、-Xmx相等以避免在每次GC 后调整堆的大小。

非堆内存分配:
  
JVM使用-XX:PermSize设置非堆内存初始值，默认是物理内存的1/64；
  
由XX:MaxPermSize设置最大非堆内存的大小，默认是物理内存的1/4。

JVM内存限制(最大值)
  
首先JVM内存限制于实际的最大物理内存，假设物理内存无限大的话，JVM内存的最大值跟操作系统有很大的关系。
  
简单的说就32位处理器虽然可控内存空间有4GB,但是具体的操作系统会给一个限制，这个限制一般是2GB-3GB (一般来说
  
Windows系统下为1.5G-2G，Linux系统下为2G-3G) ，而64bit以上的处理器就不会有限制了。

设置VM参数导致程序无法启动主要有以下几种原因:
  
1) 参数中-Xms的值大于-Xmx，或者-XX:PermSize的值大于-XX:MaxPermSize；
  
2) -Xmx的值和-XX:MaxPermSize的总和超过了JVM内存的最大限制，比如当前操作系统最大内存限制，或者实际的物理内存等等。
  
说到实际物理内存这里需要说明一点的是，如果你的内存是1024MB，但实际系统中用到的并不可能是1024MB，因为有一部分被硬件占用了。

为何将上面的参数写入到eclipse.ini文件Eclipse没有执行对应的设置？
  
那为什么同样的参数在快捷方式或者命令行中有效而在eclipse.ini文件中是无效的呢？这是因为我们没有遵守eclipse.ini文件的设置规则:
  
参数形如"项 值"这种形式，中间有空格的需要换行书写，如果值中有空格的需要用双引号包括起来。比如我们使用-vm
  
C:\Java\jre1.6.0\bin\javaw.exe参数设置虚拟机，在eclipse.ini文件中要写成这样:
  
-vm
  
C:\Java\jre1.6.0\bin\javaw.exe

按照上面所说的，最后参数在eclipse.ini中可以写成这个样子:
  
-vmargs
  
-Xms128M
  
-Xmx512M

-XX:PermSize=64M
  
-XX:MaxPermSize=128M
  
实际运行的结果可以通过Eclipse中
  
"Help"-"About Eclipse SDK"窗口里面的"Configuration Details"按钮进行查看。
  
另外需要说明
  
的是，Eclipse压缩包中自带的eclipse.ini文件内容是这样的:
  
-showsplash
  
org.eclipse.platform

-launcher.XXMaxPermSize
  
256m
  
-vmargs
  
-Xms40m
  
-Xmx256m

其中–launcher.XXMaxPermSize (注意最前面是两个连接线) 跟-XX:MaxPermSize参数的含义基本是一样的，我
  
觉得唯一的区别就是前者是eclipse.exe启动的时候设置的参数，而后者是eclipse所使用的JVM中的参数。其实二者设置一个就可以了，所以
  
这里可以把 –launcher.XXMaxPermSize和下一行使用#注释掉。

其他的启动参数。 如果你有一个双核的CPU，也许可以尝试这个参数:
  
-XX:+UseParallelGC
  
让GC可以更快的执行。

下载了新的Eclipse Indigo(3.7)，却无法启动，报错"Failed to create the Java Virtual Machine"，如图:

一开始以为是eclipse3.7要求的JRE版本高，看了下readme，说是: Oracle Java 6 Update 17，我之前装的jdk1.6.16，装了最新版本的jdk，可还是不行。

Google了一下，有一篇文章说是修改eclipse.ini文件中的

Xml代码

-launcher.XXMaxPermSize

256M

修改为128

注意: eclipse.ini中有两处"-launcher.XXMaxPermSize"，都要改。  (不明白为什么一个参数配置两遍)

试了一下这种方法我这边可行，但不明白为什么改小了就可以了。

参考:

eclipse failed to create the java virtual machine 问题图文解析

又在google.com搜了下，另一种解决方案，就是在eclipse.ini中增加jvm的完整路径:

Xml代码

-vm

D:Javajdk1.6.0_29binjavaw.exe

注意: 这个参数的放置位置，我放在文件最下面时还是不行，放在-vmargs参数上面就可以了。

参考:

[http://sunoblog.net/2010/12/eclipse-problem-failed-to-create-the-java-virtual-machine/](http://sunoblog.net/2010/12/eclipse-problem-failed-to-create-the-java-virtual-machine/)

这两种方式在我这里都是可行的，但并不保证包治百病 😀

我的环境是: win xp(32 bit) + Eclipse 3.7 + jdk1.6.0_29
