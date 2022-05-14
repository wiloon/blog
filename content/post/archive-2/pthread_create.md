---
title: pthread
author: "-"
date: 2017-03-26T09:13:38+00:00
url: /?p=9971

categories:
  - inbox
tags:
  - reprint
---
## pthread
### code
```c
    #include <pthread.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <unistd.h>

    void* xc(void* arg){
              char* c=(char*)arg;
              printf("参数%s \n",c);
              int i=0;
            for (;i<10;i++){
                    printf("循环%d\n",i);
                      if(i==5){
                          pthread_exit(1090000000);
                  }
          }
                return 100000222;
    }

    void main(){
            
            pthread_t tid;
            pthread_create(&tid,NULL,xc,"线程！！！！");

            void *status;
            pthread_join(tid,&status);
            printf("返回%d\n",(int)status);
    }
```
### pthread_create
pthread.h是UNIX环境创建线程函数头文件
```c
#include<pthread.h>
  
int pthread_create(pthread_t *restrict tidp,const pthread_attr_t  *restrict_attr,void  * ( *start_rtn)(void *),void  *restrict arg);
  
extern int pthread_create (pthread_t *__restrict __newthread,
                        const pthread_attr_t *__restrict __attr,
                        void *(*__start_routine) (void *),
                        void *__restrict __arg) __THROWNL __nonnull ((1, 3));
```

若成功则返回0,否则返回出错编号
  
返回成功时,由 __newthread 指向的内存单元被设置为新创建线程的线程ID。   
__attr 参数用于制定各种不同的线程属性。新创建的线程从start_rtn函数的地址开始运行,该函数只有一个万能指针参数arg,如果需要向start_rtn函数传递的参数不止一个,那么需要把这些参数放到一个结构中,然后把这个结构的地址作为arg的参数传入。
  
linux下用C开发多线程程序,Linux系统下的多线程遵循POSIX线程接口,称为pthread。
  
由 restrict 修饰的指针是最初唯一对指针所指向的对象进行存取的方法,仅当第二个指针基于第一个时,才能对对象进行存取。对对象的存取都限定于基于由 restrict 修饰的指针表达式中。 由 restrict 修饰的指针主要用于函数形参,或指向由 malloc() 分配的内存空间。restrict 数据类型不改变程序的语义。 编译器能通过作出 restrict 修饰的指针是存取对象的唯一方法的假设,更好地优化某些类型的例程。参数
  
第一个参数为指向线程标识符的指针。
  
第二个参数用来设置线程属性。
  
第三个参数是线程运行函数的起始地址。
  
最后一个参数是运行函数的参数。
  
另外,在编译时注意加上-lpthread参数,以调用静态链接库。因为pthread并非Linux系统的默认库示例
  
打印线程 IDs
  
#include <pthread.h>
  
#include <stdlib.h>
  
#include <stdio.h>
  
#include <unistd.h>
  
#include <string.h>
  
pthread_t ntid;
  
void printids(const char *s)
  
{
  
pid_t pid;
  
pthread_t tid;
  
pid = getpid();
  
tid = pthread_self();
  
printf("%s pid %u tid %u (0x%x)\n", s,
  
(unsigned int)pid, (unsigned int)tid, (unsigned int)tid);
  
} void \*thr_fn(void \*arg)
  
{
  
printids("new thread: ");
  
return((void *)0);
  
}
  
int main(void)
  
{
  
int err;
  
err = pthread_create(&ntid, NULL, thr_fn, NULL);
  
if (err != 0)
  
printf("can't create thread: %s\n", strerror(err));
  
printids("main thread:");
  
sleep(1);
  
exit(0);
  
}
  
$ gcc main.c -lpthread
  
$ ./a.out

向线程函数传递参数详解: 

向线程函数传递参数分为两种: 

 (1) 线程函数只有一个参数的情况: 直接定义一个变量通过应用传给线程函数。

例子: 

#include <iostream>
  
#include <pthread.h>
  
using namespace std;
  
pthread_t thread;
  
void fn(void *arg)
  
{
  
int i = \*(int \*)arg;
  
cout<<"i = "<<i<<endl;
  
return ((void *)0);
  
}
  
int main()
  
{
  
int err1;
  
int i=10;
  
err1 = pthread_create(&thread, NULL, fn, &i);
  
pthread_join(thread, NULL);
  
}
  
2. 线程函数有多个参数的情况: 这种情况就必须申明一个结构体来包含所有的参数,然后在传入线程函数,具体如下: 
  
例子: 

首先定义一个结构体: 

struct  parameter

{

int size,

int count;

。。。。。

。。。
  
};

然后在main函数将这个结构体指针,作为void *形参的实际参数传递

struct parameter arg;


通过如下的方式来调用函数: 
  
pthread_create(&ntid, NULL, fn,& (arg));
  
函数中需要定义一个parameter类型的结构指针来引用这个参数
  
void fn(void *arg)
  
{
  
int i = \*(int \*)arg;
  
cout<<"i = "<<i<<endl;
  
return ((void *)0);
  
}


void thr_fn(void *arg)
  
{
  
struct parameter *pstru;
  
pstru = ( struct parameter *) arg;
  
然后在这个函数中就可以使用指针来使用相应的变量的值了。
  
}

### pthread_join
pthread_join函数介绍: 
函数pthread_join用来等待一个线程的结束,线程间同步的操作。头文件 :  #include <pthread.h>
函数定义:  int pthread_join(pthread_t thread, void **retval);
描述 : pthread_join()函数,以阻塞的方式等待thread指定的线程结束。当函数返回时,被等待线程的资源被收回。如果线程已经结束,那么该函数会立即返回。并且thread指定的线程必须是joinable的。
参数 : thread: 线程标识符,即线程ID,标识唯一线程。retval: 用户定义的指针,用来存储被等待线程的返回值。
返回值 :  0代表成功。 失败,返回的则是错误号。





---

http://blog.csdn.net/liangxanhai/article/details/7767430  
https://blog.csdn.net/qq_37858386/article/details/78185064
https://www.jianshu.com/p/88fdd500cf44

