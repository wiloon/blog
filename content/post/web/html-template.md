---
title: HTML template, 模板
author: "-"
date: 2012-02-19T09:01:11.000+00:00
url: "/?p=2356"
categories:
- Web
tags:
- HTML

---
## HTML template, 模板

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>title0</title>
    <!–-css-–>
    
    <!--javascript-->
    <script src="path/to/foo.js"></script>
    <script type="text/javascript">
        var myVar = "hello";
        function showAlert() { alert('You triggered an alert!'); }

        function func0(){
            console.log('func0')
        }
        window.onload = function () {
            console.log('window.onload')
        }
    </script>
</head>
<body>
    body0
    <button type="button" onclick="func0()">button0</button>
</body>
</html>
```

HTML (Document Structures)

头部信息(head)里包含关于所在网页的信息。头部信息(head)里的内容,主要是被浏览器所用,不会显示在网页的正文内容里。 另外,搜索引擎如google,yahoo,baidu等也会查找你网页中的head信息链接(link)用链接(link)可以建立和外部文件的链接。常用的是对CSS外部样式表(external style sheet)的链接。
