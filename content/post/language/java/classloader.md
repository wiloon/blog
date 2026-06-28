---
title: Java ClassLoader
author: "-"
date: 2011-09-09T09:16:20+00:00
lastmod: 2026-06-28T07:12:53+08:00
url: classloader
categories:
  - language
tags:
  - AI-assisted
  - classloader
  - java
  - jvm
  - remix
---

## 概述

不同 JVM 实现细节各异，下文只讨论 **HotSpot** 在 **JDK 9 及以后**（含当前 JDK 26）的行为。JDK 8 及更早的 `ExtClassLoader`、`jre/lib/ext`、`sun.misc.Launcher` 等表述见文末「JDK 8 及更早」。

本文从四方面展开：内置 ClassLoader 层次、双亲委托、自定义 ClassLoader、打破双亲委托的常见场景。类加载器「去哪里找类」由 classpath / module path 决定，概念见 [Java Classpath 与 Module Path](./classpath.md)。

## 内置 ClassLoader 层次

JDK 运行时提供三个内置加载器（[ClassLoader 官方文档](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/lang/ClassLoader.html)）：

| 加载器 | 获取方式 | 职责 |
| ---- | ---- | ---- |
| **Bootstrap** | Java 代码中为 `null` | 加载 `java.base` 等核心模块；C++ 实现，不是 `ClassLoader` 子类 |
| **Platform**（原 Extension） | `ClassLoader.getPlatformClassLoader()` | 加载 Java SE 平台 API 及其模块（非应用 classpath） |
| **System / Application** | `ClassLoader.getSystemClassLoader()` | 加载应用 classpath、module path 上的类 |

父子关系：

```text
Bootstrap (null)
    └── PlatformClassLoader
            └── AppClassLoader (System ClassLoader)
```

实现类位于 `jdk.internal.loader.ClassLoaders`（`PlatformClassLoader`、`AppClassLoader`），均为内部 `BuiltinClassLoader` 体系。**不要**依赖具体类名写业务逻辑。

### Bootstrap ClassLoader

- 虚拟机内置，**没有** Java 父加载器；在 `getParent()` 链上用 `null` 表示。
- 由 C++ 实现，不继承 `java.lang.ClassLoader`，无法在 Java 里直接拿到实例。
- JDK 9 起通过**模块系统**加载核心库（如 `java.base` 中的 `java.lang.*`），不再从 `rt.jar` 或 `%JAVA_HOME%/jre/lib` 整包加载。

### PlatformClassLoader

- JDK 9 起取代 **ExtClassLoader**（扩展类加载器）。
- 负责 Java SE **平台类**：平台 API、其实现类，以及 JCP 标准化但不在 SE 核心里的模块。
- 平台类**由哪个加载器定义**（Bootstrap 或 Platform）因模块而异，应用代码不应假设「某个平台类一定由 Platform 加载」。
- 为支持模块升级/覆盖，Platform 有时需要委托给 System 等其它加载器，可见性比 JDK 8 的纯树形委托更灵活。

### AppClassLoader（System ClassLoader）

- `ClassLoader.getSystemClassLoader()` 的返回值，也是默认的 **context class loader** 来源之一。
- 加载应用 classpath、module path，以及部分 JDK 工具模块（如 `jdk.compiler`）。
- 线程上下文类加载器（`Thread.setContextClassLoader`）常用于 SPI 等场景（见下文）。

### 与 URLClassLoader 的关系

JDK 8 中 AppClassLoader、ExtClassLoader 继承 `java.net.URLClassLoader`。**JDK 9 起内置加载器不再继承 URLClassLoader**；自定义加载器仍可用 `URLClassLoader` 或继承 `ClassLoader` 自行实现 `findClass`。

### 查看当前层次

```java
public class ClassLoaderProbe {
    public static void main(String[] args) {
        ClassLoader ctx = Thread.currentThread().getContextClassLoader();
        ClassLoader sys = ClassLoader.getSystemClassLoader();
        ClassLoader platform = ClassLoader.getPlatformClassLoader();

        System.out.println("context:  " + ctx);
        System.out.println("system:   " + sys);
        System.out.println("platform: " + platform);
        System.out.println("system.parent:   " + sys.getParent());
        System.out.println("platform.parent: " + platform.getParent()); // null => Bootstrap
    }
}
```

在 JDK 26 上典型输出类似：

```text
system:   jdk.internal.loader.ClassLoaders$AppClassLoader@...
platform: jdk.internal.loader.ClassLoaders$PlatformClassLoader@...
system.parent:   jdk.internal.loader.ClassLoaders$PlatformClassLoader@...
platform.parent: null
```

## 双亲委托模型

加载类时，`ClassLoader` 默认采用 **parent-first（双亲委托）**：

1. 查当前加载器是否已加载（`findLoadedClass`）。
2. 未命中则委托 **父加载器** 加载（父加载器递归同样流程，直到 Bootstrap）。
3. 父链都未加载到时，由 **当前加载器** 执行 `findClass`（或内置加载器的等价逻辑）并缓存。

### 为什么要委托

JVM 里类的身份是 **全限定名 + 定义该类的 ClassLoader**（命名空间）。同名类被不同加载器加载，在 JVM 中是**两个不同的 `Class`**。

委托模型保证 `java.util.HashMap` 等核心类由 Bootstrap（或平台模块路径）统一加载，应用里的多个自定义加载器共享同一份 JDK 类型，避免「同名不同类」的混乱。

### loadClass 如何实现委托

`loadClass(String, boolean)` 未被 `final` 修饰，子类可以 override，从而打破双亲委托。默认实现逻辑（简化，与 JDK 26 源码一致）：

```java
protected Class<?> loadClass(String name, boolean resolve) throws ClassNotFoundException {
    synchronized (getClassLoadingLock(name)) {
        Class<?> c = findLoadedClass(name);
        if (c == null) {
            if (parent != null) {
                c = parent.loadClass(name, false);
            } else {
                c = findBootstrapClassOrNull(name);
            }
            if (c == null) {
                c = findClass(name);
            }
        }
        if (resolve) {
            resolveClass(c);
        }
        return c;
    }
}
```

自定义加载器若**遵循**双亲委托，通常只 override `findClass`；若 override `loadClass`，则完全自行控制委托顺序。

### findClass 与 defineClass

- **`findClass`**：默认抛 `ClassNotFoundException`，留给子类实现（从磁盘、网络、内存等读取字节码）。
- **`defineClass`**：`final`，是 JVM 校验并注册 `Class` 对象的入口；字节码须符合 class 文件格式。

能否用自定义加载器替换 `java.lang.String`？**不能**。即使打破双亲委托，`ClassLoader` 对 `java.*` 等包有访问检查，且 Bootstrap 已加载的核心类不会被应用加载器重新定义。

## 打破双亲委托的场景

### SPI 与线程上下文类加载器

JDBC、JNDI 等 **SPI** 的接口在 JDK（Bootstrap / Platform）里，实现 JAR 在应用 classpath 上。接口侧无法直接 `Class.forName` 到厂商实现，因此使用 **`Thread.currentThread().getContextClassLoader()`**（默认多为 AppClassLoader）由「子侧」加载 SPI 实现。这是典型的 **父加载器需要子加载器已加载的类** 的反常情况。

### 模块化与 OSGi、应用服务器

OSGi、部分 Java EE / 应用服务器会为每个模块/部署单元使用独立 ClassLoader，并采用 **child-first** 或扁平委托，不再严格 parent-first。

## 自定义 ClassLoader 简要流程

1. **定位字节码**（classpath、URL、数据库等）。
2. **`defineClass`** 将字节注册为 `Class`。
3. 用 `Class.getDeclaredConstructor().newInstance()` 等创建实例（勿用已废弃的 `Class.newInstance()`）。

```java
URL url = new URL("file:/path/to/classes/");
URLClassLoader loader = new URLClassLoader(new URL[] { url });
Class<?> clazz = loader.loadClass("com.example.Student");
Object stu = clazz.getDeclaredConstructor().newInstance();
```

## 不同 ClassLoader：谁能看到谁

JVM 里类的身份是 **全限定名 + 定义该类的 ClassLoader**（上文「命名空间」）。因此：

| 关系 | 可见性 |
| ---- | ------ |
| 子加载器 → 父加载器已加载的类 | **可见**（双亲委托：先让父加载） |
| 父加载器 → 子加载器加载的类 | **默认不可见** |
| 两个无父子关系的加载器（兄弟） | **互不可见**（各自命名空间），除非用反射等方式桥接 |

「互相看不到」指的是：**不能用 `Foo.class` 直接当同一个类型用**（`instanceof`、赋值会失败），不是进程里完全没有这份字节码。

自定义 `URLClassLoader` 加载的 `com.app.Plugin` 与 AppClassLoader 加载的 `com.app.Plugin`，在 JVM 里是 **两个不同的 Class**。

### 与 Java Agent 的关系

[Attach](./attach-api.md) `loadAgent` 后，**agent JAR 里的类** 通常不走业务 AppClassLoader 去 `loadClass`，而是由 JVM 的 agent 机制装入（与业务 classpath 分离，减少版本冲突）。

但这 **不意味着** agent 与业务「完全隔离、改不了业务」：

- **`Instrumentation` + `ClassFileTransformer`** 改的是 **业务类对应的字节码**（定义类仍由业务 ClassLoader 加载，只是 `retransform` 换了方法体里的指令）。
- 织入的探针里可以 `INVOKESTATIC` 到 agent 包里的类，或读写业务对象——运行时都在 **同一进程**。

详见 [Java ASM 与运行时字节码织入](./java-asm.md)、[BTrace](./btrace.md)。

## JDK 8 及更早（历史参考）

| 现代名称 | JDK 8 及更早 |
| ---- | ---- |
| PlatformClassLoader | ExtClassLoader（`sun.misc.Launcher$ExtClassLoader`） |
| AppClassLoader | `sun.misc.Launcher$AppClassLoader` |
| 平台模块 | `%JAVA_HOME%/jre/lib/ext`、`java.ext.dirs` |
| 核心库 | `rt.jar`、`sun.boot.class.path` |
| 内置加载器基类 | 二者均继承 `URLClassLoader` |

JDK 9 引入模块系统后，上述路径与类名在 HotSpot 中已废弃或仅作兼容；学习新项目应以本文「内置 ClassLoader 层次」一节为准。

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-21 | 按 JDK 9+ / Java 26 重写内置加载器、双亲委托与示例；删除 JDK 8 / 外文转载冗余段落；合并 PlatformClassLoader 说明 | 原文 ExtClassLoader、URLClassLoader、jre/lib/ext 等与现行 HotSpot 不符 |
| 2026-06-28 | 概述补充 classpath / module path 概念链到新建 [classpath.md](./classpath.md) | 拆分 classpath 概念专文，java-classloader-2.md 退役合并至此 |
