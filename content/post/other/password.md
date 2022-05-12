---
title: 密码加密存储技术详解 (Password Storage Cheat Sheet）
author: "-"
date: 2021-02-26T04:56:34+00:00
url: password
categories:
  - Development
tags:
  - reprint
---
## 密码加密存储技术详解 (Password Storage Cheat Sheet）

从最早的明文保存密码，到md5 sha1 sha256 sha512加密，到加salt、加pepper、多次hash计算，再到现代的密码加密算法Bcrypt PBKDF2 Argon2id。在保护用户密码的过程中，软件工程师作出了巨大的努力，为网络安全的建设添砖加瓦。

本文详细的描述了密码加密存储技术涉及到的方方面面，并在最后给出了Java语言的实现代码。代码虽然简单，但其中原理却非常值得一读。

介绍
大多数用户在不同的网站或应用中使用相同的密码，因此当网站的数据库被盗取，存储的密码也不应该被攻击者获取。与密码学大多数领域一样，需要考虑很多因素；幸运的是，大多数现代编程语言和框架都提供了内置的功能来帮助存储密码，让问题变得简单很多。

本文章提供了与存储密码有关的各个方面的指导。简而言之：

使用Bcrypt。除非你有足够充分的理由不这么做。
设置合理的计算因子(work factor)。
使用盐Salt (现代算法会自动帮你这么做）。
考虑使用胡椒Pepper来提供额外的防御深度 (尽管单独使用它无法提供额外的安全特性）。

><https://www.ujcms.com/knowledge/509.html>
