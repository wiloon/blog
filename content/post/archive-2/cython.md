---
title: Cython
author: "-"
date: 2016-11-22T04:11:08+00:00
url: /?p=9411
categories:
  - Uncategorized

tags:
  - reprint
---
## Cython
https://moonlet.gitbooks.io/cython-document-zh_cn/content/ch1-basic_tutorial.html

Cython 的本质可以总结如下: Cython 是包含 C 数据类型的 Python。

Cython 是 Python: 几乎所有 Python 代码都是合法的 Cython 代码。  (存在一些限制,但是差不多也可以。)  Cython 的编译器会转化 Python 代码为 C 代码,这些 C 代码均可以调用 Python/C 的 API。

Cython 可不仅仅包含这些,Cython 中的参数和变量还可以以 C 数据类型来声明。代码中的 Python 值和 C 的值可以自由地交叉混合 (intermixed) 使用, 所有的转化都是自动进行。Python 中的引用计数维护 (Reference count maintenance) 和错误检查 (error checking) 操作同样是自动进行的,并且全面支持 Python 的异常处理工具 (facilities) ,包括 `try-except` 和 `try-finally`,即便在其中操作 C 数据都是可以的。