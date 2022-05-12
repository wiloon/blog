---
title: nuxt
author: "-"
date: 2021-11-02 15:12:34
url: nuxt
categories:
  - web
tags:
  - reprint
---
## nuxt

>https://www.nuxtjs.cn/guide/installation

npx create-nuxt-app foo

## 服务端渲染 (SSR）
服务端渲染 (Server-Side Rendering），是指由服务侧完成页面的 HTML 结构拼接的页面处理技术，发送到浏览器，然后为其绑定状态与事件，成为完全可交互页面的过程。
优势: 对SEO友好，减小了http请求次数，加速了页面初次渲染速度

缺点： 不灵活，先后端耦合度过高
SSR 常用于以下两个场景：

有 SEO 诉求，用在搜索引擎检索以及社交分享，用在前台类应用。
首屏渲染时长有要求，常用在移动端、弱网情况下。

## 客户端渲染 (BSR）
前端利用ajax等数据交互手段获取服务端提供的数据以后，渲染到HTML页面。
客户端运行了页面以后才进行json

优势：灵活，真正的先后端分离，方便于先后台各自更新维护后端

缺点： 对SEO不友好，增长了http请求次数，减缓了页面加载速度

## 什么是预渲染
服务端渲染，首先得有后端服务器 (一般是 Node.js）才可以使用，如果我没有后端服务器，也想用在上面提到的两个场景，那么推荐使用预渲染。

预渲染与服务端渲染唯一的不同点在于渲染时机，服务端渲染的时机是在用户访问时执行渲染 (即服务时渲染，数据一般是最新的），预渲染的时机是在项目构建时，当用户访问时，数据不一定是最新的 (如果数据没有实时性，则可以直接考虑预渲染）。

预渲染 (Pre Render）在构建时执行渲染，将渲染后的 HTML 片段生成静态 HTML 文件。无需使用 web 服务器实时动态编译 HTML，适用于静态站点生成。


>https://umijs.org/zh-CN/docs/ssr#%E4%BB%80%E4%B9%88%E6%98%AF%E6%9C%8D%E5%8A%A1%E7%AB%AF%E6%B8%B2%E6%9F%93%EF%BC%9F

###
yarn add echarts vue-echarts
yarn add -D @vue/composition-api
yarn add -D @nuxtjs/composition-api
