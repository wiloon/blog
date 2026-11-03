---
title: "direnv: 按目录加载和卸载环境变量"
author: "-"
date: 2026-11-03T17:05:31+08:00
lastmod: 2026-11-03T17:05:31+08:00
url: direnv
categories:
  - development
tags:
  - direnv
  - shell
  - dev-env
  - remix
  - AI-assisted
---

## direnv 是什么

direnv 是一个 shell 扩展：`cd` 进一个目录时，它执行这个目录（或上级目录）里的 `.envrc`，把其中 `export` 的变量加进当前 shell；`cd` 出去时，再把这些变量还原。

和把变量写进 `~/.zshrc` 相比，区别有两点：

- 变量只在需要的目录下存在，离开就消失，不会污染所有终端。
- 不同目录可以给同一个变量不同的值，比如 `GH_TOKEN` 在 A 组织目录下是 A 的 token，在 B 组织目录下是 B 的。

[mise](./mise.md) 的 `[env]` 也能按目录设置变量，但 direnv 只做这一件事，`.envrc` 就是一段普通的 shell 脚本，可以调用任何命令。

## 安装和接入 shell

```bash
# macOS
brew install direnv

# Arch Linux
sudo pacman -S direnv
```

装好后要在 shell 配置里加 hook，否则 direnv 不会生效。zsh 加在 `~/.zshrc` 靠后的位置：

```bash
# Load per-directory .envrc files
if command -v direnv >/dev/null 2>&1; then
  eval "$(direnv hook zsh)"
fi
```

bash 把 `zsh` 换成 `bash`，写进 `~/.bashrc`。改完开一个新终端，或者 `source ~/.zshrc`。

## 基本用法

在项目目录写一个 `.envrc`：

```bash
export APP_ENV=dev
export DATABASE_URL=postgres://localhost:5432/app
```

第一次进入这个目录时，direnv 会拒绝执行：

```text
direnv: error /path/to/project/.envrc is blocked. Run `direnv allow` to approve its content
```

这是 direnv 的安全设计：`.envrc` 是可执行的脚本，如果 `git clone` 下来的仓库自带 `.envrc`，不经确认就执行会很危险。所以每个 `.envrc` 都要先 `direnv allow`，**文件内容一改，就要重新 allow**。

```bash
direnv allow     # approve the current .envrc
direnv deny      # revoke approval
direnv reload    # re-run .envrc, e.g. after an external state change
direnv status    # show which .envrc is loaded and whether it is allowed
```

进入和离开目录时，终端会提示加载了哪些变量：

```text
direnv: loading ~/project/.envrc
direnv: export +APP_ENV +DATABASE_URL
```

## 作用范围：当前目录和所有子目录

direnv 从当前目录往上找，用找到的**第一个** `.envrc`。所以放在 `~/workspace/org-a/.envrc` 的配置，对 `~/workspace/org-a/` 下的所有仓库都生效，不用每个仓库放一份。

如果子目录也有自己的 `.envrc`，默认不会再加载上级的那份。需要两份都加载，在子目录的 `.envrc` 里写：

```bash
source_up   # also load the nearest .envrc in a parent directory
```

## 常用的 stdlib 函数

`.envrc` 里除了普通 shell 语句，还能用 direnv 自带的函数：

| 函数 | 作用 |
| --- | --- |
| `PATH_add bin` | 把相对路径 `bin` 加到 `PATH` 前面 |
| `dotenv` | 加载同目录的 `.env` 文件（`KEY=value` 格式） |
| `source_up` | 继续加载上级目录的 `.envrc` |
| `source_env path` | 加载指定的 `.envrc` 文件 |
| `log_status msg` | 打印提示信息 |
| `log_error msg` | 打印错误信息（不会中断） |

完整列表：`direnv stdlib`。

## 例子：按 GitHub 组织自动切换 token

这是我实际在用的场景。我有一个个人 GitHub 账号和几个组织，每个组织一个 fine-grained PAT（区别见 [Classic vs Fine-grained PAT](./github-personal-access-token-classic-vs-fine-grained.md)）。fine-grained PAT 只能选一个 resource owner，用错 token 就会 404，或者报 `Resource not accessible by personal access token`。

token 都存在 [Bitwarden](../inbox/bitwarden.md) 里，用命令行客户端 `rbw` 读取。本地目录按组织分开：

```text
~/workspace/
├── org-a/      # repos of GitHub org "org-a"
│   └── .envrc
├── org-b/      # repos of GitHub org "org-b"
│   └── .envrc
└── projects/   # personal repos, no .envrc
```

`~/workspace/org-a/.envrc`：

```bash
# Org-scoped GitHub token for everything under this directory.
# The token stays in Bitwarden; it only lives in this shell while inside the directory.
org=org-a
if rbw unlocked >/dev/null 2>&1; then
  token="$(rbw get "github/org/token/$org")"
  if [ -n "$token" ]; then
    export GH_TOKEN="$token"             # used by gh CLI
    export TF_VAR_github_token="$token"  # used by OpenTofu / Terraform GitHub provider
  else
    log_error "rbw has no entry github/org/token/$org"
  fi
else
  log_error "rbw is locked: run 'rbw unlock', then 'direnv reload'"
fi
```

效果：

- 进入 `~/workspace/org-a/` 下的任何仓库，`gh pr create`、`tofu plan` 自动用 org-a 的 token。
- 进入 org-b 的目录，自动换成 org-b 的 token。
- 回到 `~/workspace/projects/`，变量被卸载，`gh` 回到 `gh auth login` 存在钥匙串里的个人账号。

几点说明：

- `GH_TOKEN` 和 `TF_VAR_github_token` 这两个名字不是自己起的：`GH_TOKEN` 是 gh CLI 固定读取的变量名；`TF_VAR_<name>` 是 OpenTofu / Terraform 的约定，用来给模块里名为 `<name>` 的 input variable 赋值，这里对应模块里的 `variable "github_token"`。如果想要一个自己看得懂的名字，可以再导出一个 `GITHUB_ORG_TOKEN`，让上面两个都引用它。
- `.envrc` 里**没有 token 本身**，只有一条读取命令，所以这个文件不算敏感。不过它不在任何 git 仓库里（放在仓库的上一级目录），本来也不会被提交。
- 先判断 `rbw unlocked` 再读取，是因为 vault 锁定时，`rbw get` 会尝试弹出密码输入框；在某些场景下它弹不出来，只会返回空字符串。
- 空 token 必须拦下来。`gh` 和 GitHub provider 发现 token 为空时，会**悄悄退回**去用别的凭据（环境变量 `GITHUB_TOKEN`，或者 gh 存的个人登录），结果就是用错 token，还不容易看出来。

同样的思路也适用于其他需要按目录区分的凭据，比如用 [SOPS](../cloud/sops.md) 解密配置：在 `.envrc` 里调用 `sops decrypt`。

## 需要注意的地方

**只在交互式 shell 里生效。** hook 是挂在 shell 提示符上的：每次显示提示符前，direnv 检查一次当前目录。所以脚本、CI、编辑器插件或其他程序启动的非交互 shell **不会**自动加载 `.envrc`。这些场景用 `direnv exec`：

```bash
# Run a command with the environment of ~/workspace/org-a/.envrc
direnv exec ~/workspace/org-a/ gh repo list org-a
```

**环境变量只在进程启动时继承。** 一个程序（比如编辑器、Claude Code 之类的长时间运行的进程）是在你改 `.envrc` 或删掉 `~/.zshrc` 里的变量**之前**启动的，它手里还是旧值，要重启这个程序才会更新。

**改了外部状态要 `direnv reload`。** 例如在 `.envrc` 加载时 rbw 还没解锁，解锁之后要 `direnv reload` 才会重新读取。

**不要把明文密钥写进 `.envrc` 再提交。** 如果项目的 `.envrc` 要进 git，把敏感值放在 `.env` 里用 `dotenv` 加载，并把 `.env` 加进 `.gitignore`；更好的做法是像上面那样，从密码管理器里现取。

## 参考

- [direnv 官网](https://direnv.net/)
- [direnv stdlib](https://direnv.net/man/direnv-stdlib.1.html)
- [GitHub: direnv/direnv](https://github.com/direnv/direnv)
