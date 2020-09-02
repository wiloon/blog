---
title: wordpress文章标题的优化方法
author: wiloon
type: post
date: 2012-05-23T13:21:29+00:00
url: /?p=3182
categories:
  - Wordpress

---
<http://www.xuguoping.net/wordpress-biaotiyouhua/>

wordpress是业界被公认为最佳的php版优化博客程序。就我个人而言对于seo知识了解并不是很多，但深知文章标题的优化非常的重要。进而，今天我亲自着手修改一下wordpress程序的默认标题，也算是对网站优化的现学现用，理论实战相结合。wordpress文章标题的优化方法主要分两步进行，分别是修改wordpress默认文章标题格式和wordpress默认文章链接地址。
  
    优化wordpress默认文章标题格式。一般情况下wordpress程序的默认标题是：博客网站名称-博客分类归档-博客文章名称。很显然，默认的形式文章标题放在最后面，不利于搜索引擎(尤其是百度)对标题的优化。再加上不同的wordpress主题，模板制作者会使用不同形式的博客文章标题格式，所以我把徐果萍博客的文章标题改为：博客文章标题-博客网站名称。修改方法非常简单，找到现在所使用的博客主题文件夹，然后找到header.php，将原先<title>与</title>之间的代码用下面的代码替换就行了。如果经常换wordpress主题的，也记得及时修改此段代码。
  
  
    <title><?php if ( function_exists('wp_tag_cloud') ) : if (single_tag_title(' ', false)) { echo ' ' ; } endif; ?><?php wp_title(' '); ?><?php if (wp_title(' ', false)) { echo ' – '; } ?><?php bloginfo('name'); ?> </title>
  
