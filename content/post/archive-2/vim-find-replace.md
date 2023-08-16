---
title: Vim 查找, 替换
author: "-"
date: 2018-12-19T08:49:53+00:00
url: vim/find/replace
categories:
  - Editor
tags:
  - reprint
  - VIM
---
## Vim 查找

## 查找

在 normal 模式下按下`/`即可进入查找模式(向下查找, `?` 向上查找), 输入要查找的字符串并按下回车。 Vim 会跳转到第一个匹配。按下 `n` 查找下一个, 按下 `N` 查找上一个。

## 大小写敏感 \c, \C

```bash
# 大小写不敏感
/foo\c
# 大小写敏感
/foo\C
```

## 大小写敏感配置

Vim 默认采用大小写敏感的查找, 为了方便我们常常将其配置为大小写不敏感
"设置默认进行大小写不敏感查找
  
set ignorecase
  
"如果有一个大写字母,则切换到大小写敏感查找
  
set smartcase

## vim 正则表达式

Vim 查找支持正则表达式, 例如 /vim$ 匹配行尾的 "vim"。 需要查找特殊字符需要转义,例如 /vim\$ 匹配 "vim$"。

注意查找回车应当用\n,而替换为回车应当用\r (相当于`<CR>`) 。
  
将会查找所有的"foo","FOO","Foo"等字符串。
  
将上述设置粘贴到你的~/.vimrc,重新打开Vim即可生效。

查找当前单词
  
在normal模式下按下*即可查找光标所在单词 (word) , 要求每次出现的前后为空白字符或标点符号。例如当前为foo, 可以匹配foo bar中的foo,但不可匹配foobar中的foo。 这在查找函数名、变量名时非常有用。

按下g*即可查找光标所在单词的字符序列,每次出现前后字符无要求。 即foo bar和foobar中的foo均可被匹配到。

## 使用 very magic 搜索模式查找

可以使用 \v 开关激活 very magic 搜索模式，统一所有特殊符号的规则：

very magic 搜索模式下，除下划线 _、大小写字母以及数字 0 到 9 之外的所有字符都具有特殊含义。
例如，使用 \v 模式开关查找上述匹配十六进制颜色代码的正则表达式可简化为：/\v#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})。

由于出现在起始位置的 \v 开关，位于它后面的所有字符都具有特殊含义，用于转义的反斜杠字符就可以去掉，正则表达式的可读性更强了。

## 使用 very nomagic 搜索模式查找

上面介绍的正则表达式中保留使用的特殊字符，在按模式查找时用起来很方便，但如果想按原义查找对应字符时，又该如何操作呢？

例如，如果想在下面的一段文字中查找 a.k.a，使用Vim命令 /a.k.a. 并不能立马精确地找到目标字符串，因为符号 . 在正则表达式中具有特殊含义，它会匹配任意字符，因此单词 backward 也会被搜索到。

The N key searches backward...
...the \v pattern switch (a.k.a. very magic search)...
当然，可以使用转义的方法消除 . 字符的特殊含义，即 /a\.k\.a\.。

一种更简单的使用方法是使用原义开关 \V 激活Vim的very nomagic 搜索模式。

\V 选项会使得其后的模式中有且只有反斜杠 \ 具有特殊意义，即消除了附加在 .、* 以及 ? 等大多数字符上的特殊含义。
使用 \V 原义开关精确搜索 a.k.a 的命令可以简化为：/\Va.k.a.。

介绍完上面提到的 Vim magic 搜索模式、very magic 搜索模式和 very nomagic 搜索模式后，是不是反而会觉得规则太多，没法快速地选择所需要的模式。

其实，very magic 和 very nomagic 搜索模式分别是Vim对正则表达式特殊字符的两种极端处理方式。

对于Vim的正则表达式搜索，一个通用的原则是：如果想按正则表达式查找，就用模式开关 \v，如果想按原义查找文本，就用原义开关 \V。

## vim 替换

:s (substitute) 命令用来查找和替换字符串。语法如下

```bash
:{作用范围}s/{目标}/{替换}/{替换标志}
```

例如:

```bash
:%s/foo/bar/gc
:%s/foo/bar/g
# 删除空白行
:%g/^$/d
```

### 作用范围

作用范围分为当前行、全文、选区等等。

```bash
# 默认当前行
:s/foo/bar/g

# 全文 `%`
:%s/foo/bar/g
```

选区, 在 Visual 模式下选择区域后输入:, Vim 即可自动补全为: '<,'>。

```r
:'<,'>s/foo/bar/g
```

2-11行:

```r
:5,12s/foo/bar/g
```

当前行.与接下来两行+2:

```r
:.,+2s/foo/bar/g
```

### 删除以 "#" 开头的行

```vim
:%s/^#.*$//g
```

会在全局范围(%)查找foo并替换为bar, 所有出现都会被替换 (g) 。

### 替换标志
  
上文中命令结尾的 `g` 即是替换标志之一, 表示全局 global 替换 (即替换目标的所有出现) 。 还有很多其他有用的替换标志:

空替换标志表示只替换从光标位置开始, 目标的第一次出现:

```r
:%s/foo/bar
```
  
i 表示大小写不敏感查找, I 表示大小写敏感

```r
:%s/foo/bar/i
```

#### 等效于模式中的\c (不敏感) 或\C (敏感)

```r
:%s/foo\c/bar
```
  
c 表示需要确认, 例如全局查找 "foo" 替换为 "bar" 并且需要确认:

```bash
:%s/foo/bar/gc
```
  
回车后 Vim 会将光标移动到每一次"foo"出现的位置, 并提示

```r
replace with bar (y/n/a/q/l/^E/^Y)?
```
  
按下y表示替换, n表示不替换, a表示替换所有, q表示退出查找模式, l表示替换当前位置并退出。^E与^Y是光标移动快捷键,参考:  Vim中如何快速进行光标移动。

高亮设置
  
高亮颜色设置
  
如果你像我一样觉得高亮的颜色不太舒服,可以在 ~/.vimrc 中进行设置:

highlight Search ctermbg=yellow ctermfg=black
  
highlight IncSearch ctermbg=black ctermfg=yellow
  
highlight MatchParen cterm=underline ctermbg=NONE ctermfg=NONE
  
上述配置指定 Search 结果的前景色 (foreground) 为黑色,背景色 (background) 为灰色； 渐进搜索的前景色为黑色,背景色为黄色；光标处的字符加下划线。

更多的CTERM颜色可以查阅: <http://vim.wikia.com/wiki/Xterm256_color_names_for_console_Vim>

禁用/启用高亮
  
有木有觉得每次查找替换后 Vim 仍然高亮着搜索结果？ 可以手动让它停止高亮,在normal模式下输入:

:nohighlight
  
" 等效于
  
:nohl
  
其实上述命令禁用了所有高亮,只禁用搜索高亮的命令是:set nohlsearch。 下次搜索时需要:set hlsearch再次启动搜索高亮。

延时禁用
  
怎么能够让Vim查找/替换后一段时间自动取消高亮,发生查找时自动开启呢？

" 当光标一段时间保持不动了,就禁用高亮
  
autocmd cursorhold * set nohlsearch
  
" 当输入查找命令时,再启用高亮
  
```bash
noremap n :set hlsearch<cr>n
  
noremap N :set hlsearch<cr>N

noremap / :set hlsearch<cr>/
  
noremap ? :set hlsearch<cr>?
  
noremap \* \*:set hlsearch<cr>
```
  
将上述配置粘贴到~/.vimrc,重新打开vim即可生效。

一键禁用
  
如果延时禁用搜索高亮仍然不够舒服,可以设置快捷键来一键禁用/开启搜索高亮:

```bash
noremap n :set hlsearch<cr>n
  
noremap N :set hlsearch<cr>N
  
noremap / :set hlsearch<cr>/
  
noremap ? :set hlsearch<cr>?
  
noremap \* \*:set hlsearch<cr>

nnoremap <c-h> :call DisableHighlight()<cr>
```
  
function! DisableHighlight()

set nohlsearch
  
endfunc
  
希望关闭高亮时只需要按下 Ctrl+H,当发生下次搜索时又会自动启用。

参考阅读
  
XTERM 256色: <http://vim.wikia.com/wiki/Xterm256_color_names_for_console_Vim>
  
Vim Wikia - 查找与替换: <http://vim.wikia.com/wiki/Search_and_replace>
  
用 Vim 打造 IDE 环境: <https://harttle.land/2015/11/04/vim-ide.html>
  
本文采用 知识共享署名 4.0 国际许可协议 (CC-BY 4.0) 进行许可。转载请注明来源:  <https://harttle.land/2016/08/08/vim-search-in-file.html> 欢迎对文中引用进行考证,欢迎指出任何不准确和模糊之处。可以在下面评论区评论,也可以邮件至 <harttle@harttle.com>。

<https://harttle.land/2016/08/08/vim-search-in-file.html>

<https://zhuanlan.zhihu.com/p/55330855>
