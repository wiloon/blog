---
title: 开源离线词典
author: "-"
date: 2026-05-23T10:21:41+08:00
lastmod: 2026-05-23T10:21:41+08:00
url: open-source-dictionaries
categories:
  - English
tags:
  - english
  - Linux
  - remix
  - AI-assisted
---

## 概述

离线查词依赖两样东西：**词典客户端**（软件）和**词库文件**（数据）。客户端负责检索、取词、发音；词库决定收词量、释义质量和标注信息。下面按数据来源和格式，整理几类常用的开源 / 开放词库。

常见客户端：

| 客户端 | 平台 | 主要格式 |
| --- | --- | --- |
| [GoldenDict](https://github.com/goldendict/goldendict) | Linux / Windows / macOS | StarDict、MDX |
| [StarDict / 星际译王](http://www.huzheng.org/stardict/index_cn.php) | Linux / Windows | StarDict |
| [sdcv](https://dushistov.com/software/sdcv/) | 命令行 | StarDict |
| [MDict](https://www.mdict.cn/) | Windows / Android / iOS | MDX / MDD |
| [欧陆词典](https://www.eudic.net/) | 全平台 | 欧陆原生 / MDX |
| [Bob](https://github.com/ripperhe/Bob) | macOS | 多种插件后端 |

## ECDICT

[ECDICT](https://github.com/skywind3000/ECDICT) 是 skywind3000 维护的**英文→中文双解词典数据库**，MIT 协议。收词量大，每条记录除中英文释义外，还标注考试大纲（四六级、雅思、托福等）、柯林斯星级、牛津 3000、BNC / COCA 词频，以及动词时态变形（`exchange` 字段）。

数据以 CSV 存储于 GitHub 仓库（约 76 万词条的基础版）；完整版压缩包见 `stardict.7z`。本地使用建议转为 SQLite（仓库自带 `stardict.py`，提供 `DictCsv` / `StarDict` / `DictMySQL` 三类接口），查询速度远快于直接读 CSV。

基于 ECDICT 数据生成的成品词典《简明英汉字典增强版》可在 [Releases](https://github.com/skywind3000/ECDICT/releases) 下载，格式包括：

| 文件 | 格式 | 说明 |
| --- | --- | --- |
| `ecdict-mdx-28.zip` | MDX | 有音标 |
| `ecdict-mdx-headless-28.zip` | MDX | 无音标（与其他词典并排时更紧凑） |
| `ecdict-stardict-28.zip` | StarDict | 轻量纯文本 |
| `ecdict-eudic-28.zip` | 欧陆原生 | 加载速度较快 |
| `ecdict-mobi-28.zip` | MOBI | Kindle |
| `ecdict-sqlite-28.zip` | SQLite | 供程序直接读取 |

GoldenDict 需 1.5 及以上版本才支持 MDX 格式。

## StarDict（星际译王）开放词库

[StarDict](http://www.huzheng.org/stardict/index_cn.php) 是跨平台离线词典软件，GPL 授权。其词库格式开放，每本词典通常包含 `.ifo`（元数据）、`.idx`（索引）、`.dict`（正文），可选 `.syn`（同义词）。

词库安装路径：

- Linux：`/usr/share/stardict/dic/` 或 `~/.stardict/dic/`
- macOS：`/Applications/StarDict.app/Contents/Resources/share/stardict/dic/`
- Windows：`C:\Program Files\StarDict\dic\`

官方词库下载站：[download.huzheng.org](http://download.huzheng.org/)，收录英汉 / 汉英、维基百科离线版、康熙字典等上千本免费词典。解压 `.tar.bz2` 后放入上述目录即可。

命令行用户可安装 `sdcv`（StarDict 控制台版本），配合 StarDict 格式词库在终端查词：

```bash
# Arch Linux
sudo pacman -S sdcv

sdcv hello
```

[FreeDict](https://freedict.org/downloads/) 项目也提供 StarDict 格式的多语种开源词典，GoldenDict、sdcv 等均可加载。

## Skywind 词典系列

[skywind3000](https://github.com/skywind3000) 除 ECDICT 数据库外，还基于开源资料整合制作了多本成品词典，均可离线使用：

| 词典 | 说明 |
| --- | --- |
| [简明英汉字典增强版](https://github.com/skywind3000/ECDICT/wiki/%E7%AE%80%E6%98%8E%E8%8B%B1%E6%B1%89%E5%AD%97%E5%85%B8%E5%A2%9E%E5%BC%BA%E7%89%88) | 基于 ECDICT，收词 300 万+，含词频与考纲标注 |
| [简明英汉必应版](https://github.com/skywind3000/ECDICT) | 整合必应词典开源数据 |
| [单词释义比例词典](https://github.com/skywind3000/ECDICT) | 标注各词性在语料库中的出现比例 |
| [近义词辨析词典](https://github.com/skywind3000/ECDICT) | 近义词对比与用法说明 |

上述成品词典均提供 MDX、StarDict、欧陆等格式，下载入口见 ECDICT 仓库 Wiki 与 Releases 页面。

## FreeMdict 词库合集

[FreeMdict](https://freemdict.com/) 是 MDict 格式（`.mdx` / `.mdd`）词库的社区下载站，免注册直链，收录英汉、汉英、百科等各语种词典。体量大，例如 [100G Super Big Collection](https://downloads.freemdict.com/100G_Super_Big_Collection/) 目录按词典名称组织，按需下载即可。

MDX 词库可用于 GoldenDict（1.5+）、MDict 移动端、欧陆词典等客户端。制作 MDX 词库的工具链：

- [MdxBuilder / MdxExport](https://www.mdict.cn/) — 官方打包 / 解包工具（Windows）
- [AutoMdxBuilder](https://github.com/Litles/AutoMdxBuilder) — 跨平台自动化制作，支持 PDF 转词典等

## 选用建议

- **日常桌面查词**：GoldenDict + ECDICT StarDict 版（轻量）或 MDX 版（排版更好）；macOS 可用 Bob 插件接入。
- **终端 / 脚本**：`sdcv` + StarDict 词库，或直接用 ECDICT 的 SQLite + `stardict.py`。
- **移动端**：MDict / 欧陆加载 MDX 词库；Kindle 用户用 ECDICT 的 MOBI 版。
- **二次开发 / 制卡**：ECDICT CSV / SQLite 原始数据最灵活，词频和考纲标注可直接用于 Anki 筛词。
