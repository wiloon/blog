---
title: appassembler-maven-plugin
author: "-"
date: 2016-01-05T01:51:35+00:00
url: /?p=8630
categories:
  - Inbox
tags:
  - reprint
---
## appassembler-maven-plugin

### Goals Overview

* [appassembler:assemble][1] Assembles the artifacts and generates bin scripts for the configured applications.
* [appassembler:create-repository][2] Creates an appassembler repository.
* [appassembler:generate-daemons][3] Generates JSW based daemon wrappers.

maven 自动生成运行脚本插件appassembler-maven-plugin
  
博客分类: maven

appassembler-maven-plugin可以自动生成跨平台的启动脚本,省去了手工写脚本的麻烦,而且还可以生成jsw的后台运行程序。

appassembler的配置比较简单,在pom.xml的配置文件加入插件配置。

比如说不同的启动脚本,可以如下配置

Xml代码
  
<plugin>
  
<groupId>org.codehaus.mojo</groupId>
  
appassembler-maven-plugin</artifactId>
  
<version>1.2.1</version>
  
<configuration>
  
<configurationDirectory>conf</configurationDirectory>
  
<configurationSourceDirectory>src/main/resources</configurationSourceDirectory>
  
<copyConfigurationDirectory>true</copyConfigurationDirectory>
  
<includeConfigurationDirectoryInClasspath>true</includeConfigurationDirectoryInClasspath>
  
${project.build.directory}/chj-search-client</assembleDirectory>
  
<extraJvmArguments>-Xms128m</extraJvmArguments>
  
<binFileExtensions>
  
<unix>.sh</unix>
  
</binFileExtensions>
  
<platforms>
  
<platform>windows</platform>
  
<platform>unix</platform>
  
</platforms>
  
<repositoryName>lib</repositoryName>
  
<programs>
  
<program>
  
<mainClass>com.chj360.search.client.App</mainClass>
  
</program>
  
</programs>
  
</configuration>
  
</plugin>
  
然后运行maven命令 :mvn package appassembler:assemble

就可以自动生成整个的依赖文件,配置文件和运行脚本了。

一些配置说明

configurationDirectory: 生成配置文件路径

configurationSourceDirectory: 配置文件原路径,默认为src/main/config

assembleDirectory:整体包目录

extraJvmArguments: jvm参数

binFileExtensions: 生成脚本的后缀

platforms: 生成哪几种平台

repositoryName: 依赖包目录,默认repo

programs: 这个必须参数,启动的主class

生成jsw也是一个简单的配置

eg:

Xml代码
  
<plugin>
  
<groupId>org.codehaus.mojo</groupId>
  
appassembler-maven-plugin</artifactId>
  
<version>1.2.1</version>
  
<configuration>
  
<repositoryLayout>flat</repositoryLayout>
  
<repositoryName>lib</repositoryName>
  
<includeConfigurationDirectoryInClasspath>true</includeConfigurationDirectoryInClasspath>
  
<copyConfigurationDirectory>src/main/resources</copyConfigurationDirectory>
  
<target>${project.build.directory}</target>
  
<daemons>
  
<daemon>
  
<id>chj-search-client</id>
  
<mainClass>com.chj360.search.client.App</mainClass>
  
<commandLineArguments>
  
<commandLineArgument>start</commandLineArgument>
  
</commandLineArguments>
  
<platforms>
  
<platform>jsw</platform>
  
</platforms>
  
<generatorConfigurations>
  
<generatorConfiguration>
  
<generator>jsw</generator>
  
<includes>
  
<include>linux-x86-32</include>
  
<include>linux-x86-64</include>
  
<include>windows-x86-32</include>
  
<include>windows-x86-64</include>
  
</includes>
  
<configuration>
  
<property>
  
<name>configuration.directory.in.classpath.first</name>
  
<value>etc</value>
  
</property>
  
<property>
  
<name>set.default.REPO_DIR</name>
  
<value>lib</value>
  
</property>
  
<property>
  
<name>wrapper.logfile</name>
  
<value>../logs/wrapper.log</value>
  
</property>
  
<property>
  
<name>run.as.user.envvar</name>
  
<value>johndoe</value>
  
</property>
  
</configuration>
  
</generatorConfiguration>
  
</generatorConfigurations>
  
<jvmSettings>
  
<initialMemorySize>256M</initialMemorySize>
  
<maxMemorySize>512M</maxMemorySize>
  
<systemProperties>
  
<systemProperty>java.security.policy=conf/policy.all</systemProperty>
  
<systemProperty>com.sun.management.jmxremote</systemProperty>
  
<systemProperty>com.sun.management.jmxremote.port=8999</systemProperty>
  
<systemProperty>com.sun.management.jmxremote.authenticate=false</systemProperty>
  
<systemProperty>com.sun.management.jmxremote.ssl=false</systemProperty>
  
</systemProperties>
  
<extraArguments>
  
<extraArgument>-server</extraArgument>
  
</extraArguments>
  
</jvmSettings>
  
</daemon>
  
</daemons>
  
</configuration>
  
<executions>
  
<execution>
  
<id>generate-jsw-scripts</id>
  
<phase>package</phase>
  
<goals>
  
<goal>generate-daemons</goal>
  
</goals>
  
</execution>
  
</executions>
  
</plugin>

[http://lavafree.iteye.com/blog/1502594](http://lavafree.iteye.com/blog/1502594)

[http://www.mojohaus.org/appassembler/appassembler-maven-plugin/](http://www.mojohaus.org/appassembler/appassembler-maven-plugin/)

 [1]: http://www.mojohaus.org/appassembler/appassembler-maven-plugin/assemble-mojo.html
 [2]: http://www.mojohaus.org/appassembler/appassembler-maven-plugin/create-repository-mojo.html
 [3]: http://www.mojohaus.org/appassembler/appassembler-maven-plugin/generate-daemons-mojo.html
