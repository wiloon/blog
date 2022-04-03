---
title: maven -pl 选项
author: "-"
date: 2012-06-19T07:25:10+00:00
url: /?p=3548
categories:
  - Java
tags:
  - Maven

---
## maven -pl 选项

mavenApache工作 在一个多模块的 maven 项目中，build 时如果不希望 build 项目中的所有模块，可以使用 -pl 选项来指定实际 build 的模块，各个模块之间使用逗号 (,) 分隔。 如何通过 -pl 选项来指定项目中的顶级模块呢？或许有人会说不需要，可以使用 -N 选项。的确 -N 选项可以使 maven 不会递归到子模块中运行。通过 -pl 选项也是可以指定顶级模块的。 maven 在使用 -pl 选项指定的值过滤模块的时候，通过两种方式，一是把 -pl 选项的值当做 groupId:artifactId 来查找，其次把 -pl 选项的值作为相对路径来查找，相对于用户运行 maven 时的工作目录。 例如有以下项目结构:  all [org.apache.maven:test] |- m-1 [org.apache.maven:m1] |- m-2 [org.apache.maven:m2] 如果想通过 -pl 选项来指定顶级模块 all 和 m-1 模块，可以使用一下这么命令:  mvn -pl org.apache.maven:test,m-1 clean install ps:上面的逻辑参见代码 org.apache.maven.project.ProjectSorter.findProject。 -EOF-