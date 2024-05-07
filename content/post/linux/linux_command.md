---
title: linux 命令, linux command
author: "-"
date: 2011-11-21T04:51:03+00:00
url: linux/command
categories:
  - Linux
tags:
  - reprint
  - remix
---
## linux 命令, linux command

## 查看某文件的完整路径

```Bash
realpath file_0
```

## cut

```bash
# 按字符截取字符串,返回前200个字符
cut -c 1-200
```

## mkdir

```bash
# 创建多个目录
mkdir foo bar
```

## 查看linux 运行级

runlevel

### strings

strings命令在对象文件或二进制文件中查找可打印的字符串。字符串是4个或更多可打印字符的任意序列，以换行符或空字符结束。 strings命令对识别随机对象文件很有用。

### time

用来计算  某个程序的运行耗时

```bash
    time <command0>
    time dig
```

user: 程序在 User space 执行的时间
sys: 程序在 Kernel space 执行的时间

### cp

```bash
    # 强制覆盖
    cp -f
```

## 启动时间

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

[http://man.linuxde.net/host](http://man.linuxde.net/host)

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

### iconv

iconv命令来转换文件的编码，格式：
iconv -f 原本的编码格式 -t 要转换成的编码 文件名 -o 新文件名
2、例如：
iconv -f gb2312 -t utf8 a.txt -o utf8.txt

## linux 查看硬盘温度

sudo hddtemp /dev/sda

---

[https://blog.csdn.net/q_l_s/article/details/54897684](https://blog.csdn.net/q_l_s/article/details/54897684)  
[https://blog.csdn.net/wangjunjun2008/article/details/19844755](https://blog.csdn.net/wangjunjun2008/article/details/19844755)  
[https://man.linuxde.net/strings](https://man.linuxde.net/strings)  

[https://blog.csdn.net/yangshangwei/article/details/52563123](https://blog.csdn.net/yangshangwei/article/details/52563123)

## mpstat

mpstat是Multiprocessor Statistics的缩写，是实时系统监控工具。其报告与CPU的一些统计信息，这些信息存放在/proc/stat文件中。在多CPUs系统里，其不但能查看所有CPU的平均状况信息，而且能够查看特定CPU的信息。mpstat最大的特点是：可以查看多核心cpu中每个计算核心的统计数据；而类似工具vmstat只能查看系统整体cpu情况。

mpstat [-P {|ALL}] [internal [count]]
参数 解释
-P {|ALL} 表示监控哪个CPU， cpu在[0,cpu个数-1]中取值
internal 相邻的两次采样的间隔时间、
count 采样的次数，count只能和delay一起使用
当没有参数时，mpstat则显示系统启动以后所有信息的平均值。有interval时，第一行的信息自系统启动以来的平均信息。从第二行开始，输出为前一个interval时间段的平均信息。

```bash
mpstat -P ALL 1

```

## last

列出目前与过去登入系统的用户相关信息
