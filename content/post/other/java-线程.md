---
title: Java 线程池, thread pool, ThreadPoolExecutor
author: "-"
date: 2012-08-26T11:59:46+00:00
url: /?p=3951

categories:
  - inbox
tags:
  - reprint
---
## Java 线程池, thread pool, ThreadPoolExecutor
在操作系统中，线程是一个非常重要的资源，频繁创建和销毁大量线程会大大降低系统性能。Java线程池原理类似于数据库连接池，目的就是帮助我们实现线程复用，减少频繁创建和销毁线程。ThreadPoolExecutor
  
ThreadPoolExecutor是线程池的核心类。首先看一下如何创建一个ThreadPoolExecutor。下面是ThreadPoolExecutor常用的一个构造方法: ThreadPoolExecutor(int corePoolSize, int maximumPoolSize, long keepAliveTime, TimeUnit unit, BlockingQueue<Runnable> workQueue)
  
参数介绍: 

corePoolSize
  
核心线程数量，线程池刚创建时，线程数量为0，当每次执行execute添加新的任务时会在线程池创建一个新的线程，直到线程数量达到corePoolSize为止。

workQueue
  
阻塞队列，当线程池正在运行的线程数量已经达到corePoolSize，那么再通过execute添加新的任务则会被加到workQueue队列中，在队列中排队等待执行，而不会立即执行。

maximumPoolSize
  
最大线程数量，当workQueue队列已满，放不下新的任务，再通过execute添加新的任务则线程池会再创建新的线程，线程数量大于corePoolSize但不会超过maximumPoolSize，如果超过maximumPoolSize，那么会抛出异常，如RejectedExecutionException。

**keepAliveTime (线程活动保持时间) **
  
线程池的工作线程空闲后，保持存活的时间。所以如果任务很多，并且每个任务执行的时间比较短，可以调大这个时间，提高线程的利用率

keepAliveTime when the number of threads is greater than
         
the core, this is the maximum time that excess idle threads
         
will wait for new tasks before terminating.
  
当线程数大于核心时，空闲线程等待新任务的最长时间。

TimeUnit (线程活动保持时间的单位) : 可选的单位有天 (DAYS) ，小时 (HOURS) ，分钟 (MINUTES) ，毫秒(MILLISECONDS)，微秒(MICROSECONDS, 千分之一毫秒)和毫微秒(NANOSECONDS, 千分之一微秒)。
  
总结一下线程池添加任务的整个流程: 

RejectedExecutionHandler (饱和策略) : 当队列和线程池都满了，说明线程池处于饱和状态，那么必须采取一种策略处理提交的新任务。这个策略默认情况下是AbortPolicy，表示无法处理新任务时抛出异常。以下是JDK1.5提供的四种策略。
  
AbortPolicy: 直接抛出异常。
  
CallerRunsPolicy: 只用调用者所在线程来运行任务。
  
DiscardOldestPolicy: 丢弃队列里最近的一个任务，并执行当前任务。
  
DiscardPolicy: 不处理，丢弃掉。
  
当然也可以根据应用场景需要来实现RejectedExecutionHandler接口自定义策略。如记录日志或持久化不能处理的任务。

1.当线程池小于corePoolSize时，新提交任务将创建一个新线程执行任务，即使此时线程池中存在空闲线程。
  
2.当线程池达到corePoolSize时，新提交任务将被放入workQueue中，等待线程池中任务调度执行
  
3.当workQueue已满，且maximumPoolSize>corePoolSize时，新提交任务会创建新线程执行任务
  
4.当提交任务数超过maximumPoolSize时，新提交任务由RejectedExecutionHandler处理
  
5.当线程池中超过corePoolSize线程，空闲时间达到keepAliveTime时，关闭空闲线程
  
6.当设置allowCoreThreadTimeOut(true)时，线程池中corePoolSize线程空闲时间达到keepAliveTime也将关闭

线程池刚刚创建是，线程数量为0；
  
执行execute添加新的任务时会在线程池创建一个新的线程；
  
当线程数量达到corePoolSize时，再添加新任务则会将任务放到workQueue队列；
  
当队列已满放不下新的任务，再添加新任务则会继续创建新线程，但线程数量不超过maximumPoolSize；
  
当线程数量达到maximumPoolSize时，再添加新任务则会抛出异常。
  
### Executors
  
Executors提供了一些创建线程池的工具方法。

    Executors.newSingleThreadExecutor()
  
源码实现: 

new ThreadPoolExecutor(1, 1, 0L, TimeUnit.MILLISECONDS, new LinkedBlockingQueue<Runnable>())

corePoolSize和maximumPoolSize都为1，也就是创建了一个固定大小是1的线程池，workQueue是new LinkedBlockingQueue<Runnable>()也就是队列的大小是Integer.MAX_VALUE，可以认为是队列的大小不限制。

由此可以得出通过该方法创建的线程池，每次只能同时运行一个线程，当有多个任务同时提交时，那也要一个一个排队执行。

Executors.newFixedThreadPool(int nThreads)
  
源码实现: 

new ThreadPoolExecutor(nThreads, nThreads, 0L, TimeUnit.MILLISECONDS, new LinkedBlockingQueue<Runnable>())

类似Executors.newSingleThreadExecutor()也是创建了一个固定大小的线程池，但是可以指定同时运行的线程数量为nThreads。

Executors.newCachedThreadPool()
  
源码实现: 

new ThreadPoolExecutor(0, Integer.MAX_VALUE, 60L, TimeUnit.SECONDS, new SynchronousQueue<Runnable>())

corePoolSize为0，maximumPoolSize为Integer.MAX_VALUE可以视为无穷大，workQueue是一个SynchronousQueue。SynchronousQueue可以认为是一个长度限制为0的队列，也就是向这个队列添加任务会永远是已满的状态。

由此可以得出通过该方法创建的线程池并不限制线程数量，每次添加的任务都会直接执行而不会放入workQueue，它的主要提供的功能是线程复用，但不能控制线程数量。

ExecutorService pool = Executors.newFixedThreadPool(3);
  
Thread t1 = new MyThread();
  
pool.execute(t1);
  
Executors 类使用 ExecutorService 提供了一个 ThreadPoolExecutor 的简单实现，但 ThreadPoolExecutor 提供的功能远不止这些。我们可以指定创建 ThreadPoolExecutor 实例时活跃的线程数，并且可以限制线程池的大小，还可以创建自己的 RejectedExecutionHandler 实现来处理不适合放在工作队列里的任务。

ExecutorService:  线程池接口。
  
ScheduledExecutorService 能和Timer/TimerTask类似，解决那些需要任务重复执行的问题。
  
ThreadPoolExecutor ExecutorService的默认实现。
  
ScheduledThreadPoolExecutor 继承ThreadPoolExecutor的ScheduledExecutorService接口实现，周期性任务调度的类实现。
  
要配置一个线程池是比较复杂的，尤其是对于线程池的原理不是很清楚的情况下，很有可能配置的线程池不是较优的，因此在Executors类里面提供了一些静态工厂，生成一些常用的线程池。

newSingleThreadExecutor: 创建一个单线程的线程池。这个线程池只有一个线程在工作，也就是相当于单线程串行执行所有任务。如果这个唯一的线程因为异常结束，那么会有一个新的线程来替代它。此线程池保证所有任务的执行顺序按照任务的提交顺序执行。
  
newFixedThreadPool: 创建固定大小的线程池。每次提交一个任务就创建一个线程，直到线程达到线程池的最大大小。线程池的大小一旦达到最大值就会保持不变，如果某个线程因为执行异常而结束，那么线程池会补充一个新线程。
  
newCachedThreadPool: 创建一个可缓存的线程池。如果线程池的大小超过了处理任务所需要的线程，那么就会回收部分空闲 (60秒不执行任务) 的线程，当任务数增加时，此线程池又可以智能的添加新线程来处理任务。此线程池不会对线程池大小做限制，线程池大小完全依赖于操作系统 (或者说JVM) 能够创建的最大线程大小。
  
newScheduledThreadPool: 创建一个大小无限的线程池。此线程池支持定时以及周期性执行任务的需求。
  
缓存线程池与固定线程池的区别在于对于需要执行很多短期异步任务的程序来说，缓存线程池可以提高程序性能，因为长时间保持空闲的这种类型的线程池不会占用任何资源，调用缓存线程池对象将重用以前构造的线程 (线程可用状态) ，若线程没有可用的，则创建一个新线程添加到池中，缓存线程池将终止并从池中移除60秒未被使用的线程。

1. shutdown方法: 这个方法会平滑地关闭ExecutorService，当我们调用这个方法时，ExecutorService停止接受任何新的任务且等待已经提交的任务执行完成(已经提交的任务会分两类: 一类是已经在执行的，另一类是还没有开始执行的)，当所有已经提交的任务执行完毕后将会关闭ExecutorService。这里我们先不举例在下面举例。

2. awaitTermination方法: 这个方法有两个参数，一个是timeout即超时时间，另一个是unit即时间单位。这个方法会使线程等待timeout时长，当超过timeout时间后，会监测ExecutorService是否已经关闭，若关闭则返回true，否则返回false。一般情况下会和shutdown方法组合使用。

ThreadPoolExecutor

线程池类为 java.util.concurrent.ThreadPoolExecutor，常用构造方法为: 

ThreadPoolExecutor(
  
int corePoolSize,
  
int maximumPoolSize,

long keepAliveTime,
  
TimeUnit unit,

BlockingQueue<Runnable> workQueue,

RejectedExecutionHandler handler)
  
corePoolSize:  线程池维护线程的最少数量

maximumPoolSize: 线程池维护线程的最大数量

keepAliveTime:  线程池维护线程所允许的空闲时间

unit:  线程池维护线程所允许的空闲时间的单位

workQueue:  线程池所使用的缓冲队列

handler:  线程池对拒绝任务的处理策略

一个任务通过 execute(Runnable)方法被添加到线程池，任务就是一个 Runnable类型的对象，任务的执行方法就是 Runnable类型对象的run()方法。

当一个任务通过execute(Runnable)方法欲添加到线程池时: 

l 如果此时线程池中的数量小于corePoolSize，即使线程池中的线程都处于空闲状态，也要创建新的线程来处理被添加的任务。

2 如果此时线程池中的数量等于 corePoolSize，但是缓冲队列 workQueue未满，那么任务被放入缓冲队列。

3 如果此时线程池中的数量大于corePoolSize，缓冲队列workQueue满，并且线程池中的数量小于maximumPoolSize，建新的线程来处理被添加的任务。

4 如果此时线程池中的数量大于corePoolSize，缓冲队列workQueue满，并且线程池中的数量等于maximumPoolSize，那么通过 handler所指定的策略来处理此任务。也就是: 处理任务的优先级为: 核心线程corePoolSize、任务队列workQueue、最大线程maximumPoolSize，如果三者都满了，使用handler处理被拒绝的任务。

5 当线程池中的线程数量大于 corePoolSize时，如果某线程空闲时间超过keepAliveTime，线程将被终止。这样，线程池可以动态的调整池中的线程数。

unit可选的参数为java.util.concurrent.TimeUnit中的几个静态属性: 

NANOSECONDS、MICROSECONDS、MILLISECONDS、SECONDS。

workQueue常用的是: java.util.concurrent.ArrayBlockingQueue

handler有四个选择: 

ThreadPoolExecutor.AbortPolicy()

抛出java.util.concurrent.RejectedExecutionException异常

ThreadPoolExecutor.CallerRunsPolicy()

重试添加当前的任务，他会自动重复调用execute()方法

ThreadPoolExecutor.DiscardOldestPolicy()

抛弃旧的任务

ThreadPoolExecutor.DiscardPolicy()

抛弃当前的任务

二、相关参考

一个 ExecutorService，它使用可能的几个池线程之一执行每个提交的任务，通常使用 Executors 工厂方法配置。

线程池可以解决两个不同问题: 由于减少了每个任务调用的开销，它们通常可以在执行大量异步任务时提供增强的性能，并且还可以提供绑定和管理资源 (包括执行集合任务时使用的线程) 的方法。每个 ThreadPoolExecutor 还维护着一些基本的统计数据，如完成的任务数。

为了便于跨大量上下文使用，此类提供了很多可调整的参数和扩展挂钩。但是，强烈建议程序员使用较为方便的 Executors 工厂方法Executors.newCachedThreadPool() (无界线程池，可以进行自动线程回收) 、Executors.newFixedThreadPool(int) (固定大小线程池) 和Executors.newSingleThreadExecutor() (单个后台线程) ，它们均为大多数使用场景预定义了设置。否则，在手动配置和调整此类时，使用以下指导: 

核心和最大池大小

ThreadPoolExecutor 将根据 corePoolSize (参见 getCorePoolSize()) 和 maximumPoolSize (参见 getMaximumPoolSize()) 设置的边界自动调整池大小。当新任务在方法execute(java.lang.Runnable) 中提交时，如果运行的线程少于 corePoolSize，则创建新线程来处理请求，即使其他辅助线程是空闲的。如果运行的线程多于 corePoolSize 而少于 maximumPoolSize，则仅当队列满时才创建新线程。如果设置的 corePoolSize 和 maximumPoolSize 相同，则创建了固定大小的线程池。如果将 maximumPoolSize 设置为基本的无界值 (如 Integer.MAX_VALUE) ，则允许池适应任意数量的并发任务。在大多数情况下，核心和最大池大小仅基于构造来设置，不过也可以使用setCorePoolSize(int) 和 setMaximumPoolSize(int) 进行动态更改。

按需构造

默认情况下，即使核心线程最初只是在新任务需要时才创建和启动的，也可以使用方法 prestartCoreThread() 或 prestartAllCoreThreads() 对其进行动态重写。

创建新线程

使用 ThreadFactory 创建新线程。如果没有另外说明，则在同一个 ThreadGroup 中一律使用 Executors.defaultThreadFactory() 创建线程，并且这些线程具有相同的NORM_PRIORITY 优先级和非守护进程状态。通过提供不同的 ThreadFactory，可以改变线程的名称、线程组、优先级、守护进程状态，等等。如果从 newThread 返回null 时 ThreadFactory 未能创建线程，则执行程序将继续运行，但不能执行任何任务。

保持活动时间

如果池中当前有多于 corePoolSize 的线程，则这些多出的线程在空闲时间超过 keepAliveTime 时将会终止 (参见 getKeepAliveTime(java.util.concurrent.TimeUnit)) 。这提供了当池处于非活动状态时减少资源消耗的方法。如果池后来变得更为活动，则可以创建新的线程。也可以使用方法 setKeepAliveTime(long, java.util.concurrent.TimeUnit) 动态地更改此参数。使用 Long.MAX_VALUE TimeUnit.NANOSECONDS 的值在关闭前有效地从以前的终止状态禁用空闲线程。

排队

所有 BlockingQueue 都可用于传输和保持提交的任务。可以使用此队列与池大小进行交互: 

A. 如果运行的线程少于 corePoolSize，则 Executor 始终首选添加新的线程，而不进行排队。

B. 如果运行的线程等于或多于 corePoolSize，则 Executor 始终首选将请求加入队列，而不添加新的线程。

C. 如果无法将请求加入队列，则创建新的线程，除非创建此线程超出 maximumPoolSize，在这种情况下，任务将被拒绝。

排队有三种通用策略: 

直接提交。工作队列的默认选项是 SynchronousQueue，它将任务直接提交给线程而不保持它们。在此，如果不存在可用于立即运行任务的线程，则试图把任务加入队列将失败，因此会构造一个新的线程。此策略可以避免在处理可能具有内部依赖性的请求集合时出现锁定。直接提交通常要求无界 maximumPoolSizes 以避免拒绝新提交的任务。当命令以超过队列所能处理的平均数连续到达时，此策略允许无界线程具有增长的可能性。

无界队列。使用无界队列 (例如，不具有预定义容量的 LinkedBlockingQueue) 将导致在所有 corePoolSize 线程都忙的情况下将新任务加入队列。这样，创建的线程就不会超过 corePoolSize。 (因此，maximumPoolSize 的值也就无效了。) 当每个任务完全独立于其他任务，即任务执行互不影响时，适合于使用无界队列；例如，在 Web页服务器中。这种排队可用于处理瞬态突发请求，当命令以超过队列所能处理的平均数连续到达时，此策略允许无界线程具有增长的可能性。

有界队列。当使用有限的 maximum PoolSizes 时，有界队列 (如 ArrayBlockingQueue) 有助于防止资源耗尽，但是可能较难调整和控制。队列大小和最大池大小可能需要相互折衷: 使用大型队列和小型池可以最大限度地降低 CPU 使用率、操作系统资源和上下文切换开销，但是可能导致人工降低吞吐量。如果任务频繁阻塞 (例如，如果它们是 I/O 边界) ，则系统可能为超过您许可的更多线程安排时间。使用小型队列通常要求较大的池大小，CPU 使用率较高，但是可能遇到不可接受的调度开销，这样也会降低吞吐量。

被拒绝的任务

当 Executor 已经关闭，并且 Executor 将有限边界用于最大线程和工作队列容量，且已经饱和时，在方法 execute(java.lang.Runnable) 中提交的新任务将被拒绝。在以上两种情况下，execute 方法都将调用其 RejectedExecutionHandler 的 RejectedExecutionHandler.rejectedExecution(java.lang.Runnable, java.util.concurrent.ThreadPoolExecutor) 方法。下面提供了四种预定义的处理程序策略: 

A. 在默认的 ThreadPoolExecutor.AbortPolicy 中，处理程序遭到拒绝将抛出运行时 RejectedExecutionException。

B. 在 ThreadPoolExecutor.CallerRunsPolicy 中，线程调用运行该任务的 execute 本身。此策略提供简单的反馈控制机制，能够减缓新任务的提交速度。

C. 在 ThreadPoolExecutor.DiscardPolicy 中，不能执行的任务将被删除。

D. 在 ThreadPoolExecutor.DiscardOldestPolicy 中，如果执行程序尚未关闭，则位于工作队列头部的任务将被删除，然后重试执行程序 (如果再次失败，则重复此过程) 。

定义和使用其他种类的 RejectedExecutionHandler 类也是可能的，但这样做需要非常小心，尤其是当策略仅用于特定容量或排队策略时。

挂钩方法

此类提供 protected 可重写的 beforeExecute(java.lang.Thread, java.lang.Runnable) 和 afterExecute(java.lang.Runnable, java.lang.Throwable) 方法，这两种方法分别在执行每个任务之前和之后调用。它们可用于操纵执行环境；例如，重新初始化 ThreadLocal、搜集统计信息或添加日志条目。此外，还可以重写方法 terminated() 来执行 Executor 完全终止后需要完成的所有特殊处理。

如果挂钩或回调方法抛出异常，则内部辅助线程将依次失败并突然终止。

队列维护

方法 getQueue() 允许出于监控和调试目的而访问工作队列。强烈反对出于其他任何目的而使用此方法。remove(java.lang.Runnable) 和 purge() 这两种方法可用于在取消大量已排队任务时帮助进行存储回收。

线程池的监控

通过线程池提供的参数进行监控。线程池里有一些属性在监控线程池的时候可以使用

taskCount: 线程池需要执行的任务数量。
  
completedTaskCount: 线程池在运行过程中已完成的任务数量。小于或等于taskCount。
  
largestPoolSize: 线程池曾经创建过的最大线程数量。通过这个数据可以知道线程池是否满过。如等于线程池的最大大小，则表示线程池曾经满了。
  
getPoolSize:线程池的线程数量。如果线程池不销毁的话，池里的线程不会自动销毁，所以这个大小只增不+ getActiveCount: 获取活动的线程数。
  
通过扩展线程池进行监控。通过继承线程池并重写线程池的beforeExecute，afterExecute和terminated方法，我们可以在任务执行前，执行后和线程池关闭前干一些事情。如监控任务的平均执行时间，最大执行时间和最小执行时间等。

http://www.cnblogs.com/jersey/archive/2011/03/30/2000231.html
  
http://sunnylocus.iteye.com/blog/223327

http://coach.iteye.com/blog/743185

http://www.cnblogs.com/www-35java-com/archive/2010/12/31/1923495.html

http://coach.iteye.com/blog/855850

http://dongxuan.iteye.com/blog/901689

http://www.cnblogs.com/jersey/archive/2011/03/30/2000231.html

http://denghua10.iteye.com/blog/999442

http://blog.csdn.net/java2000_net/article/details/2972352

http://www.infoq.com/cn/articles/java-threadPool
  
http://825635381.iteye.com/blog/2184680