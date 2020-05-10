---
title: chrome os, crostini, 开发环境
author: wiloon
type: post
date: 2020-02-17T05:36:02+00:00
url: /?p=15562
categories:
  - Uncategorized

---
  * crostini 的Debian 对snap 支持不全， 不能使用snap 应用

### terminal

https://snugug.com/musings/developing-on-chrome-os/

### terminal, tilix

crostini默认的terminal在使用oh my zsh时，光标显示不正常。
  
安装tilix,从chromeos启动tilix使用terminal

<pre><code class="language-bash line-numbers">sudo pacman -S tilix
# 在chromeos中启动tilix使用shell
</code></pre>

### 或者使用Secure Shell App

### idea 慢的问题

File->Settings->Plugins.
  
Click marketplace, search for &#8220;Choose Runtime&#8221;
  
Install official Choose Runtime addon from JetBrains
  
Wait for install and click to restart IDE.
  
Once back in project, press shift twice to open the search window
  
Search for Runtime. Select &#8220;Choose Runtime&#8221;
  
Change to &#8220;jbrsdk-8u-232-linux-x64-b1638.6.tar.gz&#8221;, which should be the very last one at the bottom of the list.
  
Click install, restart IDE, enjoy!

https://www.reddit.com/r/Crostini/comments/e67tij/pycharmwebstormjetbrains\_ide\_fix/
  
https://github.com/gnunn1/tilix
  
https://www.reddit.com/r/Crostini/comments/8gku8y/psa\_you\_can\_install\_a\_better\_terminal_emulator/