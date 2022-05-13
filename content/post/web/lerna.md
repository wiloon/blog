---
author: "-"
date: "2020-05-16T06:30:12Z"
title: "lerna"
categories:
  - inbox
tags:
  - reprint
---
## "lerna"
## 什么是lerna?为什么要使用lerna?

lerna到底是什么呢？lerna官网上是这样描述的。

> A tool for managing JavaScript projects with multiple packages.

这个介绍可以说很清晰了，引入lerna后，上面提到的问题不仅迎刃而解，更为开发人员提供了一种管理多packages javascript项目的方式。

1. 自动解决packages之间的依赖关系
2. 通过`git` 检测文件改动，自动发布
3. 根据`git` 提交记录，自动生成CHANGELOG

## 使用lerna的基本工作流

### 环境配置

* Git 在一个lerna工程里，是通过git来进行代码管理的。所以你首先要确保本地有正确的git环境。 如果需要多人协作开发，请先创建正确的git中心仓库的链接。 因此需要你了解基本的git操作，在此不再赘述。
* npm仓库 无论你管理的package是要发布到官网还是公司的私有服务器上，都需要正确的仓库地址和用户名。 你可运行下方的命令来检查，本地的npm `registry`地址是否正确。

    npm config ls
    复制代码

* lerna 你需要全局安装lerna工具。

    npm install lerna -g
    复制代码

### 初始化一个lerna工程

> 在这个例子中，我将在我本地`d:/` 根目录下初始化一个lerna工程。

1. 在`d:/` 下创建一个空的文件夹，命名为`lerna-demo`

    mkdir lerna-demo
    复制代码

2. 初始化 通过cmd进入相关目录，进行初始化

    cd d:/lerna-demo
    lerna init
    复制代码

执行成功后，目录下将会生成这样的目录结构。

     - packages(目录)
     - lerna.json(配置文件)
     - package.json(工程描述文件)
    复制代码

3. 添加一个测试package

> 默认情况下，package是放在`packages`目录下的。

    // 进入packages目录
    cd d:/lerna-demo/packages
    // 创建一个packge目录
    mkdir module-1
    // 进入module-1 package目录
    cd module-1
    // 初始化一个package
    npm init -y
    复制代码

执行完毕，工程下的目录结构如下

    --packages
        --module-1
            package.json
    --lerna.json
    --package.json
    
    复制代码

4. 安装各packages依赖 这一步操作，官网上是这样描述的。

> Bootstrap the packages in the current Lerna repo. Installs all of their dependencies and links any cross-dependencies.

    cd d:/lerna-demo
    lerna bootstrap
    复制代码

在现在的测试package中，module-1是没有任何依赖的，因此为了更加接近真实情况。你可已在module-1的`package.json` 文件中添加一些第三方库的依赖。 这样的话，当你执行完该条命令后，你会发现module-1的依赖已经安装上了。

5. 发布 在发布的时候，就需要`git` 工具的配合了。 所以在发布之前，请确认此时该lerna工程是否已经连接到git的远程仓库。你可以执行下面的命令进行查看。

    git remote -v
    // print log
    origin  git@github.com:LittleBreak/lerna-best-practices.git (fetch)
    origin  git@github.com:LittleBreak/lerna-best-practices.git (push)
    复制代码

本篇文章的代码托管在[Github](https://github.com/LittleBreak/lerna-best-practices)上。因此会显示此远程链接信息。 如果你还没有与远程仓库链接，请首先在github创建一个空的仓库，然后根据相关提示信息，进行链接。

    lerna publish
    复制代码

执行这条命令，你就可以根据cmd中的提示，一步步的发布packges了。

实际上在执行该条命令的时候，lerna会做很多的工作。

     -  Run the equivalent of  `lerna updated`  to determine which packages need to be published.
     -  If necessary, increment the  `version`  key in  `lerna.json`.
     -  Update the  `package.json`  of all updated packages to their new versions.
     -  Update all dependencies of the updated packages with the new versions, specified with a  [caret (^)](https://docs.npmjs.com/files/package.json#dependencies).
     -  Create a new git commit and tag for the new version.
     -  Publish updated packages to npm.
    复制代码

到这里为止，就是一个最简单的lerna的工作流了。但是lerna还有更多的功能等待你去发掘。 lerna有两种工作模式,Independent mode和Fixed/Locked mode，在这里介绍可能会对初学者造成困扰，但因为实在太重要了，还是有必要提一下的。 lerna的默认模式是Fixed/Locked mode，在这种模式下，实际上lerna是把工程当作一个整体来对待。每次发布packges，都是全量发布，无论是否修改。但是在Independent mode下，lerna会配合`Git`，检查文件变动，只发布有改动的packge。

## lerna最佳实践

为了能够使lerna发挥最大的作用，根据这段时间使用`lerna` 的经验，总结出一个最佳实践。下面是一些特性。

1. 采用Independent模式
2. 根据`Git`提交信息，自动生成changelog
3. eslint规则检查
4. prettier自动格式化代码
5. 提交代码，代码检查hook
6. 遵循semver版本规范

大家应该也可以看出来，在开发这种工程的过程的，最为重要的一点就是**规范**。因为应用场景各种各样，你必须保证发布的packge是规范的，代码是规范的，一切都是有迹可循的。这点我认为是非常重要的。 [github代码](https://github.com/LittleBreak/lerna-best-practices)

## 工具整合

在这里引入的工具都是为了解决一个问题，就是工程和代码的规范问题。

* husky
* lint-staged
* prettier
* eslint
  
作者: 破晓前  
链接: [https://juejin.im/post/5a989fb451882555731b88c2](https://juejin.im/post/5a989fb451882555731b88c2 "https://juejin.im/post/5a989fb451882555731b88c2")  
来源: 掘金  
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。