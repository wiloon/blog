---
title: startActivityForResult()
author: "-"
date: 2014-08-26T03:29:14+00:00
url: /?p=6964
categories:
  - Inbox
tags:
  - reprint
---
## startActivityForResult()
举例说我想要做的一个事情是,在一个主界面(主Activity)上能连接往许多不同子功能模块(子Activity上去),当子模块的事情做完之后就回到主界面,或许还同时返回一些子模块完成的数据交给主Activity处理。

---

目的:  A.java 是主界面,B.java 是子功能模块,要从A启动B,B干完活之后把结果汇报给A
  
先看 A.java 的相关代码
  
//- A.java -//
  
/*
  
* 要做两件事情,第一是用 startActivityForResult() 启动B,其次是回收B的结果
  
*/
  
//启动B
  
Intent bintent = new Intent(A.this, B.class);
  
//设置 bintent的Bundle的一个值
  
String bsay = "Hello, this is B speaking";
  
bintent.putExtra("listenB", bsay)
  
startActivityForResult(bintent,0); // 参数(Intent intent, Int requestCode) 的 requestCode 对应下面回收Bundle时识别用的
  
//重写onActivityResult()来处理返回的数据,建议先看B.java 的代码再回来看这里比较好理解
  
//这理有三个参数 requestCode, resultCode, data
  
protected void onActivityResult(int requestCode, int resultCode, Intent data) {
  
switch (resultCode) { //resultCode为回传的标记,我在B中回传的是RESULT_OK
  
case RESULT_OK:
  
Bundle b=data.getExtras(); //data为B中回传的Intent
  
String str=b.getString("ListenB");//str即为回传的值"Hello, this is B speaking"
  
/* 得到B回传的数据后做什么... 略 */
  
break;
  
default:
  
break;
  
}
  
}
  
-----------------------------
  
//- B.java -//
  
// 用 setResut() 准备好要回传的数据后,只要使用finish()的方法就能把打包好的数据发给A且运行onActivityResult()部分的代码
  
Intent aintent = new Intent(B.this, A.class);
  
/* 将数据打包到aintent Bundle 的过程略 */
  
setResut(RESULT_OK,aintent); //这理有2个参数(int resultCode, Intent intent)
  
... ...
  
finish();
  
-----------------------------
  
OK,代码如上,可能这个时候还会有点疑问,关于参数的疑问。直接看android sdk 帮助说得更清楚。我发现网上有些文章还有吧 requestCode 和 resultCode 混淆说明错的。
  
startActivityForResult(Intent intent, Int requestCode)
  
intent 传给B的,不解释,看不懂你还是玩玩手机算了,别想开发的事情了
  
requestCode >=0就好,随便用于在onActivityResult()区别哪个子模块回传的数据,如果还有C.java ,D甚至E子模块的话,每个区分开不同的requestCode就好。
  
setResut(int resultCode, Intent intent)
  
resultCode 如果B子模块可能有几种不同的结果返回,可以用这个参数予以识别区分。这里还有个特殊的 RESULT_OK 值,没有特殊情况用它就好了,sdk有说明的,呵。
  
intent 继续不解释,传回给A的onActivityResult()
  
onActivityResult(int requestCode, int resultCode, Intent intent)
  
这里三个都不用解释了,与上文对应的东西。如果不对requestCode和resultCode 加以识别区分的话,只要有其他activity setResult到了A onActivityResult()会无差别处理。