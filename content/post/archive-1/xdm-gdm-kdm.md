---
title: display manager(DM), 显示管理器, sddm, gdm3, lightdm
author: "-"
date: 2013-11-08T15:28:48+00:00
url: /?p=5910
tags:
  - Linux

categories:
  - inbox
---
## display manager(DM), 显示管理器, sddm, gdm3, lightdm

### sddm

    gdm - GNOME Display Manager
    kdm - KDE Display Manager
    xdm - X Display Manager 

我们先不讨论xdm/gdm/kdm这些东西。而是先看看启动X最直接的方式。首先来认识两个重要的文件，一个是X视窗启动文件-xinitrc，另外一个就是X视窗资源文件-Xdefaults.

### X视窗启动文件-xinitrc
事实上，我们一般执行startx来启动X Window System，其中startx就是xinit的前端界面[front-end].倘若我们以startx或xinit启动X，这指令会启动X server并且会执行$HOME/.xinitrc文件内的所设置的指令。倘若 $HOME没有这个文件，则系统会使用内定的的配置文件/etc/X11/xinit/xinitrc。而事实上xinitrc文件一般只包含有启动X时所要执行clients的shell script,里面定义一些指令和shell script，让X启动时，可以遵照里面的shell script来启动必要的应用程序。
例如我的简单而又实用的的$HOME/.xinitrc的内容如下: 

        LANG=zh_CN.GB2312
        LC_ALL=zh_CN.GB2312
      
      
        LC_CTYPE=zh_CN.GB2312
      
      
        KDE_LANG=zh_CN.GB2312
      
      
        export LANG LC_ALL LC_CTYPE KDE_LANG
      
      
        export XMODIFIERS=@im=Chinput
      
      
        /usr/bin/chinput &
      
      
        exec kde3
      
      
        killall chinput

对于更为详细的$HOME/.xinitrc，你可以找更专业的书籍来看，我的目标是越简单越好。前面的大家应该都比较清楚吧。先设一些环境变量，再设下一些输入法(我用的是智能五笔)， 接下来是启动视窗管理程序kde3，注意了: kde3用shell script的exec描述所执行的，这造成执行xinit程序的shell会被执行kde3的shell所取代。所以一旦kde3程序结束，就会跳出 shell，相对地，xinit将会跟着结束，X Server将关闭。这正是X Window Manager执行的方式。必须确定在.xinitrc中最后执行的是指令是以exec为开头的的命令执行X Windows Manager,而且不应该加上&放在一些背景执行，不然，那些指令也毫无意义。后面的killall chinput是告诉要结束chinput，不然极有可能会因为chinput的原因，会造成一些问题。这是最为简单的桌面设置。倘若你还要启动更多的程序和设置，都可以在前面加的。只要你在你的$HOME/.xinitrc文件中稍加增加便可做到，但要记住加在X Window Manager执行段落之前。

[2]X视窗资源文件-Xdefaults
 在X的文献中，resources有两种意义。第一种是指被server管理或建立桌面应用程序使用的东西，例如: 视窗、光标、字体等均属于这种意义。另外的一种又是指一种可以传递预设置值、参数和其它值给应用程序的方法，比如，可以定义视窗的大小、前景颜色、显示字体、快捷键等。而在X Window System的操作应用过程中，泛指的resources的意义也局限于第二种，主要是采用resources功能。在X Window System 的资源文件Xdefaults中，主要是设置合适自己喜欢的应用程序的操作操控环境或界面。一般会执行X后，会自动读取$ HOME/.Xdefaults.

呵呵，在 xterm 视窗中按有一个小技巧: 你按住Ctrl+鼠标右键会跳出一些字体等设置的东西，按住Ctrl+鼠标左键会跳出显示 xterm 应用程序的主菜单。另外，除了.Xdefaults资源可用处，还有一些应用程序会自己产生的的资源文件，一般放在
 /usr/XR116/lib/X11/app-defaults中，并以这些程序名称的大写文件名命名。比如，Xclok时钟程序的资源文件就是Xclock。其它的你自己看一下就会明白了。你可以直接修改这些应用程序的的资源文件，作为系统内定的应用程序的样式。不一定都要非得修改. Xdefaults来完成。因为.Xdefaults通常是个人爱好而使用环境来设置的东西。

2. 启动我们的 X Window System
X Window System的启动方法很多，最常用的还是上面得到的startx，除此外，还要先执行"X"启动X视窗系统，或者执行xinit启动X。现在的发行版本一般都是以xdm/gdm/kdm启动X，让Linux系统一启动就立即进入X Window System，并以图形模式让用用户来登录。倘若你想退出X Window Manager，你可以xterm中执行init 3离开。

### 以xinit/startx来启动X

这是一般的方法:我在Debain也是经常以这种方式来启动X的。就是执行/usr/XR116/bin/startx.事实上这个方法就是与直接执行/usr/X11R6/bin/xinit或是/usr/X11R6/bin/X是无异的。差别在于xinit和"X"并不会去执行读取读资源文件而去执行X Window Manager，所以一般的情况你得到的X视窗系统是个非常简朴的的一个X型鼠标指针与简朴的 xterm 而已。但xinit就是最标准的X启动方法，估计是绝大部分的系统X Window System都会支持。它是X Window System核心的程序，而startx仅是个启动xinit的shell script而已，里面同样定义执行xinit命令以启动X视窗系统。当一般执行startx时，X启动的过程大约就是这些东西了: 
  
1)xinit启动X server程序；
  
  
    2)X server会寻找$HOME/.xinintrc文件，有就执行它，没有就会转到/etc/X11/xinit/xinitrc读取系统内定的启动文件。
  
  
    3)接着就会读取$HOME/.Xdefaults，倘若没有，就会转到/usr/X11/xinit/Xcilents。从文件名 Xclients看来，这个是用来设置时执行哪些X应用的程序的文件。性质和xinitrc类似，同样是个shell script。但要注意的是:.Xdefaults是的权限具有755，即可执行。
  
  
    4)在正常的情况下，$HOME/.xinintrc是用来指派可以让X Window System正常运行的应用程序了。而.Xdefaults则被建议用来载入X资源设置和应用应用，以适合每个用户本身的喜爱程度而已。
  
  
    5)X server建立一个属于它自己的根视窗(Root windows)，并设置视窗的背景与执行所指定的应用程序，显示一个大的"X"光标，便完成启动了。
  
  
    6)在X server执行的期间，它一直控制着你的鼠标的键盘。
  
  
    这就是你能在屏幕上移动光标的原因，但由于目前还没有任何X client程序要求键盘和鼠标的输入。所以X server只是和鼠标一直移动而已。而其它的键盘或鼠标输入虽然都经过X server处理，但均被视为无作用(因为没有什么x clinet程序所接收)。这也是X启动的初期，按键盘或鼠标都没有反应的原因。但如果你能送信号给X server和X client的话，这下就有会作用了。比如: Ctrl+Alt+Backspace即是送给X Server的中断信号,当X启动到中途或者是执行时，只要按下这组合键，便会立即结束X server，跳回到command prompt terminal的状态。
  
  
7)接下来，在xinitrc唤起X server后，xinit会启动xterm程序。呵呵，xterm就是X Window terminal的缩写吧。它对X server而言是一个X Clietn程序而已。要求X server建立一个视窗，而且会告知X server在这个视窗中的鼠标和键盘的输入状态(Event)，因而启动xterm时便会视窗执行一个shell，内定的就是bash。当指标被移至视窗之内时，xterm便准备接受输入。键盘输入会被关到xterm中的shell就如同真的终端机输入一般。而从shell本身或其副程序的输出则借着 xterm显示在视窗上，xterm也接受输入，便得你能设置不同的程序操作参数和进行文本的一些操作，比如copy或paste.对于这些操作，你可以通过在xterm中执行ps auxw命令来观察到系统执行这些命令的详细步骤。
  
  
### 以xdm/gdm来启动你的X。
上面说到了以startx来启动你的X，也可通过xdm/gdm来启动你的X来启动你的X，这正是其它一些发行版本的采用的方式。比如 Redhat是gdm，而Mandrake用kdm。一般的情况，如果你要用调整你系统的run-level。比如修改你的/etc/inittab，把 id:3:initdefault中的3改为5。
  
  
    当系统以xdm/gdm来启动X Windows System。大约的步骤就是这些了:
  
  
    1)执行/etc/X11/xdm/Xserver启动X出现console登录的界面(是执行/etc/X11/xdm/GiveConsole&TakeConsole所产生的)
  
  
    2)执行/etc/X11/xdm/Xsessions来启动xdm或者是gdm。如果启动的是xdm，则装入用户家目录上的配置文件，.xsession和.Xclients。如果是gdm，则装载入/etc/X11/gdm/Sesseion与.Xclients。到此为止，就会出现X 视窗的登录的界面选项。
  
  
    3)gdm则会检查/etc/X11/gdm/Session目录的Session操作。比如Fvwm,Wmaker,Default, Failsafe，Gnome,Kde与Default等。并将显示给用户选择进入哪个X Window Manager。其实这些Sessions都是Shell Script file。如果你选择Kde，就进入KDE DeskTop environment，选择Gnome就会进入GNOME DeskTop environment了。
  
  
    4)用户如果选择是的Gnome，在输入用户名和password后，gdm GNOME Session就会找gnomerc script,$HOME/.gnomerc，如果没有这个文件，就会读会系统文件内定的GNOME resource file:/etc/X11/gdm/gnomerc，并且启动/usr/bin/gnome-session.
  
  
    这就完成了一个xdm/gdm的过程。但细心的人会发现，startx会读取$HOME/.xinitrc，而xdm/gdm为什么不会读取这个呢，它又是如何设置根视窗口背景及你的logo和X Window Manager的呢。其中的原因是因为xdm/gdm改用了/etc/X11/xdm/Setup_0来设置的。其中xsetroot是设置根视窗颜色的，并执行xconsole设置系统登录画面的登录位置(geometry)。
  
  
    如果你想修改xdm/gdm执行时所采用的color depth(色深？)，可以修改/etc/X11/xdm/Xservers中的内容。我的Mandrake90中的是这样的: 
 
    
      
        # more Xservers
      
      
        # $XConsortium: Xserv.ws.cpp,v 1.3 93/09/28 14:30:30 gildea Exp $
      
      
        #
      
      
        #
      
      
        # $XFree86: xc/programs/xdm/config/Xserv.ws.cpp,v 1.1.1.1.12.2 1998/10/04 15:23:
      
      
        14 hohndel Exp $
      
      
        #
      
      
        # Xservers file, workstation prototype
      
      
        #
      
      
        # This file should contain an entry to start the server on the
      
      
        # local display; if you have more than one display (not screen),
      
      
        # you can add entries to the list (one per line).? If you also
      
      
        # have some X terminals connected which do not support XDMCP,
      
      
        # you can add them here as well.? Each X terminal line should
      
      
        # look like:
      
      
        #? ? ? ?XTerminalName:0 foreign
      
      
        #
      
      
        :0 local /bin/nice -n -10 /usr/X11R6/bin/X -deferglyphs 16
      
    
  
  
    显然我的是采用16 bites颜色的。当然，你没有必要那么复杂，可以简单点儿，比如,我有时采用: 
  
  
    
      
        Java代码  
      
    
    
    
      
        ###使用16色
      
      
        :0 local /usr/X11R6/bin/X -bpp 16
      
      
        ###使用24色
      
      
        :0 local /usr/X11R6/bin/X -bpp 24
      
      
        ###使用32色
      
      
        :0 local /usr/X11R6/bin/X -bpp 32
      
    
  
  
    5)对于使用何种X Window Manager与载入方式，并不属于Display Manager的范围。Display Manager只要负责启动各种Sessions即可。总这一句话，X Display Manager只管理sessions，想要实现更外层的工作，则可以让sessions自己去做哦。
  
  
    6) 如果你喜欢那种方式Display Manager，你都可以选择嘛，修改成自己喜欢的东西。例如我的mandrake90中有/etc/X11/prefdm是目前系统内定使用的Display Manager。你看到它是只是一个/usr/bin/gdm一个连接而已。你还可以在/etc/inittab文件中最后定义像下面的，
 
        Java代码  
      
    
    
    
      
        #hehe,Run gdm in runlevel 5
      
      
        #gdm is now for pk'Mandrake separate server
      
      
        x:5:respawn:/etc/X11/prefdm -nodaemon
      
    
  
  
    你自己做个你系统有的xdm/gdm的连接就可以了。
  
  
    3。结束我们X Window Manager.
  
  
    这个大家都会了吧。最简单的就是选择X Window Manager中的exit或logout或相关的就可以了。
 呵呵，还记前面介绍的个 HOME/.xinitrc文件吧，是就在结束.xinitrc文件吧，执行了一个叫exec kde3的程序，这样的好处就是结束X Window Manager的时候，会连同x-server一起结束。另外的就是按CRTL+ALT+Backspace来结束你的X Window Manager吧，它就是把中断信号送给X-server结束X回到console terminal。
  
  
    上面的情况是针对用startx启动X的，如果你是用xdm/kdm/gdm来启动你的X的话，你按上面的方法是又会回到X视窗的登录界面的，X -server并不会结束。你可以在console下，运行init 3就会结束你的X-server，如果你是init 5的话，那X-server又回来了。
  
  
    Display Manager三兄弟
  
  
    X-Window下的Display Manager，可以在系统启动时自动进入图形化登录界面。现在算起来有三个，XDM、KDM和GDM。我称它们为DM三兄弟，但事实上这三兄弟的长相可 一点都不相像。老大XDM虽然丑了一点，但比较随和，一叫它就来；老二KDM长得比较标准，脾气和老大差不多；老三GDM相貌出众，总是一付很Cool的 样子，不爱搭理人，但碰到狠的，也就老实了。让我们一同来熟悉一下FreeBSD 5.1家的这DM三兄弟吧。
  
  
    0. 前言
 我拿到了FreeBSD 5.1后，就赶紧安装了起来。5.1版本的兼容性和硬件支持确实不错，在我的计算机上很顺利地就安装好了。
 由于我是预备把FreeBSD用作开发工作站，图形化的界面自然会比较轻易使用一些。我安装X-Window底层支持，和KDE、GNOME这两大窗口管理器。通过设置".xinitrc"文件，也能够在KDE和GNOME之间换来换去。但是总感觉不那么自然和彻底。看过了Linux发行版的窗口界面，知 道了Display Manager，这才开始熟悉了DM三兄弟。假如你已经安装了X-Server、KDE和GNOME，它们就已经在你的系统里了。没有的话，…。
  
  
    1. XDM
 前面说了，老大XDM比较随和。我们可以修改/etc/ttys文件，将下面的一行: 
 代码: ttyv8 "/usr/X11R6/bin/xdm -nodaemon" xterm off secure 中的off改为on。
 代码: ttyv8 "/usr/X11R6/bin/xdm -nodaemon" xterm on secure 重新启动系统，就会自动进入XDM，输入账号和密码，就会进入你原来设置好的KDE或GNOME桌面了。
 XDM确实够丑的，相信没有人想多看两眼的。裁判，换人！
  
  
    2. KDM
 为了老二KDM能够出场，我再次修改/etc/ttys文件。还是那一行，这次改为: 
 代码: ttyv8 "/usr/local/bin/kdm -nodaemon" xterm on secure 要让KDM自动在KDE和GNOME中切换，还要修改文件"/usr/X11R6/lib/X11/xdm/Xsession"。把中间的这段文字，
  
  
    
      
        Java代码  
      
    
    
    
      
        case $# in
      
      
        1)
      
      
        case $1 in
      
      
        failsafe)
      
      
        exec xterm -geometry 80x24-0-0
      
      
        ;;
      
      
        esac
      
      
        esac
      
    
  
  
    改成这样，
  
  
    
      
        Java代码  
      
    
    
    
      
        case $# in
      
      
        1)
      
      
        case $1 in
      
      
        kde)
      
      
        exec startkde
      
      
        ;;
      
      
        gnome)
      
      
        exec gnome-session
      
      
        ;;
      
      
        failsafe)
      
      
        exec xterm -geometry 80x24-0-0
      
      
        ;;
      
      
        esac
      
      
        esac
      
    
  
  
    如此目标识别已加载，让我们重新开始吧。
 慢点，还有一个地方需要修改一下。用root进入KDE中，找到"Login Manager"，在"Sessions"页下的"New Type"中，"kde"项已经有了，只要增加"gnome"，顺便再调整一下顺序吧。
 好了，现在再次重起系统，感觉如何？KDM还是很能干的。
  
  
    3. GDM
 老三GDM的大名，早有耳闻，在Linux家里也见到过，但把它请到咱FreeBSD家里来，我可是花了三个晚上，敲了无数次的门，才让它露出了真容。下面就是它提出来的条件。
 第一点，GDM好贱，需要一个特定的系统的账户，据说是为了安全。
  
  
    
      
        Java代码  
      
    
    
    
      
        pw groupadd –g 42 –n gdm
      
      
        pw useradd –c gdm –d /var/gdm –s /bin/sh –u 42 –n gdm
      
    
  
  
    如此，新建了一个gdm的Group，GID是42，一个gdm的User，UID是42。GID和UID，必须是没有被系统中其它账号占用，假如已被占 用，改用其它小于1000的。
 第二点，GDM需要一个有安全门的单间，还得过户到它的名下。
  
  
    
      
        Java代码  
      
    
    
    
      
        mkdir /var/gdm
      
      
        chmod 0750 /var/gdm
      
      
        chown gdm:gdm /var/gdm
      
    
  
  
    第三点，拉拉关系，搞好配置。这得修改 "/usr/X11R6/share/gnome/gdm/gdm.conf"才行，
 ServAuthDir=/usr/X11R6/share/gnome/gdm 改为: 
 ServAuthDir=/var/gdm
 再改Greeter=/usr/X11R6/bin/gdmlogin 为: 
 Greeter=/usr/X11R6/bin/gdmgreeter
 另外，下面的这三行，是true还是改成false，随便你了。
  
  
    
      
        Java代码  
      
    
    
    
      
        ShowGnomeChooserSession=true
      
      
        ShowGnomeFailsafeSession=true
      
      
        ShowXtermFailsafeSession=true
      
    
  
  
    第四点，GNOME和KDE都要支持。GDM是从GNOME那里来的，支持GNOME没什么问题。要支持KDE的Session，就比较啰嗦一点了。用ee编辑器写一段下面的命令，
  
  
    
      
        Java代码  
      
    
    
    
      
        #! /bin/sh
      
      
        exec /usr/X11R6/lib/X11/xdm/Xsession kde
      
    
  
  
    保存为文件 "/usr/X11R6/share/gnome/gdm/Sessions/Kde"，然后修改属性，
  
  
    
      
        Java代码  
      
    
    
    
      
        chmod –w x /usr/X11R6/share/gnome/gdm/Sessions/Kde
      
    
  
  
    第五点，现在该给老三让位了。用gdm替换kdm，这又要改"/etc/ttys"中的
 ttyv8 "/usr/local/bin/kdm -nodaemon" xterm on secure 为: 
 ttyv8 "/usr/X11R6/bin/gdm -nodaemon" xterm on secure
 做完上面的工作，重新启动系统。终于GDM总算给了面子，揭开了那漂亮的面纱，原来这GDM是她不是他，难怪难怪。忍不住要多看上几眼。
 辛劳的工作，由漂亮的DM开始，心情真好！
  



