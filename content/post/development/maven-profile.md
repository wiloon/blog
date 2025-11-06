---
title: Maven profile
author: "-"
date: 2011-10-28T01:35:50+00:00
url: /?p=1330
categories:
  - Inbox
tags:
  - Maven

---
## Maven profile
首先简单介绍下 Maven 的 profile 是什么。对于人来说，profile 是指人的肖像，轮廓，比如论坛里每个人注册了帐号后，可以设置自己的 profile，放上照片，介绍等等。对于 Maven 来说又是怎样呢？整个项目定义好了项目对象模型 (POM) ，就像论坛为每个人提供了默认的行为功能，如果我想改变我机器上的 POM 呢？这时就可以使用 profile。下面举个例子: 


  
    
      <profiles>
    
    
        <profile>
    
    
          <id>jdk16</id>
    
    
          
    
    
            <jdk>1.6</jdk>
    
    
          </activation>
    
    
          <modules>
    
    
            <module>simple-script</module>
    
    
          </modules>
    
    
        </profile>
    
    
      </profiles>
    
  

这个 profile 的意思是，当机器上的 JDK 为1.6的时候，构建 simple-script 这个子模块，如果是1.5或者1.4，那就不构建，这个 profile 是由环境自动激活的。

我们需要在合适的地方使用合适的 profile ，并且在合适的时候用合适的方式将其激活，你不能在构建服务器上激活非公共的 profile，你也不能要求开发人员写很复杂的命令来使用常规的 profile。因此这里介绍一下几种 profile 的激活方式。

1. 根据环境自动激活。

如前一个例子，当 JDK 为1.6的时候，Maven 就会自动构建 simple-script 模块。除了 JDK 之外，我们还可以根据操作系统参数和 Maven 属性等来自动激活 profile，如: 


  
    
      Xml代码
  
  
  
    
      <profile>
    
    
        <id>dev</id>
    
    
        
    
    
          false</activeByDefault>
    
    
          <jdk>1.5</jdk>
    
    
          <os>
    
    
            <name>Windows XP</name>
    
    
            <family>Windows</family>
    
    
            x86</arch>
    
    
            <version>5.1.2600</version>
    
    
          </os>
    
    
          <property>
    
    
            <name>mavenVersion</name>
    
    
            <value>2.0.5</value>
    
    
          </property>
    
    
          <file>
    
    
            <exists>file2.properties</exists>
    
    
            <missing>file1.properties</missing>
    
    
          </file>
    
    
        </activation>
    
    
        ...
    
    
      </profile>
    
  

2. 通过命令行参数激活。
这是最直接和最简单的方式，比如你定义了一个名为 myProfile 的 profile，你只需要在命令行输入 **mvn clean install -Pmyprofile** 就能将其激活，这种方式的好处很明显，但是有一个很大的弊端，当 profile 比较多的时候，在命令行输入这写 -P 参数会让人觉得厌烦，所以，如果你一直用这种方式，觉得厌烦了，可以考虑使用其它自动激活的方式。

3. 配置默认自动激活。

方法很简单，在配置 profile 的时候加上一条属性就可以了，如: 
  
http://juvenshun.iteye.com/blog/208714
  
  
    
      <profile>
    
    
        <id>dev</id>
    
    
        
    
    
          true</activeByDefault>
    
    
        </activation>
    
    
        ...
    
    
      </profile>
    
  

在一个特殊的环境下，配置默认自动激活的 profile 覆盖默认的 POM 配置，非常简单有效。

1. 配置 settings.xml 文件 profile 激活。

settings.xml 文件可以在 ~/.m2 目录下，为某个用户的自定义行为服务，也可以在 M2_HOME/conf 目录下，为整台机器的所有用户服务。而前者的配置会覆盖后者。同理，由 settings.xml 激活的 profile 意在为用户或者整个机器提供特定环境配置，比如，你可以在某台机器上配置一个指向本地数据库 URL 的 profile，然后使用该机器的 settings.xml 激活它。激活方式如下: 


  
    
      Xml代码
  
  
  
    
      <settings>
    
    
        ...
    
    
        
    
    
          local_db</activeProfile>
    
    
        </activeProfiles>
    
    
      </settings>
    
  

Maven 提供的 profile 功能非常强大和灵活，用得好的话，可以有效的隔离很多特殊的配置，使得整个项目能在不同环境中顺利的构建。但是，强大和灵活带来得问题是相对难掌握，希望本文能对 Maven 使用者有帮助。

[http://juvenshun.iteye.com/blog/208714](http://juvenshun.iteye.com/blog/208714)