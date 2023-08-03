---
title: async await
author: "-"
date: 2016-10-19T05:19:05+00:00
url: async/await
categories:
  - Inbox
tags:
  - reprint
---
## async await

async/await 是以更舒适的方式使用 promise 的一种特殊语法，同时它也非常易于理解和使用。

async function
让我们以 async 这个关键字开始。它可以被放置在一个函数前面，如下所示：

async function f() {
  return 1;
}

在函数前面的 “async” 这个单词表达了一个简单的事情：即这个函数总是返回一个 promise。其他值将自动被包装在一个 resolved 的 promise 中。

例如，下面这个函数返回一个结果为 1 的 resolved promise，让我们测试一下：

async function f() {
  return 1;
}

f().then(alert); // 1
……我们也可以显式地返回一个 promise，结果是一样的：

async function f() {
  return Promise.resolve(1);
}

f().then(alert); // 1

所以说，async 确保了函数返回一个 promise，也会将非 promise 的值包装进去。很简单，对吧？但不仅仅这些。还有另外一个叫 await 的关键词，它只在 async 函数内工作，也非常酷。

await
语法如下：

// 只在 async 函数内工作
let value = await promise;
关键字 await 让 JavaScript 引擎等待直到 promise 完成（settle）并返回结果。

这里的例子就是一个 1 秒后 resolve 的 promise：

async function f() {

  let promise = new Promise((resolve, reject) => {
    setTimeout(() => resolve("done!"), 1000)
  });

  let result = await promise; // 等待，直到 promise resolve (*)

  alert(result); // "done!"
}

f();

