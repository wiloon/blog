---
title: maven plugin
author: "-"
date: 2011-10-09T04:35:36+00:00
url: /?p=1010
categories:
  - Linux

tags:
  - reprint
---
## maven plugin
http://www.infoq.com/cn/news/2011/04/xxb-maven-7-plugin

### resouce plugin
java-使用maven将版本号输出到文本
https://www.itranslater.com/qa/details/2582583740010595328
https://blog.csdn.net/u011781521/article/details/79052725


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