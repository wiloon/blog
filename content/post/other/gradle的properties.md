---
title: Gradle的Properties
author: "-"
date: 2014-12-03T02:27:29+00:00
url: /?p=7081
categories:
  - Inbox
tags:
  - Gradle

---
## Gradle的Properties
http://hugozhu.myalert.info/2014/07/23/47-use-gradle-properties-to-set-alternative-android-build-tools.html

# 目录: <nav> 

  * [问题背景][1]
  * [解决方案][2] 
      * [修改build.gradle使用变量设置版本号][3]
      * [在setting.gradle中设置缺省的版本][4]
      * [在gradle.properties文件中重载版本号][5]
      * [命令行使用][6]
  * [参考链接][7]</nav> 

# 问题背景 {#toc_0}

团队一起在开发一个Android项目,工程师有的使用Eclipse,有个使用Intellij IDEA,有的使用Android Studio。每个人安装的Android SDK build-tools可能都不一样,有的是19.0.3,有的是19.1.0,不同版本的build-tools对Gradle Plugin也有相应的要求,如19.0.3对应的是com.android.tools.build:gradle:0.10.+,19.1.0对应的是com.android.tools.build:gradle:0.12.+,下面是一个典型的build.gradle配置文件。


  
    buildscript {
  
  
     repositories {
  
  
     mavenCentral()
  
  
     }
  
  
    
  
  
     dependencies {
  
  
     classpath 'com.android.tools.build:gradle:0.10.+'
  
  
     }
  
  
    }
  
  
    
  
  
    apply plugin: 'android-library'
  
  
    
  
  
    android {
  
  
     compileSdkVersion 19
  
  
     buildToolsVersion 19.0.3
  
  
    
  
  
     defaultConfig {
  
  
     minSdkVersion 8
  
  
     targetSdkVersion 19
  
  
     }
  
  
    }
  


在合作开发中遇到的一个尴尬的问题是,IDEA最新版还不能很好的支持Gradle Plugin 0.12+,而Android Studio最新版则要求使用0.12+。大家又共用一个Git仓库。可能的解决方案是,从Git checkout出来的项目需要有一个基础的版本号,但是开发者可以在本地通过一处文件 (不check in到git) 来重载版本号。

# 解决方案 {#toc_1}

Gradle支持三种Properties, 这三种Properties的作用域和初始化阶段都不一样,下面分别列出了其部分特点。:

  1. _System Properties: _ 
      1. 可通过gradle.properties文件,环境变量或命令行-D参数设置 2. 可在setting.gradle或build.gradle中动态修改,在setting.gradle中的修改对buildscript block可见；
      2. 所有工程可见,不建议在build.gradle中修改
      3. 多子工程项目中,子工程的gradle.properties会被忽略掉,只有root工程的gradle.properties有效；
  2. _Project Properties: _ 
      1. 可通过gradle.properties文件,环境变量或命令行-P参数设置,优先级是:
      2. 可在build.gradle中动态修改,但引用不存在的project properties会立即抛错
      3. 动态修改过的project properties在buildscript block中不可见
  3. _Project ext properties: _ 
      1. 可在项目的build.gradle中声明和使用,本工程和子工程可见
      2. 不能在setting.gradle中访问

如果有多处设置,加载次序如下 (注意: gradle 2.0是这样的, 1.10~1.12有bug) , 后面的覆盖前面的设置

  1. from gradle.properties located in project build dir.
  2. from gradle.properties located in gradle user home.
  3. from system properties, e.g. when -Dsome.property is used in the command line.
  4. setting.gradle
  5. build.gradle

根据其特点,这里给出一个使用System Properties来解决问题的方案。

## 修改build.gradle使用变量设置版本号 {#toc_2}


  
    buildscript {
  
  
     repositories {
  
  
     mavenCentral()
  
  
     }
  
  
    
  
  
     dependencies {
  
  
     classpath 'com.android.tools.build:gradle:'+System.properties['androidGradlePluginVersion']
  
  
     }
  
  
    }
  
  
    
  
  
    apply plugin: 'android-library'
  
  
    
  
  
    android {
  
  
     compileSdkVersion 19
  
  
     buildToolsVersion System.properties['buildToolsVersion']
  
  
    
  
  
     defaultConfig {
  
  
     minSdkVersion 8
  
  
     targetSdkVersion 19
  
  
     }
  
  
    }
  


## 在setting.gradle中设置缺省的版本 {#toc_3}


  
    
  
  
    //override your build tools version in project gradle.properties or ~/.gradle/gradle.properties
  
  
    
  
  
    if (!System.properties['buildToolsVersion']) {
  
  
     System.properties['buildToolsVersion'] = "19.0.3"
  
  
    }
  
  
    
  
  
    if (!System.properties['androidGradlePluginVersion']) {
  
  
     System.properties['androidGradlePluginVersion'] = "0.10.+"
  
  
    }
  
  
    
  


## 在gradle.properties文件中重载版本号 {#toc_4}

gradle.properties文件内容如下: 


  
    systemProp.buildToolsVersion=19.1.0
  
  
    systemProp.androidGradlePluginVersion=0.12.+
  
  
    
  


gradle.properties文件可以放在root project根目录下,也可以放在用户目录下 ~/.gradle/gradle.properties,后者的优先级更高。

## 命令行使用 {#toc_5}

还可以在命令行中设置参数

`./gradlew build -DbuildToolsVersion=19.1.0 -DandroidGradlePluginVersion=0.12.+ -x lint`

# 参考链接 {#toc_6}

  1. <http://www.gradle.org/docs/current/dsl/>
  2. [http://www.gradle.org/docs/current/userguide/tutorial_this_and_that.html][8]

 [1]: http://hugozhu.myalert.info/2014/07/23/47-use-gradle-properties-to-set-alternative-android-build-tools.html#toc_0
 [2]: http://hugozhu.myalert.info/2014/07/23/47-use-gradle-properties-to-set-alternative-android-build-tools.html#toc_1
 [3]: http://hugozhu.myalert.info/2014/07/23/47-use-gradle-properties-to-set-alternative-android-build-tools.html#toc_2
 [4]: http://hugozhu.myalert.info/2014/07/23/47-use-gradle-properties-to-set-alternative-android-build-tools.html#toc_3
 [5]: http://hugozhu.myalert.info/2014/07/23/47-use-gradle-properties-to-set-alternative-android-build-tools.html#toc_4
 [6]: http://hugozhu.myalert.info/2014/07/23/47-use-gradle-properties-to-set-alternative-android-build-tools.html#toc_5
 [7]: http://hugozhu.myalert.info/2014/07/23/47-use-gradle-properties-to-set-alternative-android-build-tools.html#toc_6
 [8]: http://www.gradle.org/docs/current/userguide/tutorial_this_and_that.html