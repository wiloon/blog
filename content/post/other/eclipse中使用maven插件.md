---
title: Eclipse中使用Maven插件
author: "-"
date: 2013-10-20T04:58:58+00:00
url: /?p=5855
categories:
  - Uncategorized
tags:
  - Maven

---
## Eclipse中使用Maven插件
安装Maven

下载Maven最新版本,见: http://maven.apache.org/download.html


当前版本2.0.7。解压缩下载的文件, 将其中的bin目录设置到windows Path环境变量中.


测试安装是否成功: 在命令行中输入


mvn -version

安装Maven插件

安装Eclipse的Maven插件M2Eclipse。


本文使用: 


JDK: SUN JDK1.6.0_03

Eclipse: 3.3.1.1

M2Eclipse插件网址: http://m2eclipse.codehaus.org


通过Eclipse在线更新网址: http://m2eclipse.codehaus.org/update/


具体安装步骤见插件网址。


为Maven设置Classpath变量,设置java>build path>classpath variables


通过new…按钮增加一个变量条目: 


name: M2_REPO


path: C:/Documents and Settings/zhangsan/.m2/repository,zhangsan是你的xp中的用户名


创建Maven的Java项目并导入到Eclipse中


在命令行中,进入eclipse的workspace目录下,输入: 


mvn archetype:create -DgroupId=org.marshal -DartifactId=helloworld


其中: 


org.marshal是组织名称,另外maven自动生成了源代码的包org/marshal

helloworld是项目名称

运行命令后,workspace目录下生成helloworld目录,并生成: 


项目构建文件: pom.xml

代码框架: srcmainjavaorgmarshalhelloworldApp.java

测试代码: srctestjavaorgmarshalhelloworldAppTest.java

这时可以通过文本编辑器修改App.java源代码,并通过如下命令编译打包: 


maven pacage


编写AppTest.java后,可通过下面命令运行JUnit测试: 


mvn test


通过如下命令运行main方法: 


java -cp targethelloworld-1.0-SNAPSHOT.jar org.marshal.App


不过,还是最好通过IDE工具编写和调试代码,这需要将maven项目导入为Eclipse项目。


在helloworld目录下,运行下面命令,使项目支持eclipse: 


mvn eclipse:eclipse


然后,打开Eclipse,通过File>import…,general>existing projects into workspace,将helloworld导入。


导入后,如下图: 


创建maven Web项目并导入到Eclipse中。如果需要创建maven的web项目,在eclipse的workspace目录下,运行: 


mvn archetype:create -DgroupId=org.marshal -DartifactId=myweb -DarchetypeArtifactId=maven-archetype-webapp


将创建名为myweb的web项目。


为该项目增加eclipse WTP的支持,到myweb目录下,运行: 


mvn -Dwtpversion=1.0 eclipse:eclipse


将该项目导入Eclipse,和上面java项目类似。


使用M2Eclipse插件

安装M2Eclipse插件成功后,在Eclipse点击刚才创建的web项目或者java项目。


鼠标右键,Maven>Enable dependency management,使m2eclipse插件对该项目生效。


再次鼠标右键,选择Maven>add dependency,就可以通过网络增加需要的类库了。


见下图: 


选中后,maven将自动下载该类库版本到本地,并且自动加入到eclipse类库中。