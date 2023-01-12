---
title: mvn, maven basic
author: "-"
date: 2011-09-29T04:34:14+00:00
url: maven/basic
categories:
  - Java
tags:
  - maven
---
## mvn, maven basic

```bash
# 打印当前在使用的 settings
mvn help:effective-settings
```

### download

<https://maven.apache.org/download.cgi>

### setting>mirror

<https://developer.aliyun.com/mirror/maven>

<https://repo.maven.apache.org/maven2>

### Maven 参数

```p
-D 传入属性参数
-P 使用pom中指定的配置
-e 显示maven运行出错的信息
-o 离线执行命令,即不去远程仓库更新包
-X 显示maven允许的debug信息
-U 强制去远程参考更新snapshot包
-q for only error
```

### 参数> properties

对应一个变量值，pom.xml里面配置的有，那么如果你在命令行中 以 -Dmy.filter.value=1 的格式去配置mvn命令，那么将覆盖你pom中的值。

```bash
mvn clean -Ptrip-app,daily package -Dmy.filter.value=1 -Dttidapk.ttids=21xx00
```

```xml
<project>
  <properties>
    <my.filter.value>hello</my.filter.value>
  </properties>
</project>
```

<https://blog.csdn.net/Maxiao1204/article/details/90510176>

### command

```bash
# skip test, 强制更新依赖包
  mvn -Dmaven.test.skip=true clean package -U
```

### 生成项目

```bash
# common project
# mvn archetype:generate 会自动创建项目目录 mvntest
mvn archetype:generate -DgroupId=com.wiloon.demo -DartifactId=project0 \
-DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false

# archetypeVersion 指定版本号
mvn archetype:generate -D groupId=com.wiloon.java -D artifactId=javaJpms \
-D archetypeVersion=1.4 -D archetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false

# local catalog
mvn archetype:generate -DgroupId=com.wiloon.test -DartifactId=mvntest \
-DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false -DarchetypeCatalog=local

# web project
mvn archetype:generate -DgroupId=com.wiloon.mail.web -DartifactId=mailTestWeb \
-DarchetypeArtifactId=maven-archetype-webapp -DinteractiveMode=false
```

```bash
mvn clean compile -Dmaven.test.skip=true org.apache.maven.plugins:maven-war-plugin:exploded -q
mvn clean compile -Dmaven.test.skip=true org.apache.maven.plugins:maven-war-plugin:exploded -U
#-U,--update-snapshots                  Forces a check for missing                                        releases and updated snapshots on
mvn clean compile -U
# 指定执行某一个类的测试
mvn -Dtest=com.wiloon.Foo test

```

### 检测包冲突

```bash
mvn dependency:help
mvn dependency:analyze
mvn dependency:tree
mvn dependency:tree -Dverbose
```

### upload jar to nexus

```bash
mvn deploy:deploy-file -Dfile=xxx.pom -DgroupId=com.wiloon -DartifactId=artifactid0 -Dversion=1.0.0 -Dpackaging=pom -DrepositoryId=repo0 -Durl=https://maven.wiloon.com/repository/snapshot/

mvn deploy:deploy-file -Dfile=xxx.jar -DgroupId=com.wiloon -DartifactId=artifactid0 -Dversion=1.0.0 -Dpackaging=jar -DrepositoryId=repo0 -Durl=https://maven.wiloon.net/repository/snapshot/
```

## maven ojdbc6

```bash
mvn install:install-file -DgroupId=com.oracle -DartifactId=ojdbc6 -Dversion=11.2.0.3 -Dpackaging=jar -Dfile=/home/wiloon/Downloads/ojdbc6.jar

```

```bash
#maven war plugin
mvn clean compile -Dmaven.test.skip=true org.apache.maven.plugins:maven-war-plugin:exploded

# maven-assembly-plugin 打包
>wangyue.dev/maven/assembly/plugin

#Generates JSW based daemon wrappers.
mvn appassembler:generate-daemons 

mvn -v
mvn -version

mvn install

mvn install -Dmaven.test.skip=true

#wrapper
mvn package appassembler:assemble
```

### 查看mvn 参数

```bash
mvn --help
# 指定pom文件位置
mvn -f trunk/mvntest/pom.xml install
```

```bash
mvn archetype:generate
#390 maven-archetype-webapp
#387 maven-archetype-quickstart
```

```bash
mvn clean install
  
mvn cobertura:cobertura
  
mvn surefire-report:report
  
mvn surefire-report:report-only
  
mvn pmd:pmd
  
mvn eclipse:clean
  
mvn eclipse:eclipse
  
-mvn package: 依据项目生成jar/war文件
  
mvn dependency:sources
  
mvn dependency:resolve -Dclassifier=javadoc

webApp: maven-archetype-webapp
  
-Dmvn install -Dmaven.test.skip=true  <del>编译时跳过Test</del>

-Dmaven.test.failure.ignore=true <del> Set this to true to ignore a failure during testing. Its use is NOT RECOMMENDED, but quite convenient on occasion.</del>

mvn install -rf  :MODULENAME

mvn clean install
  
mvn –version
  
mvn compile
  
mvn test
  
mvn test-compile
  
mvn package
  
mvn install
  
mvn site
  
mvn clean
  
mvn eclipse:eclipse
  
mvn eclipse:clean

# The Surefire report can also generate the report using its standalone goal
  
mvn surefire-report:report
  
# A HTML report should be generated in ${basedir}/target/site/surefire-report.html

-maven idea
```

```bash

mvn idea:idea

mvn idea:clean

```

```bash
  
#maven install jar
mvn install:install-file -DgroupId=com.oracle -DartifactId=ojdbc6 -Dversion=11.2.0.3 -Dpackaging=jar -Dfile=/home/wiloon/Downloads/ojdbc6.jar
  
```

### os-maven-plugin

os-maven-plugin 是设置各种有用属性 (从 OS 中检测的 ${os.name} 和 ${os.arch} 属性) 的 Maven 插件

### Maven项目的标准目录结构

```r
src 
  main
      java 源文件 
      resources 资源文件
      filters 资源过滤文件
      config 配置文件
      scripts 脚本文件
      webapp web应用文件
  test
      java 测试源文件
      resources 测试资源文件
      filters 测试资源过滤文件
      it 集成测试
      assembly assembly descriptors
      site Site
      target

      generated-sources

      classes

      generated-test-sources

      test-classes

      xxx.jar

      pom.xml

      LICENSE.txt

      NOTICE.txt

      README.txt
```

### pom

#### extensions

```xml
    <!-- build中的extensions是执行构建过程中可能用到的其他工lib，在执行构建的过程中被加入到classpath中。 -->
    <extensions>
        <extension>
            <groupId>commons-io</groupId>
            <artifactId>commons-io</artifactId>
            <version>2.4</version>
        </extension>
    </extensions>
```

<https://stackoverflow.com/questions/31377964/mvn-archetypegenerate-darchetypecatalog-local-does-not-list-my-archetype>

3.3 .user

对指定用户的配置。user configuration可以在${user.home}/.m2/settings.xml中指定。注: 该文件不是必须的，当该文件找不到时，maven会使用默认的配置。

关于该文件的具体配置可以参考: <http://maven.apache.org/ref/2.0.4/maven-settings/settings.html>。

3.4  配置本地Repository

本地Repository的默认值是${user.home}/.m2/repository/。可以在user configuration(即在${user.home}/.m2/setting.xml) 中改变本地Repository。

配置如下: `<settings></settings>`

`<localRepository>/path/to/local/repo</localRepository>`

 3.5 配置代理

在maven2.0中，可以为http request配置代理。同样在user configuration中配置，配置如下:

```xml
<settings></settings>
    <proxy>
      <id>optional</id>
      true</active>
      <protocol>http</protocol>
      <username>proxyuser</username>
      <password>proxypass</password>
      <host>www.hc360.com</host>
      <port>80</port>
      <nonProxyHosts>local.net,some.host.com</nonProxyHosts>
    </proxy>
```

详见: <http://maven.apache.org/guides/mini/guide-proxies.html>

3.5 安全和部署配置
在一个project中，该项目将要使用哪个Repository，是在`<distributionmanagement></distributionmanagement>`setting.xml中指定的。然而，你却不能将用户名和
码以及其它的安全设定也放在该project中。因此，你可能会在你自己的设定中定义一个server,给它指定一个id, 该id
与project将要使用那个Repository相对应。
另外，有些repository在下载时可能需要用户名和密码，这些也可以在server element中以相同的方式指定。配置如下

```xml
<server>
  <id>deploymentRepo</id>
  <username>repouser</username>
  <password>repopwd</password>
</server>
```

<http://liwanchun-xd.iteye.com/blog/144047>

```xml
<?xml version="1.0" encoding="UTF-8"?>
<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd">
 <pluginGroups>
  </pluginGroups>
 <proxies>
 </proxies>
<servers>
 </servers>
 <mirrors>
<mirror>
    <id>aliyunmaven</id>
    <mirrorOf>*</mirrorOf>
    <name>阿里云公共仓库</name>
    <url>https://maven.aliyun.com/repository/public</url>
</mirror>  
</mirrors>
  <profiles>
  </profiles>
</settings>
```

### tomcat7-maven-plugin

```bash
mvn tomcat:run
```

### maven-clean-plugin

The Clean Plugin only has one goal.

clean:clean attempts to clean a project's working directory of the files that we're generated at build-time. By default, it discovers and deletes the directories configured in project.build.directory, project.build.outputDirectory, project.build.testOutputDirectory, and project.reporting.outputDirectory.

<https://maven.apache.org/plugins/maven-clean-plugin/>

### frontend-maven-plugin

## maven plugins

<http://www.infoq.com/cn/news/2011/04/xxb-maven-7-plugin>

- maven-compiler-plugin [[maven-compiler-plugin#maven-compiler-plugin]]
- maven-resources-plugin [[maven-resources-plugin#maven-resources-plugin]]
- jib-maven-plugin [[jib-maven-plugin#jib-maven-plugin]]
