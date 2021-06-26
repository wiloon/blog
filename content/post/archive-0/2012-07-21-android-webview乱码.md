---
title: Android WebView乱码
author: "-"
type: post
date: 2012-07-21T05:15:44+00:00
url: /?p=3870
categories:
  - Uncategorized

---
### 

<div id="article_content">
   1.网页说明编码格式 <meta http-equiv="Content-Type" content="text/html;charset=gb2312"> 
  
  <p dir="ltr">
     2.设置WebView编码
      httpview.getSettings().setDefaultTextEncodingName("gbk");
 注意为gb2312或gbk
  
  <p dir="ltr">
    以上两种方法是网上给的比较好的方法，但是我都试了下都没有解决我的乱码问题。
  
  <p dir="ltr">
    原来我是用LoadData方法来解析html的，但是据说这是官方的一个BUG，不能用来解析中文。所以绕其道而行之，采用loadDataWithBaseURL的方法，其中codeingType设置为utf-8就OK了。
  
