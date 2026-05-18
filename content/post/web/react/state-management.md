---
title: React 状态管理：Zustand、Jotai 与 Redux 对比
author: "-"
date: 2026-05-18T12:18:47+08:00
lastmod: 2026-05-18T12:43:00+08:00
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

| 库                | 定位                  | 包大小 | 学习曲线 |
|-------------------|-----------------------|--------|----------|
| **Zustand**       | 轻量、直觉式 API       | ~1 KB  | 低       |
| **Jotai**         | 原子化状态，细粒度订阅 | ~3 KB  | 低       |
| **Redux Toolkit** | 功能完整，适合大型项目 | ~20 KB | 高       |

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

### 状态存在哪里

Jotai（以及 Zustand、Redux）默认把状态存在**浏览器内存**里，本质是"有订阅能力的全局变量"：

- 页面刷新 → 状态重置为初始值
- 关闭标签页 → 销毁
- 不同标签页 → 互相隔离，不共享

需要持久化时，使用 `atomWithStorage` 显式接入存储后端：

```js
import { atomWithStorage } from "jotai/utils";

// 存到 localStorage（刷新后仍保留）
const themeAtom = atomWithStorage("theme", "light");

// 存到 sessionStorage（关闭标签页后清除）
const tokenAtom = atomWithStorage("token", null, sessionStorage);
```

Zustand 用 `persist` 中间件实现同样效果：

```js
import { persist } from "zustand/middleware";

const useStore = create(
  persist(
    (set) => ({ theme: "light", setTheme: (t) => set({ theme: t }) }),
    { name: "app-settings" } // localStorage key
  )
);
```

各存储位置对比：

| 存储位置 | 生命周期 | 容量 | 典型用途 |
|---|---|---|---|
| **内存（默认）** | 刷新即丢失 | 无限制 | 弹窗状态、筛选条件、购物车 |
| **localStorage** | 永久（手动清除前） | ~5MB | 主题、语言偏好、用户设置 |
| **sessionStorage** | 关闭标签页清除 | ~5MB | 临时 token、表单草稿 |
| **IndexedDB** | 永久，大容量 | 几百MB+ | 离线缓存、大量结构化数据 |
| **Cookie** | 可设过期时间 | ~4KB | 认证 token（随请求发给服务端） |

### 与后端单例模式的对比

前端状态管理库的本质和后端**单例对象共享状态**思路一致：atom 文件定义在模块顶层，JS 模块系统天然是单例的，不同组件 import 同一个 atom 拿到的是同一个引用。

```js
// store/counter.js —— 定义一次，全局共享
export const countAtom = atom(0);
```

```js
// ComponentA.jsx
import { countAtom } from "../store/counter";
const [count, setCount] = useAtom(countAtom); // 订阅同一个 atom
```

```js
// ComponentB.jsx
import { countAtom } from "../store/counter";
const [count, setCount] = useAtom(countAtom); // 状态共享，A 改了 B 自动更新
```

与后端单例的区别在于多了一层**响应式订阅**：atom 变化时自动推送给所有订阅者，不需要主动轮询。

> 可以把状态管理库理解为：**JS 模块单例** + **发布订阅（Pub/Sub）**

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

## 如何选型

- **新项目、中小规模** → Zustand，上手快，代码简洁
- **需要细粒度性能优化** → Jotai，原子化订阅避免多余渲染
- **大型企业项目、多人协作** → Redux Toolkit，规范严格，生态完善
- **极简场景（无需第三方依赖）** → React Context，但要注意性能问题

---

## 与 Vue Pinia 的对比

| 特性          | Pinia (Vue)       | Zustand (React)            |
|---------------|-------------------|----------------------------|
| 定义 Store    | `defineStore()`   | `create()`                 |
| 读取状态      | `store.count`     | `useStore((s) => s.count)` |
| 修改状态      | 直接赋值 / action | `set()` 函数               |
| 异步 action   | 直接 async 函数   | 直接 async 函数            |
| DevTools      | ✅ Vue DevTools    | ✅ Redux DevTools（可选插件） |
| Provider 包裹 | 不需要            | 不需要                     |

两者设计理念非常接近，从 Pinia 切换到 Zustand 的学习成本很低。

---

## 与 Java 后端的对比

Java 后端没有专门的"状态管理"分类，因为**后端天然倾向于无状态设计**——状态通常外置到数据库或 Redis，而不是放在进程内存里。但 Jotai 的两个核心能力在 Java 里都有对应：

**单例共享（对应 Jotai 的模块单例部分）**

Spring Bean 默认就是单例，注入到哪里拿到的都是同一个对象：

```java
@Service  // 默认单例，全局共享
public class CounterService {
    private int count = 0;
    public void increment() { count++; }
    public int getCount() { return count; }
}
```

**响应式订阅（对应 Jotai 的 Pub/Sub 部分）**

Spring 内置事件系统：

```java
// 发布
applicationEventPublisher.publishEvent(new CountChangedEvent(newCount));

// 订阅
@EventListener
public void onCountChanged(CountChangedEvent event) { ... }
```

最接近 Jotai atom 的是 **RxJava 的 `BehaviorSubject`**，它持有当前值并在值变化时通知所有订阅者：

```java
// 定义状态（类比 atom）
BehaviorSubject<Integer> countState = BehaviorSubject.createDefault(0);

// 修改（类比 setCount）
countState.onNext(countState.getValue() + 1);

// 订阅（类比 useAtom）
countState.subscribe(count -> System.out.println("count: " + count));
```

**为什么后端没有专门的状态管理库**

| 维度 | 前端 | 后端 |
|---|---|---|
| 状态生命周期 | 跟随浏览器页面 | 跟随进程（可能随时重启） |
| 多实例 | 单个页面，状态天然集中 | 水平扩展多实例，进程内状态无法跨实例共享 |
| 状态持久化 | localStorage / IndexedDB | 数据库 / Redis |
| 状态同步 | 组件间（同一进程） | 服务间（跨进程/跨机器） |

后端一旦水平扩展，进程内存里的状态每个实例各自一份，互相不同步，所以共享状态直接存 Redis，不依赖进程内存。

**概念对照表**

| Jotai | Java 对应 |
|---|---|
| atom（单例状态） | Spring Bean（单例） |
| `useAtom`（订阅） | `@EventListener` / RxJava `subscribe` |
| 派生 atom（computed） | RxJava `map` / `combineLatest` |
| `atomWithStorage` | Redis / JPA |
| Jotai 整体 | RxJava `BehaviorSubject` 最接近 |

---

## 参考资料

- [Zustand 官方文档](https://zustand-demo.pmnd.rs)
- [Jotai 官方文档](https://jotai.org)
- [Redux Toolkit 官方文档](https://redux-toolkit.js.org)
