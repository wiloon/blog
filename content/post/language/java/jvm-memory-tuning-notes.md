---
title: JVM Memory Layout and Tuning Notes
author: "-"
date: 2012-04-14T11:45:30+00:00
lastmod: 2026-07-16T03:19:01+08:00
url: jvm-memory-tuning-notes
categories:
  - Java
tags:
  - jvm
  - memory
  - tuning
  - remix
  - AI-assisted
aliases:
  - /p2908/
---

## 说明

本文是一篇较早的 JVM 调优笔记，原文涵盖的堆栈基础、GC 算法、分代模型、G1 设计目标等内容，站内已有更完整、持续维护的独立文章：

- GC 分代模型、回收算法、收集器与发展时间线 → [Java GC](./gc.md)
- HotSpot 启动参数（堆、分代比例、GC 日志、收集器选择等）→ [HotSpot JVM 启动参数](./hotspot-options.md)
- 堆、栈、方法区基础概念 → [Java 堆栈方法区](./java-heap-stack-method.md)
- 强引用 / 软引用 / 弱引用 / 虚引用 → [Java 引用类型](./java-强引用-软引用-弱引用-虚引用.md)
- 生产环境诊断工具（Arthas、async-profiler、JFR 等）→ [Java 生产环境诊断工具选型](./java-production-diagnostics-tooling.md)

本文只保留原文中站内暂未覆盖的部分：对象内存布局与大小计算、一份历史调优配置示例、内存泄漏排查思路，以及关于 JVM 内存设计的一点延伸思考。

## Java 对象的内存布局与大小

一个空 `Object` 对象在堆中的大小是 **8 byte**，这只是对象头的大小，不包含任何字段：

```java
Object ob = new Object();
```

这行代码实际占用 **4 byte + 8 byte**：4 byte 是栈中保存引用所需的空间，8 byte 是堆中对象头的信息。因为所有 Java 非基本类型对象都默认继承 `Object`，所以任何 Java 对象的大小都必然大于 8 byte。

有了空对象的大小，可以推算其他对象的大小，例如：

```java
class NewObject {
    int count;
    boolean flag;
    Object ob;
}
```

其大小为：空对象大小（8 byte）+ int（4 byte）+ boolean（1 byte）+ Object 引用（4 byte）= 17 byte。由于 JVM 对对象内存分配按 8 字节对齐，实际占用会向上取整到 24 byte。

需要注意基本类型包装类的大小：包装类型本身是对象，本身就要有对象头开销，按 8 字节对齐后一个基本类型包装类的实际大小至少是 16 byte，是对应基本类型的数倍，因此应尽量避免不必要的装箱。

## 历史调优配置示例（仅供参考）

以下是较早期针对传统分代 GC（Parallel、CMS）的典型配置组合，现代应用（尤其是使用 G1/ZGC 之后）已不建议照搬，最新参数请见 [HotSpot JVM 启动参数](./hotspot-options.md)。

```bash
# 吞吐量优先：并行收集器
java -Xmx3800m -Xms3800m -Xmn2g -Xss128k -XX:+UseParallelGC -XX:ParallelGCThreads=20

# 响应时间优先：并发收集器（CMS，已在 JDK 14 移除）
java -Xmx3550m -Xms3550m -Xmn2g -Xss128k -XX:ParallelGCThreads=20 \
  -XX:+UseConcMarkSweepGC -XX:+UseParNewGC
```

其中体现的调优思路对现代收集器同样成立：

- 响应时间优先的应用：年轻代尽可能设大，直到接近系统能接受的最长停顿，可以减少晋升到老年代的对象。
- 吞吐量优先的应用：年轻代同样尽可能设大，配合多核并行收集，适合科学计算、批处理等无交互场景。
- `-Xms` 与 `-Xmx` 设为相同值可以避免运行期堆扩容带来的额外开销。

## 内存泄漏排查思路

内存泄漏和系统超负荷容易混淆，但两者不是一回事：内存泄漏是"用完的资源没有被回收"，系统超负荷是"确实没有更多资源可分配"。

判断内存泄漏的常见思路：系统运行一段时间后，分别在多次 Full GC 之后做堆快照，观察 GC 后剩余的堆占用是否随时间持续抬高。如果每次 GC 后的谷底值不断升高，说明可能存在无法被回收的对象，值得用堆快照对比进一步排查（常见根因是集合类持有了不该持有的引用）。

几种具体 OOM 类型的现象和解法，见对应文章：

- 老年代 / 持久代被写满 → [java.lang.OutOfMemoryError: PermGen space](./java-lang-outofmemoryerror-permgen-space.md)
- 无法创建线程 → [java.lang.OutOfMemoryError: unable to create new native thread](./java-lang-outofmemoryerror-unable-to-create-new-native-thread.md)

## 关于 JVM 内存设计的一点思考

垃圾回收减轻了手动管理内存的负担，但在高性能、高并发场景下，垃圾回收暂停本身会成为瓶颈。除了从算法层面优化（更短停顿、并发收集），也可以从系统设计层面减少 JVM 需要管理的内存：

- **数据库 / 文件系统**：把业务数据都放数据库或文件系统，JVM 内存基本只需覆盖处理一次请求所需的空间，但每次都要读写外部存储，效率较低。
- **内存-硬盘映射**：用 memcached 这类方案把数据放在独立进程的内存里，应用侧仍然按读写文件的方式访问，既有缓存的效率又不占用 JVM 自身堆内存。
- **同机部署多个 JVM**：把应用纵向（按模块）或横向（按实例）拆分成多个 JVM 进程，让每个 JVM 的堆都控制在可接受的回收停顿范围内，代价是引入了分布式的复杂性。

## 参考资料

- 《深入 Java 虚拟机》。虽然年代已久，但依旧是经典参考书。

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-16 | 文件重命名为 `jvm-memory-tuning-notes.md`；url 改为 `jvm-memory-tuning-notes`；标题改为 "JVM Memory Layout and Tuning Notes"；删除与 `gc.md` / `hotspot-options.md` / `java-heap-stack-method.md` / `java-强引用-软引用-弱引用-虚引用.md` / `java-production-diagnostics-tooling.md` 等文章重复的 GC 算法、分代模型、堆栈基础、引用类型、参数汇总、G1 早期设计、调优工具等章节，改为链接；移除大量已失效的 iteye.com 图片链接及未验证的外部参考链接；保留对象内存布局与大小计算、历史调优配置示例、内存泄漏排查思路、JVM 内存设计思考等站内独有内容；标签由 `reprint` 改为 `remix`、`AI-assisted` | 原文内容与站内多篇现代文章高度重复，且存在大量失效外链图片，作者要求整理并精简重复内容 |
