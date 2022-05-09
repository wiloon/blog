---
title: '配置文件  HOCON'
author: "-"
date: 2015-06-10T03:20:17+00:00
url: /?p=7776
categories:
  - Inbox
tags:
  - reprint
---
## '配置文件  HOCON'
HOCON (Human-Optimized Config Object Notation) 是一个易于使用的配置文件格式。
  
是由typesafe (开发scala和play framework的公司) 主导的项目
  
它被用于 Sponge 以及利用 Sponge API 的独立插件以储存重要的数据，比如配置或者玩家数据。HOCON 文件通常以 .conf 作为后缀名。

组成部分
  
一个 key 是一个键值对字符串中的前一个值
  
一个 value 可以是字符串、数字、对象、数组或者布尔值并紧随 key 的后面
  
一个 key-value separator 把键和值分离，可以是 : 或者 =
  
一个 comment 以 # 或者 // 开头，通常用于提供反馈或说明
  
示例: 

yellow-thing: "Sponge"
  
在这一示例中，key 是 yellow-thing，value 是 Sponge，而 key-value separator 是 :。

使用 HOCON
  
HOCON 要比 JSON (JavaScript Object Notation) 更灵活，因为书写一个合法的 HOCON 的方式要更多。下面是两个合法的 HOCON 的例子。

示例一: 

player: {
      
name: "Steve",
      
level: 30
  
}
  
示例二: 

player {
      
name = "Steve"
      
level = 30
  
}
  
在实际使用中，最好遵守你正在编辑的 HOCON 的格式约定。当你在编辑 Sponge 以及利用 Sponge API 的独立插件的 HOCON 配置文件的时候，除了值 (Value) 之外，其他的内容如无特殊要求，请不要动。

调试你的配置
  
如果 HOCON 配置文件似乎不会工作，这里有一些小提示。

花括号必须匹配
  
引号必须匹配
  
如果两个键重复，以后出现的为准
  
技术规范
  
在这里可以找到有关 HOCON 配置文件格式的更多信息。

https://www.zhihu.com/question/41253282
   
https://docs.spongepowered.org/stable/zh-CN/server/getting-started/configuration/hocon.html
  
https://github.com/go-akka/configuration