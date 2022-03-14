---
title: 'position,absolute、relative'
author: "-"
date: 2011-09-07T14:35:07+00:00
url: /?p=709
categories:
  - Uncategorized
tags:
  - CSS

---
## 'position,absolute、relative'
position: absolute、relative
  
CSS2.0 HandBook上的解释: 
  
设置此属性值为 absolute 会将对象拖离出正常的文档流绝对定位而不考虑它周围内容的布局。假如其他具有不同 z-index 属性的对象已经占据了给定的位置，他们之间不会相互影响，而会在同一位置层叠。此时对象不具有外补丁( margin )，但仍有内补丁( padding )和边框( border )。
  
要激活对象的绝对(absolute)定位，必须指定 left ， right ， top ， bottom 属性中的至少一个，并且设置此属性值为 absolute 。否则上述属性会使用他们的默认值 auto ，这将导致对象遵从正常的HTML布局规则，在前一个对象之后立即被呈递。

TRBL属性 (TOP、RIGHT、BOTTOM、LEFT) 只有当设定了position属性才有效。
  
当设定position:absolute
  
如果父级 (无限) 没有设定position属性，那么当前的absolute则结合TRBL属性以浏览器左上角为原始点进行定位
  
如果父级 (无限) 设定position属性，那么当前的absolute则结合TRBL属性以父级 (最近) 的左上角为原始点进行定位。

当设定position: relative
  
则参照父级 (最近) 的内容区的左上角为原始点结合TRBL属性进行定位 (或者说相对于被定位元素在父级内容区中的上一个元素进行偏移) ，无父级则以BODY的左上角为原始点。相对定位是不能层叠的。在使用相对定位时，无论元素是否进行移动，元素依然占据原来的空间。因此，移动元素会导致它覆盖其他框。

一般来讲，网页居中的话用Absolute就容易出错，因为网页一直是随着分辨率的大小自动适应的，而Absolute则会以浏览器的左上角为原始点，不会应为分辨率的变化而变化位置。有时还需要依靠z-index来设定容器的上下关系，数值越大越在最上面，数值范围是自然数。当然有一点要注意，父子关系是无法用z-index来设定上下关系的，一定是子级在上父级在下。

设置此属性值为 relative 会保持对象在正常的HTML流中，但是它的位置可以根据它的前一个对象进行偏移。在相对(relative)定位对象之后的文本或对象占有他们自己的空间而不会覆盖被定位对象的自然空间。与此不同的，在绝对(absolute)定位对象之后的文本或对象在被定位对象被拖离正常文档流之前会占有它的自然空间。放置绝对(absolute)定位对象在可视区域之外会导致滚动条出现。而放置相对(relative)定位对象在可视区域之外，滚动条不会出现。其实对于定位的主要问题是要记住每个定位的意义。相对定位是"相对于"元素在文档流中初始位置的，而绝对定位是"相对于"最近的已经定位的祖先元素