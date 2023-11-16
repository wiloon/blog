---
title: Linux 命令选项, 参数，括号, 可选, 必选
author: "-"
date: 2019-03-19T02:52:27+00:00
url: /?p=13881
categories:
  - Inbox
tags:
  - reprint
---
## Linux 命令选项, 参数，括号, 可选, 必选

[https://blog.csdn.net/raoqin/article/details/8875089](https://blog.csdn.net/raoqin/article/details/8875089)

1. []: 内的内容意思是: 可写可不写
  例如: /home下就一个list 文件，使用ls -help中的 Usage: ls [OPTION]... [FILE]...

2. {}: 那就必须要在{}内给出的选择里选一个。
3. <>: 表示必选

在数据库中
  
Transact-SQL 语法规则
  
Transact-SQL 引用中的语法关系图使用下列规则。

规范 用于
  
大写 Transact-SQL 关键字。
  
斜体 Transact-SQL 语法中用户提供的参数。
  
|  (竖线)  分隔括号或大括号内的语法项目。只能选择一个项目。
  
[ ]  (方括号)  可选语法项目。不必键入方括号。
  
{} (大括号)  必选语法项。不要键入大括号。
  
[ ,...n ] 表示前面的项可重复 n 次。每一项由逗号分隔。
  
[ ...n ] 表示前面的项可重复 n 次。每一项由空格分隔。
  
加粗 数据库名、表名、列名、索引名、存储过程、实用工具、数据类型名以及必须按所显示的原样键入的文本。
  
<标签> ::= 语法块的名称。此规则用于对可在语句中的多个位置使用的过长语法或语法单元部分进行分组和标记。适合使用语法块的每个位置由括在尖括号内的标签表示: <标签>。

## 命令行语法字符
  
在命令行语法中，某些字符与格式有着特殊的意义与含义。 本文档中的命令行语法使用以下字符格式:

### 方括号 []
  
方括号 ( [ ] ) 表示里面的元素 (参数、值或信息) 是可选的。 您可以选择一个或多个条目，也可以不选。 不要将方括号本身也输入到命令行中。

示例: [global options]、[source arguments]、[destination arguments]

### 尖括号 <>
  
尖括号 ( < > ) 表示里面的元素(参数、值或信息) 是必需的。 您需要用相应的信息来替换尖括号里面的文本。 不要将尖括号本身也输入到命令行中。

示例: -f <file name>、-printer <printer name>、-repeat <months> <days> <hours> <minutes>、date access <mm/dd/yyyy>

### 省略号 CA ARCserve Backup
  
由三个句点 ( ... ) 组成的省略号含义是"等等"，表示前述元素 (参数、值或信息) 可以在命令行中多次重复。

示例: -jobid <job id1, job id2, job id3,...>、[-exitcode <exit code 1>、<exit code2>、<exit code3> ...]

### 管道 |
  
管道符号 (竖线) 含义是"或者"，它表示在一个元素内的一个选项。 如果两个参数由管道符号分隔开，您可以选择分隔符左边的元素，也可选择分隔符右边的元素。 在一次命令使用中不可同时选择两个元素。 在方括号中，这些选项是可选的。 在尖括号中，至少需要一个选项。

示例: -ca_backup [-custom|-rotation|-gfsrotation]、-excludeday <Sun|Mon|Tue|Wed|Thu|Fri|Sat>、-runjob <start|stop>

### 斜体
  
斜体文本表示您必须通过相应的值提供的信息。 它是一个要用值来替换的选项或参数。

示例: -sessionpassword session password、-f <file name>、-printer <printer name>

注意: 命令行语法 (包括在 UNIX 和 Linux 平台中使用的用户名、密码和文件名) 是区分大小写的。 例如，commandline、CommandLine 和 COMMANDLINE 是不一样的。
