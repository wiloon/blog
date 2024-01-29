---
title: "jdk14"
author: "-"
date: ""
url: ""
categories:
  - inbox
tags:
  - inbox
---
## "jdk14"

### instanceof 模式匹配

JDK 14的新特性:instanceof模式匹配

JDK14在2020年的3月正式发布了。可惜的是正式特性只包含了最新的Switch表达式，而Records,patterns,text blocks仍然是预览特性。

本文要讲的就是JDK14的一个预览特性instanceof的pattern matching。 也就是说在instanceof中可以使用模式匹配了。

怎么理解呢？

我们先举个历史版本中使用instanceof的例子。

假如我们是动物园的管理员，动物园里面有Girraffe和Hippo两种动物。

@Data
public class Girraffe {
    private String name;
}
@Data
public class Hippo {
    private String name;
}

public class TestZoo {
    private final static Logger logger = LoggerFactory.getLogger(TestZoo.class);

    public static void main(String[] args) {
        Girraffe g = new Girraffe();
        g.setName("gg");
        testZooOld(g);
        testZooNew(g);

        Cat c = new Cat();
        c.setName("pipi");
        testZooOld(c);
        testZooNew(c);
    }

    public static void testZooOld(Object animal) {
        if (animal instanceof Girraffe) {
            Girraffe girraffe = (Girraffe) animal;
            logger.info("girraffe name is {}", girraffe.getName());
        } else if (animal instanceof Hippo) {
            Hippo hippo = (Hippo) animal;
            logger.info("hippo name is {}", hippo.getName());
        }else{
            logger.info("test zoo old, 对不起，该动物不是地球上的生物！");
        }

    }

    public static void testZooNew(Object animal){
        if(animal instanceof Girraffe girraffe){
            logger.info("name is {}",girraffe.getName());
        }else if(animal instanceof Hippo hippo){
            logger.info("name is {}",hippo.getName());
        }else{
            logger.info("test zoo new, 对不起，该动物不是地球上的生物！");
        }
    }
}

注意instanceof的用法，通过instanceof的模式匹配，就不需要二次转换了。直接使用就可以了。并且模式匹配的对象还被限定了作用域范围，会更加安全。

注意，如果你使用的最新版的IntelliJ IDEA 2020.1版本的话，语言编译版本一定要选择14(Preview),因为这个功能是preview的。

---

https://www.cnblogs.com/flydean/p/jdk14-instanceof-pattern-matching.html

