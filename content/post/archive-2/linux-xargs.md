---
title: xargs
author: "-"
date: 2016-03-10T10:02:41+00:00
url: xargs
categories:
  - linux
tags:
  - reprint
  - command
---
## xargs

xargs 可以将输入内容 (通常通过命令行管道传递), 转成后续命令的参数, 通常用途有  
命令组合: 尤其是一些命令不支持管道输入, 比如 ls  
避免参数过长: xargs可以通过 -nx 来将参数分组, 避免参数过长

- -d 参数与分隔符, 默认情况下, xargs 将换行符和空格作为分隔符, 把标准输入分解成一个个命令行参数。
- -i 表示 find 传递给xargs的结果 由{}来代替
- -n 参数分组
- -p 交互式提问y来确认命令的每次执行。
- -t 在执行前回显各个command
- -I 指定每一项命令行参数的替代字符串, 我认为是和i差不多,可以这么认为 -i 可以用 -I {} 来代替

```bash
ls *.js | xargs -t -n2 ls -al
# 输出如下, -n2表示, 将参数以两个为一组, 传给后面的命令。
curl http://foo.bar.com |xargs -t -n1 -d '\n' |xmllint --format
```

例子: 参数分组
  
命令行对参数最大长度有限制,xargs通过-nx对参数进行分组来解决这个问题。

首先,创建4个文件用来做实验。

```bash
touch a.js b.js c.js d.js
```

然后运行如下命令:

```bash
ls -al a.js b.js
-rw-r--r-- 1 root root 0 Dec 18 16:52 a.js
-rw-r--r-- 1 root root 0 Dec 18 16:52 b.js
ls -al c.js d.js
-rw-r--r-- 1 root root 0 Dec 18 16:52 c.js
-rw-r--r-- 1 root root 0 Dec 18 16:52 d.js
```

<http://blog.chinaunix.net/uid-128922-id-289992.html>

xargs在linux中是个很有用的命令,它经常和其他命令组合起来使用,非常的灵活.

xargs是给命令传递参数的一个过滤器,也是组合多个命令的一个工具.它把一个数据流分割为一些足够小的块,以方便过滤器和命令进行处理.由此 这个命令也是后置引用的一个强有力的替换.在一般使用过多参数的命令替换失败的时候,用xargs来替换它一般都能成功.通常情况下,xargs从管道或 者stdin中读取数据,但是它也能够从文件的输出中读取数据.
  
xargs的默认命令是echo.这意味着通过管道传递给 xargs 的输入将会包含换行和空白,不过通过xargs的处理,换行和空白将被空格取代.如:
  
ls -l
  
total 0
  
-rwxr-xr-x 2 root root 4096 2009-02-23 090218.txt
  
-rwxr-xr-x 2 root root 12288 2009-06-08 090607.txt
  
ls -l | xargs
  
090218.txt 090607.txt
  
find ~/mail -type f | xargs grep "Linux"
  
./misc:User-Agent: slrn/0.9.8.1 (Linux)
  
./sent-mail-jul-2005: hosted by the Linux Documentation Project.
  
./sent-mail-jul-2005: (Linux Documentation Project Site, rtf version)
  
./sent-mail-jul-2005: Subject: Criticism of Bozo's Windows/Linux article
  
. . .
  
ls | xargs -p -l gzip 使用gzips压缩当前目录下的每个文件,一次压缩一个, 并且在每次压缩前都提示用户.

注意: 另一个有用的选项是-0,使用 find -print0 或 grep -lZ 这两种组合方式. 这允许处理包含空白或引号的参数.
  
find / -type f -print0 | xargs -0 grep -liwZ GUI | xargs -0 rm -f
  
grep -rliwZ GUI / | xargs -0 rm -f
  
上边两行都可以用来删除任何包含"GUI"的文件。

还有参数-s 和 -x 具体查手册.
  
下面是另一个示例,我们希望计算这些文件中的行数:

$ file * | grep ASCII | cut -d":" -f1 | xargs wc -l

47853 alert_DBA102.log
  
19 dba102_cjq0_14493.trc
  
29053 dba102_mmnl_14497.trc
  
154 dba102_reco_14491.trc
  
43 dba102_rvwr_14518.trc
  
77122 total
  
 (注: 上述任务还可用以下命令完成: )
  
$ wc -l 'file * | grep ASCII | cut -d":" -f1 | grep ASCII | cut -d":" -f1'

该 xargs 版本用于阐释概念。Linux 可以用几种方法来完成同一个任务；请使用最适合您的情况的方法。

使用该方法,您可以快速重命名目录中的文件。

$ ls | xargs -t -i mv {} {}.bak
  
-i 选项告诉 xargs 用每项的名称替换 {}。-t 选项指示 xargs 先打印命令,然后再执行。
  
另一个非常有用的操作是当您使用 vi 打开要编辑的文件时:
  
$ file * | grep ASCII | cut -d":" -f1 | xargs vi
  
该命令使用 vi 逐个打开文件。当您希望搜索多个文件并打开它们进行编辑时,使用该命令非常方便。
  
它还有几个选项。最有用的可能是 -p 选项,它使操作具有可交互性:
  
$ file * | grep ASCII | cut -d":" -f1 | xargs -p vi

vi alert_DBA102.log dba102_cjq0_14493.trc dba102_mmnl_14497.trc

dba102_reco_14491.trc dba102_rvwr_14518.trc ?...

此处的 xarg 要求您在运行每个命令之前进行确认。如果您按下 "y",则执行命令。当您对文件进行某些可能有破坏且不可恢复的操作 (如删除或覆盖) 时,您会发现该选项非常有用。

-t 选项使用一个详细模式；它显示要运行的命令,是调试过程中一个非常有帮助的选项。

如果传递给 xargs 的输出为空怎么办？考虑以下命令:

$ file * | grep SSSSSS | cut -d":" -f1 | xargs -t wc -l wc -l 0 $

在此处,搜索 "SSSSSS" 后没有匹配的内容；因此 xargs 的输入均为空,如第二行所示 (由于我们使用 -t 这个详细选项而产生的结果) 。虽然这可能会有所帮助,但在某些情况下,如果没有要处理的内容,您可能希望停止 xargs；如果是这样,可以使用 -r 选项:

$ file * | grep SSSSSS | cut -d":" -f1 | xargs -t -r wc -l $

如果没有要运行的内容,该命令退出。

假设您希望使用 rm 命令 (该命令将作为 xargs 命令的参数) 删除文件。然而,rm 只能接受有限数量的参数。如果您的参数列表超出该限制怎么办？xargs 的 -n 选项限制单个命令行的参数个数。

下面显示了如何限制每个命令行仅使用两个参数: 即使向 xargs ls -ltr 传递五个文件,但每次向 ls -ltr 仅传递两个文件。

$ file * | grep ASCII | cut -d":" -f1 | xargs -t -n2 ls -ltr

ls -ltr alert_DBA102.log dba102_cjq0_14493.trc

-rw-r-- 1 oracle dba 738 Aug 10 19:18 dba102_cjq0_14493.trc

-rw-r-r- 1 oracle dba 2410225 Aug 13 05:31 alert_DBA102.log

ls -ltr dba102_mmnl_14497.trc dba102_reco_14491.trc

-rw-r-- 1 oracle dba 5386163 Aug 10 17:55 dba102_mmnl_14497.trc

-rw-r-- 1 oracle dba 6808 Aug 13 05:21 dba102_reco_14491.trc

ls -ltr dba102_rvwr_14518.trc

-rw-r-- 1 oracle dba 2087 Aug 10 04:30 dba102_rvwr_14518.trc

使用该方法,您可以快速重命名目录中的文件。
