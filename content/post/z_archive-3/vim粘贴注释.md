---
title: vim 粘贴注释
author: "-"
date: 2020-04-22T02:07:04+00:00
url: /?p=16040
categories:
  - Editor
tags:
  - reprint
  - VIM
---
## vim 粘贴注释

vim在粘贴代码时会自动缩进，这样会把有注释的代码搞得一团糟，可能因为某行的一个注释造成后面的代码全部被注释掉，以前就是直接粘贴的，发现不得不解决这个自动添加注释的问题。

临时方法:
  
vim 是自带缩进的，我们执行粘贴前需要设置为粘贴模式:

set paste

当我们写代码时需要缩进，进而，在粘贴完了需要改回来:

set no paste

一劳永逸方法:
  
为了避免麻烦，我们可以为vim设置快捷键:
  
在/etc/vim中,修改vimrc,追加代码:

vim /etc/vim/.vimrc

追加代码:

```r
set pastetoggle=<F9>
```

这样你每次粘贴前就按一下F9,完事之后再F9切回来，OK！

vim粘贴注释-解决方法
  
[http://www.chenglin.name/linux/blog-linux/595.html/embed#?secret=QDy4MQGTrl](http://www.chenglin.name/linux/blog-linux/595.html/embed#?secret=QDy4MQGTrl)
