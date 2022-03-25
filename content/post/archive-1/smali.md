---
title: smali
author: "-"
date: 2014-12-30T09:13:47+00:00
url: /?p=7161
categories:
  - Uncategorized

tags:
  - reprint
---
## smali
http://blog.csdn.net/caszhao/article/details/6030425

je或jz //相等则跳 (机器码是74或84) 

jne或jnz //不相等则跳 (机器码是75或85) 

常见的修改就是把对比部分的机器码中74改成75或者84改成85，在反编译的smali文件中，也是类似的。

  相等比较符号在smali中的表示


  
    
      
        符号
      
      
      
        smali语法
      
      
      
        Bao力破解修改
      
    
    
    
      
        ==
      
      
      
        if-eq
      
      
      
        if-eq改成if-ne
      
    
    
    
      
        !=
      
      
      
        if-ne
      
      
      
        if-ne 改成 if-eq
      
    
    
    
      
        equals
      
      
      
        if-eqz
      
      
      
        if-eqz改成 if-nez
      
    
    
    
      
        !equals
      
      
      
        if-nez
      
      
      
        if-nez 改成if-eqz
      
    
  
