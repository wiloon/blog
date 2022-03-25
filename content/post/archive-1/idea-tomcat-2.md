---
title: idea tomcat
author: "-"
date: 2012-12-29T04:58:37+00:00
url: /?p=4954
categories:
  - Uncategorized

tags:
  - reprint
---
## idea tomcat
部署在项目开发过程中是常有的事,特别是debug的时候。但是如果每次fix一个bug都要把整个项目重新部署一遍以便测试fix的效果或者继续debug其他bug,那对开发人员来说无疑是一大噩梦。不过谁都不想噩梦连连,有了JVM的hotSwap以及Intellij Idea对debug,hotSwap的支持,从此美梦相伴 (夸张了点:)) 。今天通过这篇文章介绍一下通过对Intellij Idea热部署的设置达到最方便的最高效的debug效果。

我想在介绍具体设置之前,不妨了解一些背景知识和概念。

  * **HotSwap**: "HotSwap"是JPDA (Java Platform Debugger Architecture) 中的一个特性,JPDA增强是自Java 2 SDK1.4新增的功能。HotSwap允许将JVM中的类定义替换为新的类定义,这就允许开发人员在debug时,将修改过的class替换JVM中旧有的class,无需重新启动服务器。不过,目前HotSwap只支持对方法body的修改,不支持对类和方法签名的修改 (比如修改类名,方法名,方法参数等) 。考虑这些限制,也是有理由的,替换类定义,就需要新类和旧类之间有一个关联,这里关联就是类的全名 (或许还有其他信息) ,类名都改了,就不知道替换哪个类了。至于方法签名的修改,应该是考虑到运行时方法的调用,通过方法签名替换已有的方法调用。
  * **三种目录**: 项目的源程序目录,构建输出目录,部署目录 (这是我按照我个人理解划分的) 。热部署的设置与这些目录有着密切关系。源程序目录包括java文件,资源文件,web资源文件等项目文件的目录；构建输出目录是指通过编译java源文件,copy资源文件构建一个应用程序部署之后应该具有的目录结构；部署目录很好理解,就是应用程序在服务器中可以存在的位置。

通常我们部署一个应用是将该应用打包成war或者ear,而通常开发阶段是构建成Server指定的目录结构来部署到Server上,如果每次要copy来copy去,那麻烦死了。所以我们要想办法减少不必要的copy。

  * **第一种方法**: 在Server部署目录下设置构建输出目录,以tomcat为例,就是在%tomcat_home%webapps目录下建立一个新的目录,目录名就是你的应用context,具体就是打开项目设置界面 (ctrl+alt+shift+S,v8.0) ,选择Modules,将你的应用Exploded Directory设置为%tomcat_home%webappsyourContext。同时,将你各个Module的编译输出路径设置为%tomcat_home%webappsyourContextWEB-INFclasses (可能需要你预先手动建立) ,这样class文件就自动生成到该目录下。
  * **第二种方法**: 现在一些Server都支持重定向,以tomcat为例,可以在%tomcat_home%confCatalinalocalhost下创建一个xml配置文件将部署目录指定为你的构建输出目录。代码片段如: <Context path="/myApp" docBase="D:workspacemyProjectoutexplodedmyApp" />。这样每次修改了java文件之后comile一下修改的文件,对于jsp需要make一下,就能达到热部署的目的。其实现在Intellj Idea默认设置使用的就是这种方法,只不过这个重定向的配置文件在你的Documents and Settings里面,所以你如果你使用这样方法,不必自己设置。

其实,这两种方法是异曲同工。

**进一步设置**: 将你的构建输出目录直接设置在源程序目录中,然后重定向的docBase直接指向你的web根目录 (就是WEB-INF的父目录) 。这样,你只要将编译输出目录设置为WEB-INFclasses就行了,而且,修改JSP文件都不要重新构建,唯一要做的就是修改了java文件之后compile一下。

**再进一步设置**: 打开Setting界面 (ctrl+alt+S) ,然后

  * 其一: 选择Compiler选项,在Deploy web application to servers after compilatoin下勾选Never,为什么选Never？因为根据我们上面的设置,对于java文件的修改,编译 (compile,ctrl+shift+f9) 之后已经更新到了部署目录,而对于其他文件 (例如jsp) ,构建 (make,ctrl+f9) 之后也都更新到了部署目录,当然如果你的部署目录就设置在源程序目录中,那jsp都不要在make了。
  * 其二: 选择Debugger-HotSwap选项,确保勾选了Make project before reloading classes,同时选择Reload classes after compilation为Always。这样我们在编译某个修改了的java文件之后,就会利用HotSwap机制reload class,而Make project before reloading classes就确保了其他修改过的文件一起同步到部署目录。

这样,经过上面这些设置,在debug时最大程度上减少了Re-deploy和重启服务器的次数。对于内存不足的电脑来说,re-deploy次数多了,就会outOfMemory,然后不得不重启服务器。

小建议: 由于HotSwap的限制,能够提前定义好的属性,方法,预先写在类里面,方法body的具体逻辑可以以后再加,这样有利于减少了hotswap失败的次数。