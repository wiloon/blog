---
title: Podman, Buildah, Skopeo
author: "-"
type: post
date: 2020-01-18T09:16:23+00:00
url: /?p=15386
categories:
  - Uncategorized

---
Podman是该工具套件的核心，用来替换Docker中了大多数子命令（RUN，PUSH，PULL等）。Podman无需守护进程，使用用户命名空间来模拟容器中的root，无需连接到具有root权限的套接字保证容器的体系安全。
  
Podman专注于维护和修改OCI镜像的所有命令和功能，例如拉动和标记。它还允许我们创建，运行和维护从这些镜像创建的容器。

### Buildah
Buildah是套件中的Build工具，用来构建OCI镜像。虽然Podman也可以用户构建Docker镜像，但是构建速度超慢，并且默认情况下使用vfs存储驱动程序会消耗大量磁盘空间。 而buildah bud（使用Dockerfile构建）非常快，并使用覆盖存储驱动程序，可以节约大量的空间。
  
### Skopeo
Skopeo是套件中镜像管理工具，允许我们通过推，拉和复制镜像来处理Docker和OC镜像。

https://zhuanlan.zhihu.com/p/77373246