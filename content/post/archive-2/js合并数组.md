---
title: JS合并数组
author: "-"
date: 2016-03-30T14:59:19+00:00
url: /?p=8845
categories:
  - JavaScript
tags:
  - reprint
---
## JS合并数组
http://blog.csdn.net/renfufei/article/details/39376311

比较JS合并数组的各种方法及其优劣
  
标签:  数组合并拼接slicereduce
  
2014-09-18 18:09 8077人阅读 评论(0) 收藏 举报
  
分类:  JS笔记 (29) 
  
原文链接: Combining JS Arrays
  
原文日期: 2014-09-09
  
翻译日期: 2014-09-18
  
翻译人员: 铁锚

本文属于JavaScript的基础技能. 我们将学习结合/合并两个JS数组的各种常用方法,并比较各种方法的优缺点.

我们先来看看具体的场景:
  
[javascript][/javascript] view plain copy 在CODE上查看代码片派生到我的代码片
  
var q = [ 5, 5, 1, 9, 9, 6, 4, 5, 8];
  
var b = [ "tie", "mao", "csdn", "ren", "fu", "fei" ];

很明显,数组 q 和 b 简单拼接的结果是:
  
[javascript][/javascript] view plain copy 在CODE上查看代码片派生到我的代码片
  
[
  
5, 5, 1, 9, 9, 6, 4, 5, 8,
  
"tie", "mao", "csdn", "ren", "fu", "fei"
  
]

concat(..)方法

最常见的用法如下:
  
[javascript][/javascript] view plain copy 在CODE上查看代码片派生到我的代码片
  
var c = q.concat( b );

q; // [5,5,1,9,9,6,4,5,8]
  
b; // ["tie","mao","csdn","ren","fu","fei"];

c; // [5,5,1,9,9,6,4,5,8,"tie","mao","csdn","ren","fu","fei"]
  
如您所见, c 是一个全新的数组, 表示 q 和 b 这两个数组的组合, 但是 q 和 b 现在没用了是吧?
  
如果 q 数组有10000个元素, b 数组也有有10000个元素? 那么数组c现在就有20000个元素, 这种方式占用了2倍的内存.
  
"这没问题!",你可能会觉得. 只要将 q 和 b 置空就行, 然后就会被垃圾回收,对吗?问题解决了!
  
[javascript][/javascript] view plain copy 在CODE上查看代码片派生到我的代码片
  
q = b = null; // \`q\` and \`b\` 现在可以被垃圾回收了
  
额? 如果数组都很小,那自然没问题. 但对大型的数组,或需要多次重复处理时, 内存就被限制了, 它还需要进行优化.

循环插入

OK, 让我们把一个数组的内容加入到另一个中试试,使用 Array#push() 方法:
  
[javascript][/javascript] view plain copy 在CODE上查看代码片派生到我的代码片
  
// 将数组 \`b\` 插入 \`q\`
  
for (var i=0; i < b.length; i++) {
  
q.push( b[i] );
  
}

q; // [5,5,1,9,9,6,4,5,8,"tie","mao","csdn","ren","fu","fei"]

b = null;

现在, q中存放了两个原始数组的内容(q + b).
  
看样子对内存优化做的不错.
  
但如果 q 数组很小而 b 又很大呢? 出于内存和速度的考虑,这时想把较小的 q 插入到 b 前面. 没问题,只要用 unshift() 方法代替 push() 即可, 对应的也要从大到小进行循环遍历:
  
[javascript][/javascript] view plain copy 在CODE上查看代码片派生到我的代码片
  
// \`q\` into \`b\`:
  
for (var i=q.length-1; i >= 0; i-) {
  
b.unshift( q[i] );
  
}

b; // [5,5,1,9,9,6,4,5,8,"tie","mao","csdn","ren","fu","fei"]

q = null;

实用技巧

悲催的是,for循环很土并且难以维护. 我们能做得更好吗?
  
我们先试试 Array#reduce :
  
[javascript][/javascript] view plain copy 在CODE上查看代码片派生到我的代码片
  
// \`b\` onto \`q\`:
  
q = b.reduce( function(coll,item){
  
coll.push( item );
  
return coll;
  
}, q );

q; // [5,5,1,9,9,6,4,5,8,"tie","mao","csdn","ren","fu","fei"]

// or \`q\` into \`b\`:
  
b = q.reduceRight( function(coll,item){
  
coll.unshift( item );
  
return coll;
  
}, b );

b; // [5,5,1,9,9,6,4,5,8,"tie","mao","csdn","ren","fu","fei"]

Array#reduce() 和 Array#reduceRight() 很高大上,但有点笨重,而且一般人也记不住. JS规范6 中的 => 箭头函数(arrow-functions) 能让代码量大大减少, 但需要对每个数组元素执行函数调用, 也是很渣的手段.
  
那么下面的代码怎么样呢?
  
[javascript][/javascript] view plain copy 在CODE上查看代码片派生到我的代码片
  
// \`b\` onto \`q\`:
  
q.push.apply( q, b );

q; // [5,5,1,9,9,6,4,5,8,"tie","mao","csdn","ren","fu","fei"]

// or \`q\` into \`b\`:
  
b.unshift.apply( b, q );

b; // [5,5,1,9,9,6,4,5,8,"tie","mao","csdn","ren","fu","fei"]

BIG更高了,是吧!? 特别是 unshift() 方法不需要像前面那样考虑相反的顺序. ES6 的展开运算符(spread operator, 加 ... 前缀)就更高端了: a.push( ...b ) 或者 b.unshift( ...a )
  
但是,事实上这种方法还是太乐观了. 在这两种情况下,不管是将 a 或 b 传递给 apply() 作为第二个参数(apply方式调用Function时第一个参数在内部变成this,即context,上下文,作用域), 还是使用 ... 展开运算符的方式, 实际上数组都会被打散成为函数的 arguments .
  
第一个主要的问题是,占用了双倍的内存(当然,是临时的!),因为需要将数组复制到函数栈之中. 此外,不同的JS引擎有不同的实现算法,可能会限制了函数可以传递的参数数量.
  
如果数组添加了一百万个元素, 那一定会超过函数栈所允许的大小, 不管是push() 或 unshift()调用. 这种方式只在几千个元素时可用,所以必须限制其不能超过一定范围.

注意: 你也可以试试 splice(), 肯定会发现他和 push(..)/unshift(..) 都是一样的限制.

一种选择是继续使用这种方法,但是采用分批次处理:
  
[javascript][/javascript] view plain copy 在CODE上查看代码片派生到我的代码片
  
function combineInto(q,b) {
  
var len = q.length;
  
for (var i=0; i < len; i=i+5000) {
  
// 一次处理5000条
  
b.unshift.apply( b, q.slice( i, i+5000 ) );
  
}
  
}

等等,我们损害了代码的可读性(甚至是性能!). 在我们放弃之前结束这个旅程吧.

总结

Array#concat() 是久经考验的方法, 用于组合两个(或多个)数组. 但他创建了一个新的数组,而不是修改现有的一个.
  
有很多变通的手法,但他们都有不同的优缺点,需要根据实际情况来选择.
  
上面列出了各种 优点/缺点,也许最好的(包括没有列出的)方法是 reduce(..) 和 reduceRight(..)
  
无论你选择什么,都应该批判性地思考你的数组合并策略,而不是把它当作理所当然的事情.