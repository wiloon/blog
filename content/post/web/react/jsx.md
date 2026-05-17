---
author: "-"
date: 2026-05-17T12:10:35+08:00
lastmod: 2026-05-17T12:22:03+08:00
title: JSX 是什么
url: jsx
categories:
  - development
tags:
  - react
  - javascript
  - jsx
  - remix
  - AI-assisted
---

## JSX 解决了什么问题

在 JSX 出现之前，用 JavaScript 描述 UI 结构需要这样写：

```javascript
const el = React.createElement(
  'div',
  { className: 'card' },
  React.createElement('h2', null, title),
  React.createElement('p', null, content),
  React.createElement('button', { onClick: handleClick }, '确认')
);
```

嵌套稍深就几乎无法阅读。而人类天然擅长读 HTML 这种树形标签结构。

JSX 解决的核心问题是：**让 UI 结构可视化，让开发者用熟悉的标签思维描述界面，同时保留 JavaScript 的全部表达能力。**

```jsx
// JSX 版本，结构一目了然
const el = (
  <div className="card">
    <h2>{title}</h2>
    <p>{content}</p>
    <button onClick={handleClick}>确认</button>
  </div>
);
```

## JSX 是什么

JSX（JavaScript XML）是一种 **JavaScript 的语法扩展**，允许在 JS 代码里直接写类似 HTML 的标签。

它既不是真正的 HTML，也不是模板引擎，而是 `React.createElement()` 的语法糖。浏览器不认识 JSX，需要由 Babel 等编译工具在构建阶段将其转换为普通 JavaScript。

```jsx
// 你写的 JSX
const element = <h1 className="title">Hello, {name}</h1>;

// Babel 编译后（React 17 之前）
const element = React.createElement(
  'h1',
  { className: 'title' },
  'Hello, ',
  name
);

// Babel 编译后（React 17+ 新 JSX Transform）
import { jsx as _jsx } from 'react/jsx-runtime';
const element = _jsx('h1', { className: 'title', children: ['Hello, ', name] });
```

React 17 之后引入了新的 JSX Transform，编译器自动引入 `react/jsx-runtime`，不再需要在每个文件顶部写 `import React from 'react'`。

## JSX 的核心规则

### 必须有一个根元素

```jsx
// 错误：多个根元素
return <h1>Title</h1><p>text</p>

// 正确：用 Fragment 包裹，不产生真实 DOM 节点
return (
  <>
    <h1>Title</h1>
    <p>text</p>
  </>
)
```

### 用 `{}` 嵌入 JavaScript 表达式

```jsx
<div>
  <p>{name}</p>
  <p>{isLoggedIn ? '已登录' : '未登录'}</p>
  <p>{items.length > 0 && <List items={items} />}</p>
</div>
```

`{}` 里只能放**表达式**（有返回值），不能放语句（`if`、`for` 等）。

### 属性名用驼峰命名

JSX 最终转成 JS 对象，HTML 属性名中有 JS 保留字的要重命名：

| HTML 属性 | JSX 属性 |
| --- | --- |
| `class` | `className` |
| `for` | `htmlFor` |
| `onclick` | `onClick` |
| `tabindex` | `tabIndex` |

内联样式用对象而非字符串：

```jsx
// HTML
<div style="color: red; font-size: 14px">

// JSX
<div style={{ color: 'red', fontSize: '14px' }}>
```

### 标签必须关闭

```jsx
// 错误
<input type="text">
<br>

// 正确
<input type="text" />
<br />
```

### 大写开头表示自定义组件

```jsx
// 小写 → 原生 DOM 元素
<div>  <span>  <input />

// 大写 → 自定义 React 组件
<Button />
<UserCard name="Alice" age={30} />
```

## JSX 不是模板语言

Vue、Angular 的模板有专属指令（`v-if`、`v-for`、`*ngIf`、`*ngFor`），JSX 没有，**完全用 JavaScript 原生语法处理逻辑**：

```jsx
// 条件渲染
{isLoggedIn ? <UserPanel /> : <LoginButton />}
{hasError && <ErrorMessage text={error} />}

// 列表渲染
{items.map(item => (
  <li key={item.id}>{item.name}</li>
))}
```

这意味着 JSX 的能力上限就是 JavaScript 本身，不受模板指令集限制。

## JSX 是 React 独有的吗

不是。JSX 是 Facebook（Meta）提出的开放规范，任何工具都可以实现对它的支持。目前使用 JSX 的场景：

### 使用 JSX 的框架和工具

| 框架 / 工具 | JSX 支持情况 |
| --- | --- |
| **React** | 最主要的使用者，JSX 事实上因 React 而普及 |
| **Preact** | React 的轻量替代，完全兼容 JSX |
| **Solid.js** | 使用 JSX，但编译策略不同，不生成虚拟 DOM |
| **Inferno** | 高性能 React-like 库，使用 JSX |
| **Stencil** | Web Components 框架，支持 JSX |
| **Qwik** | 新兴框架，使用 JSX |

### 不使用 JSX 的主流框架

| 框架 | 模板方案 |
| --- | --- |
| **Vue** | 单文件组件 `.vue`（`<template>` 标签），也可选用 JSX |
| **Angular** | HTML 模板 + 指令（`*ngIf`、`*ngFor`） |
| **Svelte** | 编译型模板，语法最接近原生 HTML |

Vue 虽然默认用 `<template>`，但官方支持 JSX，可以用 `render()` 函数配合 JSX 写复杂组件逻辑，常见于组件库开发（如 Element Plus 部分组件）。

## JSX 与 Solid.js 的差异——JSX 不等于虚拟 DOM

一个常见误解是"用了 JSX 就是在用虚拟 DOM"，Solid.js 打破了这个假设。

Solid.js 同样使用 JSX，但编译器直接生成**操作真实 DOM 的指令**，完全跳过虚拟 DOM 的创建和 Diff 过程，性能比 React 更高：

```jsx
// 同样的 JSX 写法
const App = () => <h1>Hello, {name()}</h1>;

// React 编译 → 生成虚拟 DOM → Diff → 更新真实 DOM
// Solid 编译 → 直接生成 DOM 操作代码，name() 变化时精准更新对应文本节点
```

这说明 JSX 只是**语法层面的约定**，具体的运行时行为由各框架的编译器和运行时决定。

## 小结

| 维度 | 说明 |
| --- | --- |
| 本质 | JavaScript 语法扩展，`React.createElement()` 的语法糖 |
| 解决的问题 | 让 UI 结构可视化，兼顾 HTML 的可读性和 JS 的表达力 |
| 是否 React 独有 | 否，Preact / Solid / Qwik 等均支持；Vue 也可选用 |
| 是否等于虚拟 DOM | 否，JSX 只是语法，虚拟 DOM 是 React 的运行时实现 |
| 编译工具 | Babel、SWC、esbuild 等均可处理 JSX |

## JSX 和 JSP 的对比

JSX 和 JSP（JavaServer Pages）名字相近，表面上都是"把两种语言混写在一起"，但本质上走了完全相反的方向。

### 表面相似

```jsp
<%-- JSP：HTML 里嵌 Java --%>
<html>
  <body>
    <h1>Hello, <%= user.getName() %></h1>
    <% for (Item item : items) { %>
      <li><%= item.getName() %></li>
    <% } %>
  </body>
</html>
```

```jsx
{/* JSX：JS 里嵌 HTML */}
<div>
  <h1>Hello, {user.name}</h1>
  {items.map(item => <li key={item.id}>{item.name}</li>)}
</div>
```

### 方向完全相反

| 维度 | JSP | JSX |
| --- | --- | --- |
| 宿主语言 | HTML（嵌入 Java） | JavaScript（嵌入 HTML） |
| 运行时机 | 服务端，运行时解释执行 | 客户端，构建时编译为 JS |
| 产物 | 生成 HTML 字符串推给浏览器 | 生成 JS 对象（虚拟 DOM） |
| 状态管理 | 无状态，每次请求重新渲染整页 | 有状态，局部更新 DOM |
| 混写评价 | 被认为是反模式（逻辑污染视图） | 被认为是正确封装（组件内聚） |

### 为什么 JSP 被抛弃，JSX 被接受

JSP 的问题是**分离不彻底**：HTML 模板里散落着 Java 业务逻辑，`<% %>` 里什么都能写，导致 Controller 逻辑泄漏进 View，最终一团乱麻。后来的解决思路是 **MVC 分离**，模板只负责渲染，于是有了 Thymeleaf、Freemarker 这类"无逻辑模板"。

React/JSX 的思路正好转了 180 度——**不按 MVC 分层，按组件封装**。一个 `<UserCard>` 组件把自己的 HTML 结构、交互逻辑、局部状态全部封装在一起，组件内部高度内聚，组件之间相互隔离：

```
MVC 思路（横向切割）          React 思路（纵向封装）

  View  (HTML 模板)           ┌─────────────┐
  ──────────────              │  UserCard   │
  Controller (逻辑)           │  - 结构(JSX)│
  ──────────────              │  - 逻辑(JS) │
  Model (数据)                │  - 样式(CSS)│
                              └─────────────┘
```

JSX 的"混写"是**有边界的混写**——只混在同一个组件内部，组件本身就是封装单元，这与 JSP 把逻辑散落在全局模板中有本质区别。

**一句话**：JSP 是服务端把 Java 塞进 HTML，最终输出字符串；JSX 是把 HTML 塞进 JavaScript，最终输出组件对象。前者是历史包袱，后者是架构理念从分层到组件化的演进。
