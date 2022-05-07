---
title: BNF 巴科斯范式
author: "-"
date: 2013-06-13T04:56:57+00:00
url: /?p=5528
categories:
  - Inbox
tags:
  - reprint
---
## BNF 巴科斯范式

  BNF & Augmented BNF

### 巴科斯范式

  巴科斯范式(BNF: Backus-Naur Form 的缩写)是由 John Backus 和 Peter Naur 首次引入一种形式化符号来描述给定语言的语法 (最早用于描述ALGOL 60 编程语言) 。确切地说，早在UNESCO (联合国教科文组织) 关于ALGOL 58的会议上提出的一篇报告中，Backus就引入了大部分BNF符号。虽然没有什么人读过这篇报告，但是在Peter Naur读这篇报告时，他发现Backus对ALGOL 58的解释方式和他的解释方式有一些不同之处，这使他感到很惊奇。首次设计ALGOL的所有参与者都开始发现了他的解释方式的一些弱点，所以他决定对于以后版本的ALGOL应该以一种类似的形式进行描述，以让所有参与者明白他们在对什么达成一致意见。他做了少量修改，使其几乎可以通用，在设计ALGOL 60的会议上他为ALGOL 60草拟了自己的BNF。看你如何看待是谁发明了BNF了，或者认为是Backus在1959年发明的，或者认为是Naur在1960年中发明。 (关于那个时期编程语言历史的更多细节，参见1978年8月，《Communications of the ACM (美国计算机学会通讯) 》，第21卷，第8期中介绍Backus获图灵奖的文章。这个注释是由来自Los Alamos Natl.实验室的William B. Clodius建议的) 。


  现在，几乎每一位新编程语言书籍的作者都使用巴科斯范式来定义编程语言的语法规则。

### 巴科斯范式的内容
在双引号中的字("word")代表着这些字符本身。而double_quote用来代表双引号。
在双引号外的字 (有可能有下划线) 代表着语法部分。


  尖括号( < > )内包含的为必选项。


  方括号( [ ] )内包含的为可选项。


  大括号( { } )内包含的为可重复0至无数次的项。


  竖线( | )表示在其左右两边任选一项，相当于"OR"的意思。


  ::= 是"被定义为"的意思。


  巴科斯范式示例


  这是用BNF来定义的Java语言中的For语句的实例: 


  FOR_STATEMENT ::=


  "for" "(" ( variable_declaration |


  ( expression ";" ) | ";" )


  [ expression ] ";"


  [ expression ]


  ")" statement


  这是Oracle packages的BNF定义: 


  package_body ::= "package" package_name "is"


  package_obj_body


  [ "begin" seq_of_statements ]


  "end" [ package_name ] ";"


  package_obj_body ::= variable_declaration


  | subtype_declaration


  | cursor_declaration


  | cursor_body


  | exception_declaration


  | record_declaration


  | plsql_table_declaration


  | procedure_body


  | function_body


  procedure_body ::= "procedure" procedure_name


  [ "(" argument { "," argument } ")" ]


  "return" return_type


  "is"


  [ "declare" declare_spec ";" { declare_spec ";" } ]


  "begin"


  seq_of_statements


  [ "exception" exception_handler ]


  "end" [ procedure_name ] ";"


  statement ::= comment


  | assignment_statement


  | exit_statement


  | goto_statement


  | if_statement


  | loop_statement


  | null_statement


  | raise_statement


  | return_statement


  | sql_statement


  | plsql_block


  这是用BNF来定义的BNF本身的例子: 


  syntax ::=


  rule ::= identifier "::=" expression


  expression ::= term { "|" term }


  term ::= factor


  factor ::= identifier |


  quoted_symbol |


  "(" expression ")" |


  "[" expression "]" |


  "{" expression "}"


  identifier ::= letter { letter | digit }


  quoted_symbol ::= """ """

### 扩展的巴科斯范式 Augmented BNF

  RFC2234 定义了扩展的巴科斯范式(ABNF)。近年来在Internet的定义中ABNF被广泛使用。ABNF做了更多的改进，比如说，在ABNF中，尖括号不再需要。
