---
title: "race condition"
author: "-"
date: "2021-07-01 21:56:55"
url: "template"

categories:
  - inbox
tags:
  - reprint
---
## "race condition"
数据争用(data race) 和竞态条件(race condition)

在有关多线程编程的话题中，数据争用(data race) 和竞态条件(race condition)是两个经常被提及的名词，它们两个有着相似的名字，也是我们在并行编程中极力避免出现的。但在处理实际问题时，我们应该能明确区分它们两个。

1.数据争用(data race)
定义: 多个线程对于同一个变量、同时地、进行读/写操作的现象并且至少有一个线程进行写操作。 (也就是说，如果所有线程都是只进行读操作，那么将不构成数据争用) 
后果: 如果发生了数据争用，读取该变量时得到的值将变得不可知，使得该多线程程序的运行结果将完全不可预测，可能直接崩溃。
如何防止: 对于有可能被多个线程同时访问的变量使用排他访问控制，具体方法包括使用mutex (互斥量) 和monitor (监视器) ，或者使用atomic变量。

2.竞态条件(race condition)
相对于数据争用(data race)，竞态条件(race condition)指的是更加高层次的更加复杂的现象，一般需要在设计并行程序时进行细致入微的分析，才能确定。 (也就是隐藏得更深) 
定义: 受各线程上代码执行的顺序和时机的影响，程序的运行结果产生 (预料之外) 的变化。
后果: 如果存在竞态条件(race condition)，多次运行程序对于同一个输入将会有不同的结果，但结果并非完全不可预测，它将由输入数据和各线程的执行顺序共同决定。
如何预防: 竞态条件产生的原因很多是对于同一个资源的一系列连续操作并不是原子性的，也就是说有可能在执行的中途被其他线程抢占，同时这个“其他线程”刚好也要访问这个资源。解决方法通常是: 将这一系列操作作为一个critical section (临界区) 。

3.代码示例
下面以C++实现的一个银行存款转账操作为例，说明数据争用(data race) 和竞态条件(race condition)的区别。

该系统的不変性条件: 存款余额≥0，不允许借款。
3.1.数据争用的例子
int my_account = 0;      //我的账户余额
int your_account = 100;  //你的账户余额

// 转账操作: 存在数据争用(data race)！
bool racy_transfer(int& src, int& dst, int m)
{
  if (m <= src) {  //操作结果不可预测
    src -= m;      //操作结果不可预测
    dst += m;      //操作结果不可预测
    return true;
  } else {
    return false;
  }
}

// 将下面两个函数在两个线程分别运行
racy_transfer(your_account, my_account, 50);
racy_transfer(your_account, my_account, 80);
运行上面的的代码后，不光我们双方账号的余额不可预测，甚至整个系统会发生什么事情都无法保证。

3.2.竞态条件的例子
#include 
std::atomic<int> my_account = 0; //我的账户余额
std::atomic<int> your_account = 100;  //你的账户余额

// 汇款操作:没有数据争用(data race)，但存在竞态条件(race condition)！
bool unsafe_transfer(std::atomic<int>& src, std::atomic<int>& dst, int m)
{
  if (m <= src) {
    // ★在这个时候(m <= src)是否仍然成立？
    src -= m;
    dst += m;
    return true;
  } else {
    return false;
  }
}

//将下面两个函数在两个线程分别运行
unsafe_transfer(your_account, my_account, 50);//[A]
unsafe_transfer(your_account, my_account, 80);//[B]

上面代码中★所标注的就是竞态条件，也就是这时候m > src是完全有可能的。考虑以下三种情况: 

[A]执行结束后，your_account == my_account == 50，[B]再开始执行，然而条件不满足，转账失败；
[B]执行结束后，your_account == 20 && my_account == 80，[A]再开始执行，然而条件不满足，转账失败；
[A]和[B]交错执行，而且都进入了if块之内，最终结果变成your_account == -30 && my_account == 130，程序虽然能正常退出，但显然违反了不变性条件——存款余额≥0。
对应于C++的std::atomic<int>、在Java有java.util.concurrent.atomic.AtomicInteger类 (或者volatile修饰的变量) 。

3.3.解决办法
#include <mutex>
int my_account = 0;//我的账户余额
int your_account = 100; //你的账户余额
std::mutex txn_guard;

//安全的转账操作
bool safe_transfer(int& src, int& dst, int m)
{
  //声明临界区开始
  std::lock_guard<std::mutex> lk(txn_guard);
  if (m <= src) {
    src -= m;
    dst += m;
    return true;
  } else {
    return false;
  }
}  //临界区结束

//将下面两个函数在两个线程分别运行
safe_transfer(your_account, my_account, 50);  // [A]
safe_transfer(your_account, my_account, 80);  // [B]
这样程序只会产生以下两种结果: 

[A]执行结束后，your_account == my_account == 50，[B]再开始执行，然而条件不满足，转账失败: 
[B]执行结束后，your_account == 20 && my_account == 80，[A]再开始执行，然而条件不满足，转账失败；
而不会出现[A]和[B]交错执行的情况，从而使数据始终符合系统规定的不变形条件。对应于C++的std::mutex和std::lock_guard，在Java有monitor (通常不用显式声明) +synchronized的组合。
————————————————
版权声明: 本文为CSDN博主「烧煤的快感」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接: https://blog.csdn.net/gg_18826075157/article/details/72582939




https://blog.csdn.net/gg_18826075157/article/details/72582939
