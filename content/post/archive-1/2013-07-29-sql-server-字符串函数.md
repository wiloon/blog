---
title: SQL Server 字符串函数
author: wiloon
type: post
date: 2013-07-29T01:41:33+00:00
url: /?p=5736
categories:
  - DataBase

---
#  {#docTitle}

<div id="docInfo">
</div>

<div id="docContent">
  <p>
    我们这里对 SQL Server 字符串函数进行分门别类地列出，便于查阅和记忆，相信大家都在其它方面有高深的编程基础，从字面上来说大家都知道这些函数的意义，就不对这些函数作过多的解释了，主要谈些经验，具体请参见联机丛书。
  </p>
  
  <p>
    <strong>ASCII(character_expression)</strong> 返回最左端字符的 ASCII 代码值<br /> <strong>CHAR(integer_expression)</strong>
  </p>
  
  <p>
    <strong>UNICODE(ncharacter_expression)</strong> 按照 Unicode 标准的定义，返回输入表达式的第一个字符的整数值。<br /> <strong>NCHAR(integer_expression)</strong>
  </p>
  
  <p>
    <strong>LOWER(character_expression)</strong> 以字符串中的字符小写返回<br /> <strong>UPPER(character_expression)</strong>
  </p>
  
  <p>
    <strong>LTRIM(character_expression)</strong> 截断左端英文空格<br /> <strong>RTRIM(character_expression)</strong>
  </p>
  
  <p>
    <strong>LEN(string_expression)</strong> 返回字符（不是字节）个数，不包含尾随的英文空格<br /> <strong>LEFT(character_expression, integer_expression)</strong> 尾随英文空格也可能被返回<br /> <strong>RIGHT(character_expression, integer_expression)</strong><br /> <strong>SUBSTRING(expression, start, length)</strong> 第一个字符的位置是 1
  </p>
  
  <p>
    <strong>CHARINDEX(expression1, expression2[, start_location])</strong> expression1 在 expression2 中的位置<br /> <strong>PATINDEX(%pattern%, expression) </strong>pattern 应该具有通配符，如同 like<br /> <strong>REVERSE(character_expression)</strong> 颠倒字符串<br /> <strong>REPLACE(string_expression, string_expression2, string_expression3)</strong> 用第三个表达式替换第一个表达式中的第二个表达式<br /> <strong>STUFF(character_expression, start, length, character_expression)</strong> 按 start、length 删除第一个表达式的内容并在 start 位置插入第四个表达式
  </p>
  
  <p>
    <strong>REPLICATION(character_expression, integer_expression)</strong> 重复字符串<br /> <strong>SPACE(integer_expression)</strong> 重复 integer_expression 个空格
  </p>
  
  <p>
    <strong>SOUNDEX(character_expression)</strong> 根据字符串情况，返回一个特定的四个长度的字符串<br /> <strong>DIFFERENCE(character_expression, character_expression)</strong> 比较两个表达式的 SOUNEX 返回值有几个字符不同，返回值[0-4]
  </p>
  
  <p>
    <strong>STR(float_expression[, length[, decimal]])</strong> 返回由数字转换成的字符串值<br /> <strong>QUOTENAME(character_string[, quote_character])</strong>  返回带有分隔符的 UNICODE 字符串
  </p>
  
  <p>
    <a href="http://www.cftea.com/c/2006/08/QK16SO3ZL14X15L9.asp">http://www.cftea.com/c/2006/08/QK16SO3ZL14X15L9.asp</a>
  </p>
</div>