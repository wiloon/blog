---
title: Linux 密码生成工具
author: "-"
date: 2017-08-30T00:19:52+00:00
url: /?p=11073
categories:
  - Inbox
tags:
  - reprint
---
## Linux 密码生成工具

```bash
  
pwgen -s -y
  
```

[http://blog.csdn.net/u011582658/article/details/38045311](http://blog.csdn.net/u011582658/article/details/38045311)

1.pwgen
  
pwgen生成的密码易于记忆且相当安全。从技术上来说,容易记忆的密码不会比随机生成的密码更加安全。但是,在大多数情况下,pwgen生成的密码已经足够安全,除了网银密码等需要高安全等级的情况外。使用易于记忆的密码的好处就是你不会把这些密码写下来或者存到电脑上的某个地方,这样做,本来就是不安全的。

安装pwgen,在终端窗口输入:

sudo apt-get install pwgen
  
不带任何参数运行pwgen,将会输出满屏幕的密码。你可以从中选择一个作为自己的密码然后清除屏幕。采用这种方式生成密码,即使恰好有人在背后,他也不知道你选择的到底是哪一个。
  
运行pwgen,在终端输入:

pwgen

选好密码之后,在终端输入clear清除终端窗口内容。

如果你确定背后没有人,可以使用"-1"来告知pwgen只产生一个密码。

pwgen -1

如果想生成一个完全随机的密码,使用"-s"参数。

pwgen -1 -s

在密码中使用特殊字符 (感叹号,逗号,引号,加号,减号,冒号等) 可以提高密码的安全等级。使用"-y"参数使生成的密码中至少包括一个特殊字符。

pwgen -1 -s -y

更多有趣的参数:

-0: 密码中不包含数字。
  
-B, -ambiguous:密码中不包含容易混淆的字符,比如说'1'和'l','0'和'o'。
  
-v, -no-vowels:密码不包括元音字母或者可能被误认为是元音字母的数字。这可以防止生成带有攻击性子串的密码。

2.makepasswd
  
makepasswd和pwgen的工作方式类似,但是它生成的密码不容易记忆。所有的密码都是随机生成的,可以看出,makepasswd比pwgen更加注重安全性。
  
安装makepasswd,在终端输入:
  
sudo apt-get install makepasswd
  
生成一个密码,输入:

makepasswd
  
生成五个密码,每个密码最少包含10个字符,输入:

makepasswd -count 5 -minchars 10
  
还可以指定以某个字符串为基础生成随机密码。这在生成PIN方面可能很有用。比如说,生成4位PIN,输入:

makepasswd -string 1234567890 -chars 4

3.passwordmaker
  
passwordmaker与之前的pwgen和makepasswd不同。它本来是IE,Firefox等浏览器的一个扩展程序。passwordmaker-cli是passwordmaker的命令行版本。安装passwordmaker-cli,输入:

sudo apt-get install passwordmaker-cli
  
在使用passwordmaker的时候,你需要输入一个域名 (URL) 和主密码 (master password) ,passwordmaker会利用这些输入的信息为这个URL生成一个独一无二的密码。

passwordmaker -url maketecheasier.com
  
在提示符之后输入一个安全且容易记忆的密码。我输入的是"FC(QI-Ge"。

passwordmaker的神奇之处在于如果你使用相同的URL和主密码再次运行passwordmaker,将会得到和上次完全一致的结果。这就意味着你可以从此摆脱背诵密码这件苦差。当你忘记密码时,只需要输入相应URL和主密码再次运行passwordmaker即可,而URL和主密码是比较容易记住的。

下面的例子展示了两次运行passwordmaker的结果,注意两次产生的密码是一样的。

记住: 时刻保证你的密码是安全的,不要使用过于明显的密码,比如说: "password","123456","qwerty"等等。如果你对上面提到的例子有任何疑问,在下面的评论栏写下你的问题,我们会尽最大的努力为您答疑解惑。
