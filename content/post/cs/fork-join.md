---
title: ForkJoin
author: "-"
date: 2017-06-22T02:11:10+00:00
url: ForkJoin
categories:
  - cs
tags:
  - reprint
---
## ForkJoin

ForkJoinPool适合执行计算密集型且可进行拆分任务并汇总结果(类似MapReduce)的任务，执行这种任务可以充分利用多核处理器优势提高任务处理速度，实际上ForkJoinPool内部的工作窃取队列的高性能(远高于普通线程池的BlockingQueue)也决定其适用于执行大量的简短的小任务。
————————————————
版权声明：本文为CSDN博主「heng_zou」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：<https://blog.csdn.net/heng_zou/article/details/118193846>

什么是 Fork/Join 框架
Fork/Join 框架是 Java7 提供的一个用于并行执行任务的框架(Fork/Join Framework)， 是一个把大任务分割成若干个小任务，最终汇总每个小任务结果后得到大任务结果的框架。

我们再通过 Fork 和 Join 这两个单词来理解下 Fork/Join 框架，Fork 就是把一个大任务切分为若干子任务并行的执行，Join 就是合并这些子任务的执行结果，最后得到这个大任务的结果。比如计算 1+ 2+... + 10000，可以分割成 10 个子任务，每个子任务分别对 1000 个数进行求和，最终汇总这 10 个子任务的结果。

## ForkJoinPool

<http://blog.dyngr.com/blog/2016/09/15/java-forkjoinpool-internals/>

ForkJoinPool 不是为了替代 ExecutorService, 而是它的补充, 在某些应用场景下性能比 ExecutorService 更好。 (见 Java Tip: When to use ForkJoinPool vs ExecutorService )

<https://www.infoworld.com/article/2078440/java-tip-when-to-use-forkjoinpool-vs-executorservice.html>
  
ForkJoinPool 主要用于实现"分而治之"的算法, 特别是分治之后递归调用的函数, 例如 quick sort 等。 [[quick-sort]]

ForkJoinPool 最适合的是**计算密集型**的任务, 如果存在 I/O, 线程间同步, sleep() 等会造成线程长时间阻塞的情况时, 最好配合使用 ManagedBlocker

## ManagedBlocker怎么使用？

答：ManagedBlocker相当于明确告诉ForkJoinPool框架要阻塞了，ForkJoinPool就会启另一个线程来运行任务，以最大化地利用CPU。

<https://juejin.cn/post/6844903990556098567>

## 示例

求整数数组所有元素之和: 计算1 至1000 的正整数之和。

## For-loop
  
最简单的, 显然是不使用任何并行编程的手段, 只用最直白的 for-loop 来实现。下面就是具体的实现代码。不过为了便于横向对比, 也为了让代码更加 Java Style, 首先我们先定义一个 interface。

```java
public interface Calculator {
    long sumUp(long[] numbers);
}
```

这个 interface 非常简单,只有一个函数 sumUp, 就是返回数组内所有元素的和。

再写一个 main 方法。

```java
public class Main {

public static void main(String[] args) {

long[] numbers = LongStream.rangeClosed(1, 1000).toArray();

Calculator calculator = new MyCalculator();

System.out.println(calculator.sumUp(numbers)); // 打印结果500500

}
  
}
```

接下来就是我们的 Plain Old For-loop Calculator, 简称 POFLC 的实现了。 (这其实是个段子, 和主题完全无关, 感兴趣的请见文末的彩蛋)

```java
public class ForLoopCalculator implements Calculator {

public long sumUp(long[] numbers) {

long total = 0;

for (long i : numbers) {

total += i;

}

return total;

}
  
}
```

前面花了点时间讲解了 ForkJoinPool 之前的实现方法,主要为了在代码的编写难度上进行一下对比。现在就列出本篇文章的重点 - ForkJoinPool 的实现方法。

```java
public class ForkJoinCalculator implements Calculator {

private ForkJoinPool pool;

    private static class SumTask extends RecursiveTask<Long> {
        private long[] numbers;
        private int from;
        private int to;
    
        public SumTask(long[] numbers, int from, int to) {
            this.numbers = numbers;
            this.from = from;
            this.to = to;
        }
    
        @Override
        protected Long compute() {
            // 当需要计算的数字小于6时,直接计算结果
            if (to - from < 6) {
                long total = 0;
                for (int i = from; i <= to; i++) {
                    total += numbers[i];
                }
                return total;
            // 否则,把任务一分为二,递归计算
            } else {
                int middle = (from + to) / 2;
                SumTask taskLeft = new SumTask(numbers, from, middle);
                SumTask taskRight = new SumTask(numbers, middle+1, to);
                taskLeft.fork();
                taskRight.fork();
                return taskLeft.join() + taskRight.join();
            }
        }
    }
    
    public ForkJoinCalculator() {
        // 也可以使用公用的 ForkJoinPool: 
        // pool = ForkJoinPool.commonPool()
        pool = new ForkJoinPool();
    }
    
    @Override
    public long sumUp(long[] numbers) {
        return pool.invoke(new SumTask(numbers, 0, numbers.length-1));
    }

}
```

可以看出,使用了 ForkJoinPool 的实现逻辑全部集中在了 compute() 这个函数里,仅用了14行就实现了完整的计算过程。特别是,在这段代码里没有显式地"把任务分配给线程",只是分解了任务,而把具体的任务到线程的映射交给了 ForkJoinPool 来完成。

原理

如果你除了 ForkJoinPool 的用法以外,对 ForkJoinPoll 的原理也感兴趣的话,那么请接着阅读这一节。在这一节中,我会结合 ForkJoinPool 的作者 Doug Lea 的论文——《A Java Fork/Join Framework》, 尽可能通俗地解释 Fork/Join Framework 的原理。

我一直以为, 要理解一样东西的原理, 最好就是自己尝试着去实现一遍。根据上面的示例代码, 可以看出 fork() 和 join() 是 Fork/Join Framework "魔法"的关键。我们可以根据函数名假设一下 fork() 和 join() 的作用:

fork(): 开启一个新线程 (或是重用线程池内的空闲线程), 将任务交给该线程处理。
  
join(): 等待该任务的处理线程处理完毕, 获得返回值。
  
以上模型似乎可以 (？) 解释 ForkJoinPool 能够多线程执行的事实,但有一个很明显的问题

当任务分解得越来越细时,所需要的线程数就会越来越多,而且大部分线程处于等待状态。

但是如果我们在上面的示例代码加入以下代码

System.out.println(pool.getPoolSize());
  
这会显示当前线程池的大小,在我的机器上这个值是4,也就是说只有4个工作线程。甚至即使我们在初始化 pool 时指定所使用的线程数为1时,上述程序也没有任何问题——除了变成了一个串行程序以外。

public ForkJoinCalculator() {

pool = new ForkJoinPool(1);
  
}
  
这个矛盾可以导出,我们的假设是错误的,并不是每个 fork() 都会促成一个新线程被创建,而每个 join() 也不是一定会造成线程被阻塞。Fork/Join Framework 的实现算法并不是那么"显然",而是一个更加复杂的算法——这个算法的名字就叫做 work stealing 算法。

work stealing 算法在 Doung Lea 的论文中有详细的描述,以下是我在结合 Java 1.8 代码的阅读以后——现有代码的实现有一部分相比于论文中的描述发生了变化——得到的相对通俗的解释:

基本思想

ForkJoinPool 的每个工作线程都维护着一个工作队列 (WorkQueue) ,这是一个双端队列 (Deque) ,里面存放的对象是任务 (ForkJoinTask) 。
  
每个工作线程在运行中产生新的任务 (通常是因为调用了 fork()) 时,会放入工作队列的队尾,并且工作线程在处理自己的工作队列时,使用的是 LIFO 方式,也就是说每次从队尾取出任务来执行。
  
每个工作线程在处理自己的工作队列同时, 会尝试窃取一个任务 (或是来自于刚刚提交到 pool 的任务,或是来自于其他工作线程的工作队列), 窃取的任务位于其他线程的工作队列的队首, 也就是说工作线程在窃取其他工作线程的任务时, 使用的是 FIFO 方式。
  
在遇到 join() 时,如果需要 join 的任务尚未完成, 则会先处理其他任务, 并等待其完成。
  
在既没有自己的任务, 也没有可以窃取的任务时, 进入休眠。
  
下面来介绍一下关键的两个函数: fork() 和 join() 的实现细节, 相比来说 fork() 比 join() 简单很多,所以先来介绍 fork()。

fork

fork() 做的工作只有一件事,既是把任务推入当前工作线程的工作队列里。可以参看以下的源代码:

public final ForkJoinTask<V> fork() {

Thread t;

if ((t = Thread.currentThread()) instanceof ForkJoinWorkerThread)

((ForkJoinWorkerThread)t).workQueue.push(this);

else

ForkJoinPool.common.externalPush(this);

return this;
  
}
  
join

join() 的工作则复杂得多,也是 join() 可以使得线程免于被阻塞的原因——不像同名的 Thread.join()。

检查调用 join() 的线程是否是 ForkJoinThread 线程。如果不是 (例如 main 线程) ,则阻塞当前线程,等待任务完成。如果是,则不阻塞。
  
查看任务的完成状态,如果已经完成,直接返回结果。
  
如果任务尚未完成,但处于自己的工作队列内,则完成它。
  
如果任务已经被其他的工作线程偷走,则窃取这个小偷的工作队列内的任务 (以 FIFO 方式) ,执行,以期帮助它早日完成欲 join 的任务。
  
如果偷走任务的小偷也已经把自己的任务全部做完,正在等待需要 join 的任务时,则找到小偷的小偷,帮助它完成它的任务。
  
递归地执行第5步。
  
将上述流程画成序列图的话就是这个样子:

以上就是 fork() 和 join() 的原理,这可以解释 ForkJoinPool 在递归过程中的执行逻辑,但还有一个问题

最初的任务是 push 到哪个线程的工作队列里的？

这就涉及到 submit() 函数的实现方法了

submit

其实除了前面介绍过的每个工作线程自己拥有的工作队列以外,ForkJoinPool 自身也拥有工作队列,这些工作队列的作用是用来接收由外部线程 (非 ForkJoinThread 线程) 提交过来的任务,而这些工作队列被称为 submitting queue 。

submit() 和 fork() 其实没有本质区别,只是提交对象变成了 submitting queue 而已 (还有一些同步,初始化的操作) 。submitting queue 和其他 work queue 一样,是工作线程"窃取"的对象,因此当其中的任务被一个工作线程成功窃取时,就意味着提交的任务真正开始进入执行阶段。

总结

在了解了 Fork/Join Framework 的工作原理之后,相信很多使用上的注意事项就可以从原理中找到原因。例如: 为什么在 ForkJoinTask 里最好不要存在 I/O 等会阻塞线程的行为？,这个我姑且留作思考题吧 🙂

还有一些延伸阅读的内容,在此仅提及一下:

ForkJoinPool 有一个 Async Mode ,效果是工作线程在处理本地任务时也使用 FIFO 顺序。这种模式下的 ForkJoinPool 更接近于是一个消息队列,而不是用来处理递归式的任务。
  
在需要阻塞工作线程时,可以使用 ManagedBlocker。
  
Java 1.8 新增加的 CompletableFuture 类可以实现类似于 Javascript 的 promise-chain,内部就是使用 ForkJoinPool 来实现的。
  
彩蛋

之所以煞有介事地取名为 POFLC,显然是为了模仿 POJO 。而 POJO —— Plain Old Java Object 这个词是如何产生的,在 stackoverflow 上有个帖子讨论过,摘录一下就是

I've come to the conclusion that people forget about regular Java objects because they haven't got a fancy name. That's why, while preparing for a talk in 2000, Rebecca Parsons, Josh Mackenzie, and I gave them one: POJOs (plain old Java objects).

我得出一个结论: 人们之所以总是忘记使用标准的 Java 对象是因为缺少一个足够装逼的名字 (译注: 类似于 Java Bean 这样的名字) 。因此,在准备2000年的演讲时,Rebecca Parsons,Josh Mackenzie 和我给他们起了一个名字叫做 POJO  (平淡无奇的 Java 对象) 。

><https://www.infoq.cn/article/fork-join-introduction>
><https://zhuanlan.zhihu.com/p/68554017>

之所以煞有介事地取名为 POFLC，显然是为了模仿 POJO 。而 POJO —— Plain Old Java Object 这个词是如何产生的，在 stackoverflow 上有个帖子讨论过，摘录一下就是

I’ve come to the conclusion that people forget about regular Java objects because they haven’t got a fancy name. That’s why, while preparing for a talk in 2000, Rebecca Parsons, Josh Mackenzie, and I gave them one: POJOs (plain old Java objects).

我得出一个结论：人们之所以总是忘记使用标准的 Java 对象是因为缺少一个足够装逼的名字（译注：类似于 Java Bean 这样的名字）。因此，在准备2000年的演讲时，Rebecca Parsons，Josh Mackenzie 和我给他们起了一个名字叫做 POJO （平淡无奇的 Java 对象）。

<https://stackoverflow.com/questions/3326319/what-is-meaning-of-plain-old-java-object-pojo>
