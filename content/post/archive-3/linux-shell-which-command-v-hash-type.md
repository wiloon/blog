---
title: linux shell 查找文件位置，which, command -v, hash, type
author: "-"
date: 2019-06-21T00:18:13+00:00
url: /?p=14537
categories:
  - shell
tags:
  - reprint
---
## linux shell 查找文件位置，which, command -v, hash, type

```bash
command -v foo
```

避免使用which, 相对于hash、type、command等内置命令,which是一个没有明显的功能优势的外部命令。
  
- 使用which时会启动一个新的进程
  
很多linux发行版上的which执行完后甚至没有返回码，这就意味着在上面执行完"if which foo"就不会奏效，即使"foo"命令 不存在，系统也会报告存在，这样明显是适得其反。(部分POSIX风格的shell对hash命令也会有类似情况)

很多linux发行版上的which会做一些邪恶的事情，比如改变输出结果甚至会接入到包管理器中。

<https://stackoverflow.com/questions/592620/how-to-check-if-a-program-exists-from-a-bash-script?page=1&tab=votes#tab-top>
  
<https://blog.51cto.com/xoyabc/1902804>
