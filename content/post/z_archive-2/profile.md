---
title: linux 环境 变量, /etc/profile, /etc/profile.d/
author: "-"
date: 2016-10-28T04:34:33+00:00
url: /?p=9346
categories:
  - inbox
tags:
  - reprint
---

## linux 环境 变量, /etc/profile, /etc/profile.d/

自定义的环境变量要加到 /etc/profile.d 下, 不建议手动修改 /etc/profile, /etc/profile 文件属于 filesystem 包, 这个包的的更新有可能会导致 /etc/profile 的更新, 
如果 filesystem 升级的时候发现 /etc/profile 被修改过, 会把新的文件安装到 /etc/profile.new 并且是不生效的状态, 有可能会导致某些不兼容的问题, 
比如 perl 包安装的/etc/profile.d/perlbin.sh 使用的 append_path 函数.

### /etc/profile.d/ 目录

在 /etc/profile.d 目录中存放的是一些应用程序所需的启动脚本, 比如 vim 等命令的一些附加设置, 在 /etc/profile.d 目录下添加相关的环境变量设置的 .sh 脚本文件, 
这些脚本文件的环境变量能够被生效, 是因为在 /etc/profile 被读取的时候, 会使用一个 for 循环语句来调用 /etc/profile.d 下的脚本, 
这些脚本文件所设置的环境变量就和 /etc/profile 启动时一起被设置起来了, cat /etc/profile 可以看到有一段加载 /etc/profile.d 目录下所有 .sh 脚本文件的代码:

```bash
if [ -d /etc/profile.d ]; then
  for i in /etc/profile.d/*.sh; do
    if [ -r $i ]; then
      . $i
    fi
  done
  unset i
fi
```

从上面的代码不难理解,/etc/profile.d/ 目录下设置环境变量和 /etc/profile 效果是一样的,都是全局环境变量,一旦生效后也都是永久环境变量； /etc/profile.d/ 比 /etc/profile 好维护,不想要的环境变量从 /etc/profile.d/ 目录中移除即可,创建好的环境变量拷贝文件就轻松的移植到其他的计算机,不用每次去改动 /etc/profile 文件。

根据上面描述可以推理出:

/etc/profile.d 目录下的环境变量是 /etc/profile 启动时一起被读取,那么想要在当前shell终端临时生效可以使用 source /etc/profile,要全局生效则需要注销重登录或者直接重启系统,和 /etc/profile 原理一样；
/etc/profile.d 目录下的环境变量和 /etc/profile 的环境变量优先级,根据环境变量在 /etc/profile 的for循环语句调用 /etc/profile.d 的前面还是后面,在前则被 /etc/profile.d 目录下的环境变量覆盖,在后则被 /etc/profile 的环境变量覆盖
关于/etc/profile.d 目录,我使用我的Ubuntu 14.04.5系统,切换到 /etc/profile.d 目录,再使用 ls 命令列出目录下的所有脚本文件:

```bash
unset key
```

### ~/.bashrc

Archlinux Interactive, non-login shells 会加载 `~/.bashrc`, login shell 不会加载  `~/.bashrc`

win10 WSL + zsh + oh my zsh 用 root 用户  SSH 登录 archlinux 会加载 .bash_profile, 不会加载 .bashrc
win10 putty SSH 登录 同上

### ~/.bash_profile

All interactive shells source `/etc/bash.bashrc` and `~/.bashrc`, while interactive login shells also source /etc/profile and `~/.bash_profile`

不知道你有没有遇到过这样的场景,当你需要设置一个环境变量,或者运行一个程序设置你的shell或桌面环境,但是不知道在哪里是最方便设置的位置。

有一些常见的情况,例如从Debian的包管理程序到Iaas的管理中,很多任务需要设置环境变量才能正常运行。

有时, 程序通常只需要在首次登陆时运行一次,例如 xrandr 命令。

此外,有的程序偶尔会被注入到shell中,例如rbenv,rvn或 SitePoint's自己的 envswith 程序。

让我们来看看在Debian GNU/Linux Jessie安装中出现的一些常见选项,并尝试理解这一切。

/etc/profile
  
默认情况下,Debian提供/etc/profile文件,这个文件用来设置$PATH变量 ($PATH通常用来声明命令的搜索路径) ,可以立即生效。下面的代码是/etc/profile的一部分。

```Bash
if [ "`id -u`" -eq 0 ]; then
  
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
  
else
  
PATH="/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games"
  
fi
  
export PATH
```
  
为了方便,root用户 (ID为0) 和其他任何用户的路径都不同。这是因为系统二进制目录 (sbin目录) 位置传统上是作为系统管理程序、或必须以root身份运行的程序存放的保留位置。而games路径对于root用户来说是省略的,因为不到非必要的时候,绝不可能使用root用户来运行游戏程序。

接下来,/etc/profile处理$PS1变量的设置,$PS1变量是用来设置主提示字符串 (即用户登陆时显示的字符) 。除了系统的shell是Bash以外,系统$PS1变量默认设置的是$ (root用户默认是#)。如果系统的shell使用的是Bash,则/etc/bash.bashrc 文件会替代$PS变量来处理主提示字符串 (特殊情况除外) 。后面我们会简短地说一下/etc/bash.bashrc。

所以从这一点上,我们可以推断 /etc/profile 在登陆期间 (例如使用login命令) 会被所有的 shell 读取。/etc/profile 调用 id 命令来读取用户ID, 而不是使用更高效的 Bash 内置变量 ${UID}。 Bash 使用特定来源的配置,而不是定义一个花哨的 shell 提示符, 因为 Bash 支持反斜杠转义的特殊字符,例如 \u(用户名) 和 \h (主机名) ,许多其他的shell都不支持这样定义。/etc/profile应该尝试和POSIX兼容,以便与用户可能自己安装的任何shell兼容。

Debian GNU/linux通常预装Dash,Dash是一个仅仅旨在实现POSIX (和一些伯克利) 扩展的基本shell。如果我们修改 /etc/profile (修改之前先备份) 让PS1='$ '这一行设置不同的值,然后模拟一个Dash登录 (通过dash -l命令) , 我们可以看到Dash会使用我们自定义的提示。但是,如果我们调用不带-l参数的dash命令,dash将不会读取/etc/profile。此时Dash会使用默认值 (这意味着此时PS1的值是我们修改之前的值) 。

换句话说,任何匹配/etc/profile.d/_.sh的可读内容都会被当作变量来源。这个非常重要,因为它表明直接编辑/etc/profile从来都不是实际需要的 (所以恢复你之前的备份) 。上面定义的任何变量都可以通过在一个单独的文件中配置,然后覆盖/etc/profile中的设置。这样做的好处是: 它允许系统升级时自动添加相应的变更到/etc/profile文件中。因为Debian的Apt包管理系统通常不会修改默认的配置文件。

~/.bash_profile, ~/.bash_login, and ~/.profile
  
/etc/profile存在的一个潜在问题是,它位于系统范围的路径中。这意味着修改它会影响这个系统上的所有用户。在个人计算机上,这可能不是太大的问题,但是修改它同时还需要root权限。由于这些原因,每个单独的Bash用户账户可以创建~/.bash_profile, ~/.bash_login 和 ~/.profil这几个文件中的任意一个作为Bash的配置文件来源。在列出的顺序中第一个被找到的文件会被作为配置文件,其余的都会被忽略。

其他的shell,例如Dash,支持相似的东西,但是只会查找~/.profile文件。这允许用户为Bash特定的应用场景配置单独的.bash_profile文件,如果在某些时候需要切换到Dash或其他shell作为登录shell (例如通过chsh -s dash命令) 。可以保留~/.profile作为这些shell的配置文件。

需要牢记的一点是,默认的Debian框架目录 (/etc/skel,用于存放要复制到新用户账户主目录的文件和目录) 包含.profile文件,但不包含.bash_profile和.bash_login文件。此外Debian使用Bash作为默认的shell,因此,许多Debian用户习惯于将他们的Bash 登录shell设置放在.profile文件中。

我曾经看到过一些项目的安装说明,例如RVN,这个项目建议用户创建一个.bash_profile文件,但是这样做是非常危险的,根据上面提到的知识我们知道,这个会改变用户的shell环境。即使用户没有修改.profile文件,它也可能利用默认~/.profile功能,将~/bin添加到$PATH环境变量。一个可能提高安全性的选项是,在创建用户的账户之前,将.bash_profile作为.bash_rc的符号链接文件,放到/etc/skel目录中。

如果我们查看Debian Jessie的默认.profile脚本,我们可以看到下面的代码片段:

```bash
# if running bash
  
if [ -n "$BASH_VERSION" ]; then
  
# include .bashrc if it exists
  
if [ -f "$HOME/.bashrc" ]; then
  
. "$HOME/.bashrc"
  
fi
  
fi
```
  
这和我们在/etc/profile里面看到的相似,如果shell是Bash,且发现了/etc/bash.bashrc文件,/etc/bash.bashrc文件就被当作Bash的配置文件。这一点的意义将在下一节讨论。

/etc/bash.bashrc 和 ~/.bashrc
  
启动的时候,Bash会同时读取/etc/bash.bashrc和~/.bashrc,但是只有在Bash Shell作为交互式Shell而不是登录Shell启动时 (意味着通过xtem启动) ,会依照这种顺序,这是Bash Shell的标准行为。然而,Debian分别从 /etc/profile和~/.profile登录脚本中获取配置文件。这会显著地改变行为,使得/etc/bash.bashrc和.bashrc (如果它们存在) 总是在Bash启动时调用,而不管是不是登录Shell。不要期待这种情况在不同地发行版中是一样的。

.bashrc是一个添加命令别名的好地方,实际上,一些用户拥有太多的别名,以至于他们宁愿将别名都放在一个单独的文件中去。Debian的默认.bashrc会查找.bash_alias,如果这个文件存在的话,会将它作为别名配置来源。所以你可以在这个文件中随意保存所有的Bash别名。如果用户愿意的话,.bashrc文件也是用户重写shell变量,例如$PS1或者$HISTSIZE的绝佳位置。Debian的默认.bashrc有超过100行,但是仍然可以非常清晰地阅读,且有良好地注释。见名知意,.bashrc不是其他非Bash shell的配置文件来源。

~/.xsession 和 ~/.xsessionrc
  
如果你是一个GNU/Linux桌面用户,通过显示管理器本地登录 (而不是通过getty登录程序) ,则/etc/profile和~/.profile不会像预期的那样工作。一些显示管理器会直接将这些文件视为错误地配置文件,例如Gnome显示管理器。但一些其他的显示管理器,例如LightDm不会这样。幸运的是,你还有一些其他的选项。

当启动X Window系统会话时 (不管是用显示管理或从虚拟终端启动startx) ,将会执行/etc/X11/Xsessionshell脚本。这基本上相当于登录shell调用/etc/profile。这个只对X Window生效,并且不是将其作为源配置文件,而是直接执行。但是它也相当复杂,类似于/etc/profile怎么从/etc/profile.d目录中的脚本读取配置,怎么从/etc/X11/Xsession.d/目录下的/etc/X11/Xsessions脚本中读取配置。在/etc/X11/Xsession.d目录下的所有脚本名称都以数字开头,因此所有的脚本都会按照数字顺序来读取。

Debian Jessie包含一个名叫40×11-common_xsessionrc的文件,这个文件做的工作就是检查~/.xsessionrc是不是可读的,如果是就用它作为配置文件的来源。这就使得~/.xsessions是一个加载环境变量或者运行一个一次性使用程序 (例如 xrandr 或 xmodmap ) 的完美位置 (仅适用于X会话) 。如果你希望的话,你同样可以将/etc/profile或~/.profile作为来源。那么任何指定的环境变量也都会被你的会话管理器继承 (如果还没有继承的话) 。请注意,默认情况下.xsessionrc是不存在的,需要你自己创建这个文件。

如果我们继续浏览/etc/X11/Xsession中的文件, 我们会发现50×11-common_determine-startup会决定加载哪个会话管理器。如果~/.xsessions文件存在而且是可执行的,它会被保存并且随后作为99×11-common_start的一部分执行,当~/.xsession用于运行会话管理器,X会话将会被注销。并且当这个脚本终止时,你会返回到显示管理器登录界面。

和~/.xsessionrc相似,~/.xsession默认也是不存在的,在你需要的时候你可以创建一个。你可能会创建一个类似下面给的简单的.xsession脚本

Start our session manager of choice

exec x-session-manager
  
其中x-session-manager默认设置为通过update-alternatives命令配置的任何内容,这样,你可以轻松地更改系统范围默认地会话管理器,只需要将x-session-manager替换为/usr/bin/startfce4 (切换到XFCE) ,其他的用户账户将完全不受影响。

当然,许多显示管理器提供从登录界面直接选择公共会话管理器的能力,所以这个文件通常是不必要的。然而.xsession提供了更多地灵活性,你可以用任何程序调用这个文件,而不仅仅是会话管理器。例如,在这里你可以在while循环中调用chromium或者iceweasel,而不是执行基本的kiosk模式设置。

~/.bash_logout
  
我们前面介绍了当用户运行交互式Bash登录shell时读取的文件,但是如果你想在注销以后仍然运行程序该怎么办？对于这个用例,~/.bash_logout文件就非常方便了。在Debian中默认的配置仅用于清除屏幕 (我认为从安全角度来说很重要) ,但是可以轻微地想象以下就知道能用于其他目的,例如,在你离开你的机器之前显示一个几秒钟的提醒。

主要的限制因素在于.bash_logout仅在注销交互式shell时读取,并且并不能假定它在注销X会话时会被加载。

其他选项
  
上面那些已经为你介绍了大部分的通用选项。其他的选项可能会存在,取决于你的安装环境 (例如/etc/environment) ,但是我不认为他们可能在其他的平台上存在,并且极少有需要去接触它们。

示例
  
那么你应该在哪放置你的系统范围环境变量？如果你希望一个环境变量可以影响所有用户,/etc/profiled./someifle.sh会是一个好的选择。但是,这假设你是使用一个登录管理器以/etc/profile作为配置来源。如果不是这样,你可以 (作为一个管理员) 添加一个脚本到/etc/X11/Xsession.d/来替代/etc/profile作为配置来源。

如果你希望一个脚本可以找到一个私人目录路径,并且添加它到你的PATH中,你需要考虑这个目录是不是会移动很多东西,如果你向.profile添加代码来实现,用户需要注销然后再登录来更改用户会话期间的PATH。如果你将代码添加到.bashrc中,这意味着代码将在用户每次打开xterm时执行,如果执行大约半秒以上可能就不太理想。所以这是一个权衡取舍的问题。

如果你仅仅是为了你个人登录会话时的一个环境变量,且它只关心X会话,你可以将它添加到~/.xsessionrc中。这样做的优点是,它通常将可用于通过X会话管理器启动的所有程序,因为它在启动X会话管理器之前被设置,并且被继承。例如,某些图形驱动程序可以通过运行

export vblank_mode=0
  
来禁用vsync。 所以位于.xsessionrc中的变量会影响到所有的程序。

然而如果这一行被添加到.bashrc中,则只有通过xterm登录的程序会被影响。通过一个窗口管理器启动的程序照常运行。你可以把它添加到.profile,并且从.xessionrc作为.profile的来源。但是之后,当你的X服务没有在运行的时候,你就不需要导出环境变量。

希望你现在可以更好地了解了登录和注销脚本在Debian GNU/Linux系统上的工作原理。如果你已经为这些登录和注销脚本创建、或者遇到任何特别有趣或有创新的用途,请在评论中告诉我们你是如何做到的。

在接下来的系列中,我们将讨论dotfile管理选项。

译文链接: [http://www.codeceo.com/article/linux-unix-login-script.html](http://www.codeceo.com/article/linux-unix-login-script.html)
  
英文原文: Understanding *NIX Login Scripts
  
翻译作者: 码农网 – 韩先生

[https://www.oschina.net/news/78491/linux-unix-login-script](https://www.oschina.net/news/78491/linux-unix-login-script)

## 不退出 shell 重新加载环境变量

只能是把新增的环境变量加载起来, 只在配置文件里注释掉行并不能 unset 环境变量, 需要 unset 的话得在 配置文件中显示的 unset

```Bash
“bash -l”，但这实际上创建了一个新的子shell，当你注销时，你将返回到“foo”仍在PATH中的封闭shell。

# 长格式命令
# source 是一个内置的 shell 命令，它执行作为参数传递的文件的内容, 示例中，它在当前 shell 中执行 .bashrc 文件。
source ~/.bashrc

# 较短版本
# .是“source”内置命令的 BASH 快捷方式。所以“. ~/.bashrc”对于 BASH 解释器来说与“source ~/.bashrc”是一样的。
# source 是 dot/period 的同义词。在 bash 中，但不是在 POSIX sh 中，因此为了获得最大的兼容性，请使用句点。
. ~/.bashrc

# . ~/.bashrc 或 source ~/.bashrc 将保留您当前的 shell 会话：除了将 ~/.bashrc 重新加载到当前 shell（采购）所做的修改之外，当前 shell 进程及其状态将被保留，其中包括环境变量、shell 变量、shell 选项、shell 函数和命令历史记录。

# exec 命令通过运行指定的命令行完全替换了 shell 进程。在我们的示例中，它用新的 bash 实例（使用更新的配置文件）替换当前 shell 的任何内容。
exec bash

```

