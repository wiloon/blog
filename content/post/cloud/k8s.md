---
title: "k8s"
author: "-"
date: "2026-04-10T21:39:51+08:00"
lastmod: "2026-06-23T12:32:58+08:00"
url: k8s
categories:
  - Cloud
tags:
  - AI-assisted
  - k8s
  - remix
---
## k8s

## pod

Pod 是 Kubernetes 中可部署的最小、最基本对象。一个 Pod 代表集群中正在运行的单个进程实例。  
Pod 包含一个或多个容器, 当 Pod 运行多个容器时，这些容器将作为一个实体进行管理并共用 Pod 的资源。

Pod 还包含其容器的共享网络和存储资源：

网络：系统会自动为 Pod 分配独一无二的 IP 地址。各 Pod 容器共用同一网络命名空间，包括 IP 地址和网络端口。Pod 中的各容器在 Pod 内通过 localhost 彼此通信。
存储：Pod 可以指定一组可在各容器之间共用的共享存储卷。持久化通常通过 PVC 挂载；访问模式 **RWO**（ReadWriteOnce）表示同一时刻只有一个节点可读写挂载，与 Longhorn 副本数、Deployment 滚动更新策略有关，详见 [PVC 访问模式：RWO 简介](./pvc-access-modes.md)。
可以将 Pod 视为一个自成一体的独立“逻辑主机”，其中包含该 Pod 所服务于的应用的系统需求。

## Secret

Secret 用于存放敏感数据（密码、Token、TLS 证书、私有镜像仓库凭证等），用法与 ConfigMap 类似，但语义上表示不应明文写在 Pod YAML 里。

与 ConfigMap 的区别：值在 etcd 中以 **base64** 存储，默认**不加密**；有权限的用户仍可通过 `kubectl get secret -o yaml` 查看。生产环境应配合 RBAC、etcd 加密或外部密钥方案（如 Sealed Secrets）。

常见类型：

| type                             | 用途                                  |
| -------------------------------- | ------------------------------------- |
| `Opaque`（默认）                 | 任意键值，如数据库密码                |
| `kubernetes.io/dockerconfigjson` | 私有镜像拉取（`imagePullSecrets`）    |
| `kubernetes.io/tls`              | TLS 证书（Ingress、`tls.secretName`） |

定义示例（`stringData` 写明文，API 自动转 base64）：

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
type: Opaque
stringData:
  password: "xxx"
```

Pod 引用方式：

- **环境变量**：`secretKeyRef` 或 `envFrom.secretRef`
- **挂载文件**：`volumes.secret.secretName`，每个 key 对应一个文件
- **拉镜像**：`spec.imagePullSecrets` 引用 docker 类型 Secret

修改 Secret 后，以环境变量注入的 Pod 通常需**重启**才生效；以卷挂载的会由 kubelet 周期性同步。

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

### NodePort vs hostPort

`NodePort`（Service 类型）和 `hostPort`（Pod 字段）都能让集群外部访问到 Pod，但机制完全不同。

**NodePort**：在 **Service** 层实现，由 kube-proxy 在**所有节点**上监听指定端口，流量转发到匹配的 Pod。

```yaml
apiVersion: v1
kind: Service
spec:
  type: NodePort
  ports:
    - port: 3100
      targetPort: 3100
      nodePort: 35140   # 任意节点的 35140 端口都可访问
      protocol: UDP
```

**hostPort**：在 **Pod** 层实现，把容器端口直接绑到 Pod **所在节点**的端口，不经过 kube-proxy。

```yaml
# Pod spec 里的 containers[].ports[]
containers:
  - name: alloy
    ports:
      - containerPort: 5140
        hostPort: 5140      # 只有这个 Pod 所在的那个节点的 5140 端口可访问
        protocol: UDP
```

**主要差异**：

| 对比项            | NodePort              | hostPort                      |
| ----------------- | --------------------- | ----------------------------- |
| 实现层            | Service（kube-proxy） | Pod 直接绑定宿主机端口        |
| 哪些节点可访问    | **所有**节点          | 仅 Pod **所在节点**           |
| 需要 nodeSelector | 否                    | **是**（否则不知道 Pod 在哪） |
| 端口范围          | 30000–32767（默认）   | 任意端口                      |
| UDP 兼容性        | 根据 CNI 而定         | 通常无问题                    |
| 节点故障影响      | 自动切换到其他节点    | Pod 随节点故障而不可访问      |

**何时用 hostPort**：

- 需要监听**特定小端口**（如 `514`），NodePort 默认只能用 30000+
- CNI 对 UDP NodePort 支持不确定时，hostPort 更可靠
- 简单场景，只有一个 Pod 需要对外暴露

**何时用 NodePort**：

- 不想将 Pod 锁定到某个节点，希望任意节点都可接流
- 配合 VIP（如 keepalived）使用，外部设备填 VIP 即可

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

## Descheduler

默认调度器只在 Pod **创建时**选节点，不会因为某节点变忙而把已有 Pod 迁走。若集群长期出现「个别 worker 堆很多 Pod、其他节点很空」，可部署 [Descheduler](./kubernetes-descheduler.md)：周期性按策略驱逐部分 Pod，由调度器重新分配到更合适的节点。它与 `drain` 互补——`drain` 用于维护窗口的一次性清空，Descheduler 用于日常负载重平衡。homelab 一次从 Grafana 发现 k8s-50 高负载到 Descheduler 真正见效的排查记录见 [Homelab K8s Node Rebalance 案例](./homelab-k8s-node-rebalance.md)。

## DaemonSet

DaemonSet 确保集群中每个（或部分符合条件的）节点上都运行一个 Pod 副本。当有新节点加入集群时，DaemonSet 会自动在该节点上创建 Pod；当节点被移除时，对应的 Pod 也会被回收。

### 典型使用场景

- **日志采集**：在每个节点上运行日志收集 Agent，如 Fluentd、Filebeat
- **监控指标**：在每个节点上运行节点监控 Agent，如 Prometheus Node Exporter、Datadog Agent
- **网络插件**：CNI 网络插件（如 Calico、Flannel）通常以 DaemonSet 形式部署
- **存储插件**：分布式存储的节点 Agent，如 Ceph、GlusterFS

### DaemonSet 与 Deployment 的区别

| 特性     | DaemonSet            | Deployment        |
| -------- | -------------------- | ----------------- |
| 副本数   | 每个节点一个（自动） | 手动指定 replicas |
| 调度方式 | 绑定到节点           | 由调度器自由分配  |
| 适用场景 | 节点级基础服务       | 无状态应用        |

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

| 控制器                 | 负责管理的资源                |
| ---------------------- | ----------------------------- |
| Deployment Controller  | Deployment → ReplicaSet → Pod |
| StatefulSet Controller | StatefulSet → Pod             |
| DaemonSet Controller   | DaemonSet → Pod               |
| Job Controller         | Job → Pod                     |
| Node Controller        | 监控节点健康状态              |

这些控制器都运行在 `kube-controller-manager` 进程中。

裸 Pod（Bare Pod）没有控制器，Pod 挂了没有任何东西会去重建它，所以生产环境中不推荐使用裸 Pod。

## CRD（CustomResourceDefinition）

CRD 是 Kubernetes 的**扩展机制**，允许向集群注册新的资源类型。注册后，就可以像操作内置资源（Pod、Deployment、Service）一样，用 `kubectl` 创建、查看、删除这些自定义资源。

### 为什么需要 CRD

Kubernetes 内置资源（Pod、Deployment、Service 等）描述的是通用计算单元，但很多应用有自己的概念，比如：

- Longhorn 的「Volume」「Replica」「Setting」
- ArgoCD 的「Application」「AppProject」
- Prometheus Operator 的「PrometheusRule」「ServiceMonitor」
- cert-manager 的「Certificate」「Issuer」

这些概念在标准 K8s 资源里没有对应物，CRD 让这些应用可以把自己的「业务对象」注册进 K8s API，用 K8s 统一的方式管理。

### CRD 与自定义资源

**CRD（CustomResourceDefinition）** 是类型定义，描述「这种资源叫什么、有哪些字段」；  
**CR（Custom Resource）** 是具体实例，是按 CRD 定义创建的一个对象。

类比：CRD 相当于 Go 里的 `struct` 定义，CR 是这个 struct 的一个值。

```bash
# 查看集群里注册了哪些 CRD
kubectl get crd

# Longhorn 的 CRD（部分）
kubectl get crd | grep longhorn
# volumes.longhorn.io
# replicas.longhorn.io
# settings.longhorn.io

# 操作 Longhorn Setting（CR）
kubectl get settings.longhorn.io -n longhorn-system
kubectl get settings.longhorn.io node-down-pod-deletion-policy -n longhorn-system

# ArgoCD Application 也是 CRD
kubectl get application -n argocd
```

### CRD 的生命周期

应用（如 Longhorn）安装时会一并创建 CRD；卸载时如果删除 CRD，所有对应的 CR 实例也会被级联删除。因此在 Helm 或 ArgoCD 管理的应用里，CRD 的处理往往需要格外谨慎：

- Helm：`skipCrds: true` 跳过 CRD 安装/更新（手动管理），`skipCrds: false` 由 chart 管理
- ArgoCD：通常用 `ignoreDifferences` 忽略 CRD 的 `.status` 字段，避免自动生成的 status 内容造成每次 sync 都显示 OutOfSync

## Operator 模式

Operator 是 CRD + 控制器的组合，是 Kubernetes 扩展的**标准模式**。

- **CRD**：定义应用的「业务对象」（如 `PostgreSQLCluster`）
- **控制器**：监听这些对象，执行对应的运维操作（创建 Pod、配置主从复制、触发备份等）

```
用户 kubectl apply PostgreSQLCluster CR
         ↓
控制器（Operator）检测到 CR 变化
         ↓
自动创建 StatefulSet、Service、ConfigMap
自动处理主从切换、备份、扩容...
```

常见 Operator：

| Operator | 管理对象 |
|----------|----------|
| Prometheus Operator | Prometheus、Alertmanager、告警规则 |
| cert-manager | TLS 证书自动申请/续期 |
| Longhorn | 分布式块存储 Volume、Replica、备份 |
| ArgoCD | GitOps 应用同步 |
| CloudNativePG | PostgreSQL 集群 |

Operator 把运维知识编码进控制器，实现「声明式运维」：用户只描述期望状态（如「我要一个 3 节点 PostgreSQL 集群」），Operator 负责把集群驱动到这个状态，并在故障时自动恢复。

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-18 | 新增 Descheduler 章节并链至独立文章 | 记录 Pod 重平衡与 homelab 调度实践 |
| 2026-06-23 | Descheduler 节增加 homelab-k8s-node-rebalance 案例链接 | 记录 k8s-50 高负载排查与治理全过程 |
