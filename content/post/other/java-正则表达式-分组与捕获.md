---
title: JAVA 正则表达式 分组与捕获
author: "-"
date: 2012-08-19T05:17:42+00:00
url: /?p=3918
categories:
  - Java
tags:
  - Regex

---
## JAVA 正则表达式 分组与捕获
```java
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Fenzhu
{
public static void main(String[] args)
{
Pattern p = Pattern.compile("(/d{3,5})([a-z]{2})");
String s = "123aa-34345bb-234cc-00";
Matcher m = p.matcher(s);
while(m.find())
{
System.out.println("m.group():"+m.group()); //打印所有

System.out.println("m.group(1):"+m.group(1)); //打印数字的

System.out.println("m.group(2):"+m.group(2)); //打印字母的
System.out.println();

}
System.out.println("捕获个数:groupCount()="+m.groupCount());
}
}

```

 

1        概述

1.1     什么是捕获组

捕获组就是把正则表达式中子表达式匹配的内容，保存到内存中以数字编号或显式命名的组里，方便后面引用。当然，这种引用既可以是在正则表达式内部，也可以是在正则表达式外部。

捕获组有两种形式，一种是普通捕获组，另一种是命名捕获组，通常所说的捕获组指的是普通捕获组。语法如下: 

普通捕获组: (Expression)

命名捕获组: (?<name>Expression)

普通捕获组在大多数支持正则表达式的语言或工具中都是支持的，而命名捕获组目前只有.NET、PHP、Python等部分语言支持，据说Java会在7.0中提供对这一特性的支持。上面给出的命名捕获组的语法是.NET中的语法，另外在.NET中使用(?'name'Expression)与使用(?<name>Expression)是等价的。在PHP和Python中命名捕获组语法为: (?P<name>Expression)。

另外需要说明的一点是，除(Expression)和(?<name>Expression)语法外，其它的(?...)语法都不是捕获组。

## 1.2     捕获组编号规则

编号规则指的是以数字为捕获组进行编号的规则，在普通捕获组或命名捕获组单独出现的正则表达式中，编号规则比较清晰，在普通捕获组与命名捕获组混合出现的正则表达式中，捕获组的编号规则稍显复杂。

在展开讨论之前，需要说明的是，编号为0的捕获组，指的是正则表达式整体，这一规则在支持捕获组的语言中，基本上都是适用的。下面对其它编号规则逐一展开讨论。

### 1.2.1  普通捕获组编号规则

如果没有显式为捕获组命名，即没有使用命名捕获组，那么需要按数字顺序来访问所有捕获组。在只有普通捕获组的情况下，捕获组的编号是按照"("出现的顺序，从左到右，从1开始进行编号的 。

正则表达式: **(\d{4})-(\d{2}-(\d\d))**

 

上面的正则表达式可以用来匹配格式为yyyy-MM-dd的日期，为了在下表中得以区分，月和日分别采用了\d{2}和\d\d这两种写法。

用以上正则表达式匹配字符串: 2008-12-31，匹配结果为: 


  
    
      编号
    
    
    
      命名
    
    
    
      捕获组
    
    
    
      匹配内容
    
  
  
  
    
      
    
    
    
    
    
    
      (\d{4})-(\d{2}-(\d\d))
    
    
    
      2008-12-31
    
  
  
  
    
      1
    
    
    
    
    
    
      (\d{4})
    
    
    
      2008
    
  
  
  
    
      2
    
    
    
    
    
    
      (\d{2}-(\d\d))
    
    
    
      12-31
    
  
  
  
    
      3
    
    
    
    
    
    
      (\d\d)
    
    
    
      31
    
  


### 1.2.2  命名捕获组编号规则

命名捕获组通过显式命名，可以通过组名方便的访问到指定的组，而不需要去一个个的数编号，同时避免了在正则表达式扩展过程中，捕获组的增加或减少对引用结果导致的不可控。

不过容易忽略的是，命名捕获组也参与了编号的，在只有命名捕获组的情况下，捕获组的编号也是按照"("出现的顺序，从左到右，从1开始进行编号的 。

正则表达式: **(?<year>\d{4})-(?<date>\d{2}-(?<day>\d\d))**

 

用以上正则表达式匹配字符串: 2008-12-31

匹配结果为: 


  
    
      编号
    
    
    
      命名
    
    
    
      捕获组
    
    
    
      匹配内容
    
  
  
  
    
      
    
    
    
    
    
    
      (?<year>\d{4})-(?<date>\d{2}-(?<day>\d\d))
    
    
    
      2008-12-31
    
  
  
  
    
      1
    
    
    
      year
    
    
    
      (?<year>\d{4})
    
    
    
      2008
    
  
  
  
    
      2
    
    
    
      date
    
    
    
      (?<date>\d{2}-(?<day>\d\d))
    
    
    
      12-31
    
  
  
  
    
      3
    
    
    
      day
    
    
    
      (?<day>\d\d)
    
    
    
      31
    
  


### 1.2.3  普通捕获组与命名捕获组混合编号规则

当一个正则表达式中，普通捕获组与命名捕获组混合出现时，捕获组的编号规则稍显复杂。对于其中的命名捕获组，随时都可以通过组名进行访问，而对于普通捕获组，则只能通过确定其编号后进行访问。

混合方式的捕获组编号，首先按照普通捕获组中"("出现的先后顺序，从左到右，从1开始进行编号，当普通捕获组编号完成后，再按命名捕获组中"("出现的先后顺序，从左到右，接着普通捕获组的编号值继续进行编号。

也就是先忽略命名捕获组，对普通捕获组进行编号，当普通捕获组完成编号后，再对命名捕获组进行编号。

正则表达式: **(\d{4})-(?<date>\d{2}-(\d\d))**

 

用以上正则表达式匹配字符串: 2008-12-31，匹配结果为: 


  
    
      编号
    
    
    
      命名
    
    
    
      捕获组
    
    
    
      匹配内容
    
  
  
  
    
      
    
    
    
    
    
    
      (\d{4})-(?<date>\d{2}-(\d\d))
    
    
    
      2008-12-31
    
  
  
  
    
      1
    
    
    
    
    
    
      (\d{4})
    
    
    
      2008
    
  
  
  
    
      3
    
    
    
      date
    
    
    
      (?<date>\d{2}-(\d\d))
    
    
    
      12-31
    
  
  
  
    
      2
    
    
    
    
    
    
      (\d\d)
    
    
    
      31
    
  


# 2       捕获组的引用

对捕获组的引用一般有以下几种: 

1)       正则表达式中，对前面捕获组捕获的内容进行引用，称为反向引用；

2)       正则表达式中，(?(name)yes|no)的条件判断结构；

3)       在程序中，对捕获组捕获内容的引用。

## 2.1     反向引用

捕获组捕获到的内容，不仅可以在正则表达式外部通过程序进行引用，也可以在正则表达式内部进行引用，这种引用方式就是反向引用。

反向引用的作用通常是用来查找或限定重复，限定指定标识配对出现等等。

对于普通捕获组和命名捕获组的引用，语法如下: 

普通捕获组反向引用: \k<number>，通常简写为\number

命名捕获组反向引用: \k<name>或者\k'name'

普通捕获组反向引用中number是十进制的数字，即捕获组的编号；命名捕获组反向引用中的name为命名捕获组的组名。

反向引用涉及到的内容比较多，后续单独说明。

## 2.2     条件判断表达式

条件判断结构在平衡组中谈到过，基本应用和扩展应用都可以在其中找到例子，这里不再赘述，请参考 [.NET正则基础之——平衡组][1]。

## 2.3     程序中引用

根据语言的不同，程序中对捕获组引用的方式也有所不同，下面就JavaScript和.NET进行举例说明。

### 2.3.1  JavaScript中的引用

由于JavaScript中不支持命名捕获组，所以对于捕获组的引用就只支持普通捕获组的反向引用和$number方式的引用。程序中的引用一般在替换和匹配时使用。

注: 以下应用举例仅考虑简单应用场景，对于这种复杂场景暂不考虑。

1)         在Replace中引用，通常是通过$number方式引用。

举例: 替换掉html标签中的属性。<textareaid="result"rows="10"cols="100"></textarea><scripttype="text/javascript">var data ="   

  

";var reg = /<([a-z]+)[^>]*>/ig;document.getElementById("result").value = data.replace(reg,"<$1>");</script>//输出


  
    
      test 
    
  


2)         在匹配时的引用，通常通过RegExp.$number方式引用。

举例: 同时获取<img…>中的src和name属性值，属性的顺序不固定。参考 [一条正则能不能同时取出一个img标记的src和name?][2]

 

[javascript][/javascript]

[view plain][3][copy][3]

<

ol>

  * <textarea id="result" rows="10" cols="100"></textarea>
  * <script type="text/javascript">
  * **var** data = [' <img alt="" border="0" name="g6-o44-1" onload="DrawImage" src="/bmp/foo1.jpg" />', ' <img src="/bmp/foo2.jpg" alt="" border="0" name="g6-o44-2" onload="DrawImage" />'] ;
  * **var** reg = /<img\b(?=(?:(?!name=).)_name=(['"]?)([^'"\s>]+)\1)(?:(?!src=).)_src=(['"]?)([^'"\s>]+)\3[^>]*>/i;
  * **for**(**var** i=0;i<data.length;i++)
  * {
  *     **var** s = data[i];
  *     document.getElementById("result").value += "源字符串: " + s + "\n";
  *     document.write("<br />");
  *     **if**(reg.test(s))
  *     {
  *         document.getElementById("result").value += "name: " + RegExp.$2 + "\n";
  *         document.getElementById("result").value += "src: " + RegExp.$4 + "\n";
  *     }
  * }
  * </script> 

 

 

### 2.3.2  .NET中的引用

由于.NET支持命名捕获组，所以在.NET中的引用方式会多一些。通常也是在两种场景下应用，一是替换，一是匹配。

1)         替换中的引用

普通捕获组: $number

命名捕获组: ${name}

替换中应用，仍是上面的例子。

举例: 替换掉html标签中的属性。使用普通捕获组。

string data = "  

  

";

richTextBox2.Text = Regex.Replace(data, @"(?i)<([a-z]+)[^>]*>", "<$1>");

[//输出][4]


  
    
      test 
    
  


使用命名捕获组。

string data = "  

  

";

richTextBox2.Text = Regex.Replace(data, @"(?i)<(?<tag>[a-z]+)[^>]*>", "<${tag}>");

[//输出][4]


  
    
      test 
    
  


2)         匹配后的引用

对于匹配结果中捕获组捕获内容的引用，可以通过Groups和Result对象进行引用。

string test = "CSDN";

Regex reg = new Regex(@"(?is)[^""'\s>]_)\1[^>]_>(?<text>(?:(?!).)_)");

MatchCollection mc = reg.Matches(test);

foreach (Match m in mc)

{

richTextBox2.Text += "m.Value: ".PadRight(25) + m.Value + "\n";

richTextBox2.Text += "m.Result(\"$0\"): ".PadRight(25) + m.Result("$0") + "\n";

richTextBox2.Text += "m.Groups[0].Value: ".PadRight(25) + m.Groups[0].Value + "\n";

richTextBox2.Text += "m.Result(\"$2\"): ".PadRight(25) + m.Result("$2") + "\n";

richTextBox2.Text += "m.Groups[2].Value: ".PadRight(25) + m.Groups[2].Value + "\n";

richTextBox2.Text += "m.Result(\"${url}\"): ".PadRight(25) + m.Result("${url}") + "\n";

richTextBox2.Text += "m.Groups[\"url\"].Value: ".PadRight(25) + m.Groups["url"].Value + "\n";

richTextBox2.Text += "m.Result(\"$3\"): ".PadRight(25) + m.Result("$3") + "\n";

richTextBox2.Text += "m.Groups[3].Value: ".PadRight(25) + m.Groups[3].Value + "\n";

richTextBox2.Text += "m.Result(\"${text}\"): ".PadRight(25) + m.Result("${text}") + "\n";

richTextBox2.Text += "m.Groups[\"text\"].Value: ".PadRight(25) + m.Groups["text"].Value + "\n";

}

//输出

m.Value:                  [CSDN][5]

m.Result("$0"):           [CSDN][5]

m.Groups[0].Value:        [CSDN][5]

m.Result("$2"):           http://www.csdn.net

m.Groups[2].Value:        http://www.csdn.net

m.Result("${url}"):       http://www.csdn.net

m.Groups["url"].Value:    http://www.csdn.net

m.Result("$3"):           CSDN

m.Groups[3].Value:        CSDN

m.Result("${text}"):      CSDN

m.Groups["text"].Value:   CSDN

对于捕获组0的引用，可以简写作m.Value。

 

<http://blog.csdn.net/lovingprince/article/details/2774819>


  
    正则表达式在字符串处理中经常使用，关于正则简单的用法相信有一点程序基础的人都懂得一些，这里就不介绍简单基础了。这里主要讲解一下在JAVA中实现了的正则的高级用法-分组与捕获。
  
  
    对于要重复单个字符，非常简单，直接在字符后卖弄加上限定符即可，例如 a+ 表示匹配1个或一个以上的a，a?表示匹配0个或1个a。这些限定符如下所示: 
  
  
    
      
        X?
      
      
      
        X，一次或一次也没有
      
    
    
    
      
        X*
      
      
      
        X，零次或多次
      
    
    
    
      
        X+
      
      
      
        X，一次或多次
      
    
    
    
      
        X{n}
      
      
      
        X，恰好 n 次
      
    
    
    
      
        X{n,}
      
      
      
        X，至少 n 次
      
    
    
    
      
        X{n,m}
      
      
      
        X，至少 n 次，但是不超过 m 次
      
    
  
  
    但是我们如果要对多个字符进行重复怎么办呢？此时我们就要用到分组，我们可以使用小括号"()"来指定要重复的子表达式，然后对这个子表达式进行重复，例如: (abc)? 表示0个或1个abc 这里一个括号的表达式就表示一个分组。
  
  
    分组可以分为两种形式，捕获组和非捕获组。
  
  
    捕获组
  
  
    捕获组可以通过从左到右计算其开括号来编号。例如，在表达式 ((A)(B(C))) 中，存在四个这样的组: 
  
  
    
      
        <th>
          1
        </th>
        
        
          ((A)(B(C)))
        
      
      
      
        <th>
          2
        </th>
        
        
          /A
        
      
      
      
        <th>
          3
        </th>
        
        
          (B(C))
        
      
      
      
        <th>
          4
        </th>
        
        
          (C)
        
      
    
  
  
    组零始终代表整个表达式
  
  
    之所以这样命名捕获组是因为在匹配中，保存了与这些组匹配的输入序列的每个子序列。捕获的子序列稍后可以通过Back 引用在表达式中使用，也可以在匹配操作完成后从匹配器检索。
  
  
    Back 引用 是说在后面的表达式中我们可以使用组的编号来引用前面的表达式所捕获到的文本序列(是文本不是正则)。
  
  
    例如 ([" ']).* /1   其中使用了分组，/1就是对引号这个分组的引用，它匹配包含在两个引号或者两个单引号中的所有字符串，如，"abc" 或 " ' " 或 ' " '  ，但是请注意，它并不会对" a'或者 'a"匹配。原因上面已经说明，Back引用只是引用文本而不是表达式。
  
  
    非捕获组
  
  
    以 (?) 开头的组是纯的非捕获 组，它不捕获文本，也不针对组合计进行计数。就是说，如果小括号中以?号开头，那么这个分组就不会捕获文本，当然也不会有组的编号，因此也不存在Back 引用。
  
  
    在Java中，支持的非捕获组，有如下几种: 
  
  
    
      
        
      
      
      
        
      
    
    
    
      
         
      
      
      
        
      
    
    
    
      
        
      
      
      
        
      
    
    
    
      
        (?=X)
      
      
      
            X，通过零宽度的正 lookahead
      
    
    
    
      
        (?!X)
      
      
      
            X，通过零宽度的负 lookahead
      
    
    
    
      
        (?<=X)
      
      
      
            X，通过零宽度的正 lookbehind
      
    
    
    
      
        (?<!X)
      
      
      
            X，通过零宽度的负 lookbehind
      
    
    
    
      
        
      
      
      
        
      
    
  
  
    这四个非捕获组用于匹配表达式X，但是不包含表达式的文本。
  
  
    
      
        (?=X )
      
      
      
        零宽度正先行断言。仅当子表达式 X 在 此位置的右侧匹配时才继续匹配。例如，/w+(?=/d) 与后跟数字的单词匹配，而不与该数字匹配。此构造不会回溯。
      
    
    
    
      
        (?!X)
      
      
      
        零宽度负先行断言。仅当子表达式 X 不在 此位置的右侧匹配时才继续匹配。例如，例如，/w+(?!/d) 与后不跟数字的单词匹配，而不与该数字匹配。
      
    
    
    
      
        (?<=X)
      
      
      
        零宽度正后发断言。仅当子表达式 X 在 此位置的左侧匹配时才继续匹配。例如，(?<=19)99 与跟在 19 后面的 99 的实例匹配。此构造不会回溯。
      
    
    
    
      
        (?<!X)
      
      
      
        零宽度负后发断言。仅当子表达式 X 不在此位置的左侧匹配时才继续匹配。例如，(?<!19)99 与不跟在 19 后面的 99 的实例匹配
      
    
  
  
    一般来说要如果是要对一个字符组合采用否定判定时一般都会用上先行断言和后发断言。例如左边不能包含1302和1301的字符串，因为你没法使用某种方式来否定一个1302四个字符的组合(注意: [^ (1302)|(1301)]表示不能是1或者3或者0或者2，而不是1302一个整体)，只有先行或者后发断言可以表示一个整体 : 456(?<!1302|1301)789. 举例: 
  
  
    上面都是理论性的介绍，这里就使用一些例子来说明一下问题: 
  
  
    1、测试匹配性   (?<!4)56(?=9) 这里的含义就是匹配后面的文本56前面不能是4，后面必须是9组成。因此，可以匹配如下文本 5569  ，与4569不匹配。 2 、提取字符串   提取 da12bka3434bdca4343bdca234bm   提取包含在字符a和b之间的数字，但是这个a之前的字符不能是c,b后面的字符必须是d才能提取。 例如这里就只有3434这个数字满足要求。那么我们怎么提取呢？ 首先我们写出提取这个字符串的表达式:  (?<!c)a(/d+)bd  这里就只有一个捕获组(/d+) JAVA代码片段如下:  
    
    
      
        
           Pattern p = Pattern.compile("(?<!c)a(//d+)bd");
        
        
           Matcher m = p.matcher("da12bka3434bdca4343bdca234bm");
        
        
           while(m.find()){
        
        
             System.out.println(m.group(1)); //我们只要捕获组1的数字即可。结果 3434
        
        
             System.out.println(m.group(0)); // 0组是整个表达式，看这里，并没有提炼出(?<!c)的字符 。结果 a3434bd
        
        
           }
        
      
    
    
    
      可以看到，非捕获组，最后是不会返回结果的，因为它本身并不捕获文本。
    
    
    
      正则表达式功能其实非常强大，这里只是对高级用法的简单探讨。有兴趣的朋友和本人共同讨论。
    
    
    
       
    
    
    
      http://blog.csdn.net/lxcnn/article/details/4146148
    
    
    
      http://blog.csdn.net/zhuche110/article/details/2233023
    

 [1]: http://blog.csdn.net/lxcnn/archive/2009/08/03/4402808.aspx
 [2]: http://topic.csdn.net/u/20090803/17/7bb3267c-321d-4d9b-aa34-d157a63e954d.html
 [3]: http://blog.csdn.net/lxcnn/article/details/4146148#
 [4]: http://blog.csdn.net/lovingprince/article/details/2774819
 [5]: http://www.csdn.net