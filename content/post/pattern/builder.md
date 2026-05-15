---
title: 创建者模式, 建造者模式, Builder
author: "-"
date: 2026-04-16T15:01:10+08:00
lastmod: 2026-05-15T20:06:12+08:00
url: builder-pattern
categories:
  - Pattern
tags:
  - Pattern
  - remix
  - AI-assisted

---
## 创建者模式, 建造者模式, Builder pattern

定义: 将一个复杂对象的构建与它的表示分离，使得同样的构建过程可以创建不同的表示  

### 使用场景

1. 多个部件或零件，都可以装配到一个对象中，但产生的结果又不相同时。
2. 当初始化一个对象特别复杂的时候，比如参数多，而且很多参数都有默认值。

GoF Builder 模式包含四个角色：

- **抽象建造者 (Builder)**：给出一个抽象接口，以规范产品对象各个组成成分的建造。
- **具体建造者 (ConcreteBuilder)**：实现抽象建造者声明的接口，一步一步完成创建产品实例的操作；建造完成后提供产品实例。
- **指挥者 (Director)**：调用具体建造者以创建产品对象。
- **产品 (Product)**：建造中的复杂对象。

### GoF Builder 示例：RTF 文档转换器

**RTF 背景**

RTF（Rich Text Format，富文本格式）是微软 1987 年推出的一种文档格式，用纯文本加控制命令描述带格式的文档。一段 RTF 内容长这样：

```
{\rtf1 Hello {\b World}\par}
```

- `{\b ... }` 表示加粗
- `\par` 表示段落结束

RTFReader（Director）的工作是逐个扫描这些 token：遇到 `\b` 就调 `convertFontBold(true)`，遇到普通字符就调 `convertCharacter(c)`，遇到 `\par` 就调 `convertParagraph()`。它自己不生产任何输出，只负责解析结构、驱动 Builder。虽然 RTF 现在已经很少用了，但"解析器解析 → 转换器输出不同格式"这个模型在现代依然普遍（如 Markdown 解析器输出 HTML / PDF / DOCX）。

这是 GoF 原书使用的经典案例。同一份 RTF 文档，Director（RTFReader）负责解析 token 流，每遇到字符、加粗标记、段落标记就调用 Builder 对应的方法。**Director 只管读懂结构，Builder 只管决定输出，两者通过接口解耦**：`parse()` 接收的是 `TextConverter` 接口，不需要知道背后的具体类型，也不需要知道最终输出格式——它只是把 RTF 语义事件翻译成接口调用，由各 ConcreteBuilder 自己决定如何响应：ASCIIConverter 忽略格式标记只保留字符，HTMLConverter 将加粗转为 `<b>` 标签，TeXConverter 转为 `\textbf{}` 命令。

```java
// Product - 转换结果
class Document {
    private final StringBuilder content = new StringBuilder();

    public void append(String text) { content.append(text); }

    @Override
    public String toString() { return content.toString(); }
}

// Builder 接口
interface TextConverter {
    void convertCharacter(char c);
    void convertFontBold(boolean on);
    void convertParagraph();
    Document getResult();
}

// ConcreteBuilder - 纯文本（忽略所有格式标记）
class ASCIIConverter implements TextConverter {
    private Document doc = new Document();

    public void convertCharacter(char c)    { doc.append(String.valueOf(c)); }
    public void convertFontBold(boolean on) { /* 纯文本忽略粗体 */ }
    public void convertParagraph()          { doc.append("\n"); }
    public Document getResult()             { return doc; }
}

// ConcreteBuilder - HTML（格式标记 → HTML 标签）
class HTMLConverter implements TextConverter {
    private Document doc = new Document();

    public void convertCharacter(char c)    { doc.append(String.valueOf(c)); }
    public void convertFontBold(boolean on) { doc.append(on ? "<b>" : "</b>"); }
    public void convertParagraph()          { doc.append("</p>\n<p>"); }
    public Document getResult()             { return doc; }
}

// ConcreteBuilder - TeX（格式标记 → TeX 命令）
class TeXConverter implements TextConverter {
    private Document doc = new Document();

    public void convertCharacter(char c)    { doc.append(String.valueOf(c)); }
    public void convertFontBold(boolean on) { doc.append(on ? "\\textbf{" : "}"); }
    public void convertParagraph()          { doc.append("\n\n"); }
    public Document getResult()             { return doc; }
}

// Director - RTF 解析器，逐字符扫描 token 流，驱动 converter
// 它只负责识别控制字和普通字符，不决定最终输出格式
class RTFReader {
    private final String rtf;

    public RTFReader(String rtf) { this.rtf = rtf; }

    public void parse(TextConverter converter) {
        boolean inBold = false;
        int i = 0;
        while (i < rtf.length()) {
            char c = rtf.charAt(i);
            if (c == '{') {
                i++;
            } else if (c == '}') {
                if (inBold) { converter.convertFontBold(false); inBold = false; }
                i++;
            } else if (c == '\\') {
                // 解析控制字：\word[digit][ ]
                i++;
                StringBuilder word = new StringBuilder();
                while (i < rtf.length() && Character.isLetter(rtf.charAt(i)))
                    word.append(rtf.charAt(i++));
                while (i < rtf.length() && Character.isDigit(rtf.charAt(i)))
                    i++; // 跳过数字参数（如 \rtf1 中的 1）
                if (i < rtf.length() && rtf.charAt(i) == ' ')
                    i++; // 控制字后的空格是 RTF 分隔符，消耗掉
                switch (word.toString()) {
                    case "b":   converter.convertFontBold(true); inBold = true; break;
                    case "par": converter.convertParagraph(); break;
                    // 其他控制字（如 rtf1 文件头）忽略
                }
            } else {
                converter.convertCharacter(c); // 普通字符（含内容里的空格）
                i++;
            }
        }
    }
}

// Client
public class Client {
    public static void main(String[] args) {
        // 真实 RTF 文档片段："Hello " 普通文本，"World" 加粗，段落结束
        RTFReader reader = new RTFReader("{\\rtf1 Hello {\\b World}\\par}");

        TextConverter ascii = new ASCIIConverter();
        reader.parse(ascii);
        System.out.println(ascii.getResult());
        // → Hello World

        TextConverter html = new HTMLConverter();
        reader.parse(html);
        System.out.println(html.getResult());
        // → Hello <b>World</b></p>

        TextConverter tex = new TeXConverter();
        reader.parse(tex);
        System.out.println(tex.getResult());
        // → Hello \textbf{World}
    }
}
```

GoF Builder 和 AbstractFactory 都用于创建复杂对象：Builder 强调**一步步构建**，相同过程可得到不同结果，对象不直接返回；AbstractFactory 强调**直接返回**一组相互依赖的对象。

### Builder vs 工厂方法

工厂方法注重整体对象的创建，Builder 注重部件构建的过程。如要制造一个超人：

- **工厂方法**：直接产生出一个力大无穷、能够飞翔、内裤外穿的超人
- **Builder**：先组装手、头、脚、躯干，再把内裤外穿，一步一步构建

工厂方法创建的产品粒度较粗，Builder 的产品粒度较细、可控制每个构建步骤。

两者的关键区别不是"能创建几种产品"，而是**能否控制构建过程的细节**。工厂方法的可变点是"类型"（创建哪种产品），Builder 的可变点是"过程"（按什么步骤、用什么方式组装）。

---

## Java Builder 模式：可选参数与链式调用

Joshua Bloch 在《Effective Java》中以 Pizza 为例，推荐用 Builder 解决可选参数过多的问题。Pizza 有必选的尺寸，以及若干可选配料——用构造方法重载会导致组合爆炸，用 set 方法又无法保证对象不可变。Builder 通过链式调用优雅地解决了这个问题：

```java
public class Pizza {
    private final int size;           // 必选：尺寸（英寸）
    private final boolean cheese;     // 可选：加芝士
    private final boolean pepperoni;  // 可选：加培根
    private final boolean mushrooms;  // 可选：加蘑菇

    private Pizza(Builder builder) {
        this.size      = builder.size;
        this.cheese    = builder.cheese;
        this.pepperoni = builder.pepperoni;
        this.mushrooms = builder.mushrooms;
    }

    public static class Builder {
        private final int size;
        private boolean cheese    = false;
        private boolean pepperoni = false;
        private boolean mushrooms = false;

        public Builder(int size) {
            this.size = size;
        }

        public Builder cheese(boolean val)    { cheese    = val; return this; }
        public Builder pepperoni(boolean val) { pepperoni = val; return this; }
        public Builder mushrooms(boolean val) { mushrooms = val; return this; }

        public Pizza build() { return new Pizza(this); }
    }
}
```

使用时：

```java
Pizza pizza = new Pizza.Builder(12)
        .cheese(true)
        .pepperoni(true)
        .build();
```

### Builder 继承与协变返回类型

子类继承父类 Builder 时，父类中返回 `Person.Builder` 的方法在子类中仍返回父类类型，链式调用会中断：

```java
Customer customer = new Customer.Builder("Tom", 13999999999L, "北京市")
        .age(20)        // 此处返回 Person.Builder
        .alias("昵称")  // 错误：Person.Builder 上没有 alias 方法
        .build();
```

协变返回类型（Covariant Return Type）指子类覆写方法时，可以将返回类型改为父类返回类型的子类型。解决此问题有两种方案：

**方案一：Override + 强制类型转换**

在子类 Builder 中覆写父类每个设置方法，将返回值强转为子类类型：

```java
public static class Builder extends Person.Builder {
    @Override
    public Builder age(int age) {
        return (Builder) super.age(age);
    }

    @Override
    public Builder sex(String sex) {
        return (Builder) super.sex(sex);
    }
}
```

缺点：需要覆写父类所有设置方法，代码冗长。

**方案二：泛型递归类型参数（模拟 self-type）**

将父类 Builder 声明为泛型类，用 `T extends Builder<T>` 表示"子类自身类型"：

```java
public class Person {
    public static class Builder<T extends Builder<T>> {
        public T age(int age) {
            this.age = age;
            return (T) this;
        }

        public T sex(String sex) {
            this.sex = sex;
            return (T) this;
        }
    }
}
```

子类将自身类型传入泛型参数，无需覆写各设置方法：

```java
public class Customer {
    public static class Builder extends Person.Builder<Builder> {
        @Override
        public Customer build() {
            return new Customer(this);
        }
    }
}
```

如果父类是抽象类，可将 `self()` 声明为抽象方法，由子类负责返回正确的 `this`：

```java
public abstract class Person {
    public abstract static class Builder<T extends Builder<T>> {
        public T age(int age) {
            this.age = age;
            return self();
        }

        public T sex(String sex) {
            this.sex = sex;
            return self();
        }

        abstract protected T self();
    }
}
