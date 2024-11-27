---
title: ES Modules
author: "-"
date: 2016-12-14T13:47:38+00:00
url: esmodule
categories:
  - Javascript
tags:
  - reprint
  - remix
---

ES Modules, or ECMAScript Modules

foo.js

```Javascript
class ArticleNode {
    constructor(node, paragraph) {
        this.node = node
        this.paragraph = paragraph
    }
}

export function createOneArticleNode(){
    let articleNode0 = new ArticleNode('foo', 'bar')
    console.log('a n: ', articleNode0)
}

```

bar.js

```Javascript
// jest test
import { createOneArticleNode } from '../content_module.js' 

test('test es module 0', () => {
    console.log('print foo')
    createOneArticleNode()
    console.log('print bar')
});

```

```Bash
npm run test
```