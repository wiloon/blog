---
title: zsh, oh-my-zsh, oh my zsh
author: "-"
date: 2017-04-06T04:56:02+00:00
url: zsh
categories:
  - Linux
tags:
  - reprint
  - remix
---
## zsh, oh-my-zsh, oh my zsh

```Bash
# 查看已经安装的 shell 列表
cat /etc/shells

## 查看当前 shell
echo $SHELL

# archlinux install zsh
sudo pacman -S git zsh

# ubuntu install zsh
sudo apt install zsh
```

## install oh my zsh

```Bash
# install oh-my-zsh, will set default shell to zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
# after oh my zsh installed, ubuntu user should logout and login.
```

## update oh my zsh

```Bash
# need vpn to access github
omz update
```

## 查看 zsh 版本

```bash
zsh --version
```

### 不能自动补全

```bash
rm ~/.zcompdump*
```

[https://unix.stackexchange.com/questions/210930/completions-stopped-working-after-upgrading-zsh/210931#210931](https://unix.stackexchange.com/questions/210930/completions-stopped-working-after-upgrading-zsh/210931#210931)

### 自动补全提示插件

[https://www.jianshu.com/p/aea390c1c8ef](https://www.jianshu.com/p/aea390c1c8ef)

https://github.com/zsh-users/zsh-autosuggestions

```bash
# archlinux 
sudo pacman -S zsh-autosuggestions

# install from source
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
vim .zshrc
plugins=(git zsh-autosuggestions)
```

https://ohmyz.sh/

## switch to zsh

```bash
## 查看当前 shell
chsh -l
chsh -s /bin/zsh
```

oh-my-zsh 是一个著名的,社区驱动的框架,它拥有很多有用的函数,helpers,插件,主题,可以用来简化复杂的 Zsh 配置。
  
config zsh history size

edit .zshrc and add following lines
  
## set history size
  
export HISTSIZE=10000
  
## save history after logout
  
export SAVEHIST=10000

## random theme

ZSH_THEME="random"

### theme, random 模式使用 theme 列表

使用 random 模式时经常会随机到系统不支持的主题, 使用 ZSH_THEME_RANDOM_CANDIDATES 配置, 可以把随机主题控制在一定范围内。

打开 zsh 配置文件 ~/.zshrc, 查找关键字 zSH_THEME_RANDOM_CANDIDATES, 解除注释

```bash
ZSH_THEME_RANDOM_CANDIDATES=(
  "robbyrussell"
  "agnoster"
)
```

### .zshenv

.zshenv 总是被读取,所以通常把$PATH, $EDITOR等变量写在这里,这样无论是在shell交互,或者运行程序都会读取此文件
Since .zshenv is always sourced, it often contains exported variables that should be available to other programs. For example, $PATH, $EDITOR, and $PAGER are often set in .zshenv. Also, you can set $ZDOTDIR in .zshenv to specify an alternative location for the rest of your zsh configuration.

### .zprofile

.zprofile是给ksh用户的一个.zlogin的替代品,所以我们如果使用了.zlogin就不必再关心此文件
.zprofile is basically the same as .zlogin except that it's sourced before .zshrc while .zlogin is sourced after .zshrc. According to the zsh documentation, ".zprofile is meant as an alternative to .zlogin for ksh fans; the two are not intended to be used together, although this could certainly be done if desired."

### .zshrc

.zshrc主要用在交互shell,所以主要是为shell服务的,比如对shell做的一些个性化设置都可以在这里写入
.zshrc is for interactive shell configuration. You set options for the interactive shell there with the setopt and unsetopt commands. You can also load shell modules, set your history options, change your prompt, set up zle and completion, et cetera. You also set any variables that are only used in the interactive shell (e.g. $LS_COLORS).

### .zlogin

.zlogin在login shell的时候读取,所以比如X系统启动的时候会读取此文件,所以不会再运行中重复读取
.zlogin is sourced on the start of a login shell but after .zshrc if the shell is also interactive. This file is often used to start X using startx. Some systems start X on boot, so this file is not always very useful.

### .zlogout

.zlogout这个就很好理解了, 退出终端的时候读取,用于做一些清理工作,一般我们也用不上
.zlogout is sometimes used to clear and reset the terminal. It is called when exiting, not when opening.

You should go through the configuration files of random Github users to get a better idea of what each file should contain.

#### 顺序

.zshenv → [.zprofile if login] → [.zshrc if interactive] → [.zlogin if login] → [.zlogout sometimes].

### .zshenv, .zprofile

[https://unix.stackexchange.com/questions/71253/what-should-shouldnt-go-in-zshenv-zshrc-zlogin-zprofile-zlogout](https://unix.stackexchange.com/questions/71253/what-should-shouldnt-go-in-zshenv-zshrc-zlogin-zprofile-zlogout)

[https://github.com/robbyrussell/oh-my-zsh](https://github.com/robbyrussell/oh-my-zsh)
  
[https://wiki.archlinux.org/index.php/Zsh_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)#.E5.AE.89.E8.A3.85](https://wiki.archlinux.org/index.php/Zsh_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)#.E5.AE.89.E8.A3.85)

[http://blog.xsudo.com/2019/04/12/1445/](http://blog.xsudo.com/2019/04/12/1445/)  

[https://zhuanlan.zhihu.com/p/19556676](https://zhuanlan.zhihu.com/p/19556676)  

## 修改提示词

https://blog.csdn.net/zxc3590235/article/details/109954843

oh my zsh 默认使用 robbyrussell, 路径 .oh-my-zsh/themes/robbyrussell.zsh-theme

```Bash
# 默认的
PROMPT="%(?:%{$fg_bold[green]%}%1{➜%} :%{$fg_bold[red]%}%1{➜%} ) %{$fg[cyan]%}%c%{$reset_color%}"
# 在前面加个 %M 
PROMPT="%M %(?:%{$fg_bold[green]%}%1{➜%} :%{$fg_bold[red]%}%1{➜%} ) %{$fg[cyan]%}%c%{$reset_color%}"
# 退出重新登录, 提示符前面多了个主机名
```

%T	系统时间（时：分）
%*	系统时间（时：分：秒）
%D	系统日期（年-月-日）
%n	用户名称（即：当前登陆终端的用户的名称，和whami命令输出相同）
%B - %b	开始到结束使用粗体打印
%U - %u	开始到结束使用下划线打印
%d	你当前的工作目录
%~	你目前的目录相对于～的相对路径
%M	计算机的主机名
%m	计算机的主机名（在第一个句号之前截断）
%l	你当前的tty
