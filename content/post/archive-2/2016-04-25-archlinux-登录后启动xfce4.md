---
title: archlinux 登录后启动xfce4
author: wiloon
type: post
date: 2016-04-25T05:51:34+00:00
url: /?p=8940
categories:
  - Uncategorized

---
https://wiki.archlinux.org/index.php/xinitrc

<pre><code class="language-bash line-numbers">vim  ~/.xinitrc
exec startxfce4

vim .bashrc
# change the last line to
# add as last line in .bashrc
[[ -z $DISPLAY && $XDG_VTNR -eq 1 ]] && exec startx
</code></pre>