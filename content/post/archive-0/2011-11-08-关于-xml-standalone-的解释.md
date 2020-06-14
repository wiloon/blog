---
title: 关于 XML standalone 的解释
author: wiloon
type: post
date: 2011-11-08T05:44:54+00:00
url: /?p=1462
bot_views:
  - 28
categories:
  - Uncategorized

---
<div>
  <a href="http://www.blogjava.net/javafuns/articles/257525.html">http://www.blogjava.net/javafuns/articles/257525.html</a>
</div>

XML standalone 定义了外部定义的 DTD 文件的存在性. standalone element 有效值是 yes 和 no. 如下是一个例子:

<div>
  <?xml version=&#8221;1.0" encoding=&#8221;UTF-8" standalone=&#8221;no&#8221;?><br /> <!DOCTYPE s1 PUBLIC "http://www.ibm.com/example.dtd&#8221; "example.dtd&#8221;><br /> <s1>&#8230;&#8230;&#8230;</s1>
</div>

值 no 表示这个 XML 文档不是独立的而是依赖于外部所定义的一个 DTD.  值 yes 表示这个 XML 文档是自包含的(self-contained).