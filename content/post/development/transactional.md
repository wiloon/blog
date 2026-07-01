---
title: Spring 事务 @Transactional
author: "-"
date: 2012-02-02T05:10:12+00:00
lastmod: 2026-07-01T04:31:12+08:00
url: spring-transaction
categories:
  - language
tags:
  - java
  - spring
  - remix
  - AI-assisted
---
## spring 事务

## @Transactional

使用 @Transactional 的要点有:

1. 在DAO 层使用 JdbcTemplate 实现DB操作, 在 Service 的实现类上加上 @Transactional 注解, 不推荐在 Service 接口上加 @Transactional 注解.
2. 需要进行事务控制的方法, 必须是 public 方法, 同时要打上 @Transactional 注解.
3. 也可以在Class上加上 @Transactional 注解, 这样相当于给每个 public 函数加上了 @Transactional 注解, 当然我们还可以在其中的函数上加该注解, 这时候将以函数上的设置为准.

## @Transactional 失效场景

1. **只有 public 方法生效**：`private`/`protected`/包级方法上加 `@Transactional` 不生效，因为 Spring 默认约定只处理 public 方法（CGLIB 虽然能代理 protected 方法，但 Spring 事务模块不支持）。
2. **同类自调用（self-invocation）**：`@Transactional` 依赖 Spring AOP 生成的代理对象，只有通过代理调用方法才会走事务逻辑。同一个类内部用 `this.xxx()` 直接调用会绕过代理，导致事务失效。

   ```java
   @Service
   public class OrderService {
       public void placeOrder() {
           this.updateStock(); // this 调用不经过代理，事务失效
       }

       @Transactional
       public void updateStock() { ... }
   }
   ```

   解决办法：把需要事务的方法拆到另一个 Bean 里，或注入自身代理（`AopContext.currentProxy()`，需要 `exposeProxy=true`）。

   **原理：注解是方法级的标记，代理是类级的壳**

   `@Transactional` 虽然声明在方法上，但代理对象的生成粒度是**整个类/实例**，不是单个方法：

   - Spring 只要发现 Bean 里**任意一个方法**带 `@Transactional`（或类上带），就为**整个 Bean** 生成一个代理对象（有接口用 JDK 动态代理，没接口用 CGLIB 生成子类）
   - 这一个代理对象包含目标类的所有方法；调用方法时，代理内部逐次判断"这个方法要不要被事务拦截"（通过 `TransactionAttributeSource` 匹配注解），匹配上才插入事务逻辑，没匹配上直接透传
   - 目标类内部的 `this` 永远指向**原始目标对象**（被代理包裹的真实实例），这是 Java 语言规则，与 Spring 怎么包装它无关

   所以调用链是：

   - 外部调用：`caller → proxy.updateStock() → [事务拦截器：开启/提交/回滚] → target.updateStock()` ✅ 走事务
   - 内部自调用：`target.placeOrder() → this.updateStock()` 直接就是 `target.updateStock()`，没有经过代理对象这一层，事务拦截器（挂在代理上）自然用不上 ❌ 不走事务

   一句话：**注解是方法级的"标记"，代理是类级的"壳"，`this` 调用永远在壳里面、摸不到壳外面那层，事务逻辑（附着在壳上）就用不上了。**

3. **异常类型不匹配**：默认只有抛出 `RuntimeException` 或 `Error` 才会触发回滚；受检异常（如 `IOException`）默认不回滚，必须显式指定 `rollbackFor`。

   ```java
   @Transactional(propagation = Propagation.REQUIRED, rollbackFor = MyException.class)
   ```

   **设计原则：受检异常被建模为业务分支，非受检异常被建模为意外错误**

   这条默认规则源自 Spring 对异常语义的假设（沿袭自 EJB 传统），不是技术限制——不管回滚与否，异常都会正常继续往外抛，两者互不冲突。

   | 异常类型                                        | Spring 的语义假设                                  | 默认行为         |
   | ----------------------------------------------- | -------------------------------------------------- | ---------------- |
   | 受检异常（`Exception` 但非 `RuntimeException`） | 业务上可预期的正常分支（如"库存不足""文件未找到"） | **提交**，不回滚 |
   | 非受检异常（`RuntimeException`/`Error`）        | 意外的、非预期的系统性错误                         | **回滚**         |

   需要哪一类回滚都可以通过 `rollbackFor` / `noRollbackFor` 显式覆盖，这只是一个可配置的默认值选择。

4. **方法内部 try-catch 吞掉异常**：异常被自己捕获且没有再抛出，Spring 感知不到异常，事务不会回滚。
5. **类没有交给 Spring 管理**：没加 `@Service`/`@Component` 等注解，或是手动 `new` 出来的对象，压根不存在事务代理。
6. **多线程场景**：事务通过 `ThreadLocal` 绑定当前线程的数据库连接；方法内部另起线程执行数据库操作时，新线程拿到的不是同一个事务连接，不受原事务控制。
7. **数据库存储引擎不支持事务**：例如 MySQL 表用了 MyISAM 而不是 InnoDB，本身不支持事务，加注解也无效。
8. **主调函数与多个被调函数分属不同 Service**：如果一个非事务方法顺序调用了两个不同 Service Bean 的事务方法, 它们并不在同一个事务上下文中, 而是分属于不同的事务上下文（除非用了 `Propagation.REQUIRED` 且处于同一调用链上被一个外层事务方法统一包裹）。

>[https://www.cnblogs.com/harrychinese/p/SpringBoot_jdbc_transaction.html](https://www.cnblogs.com/harrychinese/p/SpringBoot_jdbc_transaction.html)

## 维护记录

| 时间       | 修改内容                                                                                                                                                                                      | 原因                                           |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| 2026-07-01 | 修正 URL 拼写（`sprint` → `spring-transaction`）；categories 从 `Inbox` 改为 `language`；补充 `@Transactional` 失效场景（自调用代码示例、异常吞掉、事务传播、存储引擎不支持事务、多线程场景） | 原文分类不准确，且失效场景覆盖不全             |
| 2026-07-01 | 在同类自调用小节补充代理机制原理说明（注解是方法级标记、代理是类级壳、`this` 指向原始对象）                                                                                                   | 解释自调用失效的底层原因，便于理解而非死记结论 |
| 2026-07-01 | 在异常类型不匹配小节补充设计原则说明（受检异常=业务分支、非受检异常=意外错误的语义假设表格）                                                                                                  | 解释默认回滚规则的设计意图，而非单纯罗列规则   |
