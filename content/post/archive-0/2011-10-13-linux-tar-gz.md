---
title: cgroup， namespace
author: "-"
date: 2011-10-13T08:11:53+00:00
url: cgroup
categories:
  - Linux

---
## cgroup， namespace
cgroup 的主要作用：管理资源的分配、限制；
namespace 的主要作用：封装抽象，限制，隔离，使命名空间内的进程看起来拥有他们自己的全局资源；

### Chroot
Chroot 可以将进程及其子进程与操作系统的其余部分隔离开来。但是，对于 root process ，却可以任意退出 chroot。

### 现代化容器技术带来的优势
- 轻量级，基于 Linux 内核所提供的 cgroup 和 namespace 能力，创建容器的成本很低；
- 一定的隔离性；
- 标准化，通过使用容器镜像的方式进行应用程序的打包和分发，可以屏蔽掉因为环境不一致带来的诸多问题；
- DevOps 支撑（可以在不同环境，如开发、测试和生产等环境之间轻松迁移应用，同时还可保留应用的全部功能）；

### cgroup
cgroup 是 Linux 内核的一个功能，用来限制、控制与分离一个进程组的资源（如CPU、内存、磁盘输入输出等）。它是由 Google 的两位工程师进行开发的，自 2018 年 1 月正式发布的 Linux 内核 v2.6.24 开始提供此能力。

cgroup 主要限制的资源是：
- CPU
- 内存
- 网络
- 磁盘 I/O

### 一篇搞懂容器技术的基石： cgroup -- 张晋涛
采用《署名-非商业性使用-禁止演绎 4.0 国际》许可协议
>https://segmentfault.com/a/1190000040980305


