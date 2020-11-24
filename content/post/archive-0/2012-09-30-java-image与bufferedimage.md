---
title: Java Image与BufferedImage
author: w1100n
type: post
date: 2012-09-30T05:56:47+00:00
url: /?p=4354
categories:
  - Java

---


<div id="blog_content">
  Image是一个抽象列，BufferedImage是Image的实现。
 Image和BufferedImage的主要作用就是将一副图片加载到内存中。
 Java将一副图片加载到内存中的方法是： 
  
  <div id="">
    
      
        Java代码  <a title="收藏这段代码"><img src="http://javapub.iteye.com/images/icon_star.png" alt="收藏代码" /></a>
      
    
    
    <ol start="1">
      <li>
        String imgPath = "C://demo.jpg";
      </li>
      <li>
        BufferedImage image = ImageIO.read(new FileInputStream(imgPath));
      </li>
    </ol>
  
  
    该方法可以获得图片的详细信息，例如：获得图片的宽度：image.getWidth(null);图片只有加载内存中才能对图片进行进一步的处理。
  
  
    还有一个方法
  
  <div id="">
    
      
        Java代码  <a title="收藏这段代码"><img src="http://javapub.iteye.com/images/icon_star.png" alt="收藏代码" /></a>
      
    
    
    <ol start="1">
      <li>
        String imgPath = "C://demo.jpg";
      </li>
      <li>
        Image imageToolkit.getDefaultToolkit().getImage(imgPath)；
      </li>
    </ol>
  
  
    但该方法不能把图片加载到内存中，仅仅是得到图片，所以也就不能获得图片的信息，图片的长宽信息都无法拿到。
  
  
    文章地址：<a href="http://javapub.iteye.com/blog/683944" target="_blank">http://javapub.iteye.com/blog/683944</a>