---
title: mvn maven basic, command
author: w1100n
type: post
date: 2011-09-29T04:34:14+00:00
url: /?p=959
tags:
  - maven

---
### setting>mirror
https://developer.aliyun.com/mirror/maven

### 参数
对应一个变量值，pom.xml里面配置的有，那么如果你在命令行中 以 -Dmy.filter.value=1 的格式去配置mvn命令，那么将覆盖你pom中的值。
    mvn clean -Ptrip-app,daily package -Dmy.filter.value=1 -Dttidapk.ttids=21xx00

    <project>
      <properties>
        <my.filter.value>hello</my.filter.value>
      </properties>
    </project>
    https://blog.csdn.net/Maxiao1204/article/details/90510176

### command
  -e for error
  -X for debug
  -q for only error

### 生成项目

```bash
# common project
# mvn archetype:generate 会自动创建项目目录 mvntest
mvn archetype:generate -DgroupId=com.wiloon.test -DartifactId=mvntest \
-DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false

mvn archetype:generate -DgroupId=com.wiloon.java -DartifactId=javaJpms \
-DarchetypeArtifactId=maven-archetype-quickstart -DarchetypeVersion=1.4 -DinteractiveMode=false

# local catalog
mvn archetype:generate -DgroupId=com.wiloon.test -DartifactId=mvntest \
-DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false -DarchetypeCatalog=local

# web project
mvn archetype:generate -DgroupId=com.wiloon.mail.web -DartifactId=mailTestWeb \
-DarchetypeArtifactId=maven-archetype-webapp -DinteractiveMode=false
```

```bash
mvn clean compile -Dmaven.test.skip=true org.apache.maven.plugins:maven-war-plugin:exploded -q

#-U,--update-snapshots                  Forces a check for missing                                        releases and updated snapshots on
mvn clean compile -U
```
### 检测包冲突工具
    mvn dependency:help
    mvn dependency:analyze
    mvn dependency:tree
    mvn dependency:tree -Dverbose
    
```bash
# upload jar to nexus
mvn deploy:deploy-file -Dfile=xxx.pom -DgroupId=com.wiloon -DartifactId=artifactid0 -Dversion=1.0.0 -Dpackaging=pom -DrepositoryId=repo0 -Durl=https://maven.wiloon.com/repository/snapshot/

mvn deploy:deploy-file -Dfile=xxx.jar -DgroupId=com.wiloon -DartifactId=artifactid0 -Dversion=1.0.0 -Dpackaging=jar -DrepositoryId=repo0 -Durl=https://maven.wiloon.net/repository/snapshot/

#maven war plugin
mvn clean compile -Dmaven.test.skip=true org.apache.maven.plugins:maven-war-plugin:exploded

# maven-assembly-plugin 打包
mvn assembly:assembly



#Generates JSW based daemon wrappers.
mvn appassembler:generate-daemons 

mvn -version

mvn install

mvn install -Dmaven.test.skip=true

#wrapper
mvn package appassembler:assemble
```

查看mvn 参数

```bash
mvn --help
mvn install 指定 pom.xml
mvn -f trunk\mvntest\pom.xml install
```

```bash
mvn archetype:generate
#390 maven-archetype-webapp
#387 maven-archetype-quickstart
```

mvn clean install
  
mvn cobertura:cobertura
  
mvn surefire-report:report
  
mvn surefire-report:report-only
  
mvn pmd:pmd
  
mvn eclipse:clean
  
mvn eclipse:eclipse
  
-mvn package：依据项目生成jar/war文件
  
mvn dependency:sources
  
mvn dependency:resolve -Dclassifier=javadoc

webApp: maven-archetype-webapp
  
-Dmvn install -Dmaven.test.skip=true  <del>编译时跳过Test</del>

-Dmaven.test.failure.ignore=true <del> Set this to <code>true</code> to ignore a failure during testing. Its use is NOT RECOMMENDED, but quite convenient on occasion.</del>

mvn install -rf  :MODULENAME

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

#The Surefire report can also generate the report using its standalone goal:
  
mvn surefire-report:report
  
#A HTML report should be generated in ${basedir}/target/site/surefire-report.html.

-maven idea

```bash

mvn idea:idea

mvn idea:clean

```

```bash
  
#maven install jar
  
mvn install:install-file -DgroupId=com.oracle -DartifactId=ojdbc6 -Dversion=11.2.0.3 -Dpackaging=jar -Dfile=/home/wiloon/Downloads/ojdbc6.jar
  
```

### os-maven-plugin
os-maven-plugin 是设置各种有用属性（从 OS 中检测的 ${os.name} 和 ${os.arch} 属性）的 Maven 插件

### Maven项目的标准目录结构
    src 
      main
        -java 源文件 
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

### pom
#### extensions
    <!-- build中的extensions是执行构建过程中可能用到的其他工lib，在执行构建的过程中被加入到classpath中。 -->
    <extensions>
        <extension>
            <groupId>commons-io</groupId>
            <artifactId>commons-io</artifactId>
            <version>2.4</version>
        </extension>
    </extensions>


https://stackoverflow.com/questions/31377964/mvn-archetypegenerate-darchetypecatalog-local-does-not-list-my-archetype




3.3 .user

对指定用户的配置。user configuration可以在<tt>${user.home}/.m2/settings.xml中指定。注: 该文件不是必须的，当该文件找不到时，maven会使用默认的配置。</tt>

<tt>关于该文件的具体配置可以参考: <a href="http://maven.apache.org/ref/2.0.4/maven-settings/settings.html">http://maven.apache.org/ref/2.0.4/maven-settings/settings.html</a>。</tt>

3.4  <tt>配置本地Repository</tt>

<tt>本地Repository的默认值是<tt>${user.home}/.m2/repository/。可以在user configuration(即在${user.home}/.m2/setting.xml）中改变本地Repository。</tt></tt>

<tt>配置如下: </tt><settings></settings>

<localRepository>/path/to/local/repo</localRepository>
注意: 本地Repository 必须是绝对路径。

 3.5 配置代理


<tt>在maven2.0中，可以为http request配置代理。同样在user configuration中配置，配置如下: </tt>
<settings></settings>     <proxy>
      <id>optional</id>
      <active>true</active>
      <protocol>http</protocol>
      <username>proxyuser</username>
      <password>proxypass</password>
      <host>www.hc360.com</host>
      <port>80</port>
      <nonProxyHosts>local.net,some.host.com</nonProxyHosts>
    </proxy>

详见: <a href="http://maven.apache.org/guides/mini/guide-proxies.html">http://maven.apache.org/guides/mini/guide-proxies.html</a>


3.5 安全和部署配置


<tt>在一个project中，该项目将要使用哪个Repository，是在<distributionmanagement></distributionmanagement>setting.xml中指定的。然而，你却不能将用户名和</tt>
码以及其它的安全设定也放在该project中。因此，你可能会在你自己的设定中定义一个server,给它指定一个id, 该id
与project将要使用那个Repository相对应。
另外，有些repository在下载时可能需要用户名和密码，这些也可以在server element中以相同的方式指定。配置如下
    <server>
      <id>deploymentRepo</id>
      <username>repouser</username>
      <password>repopwd</password>
    </server>

<a href="http://liwanchun-xd.iteye.com/blog/144047">http://liwanchun-xd.iteye.com/blog/144047</a>

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


