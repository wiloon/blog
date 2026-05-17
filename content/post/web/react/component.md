---
title: React 函数组件与类组件
author: "-"
date: 2026-05-17T13:37:34+08:00
lastmod: 2026-05-17T13:37:34+08:00
url: react-component
categories:
  - development
tags:
  - react
  - javascript
  - frontend
  - remix
  - AI-assisted
---

React 有两种组件写法：**函数组件（Function Component）** 和 **类组件（Class Component）**。现代 React 项目几乎全面使用函数组件，类组件属于历史遗留写法。

## 函数组件

函数组件就是一个普通的 JavaScript 函数，接收 Props，返回 JSX。

```jsx
function Greeting({ name }) {
  return <h1>Hello, {name}!</h1>;
}

// 也可以用箭头函数
const Greeting = ({ name }) => <h1>Hello, {name}!</h1>;
```

React 16.8 引入 [Hooks](/react-hooks) 之后，函数组件可以使用状态和生命周期，成为主流写法。

## 类组件

类组件通过继承 `React.Component` 实现，必须定义 `render()` 方法返回 JSX。

```jsx
import { Component } from "react";

class Greeting extends Component {
  render() {
    return <h1>Hello, {this.props.name}!</h1>;
  }
}
```

有状态的类组件：

```jsx
class Counter extends Component {
  constructor(props) {
    super(props);
    this.state = { count: 0 };
  }

  render() {
    return (
      <div>
        <p>计数：{this.state.count}</p>
        <button onClick={() => this.setState({ count: this.state.count + 1 })}>
          +1
        </button>
      </div>
    );
  }
}
```

## 同一功能的对比

以一个带状态的计数器为例，对比两种写法的差异：

**类组件写法：**

```jsx
class Counter extends Component {
  constructor(props) {
    super(props);
    this.state = { count: 0 };
    this.handleClick = this.handleClick.bind(this); // 必须手动绑定 this
  }

  componentDidMount() {
    document.title = `计数：${this.state.count}`;
  }

  componentDidUpdate() {
    document.title = `计数：${this.state.count}`;
  }

  componentWillUnmount() {
    document.title = "App";
  }

  handleClick() {
    this.setState({ count: this.state.count + 1 });
  }

  render() {
    return (
      <button onClick={this.handleClick}>
        计数：{this.state.count}
      </button>
    );
  }
}
```

**函数组件写法：**

```jsx
import { useState, useEffect } from "react";

function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    document.title = `计数：${count}`;
    return () => { document.title = "App"; };
  }, [count]);

  return (
    <button onClick={() => setCount(count + 1)}>
      计数：{count}
    </button>
  );
}
```

两段代码功能完全相同，函数组件明显更简洁。

## 类组件的痛点

### 1. `this` 绑定问题

类组件中事件处理函数需要手动绑定 `this`，否则 `this` 会是 `undefined`。这是 JavaScript 中 `this` 机制导致的，容易出错且写法繁琐。

```jsx
// 必须在 constructor 中绑定，否则出错
this.handleClick = this.handleClick.bind(this);

// 或者用箭头函数定义方法（class fields 语法）
handleClick = () => {
  this.setState({ count: this.state.count + 1 });
};
```

函数组件完全不存在这个问题。

### 2. 生命周期方法把不相关逻辑混在一起

假设组件需要做两件不相关的事：订阅好友状态、开启定时器。

类组件中这两段逻辑会被强制拆散到不同生命周期方法里：

```jsx
componentDidMount() {
  // 逻辑 A：订阅
  subscribeToFriend(this.props.friendId);
  // 逻辑 B：定时器
  this.timer = setInterval(this.tick, 1000);
}

componentWillUnmount() {
  // 逻辑 A 的清理
  unsubscribeFromFriend(this.props.friendId);
  // 逻辑 B 的清理
  clearInterval(this.timer);
}
```

函数组件中可以按逻辑归组，每段逻辑自成一个 `useEffect`，代码可读性更好：

```jsx
// 逻辑 A 独立
useEffect(() => {
  subscribeToFriend(friendId);
  return () => unsubscribeFromFriend(friendId);
}, [friendId]);

// 逻辑 B 独立
useEffect(() => {
  const timer = setInterval(tick, 1000);
  return () => clearInterval(timer);
}, []);
```

### 3. 状态逻辑难以复用

类组件复用状态逻辑只能依赖 HOC（高阶组件）或 Render Props，这两种模式都会导致组件嵌套层级变深，调试困难。

函数组件可以把逻辑提取为**自定义 Hook**，直接在多个组件中调用，不改变组件结构。

```jsx
// 提取为自定义 Hook，任意组件复用
function useWindowSize() {
  const [size, setSize] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    const handler = () =>
      setSize({ width: window.innerWidth, height: window.innerHeight });
    window.addEventListener("resize", handler);
    return () => window.removeEventListener("resize", handler);
  }, []);

  return size;
}
```

## 为什么现在推荐函数组件

| 对比维度            | 函数组件                 | 类组件                                    |
|---------------------|--------------------------|-------------------------------------------|
| 代码量              | 少，简洁                  | 多，模板代码多                             |
| `this` 问题         | 无                       | 需要手动绑定                              |
| 逻辑组织            | 按关注点分组（useEffect）  | 按生命周期强制分散                        |
| 逻辑复用            | 自定义 Hook，灵活         | HOC / Render Props，复杂                   |
| 性能优化            | `React.memo` + `useMemo` | `PureComponent` / `shouldComponentUpdate` |
| React 未来方向      | ✅ 官方主推               | ⚠️ 不再新增特性                           |
| React Compiler 支持 | ✅ 完整支持               | ❌ 不支持                                  |

React 官方在 16.8 之后明确表示：**不会从类组件中移除任何功能，但新特性只会在函数组件中添加**。React 19 的 React Compiler（自动 memoization 优化）也仅支持函数组件。

## 类组件还有用武之地吗

一个例外：**错误边界（Error Boundary）**。

目前错误边界只能用类组件实现，因为对应的生命周期 `componentDidCatch` 和 `getDerivedStateFromError` 尚无 Hook 等价物。

```jsx
class ErrorBoundary extends Component {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error, info) {
    console.error(error, info);
  }

  render() {
    if (this.state.hasError) {
      return <p>页面出错了</p>;
    }
    return this.props.children;
  }
}
```

实际项目中通常直接使用 [react-error-boundary](https://github.com/bvaughn/react-error-boundary) 库，内部封装好了类组件，对外暴露友好的 API，无需自己写类组件。

## 总结

- **新项目**：全面使用函数组件 + Hooks，不写类组件
- **旧项目维护**：遇到类组件不必强制重写，但新增功能优先用函数组件
- **错误边界**：使用 `react-error-boundary` 库代替手写类组件

## 参考资料

- [React 官方文档 - 组件](https://react.dev/learn/your-first-component)
- [React 入门](/react-intro)
- [React Hooks 详解](/react-hooks)
