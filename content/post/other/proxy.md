---
title: 代理服务器
author: "-"
date: 2012-01-17T04:37:47+00:00
url: proxy
categories:
  - web
tags:
  - reprint
---
## 代理服务器

代理服务器不仅可以为局域网内的PC提供代理服务，还可以为基于Windows网络的用户提供代理服务。而且代理服务的实现十分简单，它只需在局域网的一台服务器上运行相应的服务器端软件即可。目前代理服务器软件产品主要有: Microsoft Proxy，Microsoft ISA，WinProxy、WinGate、winRoute、SyGate、CCProxy、SuperProxy等；而在UNIX/Linux系统主要采用Squid和Netscape Proxy等服务器软件作为代理。

### squid

在Unix/linux下使用的比较优秀的代理服务器软件Squid。之所以说它比较优秀，是因为它可以在代理服务器上作一个很大的缓存，可以把好多常去的网站内容存储到缓存中，这样，内部网的机器再访问那些网站，就可以从缓存里调用了。这样一方面可以加快内部网浏览因特网的速度，这就是所谓的提高客户机的访问命中率；另一方面，Squid不仅仅支持HTTP协议，而且还支持FTP，GOPHER，SSL和WAIS等协议。

考虑到简捷实用的原则，squid作为代理服务器不仅性能优异，而且还详细的纪录了各个客户端的访问纪录Squid是一个缓存internet数据的一个软件，它接收用户的下载申请，并自动处理所下载的数据。Squid可以工作在很多的操作系统中，如AIX， Digital Unix， FreeBSD， HP-UX， Irix， Linux， NetBSD， Nextstep， SCO， Solaris，OS/2等，也有不少人在其他操作系统中重新编译过Squid。由于它安装简单，使用方便，所以已经被广泛使用。

1 Microsoft Proxy Server

Microsoft Proxy Server是把对Intemet的访问带入一个组织内部每一个桌面上去的一种容易而又安全的方法，它包括Web Proxy服务器，Winsock Proxy服务器和Socks Proxy服务器。Web Proxy为Cache类代理软件，Winsock Proxy通过Winsock协议代理使LAN内的计算机好像直接连接在上一级网络上一样，实际上是通过代理服务器发送请求，但客户端要安装 Microsoft Winsock Proxy Client软件。Microsoft ProxyServer 2.0是Microsoft Bank Ofice客件之一，运行在Windows NT 或Windows 2000环境下。在Windows NT Server4.0上安装时，必须安装3.0或更高版本的IIS(Internet InformationServer)及Windows Service Pack 3或更高版本的补丁。

它容易与安全地安装，充分利用内建在Windows NTServer里的安全性，并允许网络操作员对进入或来自Intemet的访问作有效地控制。它支持全部的Internet协议包括HTTP、FTP、 Gopher、RealAudio、VDOfive、IRC、邮件和新闻协议，支持IPX/SPX和TCP/IP协议来容易访问Intemet服务器以及内部网上的应用软件。它提供超高速缓存，保存网络带宽，改善客户机的响应时问，减少网络的拥挤，并且在不加重最终用户和网络管理员负担的情况下改善对网络资源的控制。管理员可以根据用户、服务、端口或IP域来允许或拒绝入站或出站的连接，可以阻止对一些指定站点的访问，但不能采用直接导入方法来设定允许访问站点地址。它与NT网络系统管理服务集成，ProxyServer生成一套Windows NT Performance Counters来监视网络上任何一台代理服务器的状态，与Windows NT ServerDirectory Services集成来用户等级的验证。井提供防火墙等Intemet安全认证特性。

2 Wingate

Wingate是Qbic公司的产品，软件分为服务器和客户两部分。服务器可运行于Win 98或Win NT平台，提供用户认证，各种网络应用层协议代理，Intemet访问控制，包过滤等服务;客户部分为一个用户登录程序Gatekeeper，用户使用它在代理服务器上进行登录，代理服务器将用户的IP地址与相应用户账号绑在一起。如果这一用户是管理员，还可以使用Gatekeeper进行远程管理。 Wingate支持双网络接口，一个接口通过网络适配器卡连接内部局域网络，另一个网络接口连接Intemet，两块网卡问的IP转发要禁用，使内部网络与外部网络完全隔开，形成双宿网关防火墙。Wingate也支持单网卡，在许多校园网中，只允许部分计算机具有Intemet访问权，利用这些计算机作为代理服务器，为其他的计算机提供服务，只是它不具备防火墙的功能。Wingate除了提供FTP Proxy、Telnet Proxy、 POP3 Proxy、RealAudio Proxy、Socks Pmxy代理服务之外，还提供了DNS、DHCP、拨号管理等丰富功能。

3 SyGate

SyGate是一种支持多用户访问Intemet的软件，并且是只通过一台计算机，共享Intemet账号，达到上网的目的。SyGate能在目前诸多流行的操作系统上运行，譬如: Window s9 5、Windows98、Windows NT，Windows2000等操作系统;同时，SyGate还支持多数的Internet连接方式。在TCP/IP网络上，SyGate Client能让用户从任何一台计算机上远程监察和管理SyGate Server。SyGate诊断程序(SyGate Diagnostics)在任何时候都能帮助你确定你的系统设置以及解决网络连接的问题。SyGate设有使用日志文件以及系统设置文件，在需要的时候可轻易地查寻与检测。尽管这些功能并非是必须的，SyGate还是能以其高度的可配适性，满足任何小型网络中的多种需要。SyGate能设置防止访问一些不受欢迎的站点("黑名单" 站点)，也能设限使之只能访问某些受欢迎的站点("白名单"站点)。SyGate利用其"端口锁定技术"(port blocking technology)防止来自Intemet的非法入侵。它支持如下协议或服务: HTTP、H1vrPS、POP3、NNTP、SMTP、 TELNET、FTP (PASV模式)、IRC、ICQ、MS CHAT、RealAuclio(TCP模式)以及许多网络游戏。SyGate(r)Office Network或SyGate(r)Home Network version4.0及以后版本支持Windows 2000和Windows Me，使用Windows 2000或Windows Me作为SyGate server，则不可同时使用它的Internt连接共享(ICS)功能。SyGate(r)HomeNetwork 4.2或SyGate(r)Office Network 4.2 build 803及以后版本支持Windows XP，但不可同时使用它的Intemt连接共享功能或Intemet防火墙。

4 WinProxy

与前面介绍的代理服务器软件相比，WinProxy是一个集大成者。它集中了WinRoute和WinGate的强大功能与SyGate的易用于一身。 WinProxy结合了最新的Internet连接共享(Internet Connection Sharing)的技术，是一个特别易于安装和使用的代理服务器软件，价格还比较便宜。它可以在Windows 95、Windows98、Windows NT Server 4.0或Windows NT Workstation 4.0上运行。

WinProxy的一大特色是，提供了"Transparent Proxy"(透明代理)技术，吸取了Proxy Server和Network Address Transaltion(NAT)技术的优点，融合了Proxy Server的复杂的用户控制、缓存与防火墙技术及NAT技术的易于安装、对应用透明的特点。只需要几分钟，用户就可以安装好，并且使用。 WinProxy作为一个代理服务器软件，除了保护本地局域网不受外来攻击以外，还特别提供了防病毒保护，这也是其他同类软件所没有的特征。可以选择预定义的防火墙安全设置或者自己来为自己的网络定制安全设置。在最新的版本3.0里，包含了一个可以免费使用6个月的Trend Micro的检查病毒的流行软件，提供了网络层次上的防病毒保护，能够监测到隐藏在电子邮件或者FTP下载文件中的危险分子，在它们危害到您的网络之前识别出来并拒之门外。WinProxy 3.0提供了一个很有特色、也是很符合需要的功能一阻塞广告。现在Internet上虽然商业还不是太发达，但是广告却是满天飞，有时候浏览一个页面，一大半是广告，不但浪费了网络流量，还减慢了浏览速度，比较令人讨厌。可以让用户设置这个选项来阻止广告信息的下载，使每个网页只是显示其中的内容。

WinProxy在访问控制方面提供了灵活的机制。WinProxy提供了站点过滤的功能，可以把一些特定的不适合的站点过滤掉，不让用户访问这些站点;可以定义站点黑名单Blacklisting，黑名单中记录着受禁的IP地址、域和网络，与站点过滤结合，增加一些更多的不让用户访问的站点，如果用户企图访问IP地址列在黑名单中的主机，WinProxy将在用户的浏览器中显示出错信息: Forbidden HTML(受禁的HTM 还可以定义站点白名单，指定用户只能访问哪些站点，而不能访问其他任何站点，如果用户企图访问IP地址不列在白名单中的主机，WinProxy将在用户的浏览器中显示出错信息: Forbidden HTML(受禁的HTML)。WinProxy还提供了其他的安全措施。例如，可以依据IP地址限制特定的客户PC访问Intemet。可以通过限制用户对特定协议的访问，来进一步调节用户对Internet的访问权限。这样，就可以做到仅仅提供用户实际需要的协议，比如，可以提供Web和邮件访问，而限制FTP和Usenet访问。

WinProxy支持所有的Internet接入方式，包括Modem、CableModem、 DSL.ISDN等等。在协议的支持上，WinProxy是几个代理服务器软件中较为完备的，支持Internet上大部分的流行协议: HTTP、 Real Audio/Video、Mail(SMTP and POP3)、FTP.News、Telnet.Socks.Secure Sockets(ssL).DNS.IMAP4等，还支持ISP在线服务AOL美国在线、MSN微软网等等。

5 WinRoute

WinRoute除了具有代理服务器的功能外，还具有NAT (Network Address Translation，网络地址转换) 、防火墙、邮件服务器、DHCP服务器、DNS服务器等功能，能为用户提供一个功能强大的软网关。

WinRoute有很多选项设置，涉及到网络配置的方方面面，但是它的帮助系统却不是很完善，由于 WinRoute具有DHCP服务器的功能，局域网内部的机器还可配置成由WinRoute动态分配IP地址。WinRoute的Commands选单比较简单，可以进行拨号、断线、收发电子邮件。总体来说，WinRoute的网络功能相当全面，是一个优秀的软网关；美中不足的就是它的用户界面显得有些简单，帮助系统不完善，从而增加了配置工作的难度。

6 CCProxy

CCProxy功能强大，完全支持Win98.WinMe、WinNT、Win2000、WinXp、Win2003。支持共享Modem.ISDN、ADSL、DDN、专线.蓝牙、二级代理等访问Intemeh支持HTTP.FTP、Gopher、SOCK$4/5.Telnet、Secure(HTTPS)、 News(NNTP).RTSP、MMS等代理协议;支持浏览器通过H1vrP/Secure/FTP(Web)/Gopher代理上网;支持客户端使用 Outlook、OutlookExpress、Foxraail等通用邮件客户端软件收发邮件;支持OICQ、ICQ、Yahoo Messenger、MSN、iMRC、联众游戏、股票软件通过HTTPS、SOCKS5代理上网;支持CuteFTP、CuteFTP Pro.WS-FTP.FXP-FTP等FTP软件通过代理上网;支持RealPlayer

通过RTSP代理接收视频，支持 MediaPlayer通过MMS代理接收视频;支持Net1rerm通过Telnet代理上网;支持Outl00k通过News代理连接新闻服务器;支持远程拨号、自动拨号、自动断线、自动关机功能;支持二级代理，可以使代理服务器通过其他代理服务器上网。双击界面上的绿色网格可以实时观测代理用户连接信息。具有简单实用的账号管理功能，可以针对不同用户定义不同的上网限制;账号管理支持IP段设置方式和自动扫描账号，建立账号更轻松;具有多种方式的账号认证方式和混和应用功能: IP地址、MAC地址、用户名密码、域账号管理。另外，还具有HTTP和SOCKS5用户验证、内置域名解析功能DNS、时间管理功能、网站过滤、缓存、带宽控制、加载代理广告条、启动时拨号、端口映射、流量计费等功能。支持WinNT/Win2K/Wir1)(P /Win2003下以NT服务运行方式。

7 Microsoft lSA Server

ISA Server Internet Security and Acceleration (ISA)Server提供了Intemet连接方案，它不仅包括特性丰富且功能强大的防火墙，还包括用于加速Internet连接的可伸缩的Web缓存。根据组织网络的设计和需要，ISA Server的防火墙和Web缓存组件可以分开配置，也可以一起安装。利用Windows 2Oo0安全数据库，ISA Server允许根据特定的通信类型，为Windows2000 Server内定义的用户、计算机和组设置安全规则，具有先进的安全特性。

利用ISA Management控制台，ISA Server使防火墙和缓存管理变得很容易。ISA Management采用MMC，并且广泛使用任务板和向导，大大简化了最常见的管理程序，从而集中统一了服务器的管理，通过使用单一界面进行集中管理，可以得到更高的安全。ISA Server提供强大的基于策略的安全管理。这样，管理员就能将访问和带宽控制应用于所设置的任何策略单元，如用户、计算机、协议.内容类型、时间表和站点。所有的管理任务可以在一台计算机上执行，而配置却可以用于所有的计算机。ISA Server是一个拥有自己的软件开发工具包和脚本示例的高扩展性平台，利用它管理员可以根据网络业务需要量身定制Internet安全解决方案。

8 SuperProxy

SuperProxy是一个功能强大，速度快，稳定性和安全性较高的成熟产品，它运行在Windows 95/98/Me/Nt/2000/XP等平台上， 而且在每一种平台都严格地进行过100小时大用户量的压力测试，具有良好的兼容性。

它支持网络软件广泛使用的各类代理协议，例如ftp， smtp， dns， pop3， socks， http等代理，适合家庭用户，从事网吧的用户，企业和公司用户共享上网的需要，同时本软件遵从功能强大，设置简单，界面直观，性能优异的开发原则，力求做到各不同层次的用户都较容易掌握，几乎不用任何设置就可以正常工作，这是其它同类的专业软件所不能比拟。

