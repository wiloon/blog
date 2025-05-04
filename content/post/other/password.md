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

从最早的明文保存密码，到 md5 sha1 sha256 sha512 加密，到加 salt、加 pepper、多次 hash 计算，再到现代的密码加密算法Bcrypt PBKDF2 Argon2。在保护用户密码的过程中，软件工程师作出了巨大的努力，为网络安全的建设添砖加瓦。

本文详细的描述了密码加密存储技术涉及到的方方面面，并在最后给出了Java语言的实现代码。代码虽然简单，但其中原理却非常值得一读。

介绍
大多数用户在不同的网站或应用中使用相同的密码，因此当网站的数据库被盗取，存储的密码也不应该被攻击者获取。与密码学大多数领域一样，需要考虑很多因素；幸运的是，大多数现代编程语言和框架都提供了内置的功能来帮助存储密码，让问题变得简单很多。

本文章提供了与存储密码有关的各个方面的指导。简而言之：

使用Bcrypt。除非你有足够充分的理由不这么做。
设置合理的计算因子(work factor)。
使用盐Salt (现代算法会自动帮你这么做）。
考虑使用胡椒Pepper来提供额外的防御深度 (尽管单独使用它无法提供额外的安全特性）。

>[https://www.ujcms.com/knowledge/509.html](https://www.ujcms.com/knowledge/509.html)

## Argon2

设计目标：Argon2 是目前最先进的密码哈希算法，专门设计用于对抗现代硬件攻击，包括暴力破解和 GPU 破解。它在 2015 年获得了密码哈希竞赛（Password Hashing Competition, PHC）中的冠军。

工作原理：Argon2 的设计包括内存硬化和迭代机制。它提供三种变体：

Argon2d：强调防止 GPU 并行化攻击，适用于需要最大化时间复杂度的场景。

Argon2i：优化了对抗侧信道攻击，适用于对内存硬化要求较高的场景。

Argon2id：结合了 Argon2d 和 Argon2i 的优点，是最常用的版本。

优点：

高效的内存使用，适合防止使用大量并行计算能力（如 GPU）的破解。

可调整内存、时间和并行度，灵活性高。

通过设计抵抗 GPU 和 ASIC 攻击，非常适合现代硬件环境。

缺点：相比于 bcrypt 和 PBKDF2，Argon2 的实现较为复杂，可能会涉及更多的计算资源，尤其是内存要求较高。