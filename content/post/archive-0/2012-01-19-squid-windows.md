---
title: squid windows
author: w1100n
type: post
date: 2012-01-19T06:41:32+00:00
url: /?p=2157
categories:
  - Network

---
是大家也许不知道，Squid有一个for Windows的版本，下载地址为:<http://www.acmeconsulting.it/pagine/opensource/squid/SquidNT.htm>
  
先来说一下Squid for Windows的安装，需求：你要拥有一台可联网的、运行着Windows NT/2000/XP/Server 2003的计算机，还要有Squid

for windows的软件包。从网上下载的Squid for windows的二进制文件是压缩到zip文件里的，首先来解压缩这个文件，加压后会生成一个Squid的文件夹，将此文件夹拷贝到C:，至此Squid for Windows算是被"安装"到你的Windows计算机了。（备注:Squid for windows的默认安装是在C:squid下，当然，可以把Squid放到其他的路径，但是需要大量的配置squid配置文件中的路径信息，那样会比较麻烦）Unix Like的操作系统下的大部分软件都是基于命令行的，使用文本文件进行配置，这样虽说对一些用惯了Windows下软件的朋友们会有些复杂的感觉，但是这样的软件还是有好处的，毕竟其没有Gui会有更高的性能，配置文件的编写更具灵活性，下面我们来看一下具体怎么配置squid for windows。首先，单击[开始]，选择"运行"，输入 cmd 打开Windows的"命令提示符" 窗口，在命令提示符窗口内输入以下命令:

C:>cd c:squidetc
  
C:squidetc>copy squid.conf.default squid.conf   **将Squid的默认配置文件复制一份并起名为squid.conf
  
C:squidetc>copy mime.conf.default mime.conf     **将mime.conf.default复制一份并起名为mime.conf

下面，我们可以使用任意文本编辑器对squid.conf(配置文件)进行编辑，修改squid的配置语句，文件中的#后的文本表示注释。
  
首先，我们找到TAG: acl段，这里是定义访问Squid的IP地址及其对应的名称
  
我们在此段acl Safe_ports port 777 #multiling http后增加一个新行，写 "acl 名称 src IP地址"

示例:acl name1 src 192.168.100.0 #定义所有来自192.168.100.*的机器对应的名称为name1

然后我们找到TAG: http_access段，这里是定义允许访问squid的列表
  
我们在此段http_access deny CONNECT !SSL_ports后增加一个新行，写"http_access allow/deny 名称"，allow表示允许访问，deny表示拒

绝访问。

示例:http_access allow name1 #定义所有标识为name1(192.168.100.*)的机器允许访问squid代理服务器

并且在后面再增加一行 http_access deny all。

任何一个网络应用都会对应一个或N个端口，squid的默认端口是3128，如果要更改，找到 #http_port 3128 这里，删掉前面的#号，并且修改

后面的端口号。

示例:http_port 7777 #将squid的服务端口改为7777

由于Squid是基于Cache(缓存)的代理服务器，所以设置缓存的大小对优化服务器的性能是有必要的，下面来看一下如何设置cache的大小。
  
找到#cache_mem 8 MB这句 删掉前面的#号 将默认的8修改到需要的大小，这里的数值应视具体的机器可用内存而定，应在内存允许的情况下尽

量地设置的大一些以提高代理服务器性能，但不能让代理服务器的缓存大小影响本机器的性能。

示例:cache_mem 200 MB #设置squid使用200MB的内存当做代理服务器缓存

最后我们还要有一个步骤，否则在启动squid服务的时候会报错，那就是配置TAG: visible_hostname段，找到此段，再后面添加

visible_hostname 机器名（随便起） 这么一行，就搞定了。

示例:visible_hostname supersrv #将hostname设置为supersrv

至此，可以保存squid.conf并且退出文本编辑器了，简单的Squid for Windows的配置已经完成。

下面我们回到命令行，输入以下命令：
  
c:>cd c:squidsbin
  
C:squidsbin>squid -i    (注册Squid为Windows的服务，默认的服务名为SquidNT，可以使用"管理工具"中的"服务"来启动/停用服务)
  
C:squidsbin>squid -z    (生成高速缓存的目录)
  
C:squidsbin>squid       (启动squid服务，另一种比较好的方法是在"管理工具"，"服务"中选择SquidNT，然后选择启动服务)

以上简明说明了squid for Windows的安装，配置，启动，此文应用在Unix/Linux下的对Squid的简单配置也是可行的。