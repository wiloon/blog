---
title: Shell 函数
author: "-"
date: 2019-10-28T09:43:40+00:00
url: /?p=15071
categories:
  - shell
tags:
  - reprint
---
## Shell 函数
```bash
[ function ] funname [()]
{
    action;
    [return int;]
}
```

```bash
# 定义函数 fun0
fun0(){
    echo "run fun0 "
}
# 调用函数 fun0
fun0

```

```bash
# 定义带参数的函数 fun0
# 在Shell中，调用函数时可以向其传递参数。在函数体内部，通过 $n 的形式来获取参数的值，例如，$1表示第一个参数，$2表示第二个参数...
fun0(){
    echo "run fun0 $1 "
    echo "第一个参数为 $1 !"
    echo "第二个参数为 $2 !"
    echo "第十个参数为 $10 !"
}
# 调用带参数的函数 fun0
fun0 foo

```

https://www.runoob.com/linux/linux-shell-func.html
  
https://wiki.jikexueyuan.com/project/shell-tutorial/shell-function-parameter.html