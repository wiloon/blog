---
title: 开源许可证, License, BSD, MIT, Apache,GPL
author: "-"
date: 2012-08-25T11:40:04+00:00
url: license
categories:
  - open-souce

tags:
  - reprint
---
## 开源许可证, License, BSD, MIT, Apache,GPL

## BSD (二条款版) 

分发软件时，必须保留原始的许可证声明。

## BSD (三条款版) 

分发软件时，必须保留原始的许可证声明。不得使用原始作者的名字为软件促销。

### MIT
分发软件时，必须保留原始的许可证声明，与 BSD (二条款版) 基本一致。
>https://opensource.org/licenses/mit-license.php

 (4) Apache 2

分发软件时，必须保留原始的许可证声明。凡是修改过的文件，必须向用户说明该文件修改过；没有修改过的文件，必须保持许可证不变。

 (1) Affero GPL (AGPL)

如果云服务 (即 SAAS) 用到的代码是该许可证，那么云服务的代码也必须开源。

 (2) GPL

如果项目包含了 GPL 许可证的代码，那么整个项目都必须使用 GPL 许可证。

 (3) LGPL

如果项目采用动态链接调用该许可证的库，项目可以不用开源。

 (4) Mozilla (MPL) 

只要该许可证的代码在单独的文件中，新增的其他文件可以不用开源。

ISC许可

ISC许可证是一种开放源代码许可证，在功能上与两句版的BSD许可证相同。
  
这份许可证是由ISC (Internet Systems Consortium) 所发明，在ISC释出软件时所使用的。
  
当前版本 ISC License (ISC)

5.1 分发 (distribution) ？

除了 Affero GPL (AGPL) ，其他许可证都规定只有在"分发"时，才需要遵守许可证。换言之，如果不"分发"，就不需要遵守。

简单说，分发就是指将版权作品从一个人转移到另一个人。这意味着，如果你是自己使用，不提供给他人，就没有分发。另外，这里的"人"也指"法人"，因此如果使用方是公司，且只在公司内部使用，也不需要遵守许可证。

云服务 (SaaS) 是否构成"分发"呢？答案是不构成。所以你使用开源软件提供云服务，不必提供源码。但是，Affero GPL (AGPL) 许可证除外，它规定云服务也必须提供源码。

5.4 GPL 病毒是真的吗？

GPL 许可证规定，只要你的项目包含了 GPL 代码，整个项目就都变成了 GPL。有人把这种传染性比喻成"GPL 病毒"。

很多公司希望避开这个条款，既使用 GPL 软件，又不把自己的专有代码开源。理论上，这是做不到的。因为 GPL 的设计目的，就是为了防止出现这种情况。

但是实际上，不遵守 GPL，最坏情况就是被起诉。如果你向法院表示无法履行 GPL 的条件，法官只会判决你停止使用 GPL 代码 (法律上叫做"停止侵害") ，而不会强制要求你将源码开源，因为《版权法》里面的"违约救济"没有提到违约者必须开源，只提到可以停止侵害和赔偿损失。

### Choose a License
>https://creativecommons.org/choose/

http://www.ruanyifeng.com/blog/2011/05/how_to_choose_free_software_licenses.html
  
www.ruanyifeng.com/blog/2017/10/open-source-license-tutorial.html
  
https://www.zhihu.com/question/19771481