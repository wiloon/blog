---
title: linux tar
author: wiloon
type: post
date: 2011-10-13T08:11:53+00:00
url: /?p=1030
bot_views:
  - 10
views:
  - 9
categories:
  - Linux

---
[code lang=shell]
  
解包：tar xvf FileName.tar
  
打包：tar cvf FileName.tar DirName
  
\# 注：tar是打包，不是压缩！

[/code]

必要参数有如下：
  
-A 新增压缩文件到已存在的压缩
  
-B 设置区块大小
  
-c 建立新的压缩文件
  
-d 记录文件的差别
  
-r 添加文件到已经压缩的文件
  
-u 添加改变了和现有的文件到已经存在的压缩文件
  
-x 从压缩的文件中提取文件
  
-t 显示压缩文件的内容
  
-z 支持gzip解压文件
  
-j 支持bzip2解压文件
  
-Z 支持compress解压文件
  
-v 显示操作过程
  
-l 文件系统边界设置
  
-k 保留原有文件不覆盖
  
-m 保留文件不被覆盖
  
-W 确认压缩文件的正确性

可选参数如下：
  
-b 设置区块数目
  
-C 切换到指定目录
  
-f 指定压缩文件
  
&#8211;help 显示帮助信息
  
&#8211;version 显示版本信息

-z 是配合解压.GZ的
  
-x 解开一个包文件
  
-v 显示详细信息
  
-f 必须，表示使用归档文件
  
-z, &#8211;gzip, &#8211;ungzip
                
filter the archive through gzip
  
-x, &#8211;extract, &#8211;get
                
extract files from an archive
  
-v, &#8211;verbose
                
verbosely list files processed
  
-f, &#8211;file [HOSTNAME:]F
                
use archive file or device F (default &#8220;-&#8220;, meaning stdin/stdout)
  
-j, &#8211;bzip2