---
title: 创建者模式, 建造者模式, Builder
author: "-"
date: 2026-04-16T15:01:10+08:00
url: builder-pattern
categories:
  - Pattern
tags:
  - Pattern
  - remix
  - AI-assisted

---
## 创建者模式, 建造者模式, Builder

定义: 将一个复杂对象的构建与它的表示分离，使得同样的构建过程可以创建不同的表示  

### 使用场景

1. 多个部件或零件，都可以装配到一个对象中，但产生的结果又不相同时。
2. 当初始化一个对象特别复杂的时候，比如参数多，而且很多参数都有默认值。

它分为抽象建造者 (Builder) 角色、具体建造者 (ConcreteBuilder) 角色、导演者 (Director) 角色、产品 (Product) 角色四个角色。

抽象建造者 (Builder) 角色: 给 出一个抽象接口，以规范产品对象的各个组成成分的建造。

具体建造者 (ConcreteBuilder) 角色: 要完成的任务包括: 1.实现抽象建造者Builder所声明的接口，给出一步一步地完成创建产品实例的操作。2.在建造过程完成后，提供产品的实例。

导演者 (Director) 角色: 担任这个角色的类调用具体建造者角色以创建产品对象。

产品 (Product) 角色: 产品便是建造中的复杂对象。

对于Builder模式很简单，但是一直想不明白为什么要这么设计，为什么要向builder要Product而不是向知道建造过程的Director要。刚才google到一篇文章，总算清楚了。在这里转贴一下这位richardluo的比喻。

简单地说，就好象我要装修一套房子，可是我不懂施工——水电怎么走、木作怎么做，每个工种都有自己专注的领域；也不懂整体设计——用什么风格、先做哪道工序、各部分如何协调，这是设计师的职责。于是我需要找一支装修队，各工种各司其职；还得找个设计师，他来规划整体方案、协调各工种按图施工，而设计师本身不动手，只负责下命令。最后，我可以向工人要装修好的房间了。在这个过程中，设计师手里什么都没有，只有图纸和指令，所以要房间也是跟工人要，记住了！

以下是richardluo的代码，我根据他的思路加上了相应的注释。

1. 定义工人接口，即一支装修队所需具备的通用技能。

```java
// 工人接口。水电工负责布线，木工负责木作，油漆工负责涂装。
// 装修完成后，由装修队把房间交还给房主。
public interface Builder {
    void doElectrical();  // 水电工
    void doCarpentry();   // 木工
    void doPainting();    // 油漆工
    Room getRoom();
}
```

2. 定义设计师（Director），他持有图纸，协调装修队按方案施工。

```java
// 设计师（Director）。持有图纸，规定施工顺序，但不亲自动手。
public class Designer {
    public void coordinate(Builder builder) {
        builder.doElectrical();
        builder.doCarpentry();
        builder.doPainting();
    }
}
```

3. 装修队（ConcreteBuilder），负责具体的施工实施。

```java
// 各专职工人
class ElectricalWorker {
    public String work() { return "electrical done"; }
}
class Carpenter {
    public String work() { return "carpentry done"; }
}
class Painter {
    public String work() { return "painting done"; }
}

// 装修队（ConcreteBuilder）。由水电工、木工、油漆工组成，各司其职。
// 装修完成后，由装修队把房间交还给房主。
public class WorkerTeam implements Builder {
    private ElectricalWorker electrician = new ElectricalWorker();
    private Carpenter        carpenter   = new Carpenter();
    private Painter          painter     = new Painter();

    private String electrical = "";
    private String carpentry  = "";
    private String painting   = "";

    public void doElectrical() { electrical = electrician.work(); }
    public void doCarpentry()  { carpentry  = carpenter.work(); }
    public void doPainting()   { painting   = painter.work(); }

    // 把装修好的房间交还给房主
    public Room getRoom() {
        if (!electrical.equals("") && !carpentry.equals("") && !painting.equals("")) {
            System.out.println("room ready!");
            return new Room();
        } else {
            return null;
        }
    }
}
```

4. 房主（Client），雇人、收房。

```java
// 房主。聘请一支装修队和一位设计师，让设计师协调装修队按图施工，最后从装修队手上收房。
public class Client {
    public static void main(String[] args) {
        Builder team = new WorkerTeam();
        Designer designer = new Designer();
        designer.coordinate(team);
        team.getRoom();
    }
}
```

好了，我觉得这样大概能说明白了。不知各位觉得如何呢？或者有更好的应用场景解释，敬请赐教。

[GOF95]中，Builder模式将一个复杂对象的构建与它的表示分离，使得同样的构建过程可以创建不同的表示。

Builder模式和AbstractFactory模式在功能上很相似，因为都是用来创建大的复杂的对象，它们的区别是: Builder模式强调的是一步步创建对象，并通过相同的创建过程可以获得不同的结果对象，一般来说Builder模式中对象不是直接返回的。而在AbstractFactory模式中对象是直接返回的，AbstractFactory模式强调的是为创建多个相互依赖的对象提供一个同一的接口。

```java
class Room {}

// 工人接口：每个工种都实现它
interface Worker {
    String work();
}

// 普通工种
class StandardElectrician implements Worker { public String work() { return "standard electrical"; } }
class StandardCarpenter    implements Worker { public String work() { return "standard carpentry"; } }
class StandardTiler        implements Worker { public String work() { return "standard tiling"; } }
class StandardPainter      implements Worker { public String work() { return "standard painting"; } }

// 高端工种
class PremiumElectrician implements Worker { public String work() { return "premium electrical"; } }
class PremiumCarpenter    implements Worker { public String work() { return "premium carpentry"; } }
class PremiumTiler        implements Worker { public String work() { return "premium marble tiling"; } }
class PremiumPainter      implements Worker { public String work() { return "premium painting"; } }

// Builder 抽象类 - 定义装修工种的通用接口
abstract class Builder {
    protected String electrical = "";
    protected String carpentry  = "";
    protected String tiling     = "";
    protected String painting   = "";

    public void doElectrical() {}
    public void doCarpentry()  {}
    public void doTiling()     {}
    public void doPainting()   {}

    public abstract Room getRoom();
}

// Director - 设计师，持有图纸，协调装修队按图施工
abstract class Designer {
    Builder builder;

    public Designer(Builder builder) {
        this.builder = builder;
    }

    public abstract void construct();
}

// 现代简约风格：白墙 + 木作，不贴瓷砖
class ModernDesigner extends Designer {
    public ModernDesigner(Builder builder) {
        super(builder);
    }

    public void construct() {
        builder.doElectrical();
        builder.doCarpentry();
        builder.doPainting();
    }
}

// 中式古典风格：地砖 + 木作 + 涂装
class ChineseDesigner extends Designer {
    public ChineseDesigner(Builder builder) {
        super(builder);
    }

    public void construct() {
        builder.doElectrical();
        builder.doTiling();
        builder.doCarpentry();
        builder.doPainting();
    }
}

// 普通装修队：由各普通工种组成
class GeneralTeam extends Builder {
    private Worker electrician = new StandardElectrician();
    private Worker carpenter   = new StandardCarpenter();
    private Worker tiler       = new StandardTiler();
    private Worker painter     = new StandardPainter();

    public void doElectrical() { electrical = electrician.work(); }
    public void doCarpentry()  { carpentry  = carpenter.work(); }
    public void doTiling()     { tiling     = tiler.work(); }
    public void doPainting()   { painting   = painter.work(); }

    public Room getRoom() {
        System.out.println("room ready!");
        return new Room();
    }
}

// 高端装修队：由各高端工种组成，用料和工艺更高端
class PremiumTeam extends Builder {
    private Worker electrician = new PremiumElectrician();
    private Worker carpenter   = new PremiumCarpenter();
    private Worker tiler       = new PremiumTiler();
    private Worker painter     = new PremiumPainter();

    public void doElectrical() { electrical = electrician.work(); }
    public void doCarpentry()  { carpentry  = carpenter.work(); }
    public void doTiling()     { tiling     = tiler.work(); }
    public void doPainting()   { painting   = painter.work(); }

    public Room getRoom() {
        System.out.println("premium room ready!");
        return new Room();
    }
}

// 核心优势体现：同一支装修队，配合不同的设计师图纸，装出不同风格的房间。
public class HomeOwner {
    public static void main(String[] args) {
        // 普通装修队 + 现代简约图纸
        Builder team = new GeneralTeam();
        new ModernDesigner(team).construct();
        team.getRoom(); // → 现代简约风格

        // 同一支普通装修队，换中式古典图纸
        team = new GeneralTeam();
        new ChineseDesigner(team).construct();
        team.getRoom(); // → 中式古典风格

        // 高端装修队 + 现代简约图纸，同样的施工顺序，用料更高端
        Builder premiumTeam = new PremiumTeam();
        new ModernDesigner(premiumTeam).construct();
        premiumTeam.getRoom(); // → 高端现代简约风格
    }
}
```

工厂方法模式VS建造者模式
工厂方法模式注重的是整体对象的创建方法，而建造者模式注重的是部件构建的过程，旨在通过一步一步地精确构造创建出一个复杂的对象。
我们举个简单例子来说明两者的差异，如要制造一个超人，如果使用工厂方法模式，直接产生出来的就是一个力大无穷、能够飞翔、内裤外穿的超人；
而如果使用建造者模式，则需要组装手、头、脚、躯干等部分，然后再把内裤外穿，于是一个超人就诞生了。

工厂方法模式创建的产品一般都是单一性质产品，如成年超人，都是一个模样，而建造者模式创建的则是一个复合产品，它由各个部件复合而成，部件不同产品对象当然不同。
这不是说工厂方法模式创建的对象简单，而是指它们的粒度大小不同。一般来说，工厂方法模式的对象粒度比较粗，建造者模式的产品对象粒度比较细。

两者的区别有了，那在具体的应用中，我们该如何选择呢？
是用工厂方法模式来创建对象，还是用建造者模式来创建对象，这完全取决于我们在做系统设计时的意图，如果需要详细关注一个产品部件的生产、安装步骤，则选择建造者，否则选择工厂方法模式。

用装修领域来类比这两种模式的差异，会更直观：

**工厂方法** 像开发商的精装交付——你只能在有限的户型里选择，拿到手就是成品，每套房子的装修风格是固定的。可以新增一种户型（新增工厂子类），但无法定制同一套房子的内部细节。

**Builder** 像业主自己找设计师装修——同一支装修队，可以按现代简约图纸施工，也可以按中式古典图纸施工，每家的风格由图纸决定，装修的每个步骤和细节都可以控制。

两者的关键区别不是"能创建几种产品"，而是**能否控制构建过程的细节**。工厂方法的可变点是"类型"（创建哪种产品），Builder 的可变点是"过程"（按什么步骤、用什么方式组装）。

作者: ztzt123
链接: [https://www.jianshu.com/p/15b001f5b95f](https://www.jianshu.com/p/15b001f5b95f)
来源: 简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

---

[http://blog.csdn.net/surprisesdu/article/details/621046](http://blog.csdn.net/surprisesdu/article/details/621046)

[http://smartfool.iteye.com/blog/71175](http://smartfool.iteye.com/blog/71175)

作者: ztzt123
链接: [https://www.jianshu.com/p/15b001f5b95f](https://www.jianshu.com/p/15b001f5b95f)
来源: 简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
