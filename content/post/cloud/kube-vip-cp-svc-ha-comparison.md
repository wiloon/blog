---
title: kube-vip 的 cp/svc 双选举，与 keepalived+haproxy、MetalLB 的对比
author: "-"
date: 2026-08-12T08:00:00+08:00
lastmod: 2026-08-12T08:00:00+08:00
url: kube-vip-cp-svc-ha-comparison
categories:
  - cloud
tags:
  - k8s
  - kube-vip
  - keepalived
  - haproxy
  - metallb
  - ha
  - loadbalancer
  - remix
  - AI-assisted
---

## 背景

homelab 的 K8s 集群用同一个 kube-vip DaemonSet 同时做两件事：

- `cp_enable: "true"` —— 维护 **API Server** 的高可用 VIP，`kubectl`/kubeconfig 都走这个地址
- `svc_enable: "true"` —— 维护 **Kong LoadBalancer Service** 的入口 VIP，Ingress 流量走这个地址

两者目前共用同一个地址 `192.168.50.100`（详见 [Homelab 拓扑](./homelab-topology.md)）。最近一次 kube-vip 版本升级（`v0.8.0` → `v1.2.3`）和一次 control-plane 节点重启，都观察到同一个 IP 同时出现在两台 control-plane 节点上的"双挂"现象。排查过程中把 kube-vip 这套机制，跟另外两个常见的同类方案——**keepalived+haproxy**、**MetalLB**——梳理对比了一下，记在这里。

## kube-vip 在这里做的是两件不相关的事

kube-vip 内部为 `cp` 和 `svc` 各维护一把**完全独立**的 K8s Lease，靠 leader election 选出 winner，winner 在本机网卡上做 ARP 广播占用 VIP：

| Lease | 选的是谁 | 对应哪个开关 |
| ----- | -------- | ------------ |
| `plndr-cp-lock` | 谁提供 API Server（`:6443`） | `cp_enable` |
| `plndr-svcs-lock` | 谁提供 Kong 的 LoadBalancer Service 入口（`:80`/`:443`） | `svc_enable` |

两把锁互不知道对方存在，也不能互相替代——关掉其中一个，另一个照常运行，只是对应的能力消失（比如关掉 `svc_enable`，Kong 就没有 VIP 了，得换 NodePort 之类的方式暴露）。

**双挂的根因，不是"锁多余"，而是"两次独立选举被配置成盯着同一个地址"**：`daemonset.yaml` 里只有一个 `address: 192.168.50.100`，两套选举各自独立开票，开到同一个节点就只有 1 台有 VIP（正常态），开到不同节点就双挂（发生过两次：一次是批量改网关重启节点，一次是这次单独重启 k8s-67）。

## 三种方案的选型对比

homelab 场景下，"给裸机 K8s 集群一个稳定的对外/对内入口地址"这个问题，社区里常见的做法大致是这三类：

| | kube-vip（当前用的） | keepalived + haproxy | MetalLB |
| --- | --- | --- | --- |
| 解决的问题 | API Server VIP + LoadBalancer Service VIP，二合一 | 主要是 API Server VIP（也可扩展给别的 TCP 服务） | 专注 LoadBalancer Service VIP |
| 选主机制 | K8s Lease（也支持 etcd） | VRRP（独立协议，不依赖 apiserver） | K8s Lease（L2 模式）/ BGP（BGP 模式） |
| 流量模式 | active-passive（同一时刻只有 1 个节点真正处理流量） | active-passive 的 VIP + haproxy **真正负载均衡**到全部后端 | L2 模式 active-passive；BGP 模式可 ECMP 多节点分流 |
| 依赖组件 | 1 个（自己） | 2 个（keepalived 管 VIP，haproxy 管转发） | 1 个（L2 模式）；BGP 模式需路由器支持 BGP |
| 与 K8s 集成程度 | 原生（Pod 形态，读 Lease/Service） | 外部方案，K8s 感知不到 | 原生（Pod 形态，专门监听 Service） |
| 典型定位 | 轻量、一体化，kubeadm/k3s 裸机部署常用 | 更老牌、更"教科书"的高可用组合 | 裸机 LoadBalancer Service 的事实标准 |

## API Server 域：kube-vip vs keepalived+haproxy

kube-vip 的 `cp_enable`（ARP + K8s Lease 模式）是 **active-passive**：3 台 apiserver 都健康，但同一时刻只有 1 台真正被外部访问，另外 2 台空转等着接班。而且选主本身要靠 apiserver 可达才能更新 Lease，理论上存在"apiserver 全挂时没人能选出新 leader"的先有鸡先有蛋问题（kube-vip 用 `hostAliases` 把 `kubernetes` 短名指到 `127.0.0.1` 缓解，但没有从根上解决）。

keepalived + haproxy 是更传统的组合：

- **keepalived** 用 VRRP 协议做 VIP 故障转移，不依赖 K8s API，即使 apiserver 集体不健康也能完成 VIP 切换
- **haproxy** 同时往 3 台 apiserver 做**真正的负载均衡**并带健康检查，请求会分散到所有健康的后端，而不是"1 台干活、2 台陪跑"

代价是要多维护一套 haproxy 配置，且它是外部方案，K8s 完全感知不到这层，出问题时排查要多看一个组件。kubeadm 官方高可用文档长期把这个组合列为标准方案之一。

## Kong LoadBalancer 域：kube-vip vs MetalLB

社区里给裸机 K8s 提供 `LoadBalancer` 类型 Service 最主流的方案其实是 **MetalLB**，不是 kube-vip 的 `svc_enable`。但要澄清一点：MetalLB 的 **L2 模式**和 kube-vip 的 ARP 模式，机制几乎一样——都是 K8s Lease 选主 + 单节点 ARP 广播，同样是 active-passive，同样存在"选主落在不同节点导致抖动"的理论风险。所以从 MetalLB 换过来，不会带来架构上的本质提升，只是换了个生态更大、更专注这一个问题的实现。

MetalLB 真正的优势在 **BGP 模式**：如果路由器支持 BGP，可以做到多节点 ECMP 真负载均衡，而不是被动等故障转移——这一档能力 kube-vip 的 BGP 模式其实也有，只是配置和生态成熟度不如 MetalLB。

还有一种更"去中间件化"的思路：让 Kong 以 DaemonSet + hostNetwork 跑在多个节点上，在网关/路由器层面（比如 homelab 用的 OPNsense）直接做一层简单的 L4 负载均衡，指向所有跑 Kong 的节点 IP——彻底不需要在集群内部做任何选主，把 HA 完全交给网关设备，链路最短，但要求网关有这个能力。

## 小结

kube-vip 现在这套用法，本质是"一个工具、一套机制（Lease + ARP），复用去覆盖两个不同问题"，这也是双挂现象的根源——不是工具选错了，是同一个地址被两次独立选举共用了。更对症的修复方向是把两个角色拆成两个不同的 IP，而不是换成 keepalived+haproxy 或 MetalLB：换工具不解决"共用一个地址"这个具体触发条件，只是换了个同样是 active-passive 的实现。

如果之后追求"apiserver 真负载均衡"或"LoadBalancer 真多节点分流"，keepalived+haproxy／MetalLB BGP 模式才是能带来本质提升的方向，但对 3-7 节点规模的 homelab 来说，目前 kube-vip 一体化方案的运维成本明显更低，双挂本身也只是**理论上的秒级抖动风险**，实测 API/Ingress 都没受影响。

## 与已有文章的关系

| 主题 | 看哪篇 |
| ---- | ------ |
| VIP 拓扑、物理机/PVE/K8s 节点关系 | [Homelab 拓扑](./homelab-topology.md) |
| kube-vip VIP 与端口复用机制（22 端口之争） | [kube-vip LoadBalancer 与节点 SSH 的 22 端口之争](./kube-vip-loadbalancer-port-22.md) |
| K8s 概念（Pod/Service/DaemonSet 等） | [k8s](./k8s.md) |

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-08-12 | 新建本文，记录 kube-vip cp/svc 双选举机制、双挂根因，以及与 keepalived+haproxy、MetalLB 的对比 | kube-vip 升级到 v1.2.3 后又因重启节点触发了一次双挂，顺手把排查中梳理的方案对比沉淀下来 |
