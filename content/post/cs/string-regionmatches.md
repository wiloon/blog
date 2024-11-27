---
title: String.regionMatches
author: "-"
date: 2016-03-25T03:53:24+00:00
url: /?p=8826
categories:
  - Inbox
tags:
  - reprint
---
## String.regionMatches
题目: 输入两个字符串,计算两个字符串的最大公共字串的长度,并输出,字符不区分大小写

eg: 输入abcde  xxxBcyyy,输出 2。


完整Java代码: 
  
import java.util.*;
  
public class Main {
  
public static void main(String arg[]){
  
Scanner s=new Scanner(System.in);
  
String str1=s.next();
  
String str2=s.next();
  
s.close();
  
String maxStr,minStr;
  
if(str1.length()>str2.length()){
  
maxStr=str1; minStr=str2;
  
}
  
else{
  
maxStr=str2; minStr=str1;
  
}
  
int max=maxStr.length();
  
int min=minStr.length();//System.out.println(maxStr+" "+minStr+" "+max+" "+min);
  
int result=0;
  
OK:
  
for(int l=min;l>0;l-){
  
for(int i=0;i<=max-l;i++){
  
for(int j=0;j<=min-l;j++){
  
if(maxStr.regionMatches(true, i, minStr, j, l)){
  
result=l;//System.out.println(l+" "+i+" "+j);
  
break OK;
  
}
  
}
  
}
  
}
  
System.out.println(result);
  
}

}

学习点一: 利用Java标签跳出多重循环；

学习点二: 灵活使用String.regionMatches方法,来判断两个字符串的子串区域是否相等,具体可参考Java API文档如下。


regionMatches
  
public boolean regionMatches(boolean ignoreCase,
  
int toffset,
  
String other,
  
int ooffset,
  
int len)
  
测试两个字符串区域是否相等。将此 String 对象的子字符串与参数 other 的子字符串进行比较。如果这两个子字符串表示相同的字符序列,则结果为 true,当且仅当 ignoreCase 为 true 时忽略大小写。要比较的此String 对象的子字符串从索引 toffset 处开始,长度为 len。要比较的 other 的子字符串从索引 ooffset 处开始,长度为 len。当且仅当下列至少一项为 true 时,结果才为 false: 

toffset 为负。
  
ooffset 为负。
  
toffset+len 大于此 String 对象的长度。
  
ooffset+len 大于另一个参数的长度。
  
ignoreCase 为 false,且存在某个小于 len 的非负整数 k,即:  this.charAt(toffset+k) != other.charAt(ooffset+k)

ignoreCase 为 true,且存在某个小于 len 的非负整数 k,即:  Character.toLowerCase(this.charAt(toffset+k)) !=
  
Character.toLowerCase(other.charAt(ooffset+k))

以及:  Character.toUpperCase(this.charAt(toffset+k)) !=
  
Character.toUpperCase(other.charAt(ooffset+k))
  
参数: 
  
ignoreCase - 如果为 true,则比较字符时忽略大小写。
  
toffset - 此字符串中子区域的起始偏移量。
  
other - 字符串参数。
  
toffset - 字符串参数中子区域的起始偏移量。
  
len - 要比较的字符数。
  
返回: 
  
如果此字符串的指定子区域匹配字符串参数的指定子区域,则返回 true；否则返回 false。是否完全匹配或考虑大小写取决于 ignoreCase 参数。