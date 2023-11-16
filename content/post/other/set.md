---
title: set command
author: "-"
date: 2012-05-10T13:55:37+00:00
url: set
categories:
  - Linux
tags:
  - Linux

---
## set command

set 命令 作用主要是显示系统中已经存在的shell变量 (是变量, 不是环境变量)，以及设置shell变量的新变量值。使用 set 更改 shell 特性时，符号"+"和"-"的作用分别是打开和关闭指定的模式。set 命令不能够定义新的shell变量。如果要定义新的变量，可以使用`declare 命令以变量名=值` 的格式进行定义即可。

使用declare命令定义一个新的环境变量"mylove"，并且将其值设置为"Visual C++"，输入如下命令：

```bash
#定义新环境变量, 注意: 值必须带引号
declare foo='bar'   
```

再使用set命令将新定义的变量输出为环境变量，输入如下命令：

```bash
#设置为环境变量
set -a foo                 
```

执行该命令后，将会新添加对应的环境变量。用户可以使用env命令和grep命令分别显示和搜索环境变量"mylove"，输入命令如下：

```bash
#显示环境变量值
env | grep foo             
```

此时，该命令执行后，将输出查询到的环境变量值。

## 选项

```r
-a：标示已修改的变量，以供输出至环境变量。 

 -b：使被中止的后台程序立刻回报执行状态。 

 -C：转向所产生的文件无法覆盖已存在的文件。 

 -d：Shell预设会用杂凑表记忆使用过的指令，以加速指令的执行。使用-d参数可取消。 

 -e：若指令传回值不等于0，则立即退出shell。 

 -f：取消使用通配符。 

 -h：自动记录函数的所在位置。 

 -H Shell：可利用"!"加<指令编号>的方式来执行history中记录的指令。 

 -k：指令所给的参数都会被视为此指令的环境变量。 

 -l：记录for循环的变量名称。 

 -m：使用监视模式。 

 -n：只读取指令，而不实际执行。 

 -p：启动优先顺序模式。 

 -P：启动-P参数后，执行指令时，会以实际的文件或目录来取代符号连接。 

 -t：执行完随后的指令，即退出shell。 

 -u：当执行时使用到未定义过的变量，则显示错误信息。 

 -v：显示shell所读取的输入值。 

 -x：执行指令后，会先显示该指令及所下的参数。
```

-e 　若指令传回值不等于 0，则立即退出 shell。

### set -e

上面这些写法多少有些麻烦，容易疏忽。set -e 从根本上解决了这个问题，它使得脚本只要发生错误，就终止执行。

set 命令的 -e 参数，linux 自带的说明如下：
"Exit immediately if a simple command exits with a non-zero status."
也就是说，在"set -e"之后出现的代码，一旦出现了返回值非零，整个脚本就会立即退出。

版权声明：本文为CSDN博主「滴水成川」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：[https://blog.csdn.net/xiaofei125145/article/details/39345331](https://blog.csdn.net/xiaofei125145/article/details/39345331)

```bash
# !/usr/bin/env bash
set -e

foo
echo bar
```

执行结果如下。

```bash
bash foo.sh
```

script.sh:行4: foo: 未找到命令
可以看到，第4行执行失败以后，脚本就终止执行了。

set -e 根据返回值来判断，一个命令是否运行失败。但是，某些命令的非零返回值可能不表示失败，或者开发者希望在命令失败的情况下，脚本继续执行下去。这时可以暂时关闭set -e，该命令执行结束后，再重新打开set -e。

set +e
command1
command2
set -e
上面代码中，set +e表示关闭-e选项，set -e表示重新打开-e选项。

还有一种方法是使用command || true，使得该命令即使执行失败，脚本也不会终止执行。

```bash
# !/bin/bash

set -e

foo || true
echo bar
```

上面代码中，true使得这一行语句总是会执行成功，后面的echo bar会执行。

-e还有另一种写法-o errexit。

set -o errexit
六、set -o pipefail
set -e有一个例外情况，就是不适用于管道命令。

所谓管道命令，就是多个子命令通过管道运算符 (|）组合成为一个大的命令。Bash 会把最后一个子命令的返回值，作为整个命令的返回值。也就是说，只要最后一个子命令不失败，管道命令总是会执行成功，因此它后面命令依然会执行，set -e就失效了。

请看下面这个例子。

```bash
# !/usr/bin/env bash

set -e

foo | echo a
echo bar
```

执行结果如下。

$ bash script.sh
a
script.sh:行4: foo: 未找到命令
bar
上面代码中，foo是一个不存在的命令，但是foo | echo a这个管道命令会执行成功，导致后面的echo bar会继续执行。

set -o pipefail用来解决这种情况，只要一个子命令失败，整个管道命令就失败，脚本就会终止执行。

```bash
# !/usr/bin/env bash

set -eo pipefail

foo | echo a
echo bar
```

运行后，结果如下。

$ bash script.sh
a
script.sh:行4: foo: 未找到命令
可以看到，echo bar没有执行。

[http://www.ruanyifeng.com/blog/2017/11/bash-set.html](http://www.ruanyifeng.com/blog/2017/11/bash-set.html)
