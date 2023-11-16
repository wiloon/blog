---
title: slackware
author: "-"
date: 2011-11-26T06:36:29+00:00
url: /?p=1605
categories:
  - Linux
tags:
  - reprint
---
## slackware
# Slackware Linux
[http://baike.baidu.com/view/10899.htm](http://baike.baidu.com/view/10899.htm)
Slackware Linux是由Patrick Volkerding制作的GNU/Linux发行版，它是世界上依然存活的最久的Linux发行版，在它的辉煌时期，曾经在所有发行版中拥有最多的用户数量。但是，随着 Linux商业化的浪潮，Redhat、Mandrake 和Suse 这些产品通过大规模的商业推广，占据了广大的市场；Debian作为一个社区发行版，也拥有很大的用户群。相比之下，Slackware的不事声张，使得它从许多人(尤其是使用Linux的新用户)的视野中消失了。

    Slackware是Patrick Volkerding制作的Linux发行版本。Slackware 走了一条同其他的发行版本 (Red Hat、Debian、Gentoo、SuSE、 Mandriva、Ubuntu等) 不同的道路，它力图成为"UNIX风格"的Linux发行版本。它的方针是只吸收稳定版本的应用程序，并且缺少其他linux版本中那些为发行版本定制的配置工具。
  
  
  
    Slackware的历史
  
  
    第一个 Slackware 的版本1.00 在1993年
  
  
    
      Slackware
  
  
    7月16日由创立者和开发领导者Patrick Volkerding发布。 它是基于SLS Linux并以软盘为镜像在匿名FTP上发行。Slackware是现存的最古老的发行版本，在2003年度过了它的十周年纪念。
  
  
  
    "Slackware"这个名字借用自Church of the SubGenius中的术语"Slack"。
  
  
  
    在早期的发布版本中，发行版本带有三个用户帐号:  "satan", "gonzo" 和 "snake"。它们是作为示例被提供，但是后来的版本中去除了这些帐号，因为它们有潜在的安全漏洞。
  
  
  
    在1999年，Slackware的发布版本号从4一下子跨越到了 7。Patrick Volkerding 作出解释 : 这是出于市场推广的考虑，为了告诉人们 Slackware 和别的 Linux 发行版本一样"新" (up-to-date) ，当时许多其他发行版本的版本号为 6 。
  
  
  
    在2004年，Patrick Volkerding 得了严重的疾病，Slackware 未来的开发变得不可预测。 在他痊愈后很快恢复了Slackware 的开发。
  
  
  
    在2005年，GNOME桌面环境被从待发布的版本中删除，移交给了社群进行支持。GNOME的删除被Linux社群中的一些人认为是一个警讯，因为GNOME在各种Linux发行版本中都可以找到，一些由社群建立的支援计划也因此诞生。
  
  
  
    贯穿Slackware的历史，出现一些在Slackware基础上制作的发行版本和LiveCD。一些流行的发行版本就起源于 Slackware ，包括SUSE， College Linux 和 Slax。
  
  
    Slackware X86发布名称
  
  
    Slackware 主要为x86 PC 开发。然而曾经存在一些官方的移植 ，像针对DEC Alpha 和 SPARC 架构的。从2005年起，开始出现针对System/390架构的官方移植。同时也存在一些非官方的移植，ARM，Alpha，SPARC，PowerPC 和 x86-64。
  
  
  
    Slackware 13.0，官方首次提供64位的版本下载。
  
  
  
    Slackware 最新稳定发布的版本是 13.37 (直到2011年4月27日) ，其中包括了2.6.37.6和2.6.38.4版本内核，
  
  
  
    Slackware的测试/开发版本称为 '-current' ，这是为了可以使用更多超前的配置。
  
  
  
    KISS， 代表"保持简洁，笨拙" (Keep it Simple, Stupid) ，是一个可以解释很多Slackware中设计选择的概念。在这个文本中，"简洁" ('simple') 指系统设计的观点，而不是指易用性。与大多数其他的发行版不同，KISS(Keep it simple,stupid)是Slackware一贯坚持的原则，尽量保持系统的简洁，从而实现稳定、高效和安全。在KISS哲学里面，简单(Simple)指的是系统设计的简洁性，而不是用户友好(User friendly)。这可能会在一定程度上牺牲了系统的易用性，但却提高了系统的透明性和灵活性。
  
  
  
    正是一直以来对KISS原则的坚持，Slackware赢得了简洁、安全、稳定、高效的名声，也赢得了一大批的忠实用户。
  
  
    启动脚本
  
  
    Slackware 使用BSD风格的初始化脚本，其他的Linux发行版本大多使用 System V 风格的初始化脚本。基本上 System V 风格的每个运行级都是存放初始化脚本的子目录，而BSD 风格仅为每个运行级提供一个脚本。BSD 风格的拥护者认为这样更佳，因为系统可以更容易找到，读取，编辑，和维护脚本。System V的拥护者认为System V 的结构强大和灵活。
  
  
  
    但这些都无关紧要，System V初始化兼容在7.0版本之后被引入了 Slackware 中。
  
  
    软件套件管理
  
  
    Slackware的软件套件管理系统很独特。它的软件套件管理系统和别的发行版本一样可以很容易的安装、升级、移除包。但是它不会试着去追踪或者管理涉及哪些依赖关系 (也就是保证系统拥有所有的安装包内的程序需要的系统库) 。如果所需要的先决条件不能满足，在程序执行之前不会有提醒和指示。
  
  
  
    包都经过gzip压缩和tarball打包，但文件扩展名是.tgz，而不是.tar.gz。他们的结构是这样的: 当在根目录下解压缩和释放，其中的文件会放置于它们的安装位置。因此可以不使用 Slackware的包工具来安装包，而仅仅使用 tar 和 gzip命令，如果包中有doinst.sh脚本，一定要运行它。
  
  
  
    相对的，Red Hat的RPM是CPIO档案，Debian的.deb文件是ar档案。他们都包括一些依赖关系的信息，包管理器工具可以使用这些信息来寻找和安装先决条件。他们在先决条件满足前是不会安装新包的 (虽然可以强制进行) 。
  
  
  
    关于追踪或者无视依赖关系孰优孰劣的争论并不很热闹，这多少让人想起了持续甚久的"vi 对 Emacs" 的"宗教战争"。 Slackware解决问题的方法被技巧熟练的用户群很好的接受了。
  
  
    简单灵活的软件包管理机制
  
  
    Slackware在软件包管理上的独树一帜也是KISS原则的体现。
  
  
  
    Slackware的tgz安装包实际上是经过用tar打包、gzip压缩的文件，和常见的tar.gz 在格式上完全一致，所不同的是tgz包额外包含了软件描述文件和脚本文件。安装软件时， Slackware的包管理工具将安装包解压到指定的目录(默认为根目录)， 解压完之后， 如若存在脚本文件， 则运行此脚本文件。
  
  
  
    需要特别指出的是，Slackware的软件包管理系统，并没有提供自动的检测依赖机制，用户需要手动检测软件的依赖性问题。Slackware的理由则是: 系统管理员应该知道自己系统里有什么东西，也应该知道要安装什么东西。既然各种软件包管理工具都不可能从根本上杜绝dependency hell的恶梦，不如干脆由用户自己来决定。
  
  
  
    由于tgz格式的软件相对来说比较少，使用Slackware时经常需要从源代码自行编译软件。但有趣的是，尽管在软件包管理上Slackware基本上采取的是"放任自流"的方式，但编译软件时极少遇到缺这个库、少那个库的问题，大多数情况下是非常顺利的。
  
  
  
    从Slackware-13.0版本开始， Slackware的安装包开始改为txz格式， 即用tar打包、经过xz压缩的文件。但Slackware的管理器也同时兼容以前的tgz格式。
  
  
  
    为了满足一些用户对自动解决软件依赖性的需求， 目前已出现了Swaret、Slapt-get和SlackUpdate等等第三方项目。
  
  
    Slackware 的中文化支持
  
  
    能否很好地支持中文，是中文用户选择Linux发行版的一个重要标准。
  
  
  
    在很多人的印象中，Slackware对中文的支持不好，这也是Slackware的中文用户比较少的原因之一。实际上， Slackware系统中包含了所有Linux国际化支持的内容，只不过默认安装时，Slackware并没有提供针对国际化内容进行设置的选项。这需要用户手动配置符合自己语言的桌面环境。
  
  
  
    历史上，Slackware确实存在对中文支持不太好的问题，但这是在Linux国际化程度比较差的大环境下，几乎所有发行版都存在的普遍问题。在当时，这促成市场上涌现出了几种以中文处理为优势的"国产"Linux。
  
  
  
    为了方便解决中文处理的问题，海峡对岸的同胞发起了对Linux进行汉化的Chinese Linux Extension(CLE) 项目，把一些零散的中文处理技术整合成一个比较完整的解决方案。CLE的工作成果移植到Slackware之后，确实大大方便了中文用户。但是，随着 glibc、X Window对国际化支持的进步，系统及应用程序的国际化支持程度也大幅度提高，几乎所有的中文化支持都可以在系统默认配置的基础上通过较为简单的设置而实现，不再需要像过去那样安装特殊的中文应用程序。
  
  
  
    Slackware的当前版本已经可以做到通过安装中文字体、修改配置文件、安装中文输入法这几个简单的步骤，就很容易地实现中文显示和输入。系统级的中文打印和LaTeX的中文支持，也能够用比较简单的步骤实现。
  
  
     总结
  
  
    在历史上， Slackware曾经对中文支持方面较差， 结果是Slackware的中文用户数量远远低于其他名气大的发行版。国内 的用户数量少，使得Slackware被蒙上了一层神秘的面纱，直至今日， 一些不准确的传言，如难安装、中文支持不好、易用性差等等，依然让很多用户不敢轻易尝试。
  
  
  
    但实际上，Slackware一直以来是以简洁、安全和稳定所著称的，在世界范围内拥有广大的忠实用户，其地位在各大发行版中始终保持着稳定的排名。
  
  
  
    在软件包的选择上，Slackware不贪多求全，只安装一些常用的软件。软件版本不一定选最新的，而是对安全性和稳定性的考虑更多一些，目的也是减轻系统管理工作的负担。
  
  
  
    在系统的配置方面， Slackware 不遮掩内部细节， 它将系统"真实"的一面毫不隐藏的呈现给用户，让人们看到"真正的"Linux。 这要求用户需要拥有一定量的基础知识， 才能跨过使用Slackware的门槛， 否则难以驾驭此系统。 对此， 批评者认为， 这让很多事做起来太费劲；而支持者回应到这提高了系统的灵活性和透明性， 使得系统趋向于简洁。在一些人眼中，Slackware似乎没有对Linux社区做出什么贡献，它只是把现有的软件绑在一起。但是，Slackware既然能成为目前存活时间最长的发行版，拥有一批忠实的用户，是它一直坚持KISS原则、保持自己独特的风格的结果，这种坚持给用户带来一个简洁、高效和稳定的系统。
  
  
  
    Slackware打包时，对内核和软件的改动尽可能少，除非发现安全漏洞才会打补丁，最大限度地保持了内核和应用软件的原汁原味。
  
  
  
    由于Slackware在系统管理上的简单、透明，以及"不太友好"的配置工具，用户在进行系统管理时，需要对系统有更加深入的了解，更容易真正理解Linux的运行机制。
  
  
  
    正是由于上述的原因，从Slackware入手学习Linux，虽然门槛稍为有点高，但是更容易接触到Linux系统的本质。在Slackware社区，最经常被引用的一句话就是: "When you know Slackware you know Linux. When you know Red Hat, all you know is Red Hat."