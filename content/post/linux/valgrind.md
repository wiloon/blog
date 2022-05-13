---
author: "-"
date: "2021-06-15 20:44:23" 
title: "valgrind"
categories:
  - inbox
tags:
  - reprint
---
## "valgrind"


Valgrind是用于构建动态分析工具的探测框架。它包括一个工具集，每个工具执行某种类型的调试、分析或类似的任务，以帮助完善你的程序。Valgrind的架构是模块化的，所以可以容易地创建新的工具而又不会扰乱现有的结构。

Valgrind中许多有用的工具被作为标准而提供。

Memcheck是一个内存错误检测器。它有助于使你的程序，尤其是那些用C和C++写的程序，更加准确。
Cachegrind是一个缓存和分支预测分析器。它有助于使你的程序运行更快。
Callgrind是一个调用图缓存生成分析器。它与Cachegrind的功能有重叠，但也收集Cachegrind不收集的一些信息。
Helgrind是一个线程错误检测器。它有助于使你的多线程程序更加准确。
DRD也是一个线程错误检测器。它和Helgrind相似，但使用不同的分析技术，所以可能找到不同的问题。
Massif是一个堆分析器。它有助于使你的程序使用更少的内存。
DHAT是另一种不同的堆分析器。它有助于理解块的生命期、块的使用和布局的低效等问题。
SGcheck是一个实验工具，用来检测堆和全局数组的溢出。它的功能和Memcheck互补: SGcheck找到Memcheck无法找到的问题，反之亦然。
BBV是个实验性质的SimPoint基本块矢量生成器。它对于进行计算机架构的研究和开发很有用处。
也有一些对大多数用户没有用的小工具: Lackey是演示仪器基础的示例工具；Nulgrind是一个最小化的Valgrind工具，不做分析或者操作，仅用于测试目的。


---

https://yuanfentiank789.github.io/2018/11/01/%E7%94%A8Valgrind%E6%A3%80%E6%B5%8B%E5%86%85%E5%AD%98%E6%B3%84%E6%BC%8F/
