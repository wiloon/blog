---
title: java openjdk JMH
author: "-"
date: 2014-09-03T01:04:10+00:00
url: /?p=6973
categories:
  - Java
tags:
  - reprint
---
## java openjdk JMH

create test project with maven

```java
mvn archetype:generate \
-DinteractiveMode=false \
-DarchetypeGroupId=org.openjdk.jmh \
-DarchetypeArtifactId=jmh-java-benchmark-archetype \
-DgroupId=org.sample \
-DartifactId=test \
-Dversion=1.0
```

JMH 是一个由 OpenJDK/Oracle 里面那群开发了 Java 编译器的大牛们所开发的 Micro Benchmark Framework 。何谓 Micro Benchmark 呢？简单地说就是在 method 层面上的 benchmark，精度可以精确到微秒级。可以看出 JMH 主要使用在当你已经找出了热点函数，而需要对热点函数进行进一步的优化时，就可以使用 JMH 对优化的效果进行定量的分析。

比较典型的使用场景还有: 

想定量地知道某个函数需要执行多长时间，以及执行时间和输入 n 的相关性
  
一个函数有两种不同实现 (例如实现 A 使用了 FixedThreadPool，实现 B 使用了 ForkJoinPool) ，不知道哪种实现性能更好
  
尽管 JMH 是一个相当不错的 Micro Benchmark Framework，但很无奈的是网上能够找到的文档比较少，而官方也没有提供比较详细的文档，对使用造成了一定的障碍。但是有个好消息是官方的 Code Sample 写得非常浅显易懂，推荐在需要详细了解 JMH 的用法时可以通读一遍——本文则会介绍 JMH 最典型的用法和部分常用选项。

第一个例子

如果你使用 maven 来管理你的 Java 项目的话，引入 JMH 是一件很简单的事情——只需要在 pom.xml 里增加 JMH 的依赖即可<properties> <jmh.version>1.14.1</jmh.version> </properties> 

<dependencies>
      
<dependency>
          
<groupId>org.openjdk.jmh</groupId>
          
<artifactId>jmh-core</artifactId>
          
<version>${jmh.version}</version>
      
</dependency>
      
<dependency>
          
<groupId>org.openjdk.jmh</groupId>
          
jmh-generator-annprocess</artifactId>
          
<version>${jmh.version}</version>
          
<scope>provided</scope>
      
</dependency>
  
</dependencies>
  
接下来再创建我们的第一个 Benchmark

@BenchmarkMode(Mode.AverageTime)
  
@OutputTimeUnit(TimeUnit.MICROSECONDS)
  
@State(Scope.Thread)
  
public class FirstBenchmark {

    @Benchmark
    public int sleepAWhile() {
        try {
            Thread.sleep(500);
        } catch (InterruptedException e) {
            // ignore
        }
        return 0;
    }
    
    public static void main(String[] args) throws RunnerException {
        Options opt = new OptionsBuilder()
                .include(FirstBenchmark.class.getSimpleName())
                .forks(1)
                .warmupIterations(5)
                .measurementIterations(5)
                .build();
    
        new Runner(opt).run();
    }
    

}
  
有不少你可能是第一次见到的注解，不过不着急，接下来会解释这些注解的意义。我们先来跑一下这个 benchmark 吧 🙂

# JMH 1.14.1 (released 39 days ago)

# VM version: JDK 1.8.0_11, VM 25.11-b03

# VM invoker: /Library/Java/JavaVirtualMachines/jdk1.8.0_11.jdk/Contents/Home/jre/bin/java

# VM options: -Didea.launcher.port=7535 -Didea.launcher.bin.path=/Applications/IntelliJ IDEA 15 CE.app/Contents/bin -Dfile.encoding=UTF-8

# Warmup: 5 iterations, 1 s each

# Measurement: 5 iterations, 1 s each

# Timeout: 10 min per iteration

# Threads: 1 thread, will synchronize iterations

# Benchmark mode: Average time, time/op

# Benchmark: com.dyng.FirstBenchmark.sleepAWhile

# Run progress: 0.00% complete, ETA 00:00:10

# Fork: 1 of 1

# Warmup Iteration 1: 503.440 ms/op

# Warmup Iteration 2: 503.885 ms/op

# Warmup Iteration 3: 503.714 ms/op

# Warmup Iteration 4: 504.333 ms/op

# Warmup Iteration 5: 502.596 ms/op

Iteration 1: 504.352 ms/op
  
Iteration 2: 502.583 ms/op
  
Iteration 3: 501.256 ms/op
  
Iteration 4: 501.655 ms/op
  
Iteration 5: 504.212 ms/op

Result "sleepAWhile":
    
502.811 ±(99.9%) 5.495 ms/op [Average]
    
(min, avg, max) = (501.256, 502.811, 504.352), stdev = 1.427
    
CI (99.9%): [497.316, 508.306] (assumes normal distribution)

# Run complete. Total time: 00:00:12

Benchmark Mode Cnt Score Error Units
  
FirstBenchmark.sleepAWhile avgt 5 502.811 ± 5.495 ms/op
  
对 sleepAWhile() 的测试结果显示执行时间平均约为502毫秒。因为我们的测试对象 sleepAWhile() 正好就是睡眠500毫秒，所以 JMH 显示的结果可以说很符合我们的预期。

那好，现在我们再来详细地解释代码的意义。不过在这之前，需要先了解一下 JMH 的几个基本概念。

基本概念

Mode
  
Mode 表示 JMH 进行 Benchmark 时所使用的模式。通常是测量的维度不同，或是测量的方式不同。目前 JMH 共有四种模式: 

Throughput: 整体吞吐量，例如"1秒内可以执行多少次调用"。
  
AverageTime: 调用的平均时间，例如"每次调用平均耗时xxx毫秒"。
  
SampleTime: 随机取样，最后输出取样结果的分布，例如"99%的调用在xxx毫秒以内，99.99%的调用在xxx毫秒以内"
  
SingleShotTime: 以上模式都是默认一次 iteration 是 1s，唯有 SingleShotTime 是只运行一次。往往同时把 warmup 次数设为0，用于测试冷启动时的性能。
  
Iteration
  
Iteration 是 JMH 进行测试的最小单位。在大部分模式下，一次 iteration 代表的是一秒，JMH 会在这一秒内不断调用需要 benchmark 的方法，然后根据模式对其采样，计算吞吐量，计算平均执行时间等。

Warmup
  
Warmup 是指在实际进行 benchmark 前先进行预热的行为。为什么需要预热？因为 JVM 的 JIT 机制的存在，如果某个函数被调用多次之后，JVM 会尝试将其编译成为机器码从而提高执行速度。所以为了让 benchmark 的结果更加接近真实情况就需要进行预热。

注解

现在来解释一下上面例子中使用到的注解，其实很多注解的意义完全可以望文生义 🙂

@Benchmark
  
表示该方法是需要进行 benchmark 的对象，用法和 JUnit 的 @Test 类似。

@Mode
  
Mode 如之前所说，表示 JMH 进行 Benchmark 时所使用的模式。

@State
  
State 用于声明某个类是一个"状态"，然后接受一个 Scope 参数用来表示该状态的共享范围。因为很多 benchmark 会需要一些表示状态的类，JMH 允许你把这些类以依赖注入的方式注入到 benchmark 函数里。Scope 主要分为两种。

Thread: 该状态为每个线程独享。
  
Benchmark: 该状态在所有线程间共享。
  
关于State的用法，官方的 code sample 里有比较好的例子。

@OutputTimeUnit
  
benchmark 结果所使用的时间单位。

启动选项

解释完了注解，再来看看 JMH 在启动前设置的参数。

Options opt = new OptionsBuilder()
          
.include(FirstBenchmark.class.getSimpleName())
          
.forks(1)
          
.warmupIterations(5)
          
.measurementIterations(5)
          
.build();

new Runner(opt).run();
  
include
  
benchmark 所在的类的名字，注意这里是使用正则表达式对所有类进行匹配的。

fork
  
进行 fork 的次数。如果 fork 数是2的话，则 JMH 会 fork 出两个进程来进行测试。

warmupIterations
  
预热的迭代次数。

measurementIterations
  
实际测量的迭代次数。

第二个例子

在看过第一个完全只为示范的例子之后，再来看一个有实际意义的例子。

问题: 

计算 1 ~ n 之和，比较串行算法和并行算法的效率，看 n 在大约多少时并行算法开始超越串行算法

首先定义一个表示这两种实现的接口

public interface Calculator {
      
/**
       
* calculate sum of an integer array
       
* @param numbers
       
* @return
       
*/
      
public long sum(int[] numbers);

    /**
     * shutdown pool or reclaim any related resources
     */
    public void shutdown();
    

}
  
由于这两种算法的实现不是这篇文章的重点，而且本身并不困难，所以实际代码就不赘述了。如果真的感兴趣的话，可以看最后的附录。以下仅说明一下我所指的串行算法和并行算法的含义。

串行算法: 使用 for-loop 来计算 n 个正整数之和。
  
并行算法: 将所需要计算的 n 个正整数分成 m 份，交给 m 个线程分别计算出和以后，再把它们的结果相加。
  
进行 benchmark 的代码如下

@BenchmarkMode(Mode.AverageTime)
  
@OutputTimeUnit(TimeUnit.MICROSECONDS)
  
@State(Scope.Benchmark)
  
public class SecondBenchmark {
      
@Param({"10000", "100000", "1000000"})
      
private int length;

    private int[] numbers;
    private Calculator singleThreadCalc;
    private Calculator multiThreadCalc;
    
    public static void main(String[] args) throws RunnerException {
        Options opt = new OptionsBuilder()
                .include(SecondBenchmark.class.getSimpleName())
                .forks(2)
                .warmupIterations(5)
                .measurementIterations(5)
                .build();
    
        new Runner(opt).run();
    }
    
    @Benchmark
    public long singleThreadBench() {
        return singleThreadCalc.sum(numbers);
    }
    
    @Benchmark
    public long multiThreadBench() {
        return multiThreadCalc.sum(numbers);
    }
    
    @Setup
    public void prepare() {
        numbers = IntStream.rangeClosed(1, length).toArray();
        singleThreadCalc = new SinglethreadCalculator();
        multiThreadCalc = new MultithreadCalculator(Runtime.getRuntime().availableProcessors());
    }
    
    @TearDown
    public void shutdown() {
        singleThreadCalc.shutdown();
        multiThreadCalc.shutdown();
    }
    

}
  
注意到这里用到了3个之前没有使用的注解。

@Param
  
@Param 可以用来指定某项参数的多种情况。特别适合用来测试一个函数在不同的参数输入的情况下的性能。

@Setup
  
@Setup 会在执行 benchmark 之前被执行，正如其名，主要用于初始化。

@TearDown
  
@TearDown 和 @Setup 相对的，会在所有 benchmark 执行结束以后执行，主要用于资源的回收等。

最后来猜猜看实际结果如何？并行算法在哪个问题集下能够超越串行算法？

我在自己的 mac 上跑下来的结果，总数在10000时并行算法不如串行算法，总数达到100000时并行算法开始和串行算法接近，总数达到1000000时并行算法所耗时间约是串行算法的一半左右。

常用选项

还有一些 JMH 的常用选项没有提及的，简单地在此介绍一下

CompilerControl
  
控制 compiler 的行为，例如强制 inline，不允许编译等。

Group
  
可以把多个 benchmark 定义为同一个 group，则它们会被同时执行，主要用于测试多个相互之间存在影响的方法。

Level
  
用于控制 @Setup，@TearDown 的调用时机，默认是 Level.Trial，即benchmark开始前和结束后。

Profiler
  
JMH 支持一些 profiler，可以显示等待时间和运行时间比，热点函数等。

延伸阅读

IDE插件

IntelliJ 有 JMH 的插件，提供 benchmark 方法的自动生成等便利功能。

JMH 教程

Jenkov 的 JMH 教程，相比于这篇文章介绍得更为详细，非常推荐。顺便 Jenkov 的其他 Java 教程也非常值得一看。

附录

代码清单

public class SinglethreadCalculator implements Calculator {
      
public long sum(int[] numbers) {
          
long total = 0L;
          
for (int i : numbers) {
              
total += i;
          
}
          
return total;
      
}

    @Override
    public void shutdown() {
        // nothing to do
    }
    

}

public class MultithreadCalculator implements Calculator {
      
private final int nThreads;
      
private final ExecutorService pool;

    public MultithreadCalculator(int nThreads) {
        this.nThreads = nThreads;
        this.pool = Executors.newFixedThreadPool(nThreads);
    }
    
    private class SumTask implements Callable<Long> {
        private int[] numbers;
        private int from;
        private int to;
    
        public SumTask(int[] numbers, int from, int to) {
            this.numbers = numbers;
            this.from = from;
            this.to = to;
        }
    
        public Long call() throws Exception {
            long total = 0L;
            for (int i = from; i < to; i++) {
                total += numbers[i];
            }
            return total;
        }
    }
    
    public long sum(int[] numbers) {
        int chunk = numbers.length / nThreads;
    
        int from, to;
        List<SumTask> tasks = new ArrayList<SumTask>();
        for (int i = 1; i <= nThreads; i++) {
            if (i == nThreads) {
                from = (i - 1) * chunk;
                to = numbers.length;
            } else {
                from = (i - 1) * chunk;
                to = i * chunk;
            }
            tasks.add(new SumTask(numbers, from, to));
        }
    
        try {
            List<Future<Long>> futures = pool.invokeAll(tasks);
    
            long total = 0L;
            for (Future<Long> future : futures) {
                total += future.get();
            }
            return total;
        } catch (Exception e) {
            // ignore
            return 0;
        }
    }
    
    @Override
    public void shutdown() {
        pool.shutdown();
    }
    

}

http://blog.dyngr.com/blog/2016/10/29/introduction-of-jmh/
  
http://openjdk.java.net/projects/code-tools/jmh/