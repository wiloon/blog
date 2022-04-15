---
title: 输出重定向 Linux Shell 1>/dev/null 2>&1
author: "-"
date: 2018-08-31T02:21:50+00:00
url: shell/dev/null
categories:
  - shell
tags:
  - reprint
---
## 输出重定向 Linux Shell 1>/dev/null 2>&1

https://blog.csdn.net/sunboy_2050/article/details/9288353
  
shell中可能经常能看到: 

```bash
echo log > /dev/null 2>&1
```

命令的结果可以通过 ">" 的形式来定义输出

### /dev/null
代表空设备文件

- `>`  
`>` : 代表重定向到哪里,例如: 

```bash
echo "123" > /home/123.txt
```

- 1 : 表示 stdout 标准输出, 系统默认值是1, 所以 `>/dev/null` 等同于 `1>/dev/null`
- 2 : 表示 stderr 标准错误
- & : 表示等同于的意思, 2>&1, 表示2的输出重定向等同于1
- `1 > /dev/null 2>&1` 语句含义: 

    `1 > /dev/null` : 首先表示标准输出重定向到空设备文件,也就是不输出任何信息到终端,说白了就是不显示任何信息。
    `2>&1` : 接着,标准错误输出重定向 (等同于) 标准输出,因为之前标准输出已经重定向到了空设备文件,所以标准错误输出也重定向到空设备文件。

实例解析: 

cmd >a 2>a 和 cmd >a 2>&1 为什么不同？
  
cmd >a 2>a : stdout 和 stderr 都直接送往文件 a ,a 文件会被打开两遍,由此导致stdout和stderr互相覆盖。
  
cmd >a 2>&1 : stdout直接送往文件a ,stderr是继承了FD1的管道之后,再被送往文件a 。a文件只被打开一遍,就是FD1将其打开。

两者的不同点在于: 

cmd >a 2>a 相当于使用了FD1、FD2两个互相竞争使用文件 a 的管道；
  
cmd >a 2>&1 只使用了一个管道FD1,但已经包括了stdout和stderr。
  
从IO效率上来讲,cmd >a 2>&1的效率更高。

经常可以在一些脚本,尤其是在crontab调用时发现如下形式的命令调用

/tmp/test.sh > /tmp/test.log 2>&1
  
前半部分/tmp/test.sh > /tmp/test.log很容易理解,那么后面的2>&1是怎么回事呢？

要解释这个问题,还是得提到文件重定向。我们知道>和<是文件重定向符。那么1和2是什么？

在shell中,每个进程都和三个系统文件 相关联: 标准输入stdin,标准输出stdout、标准错误stderr,三个系统文件的文件描述符分别为0,1、2。所以这里2>&1 的意思就是将标准错误也输出到标准输出当中。

下面通过一个例子来展示2>&1有什么作用: 

$ cat test.sh
  
t
  
date
  
test.sh中包含两个命令,其中t是一个不存在的命令,执行会报错,默认情况下,错误会输出到stderr。date则能正确执行,并且输出时间信息,默认输出到stdout

./test.sh > test1.log
  
./test.sh: line 1: t: command not found

$ cat test1.log
  
Wed Jul 10 21:12:02 CST 2013

可以看到,date的执行结果被重定向到log文件中了,而t无法执行的错误则只打印在屏幕上。

$ ./test.sh > test2.log 2>&1

$ cat test2.log
  
./test.sh: line 1: t: command not found
  
Tue Oct 9 20:53:44 CST 2007
  
这次,stderr和stdout的内容都被重定向到log文件中了。

实际上, > 就相当于 1> 也就是重定向标准输出,不包括标准错误。通过2>&1,就将标准错误重定向到标准输出了,那么再使用>重定向就会将标准输出和标准错误信息一同重定向了。如果只想重定向标准错误到文件中,则可以使用2> file。

linux shell 中"2>&1"含义脚本是: 
         
nohup /mnt/Nand3/H2000G >/dev/null 2>&1 &

对于&1 更准确的说应该是文件描述符 1,而1 一般代表的就是STDOUT_FILENO,实际上这个操作就是一个dup2(2)调用.他标准输出到all_result ,然后复制标准输出到文件描述符2(STDERR_FILENO),其后果就是文件描述符1和2指向同一个文件表项,也可以说错误的输出被合并了,其中0 表示键盘输入 1表示屏幕输出 2表示错误输出,把标准出错重定向到标准输出,然后扔到/DEV/NULL下面去。通俗的说,就是把所有标准输出和标准出错都扔到垃圾桶里面。
         
command >out.file 2>&1 &
         
command >out.file是将command的输出重定向到out.file文件,即输出内容不打印到屏幕上,而是输出到out.file文件中。 2>&1 是将标准出错重定向到标准输出,这里的标准输出已经重定向到了out.file文件,即将标准出错也输出到out.file文件中。最后一个& , 是让该命令在后台执行。

       试想2>1代表什么,2与>结合代表错误重定向,而1则代表错误重定向到一个文件1,而不代表标准输出；
    

换成2>&1,&与1结合就代表标准输出了,就变成错误重定向到标准输出.

       你可以用
             ls 2>1测试一下,不会报没有2文件的错误,但会输出一个空的文件1；
             ls xxx 2>1测试,没有xxx这个文件的错误输出到了1中；
             ls xxx 2>&1测试,不会生成1这个文件了,不过错误跑到标准输出了；
             ls xxx >out.txt 2>&1, 实际上可换成 ls xxx 1>out.txt 2>&1；重定向符号>默认是1,错误和输出都传到out.txt了。
    

为何2>&1要写在后面？
         
command > file 2>&1
          
首先是command > file将标准输出重定向到file中, 2>&1 是标准错误拷贝了标准输出的行为,也就是同样被重定向到file中,最终结果就是标准输出和错误都被重定向到file中。
         
command 2>&1 >file
         
2>&1 标准错误拷贝了标准输出的行为,但此时标准输出还是在终端。>file 后输出才被重定向到file,但标准错误仍然保持在终端。

用strace可以看到: 
  
1. command > file 2>&1
  
这个命令中实现重定向的关键系统调用序列是: 
  
open(file) == 3
  
dup2(3,1)
  
dup2(1,2)


  
    command 2>&1 >file
 这个命令中实现重定向的关键系统调用序列是: 
 dup2(1,2)
 open(file) == 3
 dup2(3,1)
  


可以考虑一下不同的dup2()调用序列会产生怎样的文件共享结构。请参考APUE 3.10, 3.12

参考推荐: 

1>/dev/null 2>&1的含义

/dev/null 2>&1 解释