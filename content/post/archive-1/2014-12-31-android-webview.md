---
title: android WebView
author: wiloon
type: post
date: 2014-12-31T09:01:10+00:00
url: /?p=7167
categories:
  - Uncategorized

---
浏览器控件是每个开发环境都具备的，这为马甲神功提供了用武之地，windows的有webbrowser，android和ios都有webview。只是其引擎不同，相对于微软的webbrowser，android及ios的webview的引擎都是webkit，对Html5提供支持。本篇主要介绍android的webview之强大。

A.       webview组件如何使用
  
1)             添加权限：AndroidManifest.xml中必须使用许可"android.permission.INTERNET",否则会出Web page not available错误。
  
2)             在要Activity中生成一个WebView组件：WebView webView = new WebView(this);或者可以在activity的layout文件里添加webview控件：
  
<WebView

android:id="@+id/wv"

android:layout\_width="fill\_parent"

android:layout\_height="fill\_parent"

android:text="@string/hello"

/>

3)             设置WebView基本信息：
  
如果访问的页面中有Javascript，则webview必须设置支持Javascript。
  
webview.getSettings().setJavaScriptEnabled(true);
  
触摸焦点起作用
  
requestFocus();
  
取消滚动条
  
this.setScrollBarStyle(SCROLLBARS\_OUTSIDE\_OVERLAY);
  
4)             设置WevView要显示的网页：
  
互联网用：webView.loadUrl("http://www.google.com");
  
本地文件用：webView.loadUrl("file:///android_asset/XX.html");    本地文件存放在：assets文件中
  
5)             如果希望点击链接由自己处理，而不是新开Android的系统browser中响应该链接。给WebView添加一个事件监听对象（WebViewClient)并重写其中的一些方法：
  
shouldOverrideUrlLoading ：对网页中超链接按钮的响应。当按下某个连接时WebViewClient会调用这个方法，并传递参数：按下的url。比如当webview内嵌网页的某个数字被点击时，它会自动认为这是一个电话请求，会传递url：tel:123,如果你不希望如此可通过重写shouldOverrideUrlLoading 函数解决：
  
[java] view plaincopy
  
public boolean shouldOverrideUrlLoading(WebView view,String url){

if(url.indexOf("tel:")<0){//页面上有数字会导致连接电话

view.loadUrl(url);

}

return true;

}
  
另外还有其他一些可重写的方法
  
1，接收到Http请求的事件
  
onReceivedHttpAuthReques t(WebView view, HttpAuthHandler handler, String host, String realm)

2，打开链接前的事件
  
public boolean shouldOverrideUrlLoading (WebView view, String url) { view.loadUrl(url); return true; }

这个函数我们可以做很多操作，比如我们读取到某些特殊的URL，于是就可以不打开地址，取消这个操作，进行预先定义的其他操作，这对一个程序是非常必要的。

3，载入页面完成的事件
  
public void onPageFinished(WebView view, String url){ }

同样道理，我们知道一个页面载入完成，于是我们可以关闭loading条，切换程序动作。

4，载入页面开始的事件
  
public void onPageStarted(WebView view, String url, Bitmap favicon) { }

这个事件就是开始载入页面调用的，通常我们可以在这设定一个loading的页面，告诉用户程序在等待网络响应。

通过这几个事件，我们可以很轻松的控制程序操作，一边用着浏览器显示内容，一边监控着用户操作实现我们需要的各种显示方式，同时可以防止用户产生误操作。
  
6)             如果用webview点链接看了很多页以后，如果不做任何处理，点击系统"Back"键，整个浏览器会调用finish()而结束自身，如果希望浏览的网页回退而不是退出浏览器，需要在当前Activity中处理并消费掉该Back事件。
  
覆盖Activity类的onKeyDown(int keyCoder,KeyEvent event)方法。
  
[java] view plaincopy
  
public boolean onKeyDown(int keyCoder,KeyEvent event){
  
if(webView.canGoBack() && keyCoder == KeyEvent.KEYCODE_BACK){
  
webview.goBack();   //goBack()表示返回webView的上一页面

return true;
  
}
  
return false;
  
}
  
B.       Webview与js交互
  
Webview与js的双向交互才是android的webview强大所在，也是马甲精神能够彻底执行的基础保障。

首先，webview可以定义一个在其内嵌页面中可以触发的事件


[java] view plaincopy
  
wv.addJavascriptInterface(new DemoJavaScriptInterface(), "demo");

rivate final class DemoJavaScriptInterface

{
  
nbsp;DemoJavaScriptInterface(){}

public void clickonAndroid( final String order){
  
mHandler.post(newRunnable(){
  
@Override
  
public void run(){
  
jsonText="{"name":""+order+""}";
  
wv.loadUrl("javascript:wave("+jsonText+")");
  
}
  
});
  
}


通过以上代码，即可实现在其内嵌网页中触发window.demo.clickOnAndroid(str)事件并传参数str给webview。Webview接收到str之后，可以通过以上代码触发其内嵌页面中的js函数wave(str)。这样就可以实现网页触发webview的事件并传参数，webview接收参数并调用js函数。

下面看我的Html脚本：

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN""http://www.w3.org/TR/html4/loose.dtd">

<html>

<head>

<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

<title>Insert title here</title>

<script type="text/javascript" src="jquery.js"></script>

<script>

function toclient()

{

var order=$("#val").val();

window.demo.clickonAndroid(order);


}


function wave(str){

//alert(str.name);

$("#fromclient").text(str.name);

}

</script>

</head>

<body>这是一个html页面

<br/>

输入一个字符串：<br/>

<input id="val" />

<input type="submit" value="点击提交给客户端"

onclick="toclient();"/>

<br />

显示返回：<label id="fromclient"></label>

</body>

</html>


通过脚本看到wave（str）函数是负责将原来传给webview的数据重新拿回页面，效果图如下：
  
另外，如果你想获取页面的一些处理数据并交给webview客户端处理，可在wave函数里将数据alert，然后webview中重写WebChromeClient的onJsAlert函数，具体代码如下

[java] view plaincopy
  
wv.setWebChromeClient(new MyWebChromeClient());

final  class MyWebChromeClient extends WebChromeClient{

@Override

public booleanonJsAlert(WebView view, String url, String message, final JsResult result) {

//message就是wave函数里alert的字符串，这样你就可以在android客户端里对这个数据进行处理

result.confirm();

}

return true;
  
}