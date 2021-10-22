---
title: "gcm cbc"
author: "-"
date: "2021-07-17 20:48:08"
url: "gcm-cbc"
categories:
  - inbox
tags:
  - inbox
---
## "gcm cbc"

主要区别

AES-GCM可以并行加密解密，AES-CBC的模式决定了它只能串行地进行加密。因为加密是耗时较久的步骤，且加密的方式是相同的，所以并行地实现AES-GCM算法的时候，其效率是高于AES-CBC的；

AES-GCM提供了GMAC信息校验码，用以校验密文的完整性。AES-CBC没有，无法有效地校验密文的完整性；

AES-GCM是流加密的模式，不需要对明文进行填充。AES-CBC是块加密的模式，需要对明文进行填充。(AES-GCM中进行AES加密的是counter，AES-CBC中进行AES加密的是明文块)；

由于AES-CBC中必须要用到padding，导致最后一个明文块与其他密文块不同，因此可能会受到padding Oracle attacks，从而可以直接通过初始向量IV和密码，即可得到明文。


https://blog.csdn.net/weixin_39680609/article/details/111159600

