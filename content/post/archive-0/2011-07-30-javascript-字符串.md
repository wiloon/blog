---
title: javascript basic
author: wiloon
type: post
date: 2011-07-30T06:20:10+00:00
url: /?p=381
tags:
  - javascript

---
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

### 字符串长度
    var str="字符串字节长度为" ;
    alert(str.length);

### indexOf
    stringObject.indexOf(searchvalue,fromindex)

indexOf用于发现一系列的字符在一个字符串中等位置并告诉你子字符串的起始位置。如果一个字符串中不包含该子字符串则indexOf返回"-1".
  
例子：
  
var the_word = "monkey";
  
//让我们从单词 "monkey"开始。
  
var location\_of\_m = the_word.indexOf("m");
  
//location\_of\_m(字母m的位置)将为0，因为字母m位于该字符串的起始位置。
  
var location\_of\_o = the_word.indexOf("o");
  
//location\_of\_o(字母o的位置)将为1。
  
var location\_of\_key = the_word.indexOf("key");
  
//location\_of\_key(key的位置)将为3因为子字符串"key"以字母k开始，而k

在单词monkey中的位置是3。
  
var location\_of\_y = the_word.indexOf("y");
  
//location\_of\_y)字母y的位置)是5。
  
var cheeky = the_word.indexOf("q");
  
//cheeky值是-1，因为在单词"monkey"中没有字母q。

indexOf更实用之处:
  
var the_email = prompt("What's your email address?", "");
  
var the\_at\_is\_at = the\_email.indexOf("@");
  
if (the\_at\_is_at == -1)
  
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

