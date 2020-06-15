---
title: sql server data type
author: wiloon
type: post
date: 2013-02-16T07:07:12+00:00
url: /?p=5152
categories:
  - DataBase
tags:
  - SQLServer

---
<span><span style="font-size: x-large;">货币数据类型
 </span><wbr /><wbr /><wbr /><wbr /><wbr />货币数据表示正的或负的货币值。在 Microsoft® SQL Server™ 2000 中使用money 和 smallmoney 数据类型存储货币数据。货币数据存储的精确度为四位小数。
 ·money 存储范围是 -922,337,203,685,477.5808 至+922,337,203,685,477.5807
 <wbr /><wbr /><wbr /><wbr /><wbr />（需 8 个字节的存储空间）。</span>

<span>·smallmoney 存储范围是 -214,748.3648 至 214,748.3647（需 4 个字节的存储空间）。</span>

<span>·如果数值超过了上述范围，则可使用 decimal 数据类型代替。</span>