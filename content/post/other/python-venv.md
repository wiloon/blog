---
title: python 虚拟环境
author: "-"
date: -001-11-30T00:00:00+00:00
draft: true
url: python/venv
categories:
  - Inbox
tags:
  - reprint
---
## PDM

https://pdm-project.org/zh-cn/latest/

https://juejin.cn/post/7315126100539473930

PDM 是一个支持最新 PEP 标准的现代 Python 包和依赖项管理器

PDM（Python Development Master）是一款新一代的 Python 包管理工具，旨在提供更为现代化、可靠且灵活的解决方案。与传统的 pip 和 Poetry 相比，PDM 在依赖版本管理、项目隔离和性能优化等方面展现出独特的优势。

```Bash
# install pdm
curl -sSL https://pdm-project.org/install-pdm.py | python3 -
# 安装程序会将 PDM 安装到用户家目录中, linux 系统
#$HOME/.local/bin Unix 系统

```

## conda

https://zhuanlan.zhihu.com/p/554965293

conda可以理解为一个工具，其核心功能是包管理与环境管理。
conda 不会依赖于系统中已经存在的 python 进行运行。因此 conda 拥有较高的独立性以及强悍的跨版本支持，在多版本管理上
每个虚拟环境中均包含了一个完整的 python
conda 的虚拟环境更像是对整个开发环境的虚拟，而不是 poetry 和 pdm 那种在解释器层面的虚拟
