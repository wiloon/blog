---
title: CentOS 与 RHEL 的区别
author: "-"
date: 2011-12-11T02:07:25+00:00
url: /?p=1835
categories:
  - Linux
tags:
  - RedHat

---
## CentOS 与 RHEL 的区别
CentOS是Community ENTerprise Operating System的简称，我们有很多人叫它社区企业操作系统，不管你怎么叫它，它都是Linux操作系统的一个发行版本。

CentOS并不是全新的Linux发行版，倘若一说到Red Hat这个大名，大家似乎都听过。在Red Hat家族中有企业版的产品，它是Red Hat Enterprise Linux (以下称之为RHEL) ，CentOS正是这个RHEL的克隆版本。RHEL是很多企业采用的Linux发行版本，需要向Red Hat付费才可以使用，并能得到付过费用的服务和技术支持和版本升级。CentOS可以像RHEL一样的构筑Linux系统环境，但不需要向Red Hat付任何的产品和服务费用，同时也得不到任何有偿技术支持和升级服务。

Red Hat公司的产品中，有Red Hat Linux (如Redhat8,9) 和针对企业发行的版本Red Hat Enterprise Linux，都能够通过网络FTP免费的获得并使用，但是在2003年的时候，Red Hat Linux停止了发布，它的项目由Fedora Project这个项目所取代，并以Fedora Core这个名字发行并提供给普通用户免费使用。Fedora Core这个Linux发行版更新很快，大约半年左右就有新的版本发布。目前的版本是Fedora Core 6，这个Fedora Core试验的韵味比较浓厚，每次发行都有新的功能被加入到其中，得到的成功结果将被采用道RHEL的发布中。虽说这样，频繁的被改进更新的不安定产品对于企业来说并不是最好的选择，大多数企业还是会选择有偿的RHEL产品 (这里面有很深的含义，比如说企业用Linux赚钱，赚到的钱回报给企业，资金在企业间流通，回报社会，提高服务水准等) 。

在构成RHEL的大多数软件包中，都是基于GPL协议发布的，也就是我们常说的开源软件。正因为是这样，Red Hat公司也遵循这个协议，将构成RHEL的软件包公开发布，只要是遵循GPL协议，任何人都可以在原有的软件构成的基础上再开发和发布。CentOS就是这样在RHEL发布的基础上将RHEL的构成克隆再现的一个Linux发行版本。RHEL的克隆版本不只CentOS一个，还有White Box Enterprise Linux和TAO Linux 和Scientific Linux (其他的这些都没听说过，是吧？) 。

虽然说是RHEL的克隆，但并不是一模一样，所说的克隆是具有100%的互换性 (真的么？) 。但并不保障对应RHEL的软件在CentOS上面也能够100%的正常工作。并且安全漏洞的修正和软件包的升级对应RHEL的有偿服务和技术支持来说，数日数星期数个月的延迟情况也有 (其实也没看出来多慢) 。

CentOS的特点

在CentOS的全称里面我们可以看到Enterprise OS，也就是说企业系统，这个企业系统并不是企业级别的系统，而是它可以提供企业级应用所需要的要素。
  
例如: 
  
稳定的环境
  
长期的升级更新支持
  
保守性强
  
大规模的系统也能够发挥很好的性能

CentOS满足以上的要素，满足上面要素的发行版还有Fedora 。Fedora和CentOS非常的相像，但是对CentOS来说，Fedora提供更多的新的功能和软件，发布更新快等特点，这样在稳定性和管理方面就增加了很多工作。企业所需要的系统环境应该是，高效稳定的系统环境，一次构建后能够长期使用的系统环境，所以Fedora那样的频繁更新发布的系统环境并不对应企业的应用。另一方面，CentOS却能够满足以上企业的需要，在众多的RHEL的克隆版本中，CentOS是很出众很优秀的。

CentOS 与 RHEL 的区别

其实为什么有 CentOS？ CentOS 与 RHEL 有什么关系？

RHEL 在发行的时候，有两种方式。一种是二进制的发行方式，另外一种是源代码的发行方式。

无论是哪一种发行方式，你都可以免费获得 (例如从网上下载) ，并再次发布。但如果你使用了他们的在线升级 (包括补丁) 或咨询服务，就必须要付费。

RHEL 一直都提供源代码的发行方式，CentOS 就是将 RHEL 发行的源代码从新编译一次，形成一个可使用的二进制版本。由于 LINUX 的源代码是 GNU，所以从获得 RHEL 的源代码到编译成新的二进制，都是合法。只是 REDHAT 是商标，所以必须在新的发行版里将 REDHAT 的商标去掉。

REDHAT 对这种发行版的态度是: "我们其实并不反对这种发行版，真正向我们付费的用户，他们重视的并不是系统本身，而是我们所提供的商业服务。"

所以，CentOS 可以得到 RHEL 的所有功能，甚至是更好的软件。但 CentOS 并不向用户提供商业支持，当然也不负上任何商业责任。

我正逐步将我的 RHEL 转到 CentOS 上，因为我不希望为 RHEL 升级而付费。当然，这是因为我已经有多年的 UNIX 使用经验，因此 RHEL 的商业技术支持对我来说并不重要。

但如果你是单纯的业务型企业，那么我还是建议你选购 RHEL 软件并购买相应服务。这样可以节省你的 IT 管理费用，并可得到专业服务。

一句话，选用 CentOS 还是 RHEL，取决于你所在公司是否拥有相应的技术力量。

补充: 
  
1. CentOS 还修正了一些 AS 的 BUG，比如安装过程的包选择问题
  
2. CentOS 增加了 yum 在线升级
  
3. CentOS-3.1 = AS3-update1
  
CentOS-3.2 = AS3-update2
  
CentOS-3.3 = AS3-update3
  
CentOS-3.4 = AS3-update4
  
CentOS-3.5 = AS3-update5
  
CentOS-4.0 = AS4
  
CentOS-4.1 = AS4-update1
  
4. 使用 CentOS 完全合法，不涉及版权问题
  
5. 获得 CentOS 很方便，全球提供了 10 多个站点镜像 (HTTP/FTP) ，以及 BT 方式 (常年提供种子) 

很多人不知道 CentOS 是什么，还在拼命找 AS 的下载地址，劝他们他们也不听，可悲。。。

CentOS (Community ENTerprise Operating System) 是Linux发行版之一，它是将Red Hat Enterprise Linux的源代码重新编译而成 (主要是去除Red Hat商标) 。为什么Red Hat容忍CentOS的这种行为？CentOS从Red Hat 服务器下载源代码，编译，免费发放，不提供付费商业支持。Red Hat发布升级补丁，几小时后或至多几天，CentOS也会跟着放出补丁。CentOS这样做完全合法，Red Hat也无可奈何，它的商业就是基于开源模式。但CentOS确实在不断吞食Red Hat的市场，从Google趋势上也能观察到。从目前的情况来看，CentOS造成的伤害还没有到达让Red Hat不得不改变商业模式的地步。而好处是它迫使Red Hat加快创新，使之始终走在其它Linux服务器发行版的前面。CentOS巨大成功的真正的受害者是其它的发行版，如Novell的SLES，Ubuntu Server。