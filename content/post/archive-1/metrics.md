---
title: java metrics
author: "-"
date: 2015-09-08T06:40:32+00:00
url: java/metrics
categories:
  - java
tags:
  - reprint
---
## java metrics

## Metrics 类型

### Counters

Counter 就是计数器, Counter 只是用 Gauge 封装了 AtomicLong

### Gauges

最简单的度量指标，只有一个简单的返回值，例如，我们想衡量一个待处理队列中任务的个数

### Meters

Meter度量一系列事件发生的速率 (rate)，例如 TPS, Meters 会统计最近 1分钟，5分钟，15分钟，还有全部时间的速率。

### Histograms

Histogram 统计数据的分布情况。比如最小值，最大值，中间值，还有中位数，75百分位, 90百分位, 95百分位, 98百分位, 99百分位, 和 99.9百分位的值 (percentiles)。

### Timers

Timer其实是 Histogram 和 Meter 的结合， histogram 某部分代码/调用的耗时， meter 统计 TPS
  
### 其他

除此之外，Metrics还提供了 HealthCheck 用来检测某个某个系统是否健康，例如数据库连接是否正常。还有Metrics Annotation，可以很方便地实现统计某个方法，某个值的数据。感兴趣的可以点进链接看看。

https://mvnrepository.com/artifact/io.dropwizard.metrics/metrics-core

### gradle dependency

    compile group: 'io.dropwizard.metrics', name: 'metrics-core', version: '3.1.2'

```java
private static final MetricRegistry metrics = new MetricRegistry();
private static ConsoleReporter reporter = ConsoleReporter.forRegistry(metrics).build();
private static final Meter meter = metrics.meter(name(DruidTest.class, "request"));

meter.mark();

reporter.report();

//Timer

public class TimerTest {

public static Random random = new Random();

public static void main(String[] args) throws InterruptedException {
MetricRegistry registry = new MetricRegistry();
ConsoleReporter reporter = ConsoleReporter.forRegistry(registry).build();
reporter.start(1, TimeUnit.SECONDS);

Timer timer = registry.timer(MetricRegistry.name(TimerTest.class,"get-latency"));

Timer.Context ctx;

while(true){
ctx = timer.time();
Thread.sleep(random.nextInt(1000));
ctx.stop();
}

}

}

```

http://www.cnblogs.com/nexiyi/p/metrics_sample_1.html  
http://blog.csdn.net/hengyunabc/article/details/44072285  
http://wuchong.me/blog/2015/08/01/getting-started-with-metrics/

基于dropwizard/metrics ，kafka，zabbix构建应用统计数据收集展示系统
  
分类:  Java2015-03-05 23:13 1372人阅读 评论(0) 收藏 举报
  
请求metricszabbixjavakafka

目录(?)[+]

新blog地址: http://hengyunabc.github.io/about-metrics/
  
想要实现的功能
  
应用可以用少量的代码，实现统计某类数据的功能
  
统计的数据可以很方便地展示
  
metrics
  
metrics，按字面意思是度量，指标。

举具体的例子来说，一个web服务器: 
  
- 一分钟内请求多少次？
  
- 平均请求耗时多长？
  
- 最长请求时间？
  
- 某个方法的被调用次数，时长？

以缓存为例: 
  
- 平均查询缓存时间？
  
- 缓存获取不命中的次数/比例？

以jvm为例: 
  
- GC的次数？
  
- Old Space的大小？

在一个应用里，需要收集的metrics数据是多种多样的，需求也是各不同的。需要一个统一的metrics收集，统计，展示平台。

流行的metrics的库  
https://github.com/dropwizard/metrics
  
java实现，很多开源项目用到，比如hadoop，kafka。下面称为dropwizard/metrics。
https://github.com/tumblr/colossus
  
scala实现，把数据存到OpenTsdb上。

spring boot 项目里的metrics: 
http://docs.spring.io/spring-boot/docs/current/reference/html/production-ready-metrics.html

spring boot里的metrics很多都是参考dropwizard/metrics的。
