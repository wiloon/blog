---
title: android activity切换
author: w1100n
type: post
date: 2014-07-28T08:54:45+00:00
url: /?p=6838
categories:
  - Uncategorized

---
http://www.cnblogs.com/leipei2352/archive/2011/08/09/2132096.html

android中每个activity通常描述了一个屏幕上的所有画面(窗口级别的activity除外),因此通常手机屏幕两个界面(准确些说是整个屏幕)之间的切换就涉及到了activity的切换.
  
假定有两个activity,分别是Activity01和Activity02,现在Activity01页面中有一个按钮,点下之后会切换到Activity02.并且在Activity切换时,Activity01给Activity02传递了一个参数. (intent可以在切换Activity时使用,且能传递数据.)

image

怎么做呢?大体思路为:

1.在Activity01中设置一个可触发的空间,并添加一个触发器

2.在Activity01的触发器添加listener

3.在listener的接口实现中,设置一个Intent,让这个Intent能够将Activity01和Activity02绑定起来,并且通过putExtra将要传输的值放到Intent对象中存储

3.listener接口实现结尾,通过Activity01启动调用这个Intent对象,通过调用来切换到Activity02

4.在Activity02中,使用getIntent来获取上下文切换中使得自己启动了的那个Intent对象实例

5.通过获取到的intent对象实例,使用起getStringExtra来获取先前putExtra的值.

当然,后面如果对Intent更加了解时,就需要按实际情况挑选更合适的存储数据及获取数据的函数了.

以下是实现的演示:

imageimage

最后附上关键部分代码:

Activity01中:

button.setOnClickListener(new Button.OnClickListener() { //更准确点应该是View.OnClickListener
  
public void onClick(View v)
  
{
  
/\* 新建一个Intent对象 \*/
  
Intent intent = new Intent();
  
intent.putExtra("name","LeiPei");
  
/\* 指定intent要启动的类 \*/
  
intent.setClass(Activity01.this, Activity02.class);
  
/\* 启动一个新的Activity \*/
  
Activity01.this.startActivity(intent);
  
/\* 关闭当前的Activity \*/
  
Activity01.this.finish();
  
}
  
});
  
Activity02中:

String name=intent.getStringExtra("name");
  
textview2.setText("activity01传过来的值为:"+name);