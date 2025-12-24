---
title: nerdctl
author: "-"
date: 2025-12-18T15:30:00+08:00
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

## 配置 Rootless 模式（免 sudo）

Rootless 模式允许普通用户无需 sudo 权限直接使用 nerdctl，这是推荐的使用方式。

### 什么是 Rootless 模式

- **无需 root 权限**：普通用户可以直接运行容器
- **提高安全性**：容器运行在用户命名空间中，即使容器被攻破也不会影响系统
- **用户隔离**：每个用户有独立的容器环境
- **完整功能**：支持几乎所有 nerdctl 功能（网络、卷、构建等）

### 前置要求

#### 1. 检查系统支持

```bash
# 检查内核是否支持用户命名空间
cat /proc/sys/kernel/unprivileged_userns_clone
# 应该返回 1

# 如果返回 0，需要启用（需要 root 权限）
sudo sysctl kernel.unprivileged_userns_clone=1

# 永久启用（重启后保持）
echo 'kernel.unprivileged_userns_clone=1' | sudo tee /etc/sysctl.d/99-rootless.conf
```

#### 2. 检查必要的工具

```bash
# 检查是否已安装 rootless 工具
which containerd-rootless-setuptool.sh
which rootlesskit
which slirp4netns

# Arch Linux 安装依赖（如果缺失）
sudo pacman -S rootlesskit slirp4netns fuse-overlayfs
sudo apt update && sudo apt install -y rootlesskit slirp4netns uidmap
```

### 安装配置步骤

#### 步骤 1：运行安装脚本

```bash
# 以普通用户身份运行（不要用 sudo）
containerd-rootless-setuptool.sh install
```

脚本会自动完成：
- 创建 `~/.config/containerd/config.toml` 配置文件
- 创建 `~/.config/systemd/user/containerd.service` systemd 用户服务
- 配置网络（使用 slirp4netns）
- 配置存储驱动

#### 步骤 2：配置环境变量

安装完成后，脚本会提示添加环境变量。将以下内容添加到 `~/.bashrc` 或 `~/.zshrc`：

```bash
# nerdctl rootless 配置
export PATH="$HOME/bin:$PATH"
export CONTAINERD_ADDRESS="$XDG_RUNTIME_DIR/containerd/containerd.sock"
export CONTAINERD_NAMESPACE="default"
```

然后重新加载配置：

```bash
# bash 用户
source ~/.bashrc

# zsh 用户
source ~/.zshrc
```

#### 步骤 3：启动 containerd 服务

```bash
# 启动 containerd 用户服务
systemctl --user start containerd.service

# 设置开机自启动
systemctl --user enable containerd.service

# 检查服务状态
systemctl --user status containerd.service

# 启用 lingering（即使退出登录也保持服务运行）
sudo loginctl enable-linger $USER
```

#### 步骤 4：验证配置

```bash
# 测试 nerdctl（注意：不需要 sudo）
nerdctl version
nerdctl info

# 运行测试容器
nerdctl run --rm hello-world

# 运行一个简单的 nginx 容器
nerdctl run -d --name nginx -p 8080:80 nginx
nerdctl ps

# 测试访问
curl http://localhost:8080

# 清理测试容器
nerdctl stop nginx
nerdctl rm nginx
```

### Rootless 模式常用命令

```bash
# 所有 nerdctl 命令都不需要 sudo
nerdctl pull nginx
nerdctl images
nerdctl run -d --name web -p 8080:80 nginx
nerdctl ps
nerdctl logs web
nerdctl exec -it web bash
nerdctl stop web
nerdctl rm web

# 网络管理
nerdctl network create mynet
nerdctl network ls

# 卷管理
nerdctl volume create myvol
nerdctl volume ls

# 构建镜像
nerdctl build -t myapp:latest .
```

### 管理 Rootless Containerd 服务

```bash
# 查看服务状态
systemctl --user status containerd

# 启动/停止/重启服务
systemctl --user start containerd
systemctl --user stop containerd
systemctl --user restart containerd

# 查看服务日志
journalctl --user -u containerd -f

# 检查 containerd 信息
nerdctl info | grep -i rootless
```

### 卸载 Rootless 模式

如果需要卸载 rootless 配置：

```bash
# 停止服务
systemctl --user stop containerd
systemctl --user disable containerd

# 运行卸载脚本
containerd-rootless-setuptool.sh uninstall

# 删除配置文件（可选）
rm -rf ~/.config/containerd
rm -rf ~/.local/share/containerd
```

### Rootless 模式的限制

虽然 rootless 模式功能完整，但有一些限制需要注意：

1. **端口限制**：
   - 不能直接绑定 1024 以下的特权端口（如 80、443）
   - 解决方案：使用高端口映射（如 8080:80），然后用反向代理

2. **性能影响**：
   - 网络性能可能略低于 root 模式（因为使用 slirp4netns）
   - 文件系统性能略有影响（使用 fuse-overlayfs）

3. **cgroup 限制**：
   - 需要 cgroup v2 支持
   - 资源限制功能可能受限

4. **某些高级功能**：
   - 不支持修改 iptables
   - 不支持某些特权操作

5. **VPN 兼容性问题**：
   - slirp4netns 可能与某些企业 VPN（如思科 AnyConnect）冲突
   - 可能导致容器无法访问网络
   - 解决方案见下文"VPN 环境下的网络配置"

### VPN 环境下的网络配置

如果你的环境中有企业 VPN（如思科 AnyConnect、GlobalProtect 等），可能会遇到 rootless 容器网络不通的问题。

#### 问题表现

```bash
# 容器无法访问外网
nerdctl run --rm busybox ping -c 3 8.8.8.8
# 100% packet loss
```

#### 网络方案对比

Rootless containerd 支持多种网络驱动：

| 网络方案 | 说明 | VPN 兼容性 | 性能 | 配置难度 |
|---------|------|-----------|------|---------|
| **slirp4netns** | 用户态网络栈（默认） | ⚠️ 可能冲突 | 较低 | 简单 |
| **vpnkit** | Docker Desktop 使用的方案 | ✅ 较好 | 中等 | 中等 |
| **lxc-user-nic** | 需要系统配置 | ⚠️ 可能冲突 | 较好 | 复杂 |
| **host 模式** | 使用宿主机网络 | ✅ 最好 | 最佳 | 简单 |

#### 解决方案 1：切换到 vpnkit（推荐）

```bash
# 1. 安装 vpnkit
# Ubuntu/Debian
sudo apt install vpnkit

# 或从源码编译
# git clone https://github.com/moby/vpnkit.git

# 2. 配置 containerd rootless 使用 vpnkit
mkdir -p ~/.config/systemd/user/containerd.service.d
cat > ~/.config/systemd/user/containerd.service.d/vpn-compat.conf << 'EOF'
[Service]
# 使用 vpnkit 替代 slirp4netns
Environment=CONTAINERD_ROOTLESS_ROOTLESSKIT_NET=vpnkit
EOF

# 3. 重启 containerd 服务
systemctl --user daemon-reload
systemctl --user restart containerd.service

# 4. 验证
nerdctl run --rm busybox ping -c 3 8.8.8.8
```

#### 解决方案 2：使用 host 网络模式

如果切换网络驱动仍有问题，可以使用 host 网络模式（与宿主机共享网络命名空间）：

```bash
# 运行容器时指定 --network host
nerdctl run -d --name nginx --network host nginx

# 注意：host 模式下不需要端口映射
# 容器直接使用宿主机的端口
```

**host 模式的特点：**
- ✅ 完全绕过 VPN 限制
- ✅ 网络性能最佳
- ❌ 失去容器网络隔离
- ❌ 端口冲突风险

#### 解决方案 3：回退到 root 模式

如果 rootless 模式的网络问题无法解决，可以回退使用 root 模式（sudo nerdctl）：

```bash
# root 模式默认使用 CNI bridge，通常与 VPN 兼容性更好
sudo nerdctl run -d --name nginx -p 8080:80 nginx

# 或使用 host 网络
sudo nerdctl run -d --name nginx --network host nginx
```

#### 网络诊断步骤

```bash
# 1. 测试宿主机网络
curl -I https://www.google.com

# 2. 测试 rootless 容器网络（默认网络）
nerdctl run --rm busybox ping -c 3 8.8.8.8

# 3. 测试 rootless 容器网络（host 模式）
nerdctl run --rm --network host busybox ping -c 3 8.8.8.8

# 4. 测试 root 模式容器网络
sudo nerdctl run --rm busybox ping -c 3 8.8.8.8

# 5. 检查当前网络配置
journalctl --user -u containerd.service | grep -i "net="
```

#### 推荐方案总结

针对不同场景的推荐：

1. **开发环境 + VPN**：
   - 优先使用 host 网络模式
   - 简单直接，兼容性最好

2. **需要网络隔离 + VPN**：
   - 尝试切换到 vpnkit
   - 如果不行，使用 root 模式 + bridge

3. **CI/CD 环境 + VPN**：
   - 使用 root 模式
   - 配置 sudo 免密（仅 CI 用户）

4. **多用户生产环境**：
   - 评估是否必须使用 VPN
   - 或配置 VPN 路由表，排除容器网络段

### Rootless vs Root 模式对比

| 特性 | Root 模式 (sudo) | Rootless 模式 |
|------|------------------|----------------|
| **安全性** | 低（容器以 root 运行） | 高（用户命名空间隔离） |
| **权限要求** | 需要 sudo | 无需 sudo |
| **端口绑定** | 支持所有端口 | 不支持 <1024 端口 |
| **性能** | 最佳 | 略有损失 |
| **配置复杂度** | 简单 | 需要额外配置 |
| **推荐场景** | 开发/测试环境 | 生产/多用户环境 |

### 故障排查

#### 问题 1：命令找不到

```bash
# 检查环境变量
echo $PATH
echo $CONTAINERD_ADDRESS

# 重新加载配置
source ~/.bashrc  # 或 ~/.zshrc
```

#### 问题 2：服务启动失败

```bash
# 查看详细日志
journalctl --user -u containerd -n 50

# 检查配置文件
cat ~/.config/containerd/config.toml

# 手动启动测试
containerd-rootless.sh
```

#### 问题 3：网络不通

```bash
# 检查 slirp4netns 是否安装
which slirp4netns

# 测试容器网络
nerdctl run --rm busybox ping -c 2 8.8.8.8
```

#### 问题 4：存储空间问题

```bash
# 检查存储位置
nerdctl info | grep -i root

# Rootless 存储位置通常在
~/.local/share/containerd

# 清理未使用的镜像和容器
nerdctl system prune -a
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
