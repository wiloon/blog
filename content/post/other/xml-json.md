---
title: 'XML & JSON'
author: "-"
date: 2012-06-28T15:35:48+00:00
url: /?p=3693
categories:
  - Inbox
tags:
  - reprint
---
## 'XML & JSON'

  
  


  目前，在web开发领域，主要的数据交换格式有XML和JSON，对于XML相信每一个web developer都不会感到陌生；相比之下，JSON可能对于一些新步入开发领域的新手会感到有些陌生，也可能你之前已经听说过，但对于XML和 JSON的不同之处可能会不怎么了解。对于在 Ajax开发中，是选择XML还是JSON，一直存在着争议，个人还是比较倾向于JSON的，虽然JSON才处于起步阶段，但我相信JSON最终会取代XML成为Ajax的首选，到时Ajax可能要更名为Ajaj(Asynchronous JavaScript and JSON)了；

  
    1.数据交换格式比较之关于XML和JSON: 
  
  
    XML: extensible markup language,一种类似于HTML的语言，他没有预先定义的标签，使用DTD(document type definition)文档类型定义来组织数据；格式统一，跨平台和语言，早已成为业界公认的标准。具体的可以问Google或百度。相比之JSON这种轻量级的数据交换格式，XML可以称为重量级的了。
  
  
  
  
    JSON : JavaScript Object Notation 是一种轻量级的数据交换格式。易于人阅读和编写。同时也易于机器解析和生成。它基于JavaScript Programming Language , Standard ECMA-262 3rd Edition - December 1999 的一个子集。 JSON采用完全独立于语言的文本格式，但是也使用了类似于C语言家族的习惯 (包括C, C++, C#, Java, JavaScript, Perl, Python等) 。这些特性使JSON成为理想的数据交换语言。
  
  
    2.数据交换格式比较之关于轻量级和重量级: 
  
  
    轻量级和重量级是相对来说的，那么XML相对于JSON的重量级体现在哪呢？我想应该体现在解析上，XML目前设计了两种解析方式: DOM和SAX；
  
  
    DOM是把一个数据交换格式XML看成一个DOM对象，需要把XML文件整个读入内存，这一点上JSON和XML的原理是一样的，但是XML要考虑父节点和子节点，这一点上JSON的解析难度要小很多，因为JSON构建于两种结构: key/value，键值对的集合；值的有序集合，可理解为数组；
  
  
    SAX不需要整个读入文档就可以对解析出的内容进行处理，是一种逐步解析的方法。程序也可以随时终止解析。这样，一个大的文档就可以逐步的、一点一点的展现出来，所以SAX适合于大规模的解析。这一点，JSON目前是做不到得。
  
  
    所以，JSON和XML的轻/重量级的区别在于: JSON只提供整体解析方案，而这种方法只在解析较少的数据时才能起到良好的效果；而XML提供了对大规模数据的逐步解析方案，这种方案很适合于对大量数据的处理。
  
  
    3.数据交换格式比较之关于数据格式编码及解析的难度: 
  
  
    在编码上，虽然XML和JSON都有各自的编码工具，但是JSON的编码要比XML简单，即使不借助工具，也可以写出JSON代码，但要写出好的XML代码就有点困难；与XML一样，JSON也是基于文本的，且它们都使用Unicode编码，且其与数据交换格式XML一样具有可读性。
  
  
    主观上来看，JSON更为清晰且冗余更少些。JSON网站提供了对JSON语法的严格描述，只是描述较简短。从总体来看，XML比较适合于标记文档，而JSON却更适于进行数据交换处理。
  
  
    在解析上，在普通的web应用领域，开发者经常为XML的解析伤脑筋，无论是服务器端生成或处理XML，还是客户端用 JavaScript 解析XML，都常常导致复杂的代码，极低的开发效率。
  
  
    实际上，对于大多数web应用来说，他们根本不需要复杂的XML来传输数据，XML宣称的扩展性在此就很少具有优势；许多Ajax应用甚至直接返回HTML片段来构建动态web页面。和返回XML并解析它相比，返回HTML片段大大降低了系统的复杂性，但同时缺少了一定的灵活性。同XML或HTML片段相比，数据交换格式JSON 提供了更好的简单性和灵活性。在web serivice应用中，至少就目前来说XML仍有不可动摇的地位
  
