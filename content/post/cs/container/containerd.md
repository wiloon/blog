---
title: containerd, nerdctl
author: "-"
date: 2025-06-03 14:37:21
url: containerd
categories:
  - Container
tags:
  - reprint
  - remix
---
## containerd, nerdctl

## archlinux install containerd

```bash
# archlinux install containerd
pacman -S containerd runc nerdctl cni-plugins

# containerd config
sudo mkdir /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml

sudo systemctl daemon-reload

sudo systemctl enable --now containerd
# containerd 内存占用47MB
# containerd、runc、nerdctl 都是用户空间的程序, 不是内核模块，不需要重新加载内核, 不需要重启系统, 只需要运行守护进程即可, 安装完成就可以使用
sudo nerdctl pull hello-world
sudo nerdctl run --rm hello-world

# 如果需要编译镜像
pacman -S buildkit
sudo systemctl enable --now buildkit
nerdctl build -t foo:v1.0.0 .
```

```Bash
# cni plugin
mkdir -p /opt/cni/bin
tar Cxzvf /opt/cni/bin cni-plugins-linux-amd64-v1.1.1.tgz
```

## ubuntu install containerd

https://gist.github.com/Faheetah/4baf1e413691bc4e7784fad16d6275a9
https://www.techrepublic.com/article/install-containerd-ubuntu/

```Bash
# install runc
curl -LO https://github.com/opencontainers/runc/releases/download/v1.3.0/runc.amd64
sudo install -m 755 runc.amd64 /usr/local/sbin/runc

# 验证安装
runc --version

# install cni plugin
# 创建插件目录, 容器运行时默认期望插件在这个目录
sudo mkdir -p /opt/cni/bin

# 设置 cni 版本
VERSION="v1.7.1"

# 下载
curl -LO https://github.com/containernetworking/plugins/releases/download/${VERSION}/cni-plugins-linux-amd64-${VERSION}.tgz

# 解压到目标目录
sudo tar -C /opt/cni/bin -xzf cni-plugins-linux-amd64-${VERSION}.tgz

# 查看是否安装成功
ls /opt/cni/bin
# 确认 CNI 配置文件是否存在
ls /etc/cni/net.d/

# 查看 cni 版本
/opt/cni/bin/bridge --version
/opt/cni/bin/loopback --version

# install containerd
# apt 仓库里的包版本太旧， 2025-06-03 13:17:05， apt里的 containerd 1.7.27, 官网最新的 2.1.1
containerd_version="2.1.4"
curl -LO https://github.com/containerd/containerd/releases/download/v${containerd_version}/containerd-${containerd_version}-linux-amd64.tar.gz
sudo tar Cxzvf /usr/local containerd-${containerd_version}-linux-amd64.tar.gz

# containerd config
# 注意：containerd 从二进制包安装时不会自动创建 /etc/containerd/ 目录
# 原因：
# 1. containerd 可以使用内置默认配置运行（无需配置文件）
# 2. 不同使用场景可能需要不同的配置位置
# 3. 遵循最小化安装原则
# 但是强烈建议创建配置文件以便：
# - 持久化自定义配置（镜像加速、私有仓库等）
# - Kubernetes 集成需要（如 systemd cgroup）
# - 便于调试和维护
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml
# 如果用于 Kubernetes，建议启用 systemd cgroup：
# sudo sed -i 's/SystemdCgroup \= false/SystemdCgroup \= true/g' /etc/containerd/config.toml

# config systemd
sudo curl -L https://raw.githubusercontent.com/containerd/containerd/main/containerd.service -o /etc/systemd/system/containerd.service
sudo systemctl daemon-reload
sudo systemctl enable --now containerd

# 验证安装
containerd --version

# install nerdctl
# download latest version of nerdctl from https://github.com/containerd/nerdctl/releases
nerdctl_version="2.1.3"
curl -LO "https://github.com/containerd/nerdctl/releases/download/v${nerdctl_version}/nerdctl-${nerdctl_version}-linux-amd64.tar.gz"
sudo tar Cxzvf /usr/bin/ nerdctl-${nerdctl_version}-linux-amd64.tar.gz

# 验证安装
nerdctl --version
sudo nerdctl info

sudo nerdctl pull hello-world
sudo nerdctl run hello-world

# 使用 nerdctl 运行容器测试网络, 测试 CNI plugin
nerdctl run -it --rm busybox
# 在容器中执行
ping -c 2 baidu.com

# buildkit
# containerd 默认使用 buildkit
# download latest version of buildkit from https://github.com/moby/buildkit/releases
buildkit_version="0.23.2"
curl -LO "https://github.com/moby/buildkit/releases/download/v${buildkit_version}/buildkit-v${buildkit_version}.linux-amd64.tar.gz"
tar zxvf buildkit-v${buildkit_version}.linux-amd64.tar.gz
sudo mv bin/* /usr/local/bin/

# buildkit service
sudo curl -L https://raw.githubusercontent.com/moby/buildkit/refs/heads/master/examples/systemd/system/buildkit.service -o /etc/systemd/system/buildkit.service
# buildkit socket
sudo curl -L https://raw.githubusercontent.com/moby/buildkit/refs/heads/master/examples/systemd/system/buildkit.socket -o /etc/systemd/system/buildkit.socket

# edit buildkit.service, add --oci-worker=false --containerd-worker=true after buildkitd
# 禁用了本地 runc worker（oci-worker）
# 启用了 containerd worker
sudo vim /etc/systemd/system/buildkit.service

sudo systemctl daemon-reload
sudo systemctl enable --now buildkit
sudo systemctl status buildkit
sudo systemctl restart buildkit
```

## containerd

containerd 是一个行业标准的容器运行时，最初由 Docker 开发并后来捐赠给 Cloud Native Computing Foundation (CNCF)。它是一个守护进程，专门用来管理容器的完整生命周期，包括镜像传输和存储、容器执行和监督、低级存储和网络附件等。

### 主要特性

- **简单性**：专注于容器运行时的核心功能，API 简洁明了
- **稳定性**：作为生产级容器运行时，经过大规模部署验证
- **可移植性**：支持 Linux 和 Windows 平台
- **扩展性**：通过插件系统支持各种存储和网络解决方案

### 守护进程与容器隔离

containerd 确实也是一个**守护进程**，但它通过以下机制大大改善了 Docker 早期存在的守护进程单点故障问题：

#### containerd-shim 机制
- containerd 为每个容器启动一个独立的 **containerd-shim** 进程
- shim 作为容器的父进程，负责：
  - 保持容器的 stdio 和其他文件描述符打开
  - 向 containerd 报告容器的退出状态
  - 管理容器的生命周期（无需守护进程持续参与）

#### 关键优势
1. **容器独立性**：即使 containerd 守护进程崩溃或重启，**已运行的容器不会受影响**
2. **无守护进程依赖**：容器运行时不依赖守护进程持续存在，shim 接管容器生命周期
3. **平滑升级**：可以升级 containerd 而不影响正在运行的容器
4. **故障隔离**：单个容器的问题不会影响其他容器或守护进程

#### 对比 Docker 早期问题
- **Docker 早期**：所有容器都依赖 dockerd 守护进程，dockerd 崩溃会导致所有容器失控
- **containerd**：通过 shim 机制实现了容器与守护进程的解耦，大大提高了可靠性

#### 完全无守护进程的方案
如果需要完全无守护进程的容器运行时，可以考虑：
- **Podman**：无守护进程架构，容器作为用户进程的子进程运行
- **缺点**：某些高级功能（如网络管理）实现较复杂
- **在 Kubernetes 中**：Podman **不能直接**作为 Kubernetes 的 CRI 运行时使用，因为它本身不实现 CRI 接口。但可以通过 **CRI-O**（由 Podman 团队开发）在 K8s 中获得类似的无守护进程体验

### 与 Docker 的关系

containerd 是 Docker Engine 的核心组件之一。Docker 使用 containerd 来实际管理容器，而 Docker 本身提供了更高级的功能，如 Docker Compose、Docker Swarm 等。从 Docker 1.11 开始，Docker 将容器运行时功能拆分出来形成了 containerd。

### 在 Kubernetes 中的应用

Kubernetes 可以直接使用 containerd 作为容器运行时接口(CRI (Container Runtime Interface))，这样就不需要通过 Docker 这个中间层，从而提高了性能和稳定性。这也是为什么 Kubernetes 从 1.24 版本开始移除了对 dockershim 的支持，推荐使用 containerd。

## Kubernetes 支持的 CRI 运行时

除了 containerd，Kubernetes 还支持以下 CRI 运行时：

### 1. CRI-O
- **专门为 Kubernetes 设计**的轻量级容器运行时
- 由红帽(Red Hat)主导开发
- 严格遵循 Kubernetes CRI 和 OCI 标准
- 性能优异，资源占用少
- 适合生产环境，特别是 OpenShift 平台
- **注意**：CRI-O 仅设计用于 Kubernetes 环境，不适合独立使用（没有提供类似 docker/nerdctl 的命令行工具）

### 2. Docker Engine (通过 cri-dockerd)
- Kubernetes 1.24+ 移除了内置的 dockershim
- 需要使用 cri-dockerd 作为适配器
- cri-dockerd 是一个独立组件，提供 Docker Engine 的 CRI 接口
- 适合已有 Docker 基础设施的环境
- **独立使用**：✅ **完全可以**，Docker 本身就是独立的容器平台，提供完整的 CLI 工具（docker 命令）

### 3. Kata Containers
- 基于虚拟化的容器运行时
- 提供更强的安全隔离（每个容器运行在独立的轻量级虚拟机中）
- 适合多租户环境或对安全要求极高的场景
- 性能开销相对较高
- **独立使用**：⚠️ **理论可以，但不推荐**，Kata Containers 是作为低层运行时（OCI runtime），需要配合 containerd 或 CRI-O 等高层运行时使用

### 4. gVisor (runsc)
- Google 开发的容器沙箱运行时
- 提供应用层的系统调用拦截和模拟
- 增强安全性，限制容器对主机内核的访问
- 适合不信任的工作负载
- **独立使用**：⚠️ **理论可以，但不推荐**，gVisor 也是作为低层运行时（OCI runtime），通常需要配合 containerd 或 Docker 使用

### 5. Mirantis Container Runtime (原 Docker Enterprise)
- 企业级容器运行时
- 提供商业支持和额外的企业特性
- **独立使用**：✅ **可以**，本质上是 Docker 的企业版本，提供完整的独立使用能力

### CRI 运行时独立使用能力总结

| 运行时 | 能否脱离 K8s 使用 | 说明 |
|--------|------------------|------|
| **containerd** | ✅ 完全可以 | 通过 nerdctl 命令行工具，类似 docker 使用体验 |
| **CRI-O** | ❌ 不可以 | 专为 Kubernetes 设计，无独立使用的命令行工具 |
| **Docker Engine** | ✅ 完全可以 | 本身就是独立容器平台，docker 命令功能最丰富 |
| **Kata Containers** | ⚠️ 不推荐 | 是低层运行时，需要配合 containerd/Docker 使用 |
| **gVisor** | ⚠️ 不推荐 | 是低层运行时，需要配合 containerd/Docker 使用 |
| **Mirantis Runtime** | ✅ 可以 | Docker 企业版，具备完整独立使用能力 |

### 本地开发推荐

如果要在**本地开发环境**（非 Kubernetes）运行容器：

1. **Docker**：最成熟，生态最完善，功能最丰富
2. **containerd + nerdctl**：轻量级，性能好，与 K8s 生产环境一致
3. **Podman**：无守护进程，Rootless 容器，更安全

**不推荐**：CRI-O（仅用于 K8s）、Kata/gVisor（需要高层运行时配合）

### Podman 与 Kubernetes

**Podman 不能直接作为 Kubernetes 的 CRI 运行时使用**，原因如下：

1. **缺少 CRI 接口**：Podman 本身不实现 Kubernetes 的 CRI (Container Runtime Interface) 规范
2. **设计目标不同**：Podman 主要设计用于本地开发和单机环境，而非集群编排
3. **无守护进程架构**：虽然这是 Podman 的优势，但与 Kubernetes 期望的守护进程模式不兼容

#### 在 Kubernetes 中的替代方案

如果您喜欢 Podman 的无守护进程理念，可以在 Kubernetes 中使用：

- **CRI-O**：由 Podman 的开发团队（Red Hat）创建，专为 Kubernetes 设计
- CRI-O 和 Podman 共享很多底层代码和技术
- CRI-O 可以看作是 Podman 在 Kubernetes 环境中的"对应版本"

#### Podman 的使用场景

✅ **适合使用 Podman 的场景：**
- 本地开发和测试
- CI/CD 流水线中构建镜像
- 单机容器部署
- 需要 Rootless 容器（无需 root 权限）
- 替代 Docker Desktop

❌ **不适合使用 Podman 的场景：**
- 作为 Kubernetes 的容器运行时
- 需要 Kubernetes 编排的生产环境

### CRI 运行时选择建议

- **生产环境推荐**：containerd 或 CRI-O（性能好、稳定、社区活跃）
- **高安全需求**：Kata Containers 或 gVisor
- **已有 Docker 环境**：Docker Engine + cri-dockerd
- **OpenShift 平台**：CRI-O（默认选择）

### Kubernetes 运行时组合的主流选择

在 Kubernetes 生产环境中，最常见的运行时组合是：

#### 推荐组合（主流选择）

1. **containerd + runc**（最流行）
   - **高层运行时**：containerd
   - **低层运行时**：runc
   - 这是目前 Kubernetes 社区最推荐的配置
   - CNCF 官方支持，社区最活跃
   - 性能好，稳定性高

2. **CRI-O + runc**（Red Hat/OpenShift 首选）
   - **高层运行时**：CRI-O
   - **低层运行时**：runc
   - OpenShift 默认配置
   - 专为 Kubernetes 优化

**是的，runc 是 Kubernetes 环境中低层运行时的主流选择！**

几乎所有 Kubernetes 集群（无论使用 containerd 还是 CRI-O）默认都使用 **runc** 作为低层运行时。

#### 特殊需求的替代组合

- **高安全环境**：containerd/CRI-O + **gVisor (runsc)** 或 **Kata Containers**
- **性能优化**：containerd/CRI-O + **crun**（更快、更轻量）

#### 为什么 runc 是主流？

1. **成熟稳定**：经过大规模生产环境验证
2. **OCI 标准**：作为 OCI 运行时的标准参考实现
3. **广泛支持**：所有主流 CRI 运行时都默认支持
4. **社区活跃**：CNCF 项目，持续维护和更新
5. **兼容性好**：与各种容器镜像和应用完全兼容

## runc

runc 是一个**底层的容器运行时**，它是 OCI (Open Container Initiative) 运行时规范的标准实现。

### 什么是 runc

- **OCI 运行时规范实现**：runc 实现了 OCI 运行时规范，定义了如何运行容器
- **CLI 工具**：提供了命令行工具来生成和运行容器
- **轻量级**：专注于容器的创建和执行，没有镜像管理、网络等高级功能
- **低层操作**：直接与 Linux 内核交互，使用 namespace、cgroup 等技术隔离容器

### 在容器生态中的位置

容器运行时分为两个层次：

#### 高层运行时 (High-level Container Runtime)
- **containerd**、**CRI-O**、**Docker**
- 负责：镜像管理、镜像传输、镜像解压、存储管理、网络管理等
- 最终调用低层运行时来实际运行容器

#### 低层运行时 (Low-level Container Runtime)
- **runc**、**crun**、**kata-runtime**、**runsc (gVisor)**
- 负责：容器的实际创建和执行
- 直接与操作系统内核交互

### 工作流程

**在 Kubernetes 环境中的完整调用链：**

```
Kubernetes (kubelet)
    ↓ CRI 接口
containerd/CRI-O (高层运行时)
    ↓ 调用
containerd-shim
    ↓ 调用
runc (低层运行时)
    ↓ 创建
容器进程 (你的应用)
```

**是的，容器在 Kubernetes 中运行时也会使用 runc！**

无论您使用 containerd 还是 CRI-O 作为 Kubernetes 的 CRI 运行时，它们默认都会调用 **runc** 作为底层运行时来实际创建和运行容器。

#### Kubernetes 中的运行时层次

1. **Kubernetes 层**：kubelet 通过 CRI 接口与容器运行时通信
2. **高层运行时**：containerd 或 CRI-O 处理镜像、网络、存储等
3. **Shim 层**：containerd-shim 或 conmon (CRI-O) 管理容器生命周期
4. **低层运行时**：runc 实际创建容器进程
5. **内核层**：Linux namespace、cgroup 等实现隔离

#### 实际例子

当您在 Kubernetes 中运行一个 Pod 时：

```bash
kubectl run nginx --image=nginx
```

幕后发生的事情：
1. kubelet 接收到创建 Pod 的请求
2. kubelet 通过 CRI 接口调用 containerd/CRI-O
3. containerd/CRI-O 拉取镜像、准备存储和网络
4. containerd/CRI-O 启动 containerd-shim
5. **containerd-shim 调用 runc 创建容器**
6. runc 使用 Linux namespace 和 cgroup 创建隔离的容器进程
7. 您的 nginx 应用在容器中运行

#### 可以替换 runc 吗？

是的！在 Kubernetes 中也可以替换 runc：

- **使用 crun**：更快、更轻量（C 语言实现）
- **使用 kata-runtime**：基于 VM 的更强隔离
- **使用 gVisor (runsc)**：增强的安全沙箱

配置方法：在 containerd 或 CRI-O 的配置文件中指定使用不同的低层运行时。

### 主要功能

1. **创建容器**：根据 OCI 规范的配置文件创建容器
2. **启动容器**：启动容器中的进程
3. **生命周期管理**：暂停、恢复、停止、删除容器
4. **资源隔离**：使用 Linux namespace 和 cgroup 实现隔离

### 历史

- 最初由 Docker 公司开发
- 2015 年，Docker 将 runc 捐赠给 OCI，作为容器运行时的标准参考实现
- 现在几乎所有主流容器运行时（containerd、CRI-O、Podman）都使用 runc 作为默认的低层运行时

### runc 的替代品

- **crun**：用 C 语言编写，比 runc (Go 语言) 更快、资源占用更少
- **kata-runtime**：基于虚拟化的运行时，提供更强的隔离
- **runsc (gVisor)**：Google 的沙箱运行时，提供额外的安全层

### 为什么需要 runc

容器运行时的分层设计带来了诸多好处：

- **模块化**：高层运行时专注于管理功能，低层运行时专注于执行
- **标准化**：通过 OCI 规范，不同的高层运行时可以使用相同的低层运行时
- **可替换性**：可以根据需求替换不同的低层运行时（如 runc、crun、kata-runtime）
- **职责分离**：每个组件专注于自己的核心功能

## CNI（Container Network Interface）

CNI（Container Network Interface）是一套**容器网络的规范和插件系统**，用于配置 Linux 容器的网络接口。

### 什么是 CNI

- **网络接口规范**：定义了容器运行时如何调用网络插件来配置容器网络
- **插件架构**：通过可执行文件形式的插件实现具体的网络功能
- **CNCF 项目**：由 Cloud Native Computing Foundation 维护
- **标准化**：Kubernetes、containerd、CRI-O、Podman 等都支持 CNI

### CNI Plugins 是什么

**CNI Plugins** 是一组实现 CNI 规范的**可执行文件**，每个插件负责不同的网络功能。

#### 主要插件类型

**1. Main 插件（主网络插件）**
- **bridge**：创建网桥，将容器连接到网桥
- **ipvlan**：基于 Linux IPvlan 创建虚拟网络接口
- **macvlan**：基于 Linux Macvlan 创建虚拟网络接口
- **ptp**：创建点对点（veth pair）连接
- **host-device**：将已存在的设备移入容器

**2. IPAM 插件（IP 地址管理）**
- **dhcp**：通过 DHCP 服务器分配 IP 地址
- **host-local**：从预定义的地址池中分配 IP（最常用）
- **static**：分配静态 IP 地址

**3. Meta 插件（元插件，辅助功能）**
- **portmap**：配置端口映射（iptables 规则）
- **bandwidth**：限制网络带宽
- **firewall**：配置防火墙规则
- **tuning**：调整网络接口参数

### CNI 工作流程

当容器启动时，容器运行时会调用 CNI 插件：

```
容器运行时（containerd/CRI-O）
    ↓ 调用
CNI Plugin（如 bridge）
    ↓ 创建网络接口
    ↓ 调用 IPAM Plugin（如 host-local）
    ↓ 分配 IP 地址
    ↓ 配置路由
容器获得网络连接
```

### Kubernetes 中的 CNI

在 Kubernetes 中：
1. **kubelet** 通过 CNI 插件为 Pod 配置网络
2. 常用的 Kubernetes CNI 解决方案：
   - **Calico**：网络策略 + 路由
   - **Flannel**：简单的 overlay 网络
   - **Weave**：overlay 网络 + 网络策略
   - **Cilium**：基于 eBPF 的高级网络
   - **Canal**：Flannel + Calico 网络策略

### CNI Plugins 与 Calico、Flannel 的关系

#### 分层架构

CNI 生态系统采用**分层架构**：

```
┌──────────────────────────────────────────────┐
│   Kubernetes Network Solutions (高级方案)     │
│   Calico, Flannel, Weave, Cilium, etc.      │
│   - 跨节点网络                                │
│   - 网络策略                                  │
│   - 服务发现                                  │
└──────────────────────────────────────────────┘
                    ↓ 依赖/调用
┌──────────────────────────────────────────────┐
│   CNI Plugins (基础插件)                      │
│   bridge, host-local, portmap, loopback      │
│   - 本地网络接口创建                          │
│   - IP 地址分配                               │
│   - 端口映射                                  │
└──────────────────────────────────────────────┘
```

#### 关系类型

**1. CNI Plugins = 基础组件**
- CNI plugins（如 bridge, host-local）是**底层的网络配置工具**
- 只负责单机上的容器网络配置：
  - 创建 veth pair（虚拟网卡对）
  - 配置 Linux bridge
  - 分配 IP 地址
  - 设置路由表
- **无法解决跨节点通信**

**2. Calico/Flannel = 完整网络方案**
- 是**高级的 Kubernetes 网络解决方案**
- 内部**会调用基础的 CNI plugins**
- 额外提供：
  - **跨节点网络**：Pod 跨主机通信
  - **网络策略**：访问控制（Calico 提供，Flannel 不提供）
  - **路由管理**：BGP 路由（Calico）或 VXLAN 封装（Flannel）
  - **服务发现**：集成 kube-proxy

#### 具体示例

**Flannel 的工作方式**：

```
Flannel 在每个节点上：
1. 运行 flanneld 守护进程
2. 为每个节点分配子网（如 10.244.1.0/24）
3. 当 Pod 创建时，调用 CNI plugins：
   ├─ bridge plugin：创建 cni0 网桥
   ├─ host-local plugin：从 Flannel 分配的子网分配 IP
   └─ portmap plugin：配置端口映射
4. flanneld 负责跨节点通信：
   └─ 使用 VXLAN/UDP 封装数据包，实现跨节点 Pod 通信
```

**Calico 的工作方式**：

```
Calico 在每个节点上：
1. 运行 calico-node 守护进程（Felix + BIRD）
2. 当 Pod 创建时，调用 CNI plugins：
   ├─ calico plugin：创建虚拟网络接口
   ├─ host-local plugin：分配 IP 地址
   └─ portmap plugin：配置端口映射
3. Felix 负责：
   ├─ 路由规则配置（不使用 bridge，直接路由）
   ├─ 网络策略（iptables/eBPF 规则）
   └─ 与 BIRD 配合实现 BGP 路由
4. BIRD 负责：
   └─ 通过 BGP 协议在节点间交换路由信息
```

#### 对比总结

| 特性 | CNI Plugins | Flannel | Calico |
|------|-------------|---------|--------|
| **定位** | 基础工具 | 完整网络方案 | 完整网络方案 |
| **作用范围** | 单机容器网络 | 集群跨节点网络 | 集群跨节点网络 |
| **网络模式** | bridge/veth 创建 | VXLAN/UDP overlay | BGP 路由 |
| **网络策略** | ❌ | ❌ | ✅ |
| **IP 管理** | host-local IPAM | 子网分配 + host-local | IPAM 池 + host-local |
| **依赖关系** | 独立工具 | 调用 CNI plugins | 调用 CNI plugins |
| **复杂度** | 简单 | 中等 | 较高 |
| **性能** | - | 较低（封装开销） | 高（纯路由） |

#### 实际部署中的调用链

**Flannel 示例**：

```
Kubernetes 创建 Pod
    ↓
kubelet 调用 CRI（containerd）
    ↓
containerd 调用 CNI
    ↓
Flannel CNI plugin 执行：
    ├─ 调用 bridge plugin：创建网桥
    ├─ 调用 host-local plugin：分配 IP
    └─ 配置到 flanneld 的路由
    ↓
flanneld 处理跨节点通信
```

**Calico 示例**：

```
Kubernetes 创建 Pod
    ↓
kubelet 调用 CRI（containerd）
    ↓
containerd 调用 CNI
    ↓
Calico CNI plugin 执行：
    ├─ 创建 veth pair
    ├─ 调用 host-local plugin：分配 IP
    └─ 配置到 calico-node 的路由
    ↓
calico-node (Felix) 配置 iptables/路由
    ↓
BIRD 通过 BGP 同步路由信息
```

#### 为什么需要这种分层？

1. **职责分离**：
   - CNI plugins 专注于本地网络操作
   - 高级方案专注于集群级网络

2. **标准化**：
   - 所有方案都遵循 CNI 规范
   - 可以复用基础的 CNI plugins

3. **灵活性**：
   - 可以选择不同的高级网络方案
   - 底层 CNI plugins 保持一致

4. **可维护性**：
   - 基础组件稳定（CNI plugins）
   - 高级功能独立演进（Calico/Flannel）

#### 总结

**简单来说**：
- **CNI plugins** = 螺丝刀、扳手（基础工具）
- **Calico/Flannel** = 汽车装配线（完整解决方案，内部使用基础工具）

**关键点**：
1. Calico 和 Flannel **都依赖**基础的 CNI plugins
2. CNI plugins **无法独立**实现 Kubernetes 集群网络
3. 安装 Calico/Flannel 时，**仍需要**安装 CNI plugins
4. Calico/Flannel 是**更高层次**的网络抽象和管理方案

#### 与 containerd/runc 的类比

这种关系**完全类似于** containerd 与 runc 的关系：

**容器运行时分层**：
```
containerd (高层运行时)
    ↓ 调用
runc (低层运行时)
```

**网络运行时分层**：
```
Calico/Flannel (高级网络方案)
    ↓ 调用
CNI plugins (基础网络工具)
```

**对比表格**：

| 维度 | 容器运行时 | 网络实现 |
|------|-----------|---------|
| **高层组件** | containerd / CRI-O | Calico / Flannel |
| **低层组件** | runc / crun | CNI plugins (bridge, host-local) |
| **高层职责** | 镜像管理、存储管理、调度 | 跨节点通信、网络策略、路由管理 |
| **低层职责** | 容器进程创建、namespace/cgroup | 网络接口创建、IP 分配、路由配置 |
| **依赖关系** | containerd 调用 runc | Calico/Flannel 调用 CNI plugins |
| **独立性** | runc 无法独立管理容器生命周期 | CNI plugins 无法实现跨节点网络 |
| **标准化** | OCI Runtime Spec | CNI Specification |

**核心相似点**：

1. **分层抽象**：
   - containerd 处理高级功能，runc 处理底层执行
   - Calico/Flannel 处理集群网络，CNI plugins 处理本地网络

2. **职责分离**：
   - containerd 不直接创建容器，委托给 runc
   - Calico/Flannel 不直接配置网络接口，委托给 CNI plugins

3. **标准化接口**：
   - OCI 规范定义了 containerd 如何调用 runc
   - CNI 规范定义了 Calico/Flannel 如何调用 CNI plugins

4. **可替换性**：
   - runc 可以替换为 crun、kata-runtime
   - CNI plugins 可以被不同的高级方案复用

**形象比喻**：
- **containerd** : **runc** = **指挥官** : **士兵**（执行具体命令）
- **Calico/Flannel** : **CNI plugins** = **建筑设计师** : **泥瓦匠**（执行具体操作）

**关键理解**：
> 无论是容器运行时还是网络实现，都采用了**相同的分层设计模式**：
> - **高层组件**：提供完整的解决方案和高级功能
> - **低层组件**：提供基础的、原子化的操作能力
> - **标准接口**：通过规范（OCI/CNI）实现解耦和可替换性

这种设计模式在容器生态系统中非常常见，体现了**Unix 哲学**："做一件事，并做好它"。

### CNI 插件的职责

1. **网络接口创建**：为容器创建虚拟网络接口
2. **IP 地址分配**：为容器分配 IP 地址
3. **路由配置**：配置容器的网络路由
4. **网络清理**：容器删除时清理网络资源

### CNI 配置文件

CNI 配置通常存储在 `/etc/cni/net.d/` 目录下，格式为 JSON：

```json
{
  "cniVersion": "1.0.0",
  "name": "mynet",
  "type": "bridge",
  "bridge": "cni0",
  "isGateway": true,
  "ipMasq": true,
  "ipam": {
    "type": "host-local",
    "subnet": "10.244.0.0/16",
    "routes": [
      { "dst": "0.0.0.0/0" }
    ]
  }
}
```

### 安装 CNI Plugins

```bash
# 创建 CNI 插件目录
sudo mkdir -p /opt/cni/bin

# 下载并安装
VERSION="v1.7.1"
curl -LO https://github.com/containernetworking/plugins/releases/download/${VERSION}/cni-plugins-linux-amd64-${VERSION}.tgz
sudo tar -C /opt/cni/bin -xzf cni-plugins-linux-amd64-${VERSION}.tgz

# 查看安装的插件
ls /opt/cni/bin
# 输出：bridge  dhcp  firewall  host-device  host-local  ipvlan  loopback  
#      macvlan  portmap  ptp  sbr  static  tuning  vlan  vrf
```

### 为什么需要 CNI Plugins

1. **标准化**：统一的网络配置接口，支持多种容器运行时
2. **模块化**：不同插件负责不同功能，可以组合使用
3. **可扩展**：可以开发自定义 CNI 插件
4. **解耦**：容器运行时不需要内置网络功能

### 与容器运行时的关系

- **containerd**：依赖 CNI plugins 来配置容器网络
- **CRI-O**：使用 CNI plugins 为 Kubernetes Pod 配置网络
- **Docker**：有自己独特的网络实现历史

#### 单机环境 vs Kubernetes 集群环境

**重要区分**：CNI plugins 的使用场景取决于环境类型

**单机环境（本地开发/测试）**：

```bash
# 使用 nerdctl + containerd + runc 单机运行容器
# 只需要安装：
✅ containerd    # 高层运行时
✅ runc          # 低层运行时  
✅ CNI plugins   # 基础网络插件（bridge, host-local 等）
✅ nerdctl       # 命令行工具
❌ Calico        # 不需要（仅用于 Kubernetes 集群）
❌ Flannel       # 不需要（仅用于 Kubernetes 集群）
```

在单机环境下：
- CNI plugins 中的 **bridge** 插件创建本地网桥（如 `cni0`）
- **host-local** 插件从配置的子网分配 IP 地址
- 容器之间通过 bridge 在**同一台机器上**通信
- **无需跨节点网络**，因此不需要 Calico/Flannel

**Kubernetes 集群环境**：

```bash
# 在 K8s 集群中运行容器
# 需要安装：
✅ containerd/CRI-O  # 高层运行时
✅ runc              # 低层运行时
✅ CNI plugins       # 基础网络插件
✅ Calico/Flannel    # 集群网络方案（二选一）
```

在 Kubernetes 集群中：
- CNI plugins 仍然负责**本地网络配置**
- Calico/Flannel 负责**跨节点 Pod 通信**
- 两者**协同工作**，缺一不可

#### 实际安装示例对比

**单机环境安装（仅需 CNI plugins）**：

```bash
# Ubuntu/Debian
sudo mkdir -p /opt/cni/bin
VERSION="v1.7.1"
curl -LO https://github.com/containernetworking/plugins/releases/download/${VERSION}/cni-plugins-linux-amd64-${VERSION}.tgz
sudo tar -C /opt/cni/bin -xzf cni-plugins-linux-amd64-${VERSION}.tgz

# Arch Linux
pacman -S cni-plugins

# 这就够了！可以直接使用 nerdctl 运行容器
sudo nerdctl run -d nginx
```

**Kubernetes 集群安装（需要 CNI plugins + Calico）**：

```bash
# 1. 先安装 CNI plugins（基础组件）
sudo mkdir -p /opt/cni/bin
curl -LO https://github.com/containernetworking/plugins/releases/download/v1.7.1/cni-plugins-linux-amd64-v1.7.1.tgz
sudo tar -C /opt/cni/bin -xzf cni-plugins-linux-amd64-v1.7.1.tgz

# 2. 再安装 Calico（集群网络方案）
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml

# Calico 内部会调用 /opt/cni/bin/ 下的插件
```

#### 为什么单机不需要 Calico/Flannel？

1. **无跨节点需求**：
   - 单机环境中，所有容器在同一台机器上
   - 通过本地 bridge 就能互相通信
   - 不需要 Calico 的 BGP 路由或 Flannel 的 VXLAN 封装

2. **CNI plugins 足够**：
   - bridge 插件创建虚拟网桥
   - host-local 分配 IP 地址
   - portmap 配置端口映射
   - 这些功能对单机环境已经够用

3. **Calico/Flannel 的功能是多余的**：
   - 跨节点路由：单机没有多个节点
   - 网络策略：单机环境通常不需要
   - 分布式 IPAM：单机用 host-local 就够了

#### 网络配置文件示例

**单机环境的 CNI 配置** (`/etc/cni/net.d/10-mynet.conf`)：

```json
{
  "cniVersion": "1.0.0",
  "name": "mynet",
  "type": "bridge",
  "bridge": "cni0",
  "isGateway": true,
  "ipMasq": true,
  "ipam": {
    "type": "host-local",
    "subnet": "10.88.0.0/16",
    "routes": [
      { "dst": "0.0.0.0/0" }
    ]
  }
}
```

这个简单配置就能让单机容器正常联网！

#### 总结对比

| 特性 | 单机环境 | Kubernetes 集群 |
|------|---------|----------------|
| **CNI plugins** | ✅ 必需 | ✅ 必需 |
| **Calico/Flannel** | ❌ 不需要 | ✅ 必需 |
| **网络范围** | 单机本地 | 跨节点集群 |
| **网络复杂度** | 简单（bridge） | 复杂（BGP/VXLAN） |
| **典型用例** | 开发测试 | 生产集群 |

**关键理解**：
> - **单机用 containerd**：只装 CNI plugins 就够了
> - **Kubernetes 集群**：CNI plugins + Calico/Flannel 都要装
> - Calico/Flannel 是为**解决跨节点通信**而设计的，单机用不上

#### Docker 的网络实现历史

**Docker 早期（2013-2015）**
- Docker 自己内置实现网络功能
- 没有使用 CNI 规范（CNI 那时还不存在）
- 网络功能直接集成在 Docker daemon 中
- 支持 bridge、host、none 等基本网络模式

**Docker 1.7+（2015）引入 libnetwork**
- Docker 开发了自己的网络库：**libnetwork**
- libnetwork 实现了 Docker 的网络模型（Container Network Model - CNM）
- **与 CNI 是不同的规范**，两者互不兼容：
  - **CNM（Container Network Model）**：Docker 的网络模型
  - **CNI（Container Network Interface）**：Kubernetes/CNCF 的网络标准
- libnetwork 提供了更丰富的网络功能（overlay、macvlan 等）

**Docker 现状（2020+）**
- Docker 默认仍使用 libnetwork（不是 CNI）
- 但 Docker 20.10+ 可以通过配置支持 CNI plugins
- 在 Kubernetes 中使用 Docker 时，通过 dockershim/cri-dockerd 桥接到 CNI

#### CNM vs CNI 的区别

| 特性 | CNM (Docker) | CNI (Kubernetes/CNCF) |
|------|--------------|----------------------|
| **发起者** | Docker Inc. | CoreOS/CNCF |
| **设计理念** | 面向 Docker 生态 | 容器运行时无关 |
| **网络模型** | Sandbox-Endpoint-Network | 插件链式调用 |
| **使用者** | Docker、Docker Swarm | Kubernetes、containerd、CRI-O、Podman |
| **插件格式** | Go plugin/Remote driver | 独立可执行文件 |
| **标准化** | Docker 私有 | CNCF 开放标准 |

#### 为什么 Kubernetes 选择 CNI 而非 CNM？

1. **时间因素**：CNI 在 Kubernetes 早期就被采用
2. **简单性**：CNI 设计更简单，插件是独立可执行文件
3. **中立性**：CNCF 标准，不绑定特定厂商
4. **灵活性**：更容易集成和扩展
5. **社区支持**：CNCF 项目，社区驱动

#### Docker 网络实现的演变

```
Docker 早期（2013-2015）
    └─ 内置网络实现（bridge、host、none）

Docker 1.7+（2015-现在）
    └─ libnetwork (CNM 模型)
        ├─ bridge 驱动
        ├─ overlay 驱动
        ├─ macvlan 驱动
        └─ 其他第三方驱动

Docker 20.10+（可选）
    └─ 可配置使用 CNI plugins
```

#### 实际影响

- **使用 Docker 独立运行**：使用 libnetwork，无需 CNI plugins
- **使用 containerd 独立运行**：需要 CNI plugins
- **在 Kubernetes 中**：
  - 使用 containerd/CRI-O：直接使用 CNI
  - 使用 Docker（通过 cri-dockerd）：Docker 内部用 libnetwork，cri-dockerd 桥接到 CNI

这也是为什么：
- 安装 Docker 时不需要安装 CNI plugins
- 安装 containerd 时必须安装 CNI plugins
- 两者的网络配置方式完全不同

### 总结

**CNI Plugins 是容器网络配置的基础组件**：
- 提供容器网络接口的创建、配置和管理
- 是 Kubernetes 网络的基础
- 通过插件化设计实现灵活的网络方案
- containerd、CRI-O 等容器运行时都依赖它来配置网络

没有 CNI plugins，容器将无法连接到网络！

```Bash
VERSION=$(curl -Ls -o /dev/null -w %{url_effective} https://github.com/docker/buildx/releases/latest)
VERSION=${VERSION##*/}

mkdir -p $HOME/.docker/cli-plugins
wget https://github.com/docker/buildx/releases/download/$VERSION/buildx-$VERSION.linux-amd64 -O $HOME/.docker/cli-plugins/docker-buildx
```

https://www.zhangjiee.com/blog/2021/container-runtime.html
https://www.zhangjiee.com/blog/2018/different-from-docker-and-vm.html
https://www.zhangjiee.com/blog/2018/an-overall-view-on-docker-ecosystem-containers-moby-swarm-linuxkit-containerd-kubernete.html
https://www.zhangjiee.com/blog/2021/kubernetes-vs-docker.html

### containerd config

sudo vim /etc/containerd/config.toml

```Bash
[plugins.'io.containerd.cri.v1.images'.registry]
  config_path = '/etc/containerd/certs.d'
```

/etc/containerd/certs.d/192.168.50.10:5000/hosts.toml

```bash
server = "http://192.168.50.10:5000"

[host."http://192.168.50.10:5000"]
  capabilities = ["pull", "resolve", "push"]
  skip_verify = true
```

## nerdctl

nerdctl 是 **containerd 的命令行客户端工具**，它提供了与 Docker CLI 兼容的用户体验。

### 什么是 nerdctl

- **containerd 的 CLI 工具**：nerdctl 全称是 "**n**on-**e**nterprise cont**r**ol"（或 containerd ctl）
- **Docker 兼容**：命令语法与 docker 命令高度兼容，降低学习成本
- **CNCF 项目**：由 containerd 社区开发和维护
- **功能丰富**：支持 Docker 不支持的一些高级功能

### 主要特性

#### 1. Docker 兼容性
nerdctl 的命令与 docker 几乎完全兼容，可以无缝切换：

```bash
# Docker 命令
docker run -d -p 80:80 nginx
docker ps
docker images
docker build -t myapp .

# nerdctl 命令（完全相同）
nerdctl run -d -p 80:80 nginx
nerdctl ps
nerdctl images
nerdctl build -t myapp .
```

#### 2. 增强功能

nerdctl 支持一些 Docker 不支持的高级特性：

- **懒加载镜像（Lazy Pulling）**：使用 stargz/eStargz 格式，加快镜像拉取
- **镜像加密**：支持加密容器镜像
- **镜像签名**：支持 cosign 镜像签名验证
- **P2P 镜像分发**：支持 IPFS 分布式镜像存储
- **Rootless 模式**：无需 root 权限运行容器
- **多种运行时**：可配置使用不同的 OCI 运行时（runc、crun、gVisor 等）

#### 3. Kubernetes 一致性

- 与 Kubernetes 使用相同的 containerd 运行时
- 本地开发环境与生产环境（K8s）保持一致
- 便于调试 Kubernetes 相关问题

### 与 Docker 的对比

| 特性 | Docker | nerdctl |
|------|--------|---------|
| **底层运行时** | dockerd + containerd | containerd 直接 |
| **守护进程** | 需要 dockerd | 只需 containerd |
| **命令兼容性** | - | 兼容 docker 命令 |
| **镜像格式** | OCI | OCI + 增强格式（stargz） |
| **镜像加密** | ❌ | ✅ |
| **懒加载** | ❌ | ✅ |
| **Rootless** | 部分支持 | 完整支持 |
| **K8s 一致性** | 不同运行时 | 相同运行时 |
| **资源占用** | 较高 | 较低 |

### 为什么使用 nerdctl？

1. **学习成本低**：如果熟悉 docker 命令，可以直接使用 nerdctl
2. **性能更好**：直接使用 containerd，减少中间层
3. **与 K8s 一致**：本地环境和 Kubernetes 使用相同的容器运行时
4. **更轻量**：不需要额外的 dockerd 守护进程
5. **功能更强**：支持镜像加密、懒加载等高级特性

### 常用命令示例

```bash
# 运行容器
sudo nerdctl run -d --name nginx -p 80:80 nginx

# 查看容器
sudo nerdctl ps

# 查看镜像
sudo nerdctl images

# 构建镜像
sudo nerdctl build -t myapp:v1.0 .

# 推送镜像
sudo nerdctl push myapp:v1.0

# 网络管理
sudo nerdctl network create mynet
sudo nerdctl network ls

# 数据卷管理
sudo nerdctl volume create myvol
sudo nerdctl volume ls

# 查看日志
sudo nerdctl logs nginx

# 进入容器
sudo nerdctl exec -it nginx bash
```

### 安装说明

nerdctl 已经在文档的安装部分中提到：

```bash
# Arch Linux
pacman -S nerdctl

# Ubuntu/Debian（手动安装）
nerdctl_version="2.1.3"
curl -LO "https://github.com/containerd/nerdctl/releases/download/v${nerdctl_version}/nerdctl-${nerdctl_version}-linux-amd64.tar.gz"
sudo tar Cxzvf /usr/bin/ nerdctl-${nerdctl_version}-linux-amd64.tar.gz
```

### 高级用法

```Bash
# 使用私有仓库
sudo nerdctl --insecure-registry push 127.0.0.1:5000/image_0:1.4

# 网络管理
nerdctl network ls
nerdctl run --rm --network=kong-net busybox ping postgresql

# Rootless 模式（无需 sudo）
nerdctl run -d nginx
```

### 总结

**nerdctl 是 containerd 的命令行工具，提供与 Docker 兼容的命令接口**，让用户可以：
- 像使用 docker 一样使用 containerd
- 获得更好的性能和更轻量的资源占用
- 享受与 Kubernetes 一致的运行时环境
- 使用镜像加密、懒加载等高级特性

如果您在使用 containerd 作为容器运行时，nerdctl 是最佳的命令行工具选择。

## 私有容器仓库

https://github.com/goharbor/harbor
