+++
author = "w1100n"
date = "2020-05-16T03:03:37Z"
title = "vue"

+++

```bash

sudo pacman -S nodejs
sudo pacman -S yarn
yarn global add vue
yarn global remove vue-cli
yarn global add @vue/cli
```
### 用vue cli 创建一个项目 
    vue create hello-world
### 或者 使用图形界面
    vue ui
#### unit test
Jest
#### E2E test
Cypress

### run 
yarn serve

### add vuetify
    vue add vuetify
#### vuetify config
- use a pre-made template Y
- use custom theme N
- Use custom properties N
- Select icon font: Material Design Icons
- Use fonts as a dependency: y
- Use a-la-carte components: y
- Select locale: English


#### Could not find a declaration file for module 'vuetify/lib'
    vim tsconfig.json

    "compilerOptions": {
         "types": ["...", "vuetify"],


#### a-la-carte 组件
 只包含需要(想要)使用的组件,而不是获取所有组件

### 使用 axios 访问 API
    yarn add axios
    
```bash
yarn global add @vue/cli-service
yarn global add @vue/cli-plugin-babel
yarn global add @vue/cli-plugin-e2e-cypress
yarn global add @vue/cli-plugin-eslint
yarn global add @vue/cli-plugin-pwa
yarn global add @vue/cli-plugin-typescript
yarn global add @vue/cli-plugin-unit-jest
yarn global add vue-cli-plugin-vuetify
yarn add        @vue/cli-plugin-babel
yarn add @mdi/font -D
yarn global add lerna
yarn global add typescript

vue --version

vue create my-app
vue add vue-next
yarn run serve

vue add vuetify
vim tsconfig.json
"compilerOptions": {
  "types": ["...", "vuetify"],
  https://github.com/vuetifyjs/vuetify/issues/5944
```
## Project setup
```
yarn install
```

### Compiles and hot-reloads for development
```
yarn serve
```

### Compiles and minifies for production
```
yarn build
```

### Run your unit tests
```
yarn test:unit
```

### Run your end-to-end tests
```
yarn test:e2e
```

### Lints and fixes files
```
yarn lint
```

https://www.jianshu.com/p/7de5d4f612d7

### ui

[https://element.eleme.cn/#/zh-CN](https://element.eleme.cn/#/zh-CN "https://element.eleme.cn/#/zh-CN")

使用 axios 访问 API

Babel 和 webpack 的模块系统

**Modern JavaScript with ES2015/16**：阅读 Babel 的 [**Learn ES2015 guide**](https://babeljs.io/docs/learn-es2015/)。你不需要立刻记住每一个方法，但是你可以

[https://babeljs.io/docs/en/learn](https://babeljs.io/docs/en/learn "https://babeljs.io/docs/en/learn")保留这个页面以便后期参考。

webpack 或 Browserify 等构建工具

Pug，Babel (with ES2015 modules)，和 Stylus。

### Docker 部署 vue 项目

[https://juejin.im/post/5cce4b1cf265da0373719819](https://juejin.im/post/5cce4b1cf265da0373719819 "https://juejin.im/post/5cce4b1cf265da0373719819")

[https://vue-loader.vuejs.org/zh/#vue-loader-%E6%98%AF%E4%BB%80%E4%B9%88%EF%BC%9F](https://vue-loader.vuejs.org/zh/#vue-loader-%E6%98%AF%E4%BB%80%E4%B9%88%EF%BC%9F "https://vue-loader.vuejs.org/zh/#vue-loader-%E6%98%AF%E4%BB%80%E4%B9%88%EF%BC%9F")

[https://webpack.js.org/configuration/](https://webpack.js.org/configuration/ "https://webpack.js.org/configuration/")

### webstorm reformat

[https://www.jetbrains.com/help/webstorm/eslint.html](https://www.jetbrains.com/help/webstorm/eslint.html "https://www.jetbrains.com/help/webstorm/eslint.html")

[https://stackoverflow.com/questions/41735890/how-to-make-webstorm-format-code-according-to-eslint](https://stackoverflow.com/questions/41735890/how-to-make-webstorm-format-code-according-to-eslint "https://stackoverflow.com/questions/41735890/how-to-make-webstorm-format-code-according-to-eslint")

### 跨域

[https://juejin.im/post/5d1cc073f265da1bcb4f486d](https://juejin.im/post/5d1cc073f265da1bcb4f486d "https://juejin.im/post/5d1cc073f265da1bcb4f486d")

### JWT

[https://segmentfault.com/a/1190000010444825](https://segmentfault.com/a/1190000010444825 "https://segmentfault.com/a/1190000010444825")

[https://www.jianshu.com/p/aeaa353da89b](https://www.jianshu.com/p/aeaa353da89b "https://www.jianshu.com/p/aeaa353da89b")

企业微信

[https://juejin.im/post/5b3475adf265da5977597e27](https://juejin.im/post/5b3475adf265da5977597e27 "https://juejin.im/post/5b3475adf265da5977597e27")

### 取当前页面的url
- this.$route.path
- window.location.href
- this.$route.params


### 组件按组分块
    const Foo = () => import(/* webpackChunkName: "group-foo" */ './Foo.vue')
    const Bar = () => import(/* webpackChunkName: "group-foo" */ './Bar.vue')
    const Baz = () => import(/* webpackChunkName: "group-foo" */ './Baz.vue')

### JavaScript Source Map
Source map就是一个信息文件，里面储存着位置信息。也就是说，转换后的代码的每一个位置，所对应的转换前的位置。
有了它，出错的时候，除错工具将直接显示原始代码，而不是转换后的代码。

#### vue.config.js
        // 生产环境 sourceMap
        productionSourceMap: false,

### 去掉微信页面上的缩放按钮
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">

#### vue-meta
    yarn add vue-meta
#### main.ts
    import VueMeta from 'vue-meta'
    Vue.use(VueMeta)
    
##### 常规页面
    export default {
    name: 'Home',
    components: {},
    metaInfo: {
        meta: [
        { charset: 'utf-8' },
        {
            name: 'description',
            content: 'gator'
        },
        {
            name: 'viewport',
            content: 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes'
        }
        ]
    },
    data () {
        return {
        dense: false
        }
    },
    mounted () {
        console.log('qr scanner mounted: ')
    }
    }

#### 用了 vue-class-component 的页面 
    @Component({
    metaInfo: {
        meta: [
        { charset: 'utf-8' },
        { name: 'description', content: 'gator' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes' }
        ]
    },
    components: { Vin }
    })


### vue-class-component
### pwa
    vim vue.config.js

        module.exports = {
        pwa: {
            // 一些基础配置
            name: 'RSSX',
            assetsVersion: '1.0.0',
            themeColor: '#4DBA87',
            msTileColor: '#000000',
            appleMobileWebAppCapable: 'yes',
            appleMobileWebAppStatusBarStyle: 'debault',
            workboxPluginMode: 'InjectManifest',
            workboxOptions: {
            // 自定义的service worker文件的位置
            swSrc: 'src/service-worker.js'
            }
        },
    //...

#### service-worker.js
修改在 Cache Storage 中的缓存名。
程序保存在 Cache Storage 的默认缓存有两个，一个是预缓存一个是运行时缓存。

缓存名的格式是 <prefix>-<Cache ID>-<suffix>，通过修改缓存前缀和后缀，可以让缓存名独一无二，避免在使用 localhost 调试程序时因为端口号相同引发的冲突。
修改前后缀：

        workbox.core.setCacheNameDetails({
        prefix: 'my-app',
        suffix: 'v1'
        });

        // 一旦激活就开始控制任何现有客户机（通常是与skipWaiting配合使用）
        // https://developers.google.com/web/tools/workbox/reference-docs/latest/workbox-core_clientsClaim.mjs
        workbox.core.clientsClaim()
        // 跳过等待期
        // https://developers.google.com/web/tools/workbox/reference-docs/latest/workbox-core_skipWaiting.mjs
        workbox.core.skipWaiting()

### vue typescript 调用 javascript
https://blog.csdn.net/qq_29483485/article/details/86605215

    vim src/assets/foo.js

    # content
    export function foo () {
        console.log('foo')
    }

    # 组件中引用
    import { foo } from './assets/foo.js'
    //...
    mounted () {
        foo()
    }
---

### vue typescript
https://xie.infoq.cn/article/00845440bed4248cb80c15128?utm_source=rss&utm_medium=article

----
https://cli.vuejs.org/zh/guide/prototyping.html
https://blog.csdn.net/flyspace/article/details/39993103
https://www.jianshu.com/p/0093c189b0cd
https://www.webascii.cn/article/5ef2cb72071be112473165bc/
https://github.com/vuejs/vue-next
https://qingbii.com/2019/10/10/building-vue3-from-scratch/
https://juejin.im/post/5dd3d4dae51d453d493092da
 