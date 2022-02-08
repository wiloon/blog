---
title: 'java 8 > java 9+ 模块'
author: "-"
date: 2020-03-08T13:54:56+00:00
url: /?p=15700
categories:
  - Uncategorized

tags:
  - reprint
---
## 'java 8 > java 9+ 模块'
在src / main / java目录中创建一个名为module-info.java的文件

### maven plugin

    ```xml
<properties>
        <maven.jar.plugin.version>3.2.0</maven.jar.plugin.version>
        <maven.dependency.plugin.version>3.1.1</maven.dependency.plugin.version>
    </properties>

<plugin>
                <groupId>org.apache.maven.plugins</groupId>
                maven-jar-plugin</artifactId>
                <version>${maven.jar.plugin}</version>
                <configuration>
                    <outputDirectory>
                        ${project.build.directory}/modules
                    </outputDirectory>
                </configuration>
 </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                maven-dependency-plugin</artifactId>
                <version>${maven.dependency.plugin.version}</version>
                <executions>
                    <execution>
                        <phase>package</phase>
                        <goals>
                            <goal>copy-dependencies</goal>
                        </goals>
                        <configuration>
                            <outputDirectory>
                                ${project.build.directory}/modules
                            </outputDirectory>
                            <includeScope>runtime</includeScope>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
```