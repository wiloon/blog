---
title: java 模块 hello world
author: "-"
date: 2020-03-07T12:58:10+00:00
url: /?p=15691

categories:
  - inbox
tags:
  - reprint
---
## java 模块 hello world

### java 模块

    mkdir -p  src/speaker/com/pingd/test/java/module
    vim src/speaker/com/pingd/test/java/module/Hello.java

### src/speaker/com/pingd/test/java/module/Hello.java 

    package com.pingd.test.java.module;

    public class Hello{
            public static void foo (){
                    System.out.println("hello world");
            }
    }

### src/speaker/module-info.java

speaker:  模块名
requires xxx;表示这个模块需要引用的其他模块名。  
    java.base可以被自动引入  
exports:  到package级

    module speaker{
            exports com.pingd.test.java.module;
    }

### src/app/com/pingd/test/java/module/app/App.java

    package com.pingd.test.java.module.app;

    public class App{
            public static void main(String args[]){
                    com.pingd.test.java.module.Hello.foo();
            }
    }

### src/app/module-info.java

    module app{
            requires speaker;
    }

### build

    cd java-module-x
    javac -d out --module-source-path src -m speaker
    javac -d out --module-source-path src -m app

### run

   java --module-path ./out --module app/com.pingd.test.java.module.app.App

### build jar

    jar --create --file speaker.jar -C out/speaker .
    jar --create --file app.jar --main-class com.pingd.test.java.module.app.App -C out/app .

### run jar

    java --module-path . --module app

### 目录 结构

    ├── out
    │   ├── app
    │   │   ├── com
    │   │   │   └── pingd
    │   │   │       └── test
    │   │   │           └── java
    │   │   │               └── module
    │   │   │                   └── app
    │   │   │                       └── App.class
    │   │   └── module-info.class
    │   └── speaker
    │       ├── com
    │       │   └── pingd
    │       │       └── test
    │       │           └── java
    │       │               └── module
    │       │                   └── Hello.class
    │       └── module-info.class
    └── src
        ├── app
        │   ├── com
        │   │   └── pingd
        │   │       └── test
        │   │           └── java
        │   │               └── module
        │   │                   └── app
        │   │                       └── App.java
        │   └── module-info.java
        └── speaker
            ├── com
            │   └── pingd
            │       └── test
            │           └── java
            │               └── module
            │                   └── Hello.java
            └── module-info.java

module-info.java一般包含以下信息
  
模块名称
  
该模块依赖的其他模块
  
该模块提供了其他模块

四种模块类型:
  
命名的模块 (也称为应用程序模块) 包含上述module-info.java
  
平台模块 (类似于前者，但这些都是随JDK一起发货)
  
自动模块是在模块路径上提供的那些旧JAR
  
未命名的模块是标准类路径上列出的所有内容

### 对Maven用户的影响

为了能够使用JDK 9的模块系统maven-compiler-plugin版本3.6.1或更高版本

```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-compiler-plugin</artifactId>
  <version>3.6.1</version>
  <configuration>
    <showWarnings>true</showWarnings>
    <showDeprecation>true</showDeprecation>
  </configuration>
</plugin>
```

#### 工具链插件

$HOME/.m2/toolchains.xml

```xml
<toolchains>
  <toolchain>
    <type>jdk</type>
    <provides>
      <version>9</version>
      <vendor>oracle</vendor>
    </provides>
    <configuration>
      <!-- Change path to JDK9 -->
      <jdkHome>/opt/oracle/jdk-9</jdkHome>
    </configuration>
  </toolchain>
  <toolchain>
    <type>jdk</type>
    <provides>
      <version>1.8</version>
      <vendor>oracle</vendor>
    </provides>
    <configuration>
      <jdkHome>/opt/oracle/jdk-1.8.0.65</jdkHome>
    </configuration>
  </toolchain>
</toolchains>
``` 

#### pom.xml

```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  maven-toolchains-plugin</artifactId>
  <version>1.1</version>
  <configuration>
    <toolchains>
    <jdk>
        <version>9</version>
        <vendor>oracle</vendor>
    </jdk>
    </toolchains>
  </configuration>
  <executions>
    <execution>
      <goals>
        <goal>toolchain</goal>
    </goals>
    </execution>
  </executions>
</plugin>
``` 

### 启用Java 9语言支持

```xml
<properties>
  <maven.compiler.release>9</maven.compiler.release>
</properties>
``` 

属性 maven.compiler.release直接映射到该-release标志javac，而另外两个属性只对IntelliJ有必要 ，用来了解源码兼容性。

### 一个模块示例

https://blog.csdn.net/rickiyeat/article/details/78068316

### 模块文件 module-info.java

放在和模块名相同的目录下
  
如果模块名称是 com.wiloon.java9x, module-info.java 应该放在: src/com.wiloon.java9x/module-info.java

#### module-info.java

```java
module com.wiloon.java9x { }
```

### 添加代码

```bash
vim src/com.wiloon.java9x/com/wiloon/java9x/Java9Tester.java
```

```java
package com.wiloon.java9x;

public class Java9Tester {
        public static void main(String[] args){
        System.out.println("hello world");
        }
}
```

### 编译模块

```bash
mkdir -p mods/com.wiloon.java9x
avac -d mods/com.wiloon.java9x src/com.wiloon.java9x/module-info.java src/com.wiloon.java9x/com/wiloon/java9x/Java9Tester.java

```

### 运行

```bash
java --module-path mods -m com.wiloon.java9x/com.wiloon.java9x.Java9Tester
```


---

http://lizhe.name/index.php/node/273