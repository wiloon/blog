---
title: 命令行 创建多模块的Maven项目(父模块,子模块)
author: "-"
date: 2014-05-06T11:42:33+00:00
url: /?p=6584
categories:
  - Inbox
tags:
  - Maven

---
## 命令行 创建多模块的Maven项目(父模块,子模块)

我们都知道,我们常常将一个复杂的java应用拆分成多个java子应用。由于maven的出现,这种拆分就更加容易了,因为我们通过maven可以创建多个关联模块的项目 (Multiple Module Projects) 。由一个总的模块,下面包含多个子模块 (子模块还可以包含子模块) 。

一、通过在Maven命令行创建。

1. 创建父模块 (总的POM)  - cms-validator
  
使用命令mvn archetype:create -DgroupId=com.ebay.tools.cms.validator -DartifactId=cms-validator
  
创建一个maven项目,然后修改该项目的pom.xml文件,将package类型改为pom
  
<packaging>pom</packaging>
  
并删除其中的src目录。

cd cms-validator

2. 创建提供rest service的子模块: validator-rest
  
在父模块的目录下,
  
使用命令mvn archetype:create -DgroupId=com.ebay.tools.cms.validator.rest -DartifactId=validator-rest
  
创建一个maven (子) 项目。

3. 创建一个web子模块:  validator-web
  
在父模块的目录下,
  
mvn archetype:create -DgroupId=com.ebay.tools.cms.validator.web -DartifactId=validator-web -DarchetypeArtifactId=maven-archetype-webapp

完成以上3步以后,会在总的pom.xml中已经自动加入:
  
<modules>
  
<module>validator-rest</module>
  
<module>validator-web</module>
  
</modules>
  
在各个子模块中也自动的加入了:
  
<parent>

<artifactId>cms-validator</artifactId>

<groupId>com.ebay.tools.cms.validator</groupId>

<version>1.0-SNAPSHOT</version>

</parent>
  
由于默认情况下子模块继承了总POM的package(pom),这里需要修改子模块的pom的package类型。
  
validator-web模块覆盖为<packaging>war</packaging>, validator-rest模块修改为: <packaging>jar</packaging>。

4. 对父模块的特别设置:
  
需要在上级模块中设置java编译的参数,现在eclipse一般都使用比较新的版本,默认jdk是1.6,而maven默认的Jdk版本很有可能还是1.4。 所以需要设置java编译参数。
  
<plugin>

<artifactId>maven-compiler-plugin</artifactId>

<configuration>

<source>1.6</source>

<target>1.6</target>

<encoding>UTF-8</encoding>

</configuration>

</plugin>
  
5. 如果web子模块需要wtp的支持,则可以在web模块的pom中设置wtp的支持,需要设置elcipse插件:
  
<build>

<plugins>

<plugin>

<groupId>org.apache.maven.plugins</groupId>

<artifactId>maven-eclipse-plugin</artifactId>

<configuration>

<wtpmanifest>true</wtpmanifest>

<wtpapplicationxml>true</wtpapplicationxml>

<wtpversion>2.0</wtpversion>

</configuration>

</plugin>

</plugins>

</build>
  
6. 生成eclipse项目:
  
在父模块的根目录下,执行命令:
  
mvn eclipse:eclipse

注: 在eclipse中导入如上的项目后,如果没有在eclipse中设置"M2_REPO",导入的项目可能会报错,
  
可以在eclipse中设置M2_REPO, 配置步骤: window >> preferences >> Java >> Build Path >> Classpath Variables
  
新建一个 M2_REPO 的变量,变量值指向你系统的Maven2的数据仓库位置(例如我自己的路径为: C:\maven-repo\swang\ebox)。如果要在eclipse中使用m2eclipse,需要执行命令mvn eclipse:m2eclipse, 这样就不需要设置M2_REPO类库变量了。

<http://josh-persistence.iteye.com/blog/1930785>
