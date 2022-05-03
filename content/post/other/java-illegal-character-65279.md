---
title: 'java  illegal character  \65279'
author: "-"
date: 2013-12-27T03:39:49+00:00
url: /?p=6081
categories:
  - Uncategorized
tags:
  - Java

---
## 'java  illegal character  \65279'

<http://blog.csdn.net/shixing_11/article/details/6976900>

某些编辑器会往utf8文件中添加utf8标记 (editplus称其为签名) ，它会在文件开始的地方插入三个不可见的字符 (0xEF 0xBB 0xBF，即BOM) ，它的表示的是 Unicode 标记 (BOM) 。 因此要解决这个问题的关键就是把这个标记选项去掉，可按如下方法操作。
  
首先用editplus打开这个文件，从Doucument菜单中选择Permanet Settings,有三个分类，分别是General,File, Tools.点击File,右边会有一项是 UTF-8 signature: 选择 always remove signature. 点击OK 。中文版本的 Editplus 下操作的菜单结构如下: 文档->参数设置->文件->UTF-8签名->总是移除签名->确定 ，这样就设置了UTF-8格式不需要在文件前面加标记，最后把文件另存为utf-8格式就好了.

相关资料，网上摘抄:

UTF-8以字节为编码单元，没有字节序的问题。UTF-16以两个字节为编码单元，在解释一个UTF-16文本前，首先要弄清楚每个编码单元的字节序。例如收到一个"奎"的Unicode编码是594E，"乙"的Unicode编码是4E59。如果我们收到UTF-16字节流"594E"，那么这是"奎"还是"乙"？Unicode规范中推荐的标记字节顺序的方法是BOM。BOM不是"Bill Of Material"的BOM表，而是Byte Order Mark。BOM是一个有点小聪明的想法: 在UCS编码中有一个叫做"ZERO WIDTH NO-BREAK SPACE"的字符，它的编码FEFF。而FFFE在UCS中是不存在的字符，所以不应该出现在实际传输中。UCS规范建议我们在传输字节流前，先传输字符"ZERO WIDTH NO-BREAK SPACE"。这样如果接收者收到FEFF，就表明这个字节流是Big-Endian的；如果收到FFFE，就表明这个字节流是Little-Endian的。因此字符"ZERO WIDTH NO-BREAK SPACE"又被称作BOM。UTF-8不需要BOM来表明字节顺序，但可以用BOM来表明编码方式。字符"ZERO WIDTH NO-BREAK SPACE"的UTF-8编码是EF BB BF (读者可以用我们前面介绍的编码方法验证一下) 。所以如果接收者收到以EF BB BF开头的字节流，就知道这是UTF-8编码了。Windows就是使用BOM来标记文本文件的编码方式的。原来BOM是在文件的开始加了几个字节作为标记。

扩展阅读:

UTF-8, UTF-16, UTF-32 & BOM: <http://www.unicode.org/faq/utf_bom.html#BOM>

W3C官方说明: <http://www.w3.org/International/questions/qa-utf8-bom>
