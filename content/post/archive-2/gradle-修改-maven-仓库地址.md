---
title: Gradle 修改 Maven 仓库地址
author: "-"
date: 2016-03-20T05:57:31+00:00
url: /?p=8813
categories:
  - Inbox
tags:
  - reprint
---
## Gradle 修改 Maven 仓库地址

### gradle kotlin

repositories {
    mavenCentral()
    maven {
        setUrl("<MAVEN REPO URL>")
    }
}

```

http://www.yrom.net/blog/2015/02/07/change-gradle-maven-repo-url/

近来迁移了一些项目到Android Studio,采用Gradle构建确实比原来的Ant方便许多。但是编译时下载依赖的网速又着实令人蛋疼不已。

如果能切换到国内的Maven镜像仓库,如开源中国的Maven库,又或者是换成自建的Maven私服,那想必是极好的。

一个简单的办法,修改项目根目录下的build.gradle,将jcenter()或者mavenCentral()替换掉即可: 

allprojects {
  
repositories {
  
maven{ url 'http://maven.oschina.net/content/groups/public/'}
  
}
  
}

但是架不住项目多,难不成每个都改一遍么？

自然是有省事的办法,将下面这段Copy到名为init.gradle文件中,并保存到 USER_HOME/.gradle/文件夹下即可。

 

allprojects{
  
repositories {
  
def REPOSITORY_URL = 'http://maven.oschina.net/content/groups/public'
  
all { ArtifactRepository repo ->
  
if(repo instanceof MavenArtifactRepository){
  
def url = repo.url.toString()
  
if (url.startsWith('https://repo1.maven.org/maven2') || url.startsWith('https://jcenter.bintray.com/')) {
  
project.logger.lifecycle "Repository ${repo.url} replaced by $REPOSITORY_URL."
  
remove repo
  
}
  
}
  
}
  
maven {
  
url REPOSITORY_URL
  
}
  
}
  
}

init.gradle文件其实是Gradle的初始化脚本(Initialization Scripts),也是运行时的全局配置。
  
更详细的介绍请参阅 http://gradle.org/docs/current/userguide/init_scripts.html
