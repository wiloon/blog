---
title: AUTOCONF, AUTOMAKE, configure, make, make install
author: "-"
date: 2017-10-14T09:34:11+00:00
url: /?p=11269
categories:
  - Uncategorized
tags:
  - reprint
---
## AUTOCONF, AUTOMAKE, configure, make, make install

<http://blog.csdn.net/linzhiji/article/details/6774410>
  
这些都是典型的使用GNU的AUTOCONF和AUTOMAKE产生的程序的安装步骤。

./configure是用来检测你的安装平台的目标特征的。比如它会检测你是不是有CC或GCC,
  
并不是需要CC或GCC,它是个shell脚本。

make是用来编译的,它从Makefile中读取指令,然后编译。

make install是用来安装的,它也从Makefile中读取指令,安装到指定的位置。

AUTOMAKE和AUTOCONF是非常有用的用来发布C程序的东西。如果你也写程序想使用AUTOMAKE和AUTOCONF,可以参考CNGNU.ORG上的相关文章。

1. configure ,这一步一般用来生成 Makefile,为下一步的编译做准备,你可以通过在 configure 后加上参数来对安装进行控制,比如

代码:
  
./configure -prefix=/usr

上面的意思是将该软件安装在 /usr 下面,执行文件就会安装在 /usr/bin  (而不是默认的 /usr/local/bin),
  
资源文件就会安装在 /usr/share (而不是默认的/usr/local/share) 。
  
同时一些软件的配置文件你可以通过指定 -sys-config= 参数进行设定。
  
有一些软件还可以加上 -with、-enable、-without、-disable 等等参数对编译加以控制,
  
你可以通过允许 ./configure -help 察看详细的说明帮助。

    2、make ,这一步就是编译,大多数的源代码包都经过这一步进行编译

 (当然有些perl或python编写的软件需要调用perl或python来进行编译) 。
  
如果 在 make 过程中出现 error ,你就要记下错误代码 (注意不仅仅是最后一行) ,
  
然后你可以向开发者提交 bugreport (一般在 INSTALL 里有提交地址) ,
  
或者你的系统少了一些依赖库等,这些需要自己仔细研究错误代码。
  
make 的作用是开始进行源代码编译,以及一些功能的提供,
  
这些功能由他的 Makefile 设置文件提供相关的功能,比如 make install 一般表示进行安装,
  
make uninstal 是卸载,不加参数就是默认的进行源代码编译。

make 是 Linux 开发套件里面自动化编译的一个控制程序,
  
他通过借助 Makefile 里面编写的编译规范 (语法很多,类似一个可以运行的脚本程序。
  
反正我是看不懂,所以你也别问我怎么编写) 。进行自动化的调用 gcc 、ld 以及运行某些需要的程序进行编译的程序。

一般情况下,他所使用的 Makefile 控制代码,由 configure 这个设置脚本根据给定的参数和系统环境生成。

    3、make insatll ,这条命令来进行安装 (当然有些软件需要先运行 make check 或 make test

来进行一些测试) ,这一步一般需要你有 root 权限 (因为要向系统写入文件)

Q1: 安装原码程序时,都要执行三步:
  
1./configure
  
2 make
  
3 make install
  
他们是什么意思呀？
  
configure要用到gcc或cc。
  
但make时,需要什么？
  
这些都是典型的使用GNU的AUTOCONF和AUTOMAKE产生的程序的安装步骤。
  
./configure是用来检测你的安装平台的目标特征的。比如它会检测你是不是有CC或GCC,并不是需要CC或GCC,它是个shell脚本
  
make是用来编译的,它从Makefile中读取指令,然后编译。
  
make install是用来安装的,它也从Makefile中读取指令,安装到指定的位置。

AUTOMAKE和AUTOCONF是非常有用的用来发布C程序的东西。如果你也写程序想使用AUTOMAKE和AUTOCONF,可以参考CNGNU.ORG上的相关文章。
  
Q2:
  
cc和gcc又是什么？我在rh7.3用./configure时,它老说我没有cc,无法进行安装,怎么才能有cc
  
cc是gcc的连接.gcc是编译器.你安装的时候大概是没有选择开发工具.你自己到光盘上找一下gcc* 吧.装上就行了.
  
或者yum -y groupinstall "Development Tools" 自动安装基本开发工具
  
CC是makefile里用来定义编译器的,是为了方便代码移植而设定,因为不同的平台可能用到不同的编译器
  
for exampe:
  
x86 gcc
  
mips64 gcc-mips64

当我们把x86下的code移植到mips64时,只要将makefile里CC=gcc改成CC=gcc-mips64
  
而不需要将所有出现gcc的地方都改成gcc-mips64
  
Linux CC与Linux GCC的区别概括介绍。从名字上看,老的unix系统的CC程序叫做C Compiler。但GCC这个名字按GNU的说法叫做Gnu Compiler Collection。因为gcc包含很多编译器(C, C++, Objective-C, Ada, Fortran,and  Java)。所以它们是不一样的,一个是一个古老的C编译器,一个是编译器的Gnu的编译器的集合(Gcc里的C编译器比CC强大太多了,所以你没必要用CC)。当你调用gcc时不一定是调用的C/C++编译器,是gcc根据文件扩展名自动识别并调用对应的编译器,具体可查阅$man gcc。
  
你是下载不到CC的,原因是: CC来自于昂贵的Unix系统,CC是商业软件,要想用你需要打电话,写订单,而不是打开你的Browser去download。
  
linux下的cc是gcc的符号链接。可以通过$ls –l /usr/bin/cc来简单察看.而编译时看到的控制台输出CC则是一个指向gcc的变量,该变量是make程序的内建变量,就算你在Makefile中没有CC= ,该变量也会存在,并默认指向gcc。cc的符号链接和变量存在的意义在于源码的移植性,可以方便的用GCC来编译老的用cc编译的unix软件,甚至连Makefile都不要改。而且也便于linux程序在unix下编译。
  
近几年的一个新情况是越来越多的unix用户,据我所知像solaris,bsd用户也不太使用CC了,人们都一定要装一个gcc,用它来编译C/C++程序。原因显而易见,gcc足够强大,健壮。支持估计目前为止只有它支持的ISO c/c++ 新特性。当然你最好不要使用night版本的gcc。
  
Q3:
  
make 和 make install 中的mark是系统自带的命令还是可执行程序文件？。 make install中,是不是可以认为 install是mark的参数？？？
  
install 不是make的参数,而是在makefile (Makefile) 中有如: install:的语句。如果用make install,那么就执行install:后面的语句。
  
Q4:
  
./config是linux自带的吗？我一make ,老提示我找不到核心类库
  
你去把linux的内核模块安装好就行了啊。。在linux的第二张盘里
  
软件的安装方法不是一成不变的,具体的步骤看随tarball提供的INSTALL或者README
  
Q5:
  
Makefile是什么东西？有什么用？怎么用？
  
makefile是用于自动编译和链接的,一个工程有很多文件组成,每一个文件的改变都会导致工程的重新链接--但是不是所有的文件都需要重新编译,makefile能够纪录文件的信息,决定在链接的时候需要重新编译哪些文件！

在unix系统下,makefile是与make命令配合使用的。
  
有了这个Makefile文件,不论我们什么时候修改了源程序当中的什么文件,我们只要执行make命令,我们的编译器都只会去编译和我们修改的文件有关的文件,其它的文件它连理都不想去理的
