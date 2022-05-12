---
title: eclipse updating indexes
author: "-"
date: 2012-04-22T08:32:27+00:00
url: /?p=2996
categories:
  - Java
tags:
  - reprint
---
## eclipse updating indexes
解决为什么每次打开Eclipse新的workspace需要更新nexus-maven-repository-index问题

  1. 新建一个Eclipse的workspace。
  2. 打开Window—>Preferences，如下图所示: 
  3. 打开Preferences后，点击Maven，可以看到右边Maven下的Download repository index updates on startp。取消该项的勾选，点击Apply后点击OK即可。如下图所示: 

  1. 在之前已经有下载好的repository index 已有工作空间下，找到.metadata.pluginsorg.maven.ide.eclipsenexus。把该目录下的central文件夹整个复制到新建的workspace下对应的.metadata.pluginsorg.maven.ide.eclipsenexus目录下。替代原系统自动生成的central文件夹及其内容。
  2. 完成以上步骤，下面我们来进行手动设置nexus-maven-repository-index更新。打开Eclipse的Window—>Show View—>Other…，如下图所示: 

  1. 打开后，找到Maven，点击就可以看到Maven Indexes，选中点击OK进入。如下图所示: 

  1. 下面就自动出现视图窗口，里面应该有好三列记录，分别是workspace, local和central,分别对应了该工程的java代码,本地MAVEN库和官方库。如下图所示: 

  1. 选中local并点击右键，会出现Update Index，点击Update Index，即完成了手动更新nexus-maven-repository-index，不用再从远程官方库来下载了。

以上这些步骤就解决了每次新建一个工作空间，Eclipse自动从官方库下载nexus-maven-repository-index的问题了。

-

First check all of your dependencies including plugins and children in the dependency tree,
  
try to replace snapshot versions with release versions,
  
as snapshot versions will always look for a later update, whereas
  
release versions are deemed to be stable and updates are not expected for the same version number.

Secondly, assuming that you are working on a LAN, I would suggest that you install a local maven repository manager such as Nexus, and then redirect your artifact requests by setting
  
`<mirrorOf>*</mirrorOf>` in your ${user.home}/.m2/settings.xml

This will enable your downloads to be resolved quickly against a local mirror, rather than continually checking against repositories on the internet.

<http://stackoverflow.com/questions/5012567/why-does-eclipse-take-so-long-to-update-maven-dependencies>