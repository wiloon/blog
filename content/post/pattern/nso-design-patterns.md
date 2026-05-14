---
title: NSO 设计模式实践与总结
author: "-"
date: 2026-05-14T20:17:36+08:00
lastmod: 2026-05-14T22:43:32+08:00
url: nso-design-patterns
categories:
  - Pattern
tags:
  - original
  - AI-assisted
  - nso
  - redis
  - firewall
---

## 背景

在一个网络自动化项目中，防火墙策略由 NSO 缓存在 Redis 中，主要有两种数据结构：

- **object**：地址对象，`key` 是名称，`value` 是一个数组，数组元素是实际的 IP 地址或 CIDR 网段
- **group_object**：地址组，有自己的 `name` 和 `value`，`value` 是一个数组，数组元素是 `object` 的 name 或另一个 `group_object` 的 name

group 和 object 形成嵌套结构：一个 group 的 value 列表里，既可以直接引用 object，也可以引用其他 group，形成递归树。

<!-- 其余内容请从原文档补充 -->
