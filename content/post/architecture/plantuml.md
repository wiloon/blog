---
title: plantuml, puml
author: "-"
date: 2020-01-26T04:41:00+00:00
url: plantuml
categories:
  - uml
tags:
  - reprint
---
## plantuml, puml

- 时序图, Sequence Diagram
- Use Case Diagram
- 类图, Class Diagram
- Object Diagram
- 活动图, Activity Diagram
- 组件图, Component Diagram
- 部署图, Deployment Diagram
- 状态图, State Diagram
- Timing Diagram

## UML 图

### 时序图, Sequence Diagram

```puml
@startuml
Alice -> Bob: Authentication Request
Bob --> Alice: Authentication Response

Alice -> Bob: Another authentication Request
Alice <-- Bob: Another authentication Response
Alice ->> Bob: async msg
@enduml
```

### 类图, Class Diagram

```puml
@startuml
skinparam classFontColor red

class Foo
note left: parent

class Bar
Bar : String field0
Bar : String method0()

Foo<|--Bar
note left: child

abstract class Abstract0
Foo--|>Abstract0

interface Interface0

' 注意, 接口名和冒号之间必须用空格分隔
Interface0 : void method0()
@enduml
```

```puml
@startuml

skinparam class {
    BackgroundColor Lightblue
    ArrowColor #0ACF97
    BorderColor #d5d5d5
}

skinparam stereotypeCBackgroundColor YellowGreen

Class101 <|.. Class102
@enduml
```

### 活动图, Activity Diagram

```puml
@startuml
!theme plain

start

if (foo?) then (yes)
  :process0;
else (no)
  :process1;
endif

stop
@enduml
```

### 组件图, Component Diagram

- 别名后面可以标注颜色
- 修改线和箭头的颜色
- 文字颜色

#### 语法

```bash
# 把组件显示成普通矩形
skinparam componentStyle rectangle
# 组件间横向距离
skinparam nodesep 10
# 组件间纵向距离
skinparam ranksep 10
```

```puml
@startuml
skinparam componentStyle rectangle
skinparam nodesep 10
skinparam ranksep 10
skinparam ParticipantFontColor #A9DCDF

' comments line starts by single quote, 注释
[First component]
[Another component] as Comp2  
component Comp3
component [Last\ncomponent] as Comp4

[component0] as c0 #ff0000
[<color:#ff0000>component1</color>] as c1
[component2] as c2
[component3] as c3
[component4] as c4

c0 -- c1
c0-[#00ff00]-c2
c1--c3
c0--c3

c2--c4

note left of c0
note0
end note
@enduml
```

### 部署图, Deployment Diagram

```puml
@startuml
circle 1
circle 2
circle 3
agent 4

1 -- 2
1 -- 3
1 -- 4

queue 5
4 -right- 5
5 -right-2
@enduml
```

## 状态图, State Diagram

```plantuml
@startuml
[*] --> State1
State1 --> [*]
State1 : this is a string
State1 : this is another string

State1 -> State2
State2 --> [*]
@enduml

```

## 安装 graphviz

```bash
sudo apt-get install -y graphviz
```

[https://graphviz.org/download/](https://graphviz.org/download/)

VS-Code扩展

使用PlantUML

vim foo.md

## vs code 渲染 uml 的快捷键

ctrl + p> PlantUML: Preview Current Diagram

```bash
ctrl + alt + d
```

[https://www.jianshu.com/p/ed0e979657f4](https://www.jianshu.com/p/ed0e979657f4)

theme: plain,sandstone,sketchy-outline

## 线路径

添加隐藏行a -[hidden]- b
延长线a --- b的长度 (更多破折号，更长的线)
指定行的首选方向 (a -left- b)
交换关联结束 (a -- b→b -- a)
更改定义的顺序 (订单 重要......有时候)
添加空白节点，背景/边框颜色设置为透明

## plantuml server

https://hub.docker.com/r/plantuml/plantuml-server

```bash
docker run -d \
--name plantuml \
-p 30001:8080 plantuml/plantuml-server:jetty-v1.2023.13

podman run -d \
--name plantuml \
-p 30001:8080 plantuml/plantuml-server:jetty-v1.2022.14
```

## 定义组件的相对位置

一种典型的方法是将一行标记为隐藏(hidden)
hidden只支持从左到右`->`和从上到下的 `-->` 行,因此您需要相应地放置左侧和右侧(X <[hidden]- Y似乎不支持语法).

```plantuml
@startuml
component JMM {
  [heap]
  [thread stack] as ts0
  [thread stack] as ts1
  [thread stack] as ts2

  ts0 -[hidden]-> heap
  ts1 -[hidden]-> heap
  ts2 -[hidden]-> heap

}
@enduml
```

[https://github.com/plantuml/plantuml-server](https://github.com/plantuml/plantuml-server)

## dot executable /opt/local/bin/dot File does not exist

```bash
pacman -S graphviz
```

## 思维导图 mind map

```plantuml
@startmindmap
* Debian
** Ubuntu
*** Linux Mint
*** Kubuntu
*** Lubuntu
*** KDE Neon
** LMDE
** SolydXK
** SteamOS
** Raspbian with a very long name
*** <s>Raspmbc</s> => OSMC
*** <s>Raspyfi</s> => Volumio
@endmindmap
```
