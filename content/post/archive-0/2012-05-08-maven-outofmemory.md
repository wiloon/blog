---
title: Maven OutOfMemory
author: wiloon
type: post
date: 2012-05-08T03:34:21+00:00
url: /?p=3094
categories:
  - Uncategorized

---
<div>
  <h3>
    <a href="http://juvenshun.iteye.com/blog/240257">http://juvenshun.iteye.com/blog/240257</a>
  </h3>
</div>

<div id="blog_content">
  <p>
    当Maven项目很大，或者你运行诸如 mvn site 这样的命令的时候，maven运行需要很大的内存，在默认配置下，就可能遇到java的堆溢出。如：
  </p>
  
  <div>
  </div>
  
  <div>
    [INFO] Building jar: /home/dl9pf/svn/mindquarry/mindquarry-jcr/mindquarry-jcr-changes/target/mindquarry-migration-with-dependencies.jar<br /> [INFO] &#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;<br /> [ERROR] FATAL ERROR<br /> [INFO] &#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;<br /> [INFO] Java heap space<br /> [INFO] &#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;<br /> [INFO] Trace<br /> java.lang.OutOfMemoryError: Java heap space<br /> at java.lang.AbstractStringBuilder.expandCapacity(AbstractStringBuilder.java:99)<br /> at java.lang.AbstractStringBuilder.append(AbstractStringBuilder.java:518)<br /> &#8230;<br /> at org.codehaus.classworlds.Launcher.launchEnhanced(Launcher.java:315)<br /> at org.codehaus.classworlds.Launcher.launch(Launcher.java:255)<br /> at org.codehaus.classworlds.Launcher.mainWithExitCode(Launcher.java:430)<br /> at org.codehaus.classworlds.Launcher.main(Launcher.java:375)<br /> [INFO] &#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;<br /> [INFO] Total time: 7 minutes 14 seconds<br /> [INFO] Finished at: Wed Sep 05 07:44:55 CEST 2007<br /> [INFO] Final Memory: 37M/63M<br /> [INFO] &#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;
  </div>
  
  <p>
    解决的方法是调整java的堆大小的值。
  </p>
  
  <h2>
    Windows环境中
  </h2>
  
  <p>
    <strong></strong><strong>找到文件<em>%M2_HOME%binmvn.bat</em> ，这就是启动Maven的脚本文件，在该文件中你能看到有一行注释为：</strong>
  </p>
  
  <p>
    @REM set MAVEN_OPTS=-Xdebug -Xnoagent -Djava.compiler=NONE&#8230;
  </p>
  
  <p>
    它的意思是你可以设置一些Maven参数，我们就在注释下面加入一行：
  </p>
  
  <div>
  </div>
  
  <div>
    set MAVEN_OPTS= -Xms128m -Xmx512m
  </div>
  
  <p>
    之后，当你运行Maven命令如 mvn -version 的时候，你会看到如下的输出：
  </p>
  
  <div>
  </div>
  
  <div>
    E:test>mvn -versionE:test>set MAVEN_OPTS= -Xms128m -Xmx512m<br /> Maven version: 2.0.9<br /> Java version: 1.6.0_07<br /> OS name: "windows 2003&#8221; version: "5.2&#8221; arch: "x86&#8221; Family: "windows&#8221;</p>
  </div>
  
  <p>
    我们看到，配置的Maven选项生效了，OutOfMemoryError也能得以相应的解决。
  </p>
  
  <h2>
    <strong>Linux环境中</strong>
  </h2>
  
  <p>
    <strong></strong><strong>也可以通过设置环境变量解决该问题， 如，编辑文件<em> /etc/profile</em> 如下</strong>
  </p>
  
  <div>
  </div>
  
  <div>
    MAVEN_OPTS=-Xmx512m<br /> export JAVA_HOME MAVEN_HOME MAVEN_OPTS JAVA_BIN PATH CLASSPATH
  </div>
  
  <h2>
    <strong>如果你使用Hudson</strong>
  </h2>
  
  <p>
    用 Hudson + Maven做持续集成，并不幸也遇到了类似的错误，那么上述两种方式都将不再起作用了，因为Hudson使用自己的maven-agent来启动Maven，不会去调用Maven的脚本，自然相应的配置也就无效了。
  </p>
  
  <p>
    好在Hudson也给为我们提供了配置点，在Hudson的项目配置页面中，有一块Build区域，这里我们已经设置了Root Pom和Goals。注意该区域的右下角有一个&#8221;Advanced&#8230;&#8221;按钮，点击会看到JVM Options输入框，这里输入&#8221;-Xmx1024m&#8221;就OK了。
  </p>
  
  <h2>
    m2eclipse中
  </h2>
  
  <p>
    类似以上的方法都会失效，所幸m2eclipse提供了配置点。步骤如下：
  </p>
  
  <p>
    项目上右击 -> Run As -> Run Configurations -> Maven Build 上右击 -> New
  </p>
  
  <p>
    这时会看到一个maven运行配置对话框，这里面其它的配置我不多解释了，为了解决内存溢出的问题，我们可以选择第二个TAB: JRE，然后在VM arguments中输入配置如：-Xms128m -Xmx512m。
  </p>
</div>