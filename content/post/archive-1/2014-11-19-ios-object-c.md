---
title: Mutex
author: wiloon
type: post
date: 2014-11-19T08:39:34+00:00
url: /?p=7025
categories:
  - Uncategorized

---
https://casatwy.com/pthreadde-ge-chong-tong-bu-ji-zhi.html

MUTual-EXclude Lock，互斥锁。 它是理解最容易，使用最广泛的一种同步机制。顾名思义，被这个锁保护的临界区就只允许一个线程进入，其它线程如果没有获得锁权限，那就只能在外面等着。

它使用得非常广泛，以至于大多数人谈到锁就是mutex。mutex是互斥锁，pthread里面还有很多锁，mutex只是其中一种。