---
title: ECMAScript, javascript basic
author: "-"
date: "2020-12-03 11:18:50" 
categories:
  - inbox
tags:
  - reprint
---
## ECMAScript, javascript basic, js basic

## 模板字面量, 多行字符串

```js
let learnCoding = `How to start learning web development?
- Learn HTML
- Learn CSS
- Learn JavaScript
Use freeCodeCamp to learn all the above and much, much more !
`

console.log(learnCoding);


// 输出

// How to start learning web development?
// - Learn HTML
// - Learn CSS
// - Learn JavaScript
// Use freeCodeCamp to learn all the above and much, much more !

```

## 数组

JavaScript 数组是可调整大小的，并且可以包含不同的数据类型。

```js
const fruits = [];
fruits.push("banana", "apple", "peach");
console.log(fruits.length); // 3
```

[https://es6.ruanyifeng.com/](https://es6.ruanyifeng.com/)

### ES6之Object.assign()

[https://blog.fundebug.com/2017/09/11/object-assign/](https://blog.fundebug.com/2017/09/11/object-assign/)  

ES6提供了Object.assign()，用于合并/复制对象的属性。

### 箭头函数

ES6标准新增了一种新的函数: Arrow Function (箭头函数) 。

为什么叫Arrow Function？因为它的定义用的就是一个箭头:

x => x * x
上面的箭头函数相当于:

function (x) {
    return x * x;
}
箭头函数相当于匿名函数，并且简化了函数定义。箭头函数有两种格式，一种像上面的，只包含一个表达式，连{ ... }和return都省略掉了。还有一种可以包含多条语句，这时候就不能省略{ ... }和return:

x => {
    if (x > 0) {
        return x *x;
    }
    else {
return - x* x;
    }
}
如果参数不是一个，就需要用括号()括起来:

// 两个参数:
(x, y) => x *x + y* y

// 无参数:
() => 3.14

// 可变参数:
(x, y, ...rest) => {
    var i, sum = x + y;
    for (i=0; i<rest.length; i++) {
        sum += rest[i];
    }
    return sum;
}

[https://www.liaoxuefeng.com/wiki/1022910821149312/1031549578462080](https://www.liaoxuefeng.com/wiki/1022910821149312/1031549578462080)

## Js中的history.back()在FireFox和Chrome

JavaScript中后退的写法: history.back()或者history.go(-1)。

这种写法在IE上即可实现我们想要的效果，但是在FireFox和Chrome就会变得很悲催了。

FireFox:

只需要改成如下方式:  **返回**

****Chrome:

Chrome比FireFox更难搞:  **返回**

本人分析: 对于Chrome来说，首先执行window.history.back()，执行完成之后再接着执行href="#"，所以无法返回。加上 return false之后将不再执行href="#"，便能正常返回。

