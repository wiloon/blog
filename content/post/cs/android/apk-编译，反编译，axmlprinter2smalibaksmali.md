---
title: apk 编译,反编译,AXMLPrinter2,smali,baksmali
author: "-"
date: 2014-04-14T08:07:13+00:00
url: /?p=6549
categories:
  - Inbox
tags:
  - reprint
---
## apk 编译,反编译,AXMLPrinter2,smali,baksmali

[http://blog.csdn.net/android_tutor/article/details/5724435](http://blog.csdn.net/android_tutor/article/details/5724435)

1.AXMLPrinter2.jar

2.baksmali.jar

3.smali.jar

三、准备工作

为了方便起见,作者把AXMLPrinter2.jar, 还有baksmali.jar,还有smali.jar(下下来为了方便重命名),放在Android SDK tools文件夹中如下图所示:

为了便于大家更容易程序比对,作者写了一个简单的应用(叫APKInstaller)目录结构如下图所示:

四、开始拿来主义

1.用 AXMLPrinter2.jar查看apk中的布局xml文件:

将ApkInstaller应用生成的ApkInstaller.apk(为了方便起见放到tools目录里)用WinRAR等 工具打开,将res/layout/main.xml解压出来(也还是放在tools目录里哦)

打开main.xml文件,内容如下(一堆天文):

这时候AXMLPrinter2.jar派上用场了,打开cmd终端,一直进入到tools目录下,输入如下命令:

java -jar AXMLPrinter2.jar main.xml > main.txt. (如下图所示)

打开main.txt代码如下(是不是有个123了呵呵~):

<?xml version="1.0" encoding="utf-8"?>

<WebView android:id="@7F050000" android:layout_width="-1" android:layout_height="-2" >

</WebView>

</LinearLayout>

为了比对打开源程序中的main.xml代码如下(大家比对一下吧):

<?xml version="1.0" encoding="utf-8"?>

<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"

android:orientation="vertical"

android:layout_width="fill_parent"

android:layout_height="fill_parent"

<WebView

android:id="@+id/apk_web"

android:layout_height="wrap_content"

android:layout_width="fill_parent"

/>

</LinearLayout>

2.用baksmali.jar反编译classes.dex:

将ApkInstaller.apk里的classes.dex解压到tools目录里,然后baksmali.jar就派上用场了,在cmd命令行里输入如下命令:

java -jar baksmali.jar -o classout/ classes.dex .(如下图所示:)

你将会发现在tools里多一个classout文件夹里面(我代码的包目录结构清晰可见呀),如下图所示:

从上面看出除了Android本身资源的类R开头的,我的源程序里只有一个ApkInstaller.java,完全吻合,真TMD的猥琐呵呵~

下面我们看一下ApkInstaller.smali内容是什么,如以下代码:

.class public Lcom/tutor/apkinstaller/ApkInstaller;

.super Landroid/app/Activity;

.source "ApkInstaller.java"

# instance fields

.field private apkWeb:Landroid/webkit/WebView;

# direct methods

.method public constructor <init>()V

.registers 1

.prologue

.line 8

invoke-direct {p0}, Landroid/app/Activity;-><init>()V

return-void

.end method

# virtual methods

.method public onCreate(Landroid/os/Bundle;)V

.registers 5

.parameter "savedInstanceState"

.prologue

.line 13

invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V

.line 14

const/high16 v2, 0x7f03

invoke-virtual {p0, v2}, Lcom/tutor/apkinstaller/ApkInstaller;->setContentView(I)V

.line 15

const/high16 v2, 0x7f05

invoke-virtual {p0, v2}, Lcom/tutor/apkinstaller/ApkInstaller;->findViewById(I)Landroid/view/View;

move-result-object v2

check-cast v2, Landroid/webkit/WebView;

iput-object v2, p0, Lcom/tutor/apkinstaller/ApkInstaller;->apkWeb:Landroid/webkit/WebView;

.line 16

iget-object v2, p0, Lcom/tutor/apkinstaller/ApkInstaller;->apkWeb:Landroid/webkit/WebView;

invoke-virtual {v2}, Landroid/webkit/WebView;->getSettings()Landroid/webkit/WebSettings;

move-result-object v1

.line 17

.local v1, webSettings:Landroid/webkit/WebSettings;

const/4 v2, 0x1

invoke-virtual {v1, v2}, Landroid/webkit/WebSettings;->setJavaScriptEnabled(Z)V

.line 19

const-string v0, "http://frankiewei.net/apk/demos/main/index.html#home"

.line 20

.local v0, apkUrl:Ljava/lang/String;

iget-object v2, p0, Lcom/tutor/apkinstaller/ApkInstaller;->apkWeb:Landroid/webkit/WebView;

invoke-virtual {v2, v0}, Landroid/webkit/WebView;->loadUrl(Ljava/lang/String;)V

.line 21

return-void

.end method

同样为了比对我们看一下ApkInstaller.java的源代码如下:

package com.tutor.apkinstaller;

import android.app.Activity;

import android.os.Bundle;

import android.webkit.WebSettings;

import android.webkit.WebView;

public class ApkInstaller extends Activity {

private WebView apkWeb;

@Override

public void onCreate(Bundle savedInstanceState) {

super.onCreate(savedInstanceState);

setContentView(R.layout.main);

apkWeb = (WebView)findViewById(R.id.apk_web);

WebSettings webSettings = apkWeb.getSettings();

webSettings.setJavaScriptEnabled(true);

String apkUrl = "http://frankiewei.net/apk/demos/main/index.html#home";

apkWeb.loadUrl(apkUrl);

}

}

我相信大家 已经能看出来门道来了吧,hoho~

3.用smali.jar编译classout成classes.dex:

我们上一步已经将classes.dex反编译成了.smali文件,好了,我们看看smali文件看够了,在偿试把它编译成classes.dex吧,

输入如下命令:java -jar smali.jar classout/ -o classes.dex. 如下图所示:

我们可以将新生成的classes.dex塞入ApkInstaller.apk里覆盖原来的classes.dex文件,这样我们的apk还是一样能用的哦~
