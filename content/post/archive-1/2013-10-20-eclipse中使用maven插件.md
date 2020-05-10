---
title: Eclipse中使用Maven插件
author: wiloon
type: post
date: 2013-10-20T04:58:58+00:00
url: /?p=5855
categories:
  - Uncategorized
tags:
  - Maven

---
安装Maven

下载Maven最新版本，见：http://maven.apache.org/download.html

&nbsp;

当前版本2.0.7。解压缩下载的文件, 将其中的bin目录设置到windows Path环境变量中.

&nbsp;

测试安装是否成功：在命令行中输入

&nbsp;

mvn -version

&nbsp;

&nbsp;

安装Maven插件

安装Eclipse的Maven插件M2Eclipse。

&nbsp;

本文使用：

&nbsp;

&nbsp;

&nbsp;

JDK：SUN JDK1.6.0_03

Eclipse：3.3.1.1

&nbsp;

&nbsp;

M2Eclipse插件网址：http://m2eclipse.codehaus.org

&nbsp;

通过Eclipse在线更新网址：http://m2eclipse.codehaus.org/update/

&nbsp;

具体安装步骤见插件网址。

&nbsp;

为Maven设置Classpath变量，设置java>build path>classpath variables

&nbsp;

通过new…按钮增加一个变量条目：

&nbsp;

name：M2_REPO

&nbsp;

path：C:/Documents and Settings/zhangsan/.m2/repository，zhangsan是你的xp中的用户名

&nbsp;

创建Maven的Java项目并导入到Eclipse中

&nbsp;

在命令行中，进入eclipse的workspace目录下，输入：

&nbsp;

mvn archetype:create -DgroupId=org.marshal -DartifactId=helloworld

&nbsp;

其中：

&nbsp;

&nbsp;

&nbsp;

org.marshal是组织名称，另外maven自动生成了源代码的包org/marshal

helloworld是项目名称

&nbsp;

&nbsp;

运行命令后，workspace目录下生成helloworld目录，并生成：

&nbsp;

&nbsp;

&nbsp;

项目构建文件: pom.xml

代码框架：srcmainjavaorgmarshalhelloworldApp.java

测试代码：srctestjavaorgmarshalhelloworldAppTest.java

&nbsp;

&nbsp;

这时可以通过文本编辑器修改App.java源代码，并通过如下命令编译打包：

&nbsp;

maven pacage

&nbsp;

编写AppTest.java后，可通过下面命令运行JUnit测试：

&nbsp;

mvn test

&nbsp;

通过如下命令运行main方法：

&nbsp;

java -cp targethelloworld-1.0-SNAPSHOT.jar org.marshal.App

&nbsp;

不过，还是最好通过IDE工具编写和调试代码，这需要将maven项目导入为Eclipse项目。

&nbsp;

在helloworld目录下，运行下面命令，使项目支持eclipse：

&nbsp;

mvn eclipse:eclipse

&nbsp;

然后，打开Eclipse，通过File>import…，general>existing projects into workspace，将helloworld导入。

&nbsp;

导入后，如下图：

&nbsp;

&nbsp;

&nbsp;

创建maven Web项目并导入到Eclipse中。如果需要创建maven的web项目，在eclipse的workspace目录下，运行：

&nbsp;

mvn archetype:create -DgroupId=org.marshal -DartifactId=myweb -DarchetypeArtifactId=maven-archetype-webapp

&nbsp;

将创建名为myweb的web项目。

&nbsp;

为该项目增加eclipse WTP的支持，到myweb目录下，运行：

&nbsp;

mvn -Dwtpversion=1.0 eclipse:eclipse

&nbsp;

将该项目导入Eclipse，和上面java项目类似。

&nbsp;

使用M2Eclipse插件

安装M2Eclipse插件成功后，在Eclipse点击刚才创建的web项目或者java项目。

&nbsp;

鼠标右键，Maven>Enable dependency management，使m2eclipse插件对该项目生效。

&nbsp;

再次鼠标右键，选择Maven>add dependency，就可以通过网络增加需要的类库了。

&nbsp;

见下图：

&nbsp;

&nbsp;

&nbsp;

选中后，maven将自动下载该类库版本到本地，并且自动加入到eclipse类库中。