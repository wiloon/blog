+++
author = "w1100n"
date = "2021-05-06 17:29:10" 
title = "fork vfork clone"

+++

Linux通过clone系统调用实现fork.调用通过一系列的参数标志来指明父、子进程需要共享的资源。fork、vfork、和__clone的库函数都根据各自需要的参数标志去调用clone，然后由clone()去调用do_fork()。
arch(X86)架构的是：fork、vfork、和__clone的库函数最终调用的都是clone系统调用。

至于其它的架构的，可能是通过fork和vfork系统调用。这和本身的实现有关。当然在现在的大多数Linux内核中，就算调用的是fork,在底层基本上传递给do_fork的参数都带有能实现写时复制的一些标志。

fork和 pthread_create,然后利用strace跟踪两者的调用过程， 都是调用的clone。

---

在Linux中主要提供了fork、vfork、clone三个进程创建方法。 
在linux源码中这三个调用的执行过程是执行fork(),vfork(),clone()时，通过一个系统调用表映射到sys_fork(),sys_vfork(),sys_clone(),再在这三个函数中去调用do_fork()去做具体的创建进程工作。 

fork 
    fork创建一个进程时，子进程只是完全复制父进程的资源，复制出来的子进程有自己的task_struct结构和pid,但却复制父进程其它所有的资源。例如，要是父进程打开了五个文件，那么子进程也有五个打开的文件，而且这些文件的当前读写指针也停在相同的地方。所以，这一步所做的是复制。这样得到的子进程独立于父进程， 具有良好的并发性，但是二者之间的通讯需要通过专门的通讯机制，如：pipe，共享内存等机制， 另外通过fork创建子进程，需要将上面描述的每种资源都复制一个副本。这样看来，fork是一个开销十分大的系统调用，这些开销并不是所有的情况下都是必须的，比如某进程fork出一个子进程后，其子进程仅仅是为了调用exec执行另一个可执行文件，那么在fork过程中对于虚存空间的复制将是一个多余的过程。但由于现在Linux中是采取了copy-on-write(COW写时复制)技术，为了降低开销，fork最初并不会真的产生两个不同的拷贝，因为在那个时候，大量的数据其实完全是一样的。写时复制是在推迟真正的数据拷贝。若后来确实发生了写入，那意味着parent和child的数据不一致了，于是产生复制动作，每个进程拿到属于自己的那一份，这样就可以降低系统调用的开销。所以有了写时复制后呢，vfork其实现意义就不大了。 

　　fork()调用执行一次返回两个值，对于父进程，fork函数返回子程序的进程号，而对于子程序，fork函数则返回零，这就是一个函数返回两次的本质。 

　　在fork之后，子进程和父进程都会继续执行fork调用之后的指令。子进程是父进程的副本。它将获得父进程的数据空间，堆和栈的副本，这些都是副本，父子进程并不共享这部分的内存。也就是说，子进程对父进程中的同名变量进行修改并不会影响其在父进程中的值。但是父子进程又共享一些东西，简单说来就是程序的正文段。正文段存放着由cpu执行的机器指令，通常是read-only的。下面是一个验证的例子：



```
//例１：fork.c   
  
　　#include<stdio.h>   
  
　　#include<sys/types.h>   
  
　　#include<unistd.h>   
  
　　#include<errno.h>   
  
　　int main()   
  
　　{   
  
　　int a = 5;   
  
　　int b = 2;   
  
　　pid_t pid;   
  
　　pid = fork();   
  
　　if(pid == 0) {   
  
　　a = a-4;   
  
　　printf("I'm a child process with PID [%d],the value of a: %d,the value of b:%d.\n",pid,a,b);   
  
　　}else if(pid < 0) {   
  
　　perror("fork");   
  
　　}else {   
  
　　printf("I'm a parent process, with PID [%d], the value of a: %d, the value of b:%d.\n", pid, a, b);   
  
　　}   
  
　　return 0;   
  
　　}   
  
　　#gcc –o fork fork.c   
  
　　#./fork   
  
　　//运行结果：   
  
　　I’m a child process with PID[0],the value of a:1,the value of b:2.   
  
　　I’m a parent process with PID[19824],the value of a:5,the value of b:2.   
//例１：fork.c 
 
　　#include<stdio.h> 
 
　　#include<sys/types.h> 
 
　　#include<unistd.h> 
 
　　#include<errno.h> 
 
　　int main() 
 
　　{ 
 
　　int a = 5; 
 
　　int b = 2; 
 
　　pid_t pid; 
 
　　pid = fork(); 
 
　　if(pid == 0) { 
 
　　a = a-4; 
 
　　printf("I'm a child process with PID [%d],the value of a: %d,the value of b:%d.\n",pid,a,b); 
 
　　}else if(pid < 0) { 
 
　　perror("fork"); 
 
　　}else { 
 
　　printf("I'm a parent process, with PID [%d], the value of a: %d, the value of b:%d.\n", pid, a, b); 
 
　　} 
 
　　return 0; 
 
　　} 
 
　　#gcc –o fork fork.c 
 
　　#./fork 
 
　　//运行结果： 
 
　　I’m a child process with PID[0],the value of a:1,the value of b:2. 
 
　　I’m a parent process with PID[19824],the value of a:5,the value of b:2. 

可见，子进程中将变量a的值改为１,而父进程中则保持不变。 

　　vfork 

　　vfork系统调用不同于fork，用vfork创建的子进程与父进程共享地址空间，也就是说子进程完全运行在父进程的地址空间上，如果这时子进程修改了某个变量，这将影响到父进程。 

　　因此，上面的例子如果改用vfork()的话，那么两次打印a,b的值是相同的，所在地址也是相同的。 

　　但此处有一点要注意的是用vfork()创建的子进程必须显示调用exit()来结束，否则子进程将不能结束，而fork()则不存在这个情况。 

　　Vfork也是在父进程中返回子进程的进程号，在子进程中返回0。 

　　用 vfork创建子进程后，父进程会被阻塞直到子进程调用exec(exec，将一个新的可执行文件载入到地址空间并执行之。)或exit。vfork的好处是在子进程被创建后往往仅仅是为了调用exec执行另一个程序，因为它就不会对父进程的地址空间有任何引用，所以对地址空间的复制是多余的 ，因此通过vfork共享内存可以减少不必要的开销。下面这个例子可以验证子进程调用exec时父进程是否真的已经结束阻塞：
[cpp] view plain copy
例2：execl.c   
  
　　#include<stdlib.h>   
  
　　#include<sys/types.h>   
  
　　#include<sys/wait.h>   
  
　　#include<unistd.h>   
  
　　#include<stdio.h>   
  
　　#include<errno.h>   
  
　　#include<string.h>   
  
　　int main()   
  
　　{   
　　int a = 1;   
　　int b = 2;   
　　pid_t pid;   
　　int status;   
      
    pid = vfork();   
    if(pid == -1) {   
       perror("Fork failed to creat a process");   
       exit(1);   
       }  
    else if(pid == 0)   
       {   
           // sleep(3);   
            if(execl("/bin/example","example",NULL)<0)   
            {   
                 perror("Exec failed");   
                 exit(1);   
            }   
            exit(0);   
        // }else // if(pid != wait(&status)) {   
              // perror("A Signal occured before the child exited"); }  
     else   
      printf("parent process,the value of a :%d, b:%d, addr of a: %p,b: %p\n",a,b,&a,&b); exit(0); }   
  
Example.c   
#include<stdio.h>   
int main()   
{   
   int a = 1;  
   int b = 2;  
   sleep(3);  
   printf("Child process,the value of a is %d,b is %d,the address a %p,b %p\n",a,b,&a,&b);   
   return 0;   
}   
#gcc –o execl execl.c #./ execl 运行结果：  
Child process ,The value of a is 1,b is 2,the address a 0xbfb73d90,b 0xbfb73d8c   
例2：execl.c 
 
　　#include<stdlib.h> 
 
　　#include<sys/types.h> 
 
　　#include<sys/wait.h> 
 
　　#include<unistd.h> 
 
　　#include<stdio.h> 
 
　　#include<errno.h> 
 
　　#include<string.h> 
 
　　int main() 
 
　　{ 
　　int a = 1; 
　　int b = 2; 
　　pid_t pid; 
　　int status; 
    
    pid = vfork(); 
    if(pid == -1) { 
       perror("Fork failed to creat a process"); 
       exit(1); 
       }
    else if(pid == 0) 
       { 
           // sleep(3); 
            if(execl("/bin/example","example",NULL)<0) 
            { 
                 perror("Exec failed"); 
                 exit(1); 
            } 
            exit(0); 
        // }else // if(pid != wait(&status)) { 
              // perror("A Signal occured before the child exited"); }
     else 
      printf("parent process,the value of a :%d, b:%d, addr of a: %p,b: %p\n",a,b,&a,&b); exit(0); } 
 
Example.c 
#include<stdio.h> 
int main() 
{ 
   int a = 1;
   int b = 2;
   sleep(3);
   printf("Child process,the value of a is %d,b is %d,the address a %p,b %p\n",a,b,&a,&b); 
   return 0; 
} 
#gcc –o execl execl.c #./ execl 运行结果：
Child process ,The value of a is 1,b is 2,the address a 0xbfb73d90,b 0xbfb73d8c 

如果将注释掉的三行加入程序的话，由于父进程wait()而阻塞，因此即使此时子进程阻塞，父进程也得不到运行，因此运行结果如下： 

　　The value of a is 1,b is 2,the address a 0xbfb73d90,b 0xbfb73d8c 

　　Parent process,the value of a:1,b:2,addr ofa:0xbfaa710c, b:0xbf aa7108 

　　另外还应注意的是在它调用exec后父进程才可能调度运行，因此sleep(3)函数必须放在example程序中才能生效。 

　　clone 

　　系统调用fork()和vfork()是无参数的，而clone()则带有参数。fork()是全部复制，vfork()是共享内存，而clone() 是则可以将父进程资源有选择地复制给子进程，而没有复制的数据结构则通过指针的复制让子进程共享，具体要复制哪些资源给子进程，由参数列表中的 clone_flags来决定。另外，clone()返回的是子进程的pid。下面来看一个例子：
[cpp] view plain copy
例3：clone.c   
  
　　#include <stdio.h>   
  
　　#include <stdlib.h>   
  
　　#include <sched.h>   
  
　　#include <unistd.h>   
  
　　#include <fcntl.h>   
  
　　#include <sys/types.h>   
  
　　#include <sys/stat.h>   
  
　　int variable,fd;   
  
　　int do_something() {   
  
　　variable = 42;   
  
　　printf("in child process\n");   
  
　　close(fd);   
  
　　// _exit(0);   
  
　　return 0;   
  
　　}   
  
　　int main(int argc, char *argv[]) {   
  
　　void *child_stack;   
  
　　char tempch;   
  
　　variable = 9;   
  
　　fd = open("/test.txt",O_RDONLY);   
  
　　child_stack = (void *)malloc(16384);   
  
　　printf("The variable was %d\n",variable);   
  
　　clone(do_something, child_stack+10000, CLONE_VM |CLONE_FILES,NULL);   
  
　　sleep(3); /* 延时以便子进程完成关闭文件操作、修改变量 */   
  
　　printf("The variable is now %d\n",variable);   
  
　　if(read(fd,&tempch,1) < 1) {   
  
　　perror("File Read Error");   
  
　　exit(1);   
  
　　}   
  
　　printf("We could read from the file\n");   
  
　　return 0;   
  
　　}   
  
　　#gcc –o clone clone.c   
  
　　#./clone   
  
　　运行结果：   
  
　　the value was 9   
  
　　in child process   
  
　　The variable is now 42   
  
　　File Read Error   
例3：clone.c 
 
　　#include <stdio.h> 
 
　　#include <stdlib.h> 
 
　　#include <sched.h> 
 
　　#include <unistd.h> 
 
　　#include <fcntl.h> 
 
　　#include <sys/types.h> 
 
　　#include <sys/stat.h> 
 
　　int variable,fd; 
 
　　int do_something() { 
 
　　variable = 42; 
 
　　printf("in child process\n"); 
 
　　close(fd); 
 
　　// _exit(0); 
 
　　return 0; 
 
　　} 
 
　　int main(int argc, char *argv[]) { 
 
　　void *child_stack; 
 
　　char tempch; 
 
　　variable = 9; 
 
　　fd = open("/test.txt",O_RDONLY); 
 
　　child_stack = (void *)malloc(16384); 
 
　　printf("The variable was %d\n",variable); 
 
　　clone(do_something, child_stack+10000, CLONE_VM |CLONE_FILES,NULL); 
 
　　sleep(3); /* 延时以便子进程完成关闭文件操作、修改变量 */ 
 
　　printf("The variable is now %d\n",variable); 
 
　　if(read(fd,&tempch,1) < 1) { 
 
　　perror("File Read Error"); 
 
　　exit(1); 
 
　　} 
 
　　printf("We could read from the file\n"); 
 
　　return 0; 
 
　　} 
 
　　#gcc –o clone clone.c 
 
　　#./clone 
 
　　运行结果： 
 
　　the value was 9 
 
　　in child process 
 
　　The variable is now 42 
 
　　File Read Error 

从程序的输出结果可以看出： 

　　子进程将文件关闭并将变量修改（调用clone时用到的CLONE_VM、CLONE_FILES标志将使得变量和文件描述符表被共享），父进程随即就感觉到了，这就是clone的特点。由于此处没有设置标志CLONE_VFORK，因此子进程在运行时父进程也不会阻塞，两者同时运行。 

　　总结 

　　一、fork 

　　1. 调用方法 

　　#include <sys/types.h> 
   #include <unistd.h> 
   pid_t fork(void); 
   正确返回：在父进程中返回子进程的进程号，在子进程中返回0 
　　错误返回：-1 

　　2. fork函数调用的用途 

　　一个进程希望复制自身，从而父子进程能同时执行不同段的代码。 

　　二、vfork 

　　1. 调用方法 

　　与fork函数完全相同 

　　#include <sys/types.h> 

　　#include <unistd.h> 

　　pid_t vfork(void); 

　　正确返回：在父进程中返回子进程的进程号，在子进程中返回0 

　　错误返回：-1 

　　2. vfork函数调用的用途 

　　用vfork创建的进程主要目的是用exec函数执行另外的程序。 

　　三、clone 

　　1.调用方法 

　　#include <sched.h> 

　　int clone(int (*fn)(void *), void *child_stack, int flags, void *arg); 

　　正确返回：返回所创建进程的PID，函数中的flags标志用于设置创建子进程时的相关选项，具体含义参看P25 

　　错误返回：-１ 

　　2.clone()函数调用的用途 

　　用于有选择地设置父子进程之间需共享的资源 

### fork，vfork，clone的区别 

　　1. fork出来的子进程是父进程的一个拷贝，即，子进程从父进程得到了数据段和堆栈段的拷贝，这些需要分配新的内存；而对于只读的代码段，通常使用共享内存的方式访问；而vfork则是子进程与父进程共享内存空间, 子进程对虚拟地址空间任何数据的修改同样为父进程所见；clone则由用户通过参clone_flags 的设置来决定哪些资源共享，哪些资源拷贝。 

　　2. fork不对父子进程的执行次序进行任何限制，fork返回后，子进程和父进程都从调用fork函数的下一条语句开始行，但父子进程运行顺序是不定的，它取决于内核的调度算法；而在vfork调用中，子进程先运行，父进程挂起，直到子进程调用了exec或exit之后，父子进程的执行次序才不再有限制；clone中由标志CLONE_VFORK来决定子进程在执行时父进程是阻塞还是运行，若没有设置该标志，则父子进程同时运行，设置了该标志，则父进程挂起，直到子进程结束为止。


---

https://blog.csdn.net/wujiafei_njgcxy/article/details/77116175

https://zhuanlan.zhihu.com/p/59065065

