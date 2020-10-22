+++
author = "w1100n"
date = "2020-10-22 15:24:45" 
title = "中断"

+++

### 中断（ interrupts ）
中断指当出现需要时，CPU暂时停止当前程序的执行转而执行处理新情况的程序和执行过程。即在程序运行过程中，系统出现了一个必须由CPU立即处理的情况，此时，CPU暂时中止程序的执行转而处理这个新的情况的过程就叫做中断。

### 为什么需要中断?
如果让内核定期对设备进行轮询，以便处理设备，那会做很多无用功，因为外设的处理速度一般慢于CPU，而CPU不能一直等待外部事件。所以能让设备在需要内核时主动通知内核，会是一个聪明的方式，这便是中断。

### 中断处理程序

在响应一个特定中断时，内核会执行一个函数——中断处理程序。中断处理程序与其他内核函数的区别在于，中断处理程序是被内核调用来响应中断的，而它们运行于我们称之为中断上下文的特殊上下文中。

中断处理程序就是普通的C代码。特别之处在于中断处理程序是在中断上下文中运行的,它的行为受到某些限制:
1）不能向用户空间发送或接受数据
2）不能使用可能引起阻塞的函数
3）不能使用可能引起调度的函数

### 上下半部机制
我们期望让中断处理程序运行得快，并想让它完成的工作量多，这两个目标相互制约，如何解决——上下半部机制。

我们把中断处理切为两半。中断处理程序是上半部——接受中断，他就立即开始执行，但只有做严格时限的工作。能够被允许稍后完成的工作会推迟到下半部去，此后，在合适的时机，下半部会被开终端执行。上半部简单快速，执行时禁止一些或者全部中断。下半部稍后执行，而且执行期间可以响应所有的中断。这种设计可以使系统处于中断屏蔽状态的时间尽可能的短，以此来提高系统的响应能力。上半部只有中断处理程序机制，而下半部的实现有软中断实现，tasklet实现和工作队列实现。

我们用网卡来解释一下这两半。当网卡接受到数据包时，通知内核，触发中断，所谓的上半部就是，及时读取数据包到内存，防止因为延迟导致丢失，这是很急迫的工作。读到内存后，对这些数据的处理不再紧迫，此时内核可以去执行中断前运行的程序，而对网络数据包的处理则交给下半部处理。

### 上下半部划分原则
1） 如果一个任务对时间非常敏感，将其放在中断处理程序中执行；

2） 如果一个任务和硬件有关，将其放在中断处理程序中执行；

3） 如果一个任务要保证不被其他中断打断，将其放在中断处理程序中执行；

4） 其他所有任务，考虑放置在下半部执行。

下半部实现机制之软中断
软中断作为下半部机制的代表，是随着SMP（share memoryprocessor）的出现应运而生的，它也是tasklet实现的基础（tasklet实际上只是在软中断的基础上添加了一定的机制）。软中断一般是“可延迟函数”的总称，有时候也包括了tasklet（请读者在遇到的时候根据上下文推断是否包含tasklet）。它的出现就是因为要满足上面所提出的上半部和下半部的区别，使得对时间不敏感的任务延后执行，软中断执行中断处理程序留给它去完成的剩余任务，而且可以在多个CPU上并行执行，使得总的系统效率可以更高。它的特性包括：

a）产生后并不是马上可以执行，必须要等待内核的调度才能执行。软中断不能被自己打断，只能被硬件中断打断（上半部）。

b）可以并发运行在多个CPU上（即使同一类型的也可以）。所以软中断必须设计为可重入的函数（允许多个CPU同时操作），因此也需要使用自旋锁来保护其数据结构。
### 下半部实现机制之tasklet
tasklet是通过软中断实现的，所以它本身也是软中断。

软中断用轮询的方式处理。假如正好是最后一种中断，则必须循环完所有的中断类型，才能最终执行对应的处理函数。显然当年开发人员为了保证轮询的效率，于是限制中断个数为32个。

为了提高中断处理数量，顺道改进处理效率，于是产生了tasklet机制。

Tasklet采用无差别的队列机制，有中断时才执行，免去了循环查表之苦。Tasklet作为一种新机制，显然可以承担更多的优点。正好这时候SMP越来越火了，因此又在tasklet中加入了SMP机制，保证同种中断只能在一个cpu上执行。在软中断时代，显然没有这种考虑。因此同一种软中断可以在两个cpu上同时执行，很可能造成冲突。

总结下tasklet的优点：

（1）无类型数量限制；

（2）效率高，无需循环查表；

（3）支持SMP机制；

它的特性如下：

1）一种特定类型的tasklet只能运行在一个CPU上，不能并行，只能串行执行。

2）多个不同类型的tasklet可以并行在多个CPU上。

3）软中断是静态分配的，在内核编译好之后，就不能改变。但tasklet就灵活许多，可以在运行时改变（比如添加模块时）。

### 下半部实现机制之工作队列（work queue）
上面我们介绍的可延迟函数运行在中断上下文中（软中断的一个检查点就是do_IRQ退出的时候），于是导致了一些问题：软中断不能睡眠、不能阻塞。由于中断上下文出于内核态，没有进程切换，所以如果软中断一旦睡眠或者阻塞，将无法退出这种状态，导致内核会整个僵死。但可阻塞函数不能用在中断上下文中实现，必须要运行在进程上下文中，例如访问磁盘数据块的函数。因此，可阻塞函数不能用软中断来实现。但是它们往往又具有可延迟的特性。

上面我们介绍的可延迟函数运行在中断上下文中，于是导致了一些问题，说明它们不可挂起，也就是说软中断不能睡眠、不能阻塞，原因是由于中断上下文出于内核态，没有进程切换，所以如果软中断一旦睡眠或者阻塞，将无法退出这种状态，导致内核会整个僵死。因此，可阻塞函数不能用软中断来实现。但是它们往往又具有可延迟的特性。而且由于是串行执行，因此只要有一个处理时间较长，则会导致其他中断响应的延迟。为了完成这些不可能完成的任务，于是出现了工作队列，它能够在不同的进程间切换，以完成不同的工作。

如果推后执行的任务需要睡眠，那么就选择工作队列，如果不需要睡眠，那么就选择软中断或tasklet。工作队列能运行在进程上下文，它将工作托付给一个内核线程。工作队列说白了就是一组内核线程，作为中断守护线程来使用。多个中断可以放在一个线程中，也可以每个中断分配一个线程。我们用结构体workqueue_struct表示工作者线程，工作者线程是用内核线程实现的。而工作者线程是如何执行被推后的工作——有这样一个链表，它由结构体work_struct组成，而这个work_struct则描述了一个工作，一旦这个工作被执行完，相应的work_struct对象就从链表上移去，当链表上不再有对象时，工作者线程就会继续休眠。因为工作队列是线程，所以我们可以使用所有可以在线程中使用的方法。

### Linux软中断和工作队列的作用是什么
Linux中的软中断和工作队列是中断上下部机制中的下半部实现机制。

1.软中断一般是“可延迟函数”的总称，它不能睡眠，不能阻塞，它处于中断上下文，不能进城切换，软中断不能被自己打断，只能被硬件中断打断（上半部），可以并发的运行在多个CPU上。所以软中断必须设计成可重入的函数，因此也需要自旋锁来保护其数据结构。

2.工作队列中的函数处在进程上下文中，它可以睡眠，也能被阻塞，能够在不同的进程间切换，以完成不同的工作。

可延迟函数和工作队列都不能访问用户的进程空间，可延时函数在执行时不可能有任何正在运行的进程，工作队列的函数有内核进程执行，他不能访问用户空间地址。
### 硬件中断
硬件中断是一个异步信号, 表明需要注意, 或需要改变在执行一个同步事件.
硬件中断是由与系统相连的外设(比如网卡 硬盘 键盘等)自动产生的. 每个设备或设备集都有他自己的IRQ(中断请求), 基于IRQ, CPU可以将相应的请求分发到相应的硬件驱动上(注: 硬件驱动通常是内核中的一个子程序, 而不是一个独立的进程). 比如当网卡受到一个数据包的时候, 就会发出一个中断.
处理中断的驱动是需要运行在CPU上的, 因此, 当中断产生时, CPU会暂时停止当前程序的程序转而执行中断请求. 一个中断只能中断一颗CPU(也有一种特殊情况, 就是在大型主机上是有硬件通道的, 它可以在没有主CPU的支持下, 同时处理多个中断).
硬件中断可以直接中断CPU. 它会引起内核中相关代码被触发. 对于那些需要花费时间去处理的进程, 中断代码本身也可以被其他的硬件中断中断.
对于时钟中断, 内核调度代码会将当前正在运行的代码挂起, 从而让其他代码来运行. 它的存在时为了让调度代码(或称为调度器)可以调度多任务.
### 软中断
软中断的处理类似于硬中断. 但是软中断仅仅由当前运行的进程产生.
通常软中断是对一些I/O的请求.
软中断仅与内核相联系, 而内核主要负责对需要运行的任何其他进程进行调度.
软中断不会直接中断CPU, 也只有当前正在运行的代码(或进程)才会产生软中断. 软中断是一种需要内核为正在运行的进程去做一些事情(通常为I/O)的请求.
有一个特殊的软中断是Yield调用, 它的作用是请求内核调度器去查看是否有一些其他的进程可以运行.
硬件中断和软中断的区别
硬件中断是由外设引发的, 软中断是执行中断指令产生的.
硬件中断的中断号是由中断控制器提供的, 软中断的中断号由指令直接指出, 无需使用中断控制器.
硬件中断是可屏蔽的, 软中断不可屏蔽.
硬件中断处理程序要确保它能快速地完成任务, 这样程序执行时才不会等待较长时间, 称为上半部.
软中断处理硬中断未完成的工作, 是一种推后执行的机制, 属于下半部.

---

https://blog.csdn.net/jwy2014/article/details/89221142