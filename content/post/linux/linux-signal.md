+++
author = "w1100n"
date = "2021-04-30 07:20:01" 
title = "linux signal"

+++
# Linux信号(signal)机制

对于 Linux来说，实际信号是软中断，许多重要的程序都需要处理信号。信号，为 Linux 提供了一种处理异步事件的方法。比如，终端用户输入了 ctrl+c 来中断程序，会通过信号机制停止一个程序。

信号(signal)是一种软中断，信号机制是进程间通信的一种方式，采用异步通信方式

信号的名字和编号：
每个信号都有一个名字和编号，这些名字都以“SIG"开头，例如“SIGIO "、“SIGCHLD"等等。
信号定义在signal.h头文件中，信号名都定义为正整数。
具体的信号名称可以使用kill -l来查看信号的名字以及序号，信号是从1开始编号的，不存在0号信号。kill对于信号0又特殊的应用。

信号的处理：
信号的处理有三种方法，分别是：忽略、捕捉和默认动作

忽略信号，大多数信号可以使用这个方式来处理，但是有两种信号不能被忽略（分别是 SIGKILL和SIGSTOP）。因为他们向内核和超级用户提供了进程终止和停止的可靠方法，如果忽略了，那么这个进程就变成了没人能管理的的进程，显然是内核设计者不希望看到的场景
捕捉信号，需要告诉内核，用户希望如何处理某一种信号，说白了就是写一个信号处理函数，然后将这个函数告诉内核。当该信号产生时，由内核来调用用户自定义的函数，以此来实现某种信号的处理。
系统默认动作，对于每个信号来说，系统都对应由默认的处理动作，当发生了该信号，系统会自动执行。不过，对系统来说，大部分的处理方式都比较粗暴，就是直接杀死该进程。
具体的信号默认动作可以使用man 7 signal来查看系统的具体定义。在此，我就不详细展开了，需要查看的，可以自行查看。也可以参考 《UNIX 环境高级编程（第三部）》的 P251——P256中间对于每个信号有详细的说明。
 
一、信号类型
Linux系统共定义了64种信号，分为两大类：可靠信号与不可靠信号，前32种信号为不可靠信号，后32种为可靠信号。

1.1 概念
不可靠信号： 也称为非实时信号，不支持排队，信号可能会丢失, 比如发送多次相同的信号, 进程只能收到一次. 信号值取值区间为1~31；

可靠信号： 也称为实时信号，支持排队, 信号不会丢失, 发多少次, 就可以收到多少次. 信号值取值区间为32~64

1.2 信号表
在终端，可通过kill -l查看所有的signal信号

取值	名称	解释	默认动作
1	SIGHUP	挂起	 
2	SIGINT	中断, /* interrupt */ 程序终止(interrupt)信号, 在用户键入INTR字符(通常是Ctrl+C)时发出，用于通知前台进程组终止进程。	 
3	SIGQUIT	退出	 
4	SIGILL	非法指令	 
5	SIGTRAP	断点或陷阱指令	 
6	SIGABRT	abort发出的信号	 
7	SIGBUS	非法内存访问	 
8	SIGFPE	浮点异常	 
9	SIGKILL	kill信号	不能被忽略、处理和阻塞
10	SIGUSR1	用户信号1	 
11	SIGSEGV	无效内存访问	 
12	SIGUSR2	用户信号2	 
13	SIGPIPE	管道破损，没有读端的管道写数据	 
14	SIGALRM	alarm发出的信号	 
15	SIGTERM	终止信号	 
16	SIGSTKFLT	栈溢出	 
17	SIGCHLD	子进程退出	默认忽略
18	SIGCONT	进程继续	 
19	SIGSTOP	进程停止	不能被忽略、处理和阻塞
20	SIGTSTP	进程停止	 
21	SIGTTIN	进程停止，后台进程从终端读数据时	 
22	SIGTTOU	进程停止，后台进程想终端写数据时	 
23	SIGURG	I/O有紧急数据到达当前进程	默认忽略
24	SIGXCPU	进程的CPU时间片到期	 
25	SIGXFSZ	文件大小的超出上限	 
26	SIGVTALRM	虚拟时钟超时	 
27	SIGPROF	profile时钟超时	 
28	SIGWINCH	窗口大小改变	默认忽略
29	SIGIO	I/O相关	 
30	SIGPWR	关机	默认忽略
31	SIGSYS	系统调用异常	 
对于signal信号，绝大部分的默认处理都是终止进程或停止进程，或dump内核映像转储。 上述的31的信号为非实时信号，其他的信号32-64 都是实时信号。

二、信号产生
信号来源分为硬件类和软件类：

2.1 硬件方式
用户输入：比如在终端上按下组合键ctrl+C，产生SIGINT信号；
硬件异常：CPU检测到内存非法访问等异常，通知内核生成相应信号，并发送给发生事件的进程；
2.2 软件方式
通过系统调用，发送signal信号：kill()，raise()，sigqueue()，alarm()，setitimer()，abort()

kernel,使用 kill_proc_info(）等
native,使用 kill() 或者raise()等
java,使用 Procees.sendSignal()等
三、信号注册和注销
3.1 注册
在进程task_struct结构体中有一个未决信号的成员变量 struct sigpending pending。每个信号在进程中注册都会把信号值加入到进程的未决信号集。

非实时信号发送给进程时，如果该信息已经在进程中注册过，不会再次注册，故信号会丢失；
实时信号发送给进程时，不管该信号是否在进程中注册过，都会再次注册。故信号不会丢失；
3.2 注销
非实时信号：不可重复注册，最多只有一个sigqueue结构；当该结构被释放后，把该信号从进程未决信号集中删除，则信号注销完毕；
实时信号：可重复注册，可能存在多个sigqueue结构；当该信号的所有sigqueue处理完毕后，把该信号从进程未决信号集中删除，则信号注销完毕；
四、信号处理
内核处理进程收到的signal是在当前进程的上下文，故进程必须是Running状态。当进程唤醒或者调度后获取CPU，则会从内核态转到用户态时检测是否有signal等待处理，处理完，进程会把相应的未决信号从链表中去掉。

4.1 处理时机
signal信号处理时机： 内核态 -> signal信号处理 -> 用户态：

在内核态，signal信号不起作用；
在用户态，signal所有未被屏蔽的信号都处理完毕；
当屏蔽信号，取消屏蔽时，会在下一次内核转用户态的过程中执行；
4.2 处理方式
进程对信号的处理方式： 有3种

默认 接收到信号后按默认的行为处理该信号。 这是多数应用采取的处理方式。
自定义 用自定义的信号处理函数来执行特定的动作
忽略 接收到信号后不做任何反应。
4.3 信号安装
进程处理某个信号前，需要先在进程中安装此信号。安装过程主要是建立信号值和进程对相应信息值的动作。

信号安装函数

signal()：不支持信号传递信息，主要用于非实时信号安装；
sigaction():支持信号传递信息，可用于所有信号安装；
其中 sigaction结构体

sa_handler:信号处理函数
sa_mask：指定信号处理程序执行过程中需要阻塞的信号；
sa_flags：标示位
SA_RESTART：使被信号打断的syscall重新发起。
SA_NOCLDSTOP：使父进程在它的子进程暂停或继续运行时不会收到 SIGCHLD 信号。
SA_NOCLDWAIT：使父进程在它的子进程退出时不会收到SIGCHLD信号，这时子进程如果退出也不会成为僵 尸进程。
SA_NODEFER：使对信号的屏蔽无效，即在信号处理函数执行期间仍能发出这个信号。
SA_RESETHAND：信号处理之后重新设置为默认的处理方式。
SA_SIGINFO：使用sa_sigaction成员而不是sa_handler作为信号处理函数。
函数原型：

int sigaction(int signum, const struct sigaction *act, struct sigaction *oldact);

signum：要操作的signal信号。
act：设置对signal信号的新处理方式。
oldact：原来对信号的处理方式。
返回值：0 表示成功，-1 表示有错误发生。
4.4 信号发送
kill()：用于向进程或进程组发送信号；
sigqueue()：只能向一个进程发送信号，不能像进程组发送信号；主要针对实时信号提出，与sigaction()组合使用，当然也支持非实时信号的发送；
alarm()：用于调用进程指定时间后发出SIGALARM信号；
setitimer()：设置定时器，计时达到后给进程发送SIGALRM信号，功能比alarm更强大；
abort()：向进程发送SIGABORT信号，默认进程会异常退出。
raise()：用于向进程自身发送信号；
4.5 信号相关函数
信号集操作函数

sigemptyset(sigset_t *set)：信号集全部清0；
sigfillset(sigset_t *set)： 信号集全部置1，则信号集包含linux支持的64种信号；
sigaddset(sigset_t *set, int signum)：向信号集中加入signum信号；
sigdelset(sigset_t *set, int signum)：向信号集中删除signum信号；
sigismember(const sigset_t *set, int signum)：判定信号signum是否存在信号集中。
信号阻塞函数

sigprocmask(int how, const sigset_t *set, sigset_t *oldset))； 不同how参数，实现不同功能
SIG_BLOCK：将set指向信号集中的信号，添加到进程阻塞信号集；
SIG_UNBLOCK：将set指向信号集中的信号，从进程阻塞信号集删除；
SIG_SETMASK：将set指向信号集中的信号，设置成进程阻塞信号集；
sigpending(sigset_t *set))：获取已发送到进程，却被阻塞的所有信号；
sigsuspend(const sigset_t *mask))：用mask代替进程的原有掩码，并暂停进程执行，直到收到信号再恢复原有掩码并继续执行进程。


SIGHUP /* hangup */
       ~~~~~~      SIGHUP，hong up ，挂断。本信号在用户终端连接(正常或非正常)结束时发出, 通常是在终端的控制进程结束时, 通知同一session内的各个作业, 这时它们与控制终端不再关联。
       ~~~~~~      登录Linux时，系统会分配给登录用户一个终端(Session)。在这个终端运行的所有程序，包括前台进程组和 后台进程组，一般都属于这个 Session。当用户退出Linux登录时，前台进程组和后台有对终端输出的进程将会收到SIGHUP信号。这个信号的默认操作为终止进程，因此前台进 程组和后台有终端输出的进程就会中止。不过可以捕获这个信号，比如wget能捕获SIGHUP信号，并忽略它，这样就算退出了Linux登录，wget也 能继续下载。
       ~~~~~~      此外，对于与终端脱离关系的守护进程，这个信号用于通知它重新读取配置文件。
 

SIGQUIT /* quit */
       ~~~~~~      和SIGINT类似, 但由QUIT字符(通常是Ctrl+)来控制. 进程在因收到SIGQUIT退出时会产生core文件, 在这个意义上类似于一个程序错误信号。

SIGILL /* illegal instr. (not reset when caught) */
       ~~~~~~      SIGILL，illeage，非法的。执行了非法指令， 通常是因为可执行文件本身出现错误, 或者试图执行数据段. 堆栈溢出也有可能产生这个信号。

SIGTRAP
       ~~~~~~      由断点指令或其它陷阱（trap）指令产生. 由debugger使用。

SIGABRT
       ~~~~~~      调用abort函数生成的信号。

SIGBUS
       ~~~~~~      非法地址, 包括内存地址对齐(alignment)出错。比如访问一个四个字长的整数, 但其地址不是4的倍数。它与SIGSEGV的区别在于后者是由于对合法存储地址的非法访问触发的(如访问不属于自己存储空间或只读存储空间)。

SIGFPE
       ~~~~~~      FPE是floating-point exception（浮点异常）的首字母缩略字。在发生致命的算术运算错误时发出. 不仅包括浮点运算错误, 还包括溢出及除数为0等其它所有的算术的错误。SIGFPE的符号常量在头文件signal.h中定义。
在这里插入图片描述

SIGKILL
       ~~~~~~      用来立即结束程序的运行. 本信号不能被阻塞、处理和忽略。如果管理员发现某个进程终止不了，可尝试发送这个信号，终极大招。

SIGUSR1
       ~~~~~~      留给用户使用

SIGSEGV
       ~~~~~~      试图访问未分配给自己的内存, 或试图往没有写权限的内存地址写数据.

SIGUSR2
       ~~~~~~      留给用户使用

SIGPIPE
       ~~~~~~      管道破裂。这个信号通常在进程间通信产生，比如采用FIFO(管道)通信的两个进程，读管道没打开或者意外终止就往管道写，写进程会收到SIGPIPE信号。此外用Socket通信的两个进程，写进程在写Socket的时候，读进程已经终止。

SIGALRM
       ~~~~~~      时钟定时信号, 计算的是实际的时间或时钟时间. alarm函数使用该信号.

SIGTERM
       ~~~~~~      程序结束(terminate)信号, 与SIGKILL不同的是该信号可以被阻塞和处理。通常用来要求程序自己正常退出，shell命令kill缺省产生这个信号。如果进程终止不了，我们才会尝试SIGKILL。

SIGCHLD
       ~~~~~~      子进程（child）结束时, 父进程会收到这个信号。如果父进程没有处理这个信号，也没有等待(wait)子进程，子进程虽然终止，但是还会在内核进程表中占有表项，这 时的子进程称为僵尸进程。这种情 况我们应该避免(父进程或者忽略SIGCHILD信号，或者捕捉它，或者wait它派生的子进程，或者父进程先终止，这时子进程的终止自动由init进程 来接管)。

SIGCONT
       ~~~~~~      让一个停止(stopped)的进程继续执行. 本信号不能被阻塞. 可以用一个handler来让程序在由stopped状态变为继续执行时完成特定的工作. 例如, 重新显示提示符

SIGSTOP
       ~~~~~~      暂停(stopped)进程的执行. 注意它和terminate以及interrupt的区别:该进程还未结束, 只是暂停执行. 本信号不能被阻塞, 处理或忽略.

SIGTSTP
       ~~~~~~      停止进程的运行, 但该信号可以被处理和忽略. 用户键入SUSP字符时(通常是Ctrl+Z)发出这个信号

SIGTTIN
       ~~~~~~      当后台作业要从用户终端读数据时, 该作业中的所有进程会收到SIGTTIN信号. 缺省时这些进程会停止执行.
       ~~~~~~      Unix环境下，当一个进程以后台形式启动，但尝试去读写控制台终端时，将会触发SIGTTIN（读）和SIGTTOU（写）信号量，接着，进程将会暂停（linux默认情况下），read/write将会返回错误。这个时候，shell将会发送通知给用户，提醒用户切换此进程为前台进程，以便继续执行。由后台切换至前台的方式是fg命令，前台转为后台则为CTRL+Z快捷键。
  那么问题来了，如何才能在不把进程切换至前台的情况下，读写控制器不会被暂停？答案：只要忽略SIGTTIN和SIGTTOU信号量即可：signal(SIGTTOU, SIG_IGN)。
  stty stop/-stop命令是用于设置收到SIGTTOU信号量后是否执行暂停，因为有些系统的默认行为不一致，比如mac是默认忽略，而linux是默认启用。stty -a可以查看当前tty的配置参数。
在这里插入图片描述

SIGTTOU
  类似于SIGTTIN, 但在写终端(或修改终端模式)时收到。具体见上面SIGTTIN

SIGURG
  SIGURG, urgent, 紧急的。有"紧急"数据或out-of-band数据到达socket时产生.

SIGXCPU
  超过CPU时间资源限制. 这个限制可以由getrlimit/setrlimit来读取/改变。

SIGXFSZ
  当进程企图扩大文件以至于超过文件大小资源限制。

SIGVTALRM
  虚拟时钟信号. 类似于SIGALRM, 但是计算的是该进程占用的CPU时间.

SIGPROF
  类似于SIGALRM/SIGVTALRM, 但包括该进程用的CPU时间以及系统调用的时间.

SIGWINCH
  Windows Change, 窗口大小改变时发出.

SIGIO
  文件描述符准备就绪, 可以开始进行输入/输出操作.

SIGPWR
  Power failure

SIGSYS
  非法的系统调用。
  
(1)在以上列出的信号中，程序不可捕获、阻塞或忽略的信号有：SIGKILL,SIGSTOP
不能恢复至默认动作的信号有：
SIGILL,SIGTRAP
默认会导致进程流产的信号有：SIGABRT,SIGBUS,SIGFPE,SIGILL,SIGIOT,SIGQUIT,SIGSEGV,SIGTRAP,SIGXCPU,SIGXFSZ
默认会导致进程退出的信号有：SIGALRM,SIGHUP,SIGINT,SIGKILL,SIGPIPE,SIGPOLL,SIGPROF,SIGSYS,SIGTERM,SIGUSR1,SIGUSR2,SIGVTALRM
默认会导致进程停止的信号有：SIGSTOP,SIGTSTP,SIGTTIN,SIGTTOU
默认进程忽略的信号有：SIGCHLD,SIGPWR,SIGURG,SIGWINCH
此外，SIGIO在SVR4是退出，在4.3BSD中是忽略；SIGCONT在进程挂起时是继续，否则是忽略，不能被阻塞



---

http://gityuan.com/2015/12/20/signal/

作者：故事狗
链接：https://www.jianshu.com/p/f445bfeea40a
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
