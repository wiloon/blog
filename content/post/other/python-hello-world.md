---
title: Python Hello World
author: "-"
date: 2012-09-19T03:00:23+00:00
url: /?p=4075
categories:
  - Development
tags:
  - reprint
---
## Python Hello World

### install python3 pip3

    sudo dnf install python3

[http://blog.csdn.net/pjeby/article/details/1212592](http://blog.csdn.net/pjeby/article/details/1212592)

    简介
 我们将看一下如何用Python编写运行一个传统的"Hello World"程序。通过它，你将学会如何编写、保存和运行Python程序。
  
    有两种使用Python运行你的程序的方式——使用交互式的带提示符的解释器或使用源文件。我们将学习这两种方法。
  
  
    使用带提示符的解释器
          在命令行的shell提示符下键入python，启动解释器。现在输入print 'Hello World'，然后按Enter键。你应该可以看到输出的单词Hello World。
  
  
    对于Windows用户，只要你正确的设置了PATH变量，你应该可以从命令行启动解释器。或者你可以选择使用IDLE程序。IDLE是集成开发环境的缩写。点击开始->程序->Python 2.3->IDLE(Python GUI)。Linux用户也可以使用IDLE。
  
  
    注意，>>>是你键入Python语句的提示符。
  
  
    例1 使用带提示符的Python解释器
  
  
    $ python
 Python 2.4.3 (#1, Jul 26 2006, 16:42:40)
 [GCC 3.4.2 20050110 (Red Hat 3.4.2-6.fc3)] on linux2
 Type "help", "copyright", "credits" or "license" for more information.
 >>> print 'hello world'
 hello world
 >>>
  
    注意，Python会在下一行立即给出你输出！你刚才键入的是一句Python 语句 。我们使用print (不要惊讶) 来打印你提供给它的值。这里，我们提供的是文本Hello World，它被迅速地打印在屏幕上。
  
  
    如何退出Python提示符: 如果你使用的是Linux/BSD shell，那么按Ctrl-d退出提示符。如果是在Windows命令行中，则按Ctrl-z再按Enter。
 挑选一个编辑器
          在我们开始讲述以源文件方式编写Python程序之前，我们需要一个编辑器来写源文件。挑选一个编辑器确实是极其重要的。你挑选一个编辑器就如同你挑选一辆你将购买的轿车一样。一个好的编辑器会帮助你方便地编写Python程序，使你地编程旅程更加舒适，帮助你更加快捷安全地到达目的地 (实现目标) 。
  
    对于编辑器的基本要求之一是语法加亮功能，利用这一功能，你的Python程序的不同部分被标以不同的颜色，这样你可以更好 看清楚 你的程序，使它的运行显得形象化。
  
  
    如果你使用Windows，那么我建议你使用IDLE。IDLE具备语法加亮功能，还有许多其他的功能，比如允许你在IDLE中运行你的程序。特别值得注意的是: 不要使用Notepad——它是一个糟糕的选择，因为它没有语法加亮功能，而且更加重要的是，它不支持文本缩进。而我们将会看到文本缩进对于我们来说极其重要。一个好的编辑器，比如IDLE (还有VIM) 将会自动帮助你做这些事情。
  
  
    如果你使用Linux/FreeBSD，那么你有很多种选择。如果你是一位有经验的程序员，你一定已经在使用VIM或者Emacs了。勿庸置疑，它们是两个功能最强大的编辑器。使用它们编写你的Python程序，你将从中受益。我个人使用VIM编写我的大多数程序。如果你是一个初学编程的人，那么你可以使用Kate，它也是我最喜欢的编辑器之一。只要你愿意花时间学习使用VIM或Emacs，那么我强烈建议你一定要学习两者之一，因为从长远看来它们对你是极其有帮助的。
  
  
    使用源文件
 现在让我们重新开始编程。当你学习一种新的编程语言的时候，你编写运行的第一个程序通常都是"Hello World"程序，这已经成为一种传统了。在你运行"Hello World"程序的时候，它所做的事只是说声: "Hello World"。正如提出"Hello World"程序的Simon Cozens所说: "它是编程之神的传统咒语，可以帮助你更好的学习语言。"
  
    启动你选择的编辑器，输入下面这段程序，然后把它保存为helloworld.py。
  
  
    例2 使用源文件
  
  
    #!/usr/bin/python

Filename : helloworld.py

 print 'Hello World'
 为了运行这个程序，请打开shell (Linux终端或者DOS提示符) ，然后键入命令python helloworld.py。如果你使用IDLE，请使用菜单Edit->Run Script或者使用键盘快捷方式Ctrl-F5。输出如下所示。
  
    输出
 $ python helloworld.py
 Hello World
  
    如果你得到的输出与上面所示的一样，那么恭喜！——你已经成功地运行了你的第一个Python程序。
  
  
    万一你得到一个错误，那么请确保你键入的程序 准确无误 ，然后再运行一下程序。注意Python是大小写敏感的，即print与Print不一样——注意前一个是小写p而后一个是大写P。另外，确保在每一行的开始字符前没有空格或者制表符——我们将在后面讨论为什么这点是重要的。
  
  
    它如何工作:让我们思考一下这个程序的前两行。它们被称作 注释 ——任何在#符号右面的内容都是注释。注释主要作为提供给程序读者的笔记。
  
  
Python至少应当有第一行那样的特殊形式的注释。它被称作 组织行 ——源文件的头两个字符是#!，后面跟着一个程序。这行告诉你的Linux/Unix系统当你 执行 你的程序的时候，它应该运行哪个解释器。这会在下一节做详细解释。注意，你总是可以通过直接在命令行指定解释器，从而在任何平台上运行你的程序。就如同命令python helloworld.py一样。
  
  
    
          在你的程序中合理地使用注释以解释一些重要的细节——这将有助于你的程序的读者轻松地理解程序在干什么。记住，这个读者可能就是6个月以后的你！
  
  
    跟在注释之后的是一句Python 语句 ——它只是打印文本"Hello World"。print实际上是一个操作符，而"Hello World"被称为一个字符串——别担心我们会在后面详细解释这些术语。
  
  
    可执行的Python程序
 这部分内容只对Linux/Unix用户适用，不过Windows用户可能也对程序的第一行比较好奇。首先我们需要通过chmod命令，给程序可执行的许可，然后 运行 程序。
  
    chmod a+x helloworld.py
 $ ./helloworld.py
 Hello World
  
    chmod命令用来 改变 文件的 模式 ，给系统中所有用户这个源文件的执行许可。然后我们可以直接通过指定源文件的位置来执行程序。我们使用./来指示程序位于当前目录。
  
  
    为了更加有趣一些，你可以把你的文件名改成仅仅helloworld，然后运行./helloworld。这样，这个程序仍然可以工作，因为系统知道它必须用源文件第一行指定的那个解释器来运行程序。
  
  
    只要知道程序的确切位置，你现在就可以运行程序了——但是如果你希望你的程序能够从各个位置运行呢？那样的话，你可以把你的程序保存在PATH环境变量中的目录之一。每当你运行任何程序，系统会查找列在PATH环境变量中的各个目录。然后运行那个程序。你只要简单地把这个源文件复制到PATH所列目录之一就可以使你的程序在任何位置都可用了。
  
  
    $ echo $PATH
 /opt/mono/bin/:/usr/local/bin:/usr/bin:/bin:/usr/X11R6/bin:/home/swaroop/bin
 $ cp helloworld.py /home/swaroop/bin/helloworld
 $ helloworld
 Hello World
  
    我们能够用echo命令来显示PATH变量，用$给变量名加前缀以向shell表示我们需要这个变量的值。我们看到/home/swaroop/bin是PATH变量中的目录之一。swaroop是我的系统中使用的用户名。通常，在你的系统中也会有一个相似的目录。你也可以把你选择的目录添加到PATH变量中去——这可以通过运行PATH=$PATH:/home/swaroop/mydir完成，其中"/home/swaroop/mydir"是我想要添加到PATH变量中的目录。
  
  
    当你想要在任何时间、任何地方运行你的程序的时候，这个方法十分有用。它就好像创造你自己的指令，如同cd或其他Linux终端或DOS提示符命令那样。
  
  
    提示:对于Python来说，程序、脚本或者软件都是指同一个东西。
  
  
    获取帮助
 如果你需要某个Python函数或语句的快速信息帮助，那么你可以使用内建的help功能。尤其在你使用带提示符的命令行的时候，它十分有用。比如，运行help(str)——这会显示str类的帮助。str类用于保存你的程序使用的各种文本 (字符串) 。类将在后面面向对象编程的章节详细解释。
  
    注释:按q退出帮助。
  
  
    类似地，你可以获取Python中几乎所有东西的信息。使用help()去学习更多关于help本身的东西！
  
  
    如果你想要获取关于如print那样操作符的帮助，那么你需要正确的设置PYTHONDOCS环境变量。这可以在Linux/Unix中轻松地通过env命令完成。
  
  
    $ env PYTHONDOCS=/usr/share/doc/python-docs-2.4.3/html/python
 Python 2.3.4 (#1, Jul 26 2006, 16:42:40)
 [GCC 3.4.2 20050110 (Red Hat 3.4.2-6.fc3)] on linux2
 Type "help", "copyright", "credits" or "license" for more information.
 >>> help('print')
  
    你应该注意到我特意在"print"上使用了引号，那样Python就可以理解我是希望获取关于"print"的帮助而不是想要它打印东西。
  
  
    注意，我使用的位置是在Fedora Core 3 Linux中的位置——它可能在不同的发行版和版本中有所不同。
  