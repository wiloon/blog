---
title: "Celeron J3455 Mini PC: 备用软路由"
author: "-"
date: 2026-07-23T18:30:27+08:00
lastmod: 2026-07-23T18:30:27+08:00
url: j3455-mini-pc
categories:
  - Hardware
tags:
  - Hardware
  - HomeLab
  - soft-router
  - Celeron
  - J3455
  - J4105
  - Intel-I226
  - remix
  - AI-assisted
---

## 用途

Homelab 备用软路由小主机。2026-07-23 用 Arch Linux 安装 ISO（live）从 U 盘引导后盘点硬件。

## 规格摘要

| 项目 | 详情 |
| ---- | ---- |
| CPU | Intel Celeron J3455 @ 1.50GHz（Apollo Lake，4 核 / 无超线程，睿频最高 2.3GHz） |
| 虚拟化 | VT-x（`vmx`） |
| AES-NI | 有 |
| 内存 | 4 GB DDR3-1600（系统可见约 3.7 GiB） |
| 存储 | BIWIN mSATA SSD 32 GB（SATA 3.2，序列号 `2111025802427`） |
| 网卡 | 双口 Intel I226-IT 2.5G（驱动 `igc`） |
| 显卡 | Intel HD Graphics 500 |
| BIOS | AMI Aptio CRB 5.12（2023-07-12） |
| DMI | OEM 默认字符串（`Default string` / board `Aptio CRB`） |

## 网卡

| 接口 | PCI | MAC | 备注 |
| ---- | --- | --- | ---- |
| `enp1s0` | `01:00.0` I226-IT | `00:60:e0:9b:bc:e5` | 探测时已连接，协商 2500Mb/s Full |
| `enp2s0` | `02:00.0` I226-IT | `00:60:e0:9b:bc:e6` | 探测时无链路 |

## 存储现状（装系统前）

内置 `/dev/sda` 非空盘，已有分区：

- `sda1` 16M vfat
- `sda2` 1G squashfs
- `sda3` 约 239K

正式安装前需确认是否整盘清空。

## 与 J4105 对比

J3455 与 J4105 是同一条入门级低功耗 **Celeron J 系列**产品线的上下代（BGA 焊死在主板，常见于软路由 / 小主机）。**J4105 是 J3455 的下一代**，不是同代换皮。Homelab 里另有一台 [Intel J4105 软路由](./hardware.md#intel-j4105-软路由)。

| | J3455 | J4105 |
| --- | --- | --- |
| 发布 | 约 2016（Apollo Lake） | 约 2017–2018（Gemini Lake） |
| 微架构 | Goldmont | Goldmont Plus |
| 制程 / TDP | 14nm / 10W | 14nm / 10W |
| 核心 | 4 核 4 线程 | 4 核 4 线程 |
| 频率 | 1.5 → 最高 2.3 GHz | 1.5 → 最高 2.5 GHz |
| L2 缓存 | 2 MB | 4 MB |
| 核显 | HD Graphics 500 | UHD Graphics 600 |
| 内存 | 常见 DDR3L / LPDDR3/4 | 常见 DDR4 / LPDDR4 |
| 官方内存上限 | 约 8 GB | 约 8 GB |
| 性能（大致） | 基准 | 单核 / 多核大约快 20–30% |

结合两台整机：芯片上 J4105 略强；软路由更看配置。清单里的 J4105 机是 DDR4 16G + i211 千兆；本机是 4G DDR3 + 双 I226-IT 2.5G + 32G mSATA——网卡更好，CPU / 内存更弱。备用路由够用，整体算力不宜指望超过那台 16G 的 J4105。

## 适用性

双口 I226-IT + AES-NI + VT-x，适合做轻量备用软路由。主要约束是 4GB 内存与 32GB mSATA，不宜再堆重服务。
