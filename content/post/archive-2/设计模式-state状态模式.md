---
title: 设计模式 – State/状态模式
author: "-"
date: 2017-01-23T06:47:46+00:00
url: /?p=9678
categories:
  - Design Pattern
tags:
  - reprint
---
## 设计模式 – State/状态模式
State模式的定义: 不同的状态,不同的行为;或者说,每个状态有着相应的行为.

何时使用?
  
State模式在实际使用中比较多,适合"状态的切换".因为我们经常会使用If elseif else 进行状态切换, 如果针对状态的这样判断切换反复出现,我们就要联想到是否可以采取State模式了.

不只是根据状态,也有根据属性.如果某个对象的属性不同,对象的行为就不一样,这点在数据库系统中出现频率比较高,我们经常会在一个数据表的尾部,加上property属性含义的字段,用以标识记录中一些特殊性质的记录,这种属性的改变(切换)又是随时可能发生的,就有可能要使用State.
  
是否使用?
  
在实际使用,类似开关一样的状态切换是很多的,但有时并不是那么明显,取决于你的经验和对系统的理解深度.

这里要阐述的是"开关切换状态" 和" 一般的状态判断"是有一些区别的, " 一般的状态判断"也是有 if..elseif结构,例如:

if (which==1) state="hello";
  
else if (which==2) state="hi";
  
else if (which==3) state="bye";
  
这是一个 " 一般的状态判断",state值的不同是根据which变量来决定的,which和state没有关系.如果改成:

if (state.euqals("bye")) state="hello";
  
else if (state.euqals("hello")) state="hi";
  
else if (state.euqals("hi")) state="bye";
  
这就是 "开关切换状态",是将state的状态从"hello"切换到"hi",再切换到""bye";在切换到"hello",好象一个旋转开关,这种状态改变就可以使用State模式了.

如果单纯有上面一种将"hello"->"hi"->"bye"->"hello"这一个方向切换,也不一定需要使用State模式,因为State模式会建立很多子类,复杂化,但是如果又发生另外一个行为:将上面的切换方向反过来切换,或者需要任意切换,就需要State了.

请看下例:

```java

import java.awt.*;

public class OldContext {

private Color state = null;

public void push() {

//如果当前red状态 就切换到blue
   
if (state == Color.red) state = Color.blue;

//如果当前blue状态 就切换到green
   
else if (state == Color.blue) state = Color.green;

//如果当前black状态 就切换到red
   
else if (state == Color.black) state = Color.red;

//如果当前green状态 就切换到black
   
else if (state == Color.green) state = Color.black;

Sample sample = new Sample(state);
   
sample.operate();
   
}

public void pull() {

//与push状态切换正好相反

if (state == Color.green) state = Color.blue;
   
else if (state == Color.black) state = Color.green;
   
else if (state == Color.blue) state = Color.red;
   
else if (state == Color.red) state = Color.black;

Sample sample2 = new Sample(state);
   
sample2.operate();
   
}

}

```

在上例中,我们有两个动作push推和pull拉,这两个开关动作,改变了Context颜色,至此,我们就需要使用State模式优化它.


另外注意:但就上例,state的变化,只是简单的颜色赋值,这个具体行为是很简单的,State适合巨大的具体行为,因此在,就本例,实际使用中也不一定非要使用State模式,这会增加子类的数目,简单的变复杂.

例如: 银行帐户, 经常会在Open 状态和Close状态间转换.

例如: 经典的TcpConnection, Tcp的状态有创建 侦听 关闭三个,并且反复转换,其创建 侦听 关闭的具体行为不是简单一两句就能完成的,适合使用State

例如:信箱POP帐号, 会有四种状态, start HaveUsername Authorized quit,每个状态对应的行为应该是比较大的.适合使用State

例如:在工具箱挑选不同工具,可以看成在不同工具中切换,适合使用State.如 具体绘图程序,用户可以选择不同工具绘制方框 直线 曲线,这种状态切换可以使用State.

如何使用
  
State需要两种类型实体参与:

1.state manager 状态管理器 ,就是开关 ,如上面例子的Context实际就是一个state manager, 在state manager中有对状态的切换动作.
  
2.用抽象类或接口实现的父类,,不同状态就是继承这个父类的不同子类.
  
以上面的Context为例.我们要修改它,建立两个类型的实体.
  
第一步: 首先建立一个父类:

```java

import java.awt.*;
  
public abstract class State {

public abstract void handlePush(NewContext c);

public abstract void handlePull(NewContext c);

public abstract Color getColor();

}

```

父类中的方法要对应state manager中的开关行为,在state manager中 本例就是Context中,有两个开关动作push推和pull拉.那么在状态父类中就要有具体处理这两个动作:handlepush() handlepull(); 同时还需要一个获取push或pull结果的方法getcolor()


下面是具体子类的实现:

```java

import java.awt.*;

public class BlueState extends State {
   
@Override
   
public void handlePush(NewContext c) {
   
//根据push方法"如果是blue状态的切换到green" ;
   
c.setState(new GreenState());
   
}

@Override
   
public void handlePull(NewContext c) {

//根据pull方法"如果是blue状态的切换到red" ;
   
c.setState(new RedState());
   
}

public Color getColor() {
   
return (Color.blue);
   
}

}

```

同样 其他状态的子类实现如blue一样.


第二步: 要重新改写State manager 也就是本例的Context:

```java

import java.awt.*;

public class OldContext {

private Color state = null;

public void push() {

//如果当前red状态 就切换到blue
   
if (state == Color.red) state = Color.blue;

//如果当前blue状态 就切换到green
   
else if (state == Color.blue) state = Color.green;

//如果当前black状态 就切换到red
   
else if (state == Color.black) state = Color.red;

//如果当前green状态 就切换到black
   
else if (state == Color.green) state = Color.black;

Sample sample = new Sample(state);
   
sample.operate();
   
}

public void pull() {

//与push状态切换正好相反

if (state == Color.green) state = Color.blue;
   
else if (state == Color.black) state = Color.green;
   
else if (state == Color.blue) state = Color.red;
   
else if (state == Color.red) state = Color.black;

Sample sample2 = new Sample(state);
   
sample2.operate();
   
}

}

```

至此,我们也就实现了State的refactorying过程.


以上只是相当简单的一个实例,在实际应用中,handlepush或handelpull的处理是复杂的.

状态模式优点: 
  
 (1)  封装转换过程,也就是转换规则
  
 (2)  枚举可能的状态,因此,需要事先确定状态种类。
  
状态模式可以允许客户端改变状态的转换行为,而状态机则是能够自动改变状态,状态机是一个比较独立的而且复杂的机制,具体可参考一个状态机开源项目: http://sourceforge.net/projects/smframework/

状态模式在工作流或游戏等各种系统中有大量使用,甚至是这些系统的核心功能设计,例如政府OA中,一个批文的状态有多种: 未办；正在办理；正在批示；正在审核；已经完成等各种状态,使用状态机可以封装这个状态的变化规则,从而达到扩充状态时,不必涉及到状态的使用者。

在网络游戏中,一个游戏活动存在开始；开玩；正在玩；输赢等各种状态,使用状态模式就可以实现游戏状态的总控,而游戏状态决定了游戏的各个方面,使用状态模式可以对整个游戏架构功能实现起到决定的主导作用。

状态模式实质: 
  
使用状态模式前,客户端外界需要介入改变状态,而状态改变的实现是琐碎或复杂的。

使用状态模式后,客户端外界可以直接使用事件Event实现,根本不必关心该事件导致如何状态变化,这些是由状态机等内部实现。

这是一种Event-condition-State,状态模式封装了condition-State部分。

每个状态形成一个子类,每个状态只关心它的下一个可能状态,从而无形中形成了状态转换的规则。如果新的状态加入,只涉及它的前一个状态修改和定义。

状态转换有几个方法实现: 一个在每个状态实现next(),指定下一个状态；还有一种方法,设定一个StateOwner,在StateOwner设定stateEnter状态进入和stateExit状态退出行为。

状态从一个方面说明了流程,流程是随时间而改变,状态是截取流程某个时间片。


http://www.jdon.com/designpatterns/designpattern_State.htm

设计模式之State
  
板桥里人 http://www.jdon.com 2002/4/6/

