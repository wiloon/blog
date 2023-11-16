---
title: linux shell Manipulating Strings
author: "-"
date: 2012-04-08T06:13:32+00:00
url: /?p=2862
categories:
  - shell
tags:
  - reprint
---
## linux shell Manipulating Strings

[http://www.faqs.org/docs/abs/HTML/string-manipulation.html](http://www.faqs.org/docs/abs/HTML/string-manipulation.html)

## 连接字符串

```bash
a="abc"
b="def"

echo $a$b
```

expr index $string $substring
:   Numerical position in $string of first character in $substring that matches.

             1 stringZ=abcABC123ABCabc
   2 echo `expr index "$stringZ" C12`             # 6
   3                                              # C position.
   4
   5 echo `expr index "$stringZ" 1c`              # 3
   6 # 'c' (in #3 position) matches before '1'.

    This is the near equivalent of _strchr()_ in C.
    
    **ength of Matching Substring at Beginning of String**
    
    expr match "$string" '$substring'
    :   $substring is a [regular expression][1].
    
    expr "$string" : '$substring'
    :   $substring is a regular expression. 
        
        
          
            
                 1 stringZ=abcABC123ABCabc
   2 #       |------|
   3
   4 echo `expr match "$stringZ" 'abc[A-Z]*.2'`   # 8
   5 echo `expr "$stringZ" : 'abc[A-Z]*.2'`       # 8

 [1]: http://www.faqs.org/docs/abs/HTML/regexp.html#REGEXREF

## substring

```bash
b=${a:12:5}
where 12 is the offset (zero-based) and 5 is the length
```
