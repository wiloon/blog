---
title: maven-resources-plugin
author: "-"
date: 2011-10-09T04:35:36+00:00
url: maven-resources-plugin
categories:
  - Maven
tags:
  - reprint
---
## maven-resources-plugin

Apache Maven Resources Plugin是Apache Maven团队提供的官方核心插件，能够将Maven项目中的各种资源文件复制到指定的输出目录中。

1. 在Maven项目中的资源可以分为两类

main资源，指位于src/main/resources路径下的资源文件
test资源，指位于src/test/resources路径下的资源文件
2. Apache Maven Resources Plugin提供的Goals

1) resources:resources

将main资源文件复制到输出目录，默认已经加入到Maven的process-resources生命周期阶段。

`<project><build><resources>`指定要复制的main资源文件，默认位于src/main/resources路径
`<project><build><outputDirectory>`指定main资源的输出目录，默认位于target/classes/路径
2) resources:testResources

将test资源文件复制到输出目录，默认已经加入到Maven的process-test-resources生命周期阶段。

`<project><build><testResources>`指定要复制的test资源文件，默认位于src/test/resources路径
`<project><build><testOutputDirectory>`指定test资源的输出目录，默认位于target/test-classes/路径
3) resources:copy-resources

对于非main资源或非test资源，又没有在pom.xml的`<build><resources>...</build></resources>`配置的资源，在构建过程中不会输出到项目的target/classes/目录下。
————————————————
版权声明：本文为CSDN博主「易生一世」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：[https://blog.csdn.net/taiyangdao/article/details/103636330](https://blog.csdn.net/taiyangdao/article/details/103636330)

java-使用maven将版本号输出到文本
[https://www.itranslater.com/qa/details/2582583740010595328](https://www.itranslater.com/qa/details/2582583740010595328)
[https://blog.csdn.net/u011781521/article/details/79052725](https://blog.csdn.net/u011781521/article/details/79052725)

    src/main/resources/version.txt
    ${project.version}

    <plugin>
      <artifactId>maven-resources-plugin</artifactId>
      <version>3.2.0</version>
      <executions>
          <execution>
              <id>print-version-file</id>
              <phase>validate</phase>
              <goals>
                  <goal>resources</goal>
              </goals>
              <configuration>
                  <outputDirectory>${basedir}/target/classes</outputDirectory>
                  <resources>
                      <resource>
                          <directory>${basedir}/src/main/resources</directory>
                          <filtering>true</filtering>
                      </resource>
                  </resources>
              </configuration>
          </execution>
      </executions>
    </plugin>


    mvn clean validate
