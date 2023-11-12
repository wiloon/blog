---
title: 'python timed task, 定时任务'
author: "-"
date: 2011-10-23T08:46:30+00:00
url: python/timed/task
categories:
  - Python
tags:
  - Python

---
## python timed task, 定时任务

- while True sleep
- Timeloop
- threading.Timer
- sched
- schedule
- APScheduler
- Celery
- Apache Airflow

### while True: + sleep()

主要缺点：

只能设定间隔，不能指定具体的时间，比如每天早上8:00
sleep 是一个阻塞函数，也就是说 sleep 这一段时间，程序什么也不能操作。

### Timeloop库

Timeloop是一个库，可用于运行多周期任务。这是一个简单的库，它使用decorator模式在线程中运行标记函数。

### threading.Timer

threading 模块中的 Timer 是一个非阻塞函数，比 sleep 稍好一点，timer最基本理解就是定时器，我们可以启动多个定时任务，这些定时器任务是异步执行，所以不存在等待顺序执行问题。

### 内置模块sched

sched模块实现了一个通用事件调度器，在调度器类使用一个延迟函数等待特定的时间，执行任务。同时支持多线程应用程序，在每个任务执行后会立刻调用延时函数，以确保其他线程也能执行。

比threading.Timer更好，不需要循环调用。

### 调度模块schedule

schedule是一个第三方轻量级的任务调度模块，可以按照秒，分，小时，日期或者自定义事件执行时间。schedule允许用户使用简单、人性化的语法以预定的时间间隔定期运行Python函数(或其它可调用函数)。

### 任务框架 APScheduler

APScheduler（advanceded python scheduler）基于Quartz的一个Python定时任务框架，实现了Quartz的所有功能，使用起来十分方便。提供了基于日期、固定时间间隔以及crontab类型的任务，并且可以持久化任务。基于这些功能，我们可以很方便的实现一个Python定时任务系统。

它有以下三个特点：

类似于 Liunx Cron 的调度程序(可选的开始/结束时间)
基于时间间隔的执行调度(周期性调度，可选的开始/结束时间)
一次性执行任务(在设定的日期/时间运行一次任务)
APScheduler有四种组成部分：

触发器(trigger) 包含调度逻辑，每一个作业有它自己的触发器，用于决定接下来哪一个作业会运行。除了他们自己初始配置意外，触发器完全是无状态的。
作业存储(job store) 存储被调度的作业，默认的作业存储是简单地把作业保存在内存中，其他的作业存储是将作业保存在数据库中。一个作业的数据讲在保存在持久化作业存储时被序列化，并在加载时被反序列化。调度器不能分享同一个作业存储。
执行器(executor) 处理作业的运行，他们通常通过在作业中提交制定的可调用对象到一个线程或者进城池来进行。当作业完成时，执行器将会通知调度器。
调度器(scheduler) 是其他的组成部分。你通常在应用只有一个调度器，应用的开发者通常不会直接处理作业存储、调度器和触发器，相反，调度器提供了处理这些的合适的接口。配置作业存储和执行器可以在调度器中完成，例如添加、修改和移除作业。通过配置executor、jobstore、trigger，使用线程池(ThreadPoolExecutor默认值20)或进程池(ProcessPoolExecutor 默认值5)并且默认最多3个(max_instances)任务实例同时运行，实现对job的增删改查等调度控制

### 分布式消息系统Celery

Celery是一个简单，灵活，可靠的分布式系统，用于处理大量消息，同时为操作提供维护此类系统所需的工具, 也可用于任务调度。Celery 的配置比较麻烦，如果你只是需要一个轻量级的调度工具，Celery 不会是一个好选择。

### 数据流工具 Apache Airflow

Apache Airflow 是Airbnb开源的一款数据流程工具，目前是Apache孵化项目。以非常灵活的方式来支持数据的ETL过程，同时还支持非常多的插件来完成诸如HDFS监控、邮件通知等功能。Airflow支持单机和分布式两种模式，支持Master-Slave模式，支持Mesos等资源调度，有非常好的扩展性。被大量公司采用。

Airflow使用Python开发，它通过DAGs(Directed Acyclic Graph, 有向无环图)来表达一个工作流中所要执行的任务，以及任务之间的关系和依赖。

<https://cloud.tencent.com/developer/article/1887717>
