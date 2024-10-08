---
title: shell basic variable, 变量
author: "-"
date: 2016-03-03T03:25:04+00:00
url: /?p=8771
categories:
  - shell
tags:
  - reprint
---
## shell basic variable, 变量

>注意，等号两侧不能有空格, 有空格变量会不生效.

```bash
# 定义变量
foo="bar"
# 使用变量
echo ${foo}

## 变量的默认值
${xmx-600M}
```

默认情况下,Bash shell 是一种无类型的脚本语言, 除非用declare特别声明,否则它不会区分一个变量是整数变量、浮点数变量还是字符串变量。
在Bash shell中所有的变量都被看成是字符串,使用时也不需要进行声明。
  
1. 变量的命名
bash shell中变量的命名规则和C语言相同,必须是由英文字母、数字及下划线组成,第一个字符必须是字母或下划线,变量的长度没有限制,但英文字母区分大小写。虽然,bash shell中使用变量时不需要声明,但还是提倡对一些重要的变量进行声明、添加注释,以便阅读和维护。声明或创建一个变量之后,它的作用域是当前shell,子shell无法获取父shell中定义的变量,除非该变量时环境变量。

2. 设定变量
在bash shell中要设置某个变量的值是很容易的,只需要按照: 变量名称=值 的方式即可改变某个变量的值,需要注意的是等号的两边是不能有空格的,若值中含有空格的话,需要用引号括起来。

3. 获取变量值
要获取某个变量的值只需要在该变量的名称前面加上$或用${}将变量括起来即可。

```bash
echo $PATH
echo ${PATH}
```

- 取消与清空变量
当你不再需要某个变量时,你可能想取消该变量,即将该变量从当前名字空间中删除并释放该变量所占用的内存。在bash shell中可以用unset命令来取消某个变量。用法如下:

### unset

```bash
-f 仅删除函数
-v 仅删除变量
```

unset 变量名称 或 unset -v 变量名称

-v 表示取消变量,unset除了可以用来取消变量外,还可以用来取消函数,用unset来取消函数时,用法如下:

unset -f 函数名称

使用 unset 以后,变量就不复存在了,这可能并不是你想要的,你可能只是想将清除该变量中的值,使其为null,即清空变量,清空变量的操作如下:

变量名称=

- 环境变量

只有当一个变量成为环境变量时,它才能为子 shell 所用, 为了使一个变量成为环境变量, 需要使用 export 命令, 具体如下:

变量名称="xxxx"

export 变量名称

或

export 变量名称="xxxx"

除了使用export之后,还可以在声明的时候就将变量指定为环境变量,如下:

declare -x 变量名称

## bash的内置变量

除了环境变量和用户自定义的变量之外,bash shell中还会用到很多的内置变量,下面介绍一些常用的内置变量。

BASH - bash的完整路径,通常是/bin/bash

BASH_VERSION - bash的版本

BASH_ENV - 在非交互模式下,会先检查$BASH_ENV是否有指定的启动文件,如果有则先执行它

ENV - 与BASH_ENV类似,不过是在POSIX模式下,会先检查$ENV是否有指定的启动文件,如果有则先执行它

CDPATH - cd命令的搜索路径

PATH - 命令的搜索路径

EUID - 有效的用户id

FUNCNAME - 在函数执行期间,即为函数的自身的名称

HOSTNAME - 主机名

HOSTTYPE - 主机类型,如i386

OSTYPE - 执行bash的操作系统类型,如linux-gnu

HOME - 用户主目录

IFS  -  默认的字段分隔符

OPTARG - 使用getopts处理选项时,取得的选项的参数

OPTIND - 使用getopts处理选项时,选项的索引值

OPTERR - 若将OPTERR设置为1,则getopts发生错误,输出错误信息

$1~$n - 位置参数,即传入程序或函数的参数,$1即第一个参数,$2为第二个参数,其他类推

$\* -   所有的位置参数,并将其看成一个字符串,如"test.sh abc 123",则$\*为"abc 123"

$@ -  所有的位置参数,并将其看成一个字符串数组,如"test.sh abc 123",则$*为"abc 123"

$# -  位置参数的个数  
$$ -  当前bash shell的进程号

[https://www.cnblogs.com/EasonJim/p/7750298.html](https://www.cnblogs.com/EasonJim/p/7750298.html)

1. 调整变量的属性

declare命令不仅可以用来声明变量,还可以用来调整变量的属性,具体用法如下:

-p  显示变量的属性

-a  变量是一个数组

-i   变量是一个整数

-r  变量为只读的

-x  变量为环境变量
