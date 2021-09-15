---
title: plantuml, puml + vs code
author: "-"
date: 2020-01-26T04:41:00+00:00
url: plantuml

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
skinparam classFontColor red

class Foo
note left: parent

class Bar
Bar : String field0
Bar : String method0()

Foo<|--Bar
note left: child
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

### 时序图
```puml
@startuml
Alice -> Bob: Authentication Request
Bob --> Alice: Authentication Response

Alice -> Bob: Another authentication Request
Alice <-- Bob: Another authentication Response

@enduml
```

### 组件图
- 别名后面可以标注颜色
- 修改线和箭头的颜色
- 文字颜色

```puml
@startuml
skinparam componentStyle rectangle
skinparam ParticipantFontColor #A9DCDF

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
@enduml
```

### plantuml server
```bash
podman run -d \
--name plantuml-server \
-p 30001:8080 plantuml/plantuml-server:jetty
```

>https://github.com/plantuml/plantuml-server