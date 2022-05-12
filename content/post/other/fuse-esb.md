---
title: Fuse ESB
author: "-"
date: 2012-02-17T01:57:01+00:00
url: /?p=2323
categories:
  - Development
tags:
  - reprint
---
## Fuse ESB
Fuse ESB 学习笔记 (一) 构建

红薯 发表于 9-28 16:46
  
Fuse本来是开源软件商IONA的SOA集成套件，其中包括了ESB、Message Broker、Service Framework和Mediation Router。IONA现已被Progress公司于08年收购。

Fuse的SOA功能套件并不是独立开发，而是基于Apache的相关开源产品扩展和完善而来的，通过集成的方式提供了一套较为完整的SOA环境。 例如ESB产品的基础是ServiceMix，Message Broker是来自于 ActiveMQ，Service Framework基于CXF，而Mediation Router则使用的是Camel。

感觉这也是一种不错的商业和开源之间的结合模式，通过开源社区的贡献完善软件产品，再借助Progress公司商业化的运作为用户提供免费和收费的技术支持。

虽然Fuse的文档和在线支持方面做得还是不错，但是如果要想深入了解Fuse并把它应用到项目中去，学习曲线还是略显陡峭，牵扯到的技术太多，而且这些技术自身也在快速演进之中，每个小版本之间的差异就很大。

首先从Fuse的ESB产品开始学习，之前需要准备的知识有: 

Maven2 (越来越多的开源项目都在采用MVN作为构建工具，逐渐替代ANT成为开源项目构建事实标准了，想玩开源，还是先老老实实的搞懂它吧) 
  
OSGi (目前有两个比较成熟的实现，一个是Eclipse的Equinox，另一个是Apache的Felix。实现微内核架构和模块 化，Fuse ESB最新版本是基于ServiceMix 4这个版本的，从这个版本开始，ServiceMix已经将核心从JBI规范的实现转为使用OSGi实现ESB功能) 
  
Spring DM (降低OSGi的企业应用门槛，和Spring进行整合，目前已经作为Eclipse RT的高级项目从springframework.org迁移到了eclipse.org，代号为Virgo) 
  
这些都是Fuse ESB的基础技术，没有掌握的同学请先自行补课

虽然Progress提供了安装程序，但是建议还是从源码开始安装，以便于和开发环境结合，方便后续的扩展或hack。

首先从fusesource.com上下载最新的源码包，目前最新版本是4.2.0，总共1兆多点。

ServiceMix是标准的Maven项目，在根目录下直接就可以找到父pom.xml，可以看到其中包含了多个Maven的module。

构建之前要先设置Maven的环境变量，否则编译时会内存不足: MAVEN_OPTS=-Xmx512m

之后运行mvn install -Dmaven.test.skip=true，以后再次编译时，为了节省时间，可以加上-o参数，离线构建。

注意一定要跳过单元测试，否则会编译不通过

漫长的等待之后，可以看到BUILD SUCCESS。实现完整构建需要下载大量的第三方jar包，在公司的破网络环境下竟然令人发指的下载了将近6个小时。。。。。。

编译后的target放在了assembly这个module中，可以在其中找到可执行版本: apache-servicemix-4.2.0-fuse-01-00.zip

解压之后，运行bin目录下的servicemix.bat，启动成功后可以看到servicemix的console。

需要注意的是，从4.2.0这个版本开始，servicemix的console已经换成了felix中的karaf实现。console的语法相比4.1.0版本又再一次改变。好在还比较好上手，按tab键可以实现命令行自动补齐。

下边简单说明一下fuse esb里边几个在开发和部署时常用的目录功能: 

bin (启动或终止esb服务的命令行工具) 
  
data (运行时所产生的OSGi bundle的缓存、日志等存放目录) 
  
deploy (用于部署。把自己开发bc等包复制到该目录，可以自动部署) 
  
etc (配置文件的集中存放地，其中可以配置OSGi框架启动时所加载的bundle等。自定义的配置文件也放在这里) 

<http://www.oschina.net/question/12_11603>