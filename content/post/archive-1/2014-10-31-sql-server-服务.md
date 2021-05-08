---
title: Java 信号量 Semaphore
author: w1100n
type: post
date: 2014-10-31T02:46:50+00:00
url: /?p=6997
categories:
  - Uncategorized

---
http://www.cnblogs.com/whgw/archive/2011/09/29/2195555.html

Semaphore当前在多线程环境下被扩放使用，操作系统的信号量是个很重要的概念，在进程控制方面都有应用。Java 并发库 的Semaphore 可以很轻松完成信号量控制，Semaphore可以控制某个资源可被同时访问的个数，通过 acquire() 获取一个许可，如果没有就等待，而 release() 释放一个许可。比如在Windows下可以设置共享文件的最大客户端访问个数。

Semaphore实现的功能就类似厕所有5个坑，假如有10个人要上厕所，那么同时只能有多少个人去上厕所呢？同时只能有5个人能够占用，当5个人中 的任何一个人让开后，其中等待的另外5个人中又有一个人可以占用了。另外等待的5个人中可以是随机获得优先机会，也可以是按照先来后到的顺序获得机会，这取决于构造Semaphore对象时传入的参数选项。单个信号量的Semaphore对象可以实现互斥锁的功能，并且可以是由一个线程获得了"锁"，再由另一个线程释放"锁"，这可应用于死锁恢复的一些场合。

Semaphore维护了当前访问的个数，提供同步机制，控制同时访问的个数。在数据结构中链表可以保存"无限"的节点，用Semaphore可以实现有限大小的链表。另外重入锁 ReentrantLock 也可以实现该功能，但实现上要复杂些。

下面的Demo中申明了一个只有5个许可的Semaphore，而有20个线程要访问这个资源，通过acquire()和release()获取和释放访问许可。

package com.test;

import java.util.concurrent.ExecutorService;

import java.util.concurrent.Executors;

import java.util.concurrent.Semaphore;

public class TestSemaphore {

                public static void main(String[] args) {
    
                // 线程池
    
                ExecutorService exec = Executors.newCachedThreadPool();
    
                // 只能5个线程同时访问
    
                final Semaphore semp = new Semaphore(5);
    
                 // 模拟20个客户端访问
    
                 for (int index = 0; index < 20; index++) {
    
                              final int NO = index;
    
                              Runnable run = new Runnable() {
    
                                                 public void run() {
    
                                                            try {
    
                                                                    // 获取许可
    
                                                                    semp.acquire();
    
                                                                    System.out.println("Accessing: " + NO);
    
                                                                    Thread.sleep((long) (Math.random() * 10000));
    
                                                                    // 访问完后，释放
    
                                                                    semp.release();
    
                                                                    System.out.println("-----------------"+semp.availablePermits());
    
                                                            } catch (InterruptedException e) {
    
                                                                    e.printStackTrace();
    
                                                            }
    
                                                  }
    
                                      };
    
                      exec.execute(run);
    
             }
    
             // 退出线程池
    
             exec.shutdown();
    
       }
    

}

执行结果如下: 

Accessing: 0

Accessing: 1

Accessing: 3

Accessing: 4

Accessing: 2

------0

Accessing: 6

------1

Accessing: 7

------1

Accessing: 8

------1

Accessing: 10

------1

Accessing: 9

------1

Accessing: 5

------1

Accessing: 12

------1

Accessing: 11

------1

Accessing: 13

------1

Accessing: 14

------1

Accessing: 15

------1

Accessing: 16

------1

Accessing: 17

------1

Accessing: 18

------1

Accessing: 19