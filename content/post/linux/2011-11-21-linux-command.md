---
title: linux 命令, linux command
author: "-"
type: post
date: 2011-11-21T04:51:03+00:00
url: /?p=1568
categories:
  - Linux
tags:
  - RedHat

---
## linux 命令, linux command
### strings
strings命令在对象文件或二进制文件中查找可打印的字符串。字符串是4个或更多可打印字符的任意序列，以换行符或空字符结束。 strings命令对识别随机对象文件很有用。
### wc
wc(Word Count)命令用来统计文件内容信息,包括行数、字符数等

语法: wc [-lwc] fine_name

若不接文件，则统计标准输入
```bash
#显示文件内容信息,输出信息依次是:行数,字数,字节数,文件名称
wc filename
 
#显示一个文件的行数
wc -l filename
 
#显示一个文件的字节数
wc -c filename
 
#显示一个文件的字符数
wc -m filename
 
#显示一个文件中的最长行的长度
wc -L filename
 
#注意: 每行结尾的换行符也算一个字符，空格也算一个字符
#采用UTF-8编码，所以一个汉字在这里被转换为3字节
#当使用-m选项时，一个汉字就作为一个字符计算
```
### time
用来计算  某个程序的运行耗时

    time <command0>
    time dig

user: 程序在 User space 执行的时间
sys: 程序在 Kernel space 执行的时间



### cp
    # 强制覆盖
    cp -f


```bash
# 查看系统启动时间和运行时间
uptime
who -b
who -r

# Linux系统历史启动的时间
last reboot

w命令查看

# host命令是常用的分析域名查询工具，可以用来测试域名系统工作是否正常。
host wiloon.com

#pidof命令用于查找指定名称的进程的进程号id号。
pidof

#kill pid
pidof fcitx | xargs kill

```

http://man.linuxde.net/host


重启
  
reboot
  
shutdown -r now
  
init 6
  
关机
  
shutdown -h now
  
init 0
  
退出
  
init 3

启动X

init 5
  
start x


---

https://blog.csdn.net/q_l_s/article/details/54897684  
https://blog.csdn.net/wangjunjun2008/article/details/19844755  
https://man.linuxde.net/strings  