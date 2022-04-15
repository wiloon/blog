---
title: java native
author: "-"
date: 2012-09-21T08:37:25+00:00
url: /?p=4163
categories:
  - Java

tags:
  - reprint
---
## java native
Java不是完美的，Java的不足除了体现在运行速度上要比传统的C++慢许多之外，Java无法直接访问到操作系统底层 (如系统硬件等)，为此Java使用native方法来扩展Java程序的功能。

可以将native方法比作Java程序同C程序的接口，其实现步骤: 

１、在Java中声明native()方法，然后编译；

２、用javah产生一个.h文件；

３、写一个.cpp文件实现native导出方法，其中需要包含第二步产生的.h文件 (注意其中又包含了JDK带的jni.h文件) ；

４、将第三步的.cpp文件编译成动态链接库文件；

５、在Java中用System.loadLibrary()方法加载第四步产生的动态链接库文件，这个native()方法就可以在Java中被访问了。

JAVA本地方法适用的情况

1.为了使用底层的主机平台的某个特性，而这个特性不能通过JAVA API访问

2.为了访问一个老的系统或者使用一个已有的库，而这个系统或这个库不是用JAVA编写的

3.为了加快程序的性能，而将一段时间敏感的代码作为本地方法实现。

首先写好JAVA文件

/*

* Created on 2005-12-19 Author shaoqi

*/

package com.hode.hodeframework.modelupdate;

public class CheckFile

{

public native void displayHelloWorld();

static

{

System.loadLibrary("test");

}

public static void main(String[] args) {

new CheckFile().displayHelloWorld();

}

}

然后根据写好的文件编译成CLASS文件

然后在classes或bin之类的class根目录下执行javah -jni com.hode.hodeframework.modelupdate.CheckFile，

就会在根目录下得到一个com_hode_hodeframework_modelupdate_CheckFile.h的文件

然后根据头文件的内容编写com_hode_hodeframework_modelupdate_CheckFile.c文件

#include "CheckFile.h"

#include

#include

JNIEXPORT void JNICALL Java_com_hode_hodeframework_modelupdate_CheckFile_displayHelloWorld(JNIEnv *env, jobject obj)

{

printf("Hello world!n");

return;

}

之后编译生成DLL文件如"test.dll"，名称与System.loadLibrary("test")中的名称一致

vc的编译方法: cl -I%java_home%include -I%java_home%includewin32 -LD com_hode_hodeframework_modelupdate_CheckFile.c -Fetest.dll

最后在运行时加参数-Djava.library.path=[dll存放的路径]