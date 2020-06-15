---
title: rsync
author: wiloon
type: post
date: 2016-05-31T05:02:22+00:00
url: /?p=9024
categories:
  - Uncategorized

---
[code lang=shell]
  
rsync -azP source dest
  
[/code]

-z选项，压缩传输的文件：
  
-P选项非常有用，它是-progress和-partial的组合。第一个选项是用来显示传输进度条，第二个选项允许断点续传和增量传输：

使用rsync命令同步本地目录和远程主机目录
  
Rsync，代表“remote sync”，它是本地和远程主机文件同步工具。它只同步更改的文件，以此实现最小化传输数据。

基本语法

我们创建两个测试目录和一些文件：

[code lang=shell]
  
mkdir d1
  
mkdir d2
  
touch d1/somefile{1..5}

rsync -r d1/ d2
  
\# -r选项代表递归，在同步目录时使用。
  
#也可以使用-a选项，代表同步所有，包括修改时间、群组、权限、特殊文件、也包括递归。
  
rsync -anv dir1/ dir2

\# 注意上面的dir1/中的“／”不能少，它代表同步目录下文件， 如果没有“/” 代表同步这个目录。

[/code]

和远程主机进行同步目录

首先，你要确保有远程主机的SSH访问权限。

把本地目录同步到远程主机：

$ rsync -a dir1／ root@blog.topspeedsnail.com:~/dir2
  
1
  
$ rsync -a dir1／ root@blog.topspeedsnail.com:~/dir2
  
把远程主机目录同步到本地：

$ rsync -a root@blog.topspeedsnail.com:~/dir2/ dir1
  
1
  
$ rsync -a root@blog.topspeedsnail.com:~/dir2/ dir1
  
rsync有用的选项

-z选项，压缩传输的文件：

$ rsync -az source dest
  
1
  
$ rsync -az source dest
  
-P选项非常有用，它是-progress和-partial的组合。第一个选项是用来显示传输进度条，第二个选项允许断点续传和增量传输：

$ rsync -azP source dest
  
1
  
$ rsync -azP source dest
  
Share the post "使用rsync命令同步本地目录和远程主机目录&#8221;

<blockquote class="wp-embedded-content" data-secret="S2qcdaISDp">
  
    <a href="http://blog.topspeedsnail.com/archives/2668">使用rsync命令同步本地目录和远程主机目录</a>
  
</blockquote>

<iframe class="wp-embedded-content" sandbox="allow-scripts" security="restricted" style="position: absolute; clip: rect(1px, 1px, 1px, 1px);" src="http://blog.topspeedsnail.com/archives/2668/embed#?secret=S2qcdaISDp" data-secret="S2qcdaISDp" width="600" height="338" title="《使用rsync命令同步本地目录和远程主机目录》—WTF Daily Blog" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>