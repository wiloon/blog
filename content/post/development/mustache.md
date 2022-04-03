---
title: "Mustache语法"
author: "-"
date: ""
url: ""
categories:
  - inbox
tags:
  - inbox
---
## "Mustache语法"

Mustache是一个logic-less (轻逻辑) 模板解析引擎，  
它是为了使用户界面与业务数据 (内容) 分离而产生的，  
它可以生成特定格式的文档，通常是标准的HTML文档。  
比如小程序的wxml中的代码

    {{userInfo.nickName}}，这里的{{ }}就是Mustache的语法。

### Mustache的模板语法很简单，就那么几个

1. {{keyName}}
2. {{{keyName}}}
3. {{#keyName}} {{/keyName}}
4. {{^keyName}} {{/keyName}}
5. {{.}}
6. {{!comments}}
7. {{>partials}}