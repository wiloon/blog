---
title: kube-vip LoadBalancer 与节点 SSH 的 22 端口之争
author: "-"
date: 2026-06-26T12:19:51+08:00
lastmod: 2026-06-26T12:19:51+08:00
url: kube-vip-loadbalancer-port-22
categories:
  - cloud
tags:
  - k8s
  - kube-vip
  - loadbalancer
  - iptables
  - kube-proxy
  - externalTrafficPolicy
  - remix
  - AI-assisted
---

## 背景

homelab 的 K8s 集群用 kube-vip 把 VIP `192.168.50.100` 绑在某一台 control-plane 节点上，Kong 通过 `LoadBalancer` Service 占用了这个 VIP 的 443 端口对外提供 HTTPS。

最近想在集群里自建一个 Git 服务（Forgejo），它需要 SSH 端口供 `git clone` 使用。一个想法是：再建一个 `LoadBalancer` Service，把 VIP 的 **22** 端口转发给 Forgejo 的内建 SSH。

但这里有个让人犹豫的问题：

> VIP 是绑在某台宿主机上的，而那台宿主机自己的 `sshd` 也监听着 22 端口。那么发往 `192.168.50.100:22` 的流量，到底会进 Forgejo，还是会被宿主机的 `sshd` 接走？

## 先做个小实验

在集群上分三步验证，探测 `192.168.50.100:22` 返回的是什么。

第一步，**不创建任何 22 端口的 LoadBalancer Service**，直接探测 VIP 的 22 端口：

```bash
nc -w 2 192.168.50.100 22
# SSH-2.0-OpenSSH_10.3   ← 落到了宿主机的 sshd
```

第二步，建一个 `LoadBalancer` Service，把 VIP 的 22 端口指向一个普通的 HTTP 测试 Pod：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: lb-port22-test
spec:
  type: LoadBalancer
  loadBalancerIP: 192.168.50.100
  selector:
    app: nettest
  ports:
    - port: 22
      targetPort: 80
```

再探测同一个地址：

```bash
printf 'GET / HTTP/1.0\r\n\r\n' | nc -w 2 192.168.50.100 22
# HTTP/1.0 200 OK   ← 落到了 Service 后端的 Pod，不再是 sshd
```

第三步，删掉这个 Service，再探测：

```bash
nc -w 2 192.168.50.100 22
# SSH-2.0-OpenSSH_10.3   ← 又变回 sshd
```

结论很清楚：

| 状态 | `192.168.50.100:22` 落到哪 |
| ---- | -------------------------- |
| 无 22 端口的 LoadBalancer Service | 宿主机 `sshd` |
| 有 22 端口的 LoadBalancer Service | Service 后端 Pod |
| 删除该 Service 后 | 又回到宿主机 `sshd` |

也就是说，宿主机自己监听 22 的 `sshd` **会**抢到流量，但**只在没有对应 LoadBalancer Service 的时候**。

## 为什么 Service 一存在，sshd 就抢不到了

关键在于 Linux 内核网络栈的**处理顺序**：kube-proxy 装的 DNAT 规则，比 `sshd` 这种本机 socket「更早」拿到数据包。

一个目标为 `192.168.50.100:22` 的包，在持有 VIP 的那台宿主机里大致这样走：

```text
网卡收包
   │
   ▼
PREROUTING (nat 表)   ← kube-proxy 的 DNAT 规则在这里
   │
   ├─ 命中 Service (有 LB Service)：目标改写为 PodIP:targetPort
   │     │
   │     ▼  路由判定：目标不是本机地址
   │   FORWARD ──▶ 转发给 Pod   ✅ sshd 收不到
   │
   └─ 未命中 (无 LB Service)：目标仍是 VIP:22
         │
         ▼  路由判定：VIP 是本机地址
       INPUT ──▶ 本机 socket ──▶ sshd   ✅ sshd 收到
```

要点：

- `sshd` 监听在 `0.0.0.0:22`，它能收到的只有走到 **INPUT 链 → 本机 socket** 的包。
- kube-proxy 的 DNAT 发生在更早的 **PREROUTING（nat 表）**。一旦目标地址在这一步被改写成 `PodIP`，后续路由判定就认为「这个包不是发给我本机的」，于是走 **FORWARD** 转发出去，根本不进 INPUT，`sshd` 自然碰不到。

所以这不是「谁先抢到端口」，而是内核流水线的固定顺序决定的：

```text
PREROUTING(DNAT) ──▶ 路由决策 ──▶ INPUT(本机) / FORWARD(转发)
       ▲                              ▲
  kube-proxy 在这里               sshd 在这里
  （永远更早）                    （永远更晚）
```

只要 22 端口的 LoadBalancer Service 存在，发往 `VIP:22` 的包就一定在到达 `sshd` 之前被改道。这跟 Kong 用同一个 VIP 占着 443 是完全一样的机制——443 的包也是在 PREROUTING 就被 DNAT 到 Kong 的 Pod，宿主机上即便有别的程序想监听 443，也收不到这些包。

## 一个需要记住的边界情况

唯一会让 `sshd` 抢到 `VIP:22` 的情况，是 **DNAT 规则不存在**：Service 还没创建、被删除，或者 kube-proxy 异常。这时 `VIP:22` 会落回宿主机 `sshd`。

但要注意区分两条路径：

- 平时 **SSH 登录节点**用的是**节点自己的 IP**（例如 `192.168.50.38:22`），这条路径永远直达该节点的 `sshd`，不受任何 LoadBalancer Service 影响。
- 只有走 **VIP `192.168.50.100:22`** 这一条路径，才会被 22 端口的 LoadBalancer Service 接管。

两者互不干扰，这也是为什么「用 VIP 的 22 端口暴露集群内 SSH 服务」在这套架构下是可行且安全的：它不会影响你 SSH 登录宿主机本身。

## externalTrafficPolicy：Cluster 还是 Local

确定了 VIP 的 22 端口可以安全地交给 LoadBalancer Service 之后，还有一个 Service 字段需要决策：`externalTrafficPolicy`。它决定**从集群外进来的流量到达节点后，如何被转发到后端 Pod**，有两个取值。

| 值 | 转发行为 | 客户端源 IP |
| ---- | -------- | ----------- |
| `Cluster`（默认） | 入口节点收到包后，由 kube-proxy 再转发到**任意**节点上的 Pod | 经过 SNAT，Pod 看到的是节点 IP，**真实源 IP 丢失** |
| `Local` | 只转发给**本节点上**的 Pod；本节点没有 Pod 就丢弃连接 | **保留**客户端真实源 IP |

这个取舍在 kube-vip 这种「VIP 固定在某台节点」的场景里尤其要注意。VIP 绑在某台 control-plane 上，而业务 Pod（如上面的 Git 服务）通常调度在 worker 节点：

```text
客户端 ──▶ VIP:22（绑在 control-plane）
              │
              ├─ Cluster：kube-proxy 转发到 worker 上的 Pod   ✅ 能通，但源 IP 被 SNAT
              │
              └─ Local：只找 control-plane 本机的 Pod
                        本机没有 Pod ──▶ 连接被丢弃         ❌ 不通
```

也就是说，**如果 Pod 和 VIP 不在同一个节点，`Local` 会直接导致连不上**。要用 `Local` 保留源 IP，就必须把 Pod 用 `nodeSelector` 钉到持有 VIP 的那台节点，这又牺牲了调度灵活性。

### 源 IP 丢失有什么实际影响

`Cluster` 模式下源 IP 被 SNAT 掉，听起来像个缺点，但要看场景：

- **内网私有服务**（如自建 Git）：审计追责靠的是账号 + SSH key，不是 IP；也没有按 IP 做限流、封禁、白名单的需求。源 IP 是否真实**基本没有影响**。
- **对公网开放的服务**：需要靠源 IP 做风控、限流、`fail2ban` 封爆破、合规审计时，源 IP 才重要。

而且 `Cluster` 下所有客户端的源 IP 都被改写成同一个节点 IP，反而会让 `fail2ban` 这类按 IP 封禁的工具「一封封一片」，内网场景不开更省心。

### 结论

对内网、VIP 固定在某节点、Pod 在别处调度的场景，优先选 **`Cluster`**：保证「Pod 和 VIP 不在同节点也能连通」，代价（源 IP 丢失）在内网无实际影响。只有当确实需要真实源 IP，且愿意把 Pod 钉到 VIP 所在节点时，才考虑 `Local`。

## 小结

- VIP 绑在宿主机上，宿主机的 `sshd` 确实也监听 22，但 kube-proxy 的 DNAT 在 PREROUTING 阶段先改写目标地址，本机 `sshd` 在 INPUT 阶段才有机会接收，因此 LoadBalancer Service 一旦存在就会「截胡」。
- 同一个 VIP 上不同端口可以分给不同服务（443 给 Kong、22 给 Git 服务），靠端口区分，互不冲突。
- 真正的风险点不是端口冲突，而是 Service / kube-proxy 缺失时 `VIP:22` 会回落到宿主机 `sshd`；而用节点自身 IP 登录始终不受影响。
- VIP 固定在某节点、Pod 在别处时，`externalTrafficPolicy` 选 `Cluster` 才能保证连通；`Local` 虽保留源 IP，但要求 Pod 与 VIP 同节点。内网场景源 IP 无实际用途，`Cluster` 是更省心的默认选择。
