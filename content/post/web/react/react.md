---
title: React 入门
author: "-"
date: 2026-05-17T13:28:28+08:00
lastmod: 2026-06-16T19:10:45+08:00
url: react-intro
categories:
  - development
tags:
  - AI-assisted
  - frontend
  - javascript
  - react
  - remix
---

React 是由 Meta（前 Facebook）开发并开源的 JavaScript UI 库，专注于构建用户界面。它于 2013 年开源，目前已成为最流行的前端技术之一。

## react 核心概念

### 组件（Component）

React 的核心单元是**组件（Component）**。组件是一个返回 UI 描述的函数（或类），可以像拼积木一样组合成复杂的界面。

```jsx
function Greeting({ name }) {
  return <h1>Hello, {name}!</h1>;
}
```

组件分为两类：

- **函数组件**：现代 React 的主流写法，配合 Hooks 使用
- **类组件**：早期写法，新项目不推荐使用

### JSX

JSX 是 JavaScript 的语法扩展，允许在 JS 文件中写类似 HTML 的结构。它不是 HTML，会被编译工具（如 Babel、SWC）编译为 `React.createElement()` 调用。

```jsx
const element = <div className="container">Hello</div>;

// 编译后等价于：
const element = React.createElement("div", { className: "container" }, "Hello");
```

详见：[JSX 介绍](./jsx.md)

### Props

Props（属性）是组件的输入，由父组件传入，在子组件内部是**只读的**。

```jsx
function Button({ label, onClick }) {
  return <button onClick={onClick}>{label}</button>;
}

// 使用
<Button label="提交" onClick={() => console.log("clicked")} />
```

### State

State（状态）是组件内部管理的可变数据。状态变化会触发组件重新渲染。

```jsx
import { useState } from "react";

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>当前计数：{count}</p>
      <button onClick={() => setCount(count + 1)}>+1</button>
    </div>
  );
}
```

### 虚拟 DOM

React 在内存中维护一棵虚拟 DOM 树。每次状态更新时，React 通过 **Diffing 算法**对比新旧虚拟 DOM，计算出最小变更集，再批量更新真实 DOM，从而提升性能。

详见：[Virtual DOM](./virtual-dom.md)

## Hooks

Hooks 是 React 16.8 引入的特性，让函数组件也能使用状态和生命周期功能。

### useState

管理局部状态。

```jsx
const [value, setValue] = useState(initialValue);
```

### useEffect

处理副作用（如数据请求、订阅、手动 DOM 操作）。

```jsx
useEffect(() => {
  // 副作用逻辑
  fetchData();

  return () => {
    // 清理函数（组件卸载时执行）
  };
}, [dependency]); // 依赖数组
```

依赖数组规则：

- 省略 → 每次渲染后都执行
- `[]` → 只在挂载时执行一次
- `[a, b]` → `a` 或 `b` 变化时执行

### useContext

订阅 React Context，用于跨组件层级传递数据（避免 prop drilling）。

```jsx
const theme = useContext(ThemeContext);
```

### useRef

持有一个可变引用，变更不触发重渲染。常用于访问 DOM 元素或保存不需要渲染的值。

```jsx
const inputRef = useRef(null);

// 访问 DOM
inputRef.current.focus();
```

### useMemo / useCallback

用于性能优化，缓存计算结果或函数引用，避免不必要的重计算和子组件重渲染。

```jsx
const result = useMemo(() => expensiveCalc(a, b), [a, b]);
const handleClick = useCallback(() => doSomething(id), [id]);
```

## 数据流

React 遵循**单向数据流**：数据从父组件通过 Props 流向子组件，子组件通过回调函数向父组件传递事件。

```
父组件 → props → 子组件
子组件 → callback → 父组件
```

当多个组件需要共享状态时，通常将状态**提升**到最近的公共父组件，或使用 Context / 状态管理库（如 Jotai、Zustand、Redux）。

## 生命周期

函数组件通过 `useEffect` 模拟类组件的生命周期阶段：

| 生命周期 | 类组件                 | 函数组件                     |
| -------- | ---------------------- | ---------------------------- |
| 挂载后   | `componentDidMount`    | `useEffect(() => {}, [])`    |
| 更新后   | `componentDidUpdate`   | `useEffect(() => {}, [dep])` |
| 卸载前   | `componentWillUnmount` | `useEffect` 返回的清理函数   |

## 与框架的关系

React 本身只是 UI 库，不包含路由、数据请求、SSR 等能力。实际项目通常搭配框架使用：

| 框架                               | 特点                                        |
| ---------------------------------- | ------------------------------------------- |
| [Next.js](https://nextjs.org)      | 生产首选，支持 SSR / SSG / RSC，Vercel 出品 |
| [Remix](https://remix.run)         | 以 Web 标准为中心，强调服务端渲染           |
| [Vite + React](https://vitejs.dev) | 纯 SPA，构建快，适合后台管理系统            |

## React 与 ReactJS 的关系

React 和 ReactJS 是同一个东西，只是叫法不同。**React** 是 Meta（前 Facebook）在 2013 年开源时的官方名称；**ReactJS** 是早期社区的非正式叫法，加 "JS" 后缀是为了与其他同名项目区分。现在官方文档、npm 包（`react`）、GitHub 仓库全部统一使用 **React**，ReactJS 这一叫法已逐渐淡出。

## 版本演进

| 版本  | 年份      | 关键变化                                                                              |
| ----- | --------- | ------------------------------------------------------------------------------------- |
| 0.x   | 2013–2015 | 早期版本，JSX 还在实验阶段                                                            |
| v15   | 2016      | 稳定期，广泛采用                                                                      |
| v16   | 2017      | 重写核心（Fiber 架构），引入 Error Boundary                                           |
| v16.8 | 2019      | **Hooks** 正式发布，是最重大的 API 转折点，社区全面转向函数式组件                     |
| v17   | 2020      | 过渡版，无新特性，主要改善升级体验                                                    |
| v18   | 2022      | 并发模式（Concurrent Features）、`useTransition`、自动批处理                          |
| v19   | 2024      | React Compiler（自动 memoization）、Server Components 稳定、Actions API、`use()` hook |

v16.8（Hooks）是最关键的分界线：之前以 Class 组件为主，之后社区全面转向函数式组件 + Hooks 写法。

## 参考资料

- [React 官方文档](https://react.dev)
- [React GitHub](https://github.com/facebook/react)
