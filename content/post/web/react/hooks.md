---
title: React Hooks 详解
author: "-"
date: 2026-05-17T13:33:22+08:00
lastmod: 2026-05-17T13:33:22+08:00
url: react-hooks
categories:
  - development
tags:
  - react
  - hooks
  - javascript
  - frontend
  - remix
  - AI-assisted
---

Hook 是 React 16.8 引入的一类特殊函数，命名以 `use` 开头。它让函数组件拥有了原本只有类组件才有的能力：**状态管理、生命周期、跨组件共享逻辑**。

## 为什么需要 Hook

React 16.8 之前，函数组件只能做纯渲染，没有状态、没有生命周期。要用这些功能必须写类组件，但类组件存在几个痛点：

- `this` 绑定容易出错
- 生命周期方法（`componentDidMount` / `componentDidUpdate`）把不相关的逻辑强行塞在一起
- 状态逻辑难以在组件之间复用

Hook 彻底解决了这些问题，现代 React 项目基本全面使用函数组件 + Hook。

## Hook 使用规则

> 这两条规则必须严格遵守，否则会导致 Bug。

1. **只在函数组件或自定义 Hook 的顶层调用 Hook**，不能在条件语句、循环、嵌套函数中调用
2. **只在 React 函数中调用 Hook**，不能在普通 JS 函数中调用

```jsx
// ❌ 错误：在条件语句中调用
if (condition) {
  const [value, setValue] = useState(0);
}

// ✅ 正确：在顶层调用
const [value, setValue] = useState(0);
if (condition) {
  setValue(1);
}
```

## 内置 Hook

### useState

管理组件的局部状态。

```jsx
const [state, setState] = useState(initialValue);
```

- `state`：当前状态值
- `setState`：更新状态的函数，调用后触发重渲染
- `initialValue`：初始值，也可以传入一个函数（懒初始化）

```jsx
import { useState } from "react";

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>计数：{count}</p>
      <button onClick={() => setCount(count + 1)}>+1</button>
      <button onClick={() => setCount(prev => prev - 1)}>-1</button>
    </div>
  );
}
```

**函数式更新**：当新状态依赖上一个状态时，推荐传函数给 `setState`，避免闭包陷阱：

```jsx
setCount(prev => prev + 1); // ✅ 推荐
setCount(count + 1);        // ⚠️ 在异步场景可能拿到旧值
```

---

### useEffect

处理副作用：数据请求、事件订阅、手动操作 DOM、定时器等。

```jsx
useEffect(() => {
  // 副作用逻辑

  return () => {
    // 清理函数（可选），在组件卸载或下次 effect 执行前调用
  };
}, [dependency1, dependency2]);
```

**依赖数组控制执行时机：**

| 写法 | 执行时机 |
| --- | --- |
| 省略依赖数组 | 每次渲染后都执行 |
| `[]` | 只在组件挂载时执行一次 |
| `[a, b]` | 挂载时 + `a` 或 `b` 变化时执行 |

```jsx
useEffect(() => {
  document.title = `计数：${count}`;
}, [count]); // count 变化时更新标题
```

```jsx
useEffect(() => {
  const timer = setInterval(() => {
    console.log("tick");
  }, 1000);

  return () => clearInterval(timer); // 清理定时器
}, []);
```

**常见错误：遗漏依赖**

```jsx
// ❌ 错误：count 没加入依赖，始终读到初始值 0
useEffect(() => {
  console.log(count);
}, []);

// ✅ 正确
useEffect(() => {
  console.log(count);
}, [count]);
```

---

### useContext

读取 React Context 的值，实现跨层级组件通信，避免逐层传递 Props（prop drilling）。

```jsx
const value = useContext(MyContext);
```

```jsx
// 1. 创建 Context
const ThemeContext = React.createContext("light");

// 2. 提供 Context（通常在顶层组件）
function App() {
  return (
    <ThemeContext.Provider value="dark">
      <Page />
    </ThemeContext.Provider>
  );
}

// 3. 任意子组件消费
function Button() {
  const theme = useContext(ThemeContext);
  return <button className={theme}>Click</button>;
}
```

---

### useRef

持有一个在渲染之间保持稳定的可变引用，**修改 `.current` 不触发重渲染**。

```jsx
const ref = useRef(initialValue);
// ref.current === initialValue
```

**用途 1：访问 DOM 元素**

```jsx
function FocusInput() {
  const inputRef = useRef(null);

  return (
    <>
      <input ref={inputRef} />
      <button onClick={() => inputRef.current.focus()}>聚焦</button>
    </>
  );
}
```

**用途 2：保存不需要触发渲染的值**（如定时器 ID、上一次的值）

```jsx
function Timer() {
  const timerRef = useRef(null);

  const start = () => {
    timerRef.current = setInterval(() => console.log("tick"), 1000);
  };

  const stop = () => clearInterval(timerRef.current);

  return (
    <>
      <button onClick={start}>开始</button>
      <button onClick={stop}>停止</button>
    </>
  );
}
```

---

### useMemo

缓存**计算结果**，只有依赖变化时才重新计算，避免每次渲染都执行昂贵的计算。

```jsx
const result = useMemo(() => expensiveCalculation(a, b), [a, b]);
```

```jsx
function ProductList({ products, filter }) {
  const filtered = useMemo(
    () => products.filter(p => p.category === filter),
    [products, filter]
  );

  return filtered.map(p => <Product key={p.id} {...p} />);
}
```

> 不要过度使用 `useMemo`。只在计算确实耗时时使用，否则反而增加开销。

---

### useCallback

缓存**函数引用**，只有依赖变化时才返回新函数。常配合 `React.memo` 使用，避免子组件因函数引用变化而不必要地重渲染。

```jsx
const handleClick = useCallback(() => {
  doSomething(id);
}, [id]);
```

```jsx
// 子组件用 React.memo 包裹，只有 props 变化才重渲染
const Button = React.memo(({ onClick, label }) => {
  return <button onClick={onClick}>{label}</button>;
});

function Parent({ id }) {
  // 没有 useCallback：每次 Parent 渲染都生成新函数 → Button 总是重渲染
  // 有 useCallback：id 不变时函数引用稳定 → Button 不重渲染
  const handleClick = useCallback(() => {
    console.log(id);
  }, [id]);

  return <Button onClick={handleClick} label="点击" />;
}
```

---

### useReducer

`useState` 的替代方案，适合**状态逻辑复杂**或**多个子状态相互关联**的场景。思路与 Redux 类似。

```jsx
const [state, dispatch] = useReducer(reducer, initialState);
```

```jsx
function reducer(state, action) {
  switch (action.type) {
    case "increment":
      return { count: state.count + 1 };
    case "decrement":
      return { count: state.count - 1 };
    case "reset":
      return { count: 0 };
    default:
      throw new Error("未知 action");
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, { count: 0 });

  return (
    <div>
      <p>计数：{state.count}</p>
      <button onClick={() => dispatch({ type: "increment" })}>+1</button>
      <button onClick={() => dispatch({ type: "decrement" })}>-1</button>
      <button onClick={() => dispatch({ type: "reset" })}>重置</button>
    </div>
  );
}
```

---

### useLayoutEffect

与 `useEffect` 用法相同，但执行时机不同：

| Hook | 执行时机 |
| --- | --- |
| `useEffect` | 浏览器完成绘制**之后**（异步） |
| `useLayoutEffect` | DOM 更新完成、浏览器绘制**之前**（同步） |

适用场景：需要在浏览器绘制前读取/修改 DOM（如测量元素尺寸、避免闪烁）。大多数情况优先使用 `useEffect`。

---

## 自定义 Hook

自定义 Hook 是将可复用的状态逻辑提取成独立函数的方式，函数名以 `use` 开头。

```jsx
// 自定义 Hook：封装数据请求逻辑
function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch(url)
      .then(res => res.json())
      .then(data => {
        setData(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err);
        setLoading(false);
      });
  }, [url]);

  return { data, loading, error };
}

// 在任意组件中复用
function UserProfile({ userId }) {
  const { data, loading, error } = useFetch(`/api/users/${userId}`);

  if (loading) return <p>加载中...</p>;
  if (error) return <p>出错了</p>;
  return <p>{data.name}</p>;
}
```

自定义 Hook 的优势：

- 逻辑与 UI 分离，组件代码更清晰
- 同一逻辑在多个组件中复用，不需要 HOC 或 Render Props
- 便于单独测试

## Hook 对比类组件生命周期

| 类组件 | Hook 等价写法 |
| --- | --- |
| `componentDidMount` | `useEffect(() => {}, [])` |
| `componentDidUpdate` | `useEffect(() => {}, [dep])` |
| `componentWillUnmount` | `useEffect` 返回的清理函数 |
| `shouldComponentUpdate` | `React.memo` + `useMemo` / `useCallback` |

## 参考资料

- [React 官方文档 - Hooks](https://react.dev/reference/react/hooks)
- [React 入门](/react-intro)
