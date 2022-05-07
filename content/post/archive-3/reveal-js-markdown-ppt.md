---
title: 'reveal.js, markdown > PPT'
author: "-"
date: 2019-04-16T16:03:17+00:00
url: /?p=14189
categories:
  - Inbox
tags:
  - reprint
---
## 'reveal.js, markdown > PPT'
### 快捷键

全屏 f , 退出全屏 Esc
上一页 p, 下一页 n/空格
首页 Home, 末页 End
缩略图 Esc 或 o
黑屏 b
演讲提示模式 s
vi导航键: h, j, k, l
  
帮助页面: ?

### 字号

reveal.js的markdown支持4种字号#，##，###，####

# 安装nodejs
sudo pacman -S nodejs
# 安装npm
sudo pacman -S npm
# git clone reveal.js
git clone https://github.com/hakimel/reveal.js.git
cd reveal.js
npm install
mv index.html index.html.bak
ln -s scrum/index.html index.html
npm start
npm start -- --port=8001

    ```xml
<section data-markdown="example.md" data-separator-notes="^Note:" data-charset="UTF-8">
    </section>
``` 

### 内容左对齐

```bash<style>
    .reveal .slides {
        text-align: left;
    }
    .reveal .slides section>* {
        margin-left: 0;
        margin-right: 0;
    }
</style>
```

### 插入图片并控制样式

路径是相对于index.html的路径

```bash![An image](scrum/scrum.png)  <!-- .element height="50%" width="50%" -->
```

### 设备字号

 <br>
```

https://github.com/hakimel/reveal.js/issues/1349

https://github.com/hakimel/reveal.js#markdown