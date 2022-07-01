---
title: Markdown 语法
author: "-"
date: 2012-09-17T12:51:31+00:00
url: /?p=4069
categories:
  - Linux
tags:
  - reprint
---
## Markdown 语法

## 字体

### 加粗

要加粗的文字左右分别用两个*号包起来

### 斜体

要倾斜的文字左右分别用一个*号包起来 `*foo*`

*foo*

### 斜体加粗

要倾斜和加粗的文字左右分别用三个*号包起来

### 删除线

要加删除线的文字左右分别用两个~~号包起来

### 示例

**这是加粗的文字**  
*这是倾斜的文字*  
***这是斜体加粗的文字***  
~~这是加删除线的文字~~

### 标题

```bash
# 一级标题
## 二级标题
### 三级标题
#### 四级标题
##### 五级标题
###### 六级标题
```

### 图片

```bash
![Alt text](图片链接 "optional title")

#  本地图片 
![avatar](/user/desktop/doge.png)
# 网络图片
![avatar](https://dubbo.apache.org/imgs/v3/concepts/threecenters.png)
![](https://dubbo.apache.org/imgs/v3/concepts/threecenters.png)
```

### 表格

```bash
|  t0 | t1  |
| - | - |
|  c0r0 | c1r0|
|  c1r1 |  c1r1 |

```

### 引用

```bash
>foo
```

Markdown 是一种轻量级的标记语言，由John Gruber和Aaron Swartz创建，使其成为可读性最大并可再发行的可输入输出的格式。这种语言创建灵感来自于已经存在的带标记的电子邮件文本。Markdown 允许 HTML 语法，所以使用者如果需要可以直接用 HTML来表示是可以的。Markdown最初由Gruber应用在Perl语言中，但现在已经有多种编程语言应用了。它是开源项目，并以BSD-style许可证的许可方式以插件形式或内容管理系统形式发布。

### 段落与换行

换行 Line Break

1. 段落的前后必须是空行:
空行指的是行内什么都没有，或者只有空白符 (空格或制表符)

相邻两行文本，如果中间没有空行 会显示在一行中 (换行符被转换为空格)

2. 如果需要在段落内加入换行 (\<br>) :
可以在前一行的末尾加入至少两个空格
然后换行写其它的文字

3. Markdown 中的多数区块都需要在两个空行之间。

几乎每个 Markdown 应用程序都支持两个或多个空格进行换行，称为 结尾空格 (trailing whitespace) 的方式，但这是有争议的，因为很难在编辑器中直接看到空格，并且很多人在每个句子后面都会有意或无意地添加两个空格。由于这个原因，你可能要使用除结尾空格以外的其它方式来换行。幸运的是，几乎每个 Markdown 应用程序都支持另一种换行方式: HTML 的 \<br> 标签。

为了兼容性，请在行尾添加“结尾空格”或 HTML 的 \<br> 标签来实现换行。

还有两种其他方式我并不推荐使用。CommonMark 和其它几种轻量级标记语言支持在行尾添加反斜杠 (\\) 的方式实现换行，但是并非所有 Markdown 应用程序都支持此种方式，因此从兼容性的角度来看，不推荐使用。并且至少有两种轻量级标记语言支持无须在行尾添加任何内容，只须键入回车键 (return) 即可实现换行。

><https://www.markdown.xyz/basic-syntax/>

作者: 高鸿祥
链接: <https://www.jianshu.com/p/191d1e21f7ed>
来源: 简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

<https://xianbai.me/learn-md/article/syntax/paragraphs-and-line-breaks.html>

<https://markdown.com.cn/basic-syntax/line-breaks.html>

## markdown test
<http://wowubuntu.com/markdown/#autolink>

# Title

<https://en.support.wordpress.com/markdown-quick-reference/>

*Emphasize*
  
**Strong**
  
link [wiloon.com][1]

Some text with [a link][1] and
  
another [link][2].

* Item
* Item
* Item
* Item

  1. Item
  2. Item

  3. Item

  4. Item
      * Mixed
      * Mixed
  5. Item

# foo

## bar

 [1]: http://wiloon.com "title wiloon.com"
