---
title: windows wsl
author: "w1100n"
date: 2025-12-10T15:30:00+08:00
url: wsl
categories:
  - Linux
tags:
  - reprint
  - remix
  - AI-assisted
---

## Windows WSL

WSL: Windows Subsystem for Linux

## 官方文档

- [微软官方安装文档](https://learn.microsoft.com/zh-cn/windows/wsl/install)
- [WSL 文档](https://learn.microsoft.com/en-us/windows/wsl/)
- [WSL 中文文档](https://learn.microsoft.com/zh-cn/windows/wsl/)

## 基本命令

以管理员模式打开 PowerShell 或 CMD

```bash
# 查看已安装的 WSL 发行版
wsl --list --verbose
wsl -l -v

# 启动指定的发行版
wsl -d archlinux
wsl -d archlinux -u wiloon  # 指定用户

# 列出可用的发行版
wsl --list --online
wsl -l -o

# 安装 WSL Ubuntu (默认安装最新 LTS 版本)
wsl --install

# 安装指定的发行版 (如 ArchLinux)
wsl --install -d archlinux

# 卸载发行版
wsl --unregister Ubuntu-22.04

# 安装 Windows Terminal
winget install Microsoft.WindowsTerminal

# 关闭所有 WSL 实例
wsl --shutdown

# 强制关闭某一个实例
wsl --terminate Ubuntu
wsl -t Ubuntu

# 设置默认发行版
wsl --set-default archlinux
wsl -s archlinux  # 简写形式

# 查看 WSL 状态
wsl --status
```

## Ubuntu 基本设置

```bash
# 更新系统
sudo apt update && sudo apt upgrade

# git 默认已安装
```

## 文件共享

### Ubuntu 访问 Windows 文件

```bash
cd /mnt/c/
ls -l
```

### Windows 访问 Ubuntu 文件

在文件资源管理器地址栏输入：

```text
\\wsl$\Ubuntu\
```

## VSCode 连接 WSL

### 开启 Windows 功能

搜索"Windows 功能"，勾选以下两项，点击确认后会提示重启：

- 适用于 Linux 的 Windows 子系统
- 虚拟机平台

```bash
wsl --list --online
wsl --install -d Ubuntu-20.04
```

### 错误 0x800701bc

如遇到此错误，需要下载并安装 Linux 内核更新包：

- [WSL2 Linux 内核更新包](https://aka.ms/wsl2kernel)

### WSLg (GUI 应用支持)

- [WSLg 项目](https://github.com/microsoft/wslg)

升级 WSL 到最新版本：

```bash
wsl --update
```

#### 安装 Intel 显示驱动

- [Intel Graphics Windows DCH Drivers](https://downloadcenter.intel.com/download/30579/Intel-Graphics-Windows-DCH-Drivers)

## WSL 安装步骤

### 步骤 1：启用适用于 Linux 的 Windows 子系统

```bash
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
```

### 步骤 2：检查 Windows 版本

```bash
winver
```

### 步骤 3：启用虚拟机功能

```bash
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

### 步骤 4：从 Windows 应用商店安装 Ubuntu

### 步骤 5：下载并安装 Linux 内核更新包

### 步骤 6：将 WSL 2 设置为默认版本

```bash
wsl --set-default-version 2
```

### 步骤 7：将已安装的 WSL 转换为 WSL2

```bash
wsl --set-version Ubuntu-20.04 2
```

---

## Ubuntu 配置

### 配置 Ubuntu 镜像源 (阿里云)

参考：[阿里云 Ubuntu 镜像](https://developer.aliyun.com/mirror/ubuntu)

编辑源列表文件：

```bash
sudo vim /etc/apt/sources.list
```

用以下内容覆盖 `/etc/apt/sources.list`：

```bash
deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
```

### 更新系统

```bash
sudo apt update
sudo apt upgrade
```

### 安装开发工具

```bash
sudo apt install golang git python make maven openjdk-8-jdk ttf-wqy-microhei ttf-wqy-zenhei xfonts-wqy
```

### 安装 Node.js

参考：[NodeSource 安装说明](https://github.com/nodesource/distributions)

```bash
curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### 配置 npm 镜像

```bash
npm install -g mirror-config-china --registry=http://registry.npm.taobao.org
```

### 配置 Maven

```bash
mkdir ~/.m2
vim ~/.m2/settings.xml
```

### 配置 Go 代理

编辑 `~/.bashrc`：

```bash
export GO111MODULE=on
export GOPROXY=https://goproxy.cn
```

### 验证安装

```bash
node -v && npm -v && go version
```

### 运行 Spring Boot 项目

```bash
mvn spring-boot:run
```

---

## 网络配置

### 固定 IP

#### WSL 自动设置 DISPLAY IP

编辑 `~/.bashrc` 或 `~/.zshrc`：

```bash
export DISPLAY=$(awk '/nameserver / {print $2; exit}' /etc/resolv.conf 2>/dev/null):0
```

#### Windows 脚本设置网卡 IP

参考：[WSL2 固定 IP 配置](https://blog.csdn.net/manbu_cy/article/details/108476859)

```batch
@echo off
setlocal enabledelayedexpansion

:: 设置 WSL2 IP
wsl -u root ip addr | findstr "192.168.96.2" > nul
if !errorlevel! equ 0 (
    echo wsl ip has set
) else (
    wsl -u root ip addr add 192.168.96.2/28 broadcast 192.168.96.15 dev eth0 label eth0:1
    echo set wsl ip success: 192.168.96.2
)

:: 设置 Windows IP
ipconfig | findstr "192.168.96.1" > nul
if !errorlevel! equ 0 (
    echo windows ip has set
) else (
    netsh interface ip add address "vEthernet (WSL)" 192.168.96.1 255.255.255.240
    echo set windows ip success: 192.168.96.1
)

pause
```

### 设置默认用户

#### 方法 1：使用 wsl.conf 配置（推荐）

编辑 `/etc/wsl.conf`（需要 root 权限）：

```bash
sudo vim /etc/wsl.conf
```

添加或修改以下内容：

```ini
[boot]
# 是否启用 systemd
systemd=true

[interop]
enabled = true
appendWindowsPath = true

[user]
default=your_username  # 替换为你的用户名，如 wiloon
```

保存后，在 Windows PowerShell 中重启 WSL：

```powershell
wsl --shutdown
```

重新启动后，默认会以指定用户登录。

#### 方法 2：使用发行版配置命令

在 PowerShell 中执行：

```powershell
cd C:\Users\<用户名>\AppData\Local\Microsoft\WindowsApps
dir
# 找到以 ubuntu 开头的 exe 文件
ubuntu2004.exe config --default-user user0

# ArchLinux 使用
arch.exe config --default-user wiloon
```

#### 方法 3：在 Windows Terminal 中配置

打开 Windows Terminal 设置（`Ctrl + ,`），修改对应发行版的配置：

```json
{
    "guid": "{be8746a7-283c-54e5-babb-613c0628ae4d}",
    "hidden": false,
    "name": "archlinux",
    "source": "Microsoft.WSL",
    "commandline": "wsl.exe -d archlinux -u wiloon"
}
```

**参数说明：**

- `-d archlinux` - 指定 WSL 发行版名称
- `-u wiloon` - 指定默认登录用户

### WSL Interop 故障排查

#### 问题：su 切换用户后 Windows 命令不可用

**现象：**

```bash
# root 用户下可以执行
ssh-add.exe -l

# 切换到普通用户后失败
su - wiloon
ssh-add.exe -l  # command not found
```

**原因：**

使用 `su -` 切换用户时会创建全新的 login shell，不会继承以下关键环境变量：

- `WSL_INTEROP` - WSL 与 Windows 互操作的核心变量
- `PATH` - 包含 Windows 可执行文件路径

**解决方案：**

##### 方案 1：不使用 su 切换用户（强烈推荐）

使用上述方法配置默认用户，直接以目标用户启动 WSL：

```bash
# 在 Windows 中直接以指定用户启动
wsl -d archlinux -u wiloon

# 或在 Windows Terminal 中配置 commandline
```

##### 方案 2：修复 su 切换后的环境

在目标用户的 `~/.bashrc` 或 `~/.zshrc` 中添加：

```bash
# WSL Interop - 修复 su 切换用户后的问题
if [ -n "$WSL_DISTRO_NAME" ]; then
    # 重新设置 WSL_INTEROP
    if [ -z "$WSL_INTEROP" ]; then
        export WSL_INTEROP=$(ls /run/WSL/*_interop 2>/dev/null | head -1)
    fi
    
    # 确保 Windows PATH 存在
    if ! echo "$PATH" | grep -q "/mnt/c/Windows"; then
        export PATH="$PATH:/mnt/c/Windows/System32:/mnt/c/Windows:/mnt/c/Windows/System32/WindowsPowerShell/v1.0"
    fi
fi
```

应用配置：

```bash
source ~/.bashrc  # 或 source ~/.zshrc
```

验证：

```bash
# 检查环境变量
echo $WSL_INTEROP
echo $PATH | grep "/mnt/c"

# 测试 Windows 命令
ssh-add.exe -l
where.exe ssh-add.exe
```

**为什么直接启动比 su 切换更好：**

| 方式 | WSL_INTEROP | Windows PATH | 推荐度 |
|------|-------------|--------------|--------|
| `wsl -u user` | ✅ 自动设置 | ✅ 自动加载 | ⭐⭐⭐⭐⭐ |
| `/etc/wsl.conf` 默认用户 | ✅ 自动设置 | ✅ 自动加载 | ⭐⭐⭐⭐⭐ |
| `su - user` | ❌ 丢失 | ❌ 丢失 | ⭐⭐ |
| `su user`（无 -） | ⚠️ 部分保留 | ⚠️ 部分保留 | ⭐⭐⭐ |

#### 错误：cannot execute binary file: Exec format error

**现象：**

```bash
# 执行 Windows 命令时报错
ssh-add.exe -l
# bash: /mnt/c/WINDOWS/System32/OpenSSH/ssh-add.exe: cannot execute binary file: Exec format error

cmd.exe /c echo test
# bash: /mnt/c/WINDOWS/system32/cmd.exe: cannot execute binary file: Exec format error
```

**原因：**

在 ArchWSL 中启用 `systemd=true` 会导致 `binfmt_misc` 无法正确注册 Windows 可执行文件处理器，从而导致所有 `.exe` 文件都无法执行。

这是 WSL2 与 systemd 的已知兼容性问题，特别是在 ArchLinux 发行版中更为常见。

**排查步骤：**

```bash
# 1. 检查 binfmt_misc 注册情况
ls -la /proc/sys/fs/binfmt_misc/
# 如果只有 register 和 status 文件，说明 WSLInterop 未注册

# 2. 测试简单的 Windows 命令
cmd.exe /c echo test
# 如果报 "Exec format error"，确认是 interop 问题

# 3. 检查当前 wsl.conf 配置
cat /etc/wsl.conf
```

**解决方案：**

##### 方案 1：禁用 systemd（推荐，最可靠）

编辑 `/etc/wsl.conf`：

```bash
sudo nano /etc/wsl.conf
```

修改为：

```ini
[boot]
systemd=false

[interop]
enabled = true
appendWindowsPath = true

[user]
default=your_username
```

在 Windows PowerShell 中重启 WSL：

```powershell
wsl --shutdown
```

重新进入 WSL 测试：

```bash
# 测试 Windows 命令
cmd.exe /c echo "Windows interop works"
ssh-add.exe -l
```

##### 方案 2：保留 systemd 但手动修复 binfmt（不稳定）

如果必须使用 systemd，可以尝试在每次启动后手动注册 binfmt：

```bash
# 创建启动脚本（需要 root 权限）
sudo tee /usr/local/bin/fix-wsl-interop.sh > /dev/null << 'EOF'
#!/bin/bash
if [ ! -f /proc/sys/fs/binfmt_misc/WSLInterop ]; then
    echo ':WSLInterop:M::MZ::/init:PF' > /proc/sys/fs/binfmt_misc/register
fi
EOF

sudo chmod +x /usr/local/bin/fix-wsl-interop.sh

# 添加到 ~/.bashrc 或创建 systemd 服务
echo '/usr/local/bin/fix-wsl-interop.sh' | sudo tee -a /etc/profile
```

**注意：** 此方法不保证稳定，重启后可能失效。

##### 方案 3：使用完整路径配合环境变量

如果上述方案都不理想，可以在需要时临时切换配置：

```bash
# 创建配置切换脚本
# ~/.local/bin/toggle-systemd.sh

#!/bin/bash
if grep -q "systemd=true" /etc/wsl.conf; then
    sudo sed -i 's/systemd=true/systemd=false/' /etc/wsl.conf
    echo "Disabled systemd. Run 'wsl --shutdown' in Windows to apply."
else
    sudo sed -i 's/systemd=false/systemd=true/' /etc/wsl.conf
    echo "Enabled systemd. Run 'wsl --shutdown' in Windows to apply."
fi
```

**对比总结：**

| 方案 | Windows 命令 | systemd 功能 | 稳定性 | 推荐度 |
|------|-------------|-------------|--------|--------|
| 禁用 systemd | ✅ 完美支持 | ❌ 不可用 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 手动修复 binfmt | ⚠️ 不稳定 | ✅ 可用 | ⭐⭐ | ⭐⭐ |
| 按需切换 | ✅ 取决于配置 | ✅ 取决于配置 | ⭐⭐⭐ | ⭐⭐⭐ |

**最佳实践：**

对于大多数 WSL 使用场景，**不需要 systemd**。如果你主要使用 WSL 进行开发、编译、运行脚本等，禁用 systemd 可以获得更好的 Windows 互操作体验。

只有在需要运行依赖 systemd 的服务（如 Docker、某些数据库服务）时，才考虑启用 systemd，但要接受 Windows 命令可能不可用的限制。

### 字体配置（解决乱码）

参考：[WSL 字体配置](https://zhuanlan.zhihu.com/p/68336685)

在 Windows 下安装 Powerline 字体：

```bash
# Windows 下需先安装 git
git clone https://github.com/powerline/fonts.git --depth=1
# 用 PowerShell 执行 install.ps1
```

#### 修改 WSL 字体

1. 右键点击 WSL 窗口左上角图标
2. 选择"属性"
3. 选择"字体"
4. 选择"Noto Mono for Powerline"

---

## 图形界面配置

### VcXsrv 安装

从 SourceForge 下载最新版本的 VcXsrv：

- [VcXsrv 下载](https://sourceforge.net/projects/vcxsrv/files/vcxsrv/)

#### 启动 XLaunch

从开始菜单启动 XLaunch

#### VcXsrv 配置

**Display settings:**

- One large window
- Display number: -1

**Client startup:**

- Start no client

**Extra settings:**

- Clipboard → Primary Selection
- Native opengl
- Disable access control

### WSL2 安装 Xfce4

```bash
sudo apt install -y xfce4
```

### 配置 DNS 解析

编辑 `/etc/resolv.conf`，记录 nameserver 后面的地址（Windows 系统虚拟网卡的地址）

取消以下两行的注释，禁用自动重新生成配置文件：

```text
[network]
generateResolvConf = false
```

### 配置 DISPLAY 环境变量

编辑 `~/.bashrc`：

```bash
# Windows 里 WSL 网卡的 IP 每次启动都会变，使用以下命令动态设置
export DISPLAY=$(awk '/nameserver / {print $2; exit}' /etc/resolv.conf 2>/dev/null):0
```

启动 Xfce4：

```bash
startxfce4
```

### Windows 防火墙配置

**Xfce4 图形界面：**

- 需要选择"公用网络"，否则执行 `startxfce4` 后会报错"无法连接"

**固定 IP 配置：**

- 添加高级规则：允许 TCP 端口 0

### Xfce4 快捷键

- `Alt + Enter` - 全屏
- `Alt + F2` - 新建窗口
- `Alt + F3` - 搜索文本
- `Ctrl + [Shift] + Tab` - 切换窗口
- `Ctrl + = + - 0` - 缩放
- `Ctrl + Click` - 打开光标处的文件、目录名或网址

---

## WSL 管理

### Linux 内核更新包

- [WSL2 Linux 内核](https://docs.microsoft.com/en-us/windows/wsl/wsl2-kernel)

### wslconfig 命令

```bash
# 列出当前已安装且可用的发行版
wslconfig /list

# 列出所有发行版（包括正在安装、卸载和已损坏的）
wslconfig /list /all

# 卸载已安装的发行版
wslconfig /unregister <DistributionName>
```

### 迁移 WSL 磁盘到其他盘符

以管理员身份运行 PowerShell：

```powershell
# 查看当前发行版
wsl -l

# 导出发行版
wsl --export Ubuntu D:\workspace\wsl\ubuntu-wsl.tar

# 注销原发行版
wsl --unregister Ubuntu

# 创建目标目录
mkdir D:\workspace\vm\ubuntu-wsl

# 导入到新位置
wsl --import Ubuntu D:\workspace\vm\ubuntu-wsl D:\workspace\wsl\ubuntu-wsl.tar

# 验证
wsl -l
```

---

## 网络相关

### WSL2 图形化支持

参考：[WSL2 图形化应用](https://zhuanlan.zhihu.com/p/150555651)

### WSL2 IP 动态变化问题

参考：[WSL Issue #4210](https://github.com/microsoft/WSL/issues/4210)

在 Windows 中可以直接访问 `localhost:端口`，WSL2 会自动将所有端口映射到 Windows 的 localhost。

### VPN 连接后 WSL 网络问题

#### 问题现象

- 连接 VPN 后，WSL2 完全无法访问网络
- DNS 解析失败或超时

#### 根本原因

- WSL2 默认使用 NAT 网络模式，有独立的虚拟网络
- VPN 连接后，Windows 的路由表发生变化
- WSL2 的虚拟网络无法正确通过 VPN 隧道路由流量
- DNS 服务器被 VPN 覆盖，WSL2 无法使用正确的 DNS

#### 解决方案：使用镜像网络模式

镜像网络模式（`networkingMode=mirrored`）类似 Docker 的 `--network host` 模式：

- WSL2 直接使用 Windows 的网络栈（不再使用 NAT）
- WSL2 和 Windows 共享相同的网络接口和 IP 地址
- VPN 的路由规则和 DNS 配置直接应用到 WSL2
- 完美解决 VPN、代理、DNS 等网络问题

#### 配置方法

编辑 `C:\Users\<用户名>\.wslconfig`，添加镜像网络配置（详见下方配置示例）

#### 验证配置

```bash
# 重启 WSL
wsl --shutdown
wsl

# 在 WSL 中测试
ping baidu.com
ping google.com

# 检查 IP（应该与 Windows 相同）
ip addr show eth0

# Windows 中查看 IP
ipconfig
```

## .wslconfig 配置文件

配置文件位置：`C:\Users\<用户名>\.wslconfig`

**注意事项：**

- 确保使用 UTF-8 无 BOM 编码保存（推荐使用 VS Code）
- 修改后需要执行 `wsl --shutdown` 重启生效

```bash
[wsl2]
# 限制 WSL2 虚拟机最大使用 5GB 内存。
memory=5GB
# 分配给 WSL2 虚拟机的 CPU 核心数。
processors=6
swap=8GB
# 镜像网络模式 - 解决 VPN 连接后 WSL 网络问题
# 类似 Docker 的 host 网络模式，WSL2 直接使用 Windows 的网络栈
# WSL2 和 Windows 共享相同的 IP 地址和网络接口
# 优点：完美兼容 VPN、代理、DNS，网络性能最佳
# 要求：WSL 2.0.0+ 和 Windows 11 22H2+
networkingMode=mirrored
nestedVirtualization=false
debugConsole=false
# DNS 隧道 - 确保 DNS 解析正常工作
dnsTunneling=true
# 防火墙 - 使用 Windows 的防火墙规则
firewall=true
# 自动代理 - 自动继承 Windows 的代理设置
autoProxy=true

[experimental]
autoMemoryReclaim=gradual
sparseVhd=true
```

### 配置参数说明

路径：`%UserProfile%\.wslconfig` 或 `C:\Users\user0\.wslconfig`

```ini
[wsl2]
# 自定义 Linux 内核的绝对路径 (Windows 路径)
kernel=<path>

# 分配给 WSL2 虚拟机的内存大小
memory=<size>

# 分配给 WSL2 虚拟机的 CPU 核心数
processors=<number>

# 交换空间大小，设置为 0 表示不使用交换文件
swap=<size>

# 交换文件的绝对路径 (Windows 路径)
swapFile=<path>

# 是否允许从主机通过 localhost:port 访问 WSL2 中绑定的端口（默认 true）
localhostForwarding=<bool>
```

**参数格式说明：**

- `<path>` - Windows 绝对路径，使用转义反斜杠，如 `C:\\Users\\Ben\\kernel`
- `<size>` - 大小后跟单位，如 `8GB` 或 `512MB`

### 自动启动服务

参考：[WSL2 Hacks - 自动启动服务](https://github.com/shayne/wsl2-hacks)

---

## Windows Terminal 配置

### 设置默认打开路径

打开 Windows Terminal 设置（`Ctrl + ,`），找到对应的 WSL 配置：

```json
{
    "guid": "{07b52e3e-de2c-5db4-bd2d-ba144ed6c273}",
    "hidden": false,
    "name": "Ubuntu-20.04",
    "source": "Windows.Terminal.Wsl",
    "startingDirectory": "\\\\wsl$\\Ubuntu-20.04\\home\\wiloon"
}
```

修改 `startingDirectory` 为你想要的默认路径。

### 设置默认 Shell

修改 `defaultProfile` 的值为对应的 `guid`：

```json
{
    "defaultProfile": "{c6eaf9f4-32a7-5fdc-b5cf-066e8a4b1e40}"
}
```

将 `guid` 替换为你配置文件中的相应值。

---

## 其他

### Windows 访问 WSL2 文件

在文件资源管理器地址栏输入：

```text
\\wsl$\Ubuntu-20.04\home\wiloon
\\wsl$\Ubuntu-20.04\usr\bin\git
```

---

## 参考资料

- [WSL2 图形化应用](https://discourse.ubuntu.com/t/getting-graphical-applications-to-work-on-wsl2/11868)
- [Ubuntu WSL 运行图形应用](https://wiki.ubuntu.com/WSL#Running_Graphical_Applications)
- [Windows10 下使用 Linux - WSL 与桌面环境安装](https://c1oudust.me/blog/Windows10%E4%B8%8B%E4%BD%BF%E7%94%A8Linux%E7%9A%84%E5%8F%A6%E4%B8%80%E7%A7%8D%E6%96%B9%E5%BC%8F%20%E2%80%94%E2%80%94%20WSL%E4%B8%8E%E5%85%B6%E6%A1%8C%E9%9D%A2%E7%8E%AF%E5%A2%83%E5%AE%89%E8%A3%8520180509/)
- [如何在 WSL 上运行 Linux GUI 软件](http://www.yuan-ji.me/%E5%A6%82%E4%BD%95%E5%9C%A8Windows-Subsystem-for-Linux-(WSL)-%E4%B8%8A%E8%BF%90%E8%A1%8CLinux-GUI-%E8%BD%AF%E4%BB%B6/)
- [Ubuntu 18.04 DBus 修复说明](https://www.reddit.com/r/bashonubuntuonwindows/comments/9lpc0o/ubuntu_1804_dbus_fix_instructions_with/)
- [WSL 教程](https://github.com/QMonkey/wsl-tutorial)
- [ArchWSL](https://github.com/yuk7/ArchWSL)
- [WSL 使用指南](https://zhuanlan.zhihu.com/p/34884285)
- [WSL 基本命令](https://docs.microsoft.com/zh-cn/windows/wsl/basic-commands)

## ArchWSL

- [ArchWSL 安装文档](https://wsldl-pg.github.io/ArchW-docs/How-to-Setup/)

**注意：** `WSL_DEBUG_CONSOLE=true` 这个环境变量在 WSL 1.1.0 之后已被废弃，在 WSL 1.2.x / 2.x.x (Microsoft Store 版本) 中已被完全移除或忽略。

### 配置镜像源

ArchWSL 可以直接使用常规的 ArchLinux 镜像源，推荐使用国内镜像提升速度。

编辑 `/etc/pacman.d/mirrorlist`：

```bash
sudo nano /etc/pacman.d/mirrorlist
```

在文件开头添加国内镜像（任选其一）：

```text
# 清华源（推荐）
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch

# 阿里云
Server = https://mirrors.aliyun.com/archlinux/$repo/os/$arch

# 中科大
Server = https://mirrors.ustc.edu.cn/archlinux/$repo/os/$arch
```

### 初始化和更新系统

```bash
# 初始化 keyring（首次可能需要）
sudo pacman-key --init
sudo pacman-key --populate archlinux

# 更新系统
sudo pacman -Syu
```

### WSL 重启说明

**重要：WSL 中不能使用 `reboot` 命令**

- WSL 是运行在 Windows 上的子系统，不是独立虚拟机
- `reboot`、`shutdown` 等命令在 WSL 中不起作用

**正确的重启方法：**

```powershell
# 在 Windows PowerShell 或 CMD 中执行

# 方法 1: 关闭所有 WSL 实例
wsl --shutdown

# 方法 2: 只关闭 ArchLinux
wsl --terminate ArchLinux
wsl -t ArchLinux

# 然后重新启动
wsl -d ArchLinux
```

**何时需要重启 WSL：**

- 更新了 Linux 内核（`linux` 包）
- 更新了 systemd 或底层库（如 glibc）
- 修改了 `.wslconfig` 配置文件

**大部分软件包更新后无需重启，直接可用。**

### 验证配置是否生效

```bash
# 查找 WSL 安装位置
where wsl
# 新版 WSL 安装在：C:\Users\<你>\AppData\Local\Microsoft\WindowsApps\wsl.exe

# 强制更新到 Store 版 WSL
wsl --update

# 验证 .wslconfig 是否生效
free -h
nproc
```

---

## 1Password SSH Agent 与 WSL 集成

1Password 提供了优雅的 SSH 密钥管理方案，可以与 WSL 完美集成。

### 官方文档

- [1Password SSH Agent 与 WSL 集成](https://developer.1password.com/docs/ssh/integrations/wsl/)

### 前置条件

- 1Password 8 或更高版本
- WSL 2
- 1Password 订阅账户

### 配置步骤

#### 1. 启用 Windows OpenSSH Authentication Agent 服务

1. 按 `Win + R` 打开运行窗口
2. 输入 `services.msc` 按回车
3. 找到 **OpenSSH Authentication Agent**
4. 右键 → 属性 → 启动类型 → 自动
5. 点击“启动”

#### 2. 在 Windows 中启用 1Password SSH Agent

1. 打开 1Password 应用
2. 点击右上角的 **设置图标**（齿轮图标）
3. 选择 **Settings** → **Developer**
4. 找到 **SSH Agent** 部分
5. 勾选 ✅ **Use the SSH agent**
6. 勾选 ✅ **Integrate with 1Password CLI**

**注意：**

- 在 1Password 8.11.x 版本中，WSL 集成是通过启用 SSH Agent 自动实现的
- 不是所有版本都显示独立的 "Integrate with WSL" 选项
- 只要启用了 "Use the SSH agent"，WSL 集成就会自动生效

#### 3. 在 WSL 中配置环境变量

编辑 `~/.bashrc` 或 `~/.zshrc`：

```bash
# 1Password SSH Agent 集成
export SSH_AUTH_SOCK=$HOME/.1password/agent.sock
```

应用配置：

```bash
source ~/.bashrc  # 或 source ~/.zshrc
```

#### 4. 验证配置

```bash
# 查看已加载的 SSH 密钥
ssh-add -l

# 测试 SSH 连接（以 GitHub 为例）
ssh -T git@github.com
```

### 在 1Password 中添加 SSH 密钥

#### 方法 1：导入现有密钥

1. 打开 1Password
2. 点击 "+" 创建新项目
3. 选择 "SSH Key"
4. 点击 "Choose file" 导入私钥文件
5. 可选：添加密钥的公钥和备注信息

#### 方法 2：生成新密钥

1. 打开 1Password
2. 创建新项目 → SSH Key
3. 点击 "Generate new key"
4. 1Password 会自动生成并保存密钥对

### 配置 Git 使用 1Password SSH

```bash
# Git over SSH 自动使用 1Password Agent
git clone git@github.com:username/repo.git

# 无需额外配置，Git 会自动通过 SSH Agent 获取密钥
```

### 优势

- ✅ **自动解锁** - 使用 Windows Hello 生物识别快速解锁
- ✅ **无需密码** - SSH 连接时不再需要输入密钥密码
- ✅ **安全存储** - 私钥加密存储在 1Password 中
- ✅ **多设备同步** - 密钥自动同步到所有设备
- ✅ **操作简单** - 一次配置，永久使用

### 故障排查

#### 错误：Error connecting to agent: No such file or directory

这是最常见的问题，说明 1Password SSH Agent socket 文件不存在。

**排查步骤：**

```bash
# 1. 检查 socket 文件是否存在
ls -la ~/.1password/agent.sock

# 2. 检查 1Password 是否正在运行
# 在 Windows 任务管理器中确认 1Password.exe 进程存在

# 3. 检查 1Password 是否已解锁
# 打开 1Password 应用，确保已登录并解锁
```

**解决方案：**

1. 打开 1Password Windows 应用
2. 进入 Settings → Developer
3. 确认 ✅ "Use the SSH agent" 已勾选
4. **重启 1Password**（完全退出后重新打开）
5. 重启 WSL：

```powershell
# 在 Windows PowerShell 中执行
wsl --shutdown
```

#### 密钥未显示或为空

```bash
# 确认环境变量已设置
echo $SSH_AUTH_SOCK
# 应该输出：/home/username/.1password/agent.sock

# 检查 1Password 中是否有 SSH 密钥
# 打开 1Password → 查看是否有 "SSH Key" 类型的项目
```

### 其他方案对比

| 方案 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| **1Password SSH Agent** | 官方支持、配置简单、体验最佳 | 需要订阅 | ⭐⭐⭐⭐⭐ |
| KeePassXC + npiperelay | 开源免费、自主可控 | 配置复杂、需手动维护 | ⭐⭐⭐ |
| Windows SSH Agent | 系统原生、无需额外软件 | 功能有限、密钥管理不便 | ⭐⭐ |

**推荐：** 对于 WSL 使用场景，强烈推荐 1Password SSH Agent 方案，配置更简单，使用更流畅。
