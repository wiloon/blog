---
author: "-"
date: "2021-04-23 16:49:36" 
title: "后退按钮"
categories:
  - inbox
tags:
  - reprint
---
## "后退按钮"

### vue
    methods: {
        goBack(){
        let state = {
            title: '',
            url: window.location.href
        };
        window.history.pushState(state, state.title, state.url);
        }
    },
    mounted() {
        if (window.history && window.history.pushState) {
        history.pushState(null, null, document.URL); //这里有没有都无所谓，最好是有以防万一
        window.addEventListener('popstate', this.goBack, false);
        // 回退时执行goback方法
        }
    },
    // 页面销毁时，取消监听。否则其他vue路由页面也会被监听
    destroyed(){
        window.removeEventListener('popstate', this.goBack, false);
    }

---

https://www.jianshu.com/p/9ee6be02d687  
https://blog.csdn.net/qq_34179086/article/details/88081575  