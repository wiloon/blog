---
title: zsh, oh-my-zsh
author: wiloon
type: post
date: 2017-04-06T04:56:02+00:00
url: /?p=10025
categories:
  - Uncategorized

---
### 不能自动补全

```bash
rm ~/.zcompdump*
```

https://unix.stackexchange.com/questions/210930/completions-stopped-working-after-upgrading-zsh/210931#210931

### 自动补全提示插件

https://www.jianshu.com/p/aea390c1c8ef

```bash
git clone git://github.com/zsh-users/zsh-autosuggestions $ZSH_CUSTOM/plugins/zsh-autosuggestions
vim .zshrc
plugins=(git zsh-autosuggestions)
```

```bash
sudo pacman -S git zsh

chsh -l
chsh -s /bin/zsh

#install oh-my-zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```

oh-my-zsh 是一个著名的，社区驱动的框架，它拥有很多有用的函数，helpers，插件，主题，可以用来简化复杂的 Zsh 配置。
  
config zsh history size

edit .zshrc and add following lines
  
#set history size
  
export HISTSIZE=10000
  
#save history after logout
  
export SAVEHIST=10000

### theme, random 模式使用theme列表

使用random模式时经常会随机到系统不支持的主题， 使用ZSH\_THEME\_RANDOM_CANDIDATES 配置， 可以把随机主题控制在一定范围内。

```bash
zSH_THEME_RANDOM_CANDIDATES=(
  "robbyrussell"
  "agnoster"
)

```

https://github.com/robbyrussell/oh-my-zsh
  
https://wiki.archlinux.org/index.php/Zsh_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)#.E5.AE.89.E8.A3.85[