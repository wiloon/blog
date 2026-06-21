---
title: Java 模块系统：JPMS 与 Jigsaw
author: "-"
date: 2020-03-08T14:50:54+00:00
lastmod: 2026-06-21T17:21:56+08:00
url: jpms-jigsaw
categories:
  - language
tags:
  - java
  - jpms
  - jigsaw
  - remix
  - AI-assisted
---
## Java 9 之前的版本

.class 文件是 JVM 看到的最小可执行文件，而一个大型程序需要编写很多 Class，并生成一堆 .class 文件，不便于管理，所以，jar 文件就是 class 文件的容器。
在 Java 9 之前，一个大型 Java 程序会生成自己的 jar 文件，同时引用依赖的第三方 jar 文件，而 JVM 自带的 Java 标准库，实际上也是以 jar 文件形式存放的，这个文件叫 rt.jar，一共有 60 多 M。

如果是自己开发的程序，除了一个自己的 app.jar 以外，还需要一堆第三方的 jar 包，运行一个 Java 程序，一般来说，命令行写这样:

```bash
java -cp app.jar:a.jar:b.jar:c.jar com.liaoxuefeng.sample.Main
```

jar 只是用于存放 class 的容器，它并不关心 class 之间的依赖。

从 Java 9 开始，原有的 Java 标准库已经由一个单一巨大的 rt.jar 分拆成了几十个模块，这些模块以 .jmod 扩展名标识，可以在 $JAVA_HOME/jmods 目录下找到它们:

```bash
java.base.jmod
java.compiler.jmod
java.datatransfer.jmod
java.desktop.jmod
...
```

这些 `.jmod` 文件每一个都是一个 JDK 模块，模块名就是文件名去掉 `.jmod` 后缀（例如 `java.base.jmod` → 模块 `java.base`）。

### JMOD 文件

`.jmod`（Java Module）是 Java 9 为 JDK 模块化引入的打包格式，主要出现在 `$JAVA_HOME/jmods/` 目录下。可以把它理解成带特殊文件头的 ZIP 压缩包：文件开头 4 字节魔数为 `JM`，后面是标准 ZIP 结构，因此可以用 `unzip -l` 列出内容。

它**不是**「里面再套一层 `.jar`」的容器。主体是 `classes/` 目录下的 `.class` 文件（含 `module-info.class`），必要时还会带上 native 库、配置、许可证等 JDK 分发所需的内容：

| 目录 | 内容 |
| ---- | ---- |
| `classes/` | `.class` 文件、`module-info.class`、SPI 等 |
| `lib/` | 本地库（`.so`/`.dylib`）或少量 jar（如 `java.base` 里的 `lib/jrt-fs.jar`） |
| `bin/` | 原生命令 |
| `conf/` | 配置文件 |
| `legal/` | 许可证文本 |
| `include/` | 头文件 |

模块之间的依赖关系已写入 `classes/module-info.class`。所有 JDK 模块都直接或间接依赖 `java.base`，只有 `java.base` 不依赖任何其他模块，可视为「根模块」——好比所有类都从 `Object` 直接或间接继承而来。

JMOD 与日常开发用的 modular JAR（`.jar` + 根目录 `module-info.class`）用途不同：

| | modular JAR | JMOD |
| ---- | ---- | ---- |
| 用途 | 应用/第三方库打包 | JDK 模块分发、供 `jlink` 组装运行时 |
| 模块描述符位置 | jar 根目录 | `classes/module-info.class` |
| Classpath（`-cp`） | 可用 | 不可用 |
| Module path | 常规 `--module-path` | 官方设计主要给 `jlink`，不是给普通编译/运行用的 |

Java 8 的 `rt.jar` 是一个大 jar，里面全是 class；Java 9 起拆成多个 `.jmod`，相当于按模块拆开并加上 native 库等分发物。运行时一般不直接「执行 jmod」——`jlink` 读取 `$JAVA_HOME/jmods/` 按需拼出自定义 JRE；JVM 通过 `jrt:/` 文件系统访问模块内容。

可以用 `jmod describe` 查看模块导出：

```bash
jmod describe $JAVA_HOME/jmods/java.base.jmod
```

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

### 模块系统带来的好处

第一，原生的依赖管理。有了模块系统，Java 可以根据 module descriptor计算出各个模块间的依赖关系，一旦发现循环依赖，启动就会终止。同时，由于模块系统不允许不同模块导出相同的包(即 split package，分裂包)，所以在查找包时，Java 可以精准的定位到一个模块，从而获得更好的性能。

第二，精简 JRE。引入模块系统之后，JDK 自身被划分为 94 个模块(参见图-2)。通过 Java 9 新增的 jlink 工具，开发者可以根据实际应用场景随意组合这些模块，去除不需要的模块，生成自定义 JRE，从而有效缩小 JRE 大小。得益于此，JRE 11 的大小仅为 JRE 8 的 53%，从 218.4 MB缩减为 116.3 MB，JRE 中广为诟病的巨型 jar 文件 rt.jar 也被移除。更小的 JRE 意味着更少的内存占用，这让 Java 对嵌入式应用开发变得更友好。运行时按需加载与 `jlink` 裁剪详见下文。

[![s9CnYt.jpg](https://s3.ax1x.com/2021/01/03/s9CnYt.jpg)](https://imgchr.com/i/s9CnYt)

第三，更好的兼容性。自打 Java 出生以来，就只有 4 种包可见性，这让 Java 对面向对象的三大特征之一封装的支持大打折扣，类库维护者对此叫苦不迭，只能一遍又一遍的通过各种文档或者奇怪的命名来强调这些或者那些类仅供内部使用，擅自使用后果自负云云。Java 9 之后，利用 module descriptor 中的 exports 关键词，模块维护者就精准控制哪些类可以对外开放使用，哪些类只能内部使用，换句话说就是不再依赖文档，而是由编译器来保证。类可见性的细化，除了带来更好的兼容性，也带来了更好的安全性。

第四，提升 Java 语言开发效率。Java 9 之后，Java 像开挂了一般，一改原先一延再延的风格，严格遵循每半年一个大版本的发布策略，从 2017 年 9 月到 2020 年 3 月，从 Java 9 到 Java 14，三年时间相继发布了 6 个版本，无一延期，参见图-4。这无疑跟模块系统的引入有莫大关系。前文提到，Java 9 之后，JDK 被拆分为 94 个模块，每个模块有清晰的边界(module descriptor)和独立的单元测试，对于每个 Java 语言的开发者而言，每个人只需要关注其所负责的模块，开发效率因此大幅提升。这其中的差别，就好比单体应用架构升级到微服务架构一般。

## 按需加载与 jlink

模块化之后，「按需」要分两层理解：**运行时加载**和**部署裁剪**。

### 运行时：只加载依赖链上的模块

JPMS 启动时会解析模块图。应用及其依赖 `requires` 了哪些模块，JVM 就加载这条依赖链上的模块；不在链上的 JDK 模块不会被加载。

例如在服务器上跑一个只 `requires java.base`、`java.logging` 的后端应用，即使磁盘上装着完整 JDK（含 `java.desktop.jmod`），**运行时通常也不会加载 desktop 模块**——前提是代码和第三方库都没有直接或间接依赖 `java.desktop`。

### 部署：jlink 物理裁剪 JRE

`jlink` 与 JPMS、JMOD 是一套能力：`jmod` 打包 JDK 模块，`jlink` 按需组装运行时。若目标是**缩小发行体积**（Docker 镜像、嵌入式设备等），仅靠「用不到就不加载」不够——完整 JDK 仍占磁盘。这时用 **`jlink`**（Java 9 引入，[JEP 282](https://openjdk.org/jeps/282)）从 `$JAVA_HOME/jmods/` 拼出自定义运行时：

```bash
# Server-oriented runtime: omit java.desktop and other GUI modules
jlink --add-modules java.base,java.logging,java.net.http \
      --strip-debug --no-man-pages --no-header-files \
      --compress=2 \
      --output my-server-jre
```

生成目录可直接作为精简 JRE 部署；JVM 通过 `jrt:/` 访问其中的模块内容。

先用 `jdeps` 分析应用实际需要的 JDK 模块，再交给 `jlink`：

```bash
jdeps --print-module-deps myapp.jar
```

### 服务器场景：去掉 desktop 等模块

无 GUI 的服务端应用通常可以不在自定义 JRE 中包含：

- `java.desktop`（AWT/Swing）
- `java.datatransfer`（不需要剪贴板时）
- `java.sound`（不需要音频时）

具体能删哪些，取决于应用和依赖库的 `module-info.java`；某库若传递 `requires java.desktop`，就不能简单去掉。

### 注意事项

| 点 | 说明 |
| ---- | ---- |
| 完整 JDK 安装 | 磁盘上仍有全部 `.jmod`；省空间靠 `jlink` 或选用精简发行版 |
| `java.base` | 永远需要，无法移除 |
| 传递依赖 | 第三方库间接 `requires` 某模块时，裁剪会失败或运行时报错 |
| 反射 / SPI | 间接用到 AWT 等类时，可能运行期才发现缺模块 |
| Classpath 应用 | 跑在 classpath 上的非模块化 JAR 仍在「未命名模块」，裁剪收益主要在模块化应用 + 定制 JRE |

更多 JDK 9 平台变化见 [JDK 9](../../language/java/jdk-9.md)。

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

```bash
javac -p <module_path> <source>
java -p <module_path> -m <module>/<main_class>
```

应用开发侧使用 modular JAR（见下文 hello world）；JDK 自带模块则以 `.jmod` 形式存放，上文已介绍。

---

[https://www.liaoxuefeng.com/wiki/1252599548343744/1281795926523938](https://www.liaoxuefeng.com/wiki/1252599548343744/1281795926523938)
[https://www.jianshu.com/p/bec282e8fb41](https://www.jianshu.com/p/bec282e8fb41)
[https://developer.51cto.com/art/202007/620291.htm](https://developer.51cto.com/art/202007/620291.htm)

## Java 模块 hello world

### 目录与源码

```bash
mkdir -p src/speaker/com/pingd/test/java/module
vim src/speaker/com/pingd/test/java/module/Hello.java
```

`src/speaker/com/pingd/test/java/module/Hello.java`：

```java
package com.pingd.test.java.module;

public class Hello {
    public static void foo() {
        System.out.println("hello world");
    }
}
```

`src/speaker/module-info.java`（`speaker` 为模块名；`requires` 声明依赖；`exports` 导出到 package 级；`java.base` 自动引入）：

```java
module speaker {
    exports com.pingd.test.java.module;
}
```

`src/app/com/pingd/test/java/module/app/App.java`：

```java
package com.pingd.test.java.module.app;

public class App {
    public static void main(String[] args) {
        com.pingd.test.java.module.Hello.foo();
    }
}
```

`src/app/module-info.java`：

```java
module app {
    requires speaker;
}
```

### 编译与运行

```bash
cd java-module-x
javac -d out --module-source-path src -m speaker
javac -d out --module-source-path src -m app
java --module-path ./out --module app/com.pingd.test.java.module.app.App
```

### 打包 JAR

```bash
jar --create --file speaker.jar -C out/speaker .
jar --create --file app.jar --main-class com.pingd.test.java.module.app.App -C out/app .
java --module-path . --module app
```

### 目录结构

```text
├── out
│   ├── app
│   │   ├── com/.../App.class
│   │   └── module-info.class
│   └── speaker
│       ├── com/.../Hello.class
│       └── module-info.class
└── src
    ├── app/...
    └── speaker/...
```

module-info.java 一般包含以下信息：

- 模块名称
- 该模块依赖的其他模块
- 该模块导出的包或提供的服务

四种模块类型：

- 命名的模块（应用程序模块）：包含 `module-info.java`
- 平台模块：随 JDK 一起发布，同样包含 `module-info.java`
- 自动模块：模块路径上的传统 JAR，无 `module-info.java` 时自动生成
- 未命名的模块：classpath 上的内容

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

### 启用 Java 9 语言支持

```xml
<properties>
  <maven.compiler.release>9</maven.compiler.release>
</properties>
```

属性 maven.compiler.release 直接映射到该 -release 标志javac，而另外两个属性只对IntelliJ有必要 ，用来了解源码兼容性。

### 一个模块示例

[https://blog.csdn.net/rickiyeat/article/details/78068316](https://blog.csdn.net/rickiyeat/article/details/78068316)

### 模块文件 module-info.java

放在和模块名相同的目录下。如果模块名称是 `com.wiloon.java9x`，`module-info.java` 应该放在 `src/com.wiloon.java9x/module-info.java`。

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
    public static void main(String[] args) {
        System.out.println("hello world");
    }
}
```

### 编译模块

```bash
mkdir -p mods/com.wiloon.java9x
javac -d mods/com.wiloon.java9x src/com.wiloon.java9x/module-info.java src/com.wiloon.java9x/com/wiloon/java9x/Java9Tester.java
```

### 运行

```bash
java --module-path mods -m com.wiloon.java9x/com.wiloon.java9x.Java9Tester
```

---

[http://lizhe.name/index.php/node/273](http://lizhe.name/index.php/node/273)

## Java 8 迁移到 Java 9+ 模块

在 `src/main/java` 目录中创建 `module-info.java`。

### Maven plugin

```xml
<properties>
  <maven.jar.plugin.version>3.2.0</maven.jar.plugin.version>
  <maven.dependency.plugin.version>3.1.1</maven.dependency.plugin.version>
</properties>

<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-jar-plugin</artifactId>
  <version>${maven.jar.plugin.version}</version>
  <configuration>
    <outputDirectory>${project.build.directory}/modules</outputDirectory>
  </configuration>
</plugin>
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-dependency-plugin</artifactId>
  <version>${maven.dependency.plugin.version}</version>
  <executions>
    <execution>
      <phase>package</phase>
      <goals>
        <goal>copy-dependencies</goal>
      </goals>
      <configuration>
        <outputDirectory>${project.build.directory}/modules</outputDirectory>
        <includeScope>runtime</includeScope>
      </configuration>
    </execution>
  </executions>
</plugin>
```

## Jigsaw hello world

`git@github.com:wiloon/java9x.git`

- [OneAPM: Jigsaw hello world](http://blog.oneapm.com/apm-tech/724.html)
- [Stack Overflow: unrecognized option --module-path](http://stackoverflow.com/questions/39882669/unrecognized-option-modulepath)

```bash
java --module-path mods -m com.mycompany.helloworld/com.mycompany.helloworld.HelloWorld
```

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-21 | 文件重命名为 `jpms-jigsaw.md`；title/url 加入 JPMS 关键字 | 区分 Jigsaw 项目代号与 JPMS 规范名，便于检索 |
| 2026-06-21 | 新增「JMOD 文件」小节；删除 `-p & -m` 段落后重复的 jmod 说明 | 补充 jmod 格式与 modular JAR 的区别 |
| 2026-06-21 | 新增「按需加载与 jlink」小节 | 补充运行时按需加载、服务器裁剪 desktop 模块与 jlink 用法 |
| 2026-06-21 | 整理空行与列表格式；去掉与 title 重复的二级标题 | 提升可读性 |
| 2026-06-21 | 删除「jlink 放在哪讲」；关系说明并入 jlink 小节 | 去掉编辑讨论残留，保留读者向内容 |
