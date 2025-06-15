---
title: bash
author: "-"
date: 2015-01-06T03:29:57+00:00
url: bash
categories:
  - shell
tags:
  - shell

---
## bash

### bash -c

用法: `bash -c "cmd string"`
通常使用shell去运行脚本，两种方法 bash xxx.sh，另外一种就是bash -c "cmd string"
对于bash xxx.sh, 首先bash 会在当前目录去寻找xxx.sh，如果找到，就直接运行，找不到则按照环境变量$PATH的指定路径，按顺序去找，如果找到，则执行，找不到则报错。
shell 脚本的参数 $0 就是要执行的 shell 脚本 xxx.sh， $1 就是后面紧跟 xxx.sh 的参数，$2 $3依次类推

而对于bash -c "cmd string"
首先我们看看官方的说明解释

-c If the -c option is present, then commands are read from the first non-option argument command_string.  If there are arguments after the command_string, they are assigned to the positional parameters, starting with $0.

大致意思就是，如果用 -c 那么bash 会从第一个非选项参数后面的字符串中读取命令，如果字符串有多个空格，第一个空格前面的字符串是要执行的命令，也就是$0, 后面的是参数，即$1, $2....
我们看个例子
首先有个atest shell脚本,里面的内容为

echo $0
echo $1
echo $2
执行bash -c "./atest hello world"他的输出如下：

./atest
hello
world
使用bash -c 要注意两点

-c 第一个字符串一定要是命令路径，不能是文件名，如果把./atest前面的./去掉，那么就会报找不到命令
命令文件必须要有可执行权限，即./atest 的必须就有x属性
个人理解bash -c "./atest hello world"实际上和./atest hello world等价，所以也就有了上面1 2两个注意点。而且这个时候在./atest开头的位置，我们一般写的#!/usr/bin/sh #!/usr/bin/env python这种语句就起作用了 (所以，开头一定要按shell规范写），因为这种情况下真正执行脚本的程序就是开头指定的行，如果没有指定，默认使用bash(这是在shell中执行命令)。 bash -c "./atest hello world"和./atest hello world等价，那具体有没有什么区别呢？ 是有的，上面的介绍是直接在终端中运行命令。那当我们在代码中要运行上面的脚本的时候，比如fork + exec的时候，这种情况下一般就使用bash -c，但是这时候要注意bash的环境变量，就跟在crontab中跑这个脚本差不多，千万注意环境变量。
对于bash 其实还封装的有一些其他特有的环境变量，比如
$BASH_ARGV 参数数组
$BASH_ARGC 参数数组的长度
我们可以在bash中直接使用，但是这些都是bash特有的，具体参见：
[https://www.gnu.org/software/bash/manual/html_node/Bash-Variables.html](https://www.gnu.org/software/bash/manual/html_node/Bash-Variables.html)

### shopt

在 Bash 中，有两个内置命令用来控制 Bash 的各种可配置行为的开关 (打开或关闭），这些开关称之为选项 (option）。其中一个命令是 set，set 命令有三种功能：显示所有的变量和函数；修改 Bash 的位置参数；控制 Bash 的第一套选项。可见 set 命令完全违背了“一个命令只干一件事”的 UNIX 哲学。另外一个命令是 shopt，从名字 (shell options 的缩写）就可以看出，它的功能是控制 Bash 的另一套选项。

shopt 也可以控制 set 的选项

[https://www.cnblogs.com/ziyunfei/p/4913758.html](https://www.cnblogs.com/ziyunfei/p/4913758.html)

作者：llicety
链接：[https://www.jianshu.com/p/198d819d24d1](https://www.jianshu.com/p/198d819d24d1)
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
