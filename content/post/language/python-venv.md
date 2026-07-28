---
title: "Python venv, 虚拟环境与包管理工具（pdm、conda、pipx）"
author: "-"
date: 2025-11-24T08:30:00+08:00
lastmod: 2026-07-28T12:20:01+08:00
draft: true
url: python/venv
categories:
  - language
tags:
  - python
  - remix
  - AI-assisted
---
## PDM

https://pdm-project.org/zh-cn/latest/

https://juejin.cn/post/7315126100539473930

PDM 是一个支持最新 PEP 标准的现代 Python 包和依赖项管理器

PDM（Python Development Master）是一款新一代的 Python 包管理工具，旨在提供更为现代化、可靠且灵活的解决方案。与传统的 pip 和 Poetry 相比，PDM 在依赖版本管理、项目隔离和性能优化等方面展现出独特的优势。

```Bash
# install pdm
sudo apt install python3.10-venv
curl -sSL https://pdm-project.org/install-pdm.py | python3 -
# 安装程序会将 PDM 安装到用户家目录中, linux 系统
#$HOME/.local/bin Unix 系统

# 初始化项目
pdm sync
# 加入新的依赖包, pdm会自动维护 pyproject.toml 文件, 但是版本范围可能需要改一下
pdm add redis

# pdm install 和 pdm sync 的区别
# pdm install: 安装 pyproject.toml 中定义的所有依赖，并更新 pdm.lock（如果需要）
# pdm sync: 严格按照 pdm.lock 文件安装依赖，不会更新 lock 文件，确保环境完全一致
# 推荐使用场景：
# - 开发环境：使用 pdm install，允许依赖更新
# - 生产环境/CI：使用 pdm sync，确保依赖版本完全一致

pdm info --env

# pdm use 切换到 Python 3.14
pdm use python3.14

pdm self update
rm pdm.lock
pdm lock
```

### 配置文件

pyproject.toml

```
~=（兼容版本运算符: 例如，python-dotenv~=0.20.0 表示允许安装 python-dotenv 的版本为 0.20.0 到小于 0.21.0 之间的任何版本。

>=（大于或等于运算符）:

这个符号表示版本必须大于或等于指定的版本。
它允许依赖项更新到任何比指定版本新的版本。
例如，redis>=5.2.1 表示允许安装 redis 的版本为 5.2.1 或更高。

~= 提供了一种限制性更强的版本控制，通常用于确保兼容性， >= 则是更为开放的版本要求，允许依赖项更新到任何未来版本。
```


## conda

https://zhuanlan.zhihu.com/p/554965293

conda可以理解为一个工具，其核心功能是包管理与环境管理。
conda 不会依赖于系统中已经存在的 python 进行运行。因此 conda 拥有较高的独立性以及强悍地跨版本支持，在多版本管理上
每个虚拟环境中均包含了一个完整的 python
conda 的虚拟环境更像是对整个开发环境的虚拟，而不是 poetry 和 pdm 那种在解释器层面的虚拟

## pipx

pipx 用来安装和运行 Python 写的命令行工具：每个工具会单独建一个虚拟环境（依赖互不干扰），但可执行文件会链接到 `~/.local/bin`，效果上就是"全局可用的命令"，不需要手动 activate。

跟直接 `pip install` 或 `venv` 的区别：

- `pip install xxx`：装到系统 Python 环境里，多个工具的依赖容易互相冲突；新版 Arch/Debian 出于 [PEP 668](https://peps.python.org/pep-0668/) 会直接拒绝，报 `externally-managed-environment` 错误
- `venv`：需要 `source venv/bin/activate` 才能用，适合项目依赖隔离，不适合"随时在任意目录敲命令"的场景
- `pipx`：专门解决"我要装一个 CLI 工具，装完就想在任何目录直接用"这个需求

### 安装（Arch）

```bash
sudo pacman -S python-pipx
pipx ensurepath   # 把 ~/.local/bin 加入 PATH，需要重开终端或 source 配置文件生效
```

### 常用命令

```bash
pipx install grip      # 安装一个 CLI 工具
pipx list               # 查看已安装的工具
pipx upgrade grip        # 升级
pipx uninstall grip      # 卸载
pipx run cowsay hello    # 不安装，临时运行一次
```

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-28 | 补充 pipx 章节；标题改为含英文；分类由 Inbox 改为 language；删除 reprint 标签，补 python 标签；新增 lastmod；清理文末乱码 | 完善 Python 环境/包管理工具文档，修正不符合规范的 front matter |