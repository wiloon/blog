---
title: MIME
author: "-"
date: 2012-06-03T13:56:13.000+00:00
url: "/?p=3406"
categories:
- Web
tags:
  - reprint
---
## MIME

媒体类型, **用途互联网邮件扩展**

 (**MIME**，**Multipurpose Internet Mail Extensions**)

是一个互联网标准, 它扩展了电子邮件标准，使其能够支持非ASCII字符、二进制格式附件等多种格式的邮件消息。HTTP协议中也使用了MIME的框架。MIME是通过标准化电子邮件报文的头部的附加域 (fields) 而实现的；这些头部的附加域，描述新的报文类型的内容和组织形式。

内容类型 (Content-Type) ，这个头部领域用于指定消息的类型。一般以下面的形式出现。

type有下面的形式。

* Text: 用于标准化地表示的文本信息，文本消息可以是多种字符集和或者多种格式的；
* Multipart: 用于连接消息体的多个部分构成一个消息，这些部分可以是不同类型的数据；
* Application: 用于传输应用程序数据或者二进制数据；
* Message: 用于包装一个E-mail消息；
* Image: 用于传输静态图片数据；
* Audio: 用于传输音频或者音声数据；
* Video: 用于传输动态影像数据，可以是与音频编辑在一起的视频数据格式。

subtype 用于指定 type 的详细形式。

* text/plain (纯文本)
* text/html (HTML文档)
* application/xhtml+xml (XHTML文档)
* image/gif (GIF图像)
* image/jpeg (JPEG图像) 【PHP中为: image/pjpeg】
* image/png (PNG图像) 【PHP中为: image/x-png】
* video/mpeg (MPEG动画)
* application/octet-stream (任意的二进制数据)
* application/pdf (PDF文档)
* application/msword (Microsoft Word文件)
* message/rfc822 (RFC 822形式)
* multipart/alternative (HTML邮件的HTML形式和纯文本形式，相同内容使用不同形式表示)
* application/x-www-form-urlencoded (使用HTTP的POST方法提交的表单)
* multipart/form-data (同上，但主要用于表单提交时伴随文件上传的场合)

parameter可以用来指定附加的信息，更多情况下是用于指定text/plain和text/htm等的文字编码方式的charset参数。MIME根据type制定了默认的subtype，当客户端不能确定消息的subtype的情况下，消息被看作默认的subtype进行处理。Text默认是text/plain，Application默认是application/octet-stream而Multipart默认情况下被看作multipart/mixed。

### 内容传输编码

内容传输编码 (Content-Transfer-Encoding) ，这个区域使指定ASCII以外的字符编码方式成为可能。形式如下:

Content-Transfer-Encoding: [mechanism]

其中，mechanism的值可以指定为"7bit"，"8bit"，"binary"，"quoted-printable"，"base64"。

#### 7bit

7bit这里指的是7位的ASCII编码方式。

#### 8bit

8位元ASCII码。

#### binary

#### quoted-printable

因为欧洲的一些文字和ASCII字符集中的某些字符有部分相同。如果邮件消息使用的是这些语言的话，于ASCII重叠的那些字符可以原样使用，ASCII字符集中不存在的字符采用形如"=??"的方法编码。这里"??"需要用将字符编码后的16进制数字来指定。采用quoted-printable编码的消息，长度不会变得太长，而且大部分都是ASCII中的字符，即使不通过解码也大致可以读懂消息的内容。

### MIME

1. MIME的全称是"Multipurpose Internet Mail Extensions"，中译为"多用途互联网邮件扩展"，指的是一系列的电子邮件技术规范，主要包括RFC 2045、RFC 2046、RFC 2047、RFC 4288、RFC 4289和RFC 2077。

顾名思义，MIME是对传统电子邮件的一个扩展，现在已经成为电子邮件实际上的标准。

2. 传统的电子邮件是1982年定下技术规范的，文件是RFC 822。

它的一个重要特点，就是规定电子邮件只能使用ASCII字符。这导致了三个结果: 1) 非英语字符都不能在电子邮件中使用；2) 电子邮件中不能插入二进制文件 (如图片) ；3) 电子邮件不能有附件。

这实际上无法接受的，因此到了1992年，工程师们决定扩展电子邮件的技术规范，提出一系列补充规范，这就是MIME的由来。

3. 下面是一封传统的电子邮件。

From: "Tommy Lee" <lee@example.com>
To: "Jack Zhang" <zhang@example.com>
Subject: Test
Date: Wed, 17 May 2000 19:08:29 -0400
Message-ID: <NDBBIAKOPKHFGPLCODIGIEKBCHAA.lee@example.com>

Hello World.

从上面可以看出，这封信的发信人地址是lee@example.com，收信人地址是zhang@example.com，邮件主题是Test，发送时间是2000年5月17日，邮件内容是"Hello World."。

在结构上，这封信分为三个部分: 首先是信件头，然后是一个空行，最后是信件内容。收信人的客户端软件只会显示最后一部分，要查看全信，必须使用"查看原始邮件"功能。

4. MIME对传统电子邮件的扩展，表现在它在信件头部分添加了几条语句，主要有三条。

第一条是:

MIME-Version: 1.0

这条语句是必须的，而且1.0这个版本值是不变的，即使MIME本身已经升级了好几次。

有了这条语句，收信端就知道这封信使用了MIME规范。

5. 第二条语句是:

Content-Type: text/plain; charset="ISO-8859-1"

这一行是极端重要的，它表明传递的信息类型和采用的编码。

Content-Type 表明信息类型，缺省值为" text/plain"。它包含了主要类型 (primary type) 和次要类型 (subtype) 两个部分，两者之间用"/"分割。主要类型有9种，分别是application、audio、example、image、message、model、multipart、text、video。

每一种主要类型下面又有许多种次要类型，常见的有:

text/plain: 纯文本，文件扩展名.txt
text/html: HTML文本，文件扩展名.htm和.html
image/jpeg: jpeg格式的图片，文件扩展名.jpg
image/gif: GIF格式的图片，文件扩展名.gif
audio/x-wave: WAVE格式的音频，文件扩展名.wav
audio/mpeg: MP3格式的音频，文件扩展名.mp3
video/mpeg: MPEG格式的视频，文件扩展名.mpg
application/zip: PK-ZIP格式的压缩文件，文件扩展名.zip

详细的Content-Type列表，可以查看这里和这里。

如果信息的主要类型是"text"，那么还必须指明编码类型"charset"，缺省值是ASCII，其他可能值有"ISO-8859-1"、"UTF-8"、"GB2312"等等。

整个Content-Type这一行，不仅使用在电子邮件，后来也被移植到了HTTP协议中，所以现在只要是在网上传播的HTTP信息，都带有Content-Type头，以表明信息类型。

6.

前面已经说过，电子邮件的传统格式不支持非ASCII编码和二进制数据。因此MIME规定了第三条语句:

Content-transfer-encoding: base64

这条语句指明了编码转换的方式。Content-transfer-encoding的值有5种----"7bit"、"8bit"、"binary"、"quoted-printable"和"base64"----其中"7bit"是缺省值，即不用转化的ASCII字符。真正常用是"quoted-printable"和"base64"两种，它们的详细用法，我在明天的笔记中会详细介绍。

7.

下面是一封我收到的邮件的源码:

Date: Wed, 18 Jun 2008 18:07:51 +0800 (CST)
From: xxx <xxx@163.com>
To: yifeng.ruan@gmail.com
Message-ID: <14410503.1073611213783671983.JavaMail.coremail@bj163app54.163.com>
Subject: =?gbk?B?xOO6ww==?=
MIME-Version: 1.0
Content-Type: multipart/alternative;
boundary=&quot;----=_Part_287491_22998031.1213783671982&quot;

------=_Part_287491_22998031.1213783671982
Content-Type: text/plain; charset=gbk
Content-Transfer-Encoding: base64

IAq4+b7dsr+209PQudi55raoo6yyu7XD1Nq12Le9yM66zs341b7Jz7nSz+DTprXEtqvO96Osx+vE
49TaxOO1xLKpv83W0AogIArW0Ln6yr2x6tPvIC0gyO7Su7fltcTN+MLnyNXWvgoKtcS12jEy1cXN
vMasyb6z/aOst/HU8s7Sw8fXt76/xOO1xM/gudjU8MjOoaPQu9C7us/X96OhtMvNvMas1Nq4vbz+
wO/D5g==
------=_Part_287491_22998031.1213783671982
Content-Type: text/html; charset=gbk
Content-Transfer-Encoding: quoted-printable

&amp;nbsp;</DIV>
=B8=F9=BE=DD=B2=BF=B6=D3=D3=D0=B9=D8=B9=E6=B6=A8=A3=AC=B2=BB=B5=C3=D4=
=DA=B5=D8=B7=BD=C8=CE=BA=CE=CD=F8=D5=BE=C9=CF=B9=D2=CF=E0=D3=A6=B5=C4=B6=AB=
=CE=F7=A3=AC=C7=EB=C4=E3=D4=DA=C4=E3=B5=C4=B2=A9=BF=CD=D6=D0</DIV>
&amp;nbsp;
......

可以看到这封信的MIME语句是:

MIME-Version: 1.0
Content-Type: multipart/alternative;
boundary="----=_Part_287491_22998031.1213783671982"

"Content-Type: multipart/alternative;"表明这封信的内容，是纯文本和HTML文本的混合。另两个可能的值是multipart/mixed和multipart/related，分别表示"信件内容中有二进制内容"和"信件带有附件"。

"boundary="----=_Part_287491_22998031.1213783671982"
"表明不同信件内容的分割线是"----=_Part_287491_22998031.1213783671982"，它通常是一个很长的随机字符串。

信件内容部分又有两个子信件头:

Content-Type: text/plain; charset=gbk
Content-Transfer-Encoding: base64

和

Content-Type: text/html; charset=gbk
Content-Transfer-Encoding: quoted-printable

它们表明，第一个部分是gbk编码的纯文本，编码转换格式是base64。第二个部分是gbk编码的HTML文本，编码转化格式是quoted-printable。

[延伸阅读]

1. wikipedia的MIME条目

2. MIME FAQ

3. MIME邮件面面观

---

[http://www.ruanyifeng.com/blog/2008/06/mime.html](http://www.ruanyifeng.com/blog/2008/06/mime.html)
