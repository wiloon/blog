---
title: "mise: 按目录切换工具版本"
author: "-"
date: 2026-10-20T06:15:51+08:00
lastmod: 2026-10-21T11:01:06+08:00
url: mise
categories:
  - development
tags:
  - mise
  - version-manager
  - dev-env
  - remix
  - AI-assisted
---

## 解决什么问题

同一台机器上，不同项目要的工具版本常常不一样：一个项目锁 Node 24，另一个已经升到 Node 26；CI 用 Go 1.27，本机系统包里是别的版本。

常见的几种做法各有问题：

| 做法 | 问题 |
| ---- | ---- |
| 系统包管理器（pacman、Homebrew） | 一个工具只有一个版本，全局生效；要 root 或会影响全系统；版本跟着发行版走，不跟项目走 |
| 每种语言一个版本管理器（nvm / fnm、pyenv、gvm、SDKMAN） | 每个都要单独安装、单独配置 shell，切版本的方式各不相同 |
| 手动下载解压，改 PATH | 换项目时要记得手动切，很容易用错版本 |

[mise](https://github.com/jdx/mise)（读作 "meez"，原名 rtx）是一个统一的工具版本管理器，用 Rust 写的。它的核心功能是：**在项目目录里写一个 `mise.toml` 声明要哪些工具、哪个版本，进入这个目录时自动用这些版本，离开就恢复。** 一个工具管所有语言和 CLI。

它最早是 asdf 的替代品，兼容 asdf 的 `.tool-versions` 文件，但更快，也不需要为每个工具单独装插件。

## 三个功能

mise 现在做三件事，都写在同一个 `mise.toml` 里：

```toml
[tools]
go = "1.27.0"
node = "24.21.0"
task = "latest"
golangci-lint = "2.14.0"

[env]
GOPROXY = "https://goproxy.cn,direct"

[tasks.test]
run = "go test ./..."
```

- **`[tools]`**：工具版本，这是主要功能。
- **`[env]`**：进入目录时设置的环境变量，类似 direnv。
- **`[tasks]`**：项目命令，`mise run test` 执行，类似 make 或 Task。

后两个是可选的，只用 `[tools]` 也完全可以。

## 配置怎么生效

### 沿父目录向上合并

mise 从当前目录开始，一路向上找 `mise.toml`（以及 `.mise.toml`、`.tool-versions`），最后合并全局配置 `~/.config/mise/config.toml`。离当前目录越近的优先级越高。

所以一个配置文件可以管住它下面的所有子目录。比如我在 ser8 上跑无人值守 agent，配置放在 `~/enx-agent/mise.toml`，下面的仓库克隆和每个 git worktree 都自动用这里锁定的版本，出了这个目录又回到全局的 Node 26。仓库本身不需要知道 mise 的存在。

### 两种接入方式

mise 有两种方式让 shell 找到正确版本的命令：

| 方式 | 原理 | 适合 |
| ---- | ---- | ---- |
| `mise activate` | 在 `~/.zshrc` 里加 `eval "$(mise activate zsh)"`，每次显示提示符或 `cd` 时，mise 直接改 `PATH` | 交互式 shell，开销最小 |
| shims | 把 `~/.local/share/mise/shims` 放进 `PATH`，里面每个命令（`node`、`go`…）都是一个小程序，运行时按当前目录找版本再转发 | 非交互场景：IDE、systemd 服务、cron、脚本 |

ser8 上的 agent 由 systemd 计时器启动，没有交互式 shell，所以它的 `env.sh` 用的是 shims：

```bash
export PATH="$HOME/.local/share/mise/shims:$HOME/.local/bin:$PATH"
```

新装了带命令的工具后，shims 有时需要 `mise reshim` 重新生成。

### `mise trust`

`mise.toml` 能设置环境变量、定义任务，克隆一个陌生仓库时如果自动执行，就有安全风险。所以 mise 默认不信任新出现的配置文件，第一次要手动执行：

```bash
mise trust mise.toml
```

## 常用命令

```bash
# Pin a version for this directory (writes ./mise.toml)
mise use node@24.21.0

# Pin a global default (writes ~/.config/mise/config.toml)
mise use -g node@26

# Install everything the current config asks for
mise install

# What is active here, and where it comes from
mise ls --current
mise which node

# Run one command with a version, without changing any config
mise exec go@1.27.0 -- go version
```

## 工具从哪里来

`mise use` 后面的名字由不同的后端（backend）负责下载：

- **核心工具**：Node、Python、Go、Java、Ruby 等，mise 内置支持。
- **aqua / GitHub releases**：大部分单文件 CLI（gh、task、golangci-lint）直接从发布页下载二进制。
- **语言包管理器**：`npm:`、`cargo:`、`pipx:`、`go:` 前缀，比如 `npm:@anthropic-ai/claude-code`。
- **asdf 插件**：兜底，兼容老生态。

装好的工具都在 `~/.local/share/mise/installs/` 下，按用户安装，不需要 root，也不碰系统包。

## 和系统包的关系

在 Arch 这种滚动更新的发行版上，系统包里的 Go 今天是 1.27，明天就可能变成 1.28。mise 锁定的版本不受影响，因为两者是两份完全独立的文件：

| | pacman 装的 Go | mise 装的 Go 1.27.0 |
| ---- | ---- | ---- |
| 位置 | `/usr/bin/go`、`/usr/lib/go` | `~/.local/share/mise/installs/go/1.27.0/` |
| 来源 | Arch 仓库 | Go 官方发布的压缩包 |
| 更新 | `pacman -Syu` 时跟着升级 | 只有改 `mise.toml` 里的版本号才会变 |

`pacman -Syu` 只会改 `/usr` 下的文件，不会碰 mise 的安装目录。至于运行 `go` 时用哪一个，取决于 `PATH` 里谁排在前面：mise 的 shims（或 `mise activate` 加进来的路径）放在 `/usr/bin` 前面，在 `mise.toml` 管辖的目录里运行 `go`，拿到的就是 1.27.0。出了这些目录，mise 没有可用版本时就落回系统的 `/usr/bin/go`；如果全局配置也没设、系统也没装，shim 会直接报错 `No version is set for shim: go`，而不是悄悄用错版本。

所以两者分工是：

- **系统级、常驻的工具交给系统包管理器**，比如 `cursor-cli`、`git`，跟着系统一起升级。Arch 不支持部分升级，pacman 数据库旧了就应该 `pacman -Syu` 全系统升级，不该为了绕开它改用 mise 装。
- **需要按项目锁定版本的工具交给 mise**，比如 Go、Node、golangci-lint：项目要求的版本和 CI 一致，不随系统升级而变。

## 和 fnm、asdf 比较

| | fnm | asdf | mise |
| ---- | ---- | ---- | ---- |
| 管哪些工具 | 只管 Node | 所有，靠插件 | 所有，大部分内置 |
| 实现 | Rust | Shell 脚本 | Rust |
| 切换方式 | 改 PATH | 只有 shims（每次调用都有开销） | activate 或 shims，二选一 |
| 读取的版本文件 | `.nvmrc`、`.node-version` | `.tool-versions` | `mise.toml`、`.tool-versions`，可选读 `.nvmrc` 等 |
| 环境变量、任务 | 无 | 无 | 有 |

如果只写 Node，fnm 已经够用；同时用好几种语言和一堆 CLI 时，mise 能把它们收进一个配置文件。

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-21 | 删掉"pacman 数据库没同步所以用 mise"的说法，新增「和系统包的关系」一节 | 旧的数据库应该 `pacman -Syu` 解决；补充滚动更新下 mise 锁定版本为什么不受影响 |
