---
title: MessageFormat.format
author: "-"
date: 2016-03-24T10:56:57+00:00
url: /?p=8821
categories:
  - Inbox
tags:
  - reprint
---
## MessageFormat.format

<http://www.cnblogs.com/xiandedanteng/p/3321993.html>

Java里从来少不了字符串拼接的活,Java程序员也肯定用到过StringBuffer,StringBuilder,以及被编译器优化掉的+=。但这些都和下文要谈的无关。

比如有这样的字符串:

张三将去某地点找李四。

其中,张三某地点和李四都是可变的,比如张三变成王五,某地点变成纽约,李四变成赵六。于是整句变成:

王五将去纽约找赵六。

如果直接将张三,某地点和李四用变量替代,再拼接起来,可以达到目的。但是,代码不好写,也不好看,也不好维护。但是,我看过很多SQL拼接,HTML拼接都是这样做的。我自己以前也是这样,自从接触了MessageFormat.format之后才意识到有更好的形式。请看下面的代码:

String[] tdArr=...;
  
String result=MessageFormat.format("{0}{1}{2}{3}", tdArr);

这段代码将把数组tdArr中的四个元素分别插入到{0},{1},{2},{3}的位置。

你看看,是不是这样形式和内容有效的分开了。容易想象,当元素增多时,这种方式优势很明显。

一件事有很多手段来达成,知道那种手段更好,是你经验的体现和专业化的特征。

补记:

如果字符串需要输出单引号',可以用两个单引号"进行转义,下面代码请参考:

public int insertToTest_tb(String createTime,String datefrom,String dateto,String name,String intranetid,String actualhour,String planhour,String status) throws Exception{
  
StringBuilder sb=new StringBuilder();
  
sb.append("    insert into test_tb (");
  
sb.append("        createTime, ");
  
sb.append("        datefrom, ");
  
sb.append("        dateto, ");
  
sb.append("        name, ");
  
sb.append("        intranetid, ");
  
sb.append("        actualhour, ");
  
sb.append("        planhour, ");
  
sb.append("        status");
  
sb.append("    ) values (");
  
sb.append("        "{0}",");
  
sb.append("        "{1}",");
  
sb.append("        "{2}",");
  
sb.append("        "{3}",");
  
sb.append("        "{4}",");
  
sb.append("        "{5}",");
  
sb.append("        "{6}",");
  
sb.append("        "{7}"");
  
sb.append("    )");
  
String result=sb.toString();

Object[] arr={createTime,datefrom,dateto,name,intranetid,actualhour,planhour,status};
  
String sql=MessageFormat.format(result, arr);

return this.getJdbcTemplate().update(sql);
  
}
