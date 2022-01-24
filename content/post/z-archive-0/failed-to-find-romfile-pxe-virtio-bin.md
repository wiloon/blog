---
title: axios
author: "-"
date: 2012-03-13T02:06:32+00:00
url: axios
categories:
  - Web
tags:
  - axios

---
## axios

### 模拟form 提交
```javascript
Content-Type: multipart/form-data
import axios from 'axios'
let data = new FormData();
data.append('code','1234');
data.append('name','yyyy');
axios.post(`${this.$url}/test/testRequest`,data)
.then(res=>{
    console.log('res=>',res);            
})

```
>https://segmentfault.com/a/1190000015261229
