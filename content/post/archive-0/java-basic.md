---
title: java basic
author: "-"
type: post
date: 2011-09-06T05:33:25+00:00
url: /?p=676

---
# java basic
### 查看 openjdk 版本
http://openjdk.java.net/projects/jdk/

### install
#### archlinux
    sudo pacman -S 	jdk-openjdk
    sudo pacman -S 	openjdk-src

### 切换jdk版本
    archlinux-java help
    archlinux-java status
    archlinux-java set  java-14-openjdk

### 查看当前 java 版本
    java -version
    sudo archlinux-java status


```java
    //java getResource

    URL url= Thread.currentThread().getContextClassLoader().getResource("XXX");

    String fileName = this.getClass().getClassLoader().getResource("文件名").getPath();//获取文件路径
    String fileUtl = this.getClass().getResource("文件名").getFile();
    （在项目打成jar后的情况下getPath()与getFile()返回参数及用法的基本相同具体差异大研究) 
    示例路径结果: /E:/idea_work/sofn-qry-web/target/classes/CityJson.js

    //console read

    System.in.read();
```
    


方式一: 
String fileName = this.getClass().getClassLoader().getResource("文件名").getPath();//获取文件路径
String fileUtl = this.getClass().getResource("文件名").getFile();
（在项目打成jar后的情况下getPath()与getFile()返回参数及用法的基本相同具体差异大研究) 
示例路径结果: /E:/idea_work/sofn-qry-web/target/classes/CityJson.js

方式二: 
File directory = new File("");//参数为空
String courseFile = directory.getCanonicalPath()//标准的路径 ;
String author =directory.getAbsolutePath()//绝对路径;
（在jdk1.1后就有了此方法获取文件路径的方式存在了) 
示例路径结果: E:\idea_work\sofn-qry-web

方式三: 
java.net.URL uri = this.getClass().getResource("/");
（获取到Class文件存放的路径) 
示例路径结果: file:/E:/idea_work/sofn-qry-web/target/test-classes/


String property =System.getProperty("user.dir");
方式四: 

String property =System.getProperty("user.dir");
（此方法可以得到该工程项目所有文件的相关路径及环境配置信息) 
示例输出结果: 

### /usr/lib/jvm/java-8-openjdk-amd64/jre/lib/ext/libatk-wrapper.so
Java ATK Wrapper is a implementation of ATK by using JNI technic.
It converts Java Swing events into ATK events, and sends these events to
ATK-Bridge.
https://developer.gnome.org/accessibility-devel-guide/stable/dev-start-5.html.zh_CN

https://blog.csdn.net/oschina_40188932/article/details/78833754
