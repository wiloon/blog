---
title: nerdctl
author: "-"
date: 2025-12-05T10:30:00+08:00
url: nerdctl
categories:
  - Container
tags:
  - reprint
  - remix
  - AI-assisted

---
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

## 安装 nerdctl

### Arch Linux 安装

```bash
pacman -S nerdctl
```

### Ubuntu/Debian 手动安装

```bash
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
```

## 容器开机自启动配置

### 为已存在的容器设置开机自启动

使用 `nerdctl update` 命令修改容器的重启策略：

```bash
# 设置容器开机自启动（除非手动停止）
sudo nerdctl update --restart unless-stopped <容器名称或ID>

# 示例
sudo nerdctl update --restart unless-stopped kafka

# 验证重启策略是否设置成功
sudo nerdctl inspect kafka | grep -A 5 restart.policy
```

### 创建容器时设置自启动

在运行容器时直接指定重启策略：

```bash
sudo nerdctl run -d \
  --name my-container \
  --restart unless-stopped \
  <镜像名称>
```

### 重启策略说明

| 策略 | 说明 |
|------|------|
| `no` | 默认值，容器退出时不自动重启 |
| `always` | 容器退出时总是重启，包括手动停止后系统重启也会启动 |
| `unless-stopped` | 容器退出时总是重启，但如果是手动停止的，系统重启后不会启动（**推荐**） |
| `on-failure[:max-retries]` | 仅在容器非正常退出时重启，可选指定最大重试次数 |

### 常用命令

```bash
# 查看容器的重启策略
sudo nerdctl inspect <容器名称> | grep -i restart

# 取消容器的自启动
sudo nerdctl update --restart no <容器名称>

# 查看所有容器及其重启策略
sudo nerdctl ps -a --format "{{.Names}}\t{{.Status}}\t{{.Labels}}"
```

### 注意事项

- `unless-stopped` 是最常用的策略，适合大多数服务容器
- 设置重启策略后，需要确保 containerd 服务本身已设置为开机启动
- 可以通过 `sudo systemctl enable containerd` 确保 containerd 服务开机启动

## 常用命令

### 运行容器

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

# 查看日志
sudo nerdctl logs nginx

# 进入容器
sudo nerdctl exec -it nginx bash

# 导出镜像
sudo nerdctl save -o foo.tar foo:latest
```

### 网络管理

```bash
# 网络管理
sudo nerdctl network create mynet
sudo nerdctl network ls
nerdctl run --rm --network=kong-net busybox ping postgresql
```

### 数据卷管理

```bash
# 数据卷管理
sudo nerdctl volume create myvol
sudo nerdctl volume ls
```

### 高级用法

```bash
# 使用私有仓库
sudo nerdctl --insecure-registry push 127.0.0.1:5000/image_0:1.4

# Rootless 模式（无需 sudo）
nerdctl run -d nginx
```

## 总结

**nerdctl 是 containerd 的命令行工具，提供与 Docker 兼容的命令接口**，让用户可以：
- 像使用 docker 一样使用 containerd
- 获得更好的性能和更轻量的资源占用
- 享受与 Kubernetes 一致的运行时环境
- 使用镜像加密、懒加载等高级特性

如果您在使用 containerd 作为容器运行时，nerdctl 是最佳的命令行工具选择。
