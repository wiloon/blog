---
title: powermock
author: wiloon
type: post
date: 2015-08-12T08:40:14+00:00
url: /?p=8100
categories:
  - Uncategorized

---
<pre></pre>

[PowerMock LinkageError: MockClassLoader javax/management/MBeanServer][1]{.question-hyperlink}

http://stackoverflow.com/questions/20400574/powermock-linkageerror-mockclassloader-javax-management-mbeanserver

&nbsp;

@RunWith(PowerMockRunner.class)
  
@PowerMockIgnore({&#8220;javax.management.*&#8221;})
  
@PrepareForTest(ClassName.class)

&nbsp;

&nbsp;

http://blog.csdn.net/jackiehff/article/details/14000779

 [1]: http://stackoverflow.com/questions/20400574/powermock-linkageerror-mockclassloader-javax-management-mbeanserver