---
author: "-"
date: "2020-09-29 10:33:30" 
title: "promise"
categories:
  - inbox
tags:
  - reprint
---
## "promise"

ECMAscript 6 原生提供了 Promise 对象。

Promise 对象代表了未来将要发生的事件，用来传递异步操作的消息。

Promise 对象有以下两个特点:
1. 对象的状态不受外界影响。Promise 对象代表一个异步操作，有三种状态: 
- pending: 初始状态，不是成功或失败状态。
- fulfilled: 意味着操作成功完成。
- rejected: 意味着操作失败。

只有异步操作的结果，可以决定当前是哪一种状态，任何其他操作都无法改变这个状态。这也是 Promise 这个名字的由来，它的英语意思就是「承诺」，表示其他手段无法改变。

2. 一旦状态改变，就不会再变，任何时候都可以得到这个结果。Promise 对象的状态改变，只有两种可能: 从 Pending 变为 Resolved 和从 Pending 变为 Rejected。只要这两种情况发生，状态就凝固了，不会再变了，会一直保持这个结果。就算改变已经发生了，你再对 Promise 对象添加回调函数，也会立即得到这个结果。这与事件 (Event) 完全不同，事件的特点是，如果你错过了它，再去监听，是得不到结果的。

Promise 优缺点
有了 Promise 对象，就可以将异步操作以同步操作的流程表达出来，避免了层层嵌套的回调函数。此外，Promise 对象提供统一的接口，使得控制异步操作更加容易。

Promise 也有一些缺点。首先，无法取消 Promise，一旦新建它就会立即执行，无法中途取消。其次，如果不设置回调函数，Promise 内部抛出的错误，不会反应到外部。第三，当处于 Pending 状态时，无法得知目前进展到哪一个阶段 (刚刚开始还是即将完成) 。
https://www.liaoxuefeng.com/wiki/1022910821149312/1023024413276544
https://www.runoob.com/w3cnote/javascript-promise-object.html

```html
<!DOCTYPE html>
<html>

<head>
    <script type="text/javascript">
        console.log('javascript0')
        function resolve(str) {
            console.log('resolve.' + str)
        }
        function reject(str) {
            console.log('reject.' + str)
        }

        function fun0() {
            console.log('fun0 start')
            //test(resolve, reject)

            new Promise(test).then(function (result) {
                console.log('成功: ' + result);
            }, function (result) {
                console.log('成功1: ' + result);
            }).catch(function (reason) {
                console.log('失败: ' + reason);
            });
        }

        function log(str) {
            console.log(str)
        }
        function callback() {
            console.log('Done');
        }

        function test(resolveParams, rejectParams) {
            var timeOut = Math.random() * 2;
            log('set timeout to: ' + timeOut + ' seconds.');
            setTimeout(function () {
                if (timeOut < 1) {
                    log('call resolve()...');
                    resolveParams('200 OK');
                } else {
                    log('call reject()...');
                    rejectParams('timeout in ' + timeOut + ' seconds.');
                }
            }, timeOut * 1000);
        }
    </script>
</head>

<body>
    body0
    <button name="btn0" onclick="fun0()">button0</button>
</body>

</html>
```

---

https://www.cnkirito.moe/future-and-promise/
