---
title: jetty-maven-plugin, jetty maven plugin
author: wiloon
type: post
date: 2018-03-06T07:10:51+00:00
url: /?p=11958
categories:
  - Uncategorized

---
### maven plugin<pre data-language=XML>

<code class="language-markup line-numbers">&lt;plugin&gt;
    &lt;groupId&gt;org.eclipse.jetty&lt;/groupId&gt;
    &lt;artifactId&gt;jetty-maven-plugin&lt;/artifactId&gt;
    &lt;version&gt;9.4.6.v20170531&lt;/version&gt;
    &lt;configuration&gt;
        &lt;stopKey&gt;stop&lt;/stopKey&gt;
        &lt;stopPort&gt;5599&lt;/stopPort&gt;
        &lt;webApp&gt;
            &lt;contextPath&gt;/app0&lt;/contextPath&gt;
            &lt;defaultsDescriptor&gt;src/main/resources/webdefault.xml&lt;/defaultsDescriptor&gt;
        &lt;/webApp&gt;
        &lt;scanIntervalSeconds&gt;2&lt;/scanIntervalSeconds&gt;

        &lt;httpConnector&gt;
            &lt;port&gt;8081&lt;/port&gt;
        &lt;/httpConnector&gt;
    &lt;/configuration&gt;
&lt;/plugin&gt;
``` 

### webdefault.xml

可以去maven的本地仓库找到
  
.m2\repository\org\eclipse\jetty\jetty-webapp\9.4.20.v20190813
  
解压后在这里可以找到webdefault.xml
  
jetty-webapp-9.4.20.v20190813\org\eclipse\jetty\webapp

### run

```bashmvn jetty:run
mvnDebug jetty:run
# 默认调试端口8000
```

## debug &#8211; mvnDebug

<https://blog.wiloon.com/?p=15212>

mvnDebug -suspend默认为n,

http://www.blogjava.net/fancydeepin/archive/2015/06/23/maven-jetty-plugin.html
  
https://my.oschina.net/jackieyeah/blog/524556
  
https://stackoverflow.com/questions/7875002/setting-debug-configuration-for-mavenjettyeclipse