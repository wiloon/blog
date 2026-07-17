---
title: "JDK Tools: 命令行工具现状与过时工具"
author: "-"
date: 2017-02-06T00:31:53+00:00
lastmod: 2026-07-16T05:40:00+08:00
url: jdk-tool
categories:
  - language
tags:
  - java
  - jvm
  - jdk-tools
  - remix
  - AI-assisted
aliases:
  - /p9713/
---

JDK 自带的命令行工具随着版本演进变化很大：CORBA、JAX-WS/JAXB、Java Web Start 等整套技术栈在 JDK 11 前后被移除，一批老工具也随之消失；同时 `jshell`、`jlink`、`jpackage`、`jhsdb` 等是后来才加入的。本文按「现在还在用」「名存实亡」「已从 JDK 移除」三类整理，方便判断一个工具在 JDK 26 上还值不值得用。

## 仍在用的核心工具

| 分类 | 工具 | 用途 |
| ---- | ---- | ---- |
| 编译与运行 | `java` | 运行 class/jar，也可直接运行单文件源码 |
| 编译与运行 | `javac` | 编译 Java 源码 |
| 编译与运行 | `jshell` | REPL，交互式执行 Java 代码（JDK 9 引入） |
| 打包与模块 | `jar` | 打包/解包 jar 文件 |
| 打包与模块 | `jlink` | 生成裁剪后的自定义运行时镜像（JDK 9 引入） |
| 打包与模块 | `jmod` | 创建和查看 jmod 模块文件（JDK 9 引入） |
| 打包与模块 | `jpackage` | 生成平台原生安装包（JDK 14 引入，见下文 `javapackager` 的替代） |
| 签名与安全 | `jarsigner` | jar 签名与验证 |
| 签名与安全 | `keytool` | 密钥、证书管理 |
| 文档与静态分析 | `javadoc` | 生成 API 文档 |
| 文档与静态分析 | `javap` | 反汇编 class 文件 |
| 文档与静态分析 | `jdeps` | 分析类/模块依赖关系（JDK 8 引入） |
| 文档与静态分析 | `jdeprscan` | 扫描代码中用到的已废弃 API（JDK 9 引入） |
| 文档与静态分析 | `jnativescan` | 扫描 FFM API（`java.lang.foreign`）受限方法调用（JDK 22 引入） |
| 诊断与监控 | `jcmd` | 向运行中的 JVM 发送诊断命令，官方现在推荐的统一入口，详见 [jcmd](./jcmd.md) |
| 诊断与监控 | `jconsole` | 图形化 JMX 监控 |
| 诊断与监控 | `jfr` | Flight Recorder 命令行工具，详见 [Java Flight Recorder](./java-flight-recorder-jfr.md) |
| 诊断与监控 | `jhsdb` | HotSpot Serviceability Agent 统一入口，整合了旧版 `jsadebugd`/SA 调试功能（JDK 9 引入） |
| 诊断与监控 | `jps` | 列出本机 JVM 进程 |
| 诊断与监控 | `jstat` / `jstatd` | JVM 统计信息采集 / 远程统计信息服务 |
| 诊断与监控 | `jwebserver` | 内置的简单静态文件 HTTP 服务器（JDK 18 引入） |
| 调试 | `jdb` | 命令行调试器 |
| RMI | `rmiregistry` | RMI 远程对象注册表 |
| 脚本 | `jrunscript` | 命令行脚本外壳工具，见下文「名存实亡」 |
| 其它签名工具 | `serialver` | 生成 `serialVersionUID` |
| Windows 专属 | `javaw` | 不弹控制台窗口运行 Java 程序 |
| Windows 专属 | `jabswitch` / `jaccessinspector` / `jaccesswalker` | Java Access Bridge 开关与辅助功能检查工具 |
| Kerberos | `kinit` / `klist` / `ktab` | Kerberos 票据与密钥表管理 |

## 名存实亡：还在但不建议依赖

这几个工具**没有被移除**，仍出现在最新 JDK 的工具列表里，但官方已经不建议把它们当作首选：

| 工具 | 现状 |
| ---- | ---- |
| `jstack` / `jmap` / `jinfo` | Oracle 文档标注为 experimental、no compatibility guarantee，功能已被 `jcmd` 覆盖（如 `jcmd <pid> Thread.print`、`jcmd <pid> GC.heap_dump`），详见 [jstack](../../cs/jstack.md) |
| `jrunscript` | 历史上默认靠 Nashorn 引擎执行 JavaScript；Nashorn 在 JDK 15 被移除后，`jrunscript` 本身没删，但默认没有可用的 JS 引擎，需要自行在 classpath 放一个 JSR 223 脚本引擎才能用 |
| `jmc`（JDK Mission Control） | JDK 11 起不再随 JDK 一起分发，需要单独下载；作为 JFR 数据的离线分析界面依然是官方推荐工具 |
| `jvisualvm`（VisualVM） | JDK 9 起移出 JDK 发行包，独立成开源项目；本地临时排查可用，生产环境更推荐 JFR + JMC + async-profiler，详见 [VisualVM](./visualvm.md) |

## 已从 JDK 移除的过时工具

以下工具在对应版本之后已经从 JDK 里彻底删除，不要再基于它们写新脚本或文档：

| 工具 | 原用途 | 移除版本 | 现在怎么做 |
| ---- | ------ | -------- | ---------- |
| `apt` | 注解处理工具 | JDK 8（JEP 117） | 用 `javac` 内置的 Annotation Processing（`-processor`） |
| `jhat` | 堆快照分析 | JDK 9（JEP 241） | 用 `jmap`/`jcmd` 生成 heap dump，再用 Eclipse MAT 或 VisualVM 分析 |
| `extcheck` | 检测扩展 jar 版本冲突 | JDK 9 | 扩展机制（`ext` 目录）本身已随模块化废弃 |
| `native2ascii` | 文本编码与 ASCII/Unicode 转义互转 | JDK 9 | 资源文件直接用 UTF-8，无需转换 |
| `java-rmi.exe` / `java-rmi.cgi` | 浏览器触发 RMI 类加载的辅助程序 | JDK 9/10 | 该机制已废弃，不再使用 |
| `jsadebugd` | 独立的远程调试代理守护进程 | JDK 9 起被 `jhsdb debugd` 取代 | 用 `jhsdb debugd` |
| `javah` | 生成 JNI C/C++ 头文件 | JDK 10（JEP 313） | 用 `javac -h` |
| `policytool` | 图形化编辑权限策略文件 | JDK 10 | 直接手写 `.policy` 文本文件 |
| `appletviewer` | 运行浏览器 Applet | JDK 11 | Applet 技术已彻底废弃 |
| `javaws` / Java Web Start / Java Plugin | 从网页下载运行 Java 应用 | JDK 11 | 改用普通桌面安装包，见 `jpackage` |
| `javapackager` | 打包可执行程序（随 JavaFX） | JDK 11 | 用 `jpackage`（JDK 14 引入，JEP 343） |
| `idlj` / `orbd` / `servertool` / `tnameserv` | CORBA 相关工具 | JDK 11（JEP 320） | CORBA 已从 JDK 移除，需要用第三方 ORB 实现 |
| `schemagen` / `xjc` | JAXB（XML 数据绑定） | JDK 11（JEP 320） | 改用独立发布的 JAXB/Jakarta XML Binding 参考实现 |
| `wsgen` / `wsimport` | JAX-WS（Web Service 客户端/服务端生成） | JDK 11（JEP 320） | 改用独立发布的 JAX-WS/Jakarta XML Web Services 实现 |
| `pack200` / `unpack200` | JAR 高效压缩传输 | JDK 14（JEP 367，JDK 11 弃用） | 现代带宽下已无必要，直接传输普通 jar |
| `jjs` | 运行 JavaScript（Nashorn 引擎） | JDK 15（随 Nashorn 一起移除） | 需要嵌入式 JS 可用 GraalVM 或独立 Nashorn 库 |
| `rmic` | 生成 RMI stub/skeleton | JDK 15 | 动态代理早已替代静态 stub 生成，无需 `rmic` |

## 参考

- [https://docs.oracle.com/en/java/javase/25/docs/specs/man/](https://docs.oracle.com/en/java/javase/25/docs/specs/man/)
- [https://docs.oracle.com/en/java/javase/17/migrate/removed-tools-and-components.html](https://docs.oracle.com/en/java/javase/17/migrate/removed-tools-and-components.html)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-07-16 | 标题、分类改为 `language`；标签由 `reprint` 改为 `remix` + `AI-assisted`；全文按「仍在用」「名存实亡」「已移除」三类重新整理，逐条核实每个工具的移除版本（JEP 编号）；删除与 JDK 无关的「packager（微软对象包装程序）」条目；补充 `jshell`/`jlink`/`jpackage`/`jhsdb`/`jfr` 等后来加入的工具 | 原文是 2017 年按官方文档逐条翻译的工具清单，未反映 JDK 9~15 期间大量工具被移除的现状，用户想知道哪些工具已过时不建议使用 |
