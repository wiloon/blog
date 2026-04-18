---
title: "k8s"
author: "-"
date: "2026-04-10T21:39:51+08:00"
url: k8s
categories:
  - Cloud
tags:
  - k8s
  - "reprint"
  - "remix"
  - "AI-assisted"
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

Service 服务可以为一组具有相同功能的容器应用提供一个统一的入口地址。
Service 是 k8s 用来定义和管理网络访问 Pod 的一种资源对象。不同类型的 Service 决定了应用服务的暴露方式和访问范围。

Pod 在摧毁重建时ip地址是会动态变化的，这样通过客户端直接访问不合适了，这时候就可以选择使用服务来和 Pod 建立连接，通过标签选择器进行适配。这样就能有效的解决了Pod ip地址动态变换的问题了。

K8s Service有四种类型

- ClusterIP （默认类型）
  - 只在集群内部可访问，外部无法直接访问。
  - 适合微服务之间的内部通信。
  - 示例：type: ClusterIP
- NodePort
  - 在每个节点(master node and worker node, all node)的指定端口开放服务，外部可以通过节点IP+端口访问服务。
  - 一般用于开发、测试，或与外部负载均衡器配合使用。
  - 示例：type: NodePort
- LoadBalancer Service
  - 集成云服务商的负载均衡器（如 AWS ELB、GCP LB），自动分配一个外部 IP，通过该 IP 访问服务。
  - 适合生产环境，需要公网访问的服务。
  - 示例：type: LoadBalancer
- ExternalName
  - 不真正暴露端口，而是把服务名解析为 DNS 名称（如外部数据库）。
  - 适合集群内服务直接访问集群外部服务（如通过 DNS 访问外部资源）。
  - 示例：type: ExternalName

### headless service

为什么需要无头服务？
客户端想要和指定的的 Pod 直接通信
并不是随机选择
开发人员希望自己控制负载均衡的策略，不使用 Service 提供的默认的负载均衡的功能，或者应用程序希望知道属于同组服务的其它实例。
Headless Service 使用场景
有状态应用，例如数据库

例如主节点可以对数据库进行读写操作，而其它的两个工作节点只能读，在这里客户端就没必要指定 pod 服务的集群地址，直接指定数据库 Pod ip 地址即可，这里需要绑定 dns，客户端访问 dns，dns 会自动返回 pod IP 地址列表

无头服务不需要指定集群地址
无头服务适用有状态应用例如数据库
无头服务 dns 查询会返回 pod 列表，开发人员可以自定义负载均衡策略
普通 Service 可以通过负载均衡路由到不同的容器应用

————————————————
版权声明：本文为CSDN博主「独步秋风」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：[https://blog.csdn.net/qq_33326449/article/details/117401847](https://blog.csdn.net/qq_33326449/article/details/117401847)

## cordon

`kubectl cordon` 将节点标记为不可调度（`SchedulingDisabled`），新的 Pod 不会被调度到该节点，但已运行的 Pod 不受影响。

常用场景：节点维护前，先 cordon 阻止新 Pod 调度，再用 `drain` 驱逐现有 Pod。

```bash
# 标记节点不可调度
kubectl cordon <node-name>

# 恢复调度
kubectl uncordon <node-name>

# 查看节点状态
kubectl get nodes
```

执行后节点状态会变为 `Ready,SchedulingDisabled`。

与 `drain` 的区别：

- `cordon`：只阻止新调度，不驱逐现有 Pod
- `drain`：先 cordon，再驱逐所有 Pod（用于节点下线或重启）

## drain

`kubectl drain` 用于安全地将一个节点上的所有 Pod 驱逐出去，通常在节点维护（如升级、重启）前使用。

执行流程：

1. 先对节点执行 `cordon`（标记为不可调度）
1. 然后逐个驱逐节点上的 Pod
1. Pod 会被调度到其他可用节点上重新创建

```bash
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data
```

### 常用参数

- `--ignore-daemonsets`：跳过 DaemonSet 管理的 Pod。DaemonSet 的 Pod 绑定到节点，无法迁移到其他节点。不加此参数时命令会报错中止。这是一种**显式确认**设计：强迫用户明确表示"我知道 DaemonSet Pod 不会被迁移，我接受这个结果"，避免用户误以为所有 Pod 都已安全迁移。
- `--delete-emptydir-data`：允许删除使用 `emptyDir` 存储的 Pod。`emptyDir` 是临时存储卷，数据存在节点本地，Pod 被删除时数据随之消失无法迁移。不加此参数时命令会报错中止，同样是显式确认机制，避免数据被静默删除。
- `--force`：强制驱逐没有控制器管理的裸 Pod（Bare Pod）。裸 Pod 是指直接用 `kubectl run` 或直接写 Pod YAML 创建、没有被 Deployment、StatefulSet、DaemonSet 等控制器管理的 Pod。驱逐后不会在其他节点重建，同样是显式确认机制。

维护完成后用 `kubectl uncordon <node-name>` 恢复节点调度。

## DaemonSet

DaemonSet 确保集群中每个（或部分符合条件的）节点上都运行一个 Pod 副本。当有新节点加入集群时，DaemonSet 会自动在该节点上创建 Pod；当节点被移除时，对应的 Pod 也会被回收。

### 典型使用场景

- **日志采集**：在每个节点上运行日志收集 Agent，如 Fluentd、Filebeat
- **监控指标**：在每个节点上运行节点监控 Agent，如 Prometheus Node Exporter、Datadog Agent
- **网络插件**：CNI 网络插件（如 Calico、Flannel）通常以 DaemonSet 形式部署
- **存储插件**：分布式存储的节点 Agent，如 Ceph、GlusterFS

### DaemonSet 与 Deployment 的区别

| 特性 | DaemonSet | Deployment |
|------|-----------|------------|
| 副本数 | 每个节点一个（自动） | 手动指定 replicas |
| 调度方式 | 绑定到节点 | 由调度器自由分配 |
| 适用场景 | 节点级基础服务 | 无状态应用 |

### 示例

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-exporter
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: node-exporter
  template:
    metadata:
      labels:
        app: node-exporter
    spec:
      containers:
        - name: node-exporter
          image: prom/node-exporter:latest
          ports:
            - containerPort: 9100
```

### 常用命令

```bash
# 查看 DaemonSet
kubectl get daemonset -n <namespace>

# 查看 DaemonSet 详情
kubectl describe daemonset <name> -n <namespace>

# 删除 DaemonSet
kubectl delete daemonset <name> -n <namespace>
```

### 节点选择

可以通过 `nodeSelector` 或 `nodeAffinity` 限制 DaemonSet 只在特定节点上运行：

```yaml
spec:
  template:
    spec:
      nodeSelector:
        kubernetes.io/os: linux
```

## 控制器（Controller）

控制器是 Kubernetes 中负责**持续监控资源状态，并驱使集群向期望状态靠拢**的组件。

核心思想是**控制循环（Control Loop）**：

```
观察当前状态 → 与期望状态对比 → 执行操作使二者一致
```

以 Deployment 为例：声明"我要 3 个副本"，Deployment 控制器持续监控，发现只有 2 个 Pod 在运行，就自动创建第 3 个 Pod。

常见的控制器：

| 控制器 | 负责管理的资源 |
|--------|--------------|
| Deployment Controller | Deployment → ReplicaSet → Pod |
| StatefulSet Controller | StatefulSet → Pod |
| DaemonSet Controller | DaemonSet → Pod |
| Job Controller | Job → Pod |
| Node Controller | 监控节点健康状态 |

这些控制器都运行在 `kube-controller-manager` 进程中。

裸 Pod（Bare Pod）没有控制器，Pod 挂了没有任何东西会去重建它，所以生产环境中不推荐使用裸 Pod。
