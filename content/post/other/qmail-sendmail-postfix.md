---
title: qmail sendmail postfix
author: "-"
date: 2013-07-14T09:14:16+00:00
url: /?p=5657
categories:
  - Inbox
tags:
  - reprint
---
## qmail sendmail postfix

[http://liguxk.blog.51cto.com/129038/155491](http://liguxk.blog.51cto.com/129038/155491)

关于 sendmail/qmail/postfix 孰优孰劣,以及部署邮件系统的时候该选哪一个的讨论已经重复了千百次了。但事实往往并不是A好B坏,或B好A坏,必须根据场合和应用的要求来定。但虽然如此,大多数人还是需要一个相对公平的评价,以引导邮件系统的部署。

  自己一直很慎重于回答这类问题,以免引发不必要的争论甚至矛盾,但还是必须面对这个问题做一定的分析和比较的,否则很多朋友经常会问"到底用哪个好？",却拿不出完整的答案。

  首先看看三个MTA的历史...

### MTAs的发展历史

Sendmail
 毫无疑问,sendmail是最古老的MTA之一。它比 qmail和 postfix要古老得多。最早它诞生的时候, Internet还没有被标准化,当时主机之间使用的是UUCP技术来交换邮件。

  它被设计得比较灵活,便于配置和运行于各种类型的机器。

  Qmail
 qmail是新生一代的MTA代表,它以速度快、体积小、易配置安装等特性而著称。作者D. J. Bernstein(djb)是一个数学教授,富有传奇色彩。djb于1995年开发qmail,1996年发布0.70版,并使用了多种当时比较先进的技术,包括Maildir,与sendmail单个binary不同的模块化设计,权限分离,以及使用了大量由djb编写的配套工具,如daemontools,ucsip-tcp等。

  qmail迅速成为了Internet上最有名的MTA,使用者众。

  Postfix
 Postfix作者是Wietse Venema,一名著名的安全专家。最早postfix起源于1996年,当时venema 在美国IBM研究中心负责研究更安全的邮件系统,当时称为Vmailer。后因为商标问题于1998年11月正式更名为Postfix

  Postfix以替代sendmail为目的,并提供了一个更安全、更高性能的灵活的体系。它同样也采用模块化设计,使用了大量优秀的技术,以达到安全的目的。由于作者的设计理念独到,经过7,8年时间,Postfix现今已发展成为功能非常丰富,扩展性和安全性强的优秀MTA。

      概括的比较
    
    
    
      以下的分析主要基于我在CASA上发的一个小文章,对sendmail/qmail/postfix做了一个概括性的比较。
    
    
    
      sendmail
sendmai功能非常强大,很多先进功能在sendmail上都最先有实现。sendmail里的Milter技术是一个非常好的框架,目前postfix及qmail仍然没有官方发布的方案比milter要好。

但sendmail也有典型的历史问题,只有一个binary程序,需要sid权限,m4配置文件复杂难懂。这些是是阻碍sendmail更好发展的一些客观问题。客观来说,调教得好的sendmail,其性能也是相当不俗的,据一个国外的Unix杂志称,在solaris+内存文件系统+带电池的raid系统下,sendmail能达到惊人的287封/秒的注入速度！
    
    
    
      目前sendmail比较适合那些老用户,因为他们习惯了sendmail的应用环境和配置。
    
    
    
      qmail
 qmail体积非常小巧,source的gz包大概只有260多K,是三大MTA中最小的！模块化设计,避免了sid问题,基本功能齐全。配置相对sendmail而言,简单了很多,而且用户非常广泛。而且补丁和插件非常多,例如著名的vpopmail,netqmail,以及qmail-ldap等。

      但qmail有几个问题,一是djb已经5,6年没有继续开发了,补丁的良莠不齐及版本依赖是非常麻烦的事,这对初学者极为不利。二是功能扩充需要补丁来完成,扩展能力不足。
    
    
    
      总体上qmail依然是个非常不错的选择。对于希望了解mta原理,或希望修改mta代码的爱好者,qmail是值得推荐的。对于需要建立中小型邮件系统的用户也同样适合。而对于需要丰富功能却不想面对补丁困难,或者需要建立大型的系统,qmail不太合适,需要更丰富的经验和技术。
    
    
    
      postfix
 postfix如今已经独树一帜,流水线、模块化的设计,兼顾了效率和功能。灵活的配置和扩展,使得配置postfix变得富有趣味。其主要的特点是速度快、稳定,而且配置/功能非常强大,并和sendmail类似,提供了与外部程序对接的API/protocol。尤其是配置部分,可以说是一扫qmail和sendmail的各自缺点。

      但postfix管理及配置的入门依然需要一定的工夫,必须仔细阅读官方文档。postfix另一个优势是至今依然保持活跃的开发工作,而且稳步发展,适合高流量大负载的系统,扩充能力较强。
    
    
    
      大规模应用例子
 国内若干个大型emailISP (如163.net/tom.com/163.com及sohu等) 过去都使用qmail,后来全部更换成postfix。

      新浪使用qmail,yahoo使用qmail。但这些已经不是普通的qmail了。
    
    
    
      技术层面的分析
    
    
    
      这里仅探讨一些典型的技术特点,从这些特点可以看出每个MTA设计的异同,主要讨论的焦点是qmail和postfix。
    
    
    
      磁盘I/O
 从队列文件的读写来看,qmail处理每一封邮件时,都至少需要建立3个文件,mess, intd, info等。而Postfix使用的是单队列文件设计,因此磁盘I/O的开销要比qmail小得多,如果仅仅从这个方面考虑,postfix的队列是qmail的2-4倍那么快。

      从我过去的一个qmail vs postfix对比测试中,也可以发现这个问题。
    
    
    
      数据同步
 如果从MTA对待操作系统的文件是否安全写入磁盘的策略来看,qmail和postfix也是不同的。Postfix使用的是随机写,并且需要写入完成并安全同步到磁盘后才算完成。而qmail的写入则是即刻执行的,因此它将等待数据安全写入磁盘后才返回。对于高流量的系统而言,这将导致性能问题。

此外,Postfix的队列对于不要使用softupdate,除非是有磁盘后写电池。

扩充能力
 sendmail有着非常好的扩充能力,支持众多的特性,功能可谓豪华。包括频率控制到集群支持应有尽有。而milterAPI则更加使sendmail的灵活性发挥至极,通过milter,用户可以对邮件几乎所有的参数进行控制！但是在存储方面,由于只支持mbox,会有一定的问题。

      qmail在系统容量扩展上有着独到的设计,配合qmail-ldap补丁,可以充分利用qmqp及分布存储的优势。现今已有各式各样的qmail扩展方案,最著名的是qmail-ldap。但qmail缺乏类似milter的设计,功能扩展需要各种补丁,而补丁的设计水平参差不齐,配置能力有限。实施起来相对是最复杂的。
    
    
    
      Postfix同样有着非常好的容量扩充能力,利用LMTP或transport的/alias的方法,可以分布式的存储邮件,扩充容量。同时postfix的功能扩展也非常强,通过灵活的配置即可实现复杂的功能,这是其最突出的优点之一,是qmail望尘莫及的。此外,类似sendmail的milter,postfix拥有content_filter和policy 两个与外部程序/应用对接的接口,但不如milter那样功能集中和灵活,也没有完整实现qmail的qmqp及类似qmail-ldap的机制。
    
    
    
      可配置性
 sendmail 使用m4语法,单一的主配置文件 (sendmail.cf) 是三个mta中最难使用的,但是如果熟悉使用的话却能实现复杂的功能。

      qmail使用的是大量小配置文本,格式最简单,每个配置一个文件,存放在/var/qmail/control目录里。
    
    
    
      postfix也使用单一的主配置文件 (main.cf) ,同时还有对应master主服务进程的配置文件master.cf,但使用的是简明易懂的key = value 格式。
    
    
    
      总体而言,qmail的配置文件较易管理 (格式最简单) 但配置文件多 (10个以上) ,而postfix的格式简单只有2个配置文件,并配备强大的postconf工具,sendmail的配置文件最复杂。
    
    
    
      数据库支持
 sendmail通过一些插件/补丁,可以支持MySQL/pgsql/oracle等,ldap及小型的dbm/cdb等数据存储格式。

      qmail默认只支持cdb,需通过补丁才可支持ldap,MySQL,pgsql及oracle等。
    
    
    
      postfix可以支持的数据库应该是最多的,默认就包括了MySQL/pgsql/ldap及dbm/cdb和cidr/nis*/btree等一堆。还支持特殊的tcp_table(仅在snapshot里支持)
    
    
    
      稳定性/负载能力
 sendmail, qmail, postfix都比较稳定。在高负载下,配置不佳或没有打足够补丁的qmail容易被DOS攻击打跨,而postfix在遇到超过配置的限制时会降低处理能力,但系统依然有一定资源可用。

      作者介绍
 sendmail -Eric AllmanUnix专家、学者
 qmail -DJB数学教授,科学家
 Postfix -wietse venema安全专家 学者

Recommentaion - 建议

我建议在使用PostfixMTA,无论是小型系统,还是大中型系统,能带来最高的性价比。

---

在足够好的硬件条件下Postfix比qmail更快的原因分析
 benchmark,无聊还是骗局？
 qmail/postfix/sendmail 比较
 Sendmail 历史
 有关mta benchmark
 Sendmail性能调整
 qmail可靠性FAQ
  