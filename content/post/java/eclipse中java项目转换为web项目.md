---
title: eclipse中java项目转换为web项目
author: "-"
date: 2012-05-27T07:13:39+00:00
url: /?p=3264
categories:
  - Java

tags:
  - reprint
---
## eclipse中java项目转换为web项目
http://hi.baidu.com/starhuo/blog/item/cddb59eeec8cd7f7b3fb955f.html

经常在eclipse中导入web项目时，出现转不了项目类型的问题，导入后就是一个java项目，有过很多次经历，今天也有同事遇到类似问题，就把这个解决方法记下来吧，免得以后再到处去搜索。

解决步骤: 

1. 进入项目目录，可看到.project文件，打开。

2. 找到<natures>...</natures>代码片段。

3. 在第2步的代码片段中加入如下标签内容并保存: 

<nature>org.eclipse.wst.common.project.facet.core.nature</nature>
  
<nature>org.eclipse.wst.common.modulecore.ModuleCoreNature</nature>
  
<nature>org.eclipse.jem.workbench.JavaEMFNature</nature>

4. 在eclipse的项目上点右键，刷新项目。

5. 在项目上点右键，进入属性 (properties) 

6. 在左侧列表项目中点击选择"Project Facets"，在右侧选择"Dynamic Web Module"和"Java"，点击OK保存即可。