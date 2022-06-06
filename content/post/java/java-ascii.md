---
title: "java 替换 ascii 不可见字符, StringEscapeUtils.escapeJava"
author: "-"
date: ""
url: "escape"
categories:
  - Java
tags:
  - inbox
---
## "java 替换ascii不可见字符, StringEscapeUtils.escapeJava"

### StringEscapeUtils.escapeJava

```java
   StringEscapeUtils.escapeJava
```

### String.replaceAll 替换成?

```java
    my_string.replaceAll("\\p{C}", "?");
```

 <https://stackoverflow.com/questions/6198986/how-can-i-replace-non-printable-unicode-characters-in-java>

### StringEscapeUtils

 在java.commons.lang3的包中有许多方便好用的工具类，类似于处理字符串的StringUtils，处理日期的DateUtils等等，StringEscapeUtils也是其中的一员。

StringEscapeUtils是在java.commons.lang3的2.0版本中加入的工具类，在3.6版本中被标注为@deprecated，表明在之后的版本中则为过时状态，之后StringEscapeUtils类被移到java.commons.text包下。

1. 功能用途
StringEscapeUtils的主要功能就是为Java，Java Script，Html，XML进行转义与反转义。

escapeJava(String input) / unescapeJava(String unionCodeString)
将输入字符串转为unicode编码 / 将unicode字符串转为Utf-8格式的字符串
escapeHtml4(String input) / unescapeHtml4(String input)
转义/反转义html脚本
escapeEcmaScript(String input) / unescapeEcmaScript(String input)
转义/反转义js脚本
escapeXml(String input) / unescapeXml(String input)
转义/反转义xml脚本
除了列出的几个较常用的方法，还有escapeJson(String input) / unescapeJson(String input)、escapeCsv(String input) / unescapeCsv(String input)等等，可以看一下下面的执行例子，有个直观的认识。

```java
import org.apache.commons.text.StringEscapeUtils;
import org.junit.Test;

/**
 * @author liuqian
 * @date 2018/4/3 16:27
 */
public class EscapeTest {

  @Test
  public void escapeTest() {
    System.out.println("转义/反转义Java字符串");
    String javaString = "这是Java字符串";
    System.out.println(StringEscapeUtils.escapeJava(javaString));
    System.out.println(StringEscapeUtils.unescapeJava(StringEscapeUtils.escapeJava(javaString)));
    System.out.println("-------------------------------------------------------------");
    System.out.println("转义/反转义Json字符串");
    String jsonString = "{\"keyword\": \"这是Json字符串\"}";
    System.out.println(StringEscapeUtils.escapeJson(jsonString));
    System.out.println(StringEscapeUtils.unescapeJson(StringEscapeUtils.escapeJson(jsonString)));
    System.out.println("-------------------------------------------------------------");
    //除了html4还有html3等格式
    System.out.println("转义/反转义Html字符串");
    String htmlString = "加粗字符";
    System.out.println(StringEscapeUtils.escapeHtml4(htmlString));
    System.out.println(StringEscapeUtils.unescapeHtml4(StringEscapeUtils.escapeHtml4(htmlString)));
    System.out.println("-------------------------------------------------------------");
    //除了xml10还有xml11等格式
    System.out.println("转义/反转义xml字符串");
    String xmlString = "<xml>\"xml字符串\"</xml>";
    System.out.println(StringEscapeUtils.escapeXml10(xmlString));
    System.out.println(StringEscapeUtils.unescapeXml(StringEscapeUtils.escapeXml10(xmlString)));
    System.out.println("-------------------------------------------------------------");
    System.out.println("转义/反转义csv字符串");
    String csvString = "1997,Ford,E350,\"Super, luxurious truck\"";
    System.out.println(StringEscapeUtils.escapeCsv(csvString));
    System.out.println(StringEscapeUtils.unescapeCsv(StringEscapeUtils.escapeCsv(csvString)));
    System.out.println("-------------------------------------------------------------");
    System.out.println("转义/反转义Java Script字符串");
    String jsString = "<script>alert('1111')</script>";
    System.out.println(StringEscapeUtils.escapeEcmaScript(jsString));
   System.out.println(StringEscapeUtils.unescapeEcmaScript(StringEscapeUtils.escapeEcmaScript(jsString)));
  }
}
```

### 结果

```java
转义/反转义Java字符串
\u8FD9\u662FJava\u5B57\u7B26\u4E32
这是Java字符串
-------------------------------------------------------------
转义/反转义Json字符串
{\"keyword\": \"\u8FD9\u662FJson\u5B57\u7B26\u4E32\"}
{\"keyword\": \"这是Json字符串\"}
-------------------------------------------------------------
转义/反转义Html字符串
<strong>加粗字符</strong>
加粗字符
-------------------------------------------------------------
转义/反转义xml字符串
<xml>&quot;xml字符串&quot;</xml>
<xml>"xml字符串"</xml>
-------------------------------------------------------------
转义/反转义csv字符串
"1997,Ford,E350,""Super, luxurious truck"""
1997,Ford,E350,"Super, luxurious truck"
-------------------------------------------------------------
转义/反转义Java Script字符串
<script>alert(\'1111\')<\/script>
<script>alert('1111')</script>
```

<https://github.com/lq920320/blogs/issues/9>
