---
title: maven profile
author: "-"
date: 2016-01-06T03:01:01+00:00
url: /?p=8651
categories:
  - Inbox
tags:
  - Maven

---
## maven profile

<http://haohaoxuexi.iteye.com/blog/1900568>

4       profile介绍
  
4.1     profile简介
  
profile可以让我们定义一系列的配置信息,然后指定其激活条件。这样我们就可以定义多个profile,然后每个profile对应不同的激活条件和配置信息,从而达到不同环境使用不同配置信息的效果。比如说,我们可以通过profile定义在jdk1.5以上使用一套配置信息,在jdk1.5以下使用另外一套配置信息；或者有时候我们可以通过操作系统的不同来使用不同的配置信息,比如windows下是一套信息,linux下又是另外一套信息,等等。具体的激活条件有哪些我在后文会讲到。

4.2     profile的定义位置
  
对于使用Maven3,我们可以有多个地方定义profile。定义的地方不同,它的作用范围也不同。

 (1)     针对于特定项目的profile配置我们可以定义在该项目的pom.xml中。

 (2)     针对于特定用户的profile配置,我们可以在用户的settings.xml文件中定义profile。该文件在用户家目录下的".m2"目录下。

 (3)     全局的profile配置。全局的profile是定义在Maven安装目录下的"conf/settings.xml"文件中的。

4.3     profile中能定义的信息
  
profile中能够定义的配置信息跟profile所处的位置是相关的。以下就分两种情况来讨论,一种是定义在settings.xml中,另一种是定义在pom.xml中。

4.3.1  profile定义在settings.xml中
  
当profile定义在settings.xml中时意味着该profile是全局的,它会对所有项目或者某一用户的所有项目都产生作用。因为它是全局的,所以在settings.xml中只能定义一些相对而言范围宽泛一点的配置信息,比如远程仓库等。而一些比较细致一点的需要根据项目的不同来定义的就需要定义在项目的pom.xml中。具体而言,能够定义在settings.xml中的信息有 <repositories>、<pluginRepositories>和<properties>。定义在<properties>里面的键值对可以在pom.xml中使用。

4.3.2  profile定义在pom.xml中
  
定义在pom.xml中的profile可以定义更多的信息。主要有以下这些:

l  <repositories>

l  <pluginRepositories>

l  <dependencies>

l  <plugins>

l  <properties>

l  <dependencyManagement>

l  <distributionManagement>

l  还有build元素下面的子元素,主要包括:

<defaultGoal>

<resources>

<testResources>

<finalName>

4.4     profile的激活方式
  
Maven给我们提供了多种不同的profile激活方式。比如我们可以使用-P参数显示的激活一个profile,也可以根据环境条件的设置让它自动激活等。下面将对它们一一进行介绍:

4.4.1  使用activeByDefault设置激活
  
先看下面一个配置

Xml代码
  
<profiles>
  
<profile>
  
<id>profileTest1</id>
  
<properties>
  
<hello>world</hello>
  
</properties>
  
true</activeByDefault>
  
</activation>
  
</profile>

<profile>
  
<id>profileTest2</id>
  
<properties>
  
<hello>andy</hello>
  
</properties>
  
</profile>
  
</profiles>
  
我们可以在profile中的activation元素中指定激活条件,当没有指定条件,然后指定activeByDefault为true的时候就表示当没有指定其他profile为激活状态时,该profile就默认会被激活。所以当我们调用mvn package的时候上面的profileTest1将会被激活,但是当我们使用mvn package –P profileTest2的时候将激活profileTest2,而这个时候profileTest1将不会被激活。

4.4.2  在settings.xml中使用activeProfiles指定处于激活状态的profile
  
我们可以在settings.xml中使用activeProfiles来指定需要激活的profile,这种方式激活的profile将所有情况下都处于激活状态。比如现在我们定义了如下两个profile

Xml代码
  
<profiles>
  
<profile>
  
<id>profileTest1</id>
  
<properties>
  
<hello>world</hello>
  
</properties>
  
</profile>

<profile>
  
<id>profileTest2</id>
  
<properties>
  
<hello>andy</hello>
  
</properties>
  
</profile>
  
</profiles>
  
这里的profile可以是定义在settings.xml中的,也可以是定义在pom.xml中的。这个时候如果我们需要指定profileTest1为激活状态,那么我们就可以在settings.xml中定义activeProfiles,具体定义如下:

Xml代码
  
profileTest1</activeProfile>
  
</activeProfiles>
  
考虑这样一种情况,我们在activeProfiles下同时定义了多个需要激活的profile。这里还拿上面的profile定义来举例,我们定义了同时激活profileTest1和profileTest2。

Xml代码
  
profileTest1</activeProfile>
  
profileTest2</activeProfile>
  
</activeProfiles>
  
从profileTest1和profileTest2我们可以看出它们共同定义了属性hello。那么这个时候我在pom.xml中使用属性hello的时候,它到底取的哪个值呢？是根据activeProfile定义的顺序,后面的覆盖前面的吗？根据我的测试,答案是非也,它是根据profile定义的先后顺序来进行覆盖取值的,然后后面定义的会覆盖前面定义的。

4.4.3  使用-P参数显示的激活一个profile
  
假设我们现在有如下定义的profiles

Xml代码
  
<profiles>
  
<profile>
  
<id>profileTest1</id>
  
<properties>
  
<hello>world</hello>
  
</properties>
  
</profile>
  
<profile>
  
<id>profileTest2</id>
  
<properties>
  
<hello>andy</hello>
  
</properties>
  
</profile>
  
<profiles>
  
那么当我们在进行Maven操作时就可以使用-P参数显示的指定当前激活的是哪一个profile了。比如我们需要在对项目进行打包的时候使用id为profileTest1的profile,我们就可以这样做:

Cmd代码
  
mvn package –P profileTest1
  
当我们使用activeByDefault或settings.xml中定义了处于激活的profile,但是当我们在进行某些操作的时候又不想它处于激活状态,这个时候我们可以这样做:

Cmd代码
  
Mvn package –P !profileTest1
  
这里假设profileTest1是在settings.xml中使用activeProfile标记的处于激活状态的profile,那么当我们使用"-P !profile"的时候就表示在当前操作中该profile将不处于激活状态。

4.4.4根据环境来激活profile
  
profile一个非常重要的特性就是它可以根据不同的环境来激活,比如说根据操作系统的不同激活不同的profile,也可以根据jdk版本的不同激活不同的profile,等等。

4.4.4.1根据jdk来激活profile
  
Xml代码
  
<profiles>
  
<profile>
  
<id>profileTest1</id>
  
<jdk>1.5</jdk>
  
</profile>
  
<profiles>
  
上面情况表示在jdk为1.5版本系列的时候激活profileTest1。

Xml代码
  
<profiles>
  
<profile>
  
<id>profileTest1</id>
  
<jdk>[1.4,1.7)</jdk>
  
</profile>
  
<profiles>
  
上面的情况表示在jdk为1.4、1.5和1.6的时候激活profileTest1。

4.4.4.2根据操作系统来激活profile
  
Xml代码
  
<profiles>
  
<profile>
  
<id>profileTest1</id>
  
<os>
  
<name>Windows XP</name>
  
<family>Windows</family>
  
x86</arch>
  
<version>5.1.2600</version>
  
</os>
  
</activation>
  
</profile>
  
</profiles>
  
上面的情况就是根据操作系统的类型来激活profileTest1。

4.4.4.3根据系统属性来激活profile
  
Xml代码
  
<profiles>
  
<profile>
  
<id>profileTest1</id>
  
<property>
  
<name>hello</name>
  
<value>world</value>
  
</property>
  
</activation>
  
</profile>
  
</profiles>
  
上面的profileTest1将在提供了系统属性hello,并且其值为world的时候激活。下面的做法可以激活profileTest1。

Cmd代码
  
mvn package –Dhello=world
  
当是下面的这种定义形式时,profileTest1将在指定了系统属性hello,且其值为任意值的时候被激活。

Xml代码
  
<profiles>
  
<profile>
  
<id>profileTest1</id>
  
<property>
  
<name>hello</name>
  
</property>
  
</activation>
  
</profile>
  
</profiles>
  
4.4.4.4根据文件是否存在激活profile
  
Xml代码
  
<profiles>
  
<profile>
  
<id>profileTest1</id>
  
<file>
  
<exists>target</exists>
  
</file>
  
</activation>
  
</profile>
  
</profiles>
  
上面的定义表示当存在target文件时激活profileTest1。

Xml代码
  
<profiles>
  
<profile>
  
<id>profileTest1</id>
  
<file>
  
<missing>target</missing>
  
</file>
  
</activation>
  
</profile>
  
</profiles>
  
上面的定义表示当不存在target文件时激活profileTest1。

4.5     查看当前处于激活状态的profile
  
我们可以同时定义多个profile,那么在建立项目的过程中,到底激活的是哪一个profile呢？Maven为我们提供了一个指令可以查看当前处于激活状态的profile都有哪些,这个指定就是mvn help:active-profiles。

现在假设我们的settings.xml文件中有如下profile的定义:

Xml代码
  
<profiles>
  
<profile>
  
<id>profileTest1</id>
  
<file>
  
<missing>target</missing>
  
</file>
  
</activation>
  
</profile>
  
</profiles>

profileTest1</activeProfile>
  
</activeProfiles>
  
这个时候我们可以看到,我们已经定义了profileTest1始终为激活状态,这个时候我们使用mvn help:active-profiles查看处于激活状态的profile时,就会打印出如下内容:
