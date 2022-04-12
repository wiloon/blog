---
title: java 模块系统, Jigsaw
author: "-"
date: 2020-03-08T14:50:54+00:00
url: Jigsaw
categories:
  - Java
tags:
  - reprint
  - jigsaw
---
## java 模块系统, Jigsaw

## Java9 之前的版本

.class 文件是 JVM 看到的最小可执行文件，而一个大型程序需要编写很多 Class，并生成一堆 .class 文件，不便于管理，所以，jar 文件就是 class 文件的容器。  
在 Java9 之前，一个大型 Java 程序会生成自己的 jar 文件，同时引用依赖的第三方 jar 文件，而 JVM 自带的 Java 标准库，实际上也是以 jar 文件形式存放的，这个文件叫 rt.jar，一共有 60 多 M。

如果是自己开发的程序，除了一个自己的 app.jar 以外，还需要一堆第三方的 jar 包，运行一个 Java 程序，一般来说，命令行写这样:

```bash
java -cp app.jar:a.jar:b.jar:c.jar com.liaoxuefeng.sample.Main
```

jar 只是用于存放 class 的容器，它并不关心 class 之间的依赖。  

从 Java9 开始，原有的 Java 标准库已经由一个单一巨大的 rt.jar 分拆成了几十个模块，这些模块以 .jmod 扩展名标识，可以在 $JAVA_HOME/jmods 目录下找到它们:

```bash
java.base.jmod
java.compiler.jmod
java.datatransfer.jmod
java.desktop.jmod
...
```

这些.jmod文件每一个都是一个模块，模块名就是文件名

如果把 Java 8 比作单体应用，那么引入模块系统之后，从 Java 9 开始，Java 就华丽的转身为微服务。模块系统，项目代号 Jigsaw，最早于 2008 年 8 月提出(比 Martin Fowler 提出微服务还早 6 年)，2014 年跟随 Java 9 正式进入开发阶段，最终跟随 Java 9 发布于 2017 年 9 月。

## 什么是模块系统?

官方的定义是 A uniquely named, reusable group of related packages, as well as resources (such as images and XML files) and a module descriptor. 模块的载体是 jar 文件，一个模块就是一个 jar 文件，但相比于传统的 jar 文件，模块的根目录下多了一个 module-info.class 文件，也即 module descriptor。 module descriptor 包含以下信息:

- 模块名称
- 依赖哪些模块
- 导出模块内的哪些包(允许直接 import 使用)
- 开放模块内的哪些包(允许通过 Java 反射访问)
- 提供哪些服务
- 依赖哪些服务

从Java 9开始引入的模块，主要是为了解决"依赖"这个问题。如果a.jar必须依赖另一个b.jar才能运行，那我们应该给a.jar加点说明啥的，让程序在编译和运行的时候能自动定位到b.jar，这种自带"依赖关系"的class容器就是模块。

也就是说，任意一个 jar 文件，只要加上一个合法的 module descriptor，就可以升级为一个模块。

模块系统带来的好处

第一，原生的依赖管理。有了模块系统，Java 可以根据 module descriptor计算出各个模块间的依赖关系，一旦发现循环依赖，启动就会终止。同时，由于模块系统不允许不同模块导出相同的包(即 split package，分裂包)，所以在查找包时，Java 可以精准的定位到一个模块，从而获得更好的性能。

第二，精简 JRE。引入模块系统之后，JDK 自身被划分为 94 个模块(参见图-2)。通过 Java 9 新增的 jlink 工具，开发者可以根据实际应用场景随意组合这些模块，去除不需要的模块，生成自定义 JRE，从而有效缩小 JRE 大小。得益于此，JRE 11 的大小仅为 JRE 8 的 53%，从 218.4 MB缩减为 116.3 MB，JRE 中广为诟病的巨型 jar 文件 rt.jar 也被移除。更小的 JRE 意味着更少的内存占用，这让 Java 对嵌入式应用开发变得更友好。

[![s9CnYt.jpg](https://s3.ax1x.com/2021/01/03/s9CnYt.jpg)](https://imgchr.com/i/s9CnYt)

第三，更好的兼容性。自打 Java 出生以来，就只有 4 种包可见性，这让 Java 对面向对象的三大特征之一封装的支持大打折扣，类库维护者对此叫苦不迭，只能一遍又一遍的通过各种文档或者奇怪的命名来强调这些或者那些类仅供内部使用，擅自使用后果自负云云。Java 9 之后，利用 module descriptor 中的 exports 关键词，模块维护者就精准控制哪些类可以对外开放使用，哪些类只能内部使用，换句话说就是不再依赖文档，而是由编译器来保证。类可见性的细化，除了带来更好的兼容性，也带来了更好的安全性。

第四，提升 Java 语言开发效率。Java 9 之后，Java 像开挂了一般，一改原先一延再延的风格，严格遵循每半年一个大版本的发布策略，从 2017 年 9 月到 2020 年 3 月，从 Java 9 到 Java 14，三年时间相继发布了 6 个版本，无一延期，参见图-4。这无疑跟模块系统的引入有莫大关系。前文提到，Java 9 之后，JDK 被拆分为 94 个模块，每个模块有清晰的边界(module descriptor)和独立的单元测试，对于每个 Java 语言的开发者而言，每个人只需要关注其所负责的模块，开发效率因此大幅提升。这其中的差别，就好比单体应用架构升级到微服务架构一般。

## 基础
### module descriptor
模块的核心在于 module descriptor，对应根目录下的 module-info.class 文件，而这个 class 文件是由源代码根目录下的 module-info.java 编译生成。Java 为 module-info.java 设计了专用的语法，包含 module、 requires、exports等多个关键词

语法解读: 

- [open] module : 声明一个模块，模块名称应全局唯一，不可重复。加上 open 关键词表示模块内的所有包都允许通过 Java 反射访问，模块声明体内不再允许使用 opens 语句。
- requires [transitive] : 声明模块依赖，一次只能声明一个依赖，如果依赖多个模块，需要多次声明。加上 transitive 关键词表示传递依赖，比如模块 A 依赖模块 B，模块 B 传递依赖模块 C，那么模块 A 就会自动依赖模块 C，类似于 Maven。
- exports [to [, ...]]: 导出模块内的包(允许直接 import 使用)，一次导出一个包，如果需要导出多个包，需要多次声明。如果需要定向导出，可以使用 to 关键词，后面加上模块列表(逗号分隔)。
- opens [to [, ...]]: 开放模块内的包(允许通过 Java 反射访问)，一次开放一个包，如果需要开放多个包，需要多次声明。如果需要定向开放，可以使用 to 关键词，后面加上模块列表(逗号分隔)。
- provides with [, ...]: 声明模块提供的 Java SPI 服务，一次可以声明多个服务实现类(逗号分隔)。
- uses : 声明模块依赖的 Java SPI 服务，加上之后模块内的代码就可以通过 ServiceLoader.load(Class) 一次性加载所声明的 SPI 服务的所有实现类。


### -p & -m 参数

Java 9 引入了一系列新的参数用于编译和运行模块，其中最重要的两个参数是 -p 和 -m。-p 参数指定模块路径，多个模块之间用 ":"(Mac, Linux)或者 ";"(Windows)分隔，同时适用于 javac 命令和 java 命令，用法和Java 8 中的 -cp非常类似。-m 参数指定待运行的模块主函数，输入格式为模块名/主函数所在的类名，仅适用于 java 命令。两个参数的基本用法如下: 

javac -p <module_path> <source>
java -p <module_path> -m <module>/<main_class>

从Java 9开始，原有的Java标准库已经由一个单一巨大的rt.jar分拆成了几十个模块，这些模块以.jmod扩展名标识，可以在$JAVA_HOME/jmods目录下找到它们: 

java.base.jmod
  
java.compiler.jmod
  
java.datatransfer.jmod
  
java.desktop.jmod
  
这些.jmod文件每一个都是一个模块，模块名就是文件名。例如: 模块java.base对应的文件就是java.base.jmod。模块之间的依赖关系已经被写入到模块内的module-info.class文件了。所有的模块都直接或间接地依赖java.base模块，只有java.base模块不依赖任何模块，它可以被看作是"根模块"，好比所有的类都是从Object直接或间接继承而来。

### maven
maven-compiler-plugin>3.6.1

---

https://www.liaoxuefeng.com/wiki/1252599548343744/1281795926523938
https://www.jianshu.com/p/bec282e8fb41
https://developer.51cto.com/art/202007/620291.htm


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


## 'jigsaw  hello world'
git@github.com:wiloon/java9x.git


http://blog.oneapm.com/apm-tech/724.html

http://stackoverflow.com/questions/39882669/unrecognized-option-modulepath

```bash

java -module-path mods -m com.mycompany.helloworld/com.mycompany.helloworld.HelloWorld

```


