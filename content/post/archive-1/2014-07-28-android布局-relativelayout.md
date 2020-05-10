---
title: Android布局 RelativeLayout
author: wiloon
type: post
date: 2014-07-28T08:53:54+00:00
url: /?p=6836
categories:
  - Uncategorized

---
http://blog.csdn.net/johnny901114/article/details/7865617

Android布局一_RelativeLayout
  
分类： Android 2012-08-14 17:59 2875人阅读 评论(0) 收藏 举报
  
我们知道布局是Android开发中非常重要的一部分,还记得刚进公司的时候,布局界面的功底非常差,做出的界面非常山寨,更不要说什么布局效率的问题了.如果UI做得不好用户的体验是非常差的.自然就不会有很多的用户愿意用你的产品.
  
Android布局大致可以分为5类:
  
RelativeLayout,
  
LinearLayout,
  
FrameLayout,
  
TableLayout,
  
AbsoluteLayout.
  
所以把自己的积累的点滴记录下来.首先从相对布局(RelativeLayout)开始.

RelativeLayout子控件的一些属性:
  
//相对于同级控件对齐方式
  
android:layout_alignBaseline将该控件的baseline与给定ID的baseline对齐;
  
android:layout_alignTop 将该控件的顶部边缘与给定ID的顶部边缘对齐;
  
android:layout_alignBottom将该控件的底部边缘与给定ID的底部边缘对齐;
  
android:layout_alignLeft 将该控件的左边缘与给定ID的左边缘对齐;
  
android:layout_alignRight 将该控件的右边缘与给定ID的右边缘对齐;
  
// 相对于父组件对齐方式
  
android:layout_alignParentTop 如果为true,将该控件的顶部与其父控件的顶部对齐;
  
android:layout_alignParentBottom 如果为true,将该控件的底部与其父控件的底部对齐;
  
android:layout_alignParentLeft 如果为true,将该控件的左部与其父控件的左部对齐;
  
android:layout_alignParentRight 如果为true,将该控件的右部与其父控件的右部对齐;
  
// 居中
  
android:layout_centerHorizontal 如果为true,将该控件的置于水平居中;
  
android:layout_centerVertical 如果为true,将该控件的置于垂直居中;
  
android:layout_centerInParent 如果为true,将该控件的置于父控件的中央;
  
// 控件离上下左右的像素距离
  
android:layout_marginTop 上偏移的值;
  
android:layout_marginBottom 下偏移的值;
  
android:layout_marginLeft 左偏移的值;
  
android:layout_marginRight 右偏移的值;
  
//控件相对同级控件的位置
  
android:layout_toLeftOf在ID控件的左边
  
android:layout_toRightOf在ID控件的右边
  
android:layout_below在ID控件的下边
  
android:layout_above在ID控件的上边