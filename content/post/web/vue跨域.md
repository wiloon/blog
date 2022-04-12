---
author: "-"
date: "2020-05-22T05:23:52Z"
title: Vue 跨域

categories:
  - inbox
tags:
  - reprint
---
## Vue 跨域

## 缘起

最近实验课上需要重构以前写过的一个项目 (垃圾堆) ，需要添加发生邮件提醒的功能，记得以前写过一个PHP版的实现，所以想把PHP写的功能整理成一个服务，然后在前端调用。但是这个项目是JavaWeb，也就是说我需要面对跨域的问题。不过本篇文章，讲的并不是如何解决这样的跨域问题，而是我在找如何解决这个问题的路上遇到的坑。

其实，在前端工程化大行其道的现在，前后端已经分离开来，前端为了提高工作流效率往往自己开一个小型的服务器，就比如`webpack.devServer`。这样在前端调用后端接口的时候必然会面临跨域的问题， 如题，`Vue-cli 3.x + axios 跨域方案` 就是解决这里的跨域问题。这里的跨域是基于`webpack`的devServer的代理功能 (proxy) 来实现开发环境中的跨域，也就是说本篇所讨论的并不能解决生产环境下的跨域问题，因为webpack.devServer是DevDependencies，一旦打包上线，这个proxy代理就会失效。但是这并不妨碍我们开发中使用跨域来提高开发效率和体验。

## 开始填坑

其实这个问题解决起来很简单，网上也是很多教程，为了文章完整性，我这里也做一个尽量完备的展示，介绍如何配置Vue-cli 3.x来实现跨域 。

### vue.config.js中devServer.proxy的配置解析

Vue-cli3.x比Vue-cli2.x构建的项目要简化很多，根目录下只有`./src`和`./public`文件夹，所以网上很多教程说`config`目录下的`vue.config.js`是说的vue-cli 2.x版本。那么对于Vue-cli 3.x版本，构建也很简单，直接在根目录里建一个`vue.config.js`配置文件就可以了，我们直接看`devServer.proxy`里的代码:

我这里devServer的地址是: localhost:8080/，需要代理的地址是: localhost/index/phpinfo.php  (我自己写的一个测试跨域用的php，返回一个'ok')

下面是根据上面的地址需要配置的proxy对象

    module.exports = {
      devServer: {
        proxy: {
          '/api': {
            target: 'http://192.168.80.2:38081',
            ws: true,
            changeOrigin: true,
            pathRewrite: {
              '^/api': ''
            }
          }
        }
      }
    }

    # main.ts
    axios.defaults.baseURL = '/api'

大部分教程到这里就停止了，但是我在这里做一个扩展，为了让读者理解这里的配置是如何起作用的 (以下内容整理自`http-proxy-middleware`的[npm描述](https://github.com/chimurai/http-proxy-middleware#context-matching)里，`http-proxy-middleware`是一个npm模块，是proxy的底层原理实现) 。

             foo://example.com:8042/over/there?name=ferret#nose
             _/   ______________/_________/ _________/ __/
              |           |            |            |        |
           scheme     authority       path        query   fragment
    复制代码

以我上面的配置为例，`'/index'`这个`key`在`http-proxy-middleware`中被称为`context`——用来决定哪些请求需要被`target`对应的主机地址 (这里是`http://localhost/index`) 代理，它可以是 字符串，含有通配符的字符串，或是一个数组，分别对应于`path matching`(路径匹配)`wildcard path matching`(通配符路径匹配)`multiple path matching`(多路径匹配)，而这里的`path`指的就是上图所标识的path段。

简言之，这个key就是匹配`path`的，一旦匹配到符合的`path`，就会把请求转发的代理主机去，而代理主机的地址就是`target`字段对应的内容。

那`pathRewrit`是什么意思呢？意如其名，路径重写。就是把模式 (这里是`^/index`) 匹配到的`path`重写为对应的路径 (这里是`''`，相当于删除了这个匹配到的路径) 。除了删除，还有在原有路径上添加一个基础路径，或是改写一个路径的方式，这可以参考`http-proxy-middleware`的[npm描述的option.pathRewrite章节](https://github.com/chimurai/http-proxy-middleware#http-proxy-middleware-options) 。

### 在Vue中使用axios

这个使用任意一个ajax封装的库都是可行的，axios，jquery.ajax或者是vue-resource都是可以的。

在Vue中使用axios，网上有两种方法，一种是将axios加入Vue的原型里，我更推荐第二种方法:

    npm install axios vue-axios

    
    import axios from 'axios';
    import VueAxios from 'vue-axios';
    Vue.use(VueAxios,axios);

以我上面的proxy配置为基础，想要让代理成功转发到`localhost/index/phpinfo.php`，在Vue实例中axios需要这样写访问地址:

    this.axios.get('/index/phpinfo.php').then((res)=>{
            console.log(res);
          })

我们来分析这些代码整个发挥作用的原理是什么？首先，axios去访问`/index/phpinfo.php`，这是个相对地址，所以真实访问地址其实是`localhost:8080/index/phpinfo.php`，然而`/index/phpinfo.php`被我们配置的`/index`匹配到了 ，所以访问被proxy代理，那转发到哪个路径呢？在`pathRewrite`中，我们将模式`^/index`的路径清除了，所以最终的访问路径是 `target`+`pathRewrite`+ 剩余的部分 ， 这样也就是 `http://localhost/index`++`/phpinfo.php`

### 坑点

可能出现即使配置了proxy，但是依然没有任何卵用。

* 大部分情况是因为你的proxy配置和你的访问路径不匹配，或者即使匹配到了，但是转发出去的地址不对，没有命中后端给的API
* 或者看看axios，有没有使用正确姿势？
* 还有一点，或许你看到返回的response里的url依然显示的是本地主机，但是数据已经正常返回，这是正常的，因为我们访问的本来就是本地主机，只不过proxy转发了这个请求到一个新的地址。

### 生产环境部署用nginx解决

    server {
            listen 80;
            server_name foo.wiloon.com;
            rewrite ^/(.*)$ https://$host/;
    }
    server {
            listen 443 ssl;
            server_name foo.wiloon.com;
    
            include /etc/nginx/ssl.conf;
            include /etc/nginx/error-pages.conf;
    
            location /api {
                    proxy_pass http://192.168.50.xxx:38081/;
            }
            location / {
                    proxy_pass http://192.168.50.xxx:38080/;
            }
    }

<https://segmentfault.com/a/1190000010792260>

<https://juejin.im/post/5d1cc073f265da1bcb4f486d>

### axios 302

如果返回的状态码是200，这时候通过response.request.responseURL获取地址，然后进行重定向
axios.post('.', Data)
     .then(response => {
         if (response.status === 200) {
             window.location.href = response.request.responseURL;
         }
     })
     .catch(error => {console.log(error)});

><https://xudany.github.io/axios/2020/07/14/%E5%85%B3%E4%BA%8E-axios-302-%E9%87%8D%E5%AE%9A%E5%90%91%E7%9A%84%E9%97%AE%E9%A2%98/>
