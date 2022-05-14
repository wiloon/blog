---
author: "-"
date: "2021-03-05 14:54:00" 
title: Ant 风格路径表达式， ant style
categories:
  - inbox
tags:
  - reprint
---
## Ant 风格路径表达式， ant style

### ANT通配符有三种: 
    通配符     说明
    ?        匹配任何单字符
    *        匹配0或者任意数量的字符
    **        匹配0或者更多的目录

例子: 
URL路径    说明

    /app/*.x            匹配(Matches)所有在app路径下的.x文件
    /app/p?ttern        匹配(Matches) /app/pattern 和 /app/pXttern,但是不包括/app/pttern
    /**/example            匹配(Matches) /app/example, /app/foo/example, 和 /example
    /app/**/dir/file.*    匹配(Matches) /app/dir/file.jsp, /app/foo/dir/file.html,/app/foo/bar/dir/file.pdf, 和 /app/dir/file.java
    /**/*.jsp            匹配(Matches)任何的.jsp 文件

最长匹配原则(has more characters)
URL请求/app/dir/file.jsp，现在存在两个路径匹配模式/**/*.jsp和/app/dir/*.jsp，那么会根据模式/app/dir/*.jsp来匹配

作者: 芒果粑粑
链接: https://www.jianshu.com/p/189847a7d1c7
来源: 简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。