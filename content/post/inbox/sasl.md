---
title: "sasl"
author: "-"
date: "2021-08-13 17:00:11"
url: sasl
categories:
  - inbox
tags:
  - reprint
---
## "sasl"

### SASL - 简单认证和安全层

身份验证是很多C/S模式应用协议的通用需求，为了避免每个协议都单独实现一套验证逻辑，SASL(Simple Authentication and Secure Layer)被提出了, 它定位成为基于可靠连接的应用协议提供身份验证和数据安全服务的通用框架。SASL定义了通用的身份验证信息交换的流程, 并且包含一系列验证机制。这些验证机制完成具体的身份验证逻辑。这样，SASL就成为了一个将应用协议和验证机制相连接的抽象层，如下图所示。

   -------------------------------------------------------------

         +----+   +----+    +----+   +-------------------+
         |SMTP|   |LDAP|    |XMPP|   |Other protocols ...|
         +--+-+   +--+-+    +--+-+   +--+----------------+
            |        |         |        |
            |        |         |        |
      ------+--------+---------+--------+------------------
                  SASL abstraction layer
      ------+--------+---------+--------+------------------
            |        |         |        |
            |        |         |        |
      +-----+--+  +--+---+  +--+--+  +--+-----------------+
      |EXTERNAL|  |GSSAPI|  |PLAIN|  |Other machanisms ...|
      +--------+  +------+  +-----+  +--------------------+

   -------------------------------------------------------------
任何应用协议都可以使用任何验证机制，而具体使用哪个机制则由应用协议的客户端和服务器进行协商。

分别以”C:”和”S:”代表客户端和服务端，SASL规定的验证信息交换的基本流程为:

      C: 请求验证交换
      S: 最初的挑战码
      C: 最初的响应消息
      <额外的挑战码/响应消息>
      S: 身份验证结果

根据机制不同，流程略有差异。

具体应用哪个机制进行身份验证由使用SASL的应用协议来协商。服务器向客户端通告服务器所支持的机制, 客户端从中选择一个它支持且最合适的机制并通知服务器，请求开始身份验证。接下来便是上述的一系列Chalenges/Responses信息交换。这些信息载体的形式由应用协议指定。最终服务器发送回身份验证的结果。

SASL机制注册由IANA维护:
http://www.iana.org/assignments/sasl-mechanisms/sasl-mechanisms.xhtml

下面说明几个具体的SASL机制: 

EXTERNAL:
EXTERNAL机制允许客户端请求服务器使用其他途径获取的验证信息来验证该客户端。如通过TLS获取的验证信息。以ACAP(Application Configuration Access Protocol)协议来举例:

S: * ACAP (SASL "DIGEST-MD5")
C: a001 STARTTLS
S: a001 OK "Begin TLS negotiation now"
<TLS negotiation, further commands are under TLS layer>
S: * ACAP (SASL "DIGEST-MD5" "EXTERNAL")
C: a002 AUTHENTICATE "EXTERNAL"
S: + ""
C: + ""
S: a002 OK "Authenticated"
在TLS安全层建立后，服务端通告它支持DIGEST-MD5和EXTERNAL机制，客户端选择使用EXTERNAL机制，并且不使用其他授权实体。服务器使用外部信息验证通过后，返回成功的响应。

PLAIN
PLAIN机制只需要传递一条消息，这个消息由授权实体，验证实体和密码三部分组成。如下图所示:

authzid<NUL>authcid<NUL>passwd
授权实体authzid为可选的。如果提供了它，身份验证通过后，如果权限允许，将以authzid身份进行操作。如果权限不允许，则服务器返回授权失败。由于PLAIN机制直接传递密码本身，因而不应该在没有私密性保护的连接上使用。
同样以ACAP协议举例:

S: * ACAP (SASL "CRAM-MD5") (STARTTLS)
C: a001 STARTTLS
S: a001 OK "Begin TLS negotiation now"
<TLS negotiation, further commands are under TLS layer>
S: * ACAP (SASL "CRAM-MD5" "PLAIN")
C: a002 AUTHENTICATE "PLAIN" {20+}
C: Ursel<NUL>Kurt<NUL>xipj3plmq
S: a002 NO "Not authorized to requested authorization identity"
TLS安全层建立后，服务器通告它支持CRAM-MD5和PLAIN机制，客户端选择PLAIN机制，并发送身份验证消息，服务器返回授权失败，即Kurt身份验证通过，但不能以Ursel的身份进行操作。

SCRAM-SHA-1
SCRAM是一系统机制的统称，具体机制名称后缀上算法所使用的HASH函数。我们以SCRAM-SHA-1举例，它使用SHA-1哈希函数。PLAIN机制在网络上传输的是密码本身，因而只应该用在TLS等安全层之上。SCRAM机制则没有这个限制。

下面的例子略去机制协商的过程, 用户名为”user”, 密码为”pencil”:

C: n,,n=user,r=fyko+d2lbbFgONRv9qkxdawL
S: r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j,s=QSXCR+Q6sek8bf92, i=4096
C: c=biws,r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j,p=v0X8v3Bz2T0CJGbJQyF0X+HI4Ts=
S: v=rmF9pqV8S7suAoZWja4dJRkFsKQ=
SCRAM机制的消息由多个属性构成，每个属性为”a=xxx”的形式，而且属性有顺序要求。

客户端发送的首条消息包括了以下内容: 

一个GS2头，它包括一个字符，只能为”n”, “y”, “p”，是通道绑定的标识，和一个授权实体 (例子中没有提供，因而为”,,”,当需要指定时使用属性a, 如”a=dummy”) 。
属性n, 表示身份验证的用户名。
属性r, 表示客户端nonce, 一个随机的可打印字符串(不能包括”,”)。
我们把后两部分称为client_first_message_bare, 后面算法中要使用它。

然后服务器回应首条消息。属性r为客户端NONCE拼接上服务器的随机NONCE值，属性s为使用BASE64编码后的用户密码的salt值，属性i为迭代次数。在后面介绍的算法中可以看到具体用途。这条消息我们称为server_first_message, 后面算法需要使用它。

接着，客户端发送末条消息。属性c为使用BASE64编码的GS2头及通道绑定数据。例子中的”biws”解码后为”n,,”, 即客户端首条消息的第一部分，属性r与服务器回应的属性r必须相同。属性p为使用BASE64编码的客户端证明信息(ClientProof)。它由客户端使用后面介绍的算法计算得到。我们把前两个属性称为client_final_message_without_proof, 后面算法要使用它。

服务端验证客户端发送的NONCE值和证明信息(ClientProof)，如果提供了授权实体，则也需要验证是否可以授权给该实体，然后发送服务端末条消息。属性v为服务器签名(ServerSignature)。客户端通过比较计算得到的和从服务端所收到的签名是否相同来对服务器进行身份验证。如果服务器验证失败，将回应属性e, 它可以用来诊断错误原因。

下面介绍客户端和服务器签名的具体算法: 

SaltedPassword := Hi(Normalize(password), salt, i)
ClientKey := HMAC(SaltedPassword, "Client Key")
StoredKey := H(ClientKey)
AuthMessage := client-first-message-bare + "," + server-first-message + "," + client-final-message-without-proof
ClientSignature := HMAC(StoredKey, AuthMessage)
ClientProof := ClientKey XOR ClientSignature
ServerKey := HMAC(SaltedPassword, "Server Key")
ServerSignature := HMAC(ServerKey, AuthMessage)
其中HMAC原型为HMAC(key, str), Hi函数算法为:

Hi(str, salt, i):

U1 := HMAC(str, salt + INT(1))
U2 := HMAC(str, U1)
...
Ui-1 := HMAC(str, Ui-2)
Ui := HMAC(str, Ui-1)
Hi := U1 XOR U2 XOR ... XOR Ui
用PHP实现该算法来验证上述例子:


function hi($str, $salt, $i) {
    $int1 = "\0\0\0\1";
    $ui = hash_hmac("sha1", $salt . $int1, $str, true);
    $result = $ui;

    for ($k = 1; $k < $i; $k++) {
        $ui = hash_hmac("sha1", $ui, $str, true);
        $result = $result ^ $ui;
    }

    return $result;
}

$password = "pencil";
$salt = base64_decode('QSXCR+Q6sek8bf92');
$i = 4096;
$client_first_message_bare = 'n=user,r=fyko+d2lbbFgONRv9qkxdawL';
$server_first_message = 'r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j,s=QSXCR+Q6sek8bf92,i=4096';
$client_final_message_without_proof = 'c=biws,r=fyko+d2lbbFgONRv9qkxdawL3rfcNHYJY1ZVvWVs7j';

$salted_password = hi($password, $salt, $i);
$client_key = hash_hmac("sha1", "Client Key", $salted_password, true);
$stored_key = sha1($client_key, true);
$auth_message = $client_first_message_bare . ","
                . $server_first_message . ","
                . $client_final_message_without_proof;
$client_signature = hash_hmac("sha1", $auth_message, $stored_key, true);
$client_proof = $client_key ^ $client_signature;

$server_key = hash_hmac("sha1", "Server Key", $salted_password, true);
$server_signature = hash_hmac("sha1", $auth_message, $server_key, true);

echo "p=" . base64_encode($client_proof) . "\n";
echo "v=" . base64_encode($server_signature) . "\n";

输出结果为:

p=v0X8v3Bz2T0CJGbJQyF0X+HI4Ts=
v=rmF9pqV8S7suAoZWja4dJRkFsKQ=
与上述例子中值相符。

在实际项目中，一般不需要自己来实现这些验证算法。C语言可直接使用CyrusSASL库或GNU的libgsasl。


SASL是一种用来扩充C/S模式验证能力的机制认证机制,  全称Simple Authentication and Security Layer.

当你设定sasl时，你必须决定两件事；一是用于交换“标识信 息” (或称身份证书) 的验证机制；一是决定标识信息存储方法的验证架构。

sasl验证机制规范client与server之间的应答过程以及传输内容的编码方法，sasl验证架构决定服务器本身如何存储客户端的身份证书以及如何核验客户端提供的密码。

如果客户端能成功通过验证，服务器端就能确定用户的身份， 并借此决定用户具有怎样的权限。

比较常见的机制；
4.1 plain(较常用)
   plain是最简单的机制，但同时也是最危险的机制，因为身份证书 (登录名称与密码) 是以base64字符串格式通过网络，没有任何加密保护措施。因此，使用plain机制时，你可能会想要结合tls。
4.2 login
   login不是其正式支持的机制，但某些旧版的mua使用这种机制，所以cyrus sasl让你可选择其是否支持login机制。如果你的用户仍在使用这类老掉牙的mua，你必须在编译sasl函数库时，指定要包含login的支持。 login的证书交换过程类似plain。
4.3 otp
otp是一种使用“单次密码”的验证机制。此机制不提供任何加密保护，因为没必要－－每个密码都只能使用一次，每次联机都要改用新密码。smto client必须能够产生otp证书。
4.4 digest-md5(较常用)
   使用这种机制时，client与server共享同一个隐性密码，而且此密码不通过网络传输。验证过程是从服务器先提出challenge (质询) 开始， 客户端使用此challenge与隐性密码计算出一个response (应答) 。不同的challenge，不可能计算出相同的response；任何拥 有secret password的一方，都可以用相同的challenge算出相同的response。因此，服务器只要比较客户端返回的response是否与自己算 出的response相同，就可以知道客户端所拥有的密码是否正确。由于真正的密码并没有通过网络，所以不怕网络监测。
4.5 kerberos
   kerberos是一种网络型验证协议。除非你的网络已经使用kerberos，否则你应该用不到kerberos机制；相对的，如果你的网络已经架设了kerberos验证中心，sasl就能完美的将smtp验证整合进现有的体系。
4.6 anonymous
   anonymous机制对smtp没有意义，因为smtp验证的用意在于限制转发服务的使用对象，而不是为了形成open relay，sasl之所以提供这种机制，主要是为了支持其他协议。
当 客户端链接到一个支持sasl的邮件服务器时，服务器会以优先级列出可用的机制供客户端选择。如果客户端也支持多钟机制，则当第一种机制验证失败时，客户 端可能会继续尝试第二种机制，直到通过验证或是所有机制都失败为止。如果双方在一开始就无法协调出共同的机制，验证过程就算失败。
一旦双方在使用哪种机制上达成共识，就开始进行验证过程。实际的交互过程随机制而定，但通常包含一次或多次应答过程。验证协议本身也规定了应答内容的编码格式。

### 总结 
数字证书, 是级联认证派发的, 最上层是根CA认证中心. 数字证书的根本作用, 是为了保证所有人公钥的安全性和真实性. 大致认证过程是: 通过CA的公钥来解出该CA所派发的证书里面所包含的公钥(用户或者机构的). 并通过该公钥来验证证书持有人的真实性. (因为持有人并不一定是证书所有人)

通过上面对SSL的分析，我们可以看到，SSL并不能阻止别人获得你传输的数据，但是由于你传输的数据都是加密过的，别人拿到了毫无用处，一样可以保护信 息的安全。还有一点需要强调一下，SSL并不依赖于TCP，它可以建立在任何可靠的传输层协议 (比如TCP) 之上。也就是说SSL是不能建立在UDP之上 的。这是显然的，如果传输都不可靠，偶尔丢两个包或者包的顺序换一换的话，怎么保证安全呢？
SASL是提供一种用户身份认证机制, 你可以简单认为是用来认证用户的账号/密码是否运行进入系统或者使用系统的服务. 一般较长使用digest-md5, 该种机制下, 密码可以不用在网络上传输, 也就不用怕密码被窃听.

---

http://blog.csdn.net/id19870510/article/details/8232509

http://just4coding.com/2014/11/06/sasl/

### 关于 sasl

sasl(Simple Authentication and Security Layer)是一个用于网络通信协议的安全验证框架，它可以使网络协议在互相验证的阶段可以有多种验证方式可以选择。

现在实现sasl的协议主要有 imap, smtp, pop, xmpp, subersion,….。举个smtp的例子说明一下sasl的验证流程:

250-mail.example.com Hello pc.example.org [192.168.1.42], pleased to meet you
250-AUTH DIGEST-MD5 CRAM-MD5 LOGIN PLAIN
AUTH LOGIN 
334 VXNlcm5hbWU6
eHh4eAo=
334 UGFzc3dvcmQ6
b294eAo=
235 2.0.0 OK Authenticated
1 和smtp sever建立连接后,server发送欢迎信息
2 server发送自己支持的验证方式DIGEST-MD5 CRAM-MD5 LOGIN PLAIN
3 client择使用LOGIN
4 server发送base64后的challenge code,base64解码后为Username:要求client回应一个用户名
5 client回应base64后的用户名
6 server发送base64后的challenge code,base64解码后为Password:要求client回应一个密码
7 client回应base64后的密码
8 server返回验证成功的信息

很简单的流程，服务端给出选择，客户端选一个，然后根据验证方式不同进行验证流程，由于sasl仅仅是个框架，具体怎么实现是由协议决定的，比如xmpp协议的sasl验证流程

#client与server建立链接后发出一个strem头
C:
#server回应一个steam头
S:
#server发送自己支持的验证方式列表
S:
     
       DIGEST-MD5
       PLAIN
     

#client 说它要用DIGEST-MD5做验证
C:

#server 发送challenge code
S:
   cmVhbG09InNvbWVyZWFsbSIsbm9uY2U9Ik9BNk1HOXRFUUdtMmhoIixxb3A9ImF1dGgi
   LGNoYXJzZXQ9dXRmLTgsYWxnb3JpdGhtPW1kNS1zZXNzCg==

#client 回应challenge
C:

   dXNlcm5hbWU9InNvbWVub2RlIixyZWFsbT0ic29tZXJlYWxtIixub25jZT0i
   T0E2TUc5dEVRR20yaGgiLGNub25jZT0iT0E2TUhYaDZWcVRyUmsiLG5jPTAw
   MDAwMDAxLHFvcD1hdXRoLGRpZ2VzdC11cmk9InhtcHAvZXhhbXBsZS5jb20i
   LHJlc3BvbnNlPWQzODhkYWQ5MGQ0YmJkNzYwYTE1MjMyMWYyMTQzYWY3LGNo
   YXJzZXQ9dXRmLTgK
   
#server 回应验证结果
S:

当你实现一个协议的sasl部分时，如果你仅仅打算实现一两种验证方式，那么寥寥代码便可以搞定，但是如果希望提供尽可能多的验证方式，那么使用一些开源类库将是最好的选择。
对于C语言有两个成熟的lib:Cyrus SASL和libgsasl。以gsasl为例:

gsasl屏蔽了具体验证的细节，你要做的仅仅是为验证流程提供必要的信息，比如：用户名，密码，验证域等等
还是以上面的smtp验证为例，假设我们是client端，现在收到的server的mechlist，即验证方式列表，我们使用gsasl实现这次验证(虽然是我虚构的代码，但理论是可行的:))：

Gsasl *ctx = NULL;
char buffer[BUFSIZ] = "";
char *buf;
Gsasl_session *session;
int rc;
char *p;
//使用gsasl之前初始化
if ((rc = gsasl_init (&ctx)) != GSASL_OK)
{
    printf ("Cannot initialize libgsasl (%d): %s",
        rc, gsasl_strerror (rc));
    return;
}

//创建一个使用LOGIN验证方式的客户端session
if ((rc = gsasl_client_start (ctx, "LOGIN", &session)) != GSASL_OK)
{
    printf ("Cannot initialize client (%d): %s\n",
       rc, gsasl_strerror (rc));
    return;
}

//设置用户名和密码
gsasl_property_set (session, GSASL_AUTHID, "username");
gsasl_property_set (session, GSASL_PASSWORD, "password");

//假设socket_fd为我们与server已经建立连接的描述字

//告诉server我们选择使用LOGIN做验证
buf = buffer;
sprintf(buf, "AUTH LOGIN\r\n");
write(socket_fd, buf, strlen(buf));

do
 {
   buf = buffer;
   //从server读取一行，
   readline(buf, sizeof (buf) - 1, socket_fd);
   //334 是多余的 
   buf += 4;
   //将challenge code 交给gsasl处理
   rc = gsasl_step64 (session, buf, &p);

   if (rc == GSASL_NEEDS_MORE || rc == GSASL_OK)
     {
       //将gsasl的处理结果发送给server
       write(socket_fd, p, strlen(p));
       free (p);
     }
 }
while (rc == GSASL_NEEDS_MORE);

if (rc != GSASL_OK)
 {
   printf ("Authentication error (%d): %s\n",
           rc, gsasl_strerror (rc));
   return;
 }

printf("success!");

gsasl_finish (session);
gsasl_done (ctx);
使用gsasl可以让我们用类似上面代码处理所有的验证方式，唯一不同的就在于使用gsasl_property_set设置不同的字段。

除了像上面一样直接设置验证字段,还可以通过回调函数设置,当gsasl需要某一字段时会触发回调函数

int callback (Gsasl * ctx, Gsasl_session * sctx, Gsasl_property prop)
 {
   char buf[BUFSIZ] = "";
   int rc = GSASL_NO_CALLBACK;

   switch (prop)
     {
     case GSASL_AUTHID:
       gsasl_property_set (sctx, GSASL_AUTHID, "username");
       rc = GSASL_OK;
       break;
     // .............. 
     default:
       printf ("Unknown property!  Don't worry.\n");
       break;
     }
 
   return rc;
 }
//.................
gsasl_callback_set (ctx, callback);
好了，不能够再详细了，我的主要目的是分析jabberd2的验证逻辑，关于gsasl的更多请参考:http://www.gnu.org/software/gsasl/manual/gsasl.html

其他参考:http://wiki.jabbercn.org/index.php?title=RFC3920&variant=zh-cn


>https://bluehua.org/2010/12/01/1484.html

### CRAM-MD5
>https://datatracker.ietf.org/doc/html/rfc2195

### gsasl.h
https://www.gnu.org/software/gsasl/doxygen/gsasl_8h_source.html  

```bash
pacman -S libidn11

```