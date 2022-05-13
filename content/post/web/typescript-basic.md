---
author: "-"
date: "2020-10-19 16:43:49" 
title: "typescript basic"
categories:
  - inbox
tags:
  - reprint
---
## "typescript basic"

### number <> string
    let n = Number('1234')
    String(page_number);

### 遍历Array
#### 方法一，for…of
这个貌似是最常用的方法，angular 2中HTML语法绑定也是要的这种语法。

    let someArray = [1, "string", false];

    for (let entry of someArray) {
        console.log(entry); // 1, "string", false
    }

#### 方法二，for循环
for循环其实是标准的C风格语法。

    let someArray = [1, "string", false];

    for (var i = 0; i < someArray.length; i ++) {
        console.log(someArray[i]); // 1, "string", false
    }

#### 方法三， for…in
官方文档上强调了for…in和for…of的区别: 

    let list = [4, 5, 6];

    for (let i in list) {
    console.log(i); // "0", "1", "2",
    }

    for (let i of list) {
    console.log(i); // "4", "5", "6"
    }

#### 方法三，forEach
forEach其实是JavaScript的循环语法，TypeScript作为JavaScript的语法超集，当然默认也是支持的。

    let list = [4, 5, 6];
    list.forEach((val, idx, array) => {
        // val: 当前值
        // idx: 当前index
        // array: Array
    });

方法四，every和some
every和some也都是JavaScript的循环语法，TypeScript作为JavaScript的语法超集，当然默认也是支持的。因为forEach在iteration中是无法返回的，所以可以使用every和some来取代forEach。

    let list = [4, 5, 6];
    list.every((val, idx, array) => {
        // val: 当前值
        // idx: 当前index
        // array: Array
        return true; // Continues
        // Return false will quit the iteration
    });


### 类
class Car { 
    // 字段 
    engine:string; 
 
    // 构造函数 
    constructor(engine:string) { 
        this.engine = engine 
    }  
 
    // 方法 
    disp():void { 
        console.log("发动机为 :   "+this.engine) 
    } 
}

---

https://blog.csdn.net/alvachien/article/details/52475745