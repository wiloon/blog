---
title: tmux
author: "-"
date: 2016-12-02T07:15:23+00:00
url: /?p=9444
categories:
  - Inbox
tags:
  - reprint
---
## tmux
### ~/.tmux.conf

    set -g mouse on
    set-window-option -g mode-keys vi #可以设置为vi或emacs
    set-window-option -g utf8 on #开启窗口的UTF-8支持

Tmux 是一个终端复用器 (terminal multiplexer) 

窗格快捷键
下面是一些窗格操作的快捷键。

    Ctrl+b %: 划分左右两个窗格。
    Ctrl+b ": 划分上下两个窗格。
    Ctrl+b : 光标切换到其他窗格。是指向要切换到的窗格的方向键,比如切换到下方窗格,就按方向键↓。
    Ctrl+b ;: 光标切换到上一个窗格。
    Ctrl+b o: 光标切换到下一个窗格。
    Ctrl+b {: 当前窗格与上一个窗格交换位置。
    Ctrl+b }: 当前窗格与下一个窗格交换位置。
    Ctrl+b Ctrl+o: 所有窗格向前移动一个位置,第一个窗格变成最后一个窗格。
    Ctrl+b Alt+o: 所有窗格向后移动一个位置,最后一个窗格变成第一个窗格。
    Ctrl+b x: 关闭当前窗格。
    Ctrl+b !: 将当前窗格拆分为一个独立窗口。
    Ctrl+b z: 当前窗格全屏显示,再使用一次会变回原来大小。
    Ctrl+b Ctrl+: 按箭头方向调整窗格大小。
    Ctrl+b q: 显示窗格编号。


https://www.ruanyifeng.com/blog/2019/10/tmux.html

```bash
sudo pacman -S tmux
```

$    重命名当前Session

c    创建新窗口 (Window) 

%    水平分割窗口 (形成两个Pane) 

"    垂直分割窗口

d    退出当前Session

tmux ls    查看当前的tmux服务中有哪些Session

### Tmux 启用鼠标滚动
在Ubuntu上使用Tmux是一件非常舒服的事,但有时使用鼠标滚轮时,和平时使用终端的习惯不怎么一致,因此可以设置启用鼠标滚轮。
具体方式: 
按完前缀ctrl+B后,再按冒号: 进入命令行模式,
输入以下命令: 

set -g mouse on
https://blog.csdn.net/ddydavie/article/details/79031564


### tmux
tmux的复制粘贴
tmux有面板的概念,这导致普通终端下的ctrl+shift+C的模式复制出来的文本会串行。如果面板只有一列当然没有问题,但当面板有多列时,复制就会出问题。于是tmux提出了类似vim的复制模式。因此,tmux下有两套复制方法。
按下shift的同时,使用ctrl+shift+c、ctrl+shift+v可以用以前的方式进行复制粘贴。这种方式的好处就是可以复制到操作系统的粘贴板中。
下面重点介绍tmux在vim模式下的复制粘贴。

~/.tmux.conf

set-window-option -g mode-keys vi #可以设置为vi或emacs
set-window-option -g utf8 on #开启窗口的UTF-8支持
tmux复制模式下可用的命令: 

Function                 vi             emacs
Back to indentation      ^              M-m
Clear selection          Escape         C-g
Copy selection           Enter          M-w
Cursor down              j              Down
Cursor left              h              Left
Cursor right             l              Right
Cursor to bottom line    L
Cursor to middle line    M              M-r
Cursor to top line       H              M-R
Cursor up                k              Up
Delete entire line       d              C-u
Delete to end of line    D              C-k
End of line              $              C-e
Goto line                :              g
Half page down           C-d            M-Down
Half page up             C-u            M-Up
Next page                C-f            Page down
Next word                w              M-f
Paste buffer             p              C-y
Previous page            C-b            Page up
Previous word            b              M-b
Quit mode                q              Escape
Scroll down              C-Down or J    C-Down
Scroll up                C-Up or K      C-Up
Search again             n              n
Search backward          ?              C-r
Search forward           /              C-s
Start of line            0              C-a
Start selection          Space          C-Space
Transpose chars                         C-t
复制模式步骤: 
1. C-b [ 进入复制模式
2. 参考上表移动鼠标到要复制的区域,移动鼠标时可用vim的搜索功能"/","?"
3. 安空格键开始选择复制区域
4. 选择完成后安enter键退出
5. C-b ] 粘贴



接入会话
tmux attach命令用于重新接入某个已存在的会话。


# 使用会话编号
$ tmux attach -t 0

# 使用会话名称
$ tmux attach -t <session-name>
3.4 杀死会话
tmux kill-session命令用于杀死某个会话。


# 使用会话编号
$ tmux kill-session -t 0

# 使用会话名称
$ tmux kill-session -t <session-name>
3.5 切换会话
tmux switch命令用于切换会话。


# 使用会话编号
$ tmux switch -t 0

# 使用会话名称
$ tmux switch -t <session-name>