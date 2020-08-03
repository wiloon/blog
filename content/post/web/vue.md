+++
author = ""
date = "2020-05-16T03:03:37Z"
title = "vue"

+++
[https://github.com/vuejs/vue-next](https://github.com/vuejs/vue-next "https://github.com/vuejs/vue-next")

[https://qingbii.com/2019/10/10/building-vue3-from-scratch/](https://qingbii.com/2019/10/10/building-vue3-from-scratch/ "https://qingbii.com/2019/10/10/building-vue3-from-scratch/")

[https://juejin.im/post/5dd3d4dae51d453d493092da](https://juejin.im/post/5dd3d4dae51d453d493092da "https://juejin.im/post/5dd3d4dae51d453d493092da")

```bash

install nodejs
install yarn
yarn global add vue
yarn global remove vue-cli
yarn global add @vue/cli
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