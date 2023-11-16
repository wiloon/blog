---
title: "字体 , 编程字体, 等宽字体"
author: "-"
date: ""
url: ""
categories:
  - Font
tags:
  - inbox
---
## "字体 , 编程字体, 等宽字体"

### ubunti install 微软雅黑

```bash
sudo apt-get install ttf-mscorefonts-installer
# 更新字体缓存
sudo fc-cache -f -v
```

### 编程字体, 等宽字体

对于程序员来说,好的字体应该满足的基本条件:

字母和数字易于分辨,如: 英文字母 o 和 阿拉伯数字 0, 或者 英文字母 l 和 阿拉伯数字 1 ,两个单引号 '' 和双引号 ".
字体等宽,保持对齐,美观漂亮
免费开源
Source Code Pro 是 Adobe 公司号称最佳的编程字体。而且还是开源的。
它非常适合用于阅读代码,支持 Linux、Mac OS X 和 Windows 等操作系统,而且无论商业或个人都可以免费使用。

作者: jingr1
链接: [https://www.jianshu.com/p/1d5e1aaeb3f6](https://www.jianshu.com/p/1d5e1aaeb3f6)
来源: 简书
著作权归作者所有。商业转载请联系作者获得授权,非商业转载请注明出处。

[https://www.archlinux.org/packages/extra/any/adobe-source-code-pro-fonts/](https://www.archlinux.org/packages/extra/any/adobe-source-code-pro-fonts/)

### jetbrain字体

JetBrain Mono

```bash
    yay -S ttf-jetbrains-mono
```

### FiraCode

[https://github.com/tonsky/FiraCode](https://github.com/tonsky/FiraCode)

### 等宽字体

status { /*width: auto;*/

background: #ffff99;

/*-webkit-border-radius: 6px;*/

padding: 1px 3px 1px 3px;

display: none;

font-family: "Courier", "Arial", "Verdana", "sans-serif";
  
}
