---
title: kernel config 3.2.8
author: "-"
date: 2012-02-28T13:13:59+00:00
url: /?p=2483
categories:
  - Linux
tags:
  - reprint
---
## kernel config 3.2.8

[http://0123.blog.163.com/blog/static/4788312011112214258169/](http://0123.blog.163.com/blog/static/4788312011112214258169/)

[http://www.cnblogs.com/unicode/archive/2010/05/19/1739675.html](http://www.cnblogs.com/unicode/archive/2010/05/19/1739675.html)

[http://blog.csdn.net/unsigned_/article/details/6123426](http://blog.csdn.net/unsigned_/article/details/6123426)

[http://blog.csdn.net/woshixingaaa/article/details/5982246](http://blog.csdn.net/woshixingaaa/article/details/5982246)

1,仔细了解你电脑的硬件型号，越清楚越好切记切记。
  
2.一定要把SCSI控制器的驱动及与文件系统有关的都编译进内核，而不是模块。
  
3.把对启动过程没有关系的驱动，一定要编进模块。
  
4.一定要把你的.config文件复制出来，作为下次重复编译的起点
  
5.在编译前，一定要保证系统中至少有一个可以正常启动的内核
  
6.可能在你正确编译完成后，你的一些系统工具不能正常工作，所以不要盲目追新，和util-bin,linux-util,以及模块工具等不能协同工作就悲摧了。
  
7.一般来说，手动编译的内核启动速度比发行版提供的要快那么一点点，但是，一般的各发行版定制的内核都经过了不同程度的优化，选择自行编译等于放弃了这些优点。除非你清楚你在做什么，否则编译内核只适合喜欢鼓捣学习提高的童鞋。that's all,good luck!

[]Prompt for development and/or incomplete code/drivers
  
对开发中的或者未完成的代码和驱动进行提示, Linux下的很多东西,比如网络设备、文件系统、网络协议等等,它们的功能、稳定性、或者测试等级等等还不能够符合大众化的要求,还处于开发之中。这就是所谓的α版本(阿尔法版本):最初开发版本;接下来的是β版本(beta版本),公开测试版本。如果这是阿尔法版本,那么开发者为了避免收到诸如"为何这东西不工作"的信件的麻烦,常常不会让它发布出去。但是,积极的测试和使用阿尔法版本对软件的开发是非常好的。你只需要明白它未必工作得很好,在某些情况有可能会出问题。汇报详细的出错情况对开发者很有帮助。这个选项同样会让一些老的驱动可用。很多老驱动在后来的内核中已经被代替或者被移除。除非你想要帮助软件的测试,或者开发软件,或者你的机器需要这些特性,否则你可以选N ,那样你会在配置菜单中得到较少的选项。如果你选了Y, 你将会得到更多的阿尔法版本的驱动和代码的配置菜单。

() Cross-compiler tool prefix

交叉编译工具前缀，如果你要使用交叉编译工具的话输入相关前缀。默认不使用。不需要;交叉编译(cross-compile)大致的意思就是在一个平台上为另外一个平台生成代码，也就是说，你在编译时使用的编译器的host和target是不同的，比如你在x86的机器上生成mips的代码。你给本地机器编内核的话，用不到这个。

(ylxy1.2)Local version - append to kernel release
  
本地版本-附加内核发行版本. 在你的内核版本后面加上一串字符来表示版本。这些字符在你使用 uname -a命令时会显示出来。你在这设置的版本字符将会出现在文件的目录和内容中,如果这些文件调用了内核的版本号。你的字符最多不能超过64位。

[*]Automatically append version information to the version string
  
自动生成版本信息。这个选项会自动探测你的内核并且生成相应的版本，使之不会和原先的重复。这需要Perl的支持。由于在编译的命令make-kpkg 中我们会加入-append-to-version选项来生成自定义版本，所以这里选N.

[]Kernel compression mode (Gzip)

((none))Default hostname

[*]Support for paging of anonymous memory(swap)
  
这是使用交换分区或者交换文件来做为虚拟内存的，当然要选上了。

[*]System V IPC 为进程提供通信机制，这将使系统中各进程间有交换信息与保持同步的能力。有些程序只有在选Y的情况下才能运行，所以不用考虑，这里一定要选。

[*] BSD Process Accounting

这是允许用户进程访问内核，将账户信息写入文件中。这通常被认为是个好主意，建议你最好将它选上。将进程的统计信息写入文件的用户级系统调用,主要包括进程的创建时间/创建者/内存占用等信息。

[*]   BSD Process Accounting version 3 file format

选用的话前面所述的进程信息/统计信息将会以新的格式 (V3) 写入，这格式包含进程ID和父进程。注意这个格式和以前的 v0/v1/v2 格式不兼容，所以你需要 升级相关工具来使用它。选不选均可。(选了才能用bootchart)

[*]open by fhandle syscalls

-*- Export task/process statistics through netlink (EXPERIMENTAL)通过网络输出任务/进程的统计数据

-*- Enable per-task delay accounting (EXPERIMENTAL)统计数据包含每个任务/进程的延时

**[*] ..Enable extended accounting over taskstats** CONFIG_TASK_XACCT=y 统计数据包含扩展任务读取数据和发送数据使用的时间

**[*] ....Enable per-task storage I/O accounting** CONFIG_TASK_IO_ACCOUNTING=y 统计数据包括I/O设备产生的字节数

**[*] Auditing support** CONFIG_AUDIT=y 支持审计功能

**[*] ..Enable system-call auditing support** CONFIG_AUDITSYSCALL=y 开启系统调用的审计功能

**IRQ subsystem ->** 中断子系统

**-*- Support sparse irq numbering** CONFIG_SPARSE_IRQ=y 支持稀有的中断号
