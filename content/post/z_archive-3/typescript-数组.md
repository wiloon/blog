---
title: typescript 数组
author: "-"
date: 2019-08-17T06:47:09+00:00
url: /?p=14801
categories:
  - Inbox
tags:
  - reprint
---
## typescript 数组
版权声明: 本文为博主原创文章，遵循 CC 4.0 by-sa 版权协议，转载请附上原文出处链接和本声明。
  
本文链接: https://blog.csdn.net/honey199396/article/details/80750408

### 数组的声明

let array1:Array<number>;
  
let array2:number[];
  
### 数组初始化

let array1:Array<number> = new Array<number>();
  
let array2:number[] = [1，2，3];
  
### 数组元素赋值、添加、更改

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
  
### 删除

let array:Array<number> = [1,2,3,4];
  
console.log(array) // [1, 2, 3, 4]

let popValue = array.pop(); // 弹出
  
console.log(array) // [1, 2, 3]

array.splice(0, 1); // 删除元素 (index, deleteCount) 
  
console.log(array) // [2, 3]

array.shift(); // 删除第一个元素
  
console.log(array); // [3]

typescript的二维数组写法如下:
  
let twoM : string[][]

这是变成成js后的代码
  
var twoM;

也可以用Array
  
let twoM : Array>;

建议声明数组用Array, 代码比较清晰.
  
请注意这段代码, 编译成js后, 变量是不会自动初始化成数组的, 如果之后直接给twoM插入一个值会报错, 例如:
  
let twoM : string[][]
  
twoM.push(["abc"])

https://www.jianshu.com/p/be871ff2fee4
