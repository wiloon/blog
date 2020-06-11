---
title: linux shell command
author: wiloon
type: post
date: 2011-04-23T08:54:55+00:00
url: /?p=101
views:
  - 8
bot_views:
  - 5
categories:
  - Linux
tags:
  - linux

---
```bash
# 替换字符串
foo=foo-bar
bar=${foo/-/_}
echo $bar

#执行多个命令
ls && ls -l
sudo mount -t ntfs-3g /dev/sdc10 mnt1
ls -lt
ls -lrt
chown [-R] 账号名称:用户组名称 文件或目录
egrep

yum install lrzsz

lsblk

ls -l /dev/disk/by-uuid/
```

查看挂载的USB设备

lsusb

 

rmdir : delete folder
  
rm -rf
  
-r, -R, &#8211;recursive
  
remove directories and their contents recursively
  
-f, &#8211;force
  
ignore nonexistent files, never prompt
  
#ps
  
ps -ef
  
-a 显示现行终端机下的所有程序，包括其他用户的程序。
  
-A 显示所有程序。
  
-e 此参数的效果和指定&#8221;A&#8221;参数相同。
  
-f 用ASCII字符显示树状结构，表达程序间的相互关系。

md5sum : compute and check MD5 message digest

 

<span style="font-family: 宋体; font-size: medium;">统计某文件夹下<span style="color: #ff0000;">文件</span>的个数</span>

<span style="font-family: 宋体; font-size: medium;">ls -l |grep &#8220;^<span style="color: #000000;">&#8211;</span>&#8220;|wc -l</span>

<span style="font-family: 宋体; font-size: medium;">统计某文件夹下<span style="color: #ff0000;">目录</span>的个数</span>

<span style="font-family: 宋体; font-size: medium;">ls -l |grep &#8220;^ｄ&#8221;|wc -l</span>

<span style="font-family: 宋体; font-size: medium;">统计文件夹下文件的个数，包括子文件夹里的。</span>

<span style="font-family: 宋体; font-size: medium;">ls -lR|grep &#8220;^-&#8220;|wc -l</span>

<span style="font-family: 宋体; font-size: medium;">统计文件夹下目录的个数，包括子文件夹里的。</span>

<span style="font-family: 宋体; font-size: medium;">ls -lR|grep &#8220;^d&#8221;|wc -l</span>

<span style="color: #006666; font-family: 宋体; font-size: medium;">说明：</span>

<span style="font-family: 宋体; font-size: medium;">ls -l</span>

<span style="font-family: 宋体; font-size: medium;">长列表输出该目录下文件信息(注意这里的文件，不同于一般的文件，可能是目录、链接、设备文件等)</span>

<span style="font-family: 宋体; font-size: medium;">grep &#8220;^-&#8220;</span>

<span style="font-family: 宋体; font-size: medium;">这里将长列表输出信息过滤一部分，只保留一般文件，如果只保留目录就是 ^d</span>

<span style="font-family: 宋体; font-size: medium;">wc -l</span>

<span style="font-family: 宋体; font-size: medium;">统计输出信息的行数，因为已经过滤得只剩一般文件了，所以统计结果就是一般文件信息的行数，又由于</span>

 

<span style="font-family: 宋体; font-size: medium;">一行信息对应一个文件，所以也就是文件的个数。</span>

http://blog.chinaunix.net/uid-20355427-id-1700516.html

http://blog.csdn.net/zhouleiblog/article/details/9325913