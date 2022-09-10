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

<http://man.linuxde.net/host>

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

<https://blog.csdn.net/q_l_s/article/details/54897684>  
<https://blog.csdn.net/wangjunjun2008/article/details/19844755>  
<https://man.linuxde.net/strings>  

<https://blog.csdn.net/yangshangwei/article/details/52563123>
