---
title: OTF与TTF的区别
author: "-"
date: 2014-01-08T09:05:13+00:00
url: /?p=6173
categories:
  - Inbox
tags:
  - reprint
---
## OTF与TTF的区别

TTF 扩展名的 O 图标的表示 OpenType - TrueType 字体, 采用的是 TrueType 曲线, 不过支持 OpenType 的高级特性.
  
TTF 扩展名的 T 图标的表示 TrueType 字体, 采用的是 TrueType 曲线, 不支持 OpenType 特性.
  
OTF 扩展名的 O 图标的表示 OpenType - PostScript 字体, 采用的是 PostScript 曲线, 支持 OpenType 高级特性.

OpenType 是 Microsoft 与 Adobe 共同制定的标准, 在此之前有两大字体格式: TrueType 和 Type 1, 两家合作制定出的 OpenType 将之前的两大格式都包含了进去, TrueType 进化成 OpenType - TrueType, 在原有基础上增加了 OpenType 高级特性支持, 扩展名不变 (TTF), 图标由 T 变为 O; Type 1 进化成 OpenType - PostScript, 在原有基础上增加了 OpenType 高级特性支持, 扩展名定位 OTF, 图标为 O.

现在微软和 Adobe 都在努力干掉以往的 TrueType 和 Type 1 字体, 比如 Windows 的系统字体在 Vista 以后全都由 TT 转换为 OT-TT (或许是向 OT-PS 的过渡), 而 Adobe 则大力推广 OT-PS 字体.

至于 Adobe, Microsoft, Type 1, TrueType, PostScript 以及 Apple 的历史和恩恩怨怨可以参考这些... (不过读起来比较乱...)
  
<http://zh.wikipedia.org/w/index.php?...&variant=zh-cn>
  
<http://zh.wikipedia.org/w/index.php?...&variant=zh-cn>
  
<http://zh.wikipedia.org/w/index.php?...&variant=zh-cn>

So, O 图标的 TTF 和 T 图标的 TTF 还是有较大区别的, 虽然扩展名相同, 矢量曲线以及一些基本属性都相同, 但文件头及部分结构并不同. 支持 T 图标的 TTF 的软件/系统不一定也支持 O 图标的 TTF, 不过可以转换嘛.

<http://hi.baidu.com/stonegirl/item/07db7299112ce0895914612c>
