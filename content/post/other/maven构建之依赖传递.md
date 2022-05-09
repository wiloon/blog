---
title: Maven构建之依赖传递
author: "-"
date: 2014-05-28T02:30:40+00:00
url: /?p=6672
categories:
  - Inbox
tags:
  - Maven

---
## Maven构建之依赖传递
<http://a123159521.iteye.com/blog/774322>

博客分类:  Maven
  
mavenjunit项目管理配置管理Apache
  
如果断Maven的依赖构建必须每一个项目都指定,那配置是累死人了,比如A依赖了20个项目,B依赖A,那么还要添加20个项目,那就悲剧了,maven有依赖传递的功能。
  
1. Transitive Dependency (传递依赖)
  
你的项目依赖于A,A又依赖于B。你的项目是否要声明你依赖于B？ Maven的回答是它帮你自动管理这种依赖的传递,你不需要声明你依赖于B,由Maven来做。
  
[版本还是要自己指定的.]
  
2. Dependency Scope  (依赖范围)
  
因此,Maven考虑了6中可能的scope供选择:
  
- compile: 默认的scope。编译、测试、打包全都需要。compile参与依赖传递,就是说,你的项目A依赖于B(依赖scope是compile),项目C依赖于你的项目A,那么C也就依赖于B。
  
- provided: 表示JDK或者容器会在Runtime时提供这些(jar),如上面说到的servlet api。provided的东西在编译和测试时会用到,不参与传递依赖。
  
- runtime: 表示编译时不需要,但测试和运行时需要,最终打包时会包含进去。
  
- test: 只用于测试阶段 (测试的编译和测试的运行) ,典型的就是junit的jar。
  
- system: 和provided类似,但要求jar是你的系统里已有的,不会在repository里找,如rt.jar,tools.jar这些。
  
- import: 简单的说,你的项目的pom可以继承另一个项目的pom,从而继承了父项目的依赖关系,但是因为之后single inheritance的限制,所以创造了import,使得你可以"导入"或者说"继承"任何一到多个项目的依赖关系。
  
3. 依赖管理(dependencyManagement)
  
实际的项目中,你会有一大把的Maven模块,而且你往往发现这些模块有很多依赖是完全项目的,A模块有个对spring的依赖,B模块也有,它们的依赖配置一模一样,同样的groupId, artifactId, version,或者还有exclusions, classifer。细心的分会发现这是一种重复,重复就意味着潜在的问题,Maven提供的dependencyManagement就是用来消除这种重复的。

为了实现项目间的依赖,一般情况下,web项目依赖于app项目,而app项目很可能依赖于其他的app项目,比如我建了一个util项目,app依赖于util,那么webapp也需要依赖于util,但是我不配置webapp依赖util,验证一下,会不会自动加载依赖包.

util项目的构建请参照前讲,接下来看maven配置:
  
util配置;
  
Java代码 收藏代码
  
<?xml version="1.0" encoding="UTF-8"?>
  
<project xsi:schemaLocation="<http://maven.apache.org/POM/4.0.0> <http://maven.apache.org/xsd/maven-4.0.0.xsd>" xmlns="http://maven.apache.org/POM/4.0.0"
  
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  
<modelVersion>4.0.0</modelVersion>
  
<parent>
  
demo</artifactId>
  
<groupId>com.test</groupId>
  
<version>1.0.0-SNAPSHOT</version>
  
</parent>
  
<groupId>com.test.util</groupId>
  
util</artifactId>
  
<version>1.0-SNAPSHOT</version>
  
<name>util</name>
  
<url><http://maven.apache.org></url>

<build>
  
<plugins>
  
<plugin>
  
<groupId>org.apache.maven.plugins</groupId>
  
maven-compiler-plugin</artifactId>
  
<configuration>
  
<source>1.6</source>
  
<target>1.6</target>
  
</configuration>
  
</plugin>
  
</plugins>
  
</build>

<dependencies>
  
<dependency>
  
<groupId>junit</groupId>
  
junit</artifactId>
  
<version>3.8.1</version>
  
<scope>test</scope>
  
</dependency>
  
</dependencies>
  
<properties>
  
<project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  
</properties>
  
</project>

app项目的maven配置:
  
Java代码 收藏代码
  
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  
xsi:schemaLocation="<http://maven.apache.org/POM/4.0.0> <http://maven.apache.org/xsd/maven-4.0.0.xsd>">
  
<modelVersion>4.0.0</modelVersion>
  
<parent>
  
<groupId>com.test</groupId>
  
demo</artifactId>
  
<version>1.0.0-SNAPSHOT</version>
  
</parent>

<groupId>com.test.app</groupId>
  
app</artifactId>
  
<version>1.0-SNAPSHOT</version>
  
<packaging>jar</packaging>

<name>app</name>
  
<url><http://maven.apache.org></url>

<build>
  
<plugins>
  
<plugin>
  
<groupId>org.apache.maven.plugins</groupId>
  
maven-compiler-plugin</artifactId>
  
<configuration>
  
<source>1.6</source>
  
<target>1.6</target>
  
</configuration>
  
</plugin>
  
</plugins>
  
</build>

<dependencies>

<dependency>
  
<groupId>com.test.util</groupId>
  
util</artifactId>
  
</dependency>

<dependency>
  
<groupId>junit</groupId>
  
junit</artifactId>
  
</dependency>

</dependencies>
  
</project>

webapp的maven配置:
  
Java代码 收藏代码
  
<project xmlns="http://maven.apache.org/POM/4.0.0"
  
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  
xsi:schemaLocation="<http://maven.apache.org/POM/4.0.0> <http://maven.apache.org/maven-v4_0_0.xsd>">
  
<modelVersion>4.0.0</modelVersion>
  
<parent>
  
<groupId>com.test</groupId>
  
demo</artifactId>
  
<version>1.0.0-SNAPSHOT</version>
  
</parent>
  
<groupId>com.test.app</groupId>
  
webapp</artifactId>
  
<packaging>war</packaging>
  
<version>1.0-SNAPSHOT</version>
  
<name>webapp Maven Webapp</name>
  
<url><http://maven.apache.org></url>

<build>
  
<finalName>webapp</finalName>
  
<plugins>
  
<plugin>
  
<groupId>org.apache.maven.plugins</groupId>
  
maven-compiler-plugin</artifactId>
  
<configuration>
  
<source>1.6</source>
  
<target>1.6</target>
  
</configuration>
  
</plugin>
  
<!-
  
<plugin>
  
<groupId>org.codehaus.mojo</groupId>
  
tomcat-maven-plugin</artifactId>
  
<configuration>
  
<url><http://127.0.0.1:9001/manager></url>
  
<server>test</server>
  
<path>/</path>
  
</configuration>
  
</plugin>
  
->
  
</plugins>
  
</build>

<dependencies>

<dependency>
  
<groupId>com.test.app</groupId>
  
app</artifactId>
  
</dependency>

<dependency>
  
<groupId>javax.servlet</groupId>
  
servlet-api</artifactId>
  
</dependency>

<dependency>
  
<groupId>junit</groupId>
  
junit</artifactId>
  
</dependency>

</dependencies>

</project>

不禁发现,当app项目添加了一个项目依赖和webapp一点关系都没有,因为maven有依赖传递的功能,不过要注意冲突就好了.
  
外面总文件的配置;
  
Java代码 收藏代码
  
<?xml version="1.0" encoding="UTF-8"?>
  
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">

<modelVersion>4.0.0</modelVersion>
  
<groupId>com.test</groupId>
  
demo</artifactId>
  
<packaging>pom</packaging>
  
<version>1.0.0-SNAPSHOT</version>
  
<name>CE Maven Demo</name>

<modules>
  
<module>app</module>
  
<module>webapp</module>
  
<module>util</module>
  
</modules>

<dependencyManagement>
  
<!-webx-3.0 related->
  
<dependencies>
  
<dependency>
  
<groupId>com.test.util</groupId>
  
util</artifactId>
  
<version>1.0-SNAPSHOT</version>
  
</dependency>

<dependency>
  
<groupId>com.test.app</groupId>
  
app</artifactId>
  
<version>1.0-SNAPSHOT</version>
  
</dependency>

<dependency>
  
<groupId>com.test.app</groupId>
  
webapp</artifactId>
  
<version>1.0-SNAPSHOT</version>
  
</dependency>

<dependency>
  
<groupId>javax.servlet</groupId>
  
servlet-api</artifactId>
  
<version>2.4</version>
  
<scope>provided</scope>
  
</dependency>

<dependency>
  
<groupId>junit</groupId>
  
junit</artifactId>
  
<version>3.8.1</version>
  
<scope>test</scope>
  
</dependency>

</dependencies>
  
</dependencyManagement>
  
</project>
  
这种管理方式真的是very perfect,从版本,依赖,打包,构建等等都非常的到位
