---
title: TypeScript
author: "-"
date: 2015-06-13T00:22:45+00:00
lastmod: 2026-05-17T18:13:59+08:00
url: typescript
categories:
  - language
tags:
  - typescript
  - javascript
  - remix
  - AI-assisted

aliases:
  - /p7806/
---

## JavaScript vs TypeScript 对比

同样的用户问候功能，JS 和 TS 写法对比：

```javascript
// JavaScript 版本
function greetUser(user) {
  return "Hello, " + user.name + "! You are " + user.age + " years old.";
}

const user = { name: "Alice", age: 25 };
console.log(greetUser(user));        // Hello, Alice! You are 25 years old.
console.log(greetUser({ name: 42 })); // 不报错，但输出结果异常：Hello, 42! You are undefined years old.
```

```typescript
// TypeScript 版本
interface User {
  name: string;
  age: number;
}

function greetUser(user: User): string {
  return `Hello, ${user.name}! You are ${user.age} years old.`;
}

const user: User = { name: "Alice", age: 25 };
console.log(greetUser(user));         // Hello, Alice! You are 25 years old.
console.log(greetUser({ name: 42 })); // ❌ 编译错误：name 应为 string，不能传 number
```

TypeScript 在**编写代码时**就能发现类型错误，而不是等到运行时出现奇怪的 bug。

---

TypeScript 是微软开发的开源编程语言，是 JavaScript 的**超集**——所有合法的 JS 代码都是合法的 TS 代码。TypeScript 在 JS 的基础上增加了静态类型系统，最终仍需编译为 JavaScript 才能在浏览器或 Node.js 中运行。

## 为什么用 TypeScript

- **静态类型检查**：在编译阶段发现类型错误，而不是等到运行时
- **更好的 IDE 支持**：自动补全、重构、跳转定义
- **可维护性**：类型即文档，大型项目协作更清晰
- **渐进迁移**：可以逐步从 JS 迁移，无需一次性重写

## 基本类型

```typescript
let num: number = 100;
let str: string = "hello";
let flag: boolean = true;
let arr: number[] = [1, 2, 3];
let tuple: [string, number] = ["Alice", 25];

// 联合类型
let id: string | number = "abc";

// 字面量类型
let direction: "left" | "right" | "up" | "down" = "left";

// any（尽量避免）
let anything: any = 42;

// unknown（比 any 更安全）
let value: unknown = "hello";
```

## 函数类型

```typescript
function add(a: number, b: number): number {
  return a + b;
}

// 可选参数
function greet(name: string, age?: number): string {
  return age ? `${name}, ${age}` : name;
}

// 箭头函数
const multiply = (a: number, b: number): number => a * b;
```

## interface 和 type

```typescript
// interface：定义对象结构，支持继承和扩展
interface User {
  id: number;
  name: string;
  email?: string;  // 可选字段
}

// type：更灵活，可定义联合类型、交叉类型等
type Status = "active" | "inactive" | "pending";
type AdminUser = User & { role: "admin" };
```

## 泛型

```typescript
// 泛型函数
function identity<T>(value: T): T {
  return value;
}

// 泛型接口
interface ApiResponse<T> {
  data: T;
  status: number;
  message: string;
}

// 使用
const response: ApiResponse<User[]> = {
  data: [],
  status: 200,
  message: "ok",
};
```

## 常用工具类型

```typescript
interface User {
  id: number;
  name: string;
  email: string;
}

// Partial：所有字段变可选
type PartialUser = Partial<User>;

// Required：所有字段变必填
type RequiredUser = Required<User>;

// Pick：选取部分字段
type UserPreview = Pick<User, "id" | "name">;

// Omit：排除部分字段
type UserWithoutEmail = Omit<User, "email">;

// Record：构建键值对类型
type UserMap = Record<string, User>;
```

## 编译与运行

```bash
# 安装 TypeScript 编译器
npm install -g typescript

# 编译单个文件
tsc hello.ts

# 初始化项目配置
tsc --init  # 生成 tsconfig.json

# 监听模式
tsc --watch
```

## 浏览器支持现状

浏览器目前**不能直接运行** TypeScript，必须先编译为 JavaScript。常用编译工具：

| 工具 | 特点 |
| --- | --- |
| `tsc` | 官方编译器，支持完整类型检查 |
| **SWC** | Rust 编写，速度极快，Next.js 内置 |
| **esbuild** | Go 编写，速度极快，Vite 开发模式使用 |
| **Babel** | 插件丰富，只转译不做类型检查 |

> **注意**：SWC、esbuild、Babel 只做**语法转译**（剥离类型注解），不做类型检查。完整的类型检查仍需 `tsc`。

未来浏览器有可能通过 [TC39 Type Annotations 提案](https://github.com/tc39/proposal-type-annotations)（当前 Stage 1）将类型注解视为注释忽略，但不会做运行时类型检查。Node.js 23+ 已实验性支持直接执行 `.ts` 文件（同样忽略类型）。
