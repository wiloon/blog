---
title: locale command
author: "-"
date: 2016-11-17T10:27:38+00:00
url: locale
categories:
  - Inbox
tags:
  - reprint
---
## locale command

```bash
sudo vim /etc/locale.conf
```

locale 是 Linux 系统中多语言环境的设置接口，在 Linux 中，使用 locale 命令来设置和显示程序运行的语言环境，locale 会根据计算机用户所使用的语言，所在国家或者地区，以及当地的文化传统定义一个软件运行时的语言环境。

通过 locale 来设置程序运行的不同语言环境，locale 由 ANSI C 提供支持。locale 的命名规则为<语言>_<地区>.<字符集编码>，如 zh_CN.UTF-8，zh 代表中文，CN 代表大陆地区，UTF-8 表示字符集。在locale环境中，有一组变量，代表国际化环境中的不同设置。

locale 设置规则
<语言>_<地区>.<字符集编码><@修正值>

zh_CN.utf8

zh：表示中文
CN：表示大陆地区
Utf8：表示字符集

de_DE.utf-8@euro

de：表示德语
DE：表示德国
Utf-8：表示字符集
euro：表示按照欧洲习惯加以修正
使用详解
设置locale的根本就是设置一组总共12个LC开头的变量，不包括LANG和LC_ALL
locale默认文件存放位置： /usr/share/i18n/locales

（一）查看当前 locale 设置
列出所有启用的 locale：

```bash
locale
```

LANG=zh_CN.UTF-8
LC_CTYPE="zh_CN.UTF-8"
LC_NUMERIC="zh_CN.UTF-8"
LC_TIME="zh_CN.UTF-8"
LC_COLLATE="zh_CN.UTF-8"
LC_MONETARY="zh_CN.UTF-8"
LC_MESSAGES="zh_CN.UTF-8"
LC_PAPER="zh_CN.UTF-8"
LC_NAME="zh_CN.UTF-8"
LC_ADDRESS="zh_CN.UTF-8"
LC_TELEPHONE="zh_CN.UTF-8"
LC_MEASUREMENT="zh_CN.UTF-8"
LC_IDENTIFICATION="zh_CN.UTF-8"
LC_ALL=
分别介绍下：

LANG：LANG 的优先级是最低的，它是所有 LC_* 变量的默认值，下方所有以 LC_ 开头变量（LC_ALL除外）中，如果存在没有设置变量值的变量，那么系统将会使用 LANG 的变量值来给这个变量进行赋值。如果变量有值，则保持不变

LC_CTYPE：用于字符分类和字符串处理，控制所有字符的处理方式，包括字符编码，字符是单字节还是多字节，如何打印等，非常重要的一个变量。

LC_NUMERIC：用于格式化非货币的数字显示

LC_TIME：用于格式化时间和日期

- LC_COLLATE: 用于比较和排序

LC_MONETARY：用于格式化货币单位

LC_MESSAGES：用于控制程序输出时所使用的语言，主要是提示信息，错误信息，状态信息，标题，标签，按钮和菜单等

LC_PAPER：默认纸张尺寸大小

LC_NAME：姓名书写方式

LC_ADDRESS：地址书写方式

LC_TELEPHONE：电话号码书写方式

LC_MEASUREMENT：度量衡表达方式

LC_IDENTIFICATION：locale对自身包含信息的概述

LC_ALL：它不是环境变量，它是一个宏，它可通过该变量的设置覆盖所有LC_*变量，这个变量设置之后，可以废除LC_*的设置值，使得这些变量的设置值与LC_ALL的值一致，注意LANG变量不受影响。

优先级：LC_ALL > LC_* > LANG

（二）查看当前系统所有可用 locale
[root@htlwk0001host ~]# locale -a
C
C.utf8
en_AG
en_AU
en_AU.utf8
en_BW
en_BW.utf8
en_CA
en_CA.utf8
en_DK
en_DK.utf8
en_GB
en_GB.iso885915
en_GB.utf8
en_HK
en_HK.utf8
en_IE
en_IE@euro
en_IE.utf8
en_IL
en_IN
en_NG
en_NZ
en_NZ.utf8
en_PH
en_PH.utf8
en_SC.utf8
en_SG
en_SG.utf8
en_US
en_US.iso885915
en_US.utf8
en_ZA
en_ZA.utf8
en_ZM
en_ZW
en_ZW.utf8
POSIX
zh_CN
zh_CN.gb18030
zh_CN.gbk
zh_CN.utf8
zh_HK
zh_HK.utf8
zh_SG
zh_SG.gbk
zh_SG.utf8
zh_TW
zh_TW.euctw
zh_TW.utf8

（三）设置系统的 locale
可以修改/etc/profile文件
修改/etc/profile文件，在最下面增加
export LC_ALL=zh_CN.utf8
export LANG=zh_CN.utf8
命令行中使用命令 source 下配置文件，使其生效

修改/etc/locale.gen文件
将注释打开即可，修改完成后，执行下 locale-gen 命令使其生效

# en_SG ISO-8859-1
en_US.UTF-8 UTF-8
# en_US ISO-8859-1
命令行模式
localectl set-locale LANG=en_US.UTF-8
修改/etc/default/locale
注销一下，使其生效
LANG=“en_US.UTF-8”
LANGUAGE=“en_US:en”
创建/etc/locale.conf文件
LANG=en_AU.UTF-8
LC_COLLATE=C
LC_TIME=en_DK.UTF-8
source 使其生效
————————————————
版权声明：本文为CSDN博主「liaowenxiong」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：[https://blog.csdn.net/liaowenxiong/article/details/116401524](https://blog.csdn.net/liaowenxiong/article/details/116401524)

## C.UTF-8 and en_US.UTF-8 locales?

[https://stackoverflow.com/questions/55673886/what-is-the-difference-between-c-utf-8-and-en-us-utf-8-locales](https://stackoverflow.com/questions/55673886/what-is-the-difference-between-c-utf-8-and-en-us-utf-8-locales)
