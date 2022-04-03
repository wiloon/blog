---
title: yaml
author: "-"
date: 2011-08-19T02:34:08+00:00
url: /?p=450
categories:
  - Linux

tags:
  - reprint
---
## yaml
http://www.ruanyifeng.com/blog/2016/07/yaml.html

YAML 语言 (发音 /ˈjæməl/ ) 的设计目标，就是方便人类读写。它实质上是一种通用的数据串行化格式。  
它的基本语法规则如下。  
大小写敏感  
使用缩进表示层级关系  
缩进时不允许使用Tab键，只允许使用空格。  
缩进的空格数目不重要，只要相同层级的元素左侧对齐即可  

    # 表示注释，从这个字符一直到行尾，都会被解析器忽略。

### YAML 支持的数据结构有三种。  
- 对象: 键值对的集合，又称为映射 (mapping) / 哈希 (hashes)  / 字典 (dictionary)   
- 数组: 一组按次序排列的值，又称为序列 (sequence)  / 列表 (list) 
- 纯量 (scalars) : 单个的、不可再分的值