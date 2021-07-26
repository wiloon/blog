---
title: plantuml, puml + vs code
author: "-"
type: post
date: 2020-01-26T04:41:00+00:00
url: /?p=15419

---
### 安装 graphviz
    sudo apt-get install -y graphviz

VS-Code扩展

使用PlantUML

vim foo.md

### content
```puml
@startuml

[First component]
[Another component] as Comp2  
component Comp3
component [Last\ncomponent] as Comp4

@enduml
```

### vs code渲染uml的快捷键
    alt+d

https://www.jianshu.com/p/ed0e979657f4

### 活动图
```puml
@startuml
start

if (foo?) then (yes)
  :process0;
else (no)
  :process1;
endif

stop
@enduml
```

### 类图
```puml
@startuml
class Foo
note left: parent

class Bar
Bar : String field0
Bar : String method0()

Foo<|--Bar
note left: child
@enduml
```

### 线路径
添加隐藏行a -[hidden]- b
延长线a --- b的长度（更多破折号，更长的线）
指定行的首选方向（a -left- b）
交换关联结束（a -- b→b -- a）
更改定义的顺序（订单 重要......有时候）
添加空白节点，背景/边框颜色设置为透明

### 部署图
```puml
@startuml
circle 1
circle 2
circle 3

1 -- 2
1 -- 3

@enduml
```