---
title: TypeScript
author: "-"
date: 2015-06-13T00:22:45+00:00
url: /?p=7806
categories:
  - Inbox
tags:
  - JavaScript

---
## TypeScript
TypeScript是一种由微软开发的自由和开源的编程语言。它是JavaScript的一个超集，兼容JavaScript，可以载入JS代码然后运行。它与JavaScript相比进步的地方包括: 加入注释，让编译器理解所支持的对象和函数，编译器会移除注释，不会增加开销。 而JavaScript只是一个脚本语言，并非设计用于开发大型 Web 应用，JavaScript 没有提供类和模块的概念，而TypeScript扩展实现了这些特性。

它扩展了 JavaScript 的语法，因此现有的JavaScript代码可与其代码一起工作无需任何修改，它通过类型注解提供编译时的静态类型检查。TypeScript可处理已有的JavaScript代码，并只对其中的TypeScript代码进行编译。

TypeScript 最大的特点就是类型化，因此才叫做TypeScript。比起弱类型的JavaScript，类型化的TypeScript显得更加容易维护。

要在应用中使用 TypeScript 必须先编译，编译的结果是生成 js 文件，你可通过 TypeScript 编译器 tsc 命令来完成这个过程。如要编译test.ts(TypeScript文件的扩展名为.ts)，可用如下命令: 

tsc test.ts
  
编译完成后就会在当前目录生成名为test.js的文件。

注: 不要将TypeScript看作是一门新的语言，它只是为了提升JavaScript代码质量的一个工具，最终TypeScript仍然要编译成JavaScript。

yarn global add typescript

### greeter.ts

function greeter(person) {
    return "Hello, " + person;
}

let user = "Jane User";

document.body.textContent = greeter(user);
```

```bash
tsc greeter.ts
```

```xml
<!DOCTYPE html>
<html>
    <head><title>title0</title></head>
    <body>
        <script src="greeter.js"></script>
    </body>
</html>
``` 

let num: number = 100.001;
  
let str: string = num.toFixed(2);

const是对let的一个增强，它能阻止对一个变量再次赋值。

### 数组

let fibonacci: number[] = [1, 1, 2, 3, 5];
```

###
    if (typeof this.$route.query.foo === 'string') {
          this.query(this.$route.query.foo)
        }