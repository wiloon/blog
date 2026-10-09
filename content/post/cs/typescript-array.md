---
title: "TypeScript 数组"
author: "-"
date: 2019-08-17T06:47:09+00:00
lastmod: 2026-10-09T21:22:13+08:00
url: typescript-array
categories:
  - JavaScript
tags:
  - typescript
  - remix
  - AI-assisted
aliases:
  - /typescript-数组/
---
## typescript 数组

版权声明: 本文为博主原创文章，遵循 CC 4.0 by-sa 版权协议，转载请附上原文出处链接和本声明。
  
本文链接: https://blog.csdn.net/honey199396/article/details/80750408

### 数组的声明

```typescript
let array1:Array<number>;
let array2:number[];
```
  
### 数组初始化

```typescript
let array1:Array<number> = new Array<number>();
let array2:number[] = [1, 2, 3];
```
  
### 数组元素赋值、添加、更改

```typescript
let array:Array<number> = [1,2,3,4];
console.log(array) // [1, 2, 3, 4]
array[0] = 20; // 修改
console.log(array) // [20, 2, 3, 4]
array[4] = 5; // 赋值
console.log(array) // [20, 2, 3, 4, 5]
array.push(6); // 添加
console.log(array) // [20, 2, 3, 4, 5, 6]
array.unshift(8, 0); // 在第一个位置依次添加
console.log(array); // [8, 0, 20, 2, 3, 4, 5, 6]
```
  
### 删除

```typescript
let array:Array<number> = [1,2,3,4];
console.log(array) // [1, 2, 3, 4]
let popValue = array.pop(); // 弹出
console.log(array) // [1, 2, 3]
array.splice(0, 1); // 删除元素 (index, deleteCount)
console.log(array) // [2, 3]
array.shift(); // 删除第一个元素
console.log(array); // [3]
```

typescript的二维数组写法如下:
  
let twoM : string[][]

这是变成成js后的代码
  
```typescript
var twoM;
```

也可以用Array
  
```typescript
let twoM : Array>;
```

建议声明数组用Array, 代码比较清晰.
  
请注意这段代码, 编译成js后, 变量是不会自动初始化成数组的, 如果之后直接给twoM插入一个值会报错, 例如:
  
let twoM : string[][]
  
```text
twoM.push(["abc"])
```

https://www.jianshu.com/p/be871ff2fee4

## 维护记录

| 时间 | 修改内容 | 原因 |
| ---- | -------- | ---- |
| 2026-10-09 | 修复本地 Hugo 构建的 Raw HTML 警告：代码/配置放入代码块，正文中的尖括号占位符改为行内代码；文件重命名为 `typescript-array.md`；title 改为「TypeScript 数组」；url 改为 `typescript-array`；旧 url 加入 aliases；categories 改为 JavaScript | 正文中的 HTML/XML 片段被当作原始 HTML 丢弃；文件名/URL/标题按规范调整 |
