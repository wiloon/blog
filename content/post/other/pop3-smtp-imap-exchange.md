---
title: POP3、SMTP、IMAP和Exchange
author: "-"
date: 2013-05-20T11:47:32+00:00
url: pop3
categories:
  - Network
tags:
  - reprint
  - Mail
---
## POP3, SMTP, IMAP 和 Exchange

当前常用的电子邮件协议有 SMTP、POP3、IMAP4, 它们都隶属于TCP/IP协议簇, 默认状态下, 分别通过 TCP 端口 25、110 和 143 建立连接

## SMTP, Simple Mail Transfer Protocol

SMTP 是一种提供可靠且有效电子邮件传输的应用层协议。SMTP 协议属于TCP/IP协议族, 主要用于传输系统之间的邮件信息并提供来信有关的通知。

SMTP 目前已是事实上的 E-Mail 传输的标准。

SMTP端口587

SMTP 即简单邮件传输协议,它是一组用于由源地址到目的地址传送邮件的规则,由它来控制信件的中转方式。
它帮助每台计算机在发送或中转信件时找到下一个目的地。通过SMTP协议所指定的服务器, 就可以把E－mail寄到收信人的服务器上了, 整个过程只要几分钟。
SMTP 服务器则是遵循 SMTP 协议的发送邮件的服务器, 用来发送或中转发出的电子邮件。

SMTP认证,简单地说就是要求必须在提供了账户名和密码之后才可以登录 SMTP 服务器,  这就使得那些垃圾邮件的散播者无可乘之机。增加 SMTP 认证的目的是为了使用户避免受到垃圾邮件的侵扰。

SMTP 独立于特定的传输子系统,且只需要可靠有序的数据流信道支持。SMTP 重要特性之一是其能跨越网络传输邮件,即" SMTP 邮件中继"。通常,一个网络可以由公用互联网上 TCP 可相互访问的主机、防火墙分隔的 TCP/IP 网络上 TCP 可相互访问的主机,及其它 LAN/WAN 中的主机利用非 TCP传输层协议组成。使用 SMTP ,可实现相同网络上处理机之间的邮件传输,也可通过中继器或网关实现某处理机与其它网络之间的邮件传输。

在这种方式下,邮件的发送可能经过从发送端到接收端路径上的大量中间中继器或网关主机。域名服务系统 (DNS) 的邮件交换服务器可以用来识别出传输邮件的下一条 IP 地址。

在传输文件过程中使用端口: 25

是因特网电子邮件系统首要的应用 层协议。它使用由TCP提供的可靠的数据传输服务把邮件消息从发信人的邮件服务器传送到收信人的邮件服务器。跟大多数应用层协议一样,SMTP也存在两个 端: 在发信人的邮件服务器上执行的客户端和在收信人的邮件服务器上执行的服务器端。SMTP的客户端和服务器端同时运行在每个邮件服务器上。当一个邮件服 务器在向其他邮件服务器发送邮件消息时,它是作为SMTP客户在运行。当一个邮件服务器从其他邮件服务器接收邮件消息时,它是作为SMTP服务器在运行。

SMTP协议与人们用于面对面交互的礼仪之间有许多相似之处。首先,运行在发送端邮件服务器主机上的SMTP客户,发起建立一个到运行在接收端邮件服务 器主机上的SMTP服务器端口号25之间的TCP连接。如果接收邮件服务器当前不在工作,SMTP客户就等待一段时间后再尝试建立该连接。这个连接建立之 后,SMTP客户和服务器先执行一些应用层握手操作。就像人们在转手东西之前往往先自我介绍那样,SMTP客户和服务器也在传送信息之前先自我介绍一下。 在这个SMTP握手阶段,SMTP客户向服务器分别指出发信人和收信人的电子邮件地址。彼此自我介绍完毕之后,客户发出邮件消息。SMTP可以指望由 TCP提供的可靠数据传输服务把该消息无错地传送到服务器。如果客户还有其他邮件消息需发送到同一个服务器,它就在同一个TCP连接上重复上述过程;否 则,它就指示TCP关闭该连接。[1]

### curl smtp

https://everything.curl.dev/usingcurl/smtp

```Bash
curl smtp://local-lab:1025 --mail-from from0@local-lab.com --mail-rcpt receiver0@local-lab.com

curl --connect-timeout 3 smtp://local-lab:1025 --mail-from from0@local-lab.com --mail-rcpt receiver0@local-lab.com --upload-file foo.txt
```

foo.txt

```Bash
From: John Smith <john@example.com>
To: Joe Smith <smith@example.com>
Subject: an example.com example email
Date: Mon, 7 Nov 2016 08:45:16

Dear Joe,
Welcome to this example email. What a lovely day.
```

### POP协议

POP邮局协议负责从邮件服务器中检索电子邮件。它要求邮件服务器完成下面几种任务之一: 从邮件服务器中检索邮件并从服务器中删除这个邮件；从邮件服务器中检索邮件但不删除它；不检索邮件,只是询问是否有新邮件到达。POP协议支持多用户互联网邮件扩展,后者允许用户在电子邮件上附带二进制文件,如文字处理文件和电子表格文件等,实际上这样就可以传输任何格式的文件了,包括图片和声音文件等。在用户阅读邮件时,POP命令所有的邮件信息立即下载到用户的计算机上,不在服务器上保留。 POP3(Post Office Protocol 3)即邮局协议的第3个版本,是因特网电子邮件的第一个离线协议标准。

POP3协议允许电子邮件客户端下载服务器上的邮件,但是在客户端的操作 (如移动邮件、标记已读等) ,不会反馈到服务器上,比如通过客户端收取了邮箱中的3封邮件并移动到其他文件夹,邮箱服务器上的这些邮件是没有同时被移动的 。  

### IMAP

默认端口: 143

互联网信息访问协议 (IMAP) 是一种优于POP的新协议。和 POP一样,IMAP也能下载邮件、从服务器中删除邮件或询问是否有新邮件,IMAP克服了POP的一些缺点。例如,它可以决定客户机请求邮件服务器提交所收到邮件的方式,请求邮件服务器只下载所选中的邮件而不是全部邮件。客户机可先阅读邮件信息的标题和发送者的名字再决定是否下载这个邮件。通过用户的客户机电子邮件程序,IMAP可让用户在服务器上创建并管理邮件文件夹或邮箱、删除邮件、查询某封信的一部分或全部内容,完成所有这些工作时都不需要把邮件从服务器下载到用户的个人计算机上。支持种IMAP的常用邮件客户端有: ThunderMail,Foxmail,Microsoft Outlook等。

而IMAP提供webmail 与电子邮件客户端之间的双向通信,客户端的操作都会反馈到服务器上,对邮件进行的操作,服务器上的邮件也会做相应的动作。
  
同时,IMAP像POP3那样提供了方便的邮件下载服务,让用户能进行离线阅读。IMAP提供的摘要浏览功能可以让你在阅读完所有的邮件到达时间、主题、发件人、大小等信息后才作出是否下载的决定。此外,IMAP更好地支持了从多个不同设备中随时访问新邮件。

## Exchange

Exchange是个消息与协作系统的系列产品。包括服务器产品、客户端产品等等。

Exchange Server 是一个设计完备的邮件服务器产品, 提供了通常所需要的全部邮件服务功能。除了常规的 SMTP/POP 协议服务之外,它还支持 IMAP4 、LDAP 和 NNTP 协议。Exchange Server 服务器有两种版本,标准版包括 Active Server、网络新闻服务和一系列与其他邮件系统的接口；企业版除了包括标准版的功能外,还包括与 IBM OfficeVision、X.400、VM 和 SNADS 通信的电子邮件网关,Exchange Server 支持基于Web 浏览器的邮件访问。

Microsoft Exchange Online 是一个电子邮件、日程和联系人云解决方案。它提供和Microsoft Exchange Server相同的技术方案。

Microsoft Exchange Server使用RPC protocol, MAPI/RPC (Microsoft Outlook client)  ,支持Exchange ActiveSync (安全和 Exchange server同步邮件、联系人和其它数据) ,支持ActiveSync push e-mail, 这些功能已经使用到iPhone和Android 等设备。

>[http://en.wikipedia.org/wiki/Microsoft_Exchange_Server](http://en.wikipedia.org/wiki/Microsoft_Exchange_Server)
>[http://blog.csdn.net/forlong401/article/details/7545180](http://blog.csdn.net/forlong401/article/details/7545180)
