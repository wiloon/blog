---
title: xml 编码
author: "-"
date: 2012-06-10T05:08:51+00:00
url: /?p=3481
categories:
  - Development

tags:
  - reprint
---
## xml 编码
前同天和同事在讨论xml里的encoding属性和文件格式的关系，终于彻底的弄清楚了。

以前理解的是,xml里的encoding里定义必须与文件格式相匹配。即有这样的xml Introduction<? xml encoding="utf-8" .. ?>，那么，文件格式必须是一个utf-8文件，即文件的前两个字节要是一个utf-8头FF FE。 (后来才弄清楚，FF FE不是utf-8的BOM。。就是说我的错误理解持续了相当长一段时间。。) 

下面把讨论的几个阶段大概说一下。

刚开始讨论时，我很肯定的告诉他，encoding的值必须和文件格式 (即BOM，BOM就是 byte order mark的缩写) 相匹配，不然在解析XML时，可能会出现 (比如文档含有某个UNICODE字符，而encoding或BOM指定的格式不匹配，就会出错，当时我是这样的意思) ，然后他又告诉我，好像不是这样，我用DELPHI创建的XML文件，没有BOM，XML里面有中文内容，encoding里指定的是UTF-8，用IE可以正常打开啊。

他在发现他所创建的XML文件没有BOM时，有个有趣的地方，就是用UE打开这类含有UNICODE字符的文件时，UE会自动在文件前面加上FF FE，使得文件可以正常显示，所以原本没有BOM的文件，在UE下的十六进制下浏览，会看到多了个BOM，这个功能可以在UE的OPTIONS里去掉的，想知道的可以自己去找找。

然后我有点大头了，怎么会这样呢，然后想啊想，突然他发了一条信息过来，内容如下: 


W3C定义了三条XML解析器如何正确读取XML文件的编码的规则: 

1，如果文挡有BOM(字节顺序标记，一般来说，如果保存为unicode格式，则包含BOM，ANSI则无)，就定义了文件编码

2，如果没有BOM，就查看XML声明的编码属性

3，如果上述两个都没有，就假定XML文挡采用UTF-8编码


有了这三条规则，那这个规则就清楚多了。

首先，XML解析器根据文件的BOM来解析文件；如果没找到BOM，由用XML里的encoding属性指定的编码；如果xml里encoding没指定的话，就默认用utf-8来解析文档。然后又可以推出，BOM和ENCODING都有的话，则以BOM指定的为准。

啊！突然觉得有标准文档多好！虽然是那么的理所当然。

至此，终于把xml里的encoding和文件格式的关系弄懂了。虽然这篇记录只有那几百个字内容，但是我们当时在讨论的时候，总时间差不多花了2个小时。

<http://blog.csdn.net/fzy112001/article/details/4183139>

<http://www.cnblogs.com/azol/articles/1137035.html>