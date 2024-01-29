---
title: "fork"
author: "-"
date: "2020-08-28 13:10:45"
url: ""
categories:
  - inbox
tags:
  - inbox
---
## "fork"


一个进程,包括代码、数据和分配给进程的资源。fork() 函数通过系统调用创建一个与原来进程几乎完全相同的进程,也就是两个进程可以做完全相同的事,但如果初始参数或者传入的变量不同,两个进程也可以做不同的事。
一个进程调用fork() 函数后,系统先给新的进程分配资源,例如存储数据和代码的空间。然后把原来的进程的所有值都复制到新的新进程中,只有少数值与原来的进程的值不同。相当于克隆了一个自己。

### 我们来看一个例子: 
```c
/*
 *  fork_test.c
 *  version 1
 *  Created on: 2010-5-29
 *      Author: wangth
 */
#include <unistd.h>
#include <stdio.h> 
int main () 
{ 
    pid_t fpid; //fpid表示fork函数返回的值
    int count=0;
    fpid=fork(); 
    if (fpid < 0) 
        printf("error in fork!"); 
    else if (fpid == 0) {
        printf("i am the child process, my process id is %d/n",getpid()); 
        printf("我是爹的儿子/n");//对某些人来说中文看着更直白。
        count++;
    }
    else {
        printf("i am the parent process, my process id is %d/n",getpid()); 
        printf("我是孩子他爹/n");
        count++;
    }
    printf("统计结果是: %d/n",count);
    return 0;
}

```

### 运行结果是: 
    i am the child process, my process id is 5574
    我是爹的儿子
    统计结果是: 1
    i am the parent process, my process id is 5573
    我是孩子他爹
    统计结果是: 1


在语句fpid=fork()之前,只有一个进程在执行这段代码,但在这条语句之后,就变成两个进程在执行了,这两个进程的几乎完全相同,将要执行的下一条语句都是if(fpid<0)……
    为什么两个进程的fpid不同呢,这与fork函数的特性有关。fork调用的一个奇妙之处就是它仅仅被调用一次,却能够返回两次,它可能有三种不同的返回值: 
    1) 在父进程中,fork返回新创建子进程的进程ID；
    2) 在子进程中,fork返回0；
    3) 如果出现错误,fork返回一个负值；
 

### fork系统调用
1. fork系统调用说明
fork系统调用用于从已存在进程中创建一个新进程,新进程称为子进程,而原进程称为父进程。fork调用一次,返回两次,这两个返回分别带回它们各自的返回值,其中在父进程中的返回值是子进程的进程号,而子进程中的返回值则返回 0。因此,可以通过返回值来判定该进程是父进程还是子进程。

使用fork函数得到的子进程是父进程的一个复制品,它从父进程处继承了整个进程的**地址空间**,包括进程上下文、进程堆栈、内存信息、打开的文件描述符、信号控制设定、进程优先级、进程组号、当前工作目录、根目录、资源限制、控制终端等,而子进程所独有的只有它的进程号、计时器等。因此可以看出,使用fork系统调用的代价是很大的,它复制了父进程中的数据段和堆栈段里的绝大部分内容,使得fork系统调用的执行速度并不很快。

fork的返回值这样设计是有原因的,fork在子进程中返回0,子进程仍可以调用getpid函数得到自己的进程ID,也可以调用getppid函数得到父进程的进程ID。在父进程中使用getpid函数可以得到自己的进程ID,然而要想得到子进程的进程ID,只有将fork的返回值记录下来,别无它法。

fork的另一个特性是所有由父进程打开的文件描述符都被复制到子进程中。父、子进程中相同编号的文件描述符在内核中指向同一个file结构体,也就是说,file结构体的引用计数要增加。

由于代码段 (加载到内存的执行码) 在内存中是只读的,所以父子进程可共用代码段,而数据段和堆栈段子进程则完全从父进程复制拷贝了一份。

 

 (2) 父进程进行fork系统调用时完成的操作

      假设id=fork(),父进程进行fork系统调用时,fork所做工作如下: 

①    为新进程分配task_struct任务结构体内存空间。

②    把父进程task_struct任务结构体复制到子进程task_struct任务结构体。

③    为新进程在其内存上建立内核堆栈。

④    对子进程task_struct任务结构体中部分变量进行初始化设置。

⑤    把父进程的有关信息复制给子进程,建立共享关系。

⑥    把子进程加入到可运行队列中。

⑦    结束fork()函数,返回子进程ID值给父进程中栈段变量id。

⑧    当子进程开始运行时,操作系统返回0给子进程中栈段变量id。




 (3) fork调用时所发生的事情

下面代码是fork函数调用模板,fork函数调用后常与if-else语句结合使用使父子进程执行不同的流程。假设下面代码执行时产生的是X进程,fork后产生子进程的是XX进程,XX进程的进程ID号为1000。

    int pid ;

pid = fork();

    if (pid < 0) {

        perror("fork failed");

        exit(1);

    }

    if (pid == 0) {

        message = "This is the child/n";   

调用fork前,内存中只有X进程,如图12-9所示,此时XX进程还没"出生"。

     

  图12-9 fork前的内存

调用fork后,内存中不仅有X进程 (父进程) ,还有XX进程 (子进程) 。fork的时候,系统几乎把父进程整个堆栈段 (除代码段,代码段父子进程是共享的) 复制给了子进程,复制完成后,X进程和XX进程是两个独立的进程,如下图12-10所示,只不过X进程栈中变量id值此时为1000,而XX进程栈中变量id值为0。fork调用完成后,X进程由系统态回到用户态。此后,X进程和XX进程各自都需要从自己代码段指针指向的代码点继续往下执行,父进程X往下执行时判断id大于0,所以执行大于0的程序段,而子进程XX往下执行时判断id等于0,所以执行等于0的程序段。

 

  图12-10 fork后的内存

 (4) fork 函数原型

所需头文件

#include <sys/types.h>   // 提供类型 pid_t 的定义

#include <unistd.h>

函数说明

建立一个新的进程

函数原型

pid_t fork(void)

函数返回值

0: 返回给子进程

子进程的ID(大于0的整数): 返回给父进程

-1: 出错,返回给父进程,错误原因存于errno中

错误代码

EAGAIN: 内存不足

ENOMEM: 内存不足,无法配置核心所需的数据结构空间

  

 (5) fork函数使用实例

fork.c源代码如下: 

#include <sys/types.h>

#include <sys/wait.h>

#include <unistd.h>

#include <stdio.h>

#include <stdlib.h>

int main(void)

{

    pid_t pid;

    char *message;

    int n;

    pid = fork();

    if (pid < 0) {

        perror("fork failed");

        exit(-1);

    }

    if (pid == 0) {

        message = "This is the child\n";

        n = 3;

    } else {

        wait(0) ; /*阻塞等待子进程返回*/

        message = "This is the parent\n";

        n = 1;

    }

    for(; n > 0; n--) {

        printf(message);

        sleep(1);

    }

    return 0;

}

编译 gcc fork.c –o fork。

执行./fork,执行结果如下: 

This is the child

This is the child

This is the child

This is the parent

读者可以把sleep(1)改成sleep(30),然后通过ps -ef|grep fork查看进程数。

 (6) fork后程序处理的两种情形

        一种为父进程希望复制自己,使父、子进程同时执行不同的代码段。这是网络并发服务端常见的模型,父进程等待客户端的服务请求,当这种请求到达时,父进程调用fork,让子进程处理此请求,父进程则继续等待下一个服务请求。

       另一种为fork后通过exec执行另一个程序,在终端上执行命令属于这种情况,Shell进程fork后立即调用exec去执行执行命令。

  (7) fork之后处理文件描述符有两种常见情况

父进程等待子进程完成。在这种情况下,父进程无需对其文件描述符做任何处理,当子进程终止后,它曾进行过读、写操作的任一共享描述符的文件位移量已做了相应更新。

父、子进程各自执行不同的程序段。在这种情况下,在fork之后,父、子进程各自关闭它们不需使用的文件描述符,并且不干扰对方使用的文件描述符。这种方式在并发网络服务器中经常使用到。

 
### 除了打开文件之外,很多父进程的其他性质也由子进程继承
- 实际用户ID、实际组ID、有效用户ID、有效组ID；
- 附加组ID；
- 进程组ID；
- 会话ID；
- 控制终端；
- 设置-用户-ID标志和设置-组-ID标志；
- 当前工作目录；
- 根目录；
- 文件权限屏蔽字；
- 信号屏蔽和排列；
- 打开的文件描述符；
- 环境变量；
- 连接的共享存储段；
- 数据段、代码段、堆段、.bss段(Block Started by Symbol segment, 通常是指用来存放程序中未初始化的全局变量的一块内存区域)
- 资源限制。

### 父、子进程之间有如下区别
- fork的返回值；
- 进程ID；
- 不同的父进程ID；
- 子进程的tms_utime、tms_stime、tms_cutime以及tms_ustime设置为0；
- 父进程设置的锁,子进程不继承；
- 未处理的闹钟信号子进程将清除；
- 子进程的未决告警被清除；
- 子进程的未决信号集设置为空集。

### fork与vfork的区别
使用fork调用会为子进程复制父进程所拥有的资源 (进程环境、栈堆等) ,而vfork设计时要求子进程立即调用exec,而不修改任何内存,vfork新建的子进程则是和父进程共享所有的资源,在子进程中对数据的修改也就是对父进程数据的修改,这一点一定要注意。

使用fork系统调用产生父子进程,在默认情况下无需人为干预,父子进程的执行顺序是由操作系统调度的,谁先执行并不确定。而对于vfork所生成的父子进程,父进程是在子进程调用了_exit或者exec后才会继续执行,不调用这两个函数父进程会等待 (父进程由于没有收到子进程表示已执行的相关信号所以进行等待) 。

vfork的出现是为了解决当初fork浪费用户空间内存的问题,因为在fork后,很有可能去执行exec函数重生,vfork设计思想就是取消fork造成堆栈的复制,使用vfork可以避免资源的浪费,但是也带了资源共享所产生的问题。

在Linux中,对fork进行了优化,调用时采用写时复制 (COW,copy on write) 的方式,在系统调用fork生成子进程的时候,不马上为子进程复制父进程的资源,而是在遇到"写入" (对资源进行修改) 操作时才复制资源。它使得一个普通的fork调用非常类似于vfork,但又避免了vfork的缺点,使得vfork变得没有必要。      

     

摘录自《深入浅出Linux工具与编程》

### fork源码
fork是复制进程

进程是一个正在运行的程序,是资源分配的最小单位,系统管理进程是依靠对进程控制块 (PCB) 的管理完成的,每个进程的产生分两步,一是: 分配PCB,二是准备进程实体,如分配内存空间等。

fork()创建进程,fork()调用一次,返回两次,子进程的返回值是0,父进程的返回值是子进程的新ID。文件共享在fork之前父进程打开的文件子进程才能使用,一个进程打开的文件描述符是在PCB中记录的,父进程调用fork()创建子进程的过程中,子进程的PCB是拷贝附近才能合格的PCB,父进程的所有打开的文件描述符都被复制到子进程中。

vfork()创建一个新进程,子进程去调用exec,并不将父进程的地址空间完全复制到子进程中去,因为子进程会立即调用exec(或者exit),于是就不会访问该地址空间并保证子进程先运行,直到子进程调用exec或者exit之后,父进程才会运行。


---

https://blog.csdn.net/jason314/article/details/5640969  
https://blog.csdn.net/guoping16/article/details/6580006  
版权声明: 本文为CSDN博主「guoping16」的原创文章,遵循CC 4.0 BY-SA版权协议,转载请附上原文出处链接及本声明。
原文链接: https://blog.csdn.net/guoping16/article/details/6580006
https://blog.csdn.net/post_joke/article/details/90341461  