---
title: JDK 17
author: "-"
date: 2026-04-25T10:27:40+08:00
lastmod: 2026-06-20T12:53:11+08:00
url: jdk-17
categories:
  - language
tags:
  - java
  - jdk
  - remix
  - AI-assisted
aliases:
  - jdk17-new-features
  - jdk17-features
---

## 概述

JDK 17 是 Java 的**长期支持版本（LTS）**，于 2021 年 9 月发布。上一个 LTS 是 **JDK 11**（2018 年 9 月）；中间 JDK 12～16 为半年一发的**短期特性版本**，每版引入少量 JEP，最终在 JDK 17 汇总为新的 LTS 基线。

从 JDK 11 直接跳到 JDK 17 时，需要关注的不只是 JDK 17 当版的 14 个 JEP，还包括 12～16 中已转正的语言特性（`switch` 表达式、文本块、`record`、模式匹配等）以及 JVM、工具链方面的累积变化。版本节奏与 LTS 策略见 [Java 版本历史](./java-version-history.md)。

## 版本路线（JDK 11 → JDK 17）

| 版本 | 发布日期 | 类型 | JEP 数 |
| ---- | -------- | ---- | ------ |
| JDK 11 | 2018-09 | **LTS** | 17 |
| JDK 12 | 2019-03 | 短期 | 8 |
| JDK 13 | 2019-09 | 短期 | 5 |
| JDK 14 | 2020-03 | 短期 | 16 |
| JDK 15 | 2020-09 | 短期 | 14 |
| JDK 16 | 2021-03 | 短期 | 17 |
| **JDK 17** | **2021-09** | **LTS** | **14** |

---

## JDK 12（2019-03）

| JEP | 特性 | 说明 |
| --- | ---- | ---- |
| [189](https://openjdk.org/jeps/189) | Shenandoah GC（实验） | 低延迟 GC，首次以实验特性引入 |
| [230](https://openjdk.org/jeps/230) | 微基准测试套件 | JMH 纳入 JDK，便于性能基准编写 |
| [325](https://openjdk.org/jeps/325) | `switch` 表达式（预览） | `switch` 可作表达式返回值，支持 `yield` |
| [334](https://openjdk.org/jeps/334) | JVM 常量 API | `java.lang.constant` 包，描述 nominal 常量 |
| [340](https://openjdk.org/jeps/340) | 统一 AArch64 端口 | 合并 32/64 位 ARM 端口实现 |
| [341](https://openjdk.org/jeps/341) | 默认 CDS 归档 | 安装时生成默认 class 数据共享归档，缩短启动时间 |
| [344](https://openjdk.org/jeps/344) | G1 可中止混合回收 | 混合 GC 周期过长时可中止，降低停顿风险 |
| [346](https://openjdk.org/jeps/346) | G1 及时归还空闲内存 | 空闲堆内存更快归还给操作系统 |

---

## JDK 13（2019-09）

| JEP | 特性 | 说明 |
| --- | ---- | ---- |
| [350](https://openjdk.org/jeps/350) | 动态 CDS 归档 | 应用退出时生成定制 CDS 归档，进一步加速启动 |
| [351](https://openjdk.org/jeps/351) | ZGC 归还未用内存 | ZGC 将未使用堆页归还给 OS |
| [353](https://openjdk.org/jeps/353) | 重写旧版 Socket API | `Socket`/`ServerSocket` 底层实现现代化 |
| [354](https://openjdk.org/jeps/354) | `switch` 表达式（第二次预览） | 语法与行为微调 |
| [355](https://openjdk.org/jeps/355) | 文本块（预览） | 多行字符串字面量，三引号 `"""` 语法 |

---

## JDK 14（2020-03）

### 语言特性

| JEP | 特性 | 说明 |
| --- | ---- | ---- |
| [305](https://openjdk.org/jeps/305) | `instanceof` 模式匹配（预览） | 在 `instanceof` 中直接绑定变量 |
| [361](https://openjdk.org/jeps/361) | **`switch` 表达式（正式）** | 预览两轮后转正，可替代传统 `switch` 语句 |
| [359](https://openjdk.org/jeps/359) | `record`（预览） | 不可变数据载体，紧凑语法 |
| [368](https://openjdk.org/jeps/368) | 文本块（第二次预览） | 转义规则与缩进处理改进 |

`switch` 表达式示例：

```java
String dayType = switch (day) {
    case MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY -> "工作日";
    case SATURDAY, SUNDAY -> "周末";
    default -> throw new IllegalArgumentException("无效日期");
};
```

`instanceof` 模式匹配（预览阶段）示例：

```java
if (obj instanceof String s) {
    System.out.println(s.length());
}
```

### JVM、平台与工具

| JEP | 特性 | 说明 |
| --- | ---- | ---- |
| [343](https://openjdk.org/jeps/343) | 打包工具（孵化） | `jpackage` 首次以孵化 API 引入 |
| [345](https://openjdk.org/jeps/345) | G1 NUMA 感知分配 | 多插槽机器上优化 G1 内存布局 |
| [349](https://openjdk.org/jeps/349) | JFR 事件流 | 持续消费 JFR 事件，无需先写文件 |
| [352](https://openjdk.org/jeps/352) | 非易失性映射字节缓冲区 | 支持 NVRAM 上的 `MappedByteBuffer` |
| [358](https://openjdk.org/jeps/358) | 更友好的 NPE 信息 | 空指针异常附带更精确的空引用位置 |
| [362](https://openjdk.org/jeps/362) | 废弃 Solaris/SPARC 端口 | 后续在 JDK 15 移除 |
| [363](https://openjdk.org/jeps/363) | **移除 CMS 收集器** | Concurrent Mark Sweep GC 正式删除 |
| [364](https://openjdk.org/jeps/364) | ZGC 支持 macOS | |
| [365](https://openjdk.org/jeps/365) | ZGC 支持 Windows | |
| [366](https://openjdk.org/jeps/366) | 废弃 Parallel Scavenge + Serial Old 组合 | |
| [367](https://openjdk.org/jeps/367) | 移除 Pack200 | 工具与 API 一并删除 |
| [370](https://openjdk.org/jeps/370) | 外部内存访问 API（孵化） | Panama 项目，JNI 替代方向 |

---

## JDK 15（2020-09）

### 语言特性

| JEP | 特性 | 说明 |
| --- | ---- | ---- |
| [360](https://openjdk.org/jeps/360) | 密封类（预览） | `sealed`/`permits` 限制继承层次 |
| [375](https://openjdk.org/jeps/375) | `instanceof` 模式匹配（第二次预览） | |
| [378](https://openjdk.org/jeps/378) | **文本块（正式）** | 多行字符串定稿 |
| [384](https://openjdk.org/jeps/384) | `record`（第二次预览） | |

文本块示例：

```java
String json = """
        {
          "name": "Java",
          "version": 17
        }
        """;
```

### JVM、平台与工具

| JEP | 特性 | 说明 |
| --- | ---- | ---- |
| [339](https://openjdk.org/jeps/339) | EdDSA 签名算法 | `Signature` 支持 Edwards 曲线 |
| [371](https://openjdk.org/jeps/371) | 隐藏类 | 框架动态生成、不可发现的类 |
| [372](https://openjdk.org/jeps/372) | **移除 Nashorn** | JDK 内置 JavaScript 引擎删除 |
| [373](https://openjdk.org/jeps/373) | 重写 DatagramSocket API | 与 Socket 重写（JEP 353）配套 |
| [374](https://openjdk.org/jeps/374) | 禁用并废弃偏向锁 | 现代多线程负载下收益有限 |
| [377](https://openjdk.org/jeps/377) | **ZGC 生产就绪** | 低延迟 GC 脱离实验状态 |
| [379](https://openjdk.org/jeps/379) | **Shenandoah 生产就绪** | 与 JDK 12 实验引入对应 |
| [381](https://openjdk.org/jeps/381) | 移除 Solaris/SPARC 端口 | |
| [383](https://openjdk.org/jeps/383) | 外部内存访问 API（第二次孵化） | |
| [385](https://openjdk.org/jeps/385) | 废弃 RMI Activation | JDK 17 移除（JEP 407） |

---

## JDK 16（2021-03）

### 语言特性

| JEP | 特性 | 说明 |
| --- | ---- | ---- |
| [394](https://openjdk.org/jeps/394) | **`instanceof` 模式匹配（正式）** | 预览两轮后转正 |
| [395](https://openjdk.org/jeps/395) | **`record`（正式）** | 不可变数据类定稿 |
| [397](https://openjdk.org/jeps/397) | 密封类（第二次预览） | |

`record` 示例：

```java
public record Point(int x, int y) {}

Point p = new Point(1, 2);
System.out.println(p.x()); // 1
```

### JVM、平台与工具

| JEP | 特性 | 说明 |
| --- | ---- | ---- |
| [338](https://openjdk.org/jeps/338) | 向量 API（孵化） | SIMD 向量计算 |
| [347](https://openjdk.org/jeps/347) | 启用 C++14 | HotSpot 源码构建要求 |
| [357](https://openjdk.org/jeps/357) | 迁移到 Git | 版本控制从 Mercurial 切换 |
| [369](https://openjdk.org/jeps/369) | 迁移到 GitHub | OpenJDK 托管平台变更 |
| [376](https://openjdk.org/jeps/376) | ZGC 并发线程栈处理 | 降低 ZGC 停顿 |
| [380](https://openjdk.org/jeps/380) | Unix 域套接字通道 | `SocketChannel` 支持 AF_UNIX |
| [386](https://openjdk.org/jeps/386) | Alpine Linux 端口 | 容器镜像常用发行版 |
| [387](https://openjdk.org/jeps/387) | Elastic Metaspace | 元空间按需伸缩、及时归还 |
| [388](https://openjdk.org/jeps/388) | Windows/AArch64 端口 | |
| [389](https://openjdk.org/jeps/389) | 外部函数链接器 API（孵化） | Panama，调用原生函数 |
| [390](https://openjdk.org/jeps/390) | 值类型类警告 | 对 `Integer` 等误用同步发出警告 |
| [392](https://openjdk.org/jeps/392) | **打包工具（正式）** | `jpackage` 转正 |
| [393](https://openjdk.org/jeps/393) | 外部内存访问 API（第三次孵化） | |
| [396](https://openjdk.org/jeps/396) | 默认强封装 JDK 内部 API | `sun.*` 等默认不可访问；JDK 17 由 JEP 403 最终定稿 |

---

## JDK 17（2021-09，LTS）

### 语言特性

| JEP | 特性 | 说明 |
| --- | ---- | ---- |
| [409](https://openjdk.org/jeps/409) | **密封类（正式）** | 预览两轮后转正 |
| [406](https://openjdk.org/jeps/406) | `switch` 模式匹配（预览） | 在 `switch` 中对类型/值做模式匹配 |

#### 密封类（JEP 409）

密封类和密封接口用来**限制哪些类可以继承或实现某个类/接口**。

Java 原有两个极端：`final` 类完全不能继承，普通类/接口任何人都能继承，缺少「只允许指定的几个子类」这个中间选项。密封类主要解决：

**1. 模式匹配的穷举性检查**

没有密封类时，`switch` 无法知道所有子类，必须写 `default`，漏掉某种情况编译器不报错：

```java
// 旧写法：漏掉 Triangle 也不报错
String desc = switch (shape) {
    case Circle c -> "圆";
    case Rectangle r -> "矩形";
    default -> "未知";  // 掩盖了遗漏
};

// 密封类：漏掉 Triangle 编译器直接报错
String desc = switch (shape) {
    case Circle c -> "圆";
    case Rectangle r -> "矩形";
    // 编译错误：缺少 Triangle
};
```

**2. 表达领域约束**

某些业务类型天然有固定变体，密封类可以在类型系统层面强制表达这种约束，而不只是靠文档约定。

**3. 比枚举更强**

枚举每个值只是单例，无法携带不同的字段；密封类每种子类可以有完全不同的结构：

```java
sealed interface PaymentResult permits Success, Failure, Pending {}

record Success(String transactionId, BigDecimal amount) implements PaymentResult {}
record Failure(String errorCode, String message) implements PaymentResult {}
record Pending(String trackingId) implements PaymentResult {}
```

核心关键字：

- `sealed` — 声明该类/接口是密封的
- `permits` — 列出允许继承的子类
- 子类必须选择三者之一：
  - `final` — 不能再被继承
  - `sealed` — 继续密封，再限制下一级
  - `non-sealed` — 开放，任何人都可以继承

```java
public sealed interface Shape
    permits Circle, Rectangle, Triangle {}

public final class Circle implements Shape {
    double radius;
}

public final class Rectangle implements Shape {
    double width, height;
}

public non-sealed class Triangle implements Shape {
    double base, height;
}
```

配合 `switch` 表达式，编译器知道所有可能的子类型，可做完整性检查：

```java
double area = switch (shape) {
    case Circle c    -> Math.PI * c.radius * c.radius;
    case Rectangle r -> r.width * r.height;
    case Triangle t  -> 0.5 * t.base * t.height;
};
```

### JVM、平台与工具

| JEP | 特性 | 说明 |
| --- | ---- | ---- |
| [306](https://openjdk.org/jeps/306) | 恢复始终严格浮点语义 | 浮点运算恢复一致严格模式，`strictfp` 语义简化 |
| [356](https://openjdk.org/jeps/356) | 增强型伪随机数生成器 | 新增 `RandomGenerator` 接口及多种算法实现 |
| [382](https://openjdk.org/jeps/382) | macOS Metal 渲染管道 | Java 2D 在 macOS 上用 Metal 替代 OpenGL |
| [391](https://openjdk.org/jeps/391) | macOS/AArch64 移植 | 原生支持 Apple Silicon（M 系列芯片） |
| [398](https://openjdk.org/jeps/398) | 废弃 Applet API | 标记 `@Deprecated(forRemoval = true)` |
| [403](https://openjdk.org/jeps/403) | 强封装 JDK 内部 API | 延续 JEP 396，封闭 `sun.*` 等内部包 |
| [407](https://openjdk.org/jeps/407) | 移除 RMI Activation | `java.rmi.activation` 包删除 |
| [410](https://openjdk.org/jeps/410) | 移除实验性 AOT/JIT 编译器 | 基于 Graal 的实验编译器移除 |
| [411](https://openjdk.org/jeps/411) | 废弃安全管理器 | `SecurityManager` 标记待移除 |
| [412](https://openjdk.org/jeps/412) | 外部函数与内存 API（孵化） | Panama 第四次孵化，JNI 替代方向 |
| [414](https://openjdk.org/jeps/414) | 向量 API（第二次孵化） | SIMD 向量计算持续演进 |
| [415](https://openjdk.org/jeps/415) | 上下文反序列化过滤器 | 按上下文设置 Java 反序列化白名单 |

增强型随机数生成器示例：

```java
RandomGenerator generator = RandomGeneratorFactory.of("L64X128MixRandom").create();
int randomInt = generator.nextInt(100);
```

外部函数与内存 API（孵化）示例：

```java
try (MemorySegment segment = MemorySegment.allocateNative(100)) {
    // operate on off-heap memory
}
```

---

## 语言特性演进小结（JDK 12 → 17）

| 特性 | JDK 12 | JDK 13 | JDK 14 | JDK 15 | JDK 16 | JDK 17 |
| ---- | ------ | ------ | ------ | ------ | ------ | ------ |
| `switch` 表达式 | 预览 | 预览 | **正式** | | | |
| 文本块 | | 预览 | 预览 | **正式** | | |
| `instanceof` 模式匹配 | | | 预览 | 预览 | **正式** | |
| `record` | | | 预览 | 预览 | **正式** | |
| 密封类 | | | | 预览 | 预览 | **正式** |
| `switch` 模式匹配 | | | | | | 预览 |

从 JDK 11 升级到 JDK 17 时，上表中标为**正式**的特性均无需 `--enable-preview` 即可使用。

---

## 版本信息

- 发布日期：2021 年 9 月 14 日
- LTS 版本；上一个 LTS 为 JDK 11
- JDK 17 当版 JEP 数量：14 个
- Class 文件 major version：61

### Oracle 官方支持周期

| 阶段               | 截止时间         | 说明                                                                   |
| ------------------ | ---------------- | ---------------------------------------------------------------------- |
| Premier Support    | 2026 年 9 月     | 全面支持：bug 修复、安全补丁、新功能更新、性能改进                     |
| Extended Support   | 2029 年 9 月     | 仅安全补丁和关键 bug 修复，不引入新功能，Oracle JDK 用户通常需额外付费 |
| Sustaining Support | 2029 年 9 月之后 | 无限期，仅提供已有补丁的访问，不再产出新补丁                           |

## 从 JDK 17 升级到 JDK 21 的策略

JDK 17 的 Premier Support 于 2026 年 9 月到期，下一个 LTS 版本是 JDK 21。推荐采用三阶段迁移，而非一步到位：

### 阶段一：替换废弃 API（在 JDK 17 上完成）

1. 用 `jdeprscan --release 21` 扫描废弃 API 使用情况
2. 替换 `SecurityManager`、`finalize()`、`Thread.stop()` 等将被移除的 API
3. 检查所有未显式指定字符集的代码（如 `new String(bytes)`、`new FileReader(file)`），统一改为 `StandardCharsets.UTF_8`——JDK 18 起默认字符集改为 UTF-8，这是最常见的隐性 breaking change

### 阶段二：升级第三方库（仍在 JDK 17 上运行）

找到同时兼容 JDK 17 和 JDK 21 的库版本作为过渡版本，逐库升级，不要一次全换：

- Spring Boot → 3.2+（同时支持 JDK 17 和 JDK 21）
- Mockito → 5.x
- ByteBuddy → 1.14+
- 其他字节码增强类框架同步升级

升级后部署上线，稳定运行一段时间再进行下一阶段。

### 阶段三：升级 JDK 到 21

代码和依赖都已验证稳定后，切换 JDK 版本，代码不动：

1. 跑完整测试套件
2. 上线，观察 GC 行为、线程池等运行指标

这样每个阶段都有独立的回滚点，出问题能快速定位是代码变更还是运行时升级引入的。

## 参考

- [OpenJDK JDK 17](https://openjdk.org/projects/jdk/17/)
- [JDK 12](https://openjdk.org/projects/jdk/12/)～[JDK 16](https://openjdk.org/projects/jdk/16/) 项目页
- [JDK 17 Release Notes](https://www.oracle.com/java/technologies/javase/17-relnote-issues.html)
- [JDK 17 to JDK 21 Migration Guide](https://docs.oracle.com/en/java/javase/21/migrate/)
- [Java 版本历史](./java-version-history.md)

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-06-20 | title 改为「JDK 17 特性」 | 全系列统一命名，去掉「新特性」 |
| 2026-06-20 | 重命名为 `jdk-17.md`；title 改为「JDK 17」；url 改为 `jdk-17`；移至 `language/java/` | 全系列统一简洁命名 |
| 2026-06-20 | 补充 JDK 12～17 全部 JEP；明确上一 LTS 为 JDK 11；增加语言特性演进表 | 文档应覆盖 11→17 升级路径上的累积变化 |
