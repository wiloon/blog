---
title: Eclipse .classpath
author: "-"
date: 2012-05-27T06:08:06+00:00
url: /?p=3258
categories:
  - Java
tags:$
  - reprint
---
## Eclipse .classpath

  <classpathentry exported="true" kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER"/>


  
    每个新建java工程(Project)都默认存在的。
  
  
    <classpathentry kind="src" ōutput="km230/apitest/classes" path="km230/apitest/src"/>
 指定源文件位置, 对应工程属性Java build path中Source项中的一项, kind="src" 指明为源文件,
 源文件路径path, output为这条路径中源文件编译以后class文件的输出路径。
  
  
    <classpathentry kind="src" path="km230batch/src"/>
 指定源文件位置, 对应工程属性Java build path中Source项中的一项, kind="src" 指明为源文件,
 源文件路径path, 编译以后class文件的输出路径为默认输出路径。
  
  
    <classpathentry kind="output" path="km230server/approot/WEB-INF/classes"/>
 指定编译以后class文件的默认输出路径, 对应工程属性Java build path中Source项中的default output path,
 kind="output"指明为默认class输出路径, path为相应输出路径。
 注意: 这一条在文件中有且只能有一条(不可能同时出现两个默认吧?).
  
  
    <classpathentry kind="lib" path="km230/lib/Notes.jar"/>
 指定工程所用到的库文件或目录, 对应工程属性Java build path中Libraries项中的一项,
 kind="lib"指明为库文件或目录, path为库文件或目录位置。
 注意: 当指定库文件时(非库目录, 通常是jar包, 好像zip也可以, 不知道是否还有其它), 应当包含文件名。
  
  
    <classpathentry kind="var" path="JUNIT_HOME/junit.jar" sourcepath="ECLIPSE_HOME/plugins/org.eclipse.jdt.source_3.0.0/src/org.junit_3.8.1/junitsrc.zip"/>
 指定工程所用到的库文件或目录, 对应工程属性Java build path中Libraries项中的一项,
 kind="var"指明带有全局编译路径中设置的变量(Window->Prefrences->Java->Build Path->Classpath Variables),
 如上面的ECLIPSE_HOME, path为这个变量目录下的库文件(同样通常是jar包, 好像zip也可以, 也不知道是否还有其它)。
  
  
    <classpathentry excluding="**" kind="src" output="target/classes" path="src/main/resources"/>
  
  
    Since you are using m2eclipse, the .project file in your project contains
  
  <buildCommand> <name>org.maven.ide.eclipse.maven2Builder</name>  </arguments> </buildCommand> ```
  
    This is overriding the Java builder, and copying the folders in /src/main/resources into the /target/classes directory.
  
  
    If you were to remove the above build command, and clean your project, the files in /src/main/resources should go away. If you add in the build command, your files should reappear.
  
  
    I realize this doesn't answer the stated question of what excluding="**" does, but this explains the behavior your are seeing.
  
  
    <classpathentry excluding="*.txt" kind="src" path="src"/> king表示的是种类，path是路径
  
  
    king="src"表示path所指的目录下的是源码
  
  
    king="con"表示是eclipse的jar包，
  
  
    king="lib"表示是我们开发者在项目中使用的第三方jar包
  
  
    king="var"表示的也是开发者项目使用的jar包,和lib不同的是var的路径中有JAVA_HOME这样的在classpath中定义了的，而lib的路径是使用的绝对路径，比如c:/myjar/jdbc.jar
  
  
    king= "output" 表示编译的class输出的路径。
  
  
    excluding表示该path下的符合excluding后面的值的文件不被包含在classpath下，
  
  
    http://jinguo.iteye.com/blog/716693
  
  
    http://stackoverflow.com/questions/3630460/eclipse-classpath-exlusion-pattern
  
  
    http://yangblog.iteye.com/blog/949131
  
