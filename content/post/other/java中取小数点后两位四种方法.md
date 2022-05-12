---
title: java中取小数点后两位
author: "-"
date: 2012-05-28T09:41:14+00:00
url: /?p=3279
categories:
  - Java
tags:$
  - reprint
---
## java中取小数点后两位
<http://www.cnblogs.com/sharewind/archive/2007/08/29/873802.html>


  
    
      一
    
    
    
      Long是长整型，怎么有小数，是double吧
 java.text.DecimalFormat   df=new   java.text.DecimalFormat("#.##");
 double   d=3.14159;
 System.out.println(df.format(d));
    
    
    
      二
    
    
    
      java.math.BigDecimal
 BigDecimal   bd   =   new   BigDecimal("3.14159265");
 bd   =   bd.setScale(2,BigDecimal.ROUND_HALF_UP);
    
    
    
      三
    
    
    
      class   Test1{
 public   static   void   main(String[]   args){
 double   ret   =   convert(3.14159);
    
    
    
      System.out.println(ret);
 }
    
    
    
      static   double   convert(double   value){
 long   l1   =   Math.round(value*100);   //四舍五入
 double   ret   =   l1/100.0;               //注意: 使用   100.0   而不是   100
 return   ret;
 }
 }
    
    
    
      四
    
    
    
      double   d   =   13.4324;
 d=((int)(d*100))/100;
    
    
    
      我觉得第二种方法更好．
  
  
  
    你可以通过这个链接引用该篇文章:http://jxcn.bokee.com/tb.b?diaryId=14529336
  
