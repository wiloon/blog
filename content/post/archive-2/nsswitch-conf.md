---
title: nsswitch.conf
author: "-"
date: 2016-12-24T10:31:31+00:00
url: /?p=9615
categories:
  - Uncategorized

tags:
  - reprint
---
## nsswitch.conf
http://lsscto.blog.51cto.com/779396/904078

/etc/nsswitch.conf文件解释
  
2008-01-17 15:19:47
  
标签: nsswitch 文件 conf 休闲 职场
  
原创作品,允许转载,转载时请务必以超链接形式标明文章 原始出处 、作者信息和本声明。否则将追究法律责任。http://songzai.blog.51cto.com/52048/59678
  
nsswitch.conf是SUN公司开发的一种扩充 (name services switch) 
  
DESCRIPTION
  
C 程序库里很多函数都需要配置以便能在本地环境正常工作, 习惯上是使用文件(例如\`/etc/passwd') 来完成这一任务. 但别的名字服务, 如
  
网络信息服务NIS, 还有域名服务DNS等, 逐渐通用起来, 并且被加入了C 程序库里, 而它们使用的是固定的搜索顺序.

在有NYS 支持的Linux libc5以及GNU C Library 2.x (libc.so.6)里, 依靠一个更清晰完整的方案来解决该问题. 该方案模仿了Sun
  
Microsystems公司在Solaris 2 的C 程序库里的方法, 也沿袭了它们的命名, 称为 "名字服务开关(NSS)". 所用 "数据库" 及其查找顺序在文
  
件 /etc/nsswitch.conf 里指明.
  
NSS 中可用数据库如下:

aliases:    邮件别名, sendmail(8) 使用该文件.
  
ethers:     以太网号.
  
group:      用户组, getgrent(3) 函数使用该文件.
  
hosts:      主机名和主机号, gethostbyname(3) 以及类似的函数使用了该文件.
  
netgroup:   网络内主机及其用户的列表, 访问规则使用该文件.
  
network:    网络名及网络号, getnetent(3) 函数使用该文件.
  
passwd:     用户口令, getpwent(3) 函数使用该文件.
  
protocols:  网络协议, getprotoent(3) 函数使用该文件.
  
publickey:  NIS+及NFS 所使用的secure_rpc的公开密匙.
  
rpc:        远程过程调用名及调用号, getrpcbyname(3) 及类似函数使用该文件.
  
services:   网络服务, getservent(3) 函数使用该文件.
  
shadow:     shadow用户口令, getspnam(3) 函数使用该文件.

下面是 /etc/nsswitch.conf 文件的一个例子 (如果在系统中没有 /etc/nsswitch.conf 文件的话, 这就是缺省的设置):
  
ex:
  
passwd:
  
compat
  
group:
  
compat
  
shadow:
  
compat

hosts:
  
dns [!UNAVAIL=return] files
  
networks:
  
nis [NOTFOUND=return] files
  
ethers:
  
nis [NOTFOUND=return] files
  
protocols:
  
nis [NOTFOUND=return] files
  
rpc:
  
nis [NOTFOUND=return] files
  
services:
  
nis [NOTFOUND=return] files

第一栏就是上面所说的数据库, 每行的其余部分指明如何查找. 对每个数据库都可以分别指明其查找方法.
  
每个数据库的配置规范包含两个不同的项:
  
* 服务规范, 如\`files', \`db', 或者\`nis'.
  
* 对查找结果的反应, 如\`[NOTFOUND=return]'.
  
在有NYS支持的libc5里允许服务规范\`files', \`nis'及\`nisplus',此外,还可以对hosts 指明\`dns' 为额外服务, 对passwd及group 指明
  
\`compat', 但不能对shadow指明\`compat'.
  
在GNU C Library里, 每个可用的SERVICE都必须有文件 /lib/libnss_SERVICE.so.1 与之对应. 在标准安装时, 可以使用\`files',\`db', \`nis'
  
以及\`nisplus'. 此外, 还可以对hosts 指明\`dns' 为额外服务, 对passwd, group, shadow 指明\`compat', 而在有NYS 支持的libc5中, 不支
  
持最后一项服务.

说明中的第二项使用户可以更好地控制查找过程. Action项处于两个服务名之间, 被括弧括着, 常规格式如下:
  
\`[' ( \`!'? STATUS \`=' ACTION )+ \`]'
  
这里
  
STATUS => success | notfound | unavail | tryagain
  
ACTION => return | continue
  
对关键字的大小写并不敏感. STATUS的值是调用指定服务查找函数的结果, 意义如下:
  
success: 没有错误发生, 得到想要的结果. 缺省action是\`return'.
  
notfound: 查找顺利, 但是没有得到所要的结果. 缺省action是\`continue'.
  
unavail: 服务永久不可用. 这可能意味着必要的文件不可用, 或者,DNS 服务不可用或不允许查询.缺省action是\`continue'.
  
tryagain: 服务临时不可用. 可能是文件被锁住了或者服务器当前不 接受过多的连接. 缺省action是\`continue'.

使用+/-语法的交互(compat 模式)无NYS支持的linux libc5没有名字服务开关, 但允许用户做一些简单的策略控制. 在 /etc/passwd 里可以使
  
用+user或+@netgroup条目(即包括NIS passwd映射所指定用户), 以及-user或-@netgroup条目(即不包括被指定用户), 还有 + 条目(即包括每
  
个用户, 除了NIS passwd映射所排除的). 大多数人只放一个 + 在 /etc/passwd 末尾, 以此包括NIS 的所有东西. 对该情况, 开关提供更快捷
  
的替代方式(\`passwd: files nis'), 这使得无需再往 /etc/passwd, /etc/group 及 /etc/shadow 里添加单个 + 条目. 如果这还不够, NSS
  
的\`compat' 服务提供了完全的+/-语法. 我们可以对伪数据库 passwd_compat, group_compat 及 shadow_compat 指明\`nisplus'服务来覆盖缺
  
省服务\`nis', 但请注意只在GNU C Library里可以使用伪数据库.
  
文件 FILES
  
名为SERVICE的服务是通过位于/lib的共享对象libnss_SERVICE.so.1实现的.
  
/etc/nsswitch.conf 配置文件
  
/lib/libnss_compat.so.1 为GNU C Library 2.x实现\`compat'
  
/lib/libnss_db.so.1 为GNU C Library 2.x实现\`db'
  
/lib/libnss_dns.so.1 为GNU C Library 2.x实现\`dns'
  
/lib/libnss_files.so.1 为GNU C Library 2.x实现\`files'
  
/lib/libnss_hesoid.so.1 为GNU C Library 2.x实现\`hesoid'
  
/lib/libnss_nis.so.1 为GNU C Library 2.x实现\`nis'
  
/lib/libnss_nisplus.so.1 为GNU C Library 2.x实现\`nisplus'

注意 NOTES
  
每个用到了nsswitch.conf 文件的进程只完整地读一次文件, 如果该文件后面被改变了, 进程将仍然使用原来的配置.
  
在Solaris 下, 不能静态连接使用了NSS Service 的程序, 但是在Linux 下, 则毫无问题.

以上是我目前的理解,但感觉还没理解透,还请大家一起来讨论
  
本文出自 "松仔的技术博客" 博客,请务必保留此出处http://songzai.blog.51cto.com/52048/59678