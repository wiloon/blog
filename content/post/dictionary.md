---
title: dictionary
author: "-"
date: 2012-10-26T04:31:08+00:00
url: dictionary
categories:
  - dev
tags:
  - reprint
---
## dictionary

## Mercurial

Mercurial 是一种轻量级分布式版本控制系统，采用 Python 语言实现，易于学习和使用，扩展性强。相对于传统的版本控制，具有如下优点:

更轻松的管理。
  
传统的版本控制系统使用集中式的 repository，一些和 repository 相关的管理就只能由管理员一个人进行。由于采用了分布式的模型，Mercurial 中就没有这样的困扰，每个用户管理自己的 repository，管理员只需协调同步这些repository。
  
更健壮的系统。
  
分布式系统比集中式的单服务器系统更健壮，单服务器系统一旦服务器出现问题整个系统就不能运行了，分布式系统通常不会因为一两个节点而受到影响。
  
对网络的依赖性更低。
  
由于同步可以放在任意时刻进行，Mercurial 甚至可以离线进行管理，只需在有网络连接时同步。

### Redmine

Redmine 是一个开源的、基于Web的项目管理和缺陷跟踪工具。它用日历和甘特图辅助项目及进度可视化显示。同时它又支持多项目管理。Redmine是一个自由开放 源码软件解决方案，它提供集成的项目管理功能，问题跟踪，并为多个版本控制选项的支持。

虽说像IBM Rational Team Concert的商业项目调查工具已经很强大了，但想坚持一个自由和开放源码的解决方案，可能会发现Redmine是一个有用的Scrum和敏捷的选择。 由于Redmine的设计受到Rrac的较大影响，所以它们的软件包有很多相似的特征。

Redmine建立在Ruby on Rails的框架之上，支持跨平台和多种数据库。。

### Erlang

Erlang 是一种通用的面向并发的编程语言，它由瑞典电信设备制造商爱立信所辖的CS-Lab开发，目的是创造一种可以应对大规模并发活动的编程语言和运行环境。Erlang是一个结构化，动态类型编程语言，内建并行计算支持。最初是由爱立信专门为通信应用设计的，比如控制交换机或者变换协议等，因此非常适 合于构建分布式，实时软并行计算系统。 使用Erlang编写出的应用运行时通常由成千上万个轻量级进程组成，并通过消息传递相互通讯。进程间上下文切换对于Erlang来说仅仅只是一两个环节，比起C程序的线程切换要高效得多得多了。 使用Erlang来编写分布式应用要简单的多，因为它的分布式机制是透明的: 对于程序来说并不知道自己是在分布式运行。 Erlang运行时环境是一个虚拟机，有点像Java虚拟机，这样代码一经编译，同样可以随处运行。它的运行时系统甚至允许代码在不被中断 的情况下更新。另外如果你需要更高效的话，字节代码也可以编译成本地代码运行。 Yaws: 一个Erlang写的服务器，据说并发性能是apache的15倍Erlang得名于丹麦数学家及统计学家Agner Krarup Erlang，同时Erlang还可以表示Ericsson Language。
  
Erlang问世于1987年，经过十年的发展，于1998年发布开源版本[2]。Erlang是运行于虚拟机的解释性语言，但是现在也包含有乌普萨拉大学高性能Erlang计划 (HiPE) 开发的本地代码编译器，自R11B-4版本开始，Erlang也开始支持脚本式解释器。在编程范型上，Erlang属于多重范型编程语言，涵盖函数式、并发式及分布式。顺序执行的Erlang是一个及早求值, 单次赋值和动态类型的函数式编程语言。
  
Erlang并非一门新语言，它出现于1987年，只是当时对并发、分布式需求还没有今天这么普遍，当时可谓英雄无用武之地。Erlang语言创始人Joe Armstrong当年在爱立信做电话网络方面的开发，他使用Smalltalk，可惜那个时候Smalltalk太慢，不能满足电话网络的高性能要求。但Joe实在喜欢Smalltalk，于是定购了一台Tektronix Smalltalk机器。但机器要两个月时间才到，Joe在等待中百无聊赖，就开始使用Prolog，结果等Tektronix到来的时候，他已经对Prolog更感兴趣，Joe当然不满足于精通Prolog，经过一段时间的试验，Joe给Prolog加上了并发处理和错误恢复，于是Erlang就诞生了。这也是为什么Erlang的语法和Prolog有不少相似之处，比如它们的List表达都是[Head | Tail]。
  
1987年Erlang测试版推出，并在用户实际应用中不断完善，于1991年向用户推出第一个版本，带有了编译器和图形接口等更多功能。1992年，Erlang迎来更多用户，如RACE项目等。同期Erlang被移植到VxWorks、PC和 Macintosh等多种平台，两个使用Erlang的产品项目也开始启动。1993爱立信公司内部独立的组织开始维护和支持Erlang实现和Erlang工具。
  
目前，随着网络应用的兴起，对高并发、分布部署、持续服务的需求增多，Erlang的特性刚好满足这些需求，于是Erlang开始得到更多人的关注

### Trac

Trac是Edgewall公司开发并维护的开放源码网页界面项目管理、缺陷追踪软件。Trac的灵感来自于CVSTrac，因为能够与Subversion接口，所以最初叫做svntrac。

Trac使用Python编程语言开发。在2005年中以前，Trac以GPL发行；直到 0.9 版开始使用修改过的BSD许可证释出[1]。基本上都是属于自由软件的许可证。

### ISP

互联网服务供应商 (Internet service provider)

### RTFM

RTFM，是一个英文缩写，意思是: “去读那些他妈的手册” (Read The Fucking Manual) ，这句话通常用在回复那些只要查阅文件就可以解决，拿出来提问只是浪费别人时间的问题[1]。而为了避免这个缩写单词，因为用了“fuck” (他妈的) 这个单词而攻击性、火药味太重，RTFM也被解释成“去读那些愚蠢的手册” (Read The Foolish Manual) ；有的时候也解释成“去读那些友善的手册” (Read The Friendly Manual) 或“去读那些写得不错的手册” (Read The Fine Manual) 。另外，有时候就干脆把“F”拿掉，直接写成RTM (去读手册，Read The Manual) 。

### STFW

STFW是Search The Fu**ing Web的意思

### MIS

(管理信息系统--Management Information System) 系统

### WAF

(Web 应用程序防火墙)

## 语义网

语义网是对未来网络的一个设想,在这样的网络中,信息都被赋予了明确的含义,机器能够自动地处理和集成网上可用的信息.语义网使用XML来定义定制的标签格式以及用RDF的灵活性来表达数据,下一步需要的就是一种Ontology的网络语言(比如OWL)来描述网络文档中的术语的明确含义和它们之间的关系.

### country code

<https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes>

### Darwin

Darwin是由苹果公司于2000年所发布的一个开放源代码操作系统。Darwin是macOS和iOS操作环境的操作系统部分。

### oVirt

(Open Virtualization Manager）是一款免费开源虚拟化软件，是RedHat商业版本虚拟化软件RHEV的开源版本。

oVirt基于kvm，并整合使用了libvirt、gluster、patternfly、ansible等一系列优秀的开源软件。

oVirt的定位是替代vmware vsphere (<https://docs.vmware.com/cn/VMware-vSphere/index.html），oVirt目前已经成为了企业虚拟化环境可选的解决方案，另外相比OpenStack的庞大和复杂，oVirt在企业私有云建设中具备部署和维护使用简单的优势。利用oVirt管理KVM虚拟机和网络，企业可以快速的搭建起一个私有云环境。从这一点看来，oVirt的定位和另一个知名云计算项目OpenStack>的定位是有些类似的。

### 自动变量 (Automatic Variable）

在计算机编程领域，自动变量 (Automatic Variable）指的是局部作用域变量，具体来说即是在控制流进入变量作用域时系统自动为其分配存储空间，并在离开作用域时释放空间的一类变量。在许多程序语言中，自动变量与术语“局部变量” (Local Variable）所指的变量实际上是同一种变量，所以通常情况下“自动变量”与“局部变量”是同义的。

版权声明：本文为CSDN博主「前方一片光明」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：<https://blog.csdn.net/qq_26230421/article/details/106638046>

## lint

lint是最著名的C语言工具之一，一般由UNIX系统提供。与大多数C语言编译器相比，lint可以对程序进行更加广泛的错误分析，是一种更加严密的编译工具。最初，lint这个工具用来扫描C源文件并对源程序中不可移植的代码提出警告。但是现在大多数lint实用程序已经变得更加严密，它不但可以检查出可移植性问题，而且可以检查出那些虽然可移植并且完全合乎语法但却很可能是错误的特性。

### KHTML

KHTML是HTML网页排版引擎之一，由 KDE 所开发。
KDE系统自KDE2版起，在档案及网页浏览器使用了KHTML引擎。该引擎以C++编程语言所写，并以LGPL授权，支援大多数网页浏览标准。由于微软的Internet Explorer的占有率相当高，不少以FrontPage制作的网页均包含只有IE才能读取的非标准语法，为了使KHTML引擎可呈现的网页达到最多，部分IE专属的语法也一并支援。
KHTML拥有速度快捷的优点，但对错误语法的容忍度则比Mozilla产品所使用的Gecko引擎小。
苹果电脑于2002年采纳了KHTML，作为开发Safari浏览器之用，并发布所修改的最新及过去版本源代码。后来发表了开放源代码的WebCore及WebKit引擎，它们均是KHTML的衍生产品，在开发网站列出引擎改变内容，并会传回至KDE计划。由于两个衍生产品各走不同路线，使两者源代码偏离，在与KDE交换更新会出现困难。其中一个原因，是苹果在对外公开源代码之前，以一年时间编修他们的KHTML。另外，苹果传送更新至KDE计划的方式，多是一口气把大量改动一起传送，KDE在整理资料也出现一定的困难，及后苹果表示会以CVS格式来传送。再者，苹果所作出的改动包括Mac OS X系统独有的事物，如Objective-C、KWQ等，在Linux及KHTML是没有的。但KDE方面仍透过这些改动，为KHTML加入新功能及加快其排版速度。

<http://codante.org/blog/post/rendering-engine-trident-gecko-presto-khtml-webcore-webkit/>

## 正斜杠, 反斜杠

    正斜杠( forward slash '/' ) 和反斜杠 ( backslash '\')

反斜杠“\”是计算机出现了之后为了表示程序设计里的特殊含义才发明的专用标点。就是说，除了程序设计领域外，任何地方你都不应该有使用反斜杠的情况，请永远使用正斜杠“/”。

## metadata

metadata: data that describes data

## SDL

SDL (Simple DirectMedia Layer) 是一套开放源代码的跨平台多媒体开发库，使用C语言写成。SDL提供了数种控制图像、声音、输出入的函数，让开发者只要用相同或是相似的代码就可以开发出跨多个平台 (Linux、Windows、Mac OS X等) 的应用软件。目前SDL多用于开发游戏、模拟器、媒体播放器等多媒体应用领域。

## SDL (Simple DirectMedia Layer)

**SDL** (Simple DirectMedia Layer) 是一个用C语言编写的、跨平台的、免费和开源的多媒体程序库，它提供了一个简单的接口用于操作硬件平台的图形显示、声音、输入设备等。SDL库被广泛应用于各种操作系统 (如Linux、FreeBSD、Windows、Mac OS、iOS、Android等) 上的游戏开发、多媒体播放器、模拟器 (如QEMU) 等众多应用程序之中。尽管SDL是用C语言编写的，但是其他很多流行的编程语言 (如C++、C#、Java、Objective C、Lisp、Erlang、Pascal、Perl、Python、PHP、Ruby等等) 都提供了SDL库的绑定，在这些编程语言中都可以很方便的调用SDL的功能。

在QEMU模拟器中的图形显示默认就是使用SDL的。当然，需要在编译qemu-kvm时需要配置SDL的支持，之后才能编译SDL功能到QEMU的命令行工具中，最后才能启动客户机时使用SDL的功能。在编译qemu-kvm的系统中，需要有SDL的开发包的支持，在RHEL6.3系统中需要安装SDL-devel这个RPM包。如果有SDL-devel软件包，在3.4.2节中配置QEMU时默认就会配置为提供SDL的支持，通过运行configure程序，在其输出信息中可以看到"SDL support   yes"即表明SDL支持将会被编译进去。当然，如果不想将SDL的支持编译进去，在配置qemu-kvm时加上"–disable-sdl"的参数即可，configure输出信息中会显示提示"SDL support   no"。

debian install sdl

open synaptic..... install libsdl1.2-dev

## "cat"

CAT (Central Application Tracking) 是一个实时和接近全量的监控系统，它侧重于对Java应用的监控，基本接入了美团上海侧所有核心应用。目前在中间件 (MVC、RPC、数据库、缓存等) 框架中得到广泛应用，为美团各业务线提供系统的性能指标、健康状况、监控告警等。

<https://github.com/dianping/cat>

## Seam Security

Seam Security 中的验证特性是基于JAAS  (Java Authentication and Authorization Service) 开发的，它提供了用来进行用户身份认证的高度可配置的接口。然而，针对复杂多变的验证需求，Seam Security 提供了一套非常简单的验证方法来隐藏 JAAS的复杂性。

## TOAD

TOAD (Tool of Oracle Application Developer) 是一种专业化、图形化的Oracle应用开发和数据库管理工具，具有数据库访问速度快、简单易用、功能强大等特点。多年来，TOAD在Oracle专业人员中享有很高的盛誉，已经成为许多Oracle专业人士的首选工具。

TOAD具有功能强大的模式浏览器，可以快速访问数据字典、浏览表、索引和存储过程，并可以在浏览窗口中直接操作数据库对象。内置的SQL编辑器可以生成、编辑、运行和优化SQL语句。通过编辑和运行结果窗口的配合使用，可以在编辑的同时对运行结果进行测试。除了标准编辑命令外，还可以快速查询字段名或实现SQL语句格式化等功能。

为帮助用户对其应用进行彻底测试，TOAD套件中还集成了数据生成测试工具和压力测试工具。数据生成测试工具有助于开发人员快速生成大量有实际意义且引用关系正确的测试数据，简化应用的测试过程；压力测试工具则能模拟现实环境中的用户流量，预测应用系统在真实生产环境中的运行性能，帮助用户主动解决应用系统的性能和扩展性问题。TOAD的启动方式与其他工具相似，都需要进行连接，如图3-8所示。具体使用方法请参考其他相关资料或联机帮助。

<http://www.toadworld.com>

## update-alternatives

update-alternatives是 dpkg 的实用工具，用来维护系统命令的符号链接，以决定系统默认使用什么命令。在Debian系统中，我们可能会同时安装有很多功能类似的程序和可选配置，如Web浏览器程序(firefox，konqueror)、窗口管理器(wmaker、metacity)和鼠标的不同主题等。这样，用户在使用系统时就可进行选择，以满足自已的需求。但对于普通用户来说，在这些程序间进行选择配置会较困难。update-alternatives工具就是为了解决这个问题，帮助用户能方便地选择自已喜欢程序和配置系统功能。

## hue

<http://www.cnblogs.com/smartloli/p/4527168.html>
  
Hue是一个开源的Apache Hadoop UI系统,由Cloudera Desktop演化而来,最后Cloudera公司将其贡献给Apache基金会的Hadoop社区,它是基于Python Web框架Django实现的。通过使用Hue我们可以在浏览器端的Web控制台上与Hadoop集群进行交互来分析处理数据,例如操作HDFS上的数据,运行MapReduce Job,执行Hive的SQL语句,浏览HBase数据库等等。

Hue在数据库方面,默认使用的是SQLite数据库来管理自身的数据,包括用户认证和授权,另外,可以自定义为MySQL数据库、Postgresql数据库、以及Oracle数据库。其自身的功能包含有:

对HDFS的访问,通过浏览器来查阅HDFS的数据。
  
Hive编辑器: 可以编写HQL和运行HQL脚本,以及查看运行结果等相关Hive功能。
  
提供Solr搜索应用,并对应相应的可视化数据视图以及DashBoard。
  
提供Impala的应用进行数据交互查询。
  
最新的版本集成了Spark编辑器和DashBoard
  
支持Pig编辑器,并能够运行编写的脚本任务。
  
Oozie调度器,可以通过DashBoard来提交和监控Workflow、Coordinator以及Bundle。
  
支持HBase对数据的查询修改以及可视化。
  
支持对Metastore的浏览,可以访问Hive的元数据以及对应的HCatalog。
  
另外, 还有对Job的支持, Sqoop, ZooKeeper 以及 DB (MySQL,SQLite,Oracle等) 的支持。
  
下面就通过集成部署,来预览相关功能。

## PMU

本文引用地址：http://www.eepw.com.cn/article/273622.htm

1.PMU是什么–简介
　　PMU是power management unit的缩写，中文名称为电源管理单元，是一种高度集成的、针对便携式应用的电源管理方案，即将传统分立的若干类电源管理器件整合在单个的封装之内，这样可实现更高的电源转换效率和更低功耗。PMU智能电源管理已经是大势所趋，“主控+PMU”的模式越来越受到产业上下游的青睐，包括TI、Philips Semiconductor、National Semiconductor国际巨头都推出了相应的产品。

2.PMU是什么–作用
　　电源管理单元主要功能是提供系统所需的稳定电源,但是为什么要控制系统电源呢?下面我们就来学习一下吧!

1.系统使用的芯片通常使用不同的电压,开通和关闭电源时,如果不严格遵循芯片要求的顺序和时间,不但系统不能起动,严重时会烧毁芯片。
　　2.半导体电路工作时,工作电流会时大时小,用行业术语来说,就是负载不是恒定的.这对提供电源的电路,要求负载变动时,电源电路要能保持负载芯片得到的电压不变。
　　3.系统使用的电源电压可能不稳定,这就要求电源电路的输出在输入电压的变动下也必须稳定。
　　4.为了节省电能,主要是考虑电池供电系统,不用的电源尽量关掉,比如照相功能,不用这功能时,就关上有关的电源.

3.PMU是什么–架构
　　当设计者要决定系统如何划分时，必须在集中式与分布式电源分配方案中作出选择：前者是将单只PMU紧靠系统的主处理器用于实现所有的电源切换与电压调整功能;后者则是每个子系统都拥有自己的PMU。决策过程取决于两个主要因素：应用及响应速度，以及所需电源管理的间隔尺度(granularity)。

在很多应用中例如高端多媒体手机，制造商用一种模块化方案来增加功能，即在一个基础设计上增加模块来实现某个特定功能，如蓝牙、Wi-Fi或手机电视模块。这种情况下，如果采用集中式PMU架构，则各种变种手机型号中未使用的PMU功能仍会继续保留，造成浪费。但对于固定架构的装置如MP3播放机或音乐播放盒，集中式PMU仍是最具成本效益的选择之一。

4.PMU是什么–应用
　　按主芯片需要而集成了电源管理，充电控制，开关机控制电路。包括自适应的USB-Compatible的PWM充电器，多路直流直流转换器，多路线性稳压器(LDO)，Charge Pump，RTC电路，马达驱动电路，LCD背光灯驱动电路，键盘背光灯驱动电路，键盘控制器，电压/电流/温度等多路12-BitADC，以及多路可配置的GPIO。此外还整合了过/欠压(OVP/UVP)、过温(OTP)、过流(OCP)等保护电路。

PMU作为消费电子(手机、MP4、GPS、PDA等)特定主芯片配套的电源管理集成单元，能提供主芯片所需要的、所有的、多档次而各不相同电压的电源，同电压的能源供给不同的手机工作单元，像处理器、射频器件、相机模块等，使这些单元能够正常工作。

## DWARF

DWARF 是一种广泛使用的标准调试信息格式，最初DWARF的设计初衷是配合ELF格式使用，不过DWARF与具体的文件格式是没有依赖关系的。DWARF这个词是中世纪幻想小说中的用语，也没有什么官方含义，后来才提出 “Debugging With Attributed Record Formats” 这个术语来作为DWARF的另一种定义。

DWARF使用DIE（Debugging Information Entry）来描述变量、数据类型、代码等，DIE中包含了标签（Tag）和一系列属性（Attributes）。

DWARF还定义了一些关键的数据结构，如行号表（Line Number Table)、调用栈信息（Call Frame Information）等，有了这些关键数据结构之后，开发者就可以在源码级别动态添加断点、显示完整的调用栈信息、查看调用栈中指定栈帧的信息。

<https://www.hitzhangjie.pro/debugger101.io/8-dwarf/>

## 降序 desc

一系列数据从高到低或从大到小排列

## 升序 asc

从低到高
