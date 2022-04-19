---
title: javascript
author: "-"
date: 2011-07-30T06:20:10+00:00
url: javascript
tags:
  - regex
categories:
  - inbox
---
## javascript

### 长数字格式化

    (10000).toLocaleString('en-US');
    // 输出 10,000

### 打印对象类型

    foo.getClass()

### window.event.keyCode ascii

    //check if ESC pressed

    if (window.event.keyCode == 27) {
    $("#english").val(");
    }
    //check if enter pressed
    keyCode == 13

## 日期

### ms > date string

    new Date(1636183170962).toLocaleString('en-US')

### 日期时间函数

var a=new Date();
  
var y = a.getFullYear()+ "- ";
  
var m = a.getMonth()+ "- ";
  
var d = a.getDate()+ "- ";
  
var h = a.getHours()+ "- ";
  
var x = a.getMinutes()+ "- ";
  
var s = a.getSeconds()+ "- ";
  
var ms=a.getMilliseconds()+ "- ";
  
var mssss= getTime();

<http://www.w3school.com.cn/js/jsref_obj_date.asp>

### 日期计算

```javascript
    this.dateStart = new Date().toISOString().substr(0, 10)
    const d = new Date()
    d.setDate(d.getDate() + 1)
    this.dateEnd = d.toISOString().substr(0, 10)
```

### 转东8区日期

```javascript
var timezone = 8; //目标时区时间，东八区
var offset_GMT = new Date().getTimezoneOffset(); // 本地时间和格林威治的时间差，单位为分钟
var nowDate = new Date().getTime(); // 本地时间距 1970 年 1 月 1 日午夜 (GMT 时间) 之间的毫秒数
var targetDate = new Date(nowDate + offset_GMT * 60 * 1000 + timezone * 60 * 60 * 1000);
console.log("东8区现在是: " + targetDate);
```

### 取字符串长度

    var pig ="ttttt"
    alert(pig.length) ;

### substring

    stringObject.substring(start,stop)

### 正则

    const imageDescription = 'https://www.wiloon.com/?key0=value0';
    const regexp = /.*?key0=(.*)$/;
    const match = imageDescription.match(regexp);
    console.log(`value=${match[1]}`);

    function checkPassWord(nubmer)  
    {  
        var re =  /^[0-9a-zA-Z]*$/;  //判断字符串是否为数字和字母组合     
        if (!re.test(nubmer))  
        {  
            return false;  
        }else{  
        return true;  
        }  
    } 

### 异常处理

    try {
            bomb();
        } catch (e) {
            // Handle all the error things
        }

## 字符串

### 字符串长度

    var str="字符串字节长度为" ;
    alert(str.length);

### JS字符串拼接/连接

    var s1 = "abc";
    var s2 = s1.concat("d" , "e" , "f");  //调用concat()连接字符串
    console.log(s2);  //返回字符串"abcdef"

### indexOf

indexOf() 方法返回调用它的 String 对象中第一次出现的指定值的索引，从 fromIndex 处进行搜索。如果未找到该值，则返回 -1。
stringObject.indexOf(searchvalue,fromindex)

indexOf用于发现一系列的字符在一个字符串中等位置并告诉你子字符串的起始位置。如果一个字符串中不包含该子字符串则indexOf返回"-1".
  
例子:
  
var the_word = "monkey";
  
//让我们从单词 "monkey"开始。
  
var location_of_m = the_word.indexOf("m");
  
//location_of_m(字母m的位置)将为0，因为字母m位于该字符串的起始位置。
  
var location_of_o = the_word.indexOf("o");
  
//location_of_o(字母o的位置)将为1。
  
var location_of_key = the_word.indexOf("key");
  
//location_of_key(key的位置)将为3因为子字符串"key"以字母k开始，而k

在单词monkey中的位置是3。
  
var location_of_y = the_word.indexOf("y");
  
//location_of_y)字母y的位置)是5。
  
var cheeky = the_word.indexOf("q");
  
//cheeky值是-1，因为在单词"monkey"中没有字母q。

indexOf更实用之处:
  
var the_email = prompt("What's your email address?", "");
  
var the_at_is_at = the_email.indexOf("@");
  
if (the_at_is_at == -1)
  
{
  
alert("You loser, email addresses must
  
have @ signs in them.");
  
}

这段代码询问用户的电子邮件地址，如果用户输入的电子邮件地址中不包含字符 则 提

示用户＂＠你输入的电子邮件地址无效，电子邮件的地址必须包含字符@。＂

```

replace()

//语法
  
stringObject.replace(regexp/substr,replacement)
  
 replace(/&quot;/g,"\"");//g 替换所有
  
```

replace() 方法用于在字符串中用一些字符替换另一些字符，或替换一个与正则表达式匹配的子串。

### js获取url参数值

#### 现代浏览器web api

    let params = (new URL(document.location)).searchParams; 
    let code = params.get("code")
    let state = params.get("state")

#### 采用正则表达式获取地址栏参数 (代码简洁，重点正则)

    function getQueryString(name) {
        let reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
        let r = window.location.search.substr(1).match(reg);
        if (r != null) {
            return decodeURIComponent(r[2]);
        };
        return null;
    }

split拆分法 (代码较复杂，较易理解)

function GetRequest() {
   const url = location.search; //获取url中"?"符后的字串
   let theRequest = new Object();
   if (url.indexOf("?") != -1) {
      let str = url.substr(1);
      strs = str.split("&");
      for(let i = 0; i < strs.length; i ++) {
         theRequest[strs[i].split["="](0)]=unescape[strs[i].split("="](1));
      }
   }
   return theRequest;
}

split拆分法(易于理解，代码中规)

function getQueryVariable(variable){
       let query = window.location.search.substring(1);
       let vars = query.split("&");
       for (let i=0;i<vars.length;i++) {
               let pair = vars[i].split("=");
               if(pair[0] == variable){return pair[1];}
       }
       return(false);
}

### 如何检查JavaScript中的字符串是否包含子字符串

 (ES6) includes

    var string ="foo",
        substring ="oo";
    string.includes(substring);

### JS对url进行编码和解码
<https://segmentfault.com/a/1190000013236956>

    escape(str0)

### String.length

var x = "Mozilla";
var empty = "";

### 替换地址栏url

```js
      let stateObj = { foo: "bar" };
      window.history.pushState(stateObj, '', 'foo');
      // 
```

console.log("Mozilla is " + x.length + " code units long");

### base64

```bash
    let str = 'foo'
    # encode
    let base64Str = btoa(str)
# decode
    let str = atob(base64Str)
```

### window.location 对象所包含的属性

属性    描述
hash    从井号 (#) 开始的 URL (锚)
host    主机名和当前 URL 的端口号
hostname    当前 URL 的主机名
href    完整的 URL
pathname    当前 URL 的路径部分
port    当前 URL 的端口号
protocol    当前 URL 的协议
search    从问号 (?) 开始的 URL (查询部分)

### JAVASRIPT 大写转小写

    str.toLowerCase()

## javascript mouse event

onmouseover: 当鼠标移动到某对象范围的上方时触发此事件

---

作者: 大小伍
链接: <https://www.jianshu.com/p/708c915fb905>
来源: 简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

————————————————
版权声明: 本文为CSDN博主「请叫我大师兄__」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接: <https://blog.csdn.net/qq_27093465/article/details/50731087>
