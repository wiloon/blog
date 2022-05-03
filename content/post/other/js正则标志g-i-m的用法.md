---
title: js正则标志/g /i /m的用法
author: "-"
date: 2014-03-10T10:13:48+00:00
url: /?p=6394
categories:
  - JavaScript
tags:
  - regex

---
## js正则标志/g /i /m的用法

正则的思想都是一样的，但是具体的写法会有所不同，在这里提到的/g,/i,/m在其他的地方也许就不能用了。

一，js正则标志/g,/i,/m说明

1，/g 表示该表达式将用来在输入字符串中查找所有可能的匹配，返回的结果可以是多个。如果不加/g最多只会匹配一个

2，/i 表示匹配的时候不区分大小写

3，/m 表示多行匹配，什么是多行匹配呢？就是匹配换行符两端的潜在匹配。影响正则中的^$符号

二，实例说明

1，/g的用法

查看复制打印?

<script type="text/javascript">

str = "tankZHang (231144)"+

"tank ying (155445)";

res = str.match(/tank/); //没有加/g

alert(res); //显示一个tank

res = str.match(/tank/g); //加了/g

alert(res); //显示为tank,tank

</script>

2，/i的用法

查看复制打印?

<script type="text/javascript">

str = "tankZHang (231144)"+

"tank ying (155445)";

res = str.match(/zhang/);

alert(res); //显示为null

res = str.match(/zhang/i); //加了/i

alert(res); //显示为ZHang

</script>

3，/m的用法

查看复制打印?

<script type="text/javascript">

var p = /$/mg;

var s = '1\n2\n3\n4\n5\n6';

alert(p.test(s)); //显示为true

alert(RegExp.rightContext.replace(/\x0A/g, '\\a')); //显示\a2\a3\a4\a5\a6

alert(RegExp.leftContext); //显示为竖的2345

alert(RegExp.rightContext); //显示为6

var p = /$/g;

var s = '1\n2\n3\n4\n5\n6';

alert(p.test(s)); //显示为true

alert(RegExp.rightContext.replace(/\x0A/g, '\\a')); //什么都不显示

alert(RegExp.leftContext); //显示为竖的123456

alert(RegExp.rightContext); //什么都不显示

var p = /^/mg;

var s = '1\n2\n3\n4\n5\n6';

alert(p.test(s)); //显示为true

alert(RegExp.rightContext.replace(/\x0A/g, '\\a')); //显示为1\a2\a3\a4\a5\a6

alert(RegExp.leftContext); //显示为竖的12345

alert(RegExp.rightContext); //显示为6

</script>

//从上例中可以看出/m影响的^$的分割方式

上面说的三个例子，/i,/g,/m分开来说的，可以排列组合使用的。个人觉得/m没有多大用处

<http://blog.51yip.com/jsjquery/1076.html>

### javascript 密码 正则

```
let testPassword = /^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)(?=.*?[!@#$%^&;*()_=+\-])[a-zA-Z\d!@#$%^&;*()_=+\-]*$/; //判断输入格式
            if(testPassword.test(this.passwordText)){
                 ...密码匹配成功
            }else {
             ...密码匹配失败
            }

```

————————————————
版权声明：本文为CSDN博主「weixin_42553179」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：<https://blog.csdn.net/weixin_42553179/article/details/103045970>
