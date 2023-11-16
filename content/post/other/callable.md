---
title: Java Callable, Future 和 FutureTask
author: "-"
date: 2014-11-26T06:43:53+00:00
url: callable
categories:
  - Java
tags:
  - reprint
  - thread
---
## Java Callable, Future 和 FutureTask

创建线程有两种方式，一种是直接继承 Thread，另外一种就是实现 Runnable 接口。
  
这两种方式都有一个缺陷就是: 在执行完任务之后无法获取执行结果。
  
如果需要获取执行结果，就必须通过共享变量或者使用线程通信的方式来达到效果，这样使用起来就比较麻烦。
  
而自从Java 1.5 开始，JDK 提供了 Callable 和 Future, 通过它们可以在任务执行完毕之后得到任务执行结果。

今天我们就来讨论一下 Callable、Future 和 FutureTask 三个类的使用方法。以下是本文的目录大纲:

- Callable 与 Runnable
- Future
- FutureTask
- 使用示例

### Callable 与 Runnable

java.lang.Runnable 是一个接口，里面只声明了一个 run() 方法

```java
public interface Runnable {      
    public abstract void run();
}
```

由于run()方法返回值为void类型，所以在执行完任务之后无法返回任何结果。

Callable 位于 java.util.concurrent 包下，它也是一个接口，在它里面也只声明了一个方法，只不过这个方法叫做 call():

```java
public interface Callable<V> {
      
V call() throws Exception;
  
}
```

可以看到，这是一个泛型接口，call()函数返回的类型就是传递进来的V类型。

那么怎么使用 Callable 呢？ 一般情况下是配合 ExecutorService 来使用的，在 ExecutorService 接口中声明了若干个 submit 方法的重载版本:

```java
<T> Future<T> submit(Callable<T> task);
  
<T> Future<T> submit(Runnable task, T result);
  
Future<?> submit(Runnable task);
```

第一个submit方法里面的参数类型就是 Callable。
  
暂时只需要知道 Callable 一般是和 ExecutorService 配合来使用的

### Future

Future就是对于具体的Runnable或者Callable任务的执行结果进行取消、查询是否完成、获取结果。必要时可以通过get方法获取执行结果，该方法会阻塞直到任务返回结果。

Future类位于java.util.concurrent包下，它是一个接口:

```java
public interface Future<V> {
      
boolean cancel(boolean mayInterruptIfRunning);
      
boolean isCancelled();
      
boolean isDone();
      
V get() throws InterruptedException, ExecutionException;
      
V get(long timeout, TimeUnit unit) throws InterruptedException, ExecutionException, TimeoutException;
}
```

在Future接口中声明了5个方法，下面依次解释每个方法的作用:

### cancel

cancel方法用来取消任务，如果取消任务成功则返回true，如果取消任务失败则返回false。参数mayInterruptIfRunning表示是否允许取消正在执行却没有执行完毕的任务，如果设置true，则表示可以取消正在执行过程中的任务。如果任务已经完成，则无论 mayInterruptIfRunning 为true还是false，此方法肯定返回false，即如果取消已经完成的任务会返回false；如果任务正在执行，若mayInterruptIfRunning设置为true，则返回true，若mayInterruptIfRunning设置为false，则返回false；如果任务还没有执行，则无论mayInterruptIfRunning为true还是false，肯定返回true。

### isCancelled

isCancelled 方法表示任务是否被取消成功，如果在任务正常完成前被取消成功，则返回 true。

### isDone

isDone 方法表示任务是否已经完成，若任务完成，则返回true；

### get

get() 方法用来获取执行结果，这个方法会产生阻塞，会一直等到任务执行完毕才返回；
  
get(long timeout, TimeUnit unit)用来获取执行结果，如果在指定时间内，还没获取到结果，就直接返回null。

也就是说Future提供了三种功能:
  
1) 判断任务是否完成；
  
2) 能够中断任务；
  
3) 能够获取任务执行结果。

Executor就是Runnable和Callable的调度容器，Future就是对于具体的Runnable或者Callable任务的执行结果进行
  
取消、查询是否完成、获取结果、设置结果操作。get方法会阻塞，直到任务返回结果(Future简介)。
  
Future只是一个接口，所以是无法直接用来创建对象使用的，因此就有了下面的FutureTask。

### FutureTask

我们先来看一下 FutureTask 的实现:

```java
public class FutureTask<V> implements RunnableFuture<V>

FutureTask 类实现了RunnableFuture接口，我们看一下RunnableFuture接口的实现:

public interface RunnableFuture<V> extends Runnable, Future<V> {

void run();
  
}
```

可以看出 RunnableFuture 继承了Runnable接口和Future接口，而FutureTask实现了RunnableFuture接口。所以它既可以作为Runnable被线程执行，又可以作为 Future 得到 Callable 的返回值。

FutureTask 提供了2个构造器:

public FutureTask(Callable<V> callable) {
}
  
public FutureTask(Runnable runnable, V result) {
}
  
事实上，FutureTask是 Future 接口的一个唯一实现类。
  
FutureTask 既是 Future
  
Runnable，又是包装了 Callable(

如果是Runnable最终也会被转换为 Callable )， 它是这两者的合体。

### 使用示例

1. 使用Callable + Future获取执行结果

```java
import java.util.concurrent.*;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Callable1 {
    private static final Logger LOGGER = LoggerFactory.getLogger(Callable1.class);

    public static void main(String[] args) {
        ExecutorService executorService = Executors.newCachedThreadPool();

        Future<Integer> future = executorService.submit(new Foo());
        executorService.submit(new Foo());
        while (true) {
            System.out.println(future.isDone());
            if (future.isDone()) {
                try {
                    System.out.println(String.valueOf(future.get()));
                } catch (InterruptedException e) {
                    e.printStackTrace();
                } catch (ExecutionException e) {
                    e.printStackTrace();
                }
                executorService.shutdownNow();
            }
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

    }

    static class Foo implements Callable<Integer> {

        @Override
        public Integer call() throws Exception {
            LOGGER.info("thread name: {}, thread id: {}", Thread.currentThread().getName(),
                    Thread.currentThread().getId());
            return 99;
        }
    }
}
```

//第二种方式，注意这种方式和第一种方式效果是类似的，只不过一个使用的是ExecutorService，一个使用的是Thread

```java
import java.util.concurrent.Callable;
import java.util.concurrent.FutureTask;

import org.slf4j.LoggerFactory;
import org.slf4j.Logger;

public class Callable0 {
    private static final Logger LOGGER = LoggerFactory.getLogger(Callable0.class);

    public static void main(String[] args) {
        FutureTask<Integer> futureTask = new FutureTask<>(new Foo());
        Thread t = new Thread(futureTask);
        t.start();
        try {
            Thread.sleep(1000);
            System.out.println(futureTask.get());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    static class Foo implements Callable<Integer> {
        @Override
        public Integer call() {
            LOGGER.info("thread name: {}, thread id: {}", Thread.currentThread().getName(),
                    Thread.currentThread().getId());

            return 99;
        }
    }
}
```

如果为了可取消性而使用 Future 但又不提供可用的结果，则可以声明 Future<?> 形式类型、并返回 null 作为底层任务的结果。

[http://www.cnblogs.com/dolphin0520/p/3949310.html](http://www.cnblogs.com/dolphin0520/p/3949310.html)

若有不正之处请多多谅解，并欢迎批评指正。  
请尊重作者劳动成果，转载请标明原文链接:  
[http://www.cnblogs.com/dolphin0520/p/3949310.html](http://www.cnblogs.com/dolphin0520/p/3949310.html)

### Callable

Runnable实现的是 void run() 方法，Callable实现的是 V call() 方法，并且可以返回执行结果，其中Runnable可以提交给Thread来包装下，直接启动一个线程来执行，而Callable则一般都是提交给ExecuteService来执行。通常在开发中结合ExecutorService使用,将任务的提交与任务的执行解耦开,同时也能更好地利用Executor提供的各种特性
