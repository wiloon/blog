---
title: Podman, Buildah, Skopeo
author: "-"
date: 2020-01-18T09:16:23+00:00
url: /?p=15386
categories:
  - Uncategorized

tags:
  - reprint
---
## Podman, Buildah, Skopeo
### podman
Podman是该工具套件的核心，用来替换Docker中了大多数子命令 (RUN，PUSH，PULL等) 。Podman无需守护进程，使用用户命名空间来模拟容器中的root，无需连接到具有root权限的 socket 保证容器的体系安全。
  
Podman专注于维护和修改OCI镜像的所有命令和功能，例如拉动和标记。它还允许我们创建，运行和维护从这些镜像创建的容器。

目前有很多可用的容器引擎，不过 Docker 最突出的竞争对手是由 Red Hat 开发的 Podman。与 Docker 不同，Podman 不需要守护进程，也不需要 root 特权，这是 Docker 长期以来一直存在的问题。从它的名字就可以看出来，Podman 不仅可以运行容器，还可以运行 Pod。Pod 是 Kubernetes 的最小计算单元，由一个或多个容器(主容器和所谓的边车)组成，Podman 用户在以后可以更容易地将他们的工作负载迁移到 Kubernetes。


### Buildah
Buildah是套件中的Build工具，用来构建OCI镜像。虽然Podman也可以用户构建Docker镜像，但是构建速度超慢，并且默认情况下使用vfs存储驱动程序会消耗大量磁盘空间。 而buildah bud (使用Dockerfile构建) 非常快，并使用覆盖存储驱动程序，可以节约大量的空间。

Buildah (https://buildah.io) 。Buildah 是 Red Hat 开发的一款工具，可以很好地与 Podman 配合使用。如果你已经安装了 Podman，可能会注意到 podman build 子命令，它实际上是经过包装的 Buildah。


### Skopeo
Skopeo是套件中镜像管理工具，允许我们通过推，拉和复制镜像来处理Docker和OC镜像。

https://zhuanlan.zhihu.com/p/77373246



除了 Docker 和 Podman 之外，还有其他容器引擎，但我认为它们没有出路或者都不适合用于本地开发。不过如果你想要对容器引擎有一个较为完整的了解，我们可以列出一些: 
LXD——是 LXC (Linux 容器)的容器管理器(守护进程)。这个工具提供了运行系统容器的能力，这些系统容器提供了类似于 VM 的容器环境。它比较小众，没有很多用户，所以除非你有特定的用例，否则最好使用 Docker 或 Podman。
CRI-O——如果你在网上搜索 cri-o 是什么东西，你可能会发现它被描述为一种容器引擎。不过，它实际上是一种容器运行时。除了不是容器引擎之外，它也不适合用于“一般”的情况。我的意思是，它是专门为 Kubernetes 运行时(CRI)而构建的，并不是给最终用户使用的。
rkt——rkt(“rocket”)是由 CoreOS 开发的容器引擎。这里提到这个项目只是为了清单的完整性，因为这个项目已经结束了，它的开发也停止了——因此它不应该再被使用。


是时候跟Docker说再见了
原文链接:  https://www.infoq.cn/article/pzvqukmvk5fh9elhipgb


unc 的另一种替代品是 crun (https://github.com/containers/crun) 。这是 Red Hat 开发的一款工具，完全用 C 语言开发(runc 是用 Go 开发的)，所以它比 runc 更快，内存效率更高。因为它也是兼容 OCI 的运行时，所以你应该可以很容易上手。尽管它现在还不是很流行，但作为 RHEL 8.3 版本的技术预览，它将作为一个可选的 OCI 运行时，又因为它是 Red Hat 的产品，它可能最终会成为 Podman 或 CRI-O 的默认配置。

