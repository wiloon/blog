---
title: Maven内置变量
author: "-"
date: 2015-09-10T00:37:50+00:00
url: /?p=8234
categories:
  - Uncategorized

tags:
  - reprint
---
## Maven内置变量
Maven内置变量说明: 

  * ${basedir} 项目根目录
  * ${project.build.directory} 构建目录，缺省为target
  * ${project.build.outputDirectory} 构建过程输出目录，缺省为target/classes

  ${project.build.finalName} 产出物名称，缺省为${project.artifactId}-${project.version}

  * ${project.packaging} 打包类型，缺省为jar

  ${project.xxx} 当前pom文件的任意节点的内容
