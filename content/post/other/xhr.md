---
title: XHR与fetch
author: "-"
date: 2012-06-10T08:10:46+00:00
url: /?p=3489
categories:
  - Java
  - Web
tags:
  - reprint
---
## XHR与fetch
XMLHttpRequest 是一个内建的浏览器对象，它允许使用 JavaScript 发送 HTTP 请求。

虽然它的名字里面有 “XML” 一词，但它可以操作任何数据，而不仅仅是 XML 格式。我们可以用它来上传/下载文件，跟踪进度等。

现如今，我们有一个更为现代的方法叫做 fetch，它的出现使得 XMLHttpRequest 在某种程度上被弃用。

在现代 Web 开发中，出于以下三种原因，我们还在使用 XMLHttpRequest：

历史原因：我们需要支持现有的使用了 XMLHttpRequest 的脚本。
我们需要兼容旧浏览器，并且不想用 polyfill (例如为了使脚本更小）。
我们需要做一些 fetch 目前无法做到的事情，例如跟踪上传进度。

>https://zh.javascript.info/xmlhttprequest

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>title0</title>
    <!–css–>

    <!--javascript-->
    <script type="text/javascript">
        window.onload = function () {
            console.log('window.onload')
        }
        function func0(){
            // 1. Create a new XMLHttpRequest object
            let xhr = new XMLHttpRequest();

            // 2. Configure it: GET-request for the URL /article/.../load
            xhr.open('GET', 'http://localhost:8000');

            // 3. Send the request over the network
            xhr.send();

            // 4. This will be called after the response is received
            xhr.onload = function () {
                if (xhr.status !== 200) {
                    // analyze HTTP status of the response
                    console.log(`Error ${xhr.status}: ${xhr.statusText}`);
                    // e.g. 404: Not Found
                } else {
                    // show the result
                    console.log(`Done, got ${xhr.response.length} bytes`);
                    // response is the server
                }

                xhr.onprogress = function (event) {
                    if (event.lengthComputable) {
                        console.log(`Received ${event.loaded} of ${event.total} bytes`);
                    } else {
                        console.log(`Received ${event.loaded} bytes`); // no Content-Length
                    }
                };
                xhr.onerror = function () {
                    console.log("Request failed");
                };
            }
        }

        function func1(){
            fetch('http://localhost:8000').then(function(response) {
                console.log('response')
                console.log(response.json());
                return response.json();
            }).then(function(data) {
                console.log('data')
                console.log(data);
            }).catch(function() {
                console.log("Booo");
            });
        }

    </script>
</head>
<body>
body0
<button type="button" onclick="func0()">button0</button>
<button type="button" onclick="func1()">button1</button>
</body>
</html>


```