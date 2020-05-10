---
title: 当装了两个tomcat后，修改tomcat端口
author: wiloon
type: post
date: 2012-05-13T10:49:12+00:00
url: /?p=3112
categories:
  - Java
  - Web
tags:
  - Tomcat

---
<div>
  <strong><a href="http://zfsn.iteye.com/blog/669901">http://zfsn.iteye.com/blog/669901</a></strong></p> 
  
  <div>
  </div>
</div>

<div id="blog_content">
  <p>
    修改Tomcat的端口号：
  </p>
  
  <p>
    在默认情况下，tomcat的端口是8080，如果出现8080端口号冲突，用如下方法可以修改Tomcat的端口号：
  </p>
  
  <p>
    首先： 在Tomcat的根（安装）目录下，有一个conf文件夹，双击进入conf文件夹，在里面找到Server.xml文件，打开该文件。
  </p>
  
  <p>
    其次：在文件中找到如下文本：<br /> <Connector port=&#8221;8080&#8243; protocol=&#8221;HTTP/1.1&#8243;<br /> maxThreads=&#8221;150&#8243; connectionTimeout=&#8221;20000&#8243;<br /> redirectPort=&#8221;8443&#8243; /><br /> 也有可能是这样的：<br /> <Connector port=&#8221;8080&#8243; maxThreads=&#8221;150&#8243; minSpareThreads=&#8221;25&#8243; maxSpareThreads=&#8221;75&#8243; enableLookups=&#8221;false&#8221; redirectPort=&#8221;8443&#8243; acceptCount=&#8221;100&#8243; debug=&#8221;0&#8243; connectionTimeout=&#8221;20000&#8243;<br /> disableUploadTimeout=&#8221;true&#8221; />等等；<br /> 最后：将port=&#8221;8080&#8243;改为其它的就可以了。如port=&#8221;8081&#8243;等。<br /> 保存server.xml文件，重新启动Tomcat服务器，Tomcat就可以使用8081端口了。
  </p>
  
  <p>
    注意，有的时候要使用两个tomcat，那么就需要修改其中的一个的端口号才能使得两个同时工作。
  </p>
  
  <p>
    修改了上面的以后，还要修改两处：<br /> （1）将 <Connector port=&#8221;8009&#8243; enableLookups=&#8221;false&#8221; redirectPort=&#8221;8443&#8243; debug=&#8221;0&#8243;<br /> protocol=&#8221;AJP/1.3&#8243; />的8009改为其它的端口。
  </p>
  
  <p>
    （2） 继续将<Server port=&#8221;8005&#8243; shutdown=&#8221;SHUTDOWN&#8221; debug=&#8221;0&#8243;>的8005改为其它的端口。<br /> 经过以上3个修改，应该就可以了。
  </p>
  
  <p>
    8443
  </p>
</div>