---
title: java maven 可执行 jar/ executable jar, maven-assembly-plugin
author: "-"
date: 2016-12-16T07:45:40+00:00
url: maven/assembly/plugin
categories:
  - maven
tags:
  - Java
  - Maven

---
## java maven 可执行 jar/ executable jar, maven-assembly-plugin

在pom中加入 maven-assembly-plugin
```xml
<project>
    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-assembly-plugin</artifactId>
                <version>3.3.0</version>
                <configuration>
                    <descriptorRefs>
                        <descriptorRef>jar-with-dependencies</descriptorRef>
                    </descriptorRefs>
                    <archive>
                        <manifest>
                            <mainClass>com.wiloon.java.lock.TestFutex</mainClass>
                        </manifest>
                    </archive>
                </configuration>
                <executions>
                    <execution>
                        <phase>package</phase>
                        <goals>
                            <goal>single</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
```


```bash
mvn clean package assembly:single
# 如果没执行过 mvn package 会报错： Cannot include project artifact: com.wiloon.java:pingd-java:jar:1.0-SNAPSHOT; it doesn't have an associated file or directory.
java -jar target/pingd-java-1.0-SNAPSHOT-jar-with-dependencies.jar

```