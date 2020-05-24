---
title: Eclipse .classpath
author: wiloon
type: post
date: 2012-05-27T06:08:06+00:00
url: /?p=3258
categories:
  - Java

---
<div>
  <classpathentry exported=&#8221;true&#8221; kind=&#8221;con&#8221; path=&#8221;org.eclipse.jdt.launching.JRE_CONTAINER&#8221;/>
</div>

<div id="blog_content">
  <p>
    每个新建java工程(Project)都默认存在的。
  </p>
  
  <p>
    <classpathentry kind=&#8221;src&#8221; ōutput=&#8221;km230/apitest/classes&#8221; path=&#8221;km230/apitest/src&#8221;/><br /> 指定源文件位置, 对应工程属性Java build path中Source项中的一项, kind=&#8221;src&#8221; 指明为源文件,<br /> 源文件路径path, output为这条路径中源文件编译以后class文件的输出路径。
  </p>
  
  <p>
    <classpathentry kind=&#8221;src&#8221; path=&#8221;km230batch/src&#8221;/><br /> 指定源文件位置, 对应工程属性Java build path中Source项中的一项, kind=&#8221;src&#8221; 指明为源文件,<br /> 源文件路径path, 编译以后class文件的输出路径为默认输出路径。
  </p>
  
  <p>
    <classpathentry kind=&#8221;output&#8221; path=&#8221;km230server/approot/WEB-INF/classes&#8221;/><br /> 指定编译以后class文件的默认输出路径, 对应工程属性Java build path中Source项中的default output path,<br /> kind=&#8221;output&#8221;指明为默认class输出路径, path为相应输出路径。<br /> 注意: 这一条在文件中有且只能有一条(不可能同时出现两个默认吧?).
  </p>
  
  <p>
    <classpathentry kind=&#8221;lib&#8221; path=&#8221;km230/lib/Notes.jar&#8221;/><br /> 指定工程所用到的库文件或目录, 对应工程属性Java build path中Libraries项中的一项,<br /> kind=&#8221;lib&#8221;指明为库文件或目录, path为库文件或目录位置。<br /> 注意: 当指定库文件时(非库目录, 通常是jar包, 好像zip也可以, 不知道是否还有其它), 应当包含文件名。
  </p>
  
  <p>
    <classpathentry kind=&#8221;var&#8221; path=&#8221;JUNIT_HOME/junit.jar&#8221; sourcepath=&#8221;ECLIPSE_HOME/plugins/org.eclipse.jdt.source_3.0.0/src/org.junit_3.8.1/junitsrc.zip&#8221;/><br /> 指定工程所用到的库文件或目录, 对应工程属性Java build path中Libraries项中的一项,<br /> kind=&#8221;var&#8221;指明带有全局编译路径中设置的变量(Window->Prefrences->Java->Build Path->Classpath Variables),<br /> 如上面的ECLIPSE_HOME, path为这个变量目录下的库文件(同样通常是jar包, 好像zip也可以, 也不知道是否还有其它)。
  </p>
  
  <p>
    <classpathentry excluding=&#8221;**&#8221; kind=&#8221;src&#8221; output=&#8221;target/classes&#8221; path=&#8221;src/main/resources&#8221;/>
  </p>
  
  <p>
    Since you are using m2eclipse, the .project file in your project contains
  </p>
  
  <pre><code>&lt;buildCommand&gt; &lt;name&gt;org.maven.ide.eclipse.maven2Builder&lt;/name&gt; &lt;arguments&gt; &lt;/arguments&gt; &lt;/buildCommand&gt; ```
  
  <p>
    This is overriding the Java builder, and copying the folders in /src/main/resources into the /target/classes directory.
  </p>
  
  <p>
    If you were to remove the above build command, and clean your project, the files in /src/main/resources should go away. If you add in the build command, your files should reappear.
  </p>
  
  <p>
    I realize this doesn&#8217;t answer the stated question of what excluding=&#8221;**&#8221; does, but this explains the behavior your are seeing.
  </p>
  
  <p>
    <classpathentry excluding=&#8221;*.txt&#8221; kind=&#8221;src&#8221; path=&#8221;src&#8221;/> king表示的是种类，path是路径
  </p>
  
  <p>
    king=&#8221;src&#8221;表示path所指的目录下的是源码
  </p>
  
  <p>
    king=&#8221;con&#8221;表示是eclipse的jar包，
  </p>
  
  <p>
    king=&#8221;lib&#8221;表示是我们开发者在项目中使用的第三方jar包
  </p>
  
  <p>
    king=&#8221;var&#8221;表示的也是开发者项目使用的jar包,和lib不同的是var的路径中有JAVA_HOME这样的在classpath中定义了的，而lib的路径是使用的绝对路径，比如c:/myjar/jdbc.jar
  </p>
  
  <p>
    king= &#8220;output&#8221; 表示编译的class输出的路径。
  </p>
  
  <p>
    excluding表示该path下的符合excluding后面的值的文件不被包含在classpath下，
  </p>
  
  <p>
    <a href="http://jinguo.iteye.com/blog/716693">http://jinguo.iteye.com/blog/716693</a>
  </p>
  
  <p>
    <a href="http://stackoverflow.com/questions/3630460/eclipse-classpath-exlusion-pattern">http://stackoverflow.com/questions/3630460/eclipse-classpath-exlusion-pattern</a>
  </p>
  
  <p>
    <a href="http://yangblog.iteye.com/blog/949131">http://yangblog.iteye.com/blog/949131</a>
  </p>
</div>