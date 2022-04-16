---
title: python调用shell命令
author: "-"
date: 2012-11-17T08:34:06+00:00
url: /?p=4709
categories:
  - Python
tags:
  - reprint
---
## python调用shell命令
<http://blog.chinaunix.net/uid-16362696-id-3067891.html>

python调用shell命令的方法有许多

1.1   os.system(command)

在一个子shell中运行command命令，并返回command命令执行完毕后的退出状态。这实际上是使用C标准库函数system()实现的。这个函数在执行command命令时需要重新打开一个终端，并且无法保存command命令的执行结果。


1.2   os.popen(command,mode)

打开一个与command进程之间的管道。这个函数的返回值是一个文件对象，可以读或者写(由mode决定，mode默认是'r')。如果mode为'r'，可以使用此函数的返回值调用read()来获取command命令的执行结果。

1.3**   **commands.getstatusoutput(command)

使用os.popen()函数执行command命令并返回一个元组(status,output)，分别表示command命令执行的返回状态和执行结果。对command的执行实际上是按照{command;} 2>&1的方式，所以output中包含控制台输出信息或者错误信息。output中不包含尾部的换行符。

2.1   subprocess.call(["some_command","some_argument","another_argument_or_path"])

subprocess.call(command,shell=True)

2.2   subprocess.Popen(command, shell=True)

如果 command 不是一个可执行文件，shell=True 不可省。

使用subprocess模块可以创建新的进程，可以与新建进程的输入/输出/错误管道连通，并可以获得新建进程执行的返回状态。使用subprocess模块的目的是替代os.system()、os.popen\*()、commands.\*等旧的函数或模块。

最简单的方法是使用class subprocess.Popen(command,shell=True)。Popen类有Popen.stdin，Popen.stdout，Popen.stderr三个有用的属性，可以实现与子进程的通信。

将调用shell的结果赋值给python变量

handle = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

print handle.communicate()[0]


如果想获取执行命令的状态值，也就是$?, 可以用os.system( cmd )

如果想获取执行命令的print内容， 可以用os.popen( cmd ).read()


既想获取状态值，也想获取打印的内容？


import commands

stat, content = commands.getstatusoutput( cmd )

# stat is the exit code

# content is the content for printing