---
title: OCR之 Tesseract
author: "-"
date: 2012-09-30T08:25:13+00:00
url: /?p=4358
categories:
  - Java

tags:
  - reprint
---
## OCR之 Tesseract
>http://www.cnblogs.com/brooks-dotnet/archive/2010/10/05/1844203.html

光学字符识别(OCR,Optical Character Recognition)是指对文本资料进行扫描，然后对图像文件进行分析处理，获取文字及版面信息的过程。OCR技术非常专业，一般多是印刷、打印行业的从业人员使用，可以快速的将纸质资料转换为电子资料。关于中文OCR，目前国内水平较高的有清华文通、汉王、尚书，其产品各有千秋，价格不菲。国外OCR发展较早，像一些大公司，如IBM、微软、HP等，即使没有推出单独的OCR产品，但是他们的研发团队早已掌握核心技术，将OCR功能植入了自身的软件系统。对于我们程序员来说，一般用不到那么高级的，主要在开发中能够集成基本的OCR功能就可以了。这两天我查找了很多免费OCR软件、类库，特地整理一下，今天首先来谈谈Tesseract，下一次将讨论下Onenote 2010中的OCR API实现。可以在这里查看OCR技术的发展简史。
    
    
    
      测试代码下载
    
    
    
      转载请注明出处: http://www.cnblogs.com/brooks-dotnet/archive/2010/10/05/1844203.html
    
    
    
      1、Tesseract概述
    
    
    
      Tesseract的OCR引擎最先由HP实验室于1985年开始研发，至1995年时已经成为OCR业内最准确的三款识别引擎之一。然而，HP不久便决定放弃OCR业务，Tesseract也从此尘封。
    
    
    
      数年以后，HP意识到，与其将Tesseract束之高阁，不如贡献给开源软件业，让其重焕新生－－2005年，Tesseract由美国内华达州信息技术研究所获得，并求诸于Google对Tesseract进行改进、消除Bug、优化工作。
    
    
    
      Tesseract目前已作为开源项目发布在Google Project，其项目主页在这里查看，其最新版本3.0已经支持中文OCR，并提供了一个命令行工具。本次我们来测试一下Tesseract 3.0，由于命令行对最终用户不太友好，我用WPF简单封装了一下，就可以方便的进行中文OCR了。
  
