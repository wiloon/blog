---
title: set
author: "-"
date: 2012-05-10T13:55:37+00:00
url: set
categories:
  - Linux
tags:
  - Linux

---
## set

-e 　若指令传回值不等于0，则立即退出shell。

### set -e
上面这些写法多少有些麻烦，容易疏忽。set -e从根本上解决了这个问题，它使得脚本只要发生错误，就终止执行。


#!/usr/bin/env bash
set -e

foo
echo bar
执行结果如下。


$ bash script.sh
script.sh:行4: foo: 未找到命令
可以看到，第4行执行失败以后，脚本就终止执行了。

set -e根据返回值来判断，一个命令是否运行失败。但是，某些命令的非零返回值可能不表示失败，或者开发者希望在命令失败的情况下，脚本继续执行下去。这时可以暂时关闭set -e，该命令执行结束后，再重新打开set -e。


set +e
command1
command2
set -e
上面代码中，set +e表示关闭-e选项，set -e表示重新打开-e选项。

还有一种方法是使用command || true，使得该命令即使执行失败，脚本也不会终止执行。


#!/bin/bash
set -e

foo || true
echo bar
上面代码中，true使得这一行语句总是会执行成功，后面的echo bar会执行。

-e还有另一种写法-o errexit。


set -o errexit
六、set -o pipefail
set -e有一个例外情况，就是不适用于管道命令。

所谓管道命令，就是多个子命令通过管道运算符 (|）组合成为一个大的命令。Bash 会把最后一个子命令的返回值，作为整个命令的返回值。也就是说，只要最后一个子命令不失败，管道命令总是会执行成功，因此它后面命令依然会执行，set -e就失效了。

请看下面这个例子。


#!/usr/bin/env bash
set -e

foo | echo a
echo bar
执行结果如下。


$ bash script.sh
a
script.sh:行4: foo: 未找到命令
bar
上面代码中，foo是一个不存在的命令，但是foo | echo a这个管道命令会执行成功，导致后面的echo bar会继续执行。

set -o pipefail用来解决这种情况，只要一个子命令失败，整个管道命令就失败，脚本就会终止执行。


#!/usr/bin/env bash
set -eo pipefail

foo | echo a
echo bar
运行后，结果如下。


$ bash script.sh
a
script.sh:行4: foo: 未找到命令
可以看到，echo bar没有执行。

>http://www.ruanyifeng.com/blog/2017/11/bash-set.html
