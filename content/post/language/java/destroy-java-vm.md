---
title: DestroyJavaVM 与 JVM 内置线程
author: "-"
date: 2017-03-30T07:30:51+00:00
lastmod: 2026-07-16T03:32:16+08:00
url: destroy-java-vm
categories:
  - Java
tags:
  - jvm
  - remix
  - AI-assisted
aliases:
  - /p9996/
---

## 现象

用 `jcmd <pid> Thread.print` 查看 Java 进程的线程 dump 时，经常能看到几个"内置"线程，其中 `DestroyJavaVM` 最容易让人误以为是 bug 或线程泄漏：

1. **DestroyJavaVM**：负责在程序退出时卸载 JVM 的线程，大部分时间都在等待，直到虚拟机真正关闭。
2. **Signal Dispatcher**：处理操作系统发给 JVM 的原生信号。
3. **Finalizer**：从 finalization 队列取出对象并调用其 `finalize` 方法。
4. **Reference Handler**：高优先级线程，负责将待处理的 Reference 加入队列，定义在 `java.lang.ref.Reference`。

## DestroyJavaVM 为什么会"一直挂着"

这是因为大多数应用不只有 `main` 一个线程，还会额外创建其它线程。

所有 POJO 应用都从 `main` 方法开始执行。最简单的情况下，`main` 方法会完成所有工作：创建对象、调用方法等。一旦 `main` 执行完毕，JVM 会启动一个 `DestroyJavaVM` 线程来关闭虚拟机，这个线程会等待所有线程都执行完毕后才真正做关闭的工作，以确保你创建的线程都能跑完再销毁 JVM。

而带 GUI 的应用通常会运行一组线程：一个监听键盘、鼠标等系统事件，一个维护窗口和显示等。这类应用的 `main` 方法可能只是启动所需的线程后就退出了。它同样会创建 `DestroyJavaVM` 线程，但这时该线程要做的就是等待所有已创建的线程完成后才关闭虚拟机。

因此，任何创建了线程并依赖这些线程完成工作的应用，都会有一个 `DestroyJavaVM` 线程在等待它们结束。由于它做的只是 `join` 其他所有运行中的线程，本身不会消耗额外资源。

## 现代 JDK（包括 JDK 26）里还存在吗

存在。`DestroyJavaVM` 是 JNI Invocation API 里虚拟机启动 / 关闭机制的一部分，从早期 JDK 到当前的 HotSpot 都没有变过，线程 dump 里依然能看到这个线程名。

需要注意的是 **Finalizer** 线程：`Object.finalize()` 从 JDK 9 起被标记为 deprecated，JDK 18（JEP 421）彻底移除了默认的 finalization 机制。因此在只用 `Cleaner` / try-with-resources、不触碰 `finalize()` 的现代应用里，Finalizer 线程可能不会被真正用到，但作为 JVM 内置线程它依然存在。

## 参考

- [Default threads like DestroyJavaVM, Reference Handler, Signal Dispatcher](https://stackoverflow.com/questions/5766026/default-threads-like-destroyjavavm-reference-handler-signal-dispatcher)
- [DestroyJavaVM thread always running](https://stackoverflow.com/questions/34433267/destroyjavavm-thread-always-running)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-16 | 文件重命名为 `destroy-java-vm.md`；url 改为 `destroy-java-vm`；标题改为「DestroyJavaVM 与 JVM 内置线程」；categories 由 `Inbox` 改为 `Java`；重新分节整理正文；补充「现代 JDK（包括 JDK 26）里还存在吗」一节，说明 DestroyJavaVM 机制未变、Finalizer 因 JEP 421 使用场景减少；标签由 `reprint` 改为 `remix`、`AI-assisted` | 内容与站内其他 Java 文章一致按规范整理，并回答作者关于现代 JDK 是否仍存在此机制的提问 |
