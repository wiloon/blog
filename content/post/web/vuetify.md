---
author: "-"
date: "2021-03-16 16:47:40" 
title: "vuetify"
categories:
  - inbox
tags:
  - reprint
---
## "vuetify"
### 安装相应包
    yarn add @mdi/font -D
    # roboto字体其实不要也行,就英文的一套字体而已
    yarn add typeface-roboto -D

### plugins/vuetify.js
    import Vue from 'vue';
    import Vuetify from 'vuetify/lib';
    import zhHans from 'vuetify/es5/locale/zh-Hans'   // 引入中文语言包
    import 'typeface-roboto/index.css'    // 引入本地的Roboto字体资源
    import '@mdi/font/css/materialdesignicons.css'  // 引入本地的Material Design Icons资源

    Vue.use(Vuetify);

    export default new Vuetify({
      lang:{
        locales: {zhHans},
        current: 'zhHans'
      },
      icons:{
        iconfont: 'mdi',    // 设置使用本地的icon资源
      }
    });

### 模板中使用
    <template>
      
        <v-icon>mdi-account-circle</v-icon>
      </div>
    </template>

    <script>

    export default {
    }
    </script>

### replace google font,mdi font with local resource
注释掉public/index.html中引用的字体

### 颜色
>https://vuetifyjs.com/zh-Hans/styles/colors/#material-82725f698868

---

https://blog.csdn.net/lpwmm/article/details/104659448

