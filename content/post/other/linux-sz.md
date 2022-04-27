---
title: Linux sz
author: "-"
date: 2015-09-16T01:07:07+00:00
url: /?p=8263
categories:
  - Uncategorized

tags:
  - reprint
---
## Linux sz

<http://codingstandards.iteye.com/blog/827637>

我使用过的Linux命令之sz - 下载文件，无需ftp/sftp
  
博客分类: Linux命令
  
LinuxCC++C#Web
  
我使用过的Linux命令之sz - 下载文件，无需ftp/sftp
  
本文链接: <http://codingstandards.iteye.com/blog/827637>    (转载请注明出处)

用途说明
  
sz命令是利用ZModem协议来从Linux服务器传送文件到本地，一次可以传送一个或多个文件。相对应的从本地上传文件到Linux服务器，可以使用rz命令。参见《我使用过的Linux命令之rz - 批量上传文件，简单易用 》。

常用参数
  
-a 以文本方式传输 (ascii) 。

-b 以二进制方式传输 (binary) 。

-e 对控制字符转义 (escape) ，这可以保证文件传输正确。

-c command

-i command 在接收端 (本地) 执行命令，但我没有尝试成功。

如果能够确定所传输的文件是文本格式的，使用 sz -a files

如果是二进制文件，使用 sz -be files

下载完了之后文件在哪个地方呢？

SecureCRT中，选择菜单项"选项(O)"下的"会话选项(S)"，左边切到"Xmodem/Zmodem"，即可看到上传和下载目录设置，也可更改。默认上传目录为 C:\Program Files\SecureCRT\upload，下载目录为 C:\Program Files\SecureCRT\download。

但在Vista下，到C:\Program Files\SecureCRT\download去看的时候并没有找到下载的文件，搜索了一下发现它们在下面的目录中: C:\Users\*\*\*\AppData\Local\VirtualStore\Program Files\SecureCRT\download，其中\*\**为用户名。

使用示例
  
示例一 批量下载文本文件
  
本例演示了下载文本文件，比如c源代码。

[root@web src]# ls *.c
  
httptunnel_codec.c  s_agent2.c  s_conf.c  s_htserv.c  s_pop3.c    s_smtp.c   s_tcpfwd.c  s_telnet.c  s_user.c  s_xort.c
  
iSurf.c             s_agent.c   s_ftp.c   s_http.c    s_run.c     s_socks.c  s_tcpgum.c  s_term.c    s_via3.c
  
proxycfg.c          s_bridge.c  s_host.c  s_mime.c    s_server.c  s_task.c   s_tcphub.c  surf.c      s_via.c
  
[root@web src]# sz -a *.c
  
rz
  
正在开始 zmodem 传输。 按 Ctrl+C 取消。
  
正在传输 httptunnel_codec.c...
  
100%      22 KB    5 KB/s 00:00:04       0 错误
  
正在传输 iSurf.c...
  
100%     890 bytes  890 bytes/s 00:00:01       0 错误
  
正在传输 proxycfg.c...
  
100%       1 KB    1 KB/s 00:00:01       0 错误
  
正在传输 s_agent2.c...
  
100%       4 KB    1 KB/s 00:00:03       0 错误
  
正在传输 s_agent.c...
  
100%       6 KB    3 KB/s 00:00:02       0 错误
  
正在传输 s_bridge.c...
  
100%       6 KB    0 KB/s 00:00:10       0 错误
  
100%       6 KB    0 KB/s 00:00:10       0 错误
  
正在传输 s_conf.c...
  
100%       9 KB    0 KB/s 00:00:41       0 错误
  
正在传输 s_ftp.c...
  
100%      18 KB    0 KB/s 00:04:26       0 错误

[root@web src]# **01000000039a32
  
-bash: **01000000039a32: command not found
  
[root@web src]#
  
由于网络不稳定，被自动终止掉了。
  
[root@web src]#
  
[root@web src]#
  
[root@web src]#
  
[root@web src]# sz -a *.c
  
rz
  
正在开始 zmodem 传输。 按 Ctrl+C 取消。
  
正在传输 httptunnel_codec.c...
  
100%      22 KB    2 KB/s 00:00:10       0 错误
  
正在传输 iSurf.c...
  
100%     890 bytes  890 bytes/s 00:00:01       0 错误
  
正在传输 proxycfg.c...
  
100%       1 KB    1 KB/s 00:00:01       0 错误
  
100%       1 KB    1 KB/s 00:00:01       0 错误
  
正在传输 s_agent2.c...
  
100%       4 KB    2 KB/s 00:00:02       0 错误
  
100%       4 KB    2 KB/s 00:00:02       0 错误
  
正在传输 s_agent.c...
  
100%       6 KB    6 KB/s 00:00:01       0 错误
  
正在传输 s_bridge.c...
  
100%       6 KB    1 KB/s 00:00:04       0 错误
  
正在传输 s_conf.c...
  
100%       9 KB    4 KB/s 00:00:02       0 错误
  
正在传输 s_ftp.c...
  
100%      18 KB    4 KB/s 00:00:04       0 错误
  
正在传输 s_host.c...
  
100%       3 KB    1 KB/s 00:00:02       0 错误
  
正在传输 s_htserv.c...
  
100%       8 KB    2 KB/s 00:00:04       0 错误
  
正在传输 s_http.c...
  
100%      32 KB    3 KB/s 00:00:09       0 错误
  
正在传输 s_mime.c...
  
100%       1 KB    1 KB/s 00:00:01       0 错误
  
100%       1 KB    1 KB/s 00:00:01       0 错误
  
正在传输 s_pop3.c...
  
100%       3 KB    3 KB/s 00:00:01       0 错误
  
正在传输 s_run.c...
  
100%     900 bytes  900 bytes/s 00:00:01       0 错误
  
正在传输 s_server.c...
  
100%       5 KB    2 KB/s 00:00:02       0 错误
  
正在传输 s_smtp.c...
  
100%     990 bytes  990 bytes/s 00:00:01       0 错误
  
正在传输 s_socks.c...
  
100%      19 KB   19 KB/s 00:00:01       0 错误
  
正在传输 s_task.c...
  
100%       1 KB    1 KB/s 00:00:01       0 错误
  
100%       1 KB    1 KB/s 00:00:01       0 错误
  
正在传输 s_tcpfwd.c...
  
100%      10 KB    5 KB/s 00:00:02       0 错误
  
正在传输 s_tcpgum.c...
  
100%       8 KB    4 KB/s 00:00:02       0 错误
  
正在传输 s_tcphub.c...
  
100%      11 KB   11 KB/s 00:00:01       0 错误
  
正在传输 s_telnet.c...
  
100%       3 KB    3 KB/s 00:00:01       0 错误
  
正在传输 s_term.c...
  
100%       7 KB    7 KB/s 00:00:01       0 错误
  
正在传输 surf.c...
  
100%       2 KB    2 KB/s 00:00:01       0 错误
  
正在传输 s_user.c...
  
100%       6 KB    3 KB/s 00:00:02       0 错误
  
正在传输 s_via3.c...
  
100%       1 KB    1 KB/s 00:00:01       0 错误
  
正在传输 s_via.c...
  
100%       5 KB    2 KB/s 00:00:02       0 错误
  
正在传输 s_xort.c...
  
100%       4 KB    4 KB/s 00:00:01       0 错误

奫root@web src]#

示例二 下载二进制文件
  
本例演示了下载二进制文件，先将前面的c源代码压缩到一个zip文件。

[root@web src]# zip source.zip *.c
  
adding: httptunnel_codec.c (deflated 88%)
  
adding: iSurf.c (deflated 58%)
  
adding: proxycfg.c (deflated 56%)
  
adding: s_agent2.c (deflated 69%)
  
adding: s_agent.c (deflated 73%)
  
adding: s_bridge.c (deflated 74%)
  
adding: s_conf.c (deflated 74%)
  
adding: s_ftp.c (deflated 79%)
  
adding: s_host.c (deflated 73%)
  
adding: s_htserv.c (deflated 76%)
  
adding: s_http.c (deflated 75%)
  
adding: s_mime.c (deflated 61%)
  
adding: s_pop3.c (deflated 66%)
  
adding: s_run.c (deflated 58%)
  
adding: s_server.c (deflated 69%)
  
adding: s_smtp.c (deflated 52%)
  
adding: s_socks.c (deflated 79%)
  
adding: s_task.c (deflated 65%)
  
adding: s_tcpfwd.c (deflated 75%)
  
adding: s_tcpgum.c (deflated 73%)
  
adding: s_tcphub.c (deflated 75%)
  
adding: s_telnet.c (deflated 65%)
  
adding: s_term.c (deflated 72%)
  
adding: surf.c (deflated 58%)
  
adding: s_user.c (deflated 72%)
  
adding: s_via3.c (deflated 52%)
  
adding: s_via.c (deflated 71%)
  
adding: s_xort.c (deflated 70%)
  
[root@web src]# ls -l source.zip
  
-rw-r-r- 1 root root 57027 11-28 21:37 source.zip
  
[root@web src]# sz -be source.zip
  
rz
  
正在开始 zmodem 传输。 按 Ctrl+C 取消。
  
正在传输 source.zip...
  
100%      55 KB    3 KB/s 00:00:15       0 错误

奜O[root@web src]#

问题思考
  
相关资料
  
【1】Linux宝库 rz/sz

【2】密州居士 linux上面的sz,rz命令与ssh的配合

【3】本系列 我使用过的Linux命令之rz - 批量上传文件，简单易用
