---
title: devpi
author: "-"
date: 2025-12-02T14:30:00+08:00
url: devpi
categories:
  - Python
tags:
  - reprint
  - remix
  - AI-assisted
---
## 什么是 devpi？

devpi 是一个强大的 Python 包服务器，提供以下核心功能：

1. **PyPI 镜像缓存** - 缓存从 PyPI 下载的包，加速后续安装
2. **私有包仓库** - 托管私有仓库的包
3. **多源聚合** - 统一访问多个上游源（官方 PyPI、私有仓库）
4. **离线使用** - 缓存后即使网络断开也能安装包
5. **Web 管理界面** - 提供友好的 Web 界面，方便浏览包列表、查看索引配置、管理用户等操作

devpi 默认运行在 `http://localhost:3141`，可以通过浏览器访问 Web 界面进行可视化管理。

## 快速开始

如果你只想快速体验 devpi 的缓存功能，执行以下最简步骤：

```bash
# 1. 启动 devpi 容器
sudo nerdctl run -d --name devpi --restart unless-stopped \
  --network host docker.io/devpi/devpi-server:latest

# 2. 配置 pip 使用 devpi（使用默认索引）
pip config set global.index-url http://localhost:3141/root/pypi/+simple/
pip config set global.trusted-host localhost

# 3. 测试安装包（第一次会从 PyPI 下载并缓存）
pip install requests

# 4. 再次安装体验缓存加速
pip uninstall -y requests && pip install requests
```

**说明**：这个配置使用 devpi 默认的 `root/pypi` 索引，自动缓存官方 PyPI 的包。数据存储在容器内部，适合快速测试。生产环境建议使用下文的完整配置。

---

## devpi 能解决什么问题？

### 1. 网络慢、重复下载浪费时间
**问题**: 

- 网络慢或 VPN 环境下，每次 `pip install` 都要从 PyPI 下载，非常耗时
- 公司有多个 VPN 节点，不同节点访问速度差异大（某节点访问 PyPI 快但连客户 Lab 慢，另一节点相反）
- 频繁切换 VPN 节点导致重复下载相同的包
- 本地编译容器镜像时，反复下载相同的 Python 包

**容器构建场景的特殊性**：

容器构建时每次都是全新的容器环境，容器内部没有任何缓存，所以即使你本地已经下载过某个包，容器构建时还是要重新下载。这个问题有几种解决方案：

1. **使用 devpi 本地缓存（推荐）**：
   - devpi 运行在宿主机上，容器构建时从宿主机的 devpi 获取包
   - 一次下载，所有容器构建共享缓存
   - 不受容器生命周期影响

2. **使用构建工具的缓存挂载**：
   ```dockerfile
   # syntax=docker/dockerfile:1
   FROM python:3.11
   RUN --mount=type=cache,target=/root/.cache/pip \
       pip install -r requirements.txt
   ```
   - 缓存 pip 下载的包文件，但每次仍需从网络下载索引
   - 适合网络稳定但带宽有限的场景
   - 不能完全解决 VPN 切换问题

3. **离线包方式**：
   ```bash
   # 预先下载所有包
   pip download -r requirements.txt --dest ./packages
   
   # Dockerfile 中使用
   COPY ./packages /packages
   RUN pip install --no-index --find-links=/packages -r requirements.txt
   ```
   - 需要手动维护离线包目录
   - 包更新麻烦，适合固定版本的生产环境

4. **多阶段构建 + 基础镜像**：
   - 预先构建一个包含常用包的基础镜像
   - 后续构建从基础镜像继承
   - 适合团队内部共享的标准化环境

**为什么 devpi 是最佳方案**：
- ✅ 自动化：无需手动维护离线包
- ✅ 灵活：支持版本更新和新包安装
- ✅ 统一：容器构建和本地开发使用同一缓存
- ✅ 高效：真正的一次下载，永久复用

**解决**: 

devpi 本地缓存一次下载，永久复用，不受网络和 VPN 切换影响。

```bash
# 第一次：从 PyPI 下载 (慢)
pip install flask==3.1.0  # 10 秒

# 第二次：从 devpi 缓存读取 (快)
pip install flask==3.1.0  # 0.5 秒

# 切换 VPN 后再次安装或容器构建
nerdctl build .  # 从本地缓存获取，0.3 秒
```

### 2. 需要访问多个 Python 仓库
**问题**: 同时需要官方 PyPI 的公开包和私有仓库的内部包，管理麻烦。

**解决**: devpi 统一入口，自动按优先级查找。

```text
pip → devpi → 官方 PyPI / 私有仓库
```

### 3. 内网环境无法访问外网
**问题**: 生产环境无外网访问，无法安装依赖。

**解决**: 预先用 devpi 缓存所需包，内网访问 devpi 服务器。

## 在 nerdctl 环境中安装 devpi

### 环境要求
- nerdctl 已安装并正常运行
- 需要 sudo 权限（如果使用系统级 nerdctl）
- 网络可访问（用于拉取镜像）

### 方案选择

#### 网络模式
- **桥接模式** (默认): 适用于普通网络环境
- **host 模式**: 适用于 VPN 环境

#### 数据存储目录
根据 Linux FHS 标准，推荐以下目录：

| 目录 | 用途 | 特点 |
|------|------|------|
| `/var/cache/devpi` | 应用缓存 | ✅ 推荐，语义明确 |
| `/var/lib/devpi` | 应用数据 | 适合持久化重要数据 |
| `/opt/devpi` | 第三方应用 | 独立隔离 |
| `~/.cache/devpi` | 用户缓存 | 无需 sudo，单用户 |

### 安装脚本

创建 `devpi-setup.sh`:

```bash
#!/bin/bash
# devpi 安装脚本 - 使用 nerdctl

# 数据目录配置
DEVPI_DATA_DIR="/var/cache/devpi"

# 创建数据目录
sudo mkdir -p "$DEVPI_DATA_DIR"

# 设置目录权限
sudo chown -R $USER:$USER "$DEVPI_DATA_DIR"
chmod 755 "$DEVPI_DATA_DIR"

# 运行 devpi 容器
# 注意：如果在 VPN 环境下，添加 --network host
sudo nerdctl run -d \
  --name devpi \
  --restart unless-stopped \
  --network host \
  -v "$DEVPI_DATA_DIR":/data \
  -e DEVPI_SERVERDIR=/data \
  docker.io/devpi/devpi-server:latest

# 等待容器启动
echo "等待 devpi 容器启动..."
sleep 5

echo "================================"
echo "devpi 安装完成!"
echo "访问地址: http://localhost:3141"
echo "数据目录: $DEVPI_DATA_DIR"
echo "================================"
```

执行安装：

```bash
chmod +x devpi-setup.sh
./devpi-setup.sh
```

### 验证安装

```bash
# 1. 检查容器状态
sudo nerdctl ps | grep devpi

# 2. 检查服务是否响应
curl http://localhost:3141

# 3. 查看日志
sudo nerdctl logs devpi
```

## 配置 devpi

### 1. 安装 devpi-client

devpi-client 是 devpi 的命令行管理工具，用于配置索引、管理用户等。

**devpi-client vs Web UI 功能对比**:

| 功能类别 | devpi-client | Web UI |
|---------|-------------|--------|
| 浏览包列表 | ✅ `devpi list` | ✅ 可视化浏览 |
| 查看索引配置 | ✅ `devpi index` | ✅ 查看（只读） |
| 创建/修改索引 | ✅ `devpi index -c/m` | ❌ 不支持 |
| 用户管理 | ✅ `devpi user` | ❌ 不支持 |
| 上传包 | ✅ `devpi upload` | ❌ 不支持 |
| 删除包 | ✅ `devpi remove` | ❌ 不支持 |
| 配置镜像源 | ✅ `devpi index mirror_url` | ❌ 不支持 |
| 搜索包 | ✅ `devpi list` | ✅ 支持 |

**结论**: Web UI 主要用于**查看和浏览**，devpi-client 才能完成**配置和管理**操作。如果需要创建索引、配置上游源、管理用户等操作，必须使用 devpi-client。

```bash
# 从官方 PyPI 安装
pip install --break-system-packages \
  --index-url https://pypi.org/simple/ \
  devpi-client
```

验证安装：

```bash
devpi --version
```

### 2. 配置上游源

devpi 安装后需要配置索引才能使用。以下是三种常见配置场景：

#### 场景 1: 仅使用官方 PyPI（最简单）

最简单的配置，直接使用 devpi 默认的 `root/pypi` 索引，它会自动从 PyPI 获取包并缓存。

```bash
# 无需额外配置，直接使用默认索引
pip config set global.index-url http://localhost:3141/root/pypi/+simple/
pip config set global.trusted-host localhost
```

**说明**：devpi 的 `root/pypi` 索引默认指向 `https://pypi.org/simple/`，会自动缓存下载的包。

#### 场景 2: 使用私有仓库

如果有私有 PyPI 仓库（如 Artifactory、Nexus），可以配置为上游源。

```bash
# 连接到 devpi
devpi use http://localhost:3141

# 登录 root 用户（默认密码为空）
devpi login root --password=''

# 创建私有仓库索引
devpi index -c root/private type=mirror mirror_url=<YOUR_PRIVATE_REPO_URL>

# 示例（使用占位符）:
# devpi index -c root/private type=mirror mirror_url=https://username:token@your-company.com/artifactory/api/pypi/your-repo/simple
```

#### 场景 3: 同时使用官方 PyPI 和私有仓库（推荐）

创建组合索引，**通过 `bases` 参数控制查找顺序**（从左到右依次查找）。

**选项 A: 优先官方 PyPI，找不到再查私有仓库**

```bash
# 1. 创建官方 PyPI 镜像索引
devpi use http://localhost:3141
devpi login root --password=''
# -c: create（创建新索引）
# root/pypi-public: 索引路径（用户名/索引名）
# type=mirror: 索引类型为镜像
# mirror_url: 上游镜像地址
devpi index -c root/pypi-public type=mirror mirror_url=https://pypi.org/simple/

# 2. 配置私有仓库索引
# devpi index -c root/private type=mirror mirror_url=<YOUR_PRIVATE_REPO_URL>

# 3. 创建组合索引，优先官方 PyPI（从左到右查找）
# -c: create（创建新索引）
# root/dev: 新索引的路径
# bases: 指定上游索引列表（从左到右查找）
# volatile=False: 包一旦发布就不可修改（推荐生产环境，确保包的稳定性）
devpi index -c root/dev bases=root/pypi-public,root/private volatile=False

# 4. 查看配置
devpi index root/dev
```

查找顺序：
```text
pip → root/dev → ① root/pypi-public (官方 PyPI) 
                 ② root/private (私有仓库)
```

**选项 B: 优先私有仓库，找不到再查官方 PyPI**

```bash
# 创建组合索引，优先私有仓库（调整 bases 顺序）
devpi index -c root/dev bases=root/private,root/pypi-public volatile=False
```

查找顺序：
```text
pip → root/dev → ① root/private (私有仓库)
                 ② root/pypi-public (官方 PyPI)
```

**使用场景建议**：
- **优先官方**：适合大部分场景，官方包更新及时、稳定
- **优先私有**：私有包覆盖官方包时（如打了补丁的版本）

### 3. 配置 pip 使用 devpi

#### 临时使用（单次命令）

```bash
pip install --index-url http://localhost:3141/root/dev/+simple/ \
  --trusted-host localhost \
  package-name
```

#### 永久配置（推荐）

```bash
# 设置默认索引
pip config set global.index-url http://localhost:3141/root/dev/+simple/
pip config set global.trusted-host localhost

# 可选：设置超时时间（对于首次下载大包有用）
pip config set global.timeout 120

# 查看配置
pip config list
```

配置文件位置：`~/.config/pip/pip.conf`

```ini
[global]
index-url = http://localhost:3141/root/dev/+simple/
trusted-host = localhost
timeout = 120
```

## 验证 devpi 是否可用

### 1. 查看配置

```bash
# 查看当前 pip 配置
pip config list

# 查看使用的索引地址
pip config get global.index-url
# 输出: http://localhost:3141/root/dev/+simple/
```

### 2. 查询包版本

```bash
# 查询包的可用版本
pip index versions flask

# 输出示例:
# flask (3.1.2)
# Available versions: 3.1.2, 3.1.1, 3.1.0, ...
```

### 3. 下载测试

```bash
# 下载包到指定目录（不安装）
pip download --no-deps --dest /tmp flask==3.1.0

# 输出应显示从 devpi 下载:
# Looking in indexes: http://localhost:3141/root/dev/+simple/
# Downloading http://localhost:3141/root/pypi-public/...
```

### 4. 测试缓存效果

```bash
# 第一次下载（从上游）
rm /tmp/flask*.whl
time pip download --no-deps --dest /tmp flask==3.1.0
# 耗时: 约 5-10 秒

# 第二次下载（从缓存）
rm /tmp/flask*.whl
time pip download --no-deps --dest /tmp flask==3.1.0
# 耗时: 约 0.5 秒
```

### 5. 查看缓存

```bash
# 查看缓存目录大小
du -sh /var/cache/devpi/

# 查看缓存的包文件
find /var/cache/devpi/+files -name "*.whl" | head -10
```

## devpi-client 常用命令

### 基础操作

```bash
# 连接到 devpi 服务器
devpi use http://localhost:3141

# 登录用户
devpi login <username> --password=<password>

# 登出
devpi logoff

# 查看当前状态
devpi use
```

### 索引管理

```bash
# 列出所有索引
devpi use -l

# 查看索引详情（示例：查看 root/dev 索引）
devpi index root/dev

# 创建新索引（通用格式）
devpi index -c <username>/<indexname>

# 修改索引配置（示例：修改镜像地址）
devpi index <username>/<indexname> mirror_url=<url>

# 删除索引
devpi index --delete <username>/<indexname>
```

### 用户管理

```bash
# 创建用户
devpi user -c <username> password=<password> email=<email>

# 修改密码
devpi user -m <username> password=<newpassword>

# 查看用户信息
devpi user <username>

# 删除用户
devpi user --delete <username>
```

### 包管理

```bash
# 上传包到 devpi
devpi upload

# 上传指定文件
devpi upload dist/*

# 查看索引中的包
devpi list <packagename>

# 删除包
devpi remove <packagename>==<version>
```

## 常用 pip 命令示例

### 安装包

```bash
# 安装最新版本
pip install requests

# 安装指定版本
pip install flask==3.1.0

# 安装兼容版本
pip install "flask~=3.1.0"

# 从 requirements.txt 安装
pip install -r requirements.txt
```

### 下载包

```bash
# 下载包（不安装）
pip download --no-deps --dest /tmp flask

# 下载包及其依赖
pip download --dest /tmp flask

# 下载所有依赖到目录（用于离线安装）
pip download -r requirements.txt --dest ./packages
```

### 查询包信息

```bash
# 查看包的可用版本
pip index versions flask

# 搜索包（需要 PyPI 支持）
pip search flask

# 查看已安装包的信息
pip show flask

# 列出已安装的包
pip list
```

## 检查包的下载状态

devpi 在下载和缓存包时，可以通过以下方法检查包的状态：

### 方法 1: 通过 Web UI 查看（最直观）

访问 devpi Web 界面：`http://localhost:3141`

1. 浏览到对应的索引（如 `root/pypi`）
2. 搜索包名
3. 点击包名查看详情
4. 查看包版本列表和文件列表

**状态判断**：
- ✅ **已缓存**：能看到包的详细信息，包括 `.whl` 或 `.tar.gz` 文件链接
- ⏳ **正在下载**：包列表中存在，但点击后文件列表为空或加载中
- ❌ **未缓存**：包列表中不存在

### 方法 2: 通过 devpi-client 命令行查看

```bash
# 首次使用需要指定 devpi 服务器地址（只需执行一次）
devpi use http://localhost:3141

# 查看某个包的所有版本（查询公开索引无需登录）
devpi list flask

# 输出示例（已缓存）:
# http://localhost:3141/root/pypi/+f/abc/flask-3.1.0-py3-none-any.whl
# http://localhost:3141/root/pypi/+f/def/flask-3.1.0.tar.gz

# 查看指定版本的详细信息
devpi list flask==3.1.0

# 如果输出为空或没有文件链接，说明未缓存或正在下载

# 注意：如果查询私有索引或遇到权限错误，需要先登录
# devpi login root --password=''
```

### 方法 3: 检查缓存目录中的文件

```bash
# 查看缓存目录
ls -lh /var/cache/devpi/+files/

# 搜索特定包的文件
find /var/cache/devpi/+files -name "*flask*" -type f

# 输出示例（已缓存）:
# /var/cache/devpi/+files/abc123/flask-3.1.0-py3-none-any.whl
# /var/cache/devpi/+files/def456/flask-3.1.0.tar.gz

# 查看文件大小（判断是否下载完整）
du -h /var/cache/devpi/+files/*flask*

# 实时监控缓存目录变化（适合观察正在下载的包）
watch -n 1 'ls -lh /var/cache/devpi/+files/ | grep flask'
```

### 方法 4: 查看 devpi 日志

```bash
# 实时查看 devpi 日志
sudo nerdctl logs -f devpi

# 查看最近的日志（包含下载活动）
sudo nerdctl logs --tail 100 devpi

# 输出示例（正在下载）:
# [INFO] fetching https://files.pythonhosted.org/packages/.../flask-3.1.0-py3-none-any.whl
# [INFO] storing flask-3.1.0-py3-none-any.whl (size: 101KB)

# 过滤特定包的日志
sudo nerdctl logs devpi | grep flask
```

### 方法 5: 使用 HTTP API 检查（编程方式）

devpi 提供 JSON API 接口，可以编程查询包状态：

```bash
# 查询包的元数据
curl http://localhost:3141/root/pypi/flask/ | jq

# 查询特定版本
curl http://localhost:3141/root/pypi/flask/3.1.0 | jq

# 检查包文件是否存在（返回 200 表示已缓存）
curl -I http://localhost:3141/root/pypi/+f/abc123/flask-3.1.0-py3-none-any.whl

# 输出示例（已缓存）:
# HTTP/1.1 200 OK
# Content-Type: application/octet-stream
# Content-Length: 103456

# 输出示例（未缓存/正在下载）:
# HTTP/1.1 404 Not Found
```

### 方法 6: 测试下载速度判断状态

```bash
# 第一次下载（如果未缓存，会从上游下载，较慢）
time pip download --no-deps --dest /tmp flask==3.1.0
# 耗时 > 3 秒 → 可能正在首次下载

# 第二次下载（如果已缓存，非常快）
rm /tmp/flask*.whl
time pip download --no-deps --dest /tmp flask==3.1.0
# 耗时 < 1 秒 → 已完成缓存

# 使用 pip 的 -v 参数查看详细日志
pip download --no-deps --dest /tmp -v flask==3.1.0
# 输出会显示从哪个地址下载，以及是否命中缓存
```

### 下载状态总结表

| 状态 | Web UI | devpi list | 缓存目录 | 日志 | 下载速度 |
|------|--------|------------|----------|------|----------|
| **未缓存** | 无记录 | 无输出 | 无文件 | 无日志 | - |
| **正在下载** | 有记录但无文件 | 有记录但无文件链接 | 文件不完整或临时文件 | 显示 fetching | 较慢（首次） |
| **已缓存** | 显示完整信息和文件 | 显示文件链接 | 文件完整 | 显示 stored | 极快（< 1s） |

### 实用脚本：检查包是否已缓存

创建 `check-devpi-cache.sh`：

```bash
#!/bin/bash
# 检查 devpi 中的包是否已缓存

PACKAGE=$1
VERSION=$2

if [ -z "$PACKAGE" ]; then
    echo "用法: $0 <package-name> [version]"
    echo "示例: $0 flask 3.1.0"
    exit 1
fi

# 构造查询 URL
if [ -z "$VERSION" ]; then
    URL="http://localhost:3141/root/pypi/$PACKAGE/"
else
    URL="http://localhost:3141/root/pypi/$PACKAGE/$VERSION"
fi

# 查询包信息
echo "查询: $URL"
RESPONSE=$(curl -s "$URL")

# 检查是否有文件链接（已缓存的标志）
if echo "$RESPONSE" | grep -q "+f/.*\.whl\|+f/.*\.tar\.gz"; then
    echo "✅ 包已缓存"
    # 提取文件链接
    echo "$RESPONSE" | grep -oP '"\+f/[^"]+\.(whl|tar\.gz)"' | sed 's/"//g'
else
    echo "❌ 包未缓存或正在下载"
fi
```

使用方法：

```bash
chmod +x check-devpi-cache.sh

# 检查包（所有版本）
./check-devpi-cache.sh flask

# 检查特定版本
./check-devpi-cache.sh flask 3.1.0
```

## 性能优化建议

### 1. 调整超时时间

首次下载大包或网络慢时，增加超时：

```bash
pip config set global.timeout 180
```

### 3. 监控缓存大小

```bash
# 定期检查缓存大小
du -sh /var/cache/devpi/
```

### 4. 网络优化

如果在 VPN 环境下：
- 使用 `--network host` 模式
- 配置更长的超时时间

## 总结

devpi 是一个功能强大的 Python 包管理工具，通过本地缓存和多源聚合，能够：

1. ✅ 大幅提升包安装速度（缓存后秒级完成）
2. ✅ 统一管理多个 Python 包源
3. ✅ 支持私有包托管
4. ✅ 适用于离线和受限网络环境
5. ✅ 节省带宽和存储资源

通过 nerdctl 容器化部署，devpi 的安装和管理变得简单高效。配合 devpi-client 工具，可以灵活配置各种使用场景，是 Python 开发团队的理想选择。

## 前端项目的类似方案

对于 npm/pnpm 项目，有以下本地缓存解决方案：

### 1. Verdaccio（推荐，类似 devpi）

Verdaccio 是一个轻量级的私有 npm 代理注册表，功能与 devpi 类似：

**核心功能**：
- 🔄 npm 官方源镜像缓存
- 📦 私有包托管
- 🌐 离线使用
- 🚀 加速包安装
- 🎨 Web 管理界面

**快速开始**：

```bash
# 1. 启动 Verdaccio 容器
sudo nerdctl run -d --name verdaccio --restart unless-stopped \
  --network host \
  -v /var/cache/verdaccio:/verdaccio/storage \
  docker.io/verdaccio/verdaccio:latest

# 2. 配置 npm 使用 Verdaccio
npm config set registry http://localhost:4873/

# 3. 配置 pnpm 使用 Verdaccio
pnpm config set registry http://localhost:4873/

# 4. 测试安装包（第一次会从 npm 下载并缓存）
npm install lodash

# 5. 再次安装体验缓存加速
npm uninstall lodash && npm install lodash
```

**Web 界面**：访问 `http://localhost:4873` 查看缓存的包

**配置文件** (`/var/cache/verdaccio/config.yaml`)：

```yaml
storage: /verdaccio/storage

auth:
  htpasswd:
    file: /verdaccio/htpasswd

uplinks:
  npmjs:
    url: https://registry.npmjs.org/

packages:
  '@*/*':
    access: $all
    publish: $authenticated
    proxy: npmjs

  '**':
    access: $all
    publish: $authenticated
    proxy: npmjs

logs:
  - {type: stdout, format: pretty, level: http}
```

### 2. pnpm 内置缓存（最简单）

pnpm 本身就有强大的本地缓存机制，**无需额外工具**：

```bash
# pnpm 的缓存位置
~/.local/share/pnpm/store  # Linux
~/Library/pnpm/store       # macOS
%LOCALAPPDATA%\pnpm\store  # Windows

# 查看缓存信息
pnpm store path
pnpm store status

# 清理缓存（如果需要）
pnpm store prune
```

**工作原理**：
- pnpm 使用内容寻址存储（CAS），所有包存储在全局 store
- 项目中的 `node_modules` 只是硬链接或软链接
- 同一个包版本只存储一次，多个项目共享

**推荐使用场景**：
- ✅ 单机开发环境
- ✅ 不需要私有包托管
- ✅ 追求极简配置

### 3. npm cache（npm 自带）

npm 也有内置缓存，但功能较弱：

```bash
# 查看缓存位置
npm config get cache

# 验证缓存完整性
npm cache verify

# 清理缓存
npm cache clean --force
```

**局限**：
- ❌ 不支持离线安装
- ❌ 缓存命中率低
- ❌ 无法跨项目共享

### 4. 其他方案对比

| 方案 | 镜像缓存 | 私有包 | 离线 | 团队共享 | 复杂度 |
|------|---------|--------|------|---------|--------|
| **Verdaccio** | ✅ | ✅ | ✅ | ✅ | 中 |
| **pnpm store** | ✅ | ❌ | ⚠️ | ❌ | 低 |
| **npm cache** | ⚠️ | ❌ | ❌ | ❌ | 低 |
| **cnpm** | ✅ | ✅ | ⚠️ | ✅ | 高 |

### 推荐方案

**个人开发**：
- 直接使用 **pnpm**（自带缓存，无需配置）

**团队/企业**：
- 使用 **Verdaccio**（完整的私有 npm 注册表）

**容器构建加速**：
```dockerfile
# 使用 pnpm 并挂载缓存
FROM node:20
RUN npm install -g pnpm

# 使用 BuildKit 缓存挂载
RUN --mount=type=cache,target=/root/.local/share/pnpm/store \
    pnpm install --frozen-lockfile
```

### Verdaccio vs devpi 对比

| 特性 | Verdaccio (npm) | devpi (Python) |
|------|----------------|----------------|
| 镜像缓存 | ✅ | ✅ |
| 私有包托管 | ✅ | ✅ |
| Web UI | ✅ | ✅ |
| 多源聚合 | ✅ | ✅ |
| 用户管理 | ✅ | ✅ |
| 默认端口 | 4873 | 3141 |

### 参考资源

**Verdaccio**：
- [官方文档](https://verdaccio.org/)
- [GitHub](https://github.com/verdaccio/verdaccio)
- [Docker Hub](https://hub.docker.com/r/verdaccio/verdaccio)

**pnpm**：
- [官方文档](https://pnpm.io/)
- [缓存机制说明](https://pnpm.io/next/how-peers-are-resolved)

## 参考资源

- [devpi 官方文档](https://devpi.net/)
- [devpi GitHub](https://github.com/devpi/devpi)
- [pip 官方文档](https://pip.pypa.io/)
- [nerdctl GitHub](https://github.com/containerd/nerdctl)
