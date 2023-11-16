---
title: "k8s"
author: "-"
date: ""
url: k8s
categories:
  - K8S
tags:
  - K8S
  - "reprint"
  - "remix"
---
## k8s

## pod

Pod 是 Kubernetes 中可部署的最小、最基本对象。一个 Pod 代表集群中正在运行的单个进程实例。  
Pod 包含一个或多个容器, 当 Pod 运行多个容器时，这些容器将作为一个实体进行管理并共用 Pod 的资源。

Pod 还包含其容器的共享网络和存储资源：

网络：系统会自动为 Pod 分配独一无二的 IP 地址。各 Pod 容器共用同一网络命名空间，包括 IP 地址和网络端口。Pod 中的各容器在 Pod 内通过 localhost 彼此通信。
存储：Pod 可以指定一组可在各容器之间共用的共享存储卷。
可以将 Pod 视为一个自成一体的独立“逻辑主机”，其中包含该 Pod 所服务于的应用的系统需求。

## K8s Service

Service服务可以为一组具有相同功能的容器应用提供一个统一的入口地址。

Pod在摧毁重建时ip地址是会动态变化的，这样通过客户端直接访问不合适了，这时候就可以选择使用服务来和Pod建立连接，通过标签选择器进行适配。这样就能有效的解决了Pod ip地址动态变换的问题了。

K8s Service有四种类型

- Service
- Headless Service
- NodePort Service
- LoadBalancer Service

### headless service

为什么需要无头服务？
客户端想要和指定的的Pod直接通信
并不是随机选择
开发人员希望自己控制负载均衡的策略，不使用Service提供的默认的负载均衡的功能，或者应用程序希望知道属于同组服务的其它实例。
Headless Service使用场景
有状态应用，例如数据库

例如主节点可以对数据库进行读写操作，而其它的两个工作节点只能读，在这里客户端就没必要指定pod服务的集群地址，直接指定数据库Pod ip地址即可，这里需要绑定dns，客户端访问dns，dns会自动返回pod IP地址列表

无头服务不需要指定集群地址
无头服务适用有状态应用例如数据库
无头服务dns查询会返回pod列表，开发人员可以自定义负载均衡策略
普通Service可以通过负载均衡路由到不同的容器应用

————————————————
版权声明：本文为CSDN博主「独步秋风」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：[https://blog.csdn.net/qq_33326449/article/details/117401847](https://blog.csdn.net/qq_33326449/article/details/117401847)
