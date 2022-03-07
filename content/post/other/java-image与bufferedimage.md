---
title: Java Image与BufferedImage
author: "-"
date: 2012-09-30T05:56:47+00:00
url: /?p=4354
categories:
  - Java

tags:
  - reprint
---
## Java Image 与 BufferedImage

Image是一个抽象类，BufferedImage是Image的实现。Image和BufferedImage的主要作用就是将一副图片加载到内存中。

Java将一副图片加载到内存中的方法是:  

String imgPath = "C://demo.jpg";
      
      
        BufferedImage image = ImageIO.read(new FileInputStream(imgPath));
      
    
  
  
    该方法可以获得图片的详细信息，例如: 获得图片的宽度: image.getWidth(null);图片只有加载内存中才能对图片进行进一步的处理。
  
  
    还有一个方法
    
    
      
        String imgPath = "C://demo.jpg";
      
      
        Image imageToolkit.getDefaultToolkit().getImage(imgPath)；
      
    
  
  
    但该方法不能把图片加载到内存中，仅仅是得到图片，所以也就不能获得图片的信息，图片的长宽信息都无法拿到。
  
  
    文章地址: http://javapub.iteye.com/blog/683944