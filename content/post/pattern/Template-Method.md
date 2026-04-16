---
title: 设计模式 – 模板方法, Template Method
author: "-"
date: 2026-04-16T17:39:47+08:00
url: design-pattern/template-method
categories:
  - Pattern
tags:
  - Pattern
  - remix
  - AI-assisted
---

模板方法模式是类的行为模式。准备一个抽象类，将部分逻辑以具体方法以及具体构造函数的形式实现，然后声明一些抽象方法来迫使子类实现剩余的逻辑。不同的子类可以以不同的方式实现这些抽象方法，从而对剩余的逻辑有不同的实现。这就是模板方法模式的用意。

## 模式结构

模板方法模式是所有模式中最为常见的几个模式之一，是基于继承的代码复用的基本技术。

模板方法模式需要开发抽象类和具体子类的设计师之间的协作。一个设计师负责给出一个算法的轮廓和骨架，另一些设计师则负责给出这个算法的各个逻辑步骤。代表这些具体逻辑步骤的方法称做基本方法（primitive method）；而将这些基本方法汇总起来的方法叫做模板方法（template method），这个设计模式的名字就是从此而来。

模板方法所代表的行为称为顶级行为，其逻辑称为顶级逻辑。

这里涉及到两个角色：

**抽象模板（Abstract Template）** 角色的责任：

- 定义了一个或多个抽象操作，以便让子类实现。这些抽象操作叫做基本操作，它们是一个顶级逻辑的组成步骤。
- 定义并实现了一个模板方法。这个模板方法一般是一个具体方法，它给出了一个顶级逻辑的骨架，而逻辑的组成步骤在相应的抽象操作中，推迟到子类实现。顶级逻辑也有可能调用一些具体方法。

**具体模板（Concrete Template）** 角色的责任：

- 实现父类所定义的一个或多个抽象方法，它们是一个顶级逻辑的组成步骤。
- 每一个抽象模板角色都可以有任意多个具体模板角色与之对应，而每一个具体模板角色都可以给出这些抽象方法（也就是顶级逻辑的组成步骤）的不同实现，从而使得顶级逻辑的实现各不相同。

## 基础示例

抽象模板角色类，`abstractMethod()`、`hookMethod()` 等基本方法是顶级逻辑的组成步骤，这个顶级逻辑由 `templateMethod()` 方法代表。

```java
public abstract class AbstractTemplate {

    /**
     * 模板方法
     */
    public void templateMethod() {
        // 调用基本方法
        abstractMethod();
        hookMethod();
        concreteMethod();
    }

    /**
     * 基本方法的声明（由子类实现）
     */
    protected abstract void abstractMethod();

    /**
     * 基本方法（空方法）
     */
    protected void hookMethod() {}

    /**
     * 基本方法（已经实现）
     */
    private final void concreteMethod() {
        // 业务相关的代码
    }
}
```

具体模板角色类实现了父类所声明的基本方法，`abstractMethod()` 方法所代表的就是强制子类实现的剩余逻辑，而 `hookMethod()` 方法是可选择实现的逻辑。

```java
public class ConcreteTemplate extends AbstractTemplate {

    @Override
    public void abstractMethod() {
        // 业务相关的代码
    }

    @Override
    public void hookMethod() {
        // 业务相关的代码
    }
}
```

模板模式的关键是：子类可以置换掉父类的可变部分，但是子类却不可以改变模板方法所代表的顶级逻辑。

每当定义一个新的子类时，不要按照控制流程的思路去想，而应当按照"责任"的思路去想。换言之，应当考虑哪些操作是必须置换掉的，哪些操作是可以置换掉的，以及哪些操作是不可以置换掉的。使用模板模式可以使这些责任变得清晰。

## 模板方法中的方法分类

模板方法中的方法可以分为两大类：**模板方法**和**基本方法**。

**模板方法**

一个模板方法是定义在抽象类中的，把基本操作方法组合在一起形成一个总算法或一个总行为的方法。一个抽象类可以有任意多个模板方法，而不限于一个。每一个模板方法都可以调用任意多个具体方法。

**基本方法**

基本方法又可以分为三种：抽象方法（Abstract Method）、具体方法（Concrete Method）和钩子方法（Hook Method）。

- **抽象方法**：一个抽象方法由抽象类声明，由具体子类实现。在 Java 语言里抽象方法以 `abstract` 关键字标示。
- **具体方法**：一个具体方法由抽象类声明并实现，而子类并不实现或置换。
- **钩子方法**：一个钩子方法由抽象类声明并实现，而子类会加以扩展。通常抽象类给出的实现是一个空实现，作为方法的默认实现。

**命名规则**

钩子方法的名字应当以 `do` 开始，这是熟悉设计模式的 Java 开发人员的标准做法。在 `HttpServlet` 类中，也遵从这一命名规则，如 `doGet()`、`doPost()` 等方法。

## 存款利息示例

考虑一个计算存款利息的例子。假设系统需要支持两种存款账号：货币市场（Money Market）账号和定期存款（Certificate of Deposit）账号。这两种账号的存款利息是不同的，因此，在计算一个存户的存款利息额时，必须区分两种不同的账号类型。

这个系统的总行为应当是计算出利息，这也就决定了作为一个模板方法模式的顶级逻辑应当是利息计算。由于利息计算涉及到两个步骤：一个基本方法给出账号种类，另一个基本方法给出利息百分比。这两个基本方法构成具体逻辑，因为账号的类型不同，所以具体逻辑会有所不同。

抽象模板角色类：

```java
public abstract class Account {

    /**
     * 模板方法，计算利息数额
     * @return 返回利息数额
     */
    public final double calculateInterest() {
        double interestRate = doCalculateInterestRate();
        String accountType = doCalculateAccountType();
        double amount = calculateAmount(accountType);
        return amount * interestRate;
    }

    /**
     * 基本方法留给子类实现
     */
    protected abstract String doCalculateAccountType();

    /**
     * 基本方法留给子类实现
     */
    protected abstract double doCalculateInterestRate();

    /**
     * 基本方法，已经实现
     */
    private double calculateAmount(String accountType) {
        // 省略相关的业务逻辑
        return 7243.00;
    }
}
```

具体模板角色类：

```java
public class MoneyMarketAccount extends Account {

    @Override
    protected String doCalculateAccountType() {
        return "Money Market";
    }

    @Override
    protected double doCalculateInterestRate() {
        return 0.045;
    }
}
```

```java
public class CDAccount extends Account {

    @Override
    protected String doCalculateAccountType() {
        return "Certificate of Deposit";
    }

    @Override
    protected double doCalculateInterestRate() {
        return 0.06;
    }
}
```

客户端类：

```java
public class Client {

    public static void main(String[] args) {
        Account account = new MoneyMarketAccount();
        System.out.println("货币市场账号的利息数额为: " + account.calculateInterest());
        account = new CDAccount();
        System.out.println("定期账号的利息数额为: " + account.calculateInterest());
    }
}
```

## 模板方法模式在 Servlet 中的应用

使用过 Servlet 的人都清楚，除了要在 web.xml 做相应的配置外，还需继承一个叫 `HttpServlet` 的抽象类。`HttpServlet` 类提供了一个 `service()` 方法，这个方法调用七个 do 方法中的一个或几个，完成对客户端调用的响应。这些 do 方法需要由 `HttpServlet` 的具体子类提供，因此这是典型的模板方法模式。下面是 `service()` 方法的源代码：

```java
protected void service(HttpServletRequest req, HttpServletResponse resp)
        throws ServletException, IOException {

    String method = req.getMethod();

    if (method.equals(METHOD_GET)) {
        long lastModified = getLastModified(req);
        if (lastModified == -1) {
            doGet(req, resp);
        } else {
            long ifModifiedSince = req.getDateHeader(HEADER_IFMODSINCE);
            if (ifModifiedSince < (lastModified / 1000 * 1000)) {
                maybeSetLastModified(resp, lastModified);
                doGet(req, resp);
            } else {
                resp.setStatus(HttpServletResponse.SC_NOT_MODIFIED);
            }
        }
    } else if (method.equals(METHOD_HEAD)) {
        long lastModified = getLastModified(req);
        maybeSetLastModified(resp, lastModified);
        doHead(req, resp);
    } else if (method.equals(METHOD_POST)) {
        doPost(req, resp);
    } else if (method.equals(METHOD_PUT)) {
        doPut(req, resp);
    } else if (method.equals(METHOD_DELETE)) {
        doDelete(req, resp);
    } else if (method.equals(METHOD_OPTIONS)) {
        doOptions(req, resp);
    } else if (method.equals(METHOD_TRACE)) {
        doTrace(req, resp);
    } else {
        String errMsg = lStrings.getString("http.method_not_implemented");
        Object[] errArgs = new Object[1];
        errArgs[0] = method;
        errMsg = MessageFormat.format(errMsg, errArgs);
        resp.sendError(HttpServletResponse.SC_NOT_IMPLEMENTED, errMsg);
    }
}
```

当然，这个 `service()` 方法也可以被子类置换掉。下面给出一个简单的 Servlet 例子：

```java
public class TestServlet extends HttpServlet {

    public void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        System.out.println("using the GET method");
    }

    public void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        System.out.println("using the POST method");
    }
}
```

从上面的例子可以看出这是一个典型的模板方法模式：

- `HttpServlet` 担任**抽象模板**角色：模板方法由 `service()` 方法担任，基本方法由 `doPost()`、`doGet()` 等方法担任。
- `TestServlet` 担任**具体模板**角色：置换掉了父类 `HttpServlet` 中七个基本方法中的其中两个，分别是 `doGet()` 和 `doPost()`。

---

> 参考：[http://www.cnblogs.com/java-my-life/archive/2012/05/14/2495235.html](http://www.cnblogs.com/java-my-life/archive/2012/05/14/2495235.html)
