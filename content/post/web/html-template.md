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
    <!--css-->
    <style>
        body {
            background-color: powderblue;
        }
    </style>
    <!--javascript-->
    <script src="path/to/foo.js"></script>
    <script type="text/javascript">
        var myVar = "hello";
        function showAlert() { alert('You triggered an alert!'); }

        function func0() {
            console.log('func0')
            var outerDiv = document.getElementById('div_0');

            // 获取最外层 div 元素的内容
            var outerDivContent = outerDiv.childNodes;

            // 过滤出文本节点
            var textContent = '';
            outerDivContent.forEach(function (node) {
                if (node.nodeType === Node.TEXT_NODE) {
                    textContent += node.textContent.trim() + '\n';
                }
            });

            // 输出结果
            console.log(textContent.trim());
        }
        window.onload = function () {
            console.log('window.onload')
        }
    </script>
    <!--css-->
    <link rel="stylesheet" type="text/css" href="foo.css">
</head>

<body>
body0
<button type="button" onclick="func0()">button0</button>
<div id="div_0" style="background: red">
    text_0
    <div id="div_1" style="background: green; width: 100px;">
        text_1
    </div>
    text_2
</div>
</body>

</html>

```

```bash
# 在浏览器里直接访问这个文件
file:///home/wiloon/tmp/foo.htm
```

HTML (Document Structures)

头部信息(head)里包含关于所在网页的信息。头部信息(head)里的内容,主要是被浏览器所用,不会显示在网页的正文内容里。 另外,搜索引擎如google,yahoo,baidu等也会查找你网页中的head信息链接(link)用链接(link)可以建立和外部文件的链接。常用的是对CSS外部样式表(external style sheet)的链接。
