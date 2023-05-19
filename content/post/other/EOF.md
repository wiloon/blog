---
title: EOF
author: "-"
date: 2014-07-31T08:34:42+00:00
url: eof
categories:
  - Inbox
tags:
  - reprint
---
## EOF

EOF（End of File），是ASCII码中的替换字符（Control-Z，代码26）

EOF不是特殊字符，而是定义在 `<stdio.h>` 中的一个常量，一般等于-1。#define EOF (-1)

以EOF作为文件结束标志的文件，必须是文本文件。在文本文件中，数据都是以字符的ASCII代码值的形式存放。ASCII代码值的范围是0~127，不可能出现-1，因此可以用EOF作为文件结束标志。
————————————————
版权声明：本文为CSDN博主「咕咕怪」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：<https://blog.csdn.net/weixin_38911591/article/details/89605221>

EOF (as defined in the C language) is not a character/not an ASCII value. That's why getc returns an int and not an unsigned char - because the character read could have any value in the range of unsigned char, and the return value of getc also needs to be able to represent the non-character value EOF (which is necessarily negative).

<https://stackoverflow.com/questions/7622699/what-is-the-ascii-value-of-eof-in-c>

## eol

end of line
