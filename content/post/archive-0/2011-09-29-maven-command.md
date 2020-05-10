---
title: maven command
author: wiloon
type: post
date: 2011-09-29T04:34:14+00:00
url: /?p=959
bot_views:
  - 7
views:
  - 3
categories:
  - DataBase
tags:
  - Maven

---
-e for error
  
-X for debug
  
-q for only error

### 生成项目

<pre><code class="language-bash line-numbers"># common project
# mvn archetype:generate 会自动创建项目目录mvntest
mvn archetype:generate -DgroupId=com.wiloon.test -DartifactId=mvntest \
-DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false

# local catalog
mvn archetype:generate -DgroupId=com.wiloon.test -DartifactId=mvntest \
-DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false -DarchetypeCatalog=local

#web project
mvn archetype:generate -DgroupId=com.wiloon.mail.web -DartifactId=mailTestWeb \
-DarchetypeArtifactId=maven-archetype-webapp -DinteractiveMode=false
</code></pre>

<pre><code class="language-bash line-numbers">mvn clean compile -Dmaven.test.skip=true org.apache.maven.plugins:maven-war-plugin:exploded -q

#-U,--update-snapshots                  Forces a check for missing                                        releases and updated snapshots on
mvn clean compile -U
</code></pre>

<pre><code class="language-bash line-numbers"># upload jar to nexus
mvn deploy:deploy-file -Dfile=xxx.pom -DgroupId=com.wiloon -DartifactId=artifactid0 -Dversion=1.0.0 -Dpackaging=pom -DrepositoryId=repo0 -Durl=https://maven.wiloon.com/repository/snapshot/

mvn deploy:deploy-file -Dfile=xxx.jar -DgroupId=com.wiloon -DartifactId=artifactid0 -Dversion=1.0.0 -Dpackaging=jar -DrepositoryId=repo0 -Durl=https://maven.wiloon.net/repository/snapshot/

#maven war plugin
mvn clean compile -Dmaven.test.skip=true org.apache.maven.plugins:maven-war-plugin:exploded

# maven-assembly-plugin 打包
mvn assembly:assembly

mvn dependency:tree

#Generates JSW based daemon wrappers.
mvn appassembler:generate-daemons 

mvn -version

mvn install

mvn install -Dmaven.test.skip=true

#wrapper
mvn package appassembler:assemble
</code></pre>

查看mvn 参数

<pre><code class="language-bash line-numbers">mvn --help
mvn install 指定 pom.xml
mvn -f trunk\mvntest\pom.xml install
</code></pre>

<pre><code class="language-bash line-numbers">mvn archetype:generate
#390 maven-archetype-webapp
#387 maven-archetype-quickstart
</code></pre>

mvn clean install
  
mvn cobertura:cobertura
  
mvn surefire-report:report
  
mvn surefire-report:report-only
  
mvn pmd:pmd
  
mvn eclipse:clean
  
mvn eclipse:eclipse
  
&#8211;mvn package：依据项目生成jar/war文件
  
mvn dependency:sources
  
mvn dependency:resolve -Dclassifier=javadoc

webApp: maven-archetype-webapp
  
-Dmvn install -Dmaven.test.skip=true  <del>编译时跳过Test</del>

-Dmaven.test.failure.ignore=true <del> Set this to <code>true</code> to ignore a failure during testing. Its use is <strong>NOT RECOMMENDED</strong>, but quite convenient on occasion.</del>

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

&#8212;maven idea

[shell]

mvn idea:idea

mvn idea:clean

[/shell]

[shell]
  
#maven install jar
  
mvn install:install-file -DgroupId=com.oracle -DartifactId=ojdbc6 -Dversion=11.2.0.3 -Dpackaging=jar -Dfile=/home/wiloon/Downloads/ojdbc6.jar
  
[/shell]

### Maven项目的标准目录结构

  * src 
      * main
  
        -java 源文件</p> 
          * resources 资源文件
          * filters 资源过滤文件
          * config 配置文件
  
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

https://stackoverflow.com/questions/31377964/mvn-archetypegenerate-darchetypecatalog-local-does-not-list-my-archetype