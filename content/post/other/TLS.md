---
title: TLS, HTTPS
author: "-"
date: 2012-03-21T02:51:42+00:00
url: tls
categories:
  - Network
  - Security
tags:
  - reprint
  - remix
---
## TLS, HTTPS

## 创建自签名TLS/SSL证书和私钥

https://www.ssldragon.com/zh/how-to/openssl/create-self-signed-certificate-openssl/

```Bash
# 生成私钥
openssl genpkey -algorithm RSA -out private.key
```

自签名证书里的域名不能用 .dev 结尾, .dev 是 Google 持有的顶级域名, 不能用在自签名证书里

https://stackoverflow.com/questions/49503337/self-signed-dev-cert-untrusted-using-firefox-59-on-ubuntu

https://blog.ideawand.com/2017/11/22/build-certificate-that-support-Subject-Alternative-Name-SAN/
https://www.mikesay.com/2018/12/30/create-self-signed-ssl/
创建 CA 证书用的配置文件 ca.cnf

https://www.mikesay.com/2018/12/30/create-self-signed-ssl/

```Bash
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout selfsigned-key.key -out selfsigned-certificate.crt
```

openssl: 基本命令行工具，用来创建和管理OpenSSL证书，私钥和其它文件。
req: 子命令，主要是用来创建和处理PKCS#10格式的证书请求。它也能创建被用作根证书的自签名证书。
-x509: 这个选项告诉openssl创建一个自签名证书而不是一个证书请求。
-nodes: 这个选项告诉openssl不要加密私钥，否则当使用在Nginx上时，每次Nginx启动都要提示输入密码。
-days 365: 设置证书的有效期为1年（365天）。
-newkey rsa:2048: 这个选项告诉 openss l在生成证书的同时生成私钥。rsa:2048 说明创建一个 2048 比特长的 RSA 私钥。
-keyout: 告诉 openssl 生成的私钥的名字和路径。
-out: 告诉openssl生成的自签名证书和路径。

### 客户端安装自签名证书

```Bash
# ubuntu
# 将证书拷贝到目录“/usr/local/share/ca-certificates”
sudo cp selfsigned-certificate.crt /usr/local/share/ca-certificates
# 更新CA存储
sudo update-ca-certificates

# 删除sudo update-ca-certificates --fresh
sudo rm /usr/local/share/ca-certificates/selfsigned-certificate.crt
sudo update-ca-certificates --fresh
```

## SAN

SAN, Subject Alternative Name（证书主体别名）
是 SSL 标准 x509 中定义的一个扩展。它允许一个证书支持多个不同的域名。通过使用 SAN 字段，可以在一个证书中指定多个 DNS 名称（域名）、
IP 地址或其他类型的标识符，这样证书就可以同时用于多个不同的服务或主机上。这种灵活性意味着企业不需要为每个域名单独购买和安装证书，
从而降低了成本和复杂性。

SAN 的由来, 在早期的互联网中，每个 TLS 证书通常只包含一个 CN 字段，用于标识单一的域名或 IP 地址。
随着虚拟主机技术的发展和企业对于简化管理的需求增加，需要一种机制能够允许单个证书有效的代表多个域名或服务。
例如，一个企业可能拥有多个子域名，希望用单一的证书来保护它们。

为了解决这个问题，SAN 扩展被引入到 X.509 证书标准中。最初在 1999 年的 RFC 2459 中提出，SAN 提供了一种方法来指定额外的主题名称，
从而使得一个证书能有效地代表多个实体。

SAN 的作用和重要性
多域名保护：SAN 使得一个证书可以保护多个域名或子域名，减少了管理的复杂性和成本。
灵活性增强：企业和组织可以更灵活地管理和部署证书，根据需要快速调整和扩展保护范围。
兼容性：随着技术的发展，现代浏览器和客户端软件都已经支持 SAN。它们会优先检查 SAN 字段，如果找到匹配项，通常不会再回退到检查 CN。

如何使用 SAN, 在申请 TLS 证书时，可以指定一个或多个 SAN 值。这些值通常是你希望证书保护的域名或 IP 地址。
证书颁发机构（CA）在颁发证书时会验证这些信息的正确性，并将它们包含在证书的 SAN 字段中。

2、如何在 OpenSSL 证书中添加 SAN
在 OpenSSL 中创建证书时添加 SAN，需要在配置文件中添加一个 subjectAltName 扩展。这通常涉及到以下几个步骤：

准备配置文件：在配置文件中指定 subjectAltName 扩展，并列出要包含的域名和 IP 地址。
生成密钥：使用 OpenSSL 生成私钥。
生成证书签发请求（CSR）：使用私钥和配置文件生成CSR，该CSR将包含SAN信息。
签发证书：使用CA（证书颁发机构）或自签名方式签发证书，证书中将包含SAN信息。

csr.conf

```
[ req ] 
default_bits = 2048 
prompt = no 
default_md = sha256 
req_extensions = v3_ext 
distinguished_name = dn 
   
[ dn ] 
C = CN
ST = Liaoning
L = SZ 
O = Wise2c 
OU = Wise2c 
CN = zmc 
   
[ req_ext ] 
subjectAltName = @alt_names 
   
[ alt_names ] 
DNS.1 = *.zmcheng.com 
DNS.2 = *.zmcheng.net 
DNS.3 = *.zmc.com 
DNS.4 = *.zmc.net 
   
[ v3_ext ] 
basicConstraints=CA:FALSE 
keyUsage=keyEncipherment,dataEncipherment 
extendedKeyUsage=serverAuth,clientAuth 
subjectAltName=@alt_names
```

---

[http://lingfengjazz.popo.blog.163.com/blog/static/94709922008426102358851/](http://lingfengjazz.popo.blog.163.com/blog/static/94709922008426102358851/)

SSL/HTTPS加密技术

SSL (Secure Socket Layer)

为Netscape所研发，用以保障在Internet上数据传输之安全，利用数据加密(Encryption)技术，可确保数据在网络上之传输过程中不会被截取及窃听。目前一般通用之规格为40 bit之安全标准，美国则已推出128 bit之更高安全标准，但限制出境。只要3.0版本以上之I.E.或Netscape浏览器即可支持SSL。

当前版本为3.0。它已被广泛地用于Web浏览器与服务器之间的身份认证和加密数据传输。

SSL协议位于TCP/IP协议与各种应用层协议之间，为数据通讯提供安全支持。SSL协议可分为两层:  SSL记录协议 (SSL Record Protocol) : 它建立在可靠的传输协议 (如TCP) 之上，为高层协议提供数据封装、压缩、加密等基本功能的支持。 SSL握手协议 (SSL Handshake Protocol) : 它建立在SSL记录协议之上，用于在实际的数据传输开始前，通讯双方进行身份认证、协商加密算法、交换加密密钥等。

SSL协议提供的服务主要有:

1) 认证用户和服务器，确保数据发送到正确的客户机和服务器；

2) 加密数据以防止数据中途被窃取；

3) 维护数据的完整性，确保数据在传输过程中不被改变。

SSL协议的工作流程:

服务器认证阶段:

1) 客户端向服务器发送一个开始信息"Hello"以便开始一个新的会话连接；

2) 服务器根据客户的信息确定是否需要生成新的主密钥，如需要则服务器在响应客户的"Hello"信息时将包含生成主密钥所需的信息；

3) 客户根据收到的服务器响应信息，产生一个主密钥，并用服务器的公开密钥加密后传给服务器；

4) 服务器恢复该主密钥，并返回给客户一个用主密钥认证的信息，以此让客户认证服务器。

用户认证阶段: 在此之前，服务器已经通过了客户认证，这一阶段主要完成对客户的认证。经认证的服务器发送一个提问给客户，客户则返回 (数字) 签名后的提问和其公开密钥，从而向服务器提供认证。

从SSL 协议所提供的服务及其工作流程可以看出，SSL协议运行的基础是商家对消费者信息保密的承诺，这就有利于商家而不利于消费者。在电子商务初级阶段，由于运作电子商务的企业大多是信誉较高的大公司，因此这问题还没有充分暴露出来。但随着电子商务的发展，各中小型公司也参与进来，这样在电子支付过程中的单一认证问题就越来越突出。虽然在SSL3.0中通过数字签名和数字证书可实现浏览器和Web服务器双方的身份验证，但是SSL协议仍存在一些问题，比如，只能提供交易中客户与服务器间的双方认证，在涉及多方的电子交易中，SSL协议并不能协调各方间的安全传输和信任关系。在这种情况下，Visa和 MasterCard两大信用卡公组织制定了SET协议，为网上信用卡支付提供了全球性的标准。

https介绍

HTTPS (Secure Hypertext Transfer Protocol) 安全超文本传输协议

它是由Netscape开发并内置于其浏览器中，用于对数据进行压缩和解压操作，并返回网络上传送回的结果。HTTPS实际上应用了Netscape的安全 socket 层 (SSL) 作为HTTP应用层的子层。 (HTTPS使用端口443，而不是象HTTP那样使用端口80来和TCP/IP进行通信。) SSL使用40 位关键字作为RC4流加密算法，这对于商业信息的加密是合适的。HTTPS和SSL支持使用X.509数字认证，如果需要的话用户可以确认发送者是谁。

https是以安全为目标的HTTP通道，简单讲是HTTP的安全版。即HTTP下加入SSL层，https的安全基础是SSL，因此加密的详细内容请看SSL。

它是一个URI scheme(抽象标识符体系)，句法类同http:体系。用于安全的HTTP数据传输。https:URL表明它使用了HTTP，但HTTPS存在不同于HTTP的默认端口及一个加密/身份验证层 (在HTTP与TCP之间) 。这个系统的最初研发由网景公司进行，提供了身份验证与加密通讯方法，现在它被广泛用于万维网上安全敏感的通讯，例如交易支付方面。

限制

它的安全保护依赖浏览器的正确实现以及服务器软件、实际加密算法的支持.

一种常见的误解是"银行用户在线使用https:就能充分彻底保障他们的银行卡号不被偷窃。"实际上，与服务器的加密连接中能保护银行卡号的部分，只有用户到服务器之间的连接及服务器自身。并不能绝对确保服务器自己是安全的，这点甚至已被攻击者利用，常见例子是模仿银行域名的钓鱼攻击。少数罕见攻击在网站传输客户数据时发生，攻击者尝试窃听数据于传输中。

商业网站被人们期望迅速尽早引入新的特殊处理程序到金融网关，仅保留传输码(transaction number)。不过他们常常存储银行卡号在同一个数据库里。那些数据库和服务器少数情况有可能被未授权用户攻击和损害。

## SSL, TLS

[http://www.ruanyifeng.com/blog/2014/02/ssl_tls.html](http://www.ruanyifeng.com/blog/2014/02/ssl_tls.html)
  
[http://www.ruanyifeng.com/blog/2011/08/what_is_a_digital_signature.html](http://www.ruanyifeng.com/blog/2011/08/what_is_a_digital_signature.html)
  
[http://www.ruanyifeng.com/blog/2013/06/rsa_algorithm_part_one.html](http://www.ruanyifeng.com/blog/2013/06/rsa_algorithm_part_one.html)
  
[http://www.youdzone.com/signature.html](http://www.youdzone.com/signature.html)
  
[http://www.ruanyifeng.com/blog/2006/12/notes_on_cryptography.html](http://www.ruanyifeng.com/blog/2006/12/notes_on_cryptography.html)
  
[http://www.ruanyifeng.com/blog/2013/07/rsa_algorithm_part_two.html](http://www.ruanyifeng.com/blog/2013/07/rsa_algorithm_part_two.html)

SSL (Secure Socket Layer)
  
为Netscape所研发，用以保障在Internet上数据传输之安全，利用数据加密(Encryption)技术，可确保数据在网络上之传输过程中不会被截取及窃听。目前一般通用之规格为40 bit之安全标准，美国则已推出128 bit之更高安全标准，但限制出境。只要3.0版本以上之I.E.或Netscape浏览器即可支持SSL.
  
当前版本为3.0。它已被广泛地用于Web浏览器与服务器之间的身份认证和加密数据传输。
  
SSL协议位于TCP/IP协议与各种应用层协议之间，为数据通讯提供安全支持。SSL协议可分为两层:  SSL记录协议 (SSL Record Protocol) : 它建立在可靠的传输协议 (如TCP) 之上，为高层协议提供数据封装、压缩、加密等基本功能的支持。 SSL握手协议 (SSL Handshake Protocol) : 它建立在SSL记录协议之上，用于在实际的数据传输开始前，通讯双方进行身份认证、协商加密算法、交换加密密钥等。
  
SSL协议提供的服务主要有:
  
1) 认证用户和服务器，确保数据发送到正确的客户机和服务器；
  
2) 加密数据以防止数据中途被窃取；
  
3) 维护数据的完整性，确保数据在传输过程中不被改变。

SSL协议的工作流程:
  
服务器认证阶段: 1) 客户端向服务器发送一个开始信息"Hello"以便开始一个新的会话连接；2) 服务器根据客户的信息确定是否需要生成新的主密钥，如需要则服务器在响应客户的"Hello"信息时将包含生成主密钥所需的信息；3) 客户根据收到的服务器响应信息，产生一个主密钥，并用服务器的公开密钥加密后传给服务器；4) 服务器恢复该主密钥，并返回给客户一个用主密钥认证的信息，以此让客户认证服务器。
  
用户认证阶段: 在此之前，服务器已经通过了客户认证，这一阶段主要完成对客户的认证。经认证的服务器发送一个提问给客户，客户则返回 (数字) 签名后的提问和其公开密钥，从而向服务器提供认证。
  
从SSL 协议所提供的服务及其工作流程可以看出，SSL协议运行的基础是商家对消费者信息保密的承诺，这就有利于商家而不利于消费者。在电子商务初级阶段，由于运作电子商务的企业大多是信誉较高的大公司，因此这问题还没有充分暴露出来。但随着电子商务的发展，各中小型公司也参与进来，这样在电子支付过程中的单一认证问题就越来越突出。虽然在SSL3.0中通过数字签名和数字证书可实现浏览器和Web服务器双方的身份验证，但是SSL协议仍存在一些问题，比如，只能提供交易中客户与服务器间的双方认证，在涉及多方的电子交易中，SSL协议并不能协调各方间的安全传输和信任关系。在这种情况下，Visa和 MasterCard两大信用卡公组织制定了SET协议，为网上信用卡支付提供了全球性的标准。

TLS: 安全传输层协议

 (TLS: Transport Layer Security Protocol)

安全传输层协议 (TLS) 用于在两个通信应用程序之间提供保密性和数据完整性。该协议由两层组成:  TLS 记录协议 (TLS Record) 和 TLS 握手协议 (TLS Handshake) 。较低的层为 TLS 记录协议，位于某个可靠的传输协议 (例如 TCP) 上面。 TLS 记录协议提供的连接安全性具有两个基本特性:

私有――对称加密用以数据加密 (DES 、RC4 等) 。对称加密所产生的密钥对每个连接都是唯一的，且此密钥基于另一个协议 (如握手协议) 协商。记录协议也可以不加密使用。
  
可靠――信息传输包括使用密钥的 MAC 进行信息完整性检查。安全哈希功能 ( SHA、MD5 等) 用于 MAC 计算。记录协议在没有 MAC 的情况下也能操作，但一般只能用于这种模式，即有另一个协议正在使用记录协议传输协商安全参数。

TLS 记录协议用于封装各种高层协议。作为这种封装协议之一的握手协议允许服务器与客户机在应用程序协议传输和接收其第一个数据字节前彼此之间相互认证，协商加密算法和加密密钥。 TLS 握手协议提供的连接安全具有三个基本属性:

可以使用非对称的，或公共密钥的密码术来认证对等方的身份。该认证是可选的，但至少需要一个结点方。
  
共享加密密钥的协商是安全的。对偷窃者来说协商加密是难以获得的。此外经过认证过的连接不能获得加密，即使是进入连接中间的攻击者也不能。
  
协商是可靠的。没有经过通信方成员的检测，任何攻击者都不能修改通信协商。

TLS 的最大优势就在于: TLS 是独立于应用协议。高层协议可以透明地分布在 TLS 协议上面。然而， TLS 标准并没有规定应用程序如何在 TLS 上增加安全性；它把如何启动 TLS 握手协议以及如何解释交换的认证证书的决定权留给协议的设计者和实施者来判断。

协议结构

TLS 协议包括两个协议组―― TLS 记录协议和 TLS 握手协议――每组具有很多不同格式的信息。在此文件中我们只列出协议摘要并不作具体解析。具体内容可参照相关文档。

TLS 记录协议是一种分层协议。每一层中的信息可能包含长度、描述和内容等字段。记录协议支持信息传输、将数据分段到可处理块、压缩数据、应用 MAC 、加密以及传输结果等。对接收到的数据进行解密、校验、解压缩、重组等，然后将它们传送到高层客户机。

TLS 连接状态指的是 TLS 记录协议的操作环境。它规定了压缩算法、加密算法和 MAC 算法。

TLS 记录层从高层接收任意大小无空块的连续数据。密钥计算: 记录协议通过算法从握手协议提供的安全参数中产生密钥、 IV 和 MAC 密钥。 TLS 握手协议由三个子协议组构成，允许对等双方在记录层的安全参数上达成一致、自我认证、例示协商安全参数、互相报告出错条件。

## SNI

Server Name Indication (SNI) 是 TLS 协议（以前称为 SSL 协议）的扩展，该协议在 HTTPS 中使用。它包含在 TLS 握手流程中，
以确保客户端设备能够看到他们尝试访问的网站的正确 TLS 证书。该扩展使得可以在 TLS 握手期间指定网站的主机名或域名,
而不是在握手之后打开 HTTP 连接时指定。

SNI的技术原理

SNI通过让客户端发送虚拟域的名称作为 TLS 协商的 ClientHello 消息的一部分来解决此问题。这使服务器可以及早选择正确的虚拟域，
并向浏览器提供包含正确名称的证书。

————————————————
版权声明：本文为CSDN博主「程序猿编码」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：[https://blog.csdn.net/chen1415886044/article/details/116330304](https://blog.csdn.net/chen1415886044/article/details/116330304)

## No subject alternative names present

[https://medium.com/@sajithekanayaka/solved-java-security-cert-certificateexception-no-subject-alternative-names-present-eec1669faf0d](https://medium.com/@sajithekanayaka/solved-java-security-cert-certificateexception-no-subject-alternative-names-present-eec1669faf0d)

## Chrome

Chrome 浏览器内置了一个受信任的根证书颁发机构（CA）列表。 
Chrome 不读取 linux 系统的 ca-certificates, 比如: /usr/local/share/ca-certificates
想在 chrome 里访问 自签名证书的站点, 要把 自签名的 CA 证书加到 chrome里, settings> privacy and security> security> manage certificates> authorities> import> 选择自签名用的 ca.pem
