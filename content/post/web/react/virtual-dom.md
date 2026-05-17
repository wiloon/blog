---
author: "-"
date: 2026-05-17T11:52:39+08:00
lastmod: 2026-05-17T12:01:18+08:00
title: React 虚拟 DOM 与 Diff 算法
url: react-virtual-dom
categories:
  - development
tags:
  - react
  - javascript
  - remix
  - AI-assisted
---

## 什么是虚拟 DOM

虚拟 DOM（Virtual DOM）是用 **JavaScript 对象**来描述真实 DOM 结构的一棵树，存在于内存中，是真实 DOM 的轻量级副本。

## 内存中的实际结构

### React Element

虚拟 DOM 节点是一个普通的 **JavaScript 对象（Plain Object）**，React 内部称它为 **React Element**，由 `React.createElement()` 创建。

```javascript
// 你写的 JSX
const el = <div className="box"><h1>Hello</h1></div>

// Babel 编译后实际执行的
const el = React.createElement(
  'div',
  { className: 'box' },
  React.createElement('h1', null, 'Hello')
)

// 返回的对象结构
{
  $$typeof: Symbol(react.element),  // 防 XSS 的安全标记
  type: 'div',
  key: null,
  ref: null,
  props: {
    className: 'box',
    children: {
      $$typeof: Symbol(react.element),
      type: 'h1',
      key: null,
      ref: null,
      props: { children: 'Hello' },
      _owner: null,
    }
  },
  _owner: null,
}
```

树状结构靠 `props.children` 的引用嵌套形成，多个子节点时 `children` 是一个数组：

```
div (React Element)
└── props.children: [
      h1 (React Element)
      └── props.children: "Hello"
      p (React Element)
      └── props.children: "World"
    ]
```

React Element 只是"描述长什么样"的**不可变快照**，每次渲染都会重新创建，不会长期驻留内存。

## 为什么需要虚拟 DOM

直接操作真实 DOM 代价昂贵，每次访问或修改 DOM，浏览器都要触发完整的渲染流水线：

**样式计算 → 布局（Layout）→ 绘制（Paint）→ 合成（Composite）**

频繁操作 DOM 会导致多次"重排（reflow）"和"重绘（repaint）"，性能开销很大。

虚拟 DOM 的核心思路：**先在内存中计算出最终状态，再一次性以最小代价更新真实 DOM。**

## 工作流程

```
状态变化（setState）
      ↓
生成新的虚拟 DOM 树
      ↓
与旧的虚拟 DOM 树做 Diff（差异比较）
      ↓
找出最小变更集（Patch）
      ↓
一次性更新真实 DOM
```

## Diff 算法

朴素的树 Diff 算法复杂度是 O(n³)，React 通过三个启发式假设将其降低到 **O(n)**：

### 1. 跨层级移动不考虑

不同层级的节点直接删除重建，不做跨层移动匹配。

### 2. 同类型节点才递归比较

节点类型不同（如 `div` → `span`），直接销毁整棵子树并重建，不尝试复用。

### 3. key 优化列表 Diff

列表渲染时，`key` 帮助 React 识别节点身份，区分"移动"和"新增/删除"：

```jsx
// 没有 key：React 按位置比较，插入一项可能导致后续全部重建
<ul>
  <li>Apple</li>
  <li>Banana</li>
</ul>

// 有 key：React 能精确追踪每个节点，只做必要的更新
<ul>
  <li key="1">Apple</li>
  <li key="2">Banana</li>
</ul>
```

**常见错误**：用数组 index 做 key，在列表头部插入时 index 全部变化，Diff 结果和没有 key 一样差。应使用稳定唯一的业务 ID。

## 虚拟 DOM 一定比直接操作 DOM 快吗

不一定，这是常见误区。

| 场景 | 结论 |
| --- | --- |
| 频繁、复杂的状态更新 | 虚拟 DOM 更高效（批量计算后统一更新） |
| 简单的单次 DOM 操作 | 直接操作真实 DOM 反而更快（省去 Diff 开销） |

虚拟 DOM 真正的价值在于：

- **开发体验**：声明式描述 UI，不用手动管理 DOM 操作顺序
- **跨平台**：虚拟 DOM 是平台无关的抽象层，React Native 用同一套机制渲染原生组件

## Fiber 架构（React 16+）

React Element 只是不可变的描述快照，真正在内存里长期存活、用于调度和渲染的是 **Fiber 节点**。每个组件或 DOM 节点都对应一个 Fiber 对象：

```javascript
{
  // 组件信息
  type: 'div',           // 或函数组件、类组件
  key: null,

  // 链表指针（不是数组！）
  return: FiberNode,     // 父节点
  child: FiberNode,      // 第一个子节点
  sibling: FiberNode,    // 右边的兄弟节点

  // 状态和副作用
  memoizedState: ...,    // hooks 链表 / 类组件 state
  memoizedProps: {...},
  pendingProps: {...},
  flags: 0b000010,       // 标记需要插入/更新/删除
  lanes: ...,            // 优先级

  // 双缓冲
  alternate: FiberNode,  // 指向另一棵树的对应节点
}
```

Fiber 树用**链表**而非数组表示子节点：`child` 只指向第一个子节点，兄弟节点通过 `sibling` 串联。这样遍历时可以随时中断并记住当前位置，下次继续——这是并发模式可中断渲染的底层基础。

### 双缓冲机制

React 同时维护**两棵 Fiber 树**：

- `current` 树：当前屏幕上显示的版本
- `workInProgress` 树：正在后台计算的新版本

两棵树的节点通过 `alternate` 互相引用，计算完成后直接切换指针，类似 GPU 渲染里的双缓冲，避免中间状态被用户看到。

```
current tree  ←── alternate ──→  workInProgress tree
     ↑                                    ↓
  屏幕显示                            后台计算中
```

Fiber 让渲染工作可以拆分成小单元，支持**中断和恢复**，为 React 18 的并发特性奠定基础。

## React 18 并发模式

React 18 在 Fiber 基础上引入 Concurrent Mode（并发模式）：

- 渲染可以**中断、暂停、恢复**，不再是同步阻塞的
- 高优先级更新（如用户点击）可以打断低优先级更新（如后台数据渲染）
- 相关 API：`useTransition`、`useDeferredValue`、`startTransition`

```jsx
const [isPending, startTransition] = useTransition();

// 低优先级更新，不阻塞用户交互
startTransition(() => {
  setSearchResults(computeHeavyFilter(input));
});
```

## 小结

| 概念 | 要点 |
| --- | --- |
| 虚拟 DOM | JS 对象描述的 DOM 树，存在于内存 |
| React Element | `React.createElement()` 返回的不可变 Plain Object，每次渲染重新创建 |
| `$$typeof` | Symbol 标记，防止 JSON 注入伪造 React Element |
| Diff 算法 | O(n) 复杂度，三个启发式规则 |
| key | 帮助识别列表节点身份，应使用稳定业务 ID |
| Fiber | 用链表（child/sibling/return）表示树，可中断，支持优先级调度 |
| 双缓冲 | current 树 + workInProgress 树，alternate 互指，渲染完切换指针 |
| 并发模式 | 高优先级任务可打断低优先级渲染 |
