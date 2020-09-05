+++
author = "w1100n"
date = "2020-08-28 13:10:45" 
title = "fork"

+++
 一个进程，包括代码、数据和分配给进程的资源。fork（）函数通过系统调用创建一个与原来进程几乎完全相同的进程，也就是两个进程可以做完全相同的事，但如果初始参数或者传入的变量不同，两个进程也可以做不同的事。
    一个进程调用fork（）函数后，系统先给新的进程分配资源，例如存储数据和代码的空间。然后把原来的进程的所有值都复制到新的新进程中，只有少数值与原来的进程的值不同。相当于克隆了一个自己。

     我们来看一个例子：

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

     运行结果是：
    i am the child process, my process id is 5574
    我是爹的儿子
    统计结果是: 1
    i am the parent process, my process id is 5573
    我是孩子他爹
    统计结果是: 1



    https://blog.csdn.net/jason314/article/details/5640969
    