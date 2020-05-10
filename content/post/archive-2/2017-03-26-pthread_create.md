---
title: pthread_create
author: wiloon
type: post
date: 2017-03-26T09:13:38+00:00
url: /?p=9971
categories:
  - Uncategorized

---
http://blog.csdn.net/liangxanhai/article/details/7767430

&nbsp;

pthread_create函数的详细讲解(包括向线程函数传递参数详解)
  
标签： threadinclude编译器nulllinuxgcc
  
2012-07-20 14:52 56250人阅读 评论(4) 收藏 举报
  
分类：
  
unix高级编程学习（6）
  
版权声明：本文为博主原创文章，未经博主允许不得转载。

目录(?)[+]

pthread_create是UNIX环境创建线程函数头文件
  
#include<pthread.h>函数声明
  
int pthread\_create(pthread\_t\*restrict tidp,const pthread\_attr\_t \*restrict\_attr,void\*（\*start\_rtn)(void\*),void \*restrict arg);返回值
  
若成功则返回0，否则返回出错编号
  
返回成功时，由tidp指向的内存单元被设置为新创建线程的线程ID。attr参数用于制定各种不同的线程属性。新创建的线程从start\_rtn函数的地址开始运行，该函数只有一个万能指针参数arg，如果需要向start\_rtn函数传递的参数不止一个，那么需要把这些参数放到一个结构中，然后把这个结构的地址作为arg的参数传入。
  
linux下用C开发多线程程序，Linux系统下的多线程遵循POSIX线程接口，称为pthread。
  
由 restrict 修饰的指针是最初唯一对指针所指向的对象进行存取的方法，仅当第二个指针基于第一个时，才能对对象进行存取。对对象的存取都限定于基于由 restrict 修饰的指针表达式中。 由 restrict 修饰的指针主要用于函数形参，或指向由 malloc() 分配的内存空间。restrict 数据类型不改变程序的语义。 编译器能通过作出 restrict 修饰的指针是存取对象的唯一方法的假设，更好地优化某些类型的例程。参数
  
第一个参数为指向线程标识符的指针。
  
第二个参数用来设置线程属性。
  
第三个参数是线程运行函数的起始地址。
  
最后一个参数是运行函数的参数。
  
另外，在编译时注意加上-lpthread参数，以调用静态链接库。因为pthread并非Linux系统的默认库示例
  
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
  
printf(&#8220;%s pid %u tid %u (0x%x)\n&#8221;, s,
  
(unsigned int)pid, (unsigned int)tid, (unsigned int)tid);
  
} void \*thr_fn(void \*arg)
  
{
  
printids(&#8220;new thread: &#8220;);
  
return((void *)0);
  
}
  
int main(void)
  
{
  
int err;
  
err = pthread\_create(&ntid, NULL, thr\_fn, NULL);
  
if (err != 0)
  
printf(&#8220;can&#8217;t create thread: %s\n&#8221;, strerror(err));
  
printids(&#8220;main thread:&#8221;);
  
sleep(1);
  
exit(0);
  
}
  
$ gcc main.c -lpthread
  
$ ./a.out

向线程函数传递参数详解：

向线程函数传递参数分为两种：

（1）线程函数只有一个参数的情况：直接定义一个变量通过应用传给线程函数。

例子：

#include <iostream>
  
#include <pthread.h>
  
using namespace std;
  
pthread_t thread;
  
void fn(void *arg)
  
{
  
int i = \*(int \*)arg;
  
cout<<&#8220;i = &#8220;<<i<<endl;
  
return ((void *)0);
  
}
  
int main()
  
{
  
int err1;
  
int i=10;
  
err1 = pthread_create(&thread, NULL, fn, &i);
  
pthread_join(thread, NULL);
  
}
  
2、线程函数有多个参数的情况：这种情况就必须申明一个结构体来包含所有的参数，然后在传入线程函数，具体如下：
  
例子：

首先定义一个结构体：

struct  parameter

{

int size,

int count;

。。。。。

。。。
  
};

然后在main函数将这个结构体指针，作为void *形参的实际参数传递

struct parameter arg;

&nbsp;

通过如下的方式来调用函数：
  
pthread_create(&ntid, NULL, fn,& (arg));
  
函数中需要定义一个parameter类型的结构指针来引用这个参数
  
void fn(void *arg)
  
{
  
int i = \*(int \*)arg;
  
cout<<&#8220;i = &#8220;<<i<<endl;
  
return ((void *)0);
  
}

&nbsp;

void thr_fn(void *arg)
  
{
  
struct parameter *pstru;
  
pstru = ( struct parameter *) arg;
  
然后在这个函数中就可以使用指针来使用相应的变量的值了。
  
}