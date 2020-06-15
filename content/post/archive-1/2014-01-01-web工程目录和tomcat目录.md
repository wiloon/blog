---
title: JavaEE Web 工程／项目 目录结构
author: wiloon
type: post
date: 2014-01-01T14:16:26+00:00
url: /?p=6096
categories:
  - Uncategorized
tags:
  - Java

---
### Maven 标准目录结构

好的目录结构可以使开发人员更容易理解项目，为以后的维护工作也打下良好的基础。Maven2根据业界公认的最佳目录结构，为开发者提供了缺省的标准目录模板。Maven2的标准目录结构如下：

<table border="0">
  <tr>
    <td align="left">
      <tt>src/main/java</tt>
    </td>
    
    <td align="left">
      Application/Library sources
    </td>
  </tr>
  
  <tr>
    <td align="left">
      <tt>src/main/resources</tt>
    </td>
    
    <td align="left">
      Application/Library resources
    </td>
  </tr>
  
  <tr>
    <td align="left">
      <tt>src/main/webapp</tt>
    </td>
    
    <td align="left">
      Web application sources
    </td>
  </tr>
  
  <tr>
    <td align="left">
      <tt>src/test/java</tt>
    </td>
    
    <td align="left">
      Test sources
    </td>
  </tr>
  
  <tr>
    <td align="left">
      <tt>src/test/resources</tt>
    </td>
    
    <td align="left">
      Test resources
    </td>
  </tr>
  
  <tr>
    <td align="left">
      <tt>src/main/filters</tt>
    </td>
    
    <td align="left">
      Resource filter files
    </td>
  </tr>
  
  <tr>
    <td align="left">
      <tt>src/main/assembly</tt>
    </td>
    
    <td align="left">
      Assembly descriptors
    </td>
  </tr>
  
  <tr>
    <td align="left">
      <tt>src/main/config</tt>
    </td>
    
    <td align="left">
      Configuration files
    </td>
  </tr>
  
  <tr>
    <td align="left">
      <tt>src/main/scripts</tt>
    </td>
    
    <td align="left">
      Application/Library scripts
    </td>
  </tr>
  
  <tr>
    <td align="left">
      <tt>src/test/filters</tt>
    </td>
    
    <td align="left">
      Test resource filter files
    </td>
  </tr>
  
  <tr>
    <td align="left">
      <tt>src/site</tt>
    </td>
    
    <td align="left">
      Site
    </td>
  </tr>
  
  <tr>
    <td align="left">
      <tt>LICENSE.txt</tt>
    </td>
    
    <td align="left">
      Project&#8217;s license
    </td>
  </tr>
  
  <tr>
    <td align="left">
      <tt>NOTICE.txt</tt>
    </td>
    
    <td align="left">
      Notices and attributions required by libraries that the project depends on
    </td>
  </tr>
  
  <tr>
    <td align="left">
      <tt>README.txt</tt>
    </td>
    
    <td align="left">
      Project&#8217;s readme
    </td>
  </tr>
</table>

使用目录模板，可以使 pom.xml 更简洁。因为 Maven2 已经根据缺省目录，预定义了相关的动作，而无需人工的干预。以 resources 目录为例：

  * src/main/resources，负责管理项目主体的资源。在使用Maven2执行compile之后，这个目录中的所有文件及子目录，会复制到target/classes目录中，为以后的打包提供了方便。
  * src/test/resources，负责管理项目测试的资源。在使用Maven2执行test-compile之后，这个目录中的所有文件及子目录，会复制到target/test-classes目录中，为后续的测试做好了准备。

这些动作在 Maven1 中，是需要在 maven.xml 中使用<preGoal>或<postGoal>来完成的。如今，完全不需要在pom.xml中指定就能够自动完成。在src和test都使用resources，方便构建和测试，这种方式本就已是前人的经验。通过使用Maven2，使这个经验在开发团队中得到普及。

创建标准目录模板，可以通过如下命令：


  mvn archetype:create -DgroupId=com.codeline.commons -DartifactId=codelineCommons


groupId和artifactId的含义与Maven1中的含义一样，参数artifactId的值会作为项目根目录的名字。除了建立相应的目录之外，Maven2还会创建缺省的pom.xml。

Maven2也考虑到：不同类型的项目需要拥有不同的目录结构。如创建web项目，可以使用命令：


  mvn archetype:create -DgroupId=com.mycompany.app
-DartifactId=my-webapp
-DarchetypeArtifactId=maven-archetype-webapp


### 

在Eclipse中只要创建一个Dynamic Web Project，就可以根据创建向导创建出一个典型Java Web站点的目录结构。除非有特殊需要，在大多数情况下都没有必要修改这个目录结构，这也是Web容器的缺省目录结构，我们只要直接使用即可。一般的目录结构如下：

WebContent (站点根目录)

|&#8212;META-INF (META-INF文件夹)<http://www.wiloon.com/wordpress/?p=6102>

| |&#8212;MANIFEST.MF (MANIFEST.MF配置清单文件)

|&#8212;WEB-INF (WEB-INF文件夹)

| |&#8212;web.xml (站点配置web.xml)

| |&#8212;lib (第三方库文件夹)

| | |&#8212;*.jar (程序需要的jar包)

| |&#8212;classes (class文件目录)

| |&#8212;&#8230;*.class (class文件)

|&#8212;<userdir> (自定义的目录)

| |&#8212;\*.jsp,\*.js,\*.css，\*images (自定义的资源文件)

|&#8212;<userfiles> (自定义的资源文件)

1.WebRoot(WebContent)下是发布到服务器上的内容。

2.META-INF是工程自身相关的一些信息，元文件信息，通常由开发工具，环境自动生成。

3．文件web.xml：完成servlet在web容器的注册。web.xml是Web应用程序的部署描述文件，是用来给Web服务器解析并获取Web应用程序相关描述的。

不按照sun公司的规范做应用web程序的结构，web容器找不到，比如，xml文件写错了，启动tomcat的时候会报错

4．凡是客户端能访问的资源(\*.html,\*.jpg)必须跟WEB-INF在同一目录。即放在Web根目录下的资源，从客户端是可以通过URL地址直接访问。

5. 切忌：凡是WEB-INF里面的文件都不能被客户端直接访问(比如隐藏的信息)。WEB-INF目录下的资源对用户来说是不可见的，而对Web服务器来说则没有这样的限制。

例如在WEB-INF下的index.htm，客户端无法与对待其他文件夹内的信息一样，通过http://yourserver/yourwebapp/WEB-INF/index.htm访问。WEB-INF文件夹是禁止通过URL访问的。

6. 在WEB-INF目录的classes及lib子目录下，都可以存放Java类文件。在运行时，Servlet容器的类加载器先加载classes目录下的类，再加载lib目录下的JAR文件（Java类库的打包文件）中的类，jar包是许多class文件的集合。因此，如果两个目录下存在同名的类，classes目录下的类具有优先权。

Tomcat固定的目录结构

/bin

存放在Windows平台以及Linux平台上启动和关闭Tomat的脚本文件

/conf

存放Tomat服务器的各种配置文件， 其中最重要的文件是Server.xml

/server

包含3个子目录：classes,lib和webapps

/server/lib

存放Tomat服务器所需的Jar文件

/server/webapps

存放Tomat自带的两个Web应用：admin应用和manager应用

/common/lib

存放Tomat服务器以及所有Web应用都可以访问的Jar应用

/share/lib

存放所有Web应用都可以访问的Jar文件

/logs

存放Tomat的日志文件

/webapps

当发布Web应用时，默认情况下把Web应用文件放于此目录下

/work

Tomcat把由Jsp生成的Servlet放于此目录下

<http://www.cnblogs.com/haippy/archive/2012/07/05/2577233.html>

<http://blog.csdn.net/ystyaoshengting/article/details/6204886>