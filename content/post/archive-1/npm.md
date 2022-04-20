---
title: npm basic
author: "-"
date: 2014-02-19T05:50:38+00:00
url: npm
tags:
  - node, npm
categories:
  - inbox
---
## npm basic

## 编译

```bash
npm run build

### 指定 package.json 路径 
# /path/to/project 是包含 package.json 的目录。
npm --prefix /path/to/project run build
```

### node-gyp

gyp 是为 Chromium 项目创建的项目生成工具，可以从平台无关的配置生成平台相关的 Visual Studio、Xcode、Makefile 的项目文件。这样一来我们就不需要花额外的时间处理每个平台不同的项目配置以及项目之间的依赖关系。

## 更新包

### 手动跟新

修改 package.json 中依赖包版本，执行 npm install --force

### 使用第三方插件

```bash
npm install -g npm-check-updates
ncu # 查看可更新包
ncu -u # 更新 package.json
npm install # 升级到最新版本
```

### install npm

### archlinux

```bash
sudo npm uninstall -g @angular/cli
pacman -S nodejs
npm info pkg
```

### nvm, Node Version Manager

<https://github.com/nvm-sh/nvm>

```bash
yay -S nvm
source /usr/share/nvm/init-nvm.sh
echo 'source /usr/share/nvm/init-nvm.sh' >> ~/.bashrc
nvm ls-remote
nvm install --lts
```

### ubuntu

```bash
apt install python3.9
apt install python
```

### npm install

```bash
npm install --registry=https://registry.npm.taobao.org
```

### registory, mirror

```bash
# list registory
npm config get registry
# set registry
npm config set registry https://registry.npm.taobao.org
# 恢复
npm config set registry https://registry.npmjs.org
```

### cnpm

<https://developer.aliyun.com/mirror/NPM>

```bash
npm install -g cnpm --registry=https://registry.npm.taobao.org
# 或:  
echo '\n#alias for cnpm\nalias cnpm="npm --registry=https://registry.npm.taobao.org \
    --cache=$HOME/.npm/.cache/cnpm \
    --disturl=https://npm.taobao.org/dist \
    --userconfig=$HOME/.cnpmrc"' >> ~/.zshrc && source ~/.zshrc
```

### npm commands

```bash
npm install -help
# global install
sudo npm install --global @vue/cli
# 指定仓库
npm install --registry=https://registry.npm.taobao.org
# 指定缓存目录
npm install --cache /tmp/empty-cache
# 清除缓存
npm cache clean

# 查看缓存目录位置
npm config get cache
#清空缓存目录
npm cache clean
npm install express --save
npm install express --save-dev
# --save参数表示将该模块写入dependencies属性，--save-dev表示将该模块写入devDependencies属性。

npm cache clean
npm cache clean --force

# 检查更新
npm outdated
### 更新依赖
npm update webpack
npm uninstall grunt-cli
  
# 卸载0.1.9版本的grunt-cli

npm uninstall grunt-cli@"0.1.9"
```

### npm uninstall

 ```bash
# 删除 node_modules 目录下面的包 (package) 
npm uninstall lodash
# 从 package.json 文件中删除依赖，需要在命令后添加参数 --save
npm uninstall --save lodash

npm uninstall vue-cli -g 
 ```

#### 安装但不写入package.json

```bash
    npm install xxx
```

#### 安装并写入 package.json的"dependencies"中

```bash
    npm install xxx –S
    # 简写
    npm i @vue/composition-api -S
    # 指定版本
    npm install jquery@3.0.0 --save
```

### 打印依赖树

```bash
# list dependency
npm list
npm ls

# 查看某一个包的依赖树
npm install -g npm-remote-ls
npm-remote-ls foo

# 查看某个包为什么被安装

```

### 查看包版本

```bash
    npm info vue
    npm view vue version
    # 查看所有版本
    npm view vue versions
```

### 安装并写入package.json的"devDependencies"中

```bash
    npm install xxx –D
```

### 全局安装

```bash
    npm install xxx -g
```

### 安装指定版本

```bash
    npm install xxx@1.2.0
```

### report

```bash
    npm run build --report
```

--save和--save-dev区别
一句话:--save-dev是你开发时依赖的东西，--save是发布后还依赖的东西.

nodejs的出现，可以算是前端里程碑式的一个事件，它让前端攻城狮们摆脱了浏览器的束缚，踏上了一个更加宽广的舞台。前端的可能性，从此更加具有想象空间。

随着一系列基于nodejs的应用/工具的出现，工作中与nodejs打交道的机会越来越多。无论在node应用的开发，还是使用中，包管理都扮演着一个很重要的作用。NPM (node package manager) ，作为node的包管理工具，极大地便利了我们的开发工作，很有必要了解一下。

### NPM是什么

NPM (node package manager) ，通常称为node包管理器。顾名思义，它的主要功能就是管理node包，包括: 安装、卸载、更新、查看、搜索、发布等。

npm的背后，是基于couchdb的一个数据库，详细记录了每个包的信息，包括作者、版本、依赖、授权信息等。它的一个很重要的作用就是: 将开发者从繁琐的包管理工作 (版本、依赖等) 中解放出来，更加专注于功能的开发。

npm官网: <https://npmjs.org/>
npm官方文档: <https://npmjs.org/doc/README.html>
我们需要了解什么
npm的安装、卸载、升级、配置
  
npm的使用: package的安装、卸载、升级、查看、搜索、发布
  
npm包的安装模式: 本地 vs 全局
  
### package.json: 包描述信息

package版本: 常见版本声明形式

#### keywords

"keywords": ["server", "osiolabs", "express", "compression"]

npm包安装模式

在具体介绍npm包的管理之前，我们首先得来了解一下npm包的两种安装模式。

本地安装 vs 全局安装 (重要)

node包的安装分两种: 本地安装、全局安装。两者的区别如下，后面会通过简单例子说明

本地安装: package会被下载到当前所在目录，也只能在当前目录下使用。
  
全局安装: package会被下载到到特定的系统目录下，安装的package能够在所有目录下使用。
  
npm install pkg – 本地安装

运行如下命令，就会在当前目录下安装grunt-cli (grunt命令行工具)

npm install grunt-cli
  
安装结束后，当前目录下回多出一个node_modules目录，grunt-cli就安装在里面。同时注意控制台输出的信息:

grunt-cli@0.1.9 node_modules/grunt-cli
  
├── resolve@0.3.1
  
├── nopt@1.0.10 (abbrev@1.0.4)
  
└── findup-sync@0.1.2 (lodash@1.0.1, glob@3.1.21)
  
简单说明一下:

grunt-cli@0.1.9: 当前安装的package为grunt-cli，版本为0.19
  
node_modules/grunt-cli: 安装目录
  
resolve@0.3.1: 依赖的包有resolve、nopt、findup-sync，它们各自的版本、依赖在后面的括号里列出来
  
npm install -g pkg- 全局安装

上面已经安装了grunt-cli，然后你跑到其他目录下面运行如下命令

grunt
  
果断提示你grunt命令不存在，为什么呢？因为上面只是进行了本地安装，grunt命令只能在对应安装目录下使用。

-bash: grunt: command not found
  
如果为了使用grunt命令，每到一个目录下都得重新安装一次，那不抓狂才怪。肿么办呢？

很简单，采用全局安装就行了，很简单，加上参数-g就可以了

npm install -g grunt-cli
  
于是，在所有目录下都可以无压力使用grunt命令了。这个时候，你会注意到控制台输入的信息有点不同。主要的区别在于安装目录，现在变成了/usr/local/lib/node_modules/grunt-cli，/usr/local/lib/node_modules/也就是之前所说的全局安装目录啦。

grunt-cli@0.1.9 /usr/local/lib/node_modules/grunt-cli
  
├── resolve@0.3.1
  
├── nopt@1.0.10 (abbrev@1.0.4)
  
└── findup-sync@0.1.2 (lodash@1.0.1, glob@3.1.21)
  
npm包管理

npm的包管理命令是使用频率最高的，所以也是我们需要牢牢记住并熟练使用的。其实无非也就是几个动作: 安装、卸载、更新、查看、搜索、发布等。

安装最新版本的grunt-cli

npm install grunt-cli
  
安装0.1.9版本的grunt-cli

npm install grunt-cli@"0.1.9"
  
通过package.json进行安装

如果我们的项目依赖了很多package，一个一个地安装那将是个体力活。我们可以将项目依赖的包都在package.json这个文件里声明，然后一行命令搞定

npm ls pkg: 查看特定package的信息

运行如下命令，输出grunt-cli的信息

npm ls grunt-cli
  
输出的信息比较有限，只有安装目录、版本，如下:

/private/tmp/npm└── grunt-cli@0.1.9
  
如果要查看更详细信息，可以通过npm info pkg，输出的信息非常详尽，包括作者、版本、依赖等。

npm info grunt-cli
  
npm update pkg: package更新

npm update grunt-cli
  
npm search pgk: 搜索

输入如下命令

npm search grunt-cli
  
返回结果如下

npm http GET <http://registry.npmjs.org/-/all/since?stale=update_after&startkey=1375519407838npm> http 200 <http://registry.npmjs.org/-/all/since?stale=update_after&startkey=1375519407838NAME> DESCRIPTION AUTHOR DATE KEYWORDSgrunt-cli The grunt command line interface. =cowboy =tkellen 2013-07-27 02:24grunt-cli-dev-exitprocess The grunt command line interface. =dnevnik 2013-03-11 16:19grunt-client-compiler Grunt wrapper for client-compiler. =rubenv 2013-03-26 09:15 gruntplugingrunt-clientside Generate clientside js code from CommonJS modules =jga 2012-11-07 01:20 gruntplugin
  
npm发布

这个命令我自己也还没实际用过，不误导大家，语法如下，也可参考官方对于package发布的说明<https://npmjs.org/doc/developers.html>:

```bash
npm publish <tarball> npm publish <folder>
```
  
NPM配置

npm的配置工作主要是通过npm config命令，主要包含增、删、改、查几个步骤，下面就以最为常用的proxy配置为例。

设置proxy

内网使用npm很头痛的一个问题就是代理，假设我们的代理是 <http://proxy.example.com:8080>，那么命令如下:

npm config set proxy <http://proxy.example.com:8080>
  
由于npm config set命令比较常用，于是可以如下简写

npm set proxy <http://proxy.example.com:8080>
  
查看proxy

设置完，我们查看下当前代理设置

npm config get proxy
  
输出如下:

<http://proxy.example.com:8080/>
  
同样可如下简写:

npm get proxy
  
删除proxy

代理不需要用到了，那删了吧

npm delete proxy
  
查看所有配置

npm config list
  
直接修改配置文件

有时候觉得一条配置一条配置地修改有些麻烦，就直接进配置文件修改了

npm config edit
  
关于package.json

这货在官网似乎没有详细的描述，其实就是包的描述信息啦。假设当我们下载了node应用，这个node应用依赖于A、B、C三个包，如果没有package.json，我们需要人肉安装这个三个包 (如果对版本有特定要求就更悲剧了) :

npm install Anpm install Bnpm install C
  
有了package.json，一行命令安装所有依赖。

npm install
  
package.json字段简介

字段相当多，但最重要的的是下面几个

name: package的名字 (由于他会成为url的一部分，所以 non-url-safe 的字母不会通过，也不允许出现"."、"_") ，最好先在<http://registry.npmjs.org/>上搜下你取的名字是否已经存在
  
version: package的版本，当package发生变化时，version也应该跟着一起变化，同时，你声明的版本需要通过semver的校验 (semver可自行谷歌)
  
dependencies: package的应用依赖模块，即别人要使用这个package，至少需要安装哪些东西。应用依赖模块会安装到当前模块的node_modules目录下。
  
devDependencies: package的开发依赖模块，即别人要在这个package上进行开发
  
其他: 参见官网
  
package版本

在package.json里，你经常会在包名后看到类似"~0.1.0″这样的字符串，这就是包的版本啦。下面会列举最常见的版本声明形式，以及版本书写的要求:

常见版本声明形式

a、"~1.2.3″ 是神马意思呢，看下面领悟

"~1.2.3" = ">=1.2.3 <1.3.0""~1.2" = ">=1.2.0 <1.3.0""~1" = ">=1.0.0 <1.1.0"
  
b、"1.x.x"是什么意思呢，继续自行领悟

"1.2.x" = ">=1.2.0 <1.3.0""1.x.x" = ">=1.0.0 <2.0.0""1.2" = "1.2.x""1.x" = "1.x.x""1" = "1.x.x"
  
版本书写要求

版本可以v开头，比如 v1.0.1 (v只是可选)
  
1.0.1-7，这里的7是所谓的"构建版本号"，不理是神马，反正版本大于1.0.1
  
1.0.1beta，或者1.0.1-beta，如果1.0.1后面不是 "连字符加数字" 这种形式，那么它是pre release 版本，即版本小于 1.0.1
  
根据b、c，有: 0.1.2-7 > 0.1.2-7-beta > 0.1.2-6 > 0.1.2 > 0.1.2beta
  
写在后面

内容只是简单地把最常见的命令，以及一些需要了解的内容列了出来。如要进一步了解，可参考官网说明。此外，npm help是我们最好的朋友，如果忘了有哪些命令，命令下有哪些参数，可通过help进行查看。

Windows平台下的Node.js安装

在过去，Node.js一直不支持在Windows平台下原生编译，需要借助Cygwin或MinGW来模拟POSIX系统，才能编译安装。幸运的是2011年6月微软开始与Joyent合作移植Node.js到Windows平台上 (<http://www.infoq.com/cn/news/2011/06/node-exe> ) ，这次合作的成果最终呈现在0.6.x的稳定版的发布上。这次的版本发布使得Node.js在Windows平台上的性能大幅度提高，使用方面也更容易和轻巧，完全摆脱掉Cygwin或MinGW等实验室式的环境，并且在某些细节方面，表现出比Linux下更高的性能，细节参见<http://www.infoq.com/news/2011/11/Nodejs-Windows>。

在Windows (Windows7) 平台下，我将介绍二种安装Node.js的方法，即普通和文艺安装方法。

普通的安装方法

普通安装方法其实就是最简单的方法了，对于大多Windows用户而言，都是不太喜欢折腾的人，你可以从这里 (<http://nodejs.org/dist/v0.6.1/node-v0.6.1.msi> ) 直接下载到Node.js编译好的msi文件。然后双击即可在程序的引导下完成安装。

在命令行中直接运行:

node -v
  
命令行将打印出:

v0.6.1
  
该引导步骤会将node.exe文件安装到C:\Program Files (x86)\nodejs\目录下，并将该目录添加进PATH环境变量。

### npm ci 和 npm install 差异v

项目必须存在 package-lock.json 或 npm-shrinkwrap.json。
如果 lockfiles 中的依赖和 package.json 中不匹配，npm ci 会退出并且报错，而不是去更新 lockfiles。
npm ci 只能安装整个项目的依赖，无法安装单个依赖。
如果 node_modules 已经存在，它将在 npm ci 开始安装之前自动删除。
npm ci 永远不会改变 package.json 和 package-lock.json。

补充

npm install 读取 package.json 创建依赖项列表，并使用 package-lock.json 来通知要安装这些依赖项的哪个版本。如果某个依赖项在 package.json 中，但是不在 package-lock.json 中，运行 npm install 会将这个依赖项的确定版本更新到 package-lock.json 中。

npm ci 是根据 package-lock.json 去安装确定的依赖，package.json 只是用来验证是不是有不匹配的版本，假设 package-lock.json 中存在一个确定版本的依赖 A，如果 package.json 中不存在依赖 A 或者依赖 A 版本和 lock 中不兼容，npm ci 就会报错。

作者: 小被子
链接: <https://juejin.cn/post/6844903903193104398>
来源: 掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

### npx

npm 从5.2版开始，增加了 npx 命令  
npx 想要解决的主要问题，就是调用项目内部安装的模块  

---

<http://weibo.com/chyingp>  
<http://www.zcool.com.cn/u/346408/>  
<http://www.cnblogs.com/chyingp/p/npm.html>  
<http://www.infoq.com/cn/articles/nodejs-npm-install-config>  
<https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager#arch-linux>

## 版本号规则

- `^`: 只会执行不更改最左边非零数字的更新。 如果写入的是 ^0.13.0，则当运行 npm update 时，可以更新到 0.13.1、0.13.2 等，但不能更新到 0.14.0 或更高版本。 如果写入的是 ^1.13.0，则当运行 npm update 时，可以更新到 1.13.1、1.14.0 等，但不能更新到 2.0.0 或更高版本。
- `~`: 如果写入的是 〜0.13.0，则当运行 npm update 时，会更新到补丁版本：即 0.13.1 可以，但 0.14.0 不可以。
- `*` 匹配 >=0.0.0
