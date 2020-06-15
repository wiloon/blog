---
title: MessageFormat.format
author: wiloon
type: post
date: 2016-03-24T10:56:57+00:00
url: /?p=8821
categories:
  - Uncategorized

---
http://www.cnblogs.com/xiandedanteng/p/3321993.html

Java里从来少不了字符串拼接的活，Java程序员也肯定用到过StringBuffer，StringBuilder，以及被编译器优化掉的+=。但这些都和下文要谈的无关。

比如有这样的字符串：

张三将去某地点找李四。

其中，张三某地点和李四都是可变的，比如张三变成王五，某地点变成纽约，李四变成赵六。于是整句变成：

王五将去纽约找赵六。

如果直接将张三，某地点和李四用变量替代，再拼接起来，可以达到目的。但是，代码不好写，也不好看，也不好维护。但是，我看过很多SQL拼接，HTML拼接都是这样做的。我自己以前也是这样，自从接触了MessageFormat.format之后才意识到有更好的形式。请看下面的代码：

String[] tdArr=&#8230;;
  
String result=MessageFormat.format("<tr bgcolor=&#8217;#cef&#8217;><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>&#8221;, tdArr);

这段代码将把数组tdArr中的四个元素分别插入到{0}，{1}，{2}，{3}的位置。

你看看，是不是这样形式和内容有效的分开了。容易想象，当元素增多时，这种方式优势很明显。

一件事有很多手段来达成，知道那种手段更好，是你经验的体现和专业化的特征。

补记：

如果字符串需要输出单引号&#8217;,可以用两个单引号&#8221;进行转义，下面代码请参考：

public int insertToTest_tb(String createTime,String datefrom,String dateto,String name,String intranetid,String actualhour,String planhour,String status) throws Exception{
  
StringBuilder sb=new StringBuilder();
  
sb.append(&#8221;    insert into test_tb (");
  
sb.append(&#8221;        createTime, ");
  
sb.append(&#8221;        datefrom, ");
  
sb.append(&#8221;        dateto, ");
  
sb.append(&#8221;        name, ");
  
sb.append(&#8221;        intranetid, ");
  
sb.append(&#8221;        actualhour, ");
  
sb.append(&#8221;        planhour, ");
  
sb.append(&#8221;        status&#8221;);
  
sb.append(&#8221;    ) values (");
  
sb.append(&#8221;        &#8221;{0}&#8221;,&#8221;);
  
sb.append(&#8221;        &#8221;{1}&#8221;,&#8221;);
  
sb.append(&#8221;        &#8221;{2}&#8221;,&#8221;);
  
sb.append(&#8221;        &#8221;{3}&#8221;,&#8221;);
  
sb.append(&#8221;        &#8221;{4}&#8221;,&#8221;);
  
sb.append(&#8221;        &#8221;{5}&#8221;,&#8221;);
  
sb.append(&#8221;        &#8221;{6}&#8221;,&#8221;);
  
sb.append(&#8221;        &#8221;{7}&#8221;&#8221;);
  
sb.append(&#8221;    )&#8221;);
  
String result=sb.toString();

Object[] arr={createTime,datefrom,dateto,name,intranetid,actualhour,planhour,status};
  
String sql=MessageFormat.format(result, arr);

return this.getJdbcTemplate().update(sql);
  
}

