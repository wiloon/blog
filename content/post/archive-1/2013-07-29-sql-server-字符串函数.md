---
title: SQL Server 字符串函数
author: "-"
type: post
date: 2013-07-29T01:41:33+00:00
url: /?p=5736
categories:
  - DataBase

---
#  {#docTitle}




  
    我们这里对 SQL Server 字符串函数进行分门别类地列出，便于查阅和记忆，相信大家都在其它方面有高深的编程基础，从字面上来说大家都知道这些函数的意义，就不对这些函数作过多的解释了，主要谈些经验，具体请参见联机丛书。
  
  
    ASCII(character_expression) 返回最左端字符的 ASCII 代码值
 CHAR(integer_expression)
  
  
    UNICODE(ncharacter_expression) 按照 Unicode 标准的定义，返回输入表达式的第一个字符的整数值。
 NCHAR(integer_expression)
  
  
    LOWER(character_expression) 以字符串中的字符小写返回
 UPPER(character_expression)
  
  
    LTRIM(character_expression) 截断左端英文空格
 RTRIM(character_expression)
  
  
    LEN(string_expression) 返回字符（不是字节) 个数，不包含尾随的英文空格
 LEFT(character_expression, integer_expression) 尾随英文空格也可能被返回
 RIGHT(character_expression, integer_expression)
 SUBSTRING(expression, start, length) 第一个字符的位置是 1
  
  
    CHARINDEX(expression1, expression2[, start_location]) expression1 在 expression2 中的位置
 PATINDEX(%pattern%, expression) pattern 应该具有通配符，如同 like
 REVERSE(character_expression) 颠倒字符串
 REPLACE(string_expression, string_expression2, string_expression3) 用第三个表达式替换第一个表达式中的第二个表达式
 STUFF(character_expression, start, length, character_expression) 按 start、length 删除第一个表达式的内容并在 start 位置插入第四个表达式
  
  
    REPLICATION(character_expression, integer_expression) 重复字符串
 SPACE(integer_expression) 重复 integer_expression 个空格
  
  
    SOUNDEX(character_expression) 根据字符串情况，返回一个特定的四个长度的字符串
 DIFFERENCE(character_expression, character_expression) 比较两个表达式的 SOUNEX 返回值有几个字符不同，返回值[0-4]
  
  
    STR(float_expression[, length[, decimal]]) 返回由数字转换成的字符串值
 QUOTENAME(character_string[, quote_character])  返回带有分隔符的 UNICODE 字符串
  
  
    http://www.cftea.com/c/2006/08/QK16SO3ZL14X15L9.asp
  
