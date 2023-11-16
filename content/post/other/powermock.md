---
title: powermock
author: "-"
date: 2015-08-12T08:40:14+00:00
url: /?p=8100
categories:
  - Inbox
tags:
  - reprint
---
## powermock

[PowerMock LinkageError: MockClassLoader javax/management/MBeanServer][1]{.question-hyperlink}

[http://stackoverflow.com/questions/20400574/powermock-linkageerror-mockclassloader-javax-management-mbeanserver](http://stackoverflow.com/questions/20400574/powermock-linkageerror-mockclassloader-javax-management-mbeanserver)

@RunWith(PowerMockRunner.class)
  
@PowerMockIgnore({"javax.management.*"})
  
@PrepareForTest(ClassName.class)

[http://blog.csdn.net/jackiehff/article/details/14000779](http://blog.csdn.net/jackiehff/article/details/14000779)

 [1]: http://stackoverflow.com/questions/20400574/powermock-linkageerror-mockclassloader-javax-management-mbeanserver
