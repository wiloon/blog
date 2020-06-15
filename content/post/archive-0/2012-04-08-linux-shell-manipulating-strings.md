---
title: linux shell Manipulating Strings
author: wiloon
type: post
date: 2012-04-08T06:13:32+00:00
url: /?p=2862
categories:
  - Linux

---
<http://www.faqs.org/docs/abs/HTML/string-manipulation.html>



连接字符串

[shell]

a="abc"

b="def"

echo $a$b

[/shell]

expr index $string $substring
:   Numerical position in $string of first character in $substring that matches. 
    
    <table width="90%" border="0" bgcolor="#E0E0E0">
      <tr>
        <td>
          <pre>   1 stringZ=abcABC123ABCabc
   2 echo `expr index "$stringZ" C12`             # 6
   3                                              # C position.
   4 
   5 echo `expr index "$stringZ" 1c`              # 3
   6 # 'c' (in #3 position) matches before '1'.</pre>
        </td>
      </tr>
    </table>
    
    This is the near equivalent of _strchr()_ in C.
    
    **ength of Matching Substring at Beginning of String**
    
    expr match "$string&#8221; &#8216;$substring&#8217;
    :   <tt><em>$substring</em></tt> is a [regular expression][1].
    
    expr "$string&#8221; : &#8216;$substring&#8217;
    :   <tt><em>$substring</em></tt> is a regular expression. 
        
        <table width="90%" border="0" bgcolor="#E0E0E0">
          <tr>
            <td>
              <pre>   1 stringZ=abcABC123ABCabc
   2 #       |------|
   3 
   4 echo `expr match "$stringZ" 'abc[A-Z]*.2'`   # 8
   5 echo `expr "$stringZ" : 'abc[A-Z]*.2'`       # 8</pre>
            </td>
          </tr>
        </table>

 [1]: http://www.faqs.org/docs/abs/HTML/regexp.html#REGEXREF