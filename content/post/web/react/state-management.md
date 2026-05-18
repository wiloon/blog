---
title: React 状态管理：Zustand、Jotai 与 Redux 对比
author: "-"
date: 2026-05-18T12:18:47+08:00
lastmod: 2026-05-18T12:18:47+08:00
url: react-state-management
categories:
  - development
tags:
  - react
  - javascript
  - frontend
  - zustand
  - jotai
  - redux
  - remix
  - AI-assisted
---

## 什么是状态管理，它解决什么问题

React 的数据流是单向的：数据通过 Props 从父组件流向子组件。这在小型应用中很好用，但随着应用规模扩大，会遇到两个典型痛点：

**Prop Drilling（属性透传）**

同一份数据需要从顶层组件一层一层往下传，中间层组件本身并不使用这个数据，却不得不接收并转发它。组件层级越深，代码越难维护。

```
App（持有 user 状态）
  └─ Layout
       └─ Sidebar
            └─ UserAvatar（需要 user）← 要传三层 props
```

**跨组件状态同步困难**

当两个没有父子关系的组件需要访问同一份数据时，只能把状态提升到它们共同的祖先组件，然后再层层传下去。状态越分散，同步越容易出 bug。

**状态管理库的解法**

把共享状态提取到组件树之外的独立 **Store**，任何组件都可以直接订阅和修改，不需要层层传递 Props。

```
        Store（独立于组件树）
       ↗         ↗
ComponentA    ComponentB
```

---

## React 主流状态管理方案对比

| 库 | 定位 | 包大小 | 学习曲线 |
| --- | --- | --- | --- |
| **Zustand** | 轻量、直觉式 API | ~1 KB | 低 |
| **Jotai** | 原子化状态，细粒度订阅 | ~3 KB | 低 |
| **Redux Toolkit** | 功能完整，适合大型项目 | ~20 KB | 高 |

---

## Zustand

Zustand 是目前最流行的轻量状态管理库，API 极简，和 Vue 的 Pinia 非常相似。

**创建 Store：**

```js
import { create } from "zustand";

const useCounterStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 }),
}));
```

**在组件中使用：**

```jsx
function Counter() {
  const { count, increment, decrement } = useCounterStore();

  return (
    <div>
      <p>当前计数：{count}</p>
      <button onClick={increment}>+1</button>
      <button onClick={decrement}>-1</button>
    </div>
  );
}
```

**异步操作：**

```js
const useUserStore = create((set) => ({
  user: null,
  loading: false,
  fetchUser: async (id) => {
    set({ loading: true });
    const data = await fetchUserById(id);
    set({ user: data, loading: false });
  },
}));
```

Zustand 不需要 Provider 包裹，Store 是全局单例，直接在任何组件里调用即可。

---

## Jotai

Jotai 采用**原子化（Atom）**的设计思路：把状态拆成最小单元（atom），组件只订阅自己需要的那部分，变更时只有相关组件重渲染，性能更精确。

```js
import { atom, useAtom } from "jotai";

// 定义原子
const countAtom = atom(0);
const nameAtom = atom("Alice");

// 派生原子（类似 computed）
const doubleCountAtom = atom((get) => get(countAtom) * 2);
```

```jsx
function Counter() {
  const [count, setCount] = useAtom(countAtom);

  return (
    <div>
      <p>{count}</p>
      <button onClick={() => setCount((c) => c + 1)}>+1</button>
    </div>
  );
}
```

Jotai 适合状态之间有复杂依赖关系、需要精细控制渲染性能的场景。

---

## Redux Toolkit

Redux 是 React 最老牌的状态管理方案，曾经因为样板代码多而饱受诟病。Redux Toolkit（RTK）是官方推出的简化版，大幅减少了冗余代码。

```js
import { createSlice, configureStore } from "@reduxjs/toolkit";

const counterSlice = createSlice({
  name: "counter",
  initialState: { value: 0 },
  reducers: {
    increment: (state) => { state.value += 1; },
    decrement: (state) => { state.value -= 1; },
  },
});

const store = configureStore({
  reducer: { counter: counterSlice.reducer },
});
```

```jsx
import { useSelector, useDispatch } from "react-redux";

function Counter() {
  const count = useSelector((state) => state.counter.value);
  const dispatch = useDispatch();

  return (
    <button onClick={() => dispatch(counterSlice.actions.increment())}>
      {count}
    </button>
  );
}
```

Redux 的优势在于完善的 DevTools、中间件生态，以及对大型团队友好的严格数据流约束。

---

## React Context + useReducer（内置方案）

不引入第三方库时，可以用 React 内置的 Context + useReducer 组合实现简单的全局状态：

```jsx
const CounterContext = createContext();

function counterReducer(state, action) {
  switch (action.type) {
    case "increment": return { count: state.count + 1 };
    case "decrement": return { count: state.count - 1 };
    default: return state;
  }
}

function CounterProvider({ children }) {
  const [state, dispatch] = useReducer(counterReducer, { count: 0 });
  return (
    <CounterContext.Provider value={{ state, dispatch }}>
      {children}
    </CounterContext.Provider>
  );
}
```

缺点：Context 的每次更新都会导致所有消费者重渲染，大规模使用时性能较差，也缺乏 DevTools 支持。

---

## 如何选型

- **新项目、中小规模** → Zustand，上手快，代码简洁
- **需要细粒度性能优化** → Jotai，原子化订阅避免多余渲染
- **大型企业项目、多人协作** → Redux Toolkit，规范严格，生态完善
- **极简场景（无需第三方依赖）** → React Context，但要注意性能问题

---

## 与 Vue Pinia 的对比

| 特性 | Pinia (Vue) | Zustand (React) |
| --- | --- | --- |
| 定义 Store | `defineStore()` | `create()` |
| 读取状态 | `store.count` | `useStore((s) => s.count)` |
| 修改状态 | 直接赋值 / action | `set()` 函数 |
| 异步 action | 直接 async 函数 | 直接 async 函数 |
| DevTools | ✅ Vue DevTools | ✅ Redux DevTools（可选插件） |
| Provider 包裹 | 不需要 | 不需要 |

两者设计理念非常接近，从 Pinia 切换到 Zustand 的学习成本很低。

---

## 参考资料

- [Zustand 官方文档](https://zustand-demo.pmnd.rs)
- [Jotai 官方文档](https://jotai.org)
- [Redux Toolkit 官方文档](https://redux-toolkit.js.org)
