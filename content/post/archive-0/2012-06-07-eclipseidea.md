---
title: 'eclipse>IDEA'
author: wiloon
type: post
date: 2012-06-07T06:36:37+00:00
url: /?p=3431
categories:
  - Development
tags:
  - IDEA

---
outline - structure, Ctrl+F12

本文转自：<http://gagi.iteye.com/blog/633778>



1、比如输入eclipse下面的main，sysout等，在idea里面同样可以实现，如下：


  
    
      Java代码  <a title="收藏这段代码"><img src="http://gagi.iteye.com/images/icon_star.png" alt="收藏代码" /></a>
    
  
  
  <ol>
    <li>
      sysout(sout 按tab)，main(psvm按tab),具体可按照ctrl+j
    </li>
  </ol>


2、性能优化


  
    
      Java代码  <a title="收藏这段代码"><img src="http://gagi.iteye.com/images/icon_star.png" alt="收藏代码" /></a>
    
  
  
  <ol>
    <li>
      修改idea.exe.vmoptions配置文件调整以下内容：
    </li>
    <li>
      -Xms256m
    </li>
    <li>
      -Xmx384m
    </li>
    <li>
      -XX:MaxPermSize=128m
    </li>
    <li>
      -XX:NewRatio=4
    </li>
    <li>
      -Xss128k
    </li>
    <li>
      -Dsun.awt.keepWorkingSetOnMinimize=true
    </li>
    <li>
      -server
    </li>
    <li>
      -Xms256m设置初时的内存数，你需要设置一个合理的值， 增加该值可以提高Java程序的启动速度。如果你的内存够大，如2G，可以设置到400m。
    </li>
    <li>
      -Xmx384m设置最大内存数，提高该值，可以减少内存Garage收集的频率，提高程序性能。
    </li>
    <li>
      -Dsun.awt.keepWorkingSetOnMinimize=true可以让IDEA最小化到任务栏时依然保持以占有的内存，当你重新回到IDEA，能够被快速显示，而不是由灰白的界面逐渐显现整个界面，加快回复到原界面的速度。
    </li>
    <li>
      -server控制内存garage方式，这样你无需在花一到两分钟等待内存garage的收集。
    </li>
  </ol>


3、优化文件保存和工程加载


  
    
      Java代码  <a title="收藏这段代码"><img src="http://gagi.iteye.com/images/icon_star.png" alt="收藏代码" /></a>
    
  
  
  <ol>
    <li>
      取消“Synchronize file on frame activation”和“Save files on framedeactivation”的选择
    </li>
    <li>
      同时我们选择&#8221;Save files automatically&#8221;, 并将其设置为30秒，这样IDEA依然可以自动保持文件,所以在每次切换时，你需要按下Ctrl+S保存文件
    </li>
    <li>
    </li>
    <li>
      如何让IntelliJ IDEA动的时候不打开工程文件：Settings->General去掉Reopen last project on startup
    </li>
  </ol>


4、用*标识编辑过的文件


  
    
      Java代码  <a title="收藏这段代码"><img src="http://gagi.iteye.com/images/icon_star.png" alt="收藏代码" /></a>
    
  
  
  <ol>
    <li>
      Editor –> Editor Tabs
    </li>
    <li>
      —————————————–
    </li>
    <li>
      在IDEA中，你需要做以下设置, 这样被修改的文件会以*号标识出来，你可以及时保存相关的文件。
    </li>
    <li>
      "Mark modifyied tabs with asterisk&#8221;
    </li>
  </ol>


5、显示行号


  
    
      Java代码  <a title="收藏这段代码"><img src="http://gagi.iteye.com/images/icon_star.png" alt="收藏代码" /></a>
    
  
  
  <ol>
    <li>
      如何显示行号：Settings->Editor->Appearance标签项，勾选Show line numbers
    </li>
  </ol>


6、自定义键盘快捷方式


  
    
      Java代码  <a title="收藏这段代码"><img src="http://gagi.iteye.com/images/icon_star.png" alt="收藏代码" /></a>
    
  
  
  <ol>
    <li>
      如果默认代码提示和补全快捷键跟输入法冲突，如何解决：Settings->Keymap
    </li>
  </ol>


7、如何让光标不随意定位


  
    
      Java代码  <a title="收藏这段代码"><img src="http://gagi.iteye.com/images/icon_star.png" alt="收藏代码" /></a>
    
  
  
  <ol>
    <li>
      Settings->Editor中去掉Allow placement of caret after end of line。
    </li>
  </ol>


8、中文乱码问题


  
    
      Java代码  <a title="收藏这段代码"><img src="http://gagi.iteye.com/images/icon_star.png" alt="收藏代码" /></a>
    
  
  
  <ol>
    <li>
      在包含中文文件名或者文件夹的时候会出现??的乱码，解决方法如下：
    </li>
    <li>
    </li>
    <li>
      File菜单->Settings->Colors & Fonts->Editor Font=宋体, size=12, line spacing =1.0
    </li>
    <li>
      File菜单->Settings->Appearance-> Font Name=Simsun，size=12
    </li>
  </ol>


9、如何完美显示中文


  
    
      Java代码  <a title="收藏这段代码"><img src="http://gagi.iteye.com/images/icon_star.png" alt="收藏代码" /></a>
    
  
  
  <ol>
    <li>
      Settings->Appearance中勾选Override default fonts by (not recommended)，设置Name:NSimSun，Size:12
    </li>
  </ol>


10编辑自动提示


  
    
      Java代码  <a title="收藏这段代码"><img src="http://gagi.iteye.com/images/icon_star.png" alt="收藏代码" /></a>
    
  
  
  <ol>
    <li>
      editor->code completion->autopopup的三个选项都选上，都设置为0
    </li>
    <li>
      Case sensitive completion ->none
    </li>
    <li>
      parameter info->autoopopup in ->0
    </li>
  </ol>




11、一些有用的快捷键


  
    
      Java代码  <a title="收藏这段代码"><img src="http://gagi.iteye.com/images/icon_star.png" alt="收藏代码" /></a>
    
  
  
  <ol>
    <li>
      Ctrl+Shift+N 查找文件
    </li>
    <li>
      Ctrl+Alt+L  格式化代码
    </li>
    <li>
      Ctrl+Alt+O 优化导入的类和包
    </li>
    <li>
      Alt+/ 自动补全代码 注：默认与输入法有冲突，在setting->keymap->main menu->code->complete code->basic
    </li>
    <li>
      Ctrl+P 方法参数提示
    </li>
    <li>
      Ctrl+X 删除行
    </li>
    <li>
      Ctrl+D 复制行
    </li>
    <li>
      Ctrl+H 显示类结构图
    </li>
    <li>
      Ctrl+Q 显示注释文档
    </li>
    <li>
      [b]Alt+1 快速打开或隐藏工程面板[/b]
    </li>
    <li>
      F2 或Shift+F2 高亮错误或警告快速定位
    </li>
    <li>
      代码标签输入完成后，按Tab，生成代码。
    </li>
    <li>
      选中文本，按Ctrl+Shift+F7 ，高亮显示所有该文本，按Esc高亮消失。
    </li>
    <li>
      Ctrl+W 选中代码，连续按会有其他效果
    </li>
    <li>
      选中文本，按Alt+F3 ，逐个往下查找相同文本，并高亮显示。
    </li>
    <li>
      Ctrl+Up/Down 光标跳转到第一行或最后一行下
    </li>
    <li>
      Ctrl+B 快速打开光标处的类或方法
    </li>
  </ol>
