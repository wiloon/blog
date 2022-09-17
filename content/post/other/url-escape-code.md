---
title: url转义字符
author: "-"
date: 2012-07-10T04:26:11+00:00
url: url/escape
categories:
  - web
tags:
  - reprint
---
## url转义字符

## url 转义字符, URL escape codes

对与通过get方式提交的url，浏览器在提交前首先根据http协议把参数及其值解析配对。而url的参数间是通过&分割的，这就是浏览器进行参数配置的分割依据。如果你的参数值中含有&等url特殊字符，那么你在服务器端就会拿到意想不到的值。所以必须对url的特殊字符进行转义。

编码的格式为: %加字符的ASCII码，即一个百分号%，后面跟对应字符的ASCII (16进制) 码值。例如 空格的编码值是"%20"。

### url转义字符, URL特殊符号及编码

```r
                                  十六进制值
+    URL中+号表示空格               %2B
空格 URL中的空格可以用+号或者编码    %20
/    分隔目录和子目录               %2F
?     分隔实际的 URL 和参数         %3F
%     指定特殊字符                  %25
#     表示书签                      %23
&     URL 中指定的参数间的分隔符      %26
:                                   %3A
.     URL 中指定参数的值             %3D
=
: 冒号                              %3A
, 逗号                              %2C
{                                   %7B
```

<http://www.wetools.com/url-escape-code>

<http://alipay.iteye.com/blog/68412>

<http://www.w3schools.com/tags/ref_urlencode.asp>

<https://www.december.com/html/spec/esccodes.html>
