---
title: Redmine wiki编辑
author: wiloon
type: post
date: 2013-02-22T01:54:37+00:00
url: /?p=5225
categories:
  - Uncategorized

---
http://redmine.ossxp.com/redmine/documents/8

Redmine默认使用Textile作为wiki的文本格式过滤器, 当然你也可以下载其他文本格式过滤器插件(Markdown, reST等). 以下介绍的语法都是基于Textile的语法.


## 链接


### Redmine链接

Redmine允许在任何wiki文本格式里使用问题，变更集和wiki页面的超链接。

  * 链接到问题： #124 (显示 #124, 如果此问题已经关闭则显示删除线)
  * 链接到变更集：r758 (显示 r758)
  * 使用非数字的哈希值链接到变更集： commit:c6f4d0fd(显示c6f4d0fd)。该特征出现在主线 1236。


### wiki链接

  * [[Guide]] 显示一个链接到"Guide"的链接：Guide
  * [[Guide|Use manual]] 显示指向同一页面的链接，链接显示的文本是：Use manual
  * [[Guide#Use-guide|Use guide]] 显示指向同一页面头的链接，链接显示的文本是：Use guide


### 可以加入指向其它项目wiki页面的链接

  * [[sandbox:some page]] 显示一个指向Sandbox项目名称为"Some page"的wiki页面的链接。
  * [[sandbox:]] 显示一个指向Sandbox项目Wiki主页面的链接。

如果Wiki还不存在，则连接将显示为红色，例如： Nonexistent page.


### 链接到其他资源：

**文档：**

  * document#17 (链接到ID为17的文档）
  * document:Geetings (链接到标题为"Geetings"的文档）
  * document:"Some document" (当文档标题含有空格时需要使用双引号）

**版本：**

  * vesion#3 (链接到ID为3的版本)
  * vesion:1.0.0 (链接到名称为"1.0.0"的版本)
  * vesion:"1.0 beta 2" (当版本名称含有空格时需要使用双引号)

**附件:**

  * attachment:file.zip (链接到当前页面名称为 file.zip 的附件)
  * 到目前为止, 只能引用当前页面的附件(如果您在编辑问题，则只能引用此问题的附件)

**版本库:**

  * souce:some/file 链接到项目版本库的 /some/file 文件
  * souce:some/file@52 链接到项目版本库 /some/file 文件的第52版本
  * souce:some/file#L120 链接到项目版本库 /some/file 文件的第120行
  * souce:some/file@52#L120 链接到项目版本库 /some/file 文件的第52版本的第120行
  * souce:"some file@52#L120" 如果URL中有空格，需要使用双引号来。链接到项目版本库 some file 文件的第52版本的第120行
  * expot:some/file 强制显示该文件的下载链接

**转意字符:**

如果您不希望Redmine将上述标记解释为链接，可以在它们前面添加一个感叹号：!


### 外部链接

HTTP URLs和邮件地址将自动转换为可点击的链接:

http://redmine.ossxp.com, someone@foo.bar

显示为: http://redmine.ossxp.com, someone@foo.bar

如果你想指定链接显示的文本,你可以使用标准的textile语法:

"群英汇":http://ossxp.com

显示为: 群英汇


## 文本格式:

对于标题、粗体、表格、列表，Redmine支持Textile语法。参考 http://www.textism.com/tools/textile/ 上对使用这些特征的详细信息.

下面列出一些例子, 但是Textile引擎可以做的更多.


### 字体样式:

* *bold*
* _italic_
* *_bold italic_*
* +underline+
* -strike-through-

显示结果:

  * **bold**
  * _italic_
  * _**bold italic**_
  * <ins>underline</ins>
  * <del>strike-through</del>


### 内嵌图片:

!image_url! 显示地址为image_url的图片(textile语法)
!>image_url! 图片右悬浮
!{width:300px}image_url! 设置图片的显示宽度

如果你的wiki页面有图片附件,你可以使用文件名:!attached_image.png!显示它


### 标题

h1. 一级标题
h2. 二级标题
h3. 三级标题


### 段落

p>. 右对齐
p=. 居中


### 块引用

段落以 bq. 开始
bq. 这是块引用的示例

显示为:

> 这是块引用的示例


### 无序列表

* Item 1
* Item 2
** Item 21
** Item 22
* Item 3

显示为:

  * Item 1
  * Item 2 
      * Item 21
      * Item 22
  * Item 3


### 有序列表

# Item 1
# Item 2
# Item 3
## Item 3.1
## Item 3.2

显示为:

  1. Item 1
  2. Item 2
  3. Item 3 
      1. Item 3.1
      2. Item 3.2


### 表格

|_.UserID|_.Name|_.Group|
|3=.IT|
|1|张三|/2.Users|
|2|李四|
|3|王五|Admin|

显示为:

<table>
  <tr>
    <th>
      UserID
    </th>
    
    <th>
      Name
    </th>
    
    <th>
      Group
    </th>
  </tr>
  
  <tr>
    <td colspan="3">
      IT
    </td>
  </tr>
  
  <tr>
    <td>
      1
    </td>
    
    <td>
      张三
    </td>
    
    <td rowspan="2">
      Users
    </td>
  </tr>
  
  <tr>
    <td>
      2
    </td>
    
    <td>
      李四
    </td>
  </tr>
  
  <tr>
    <td>
      3
    </td>
    
    <td>
      王五
    </td>
    
    <td>
      Admin
    </td>
  </tr>
</table>


### 内容列表

{{toc}} => toc左对齐
{{>toc}} => toc右对齐

具体参考 内容列表演示


### 宏(Macros)

Redmine有以下内置宏:

  * **子页面:**

显示子页面列表. 当没有参数时,将显示当前wiki页面的子页面. 例如:

{{child_paegs}} 该功能只有在wiki页面有效
{{child_pages(Foo)}} 列出Foo页面的子页面
{{child_paegs(Foo,parent=1)}} 和上面的功能一样,只不过多了一个链到Foo页面的链接

  * **hello_world**

一个宏示例

  * **include**

包含一个wiki页面.例如:

{{include(Foo)}}

或者包含一个指定项目的wiki页面

{{include(projectname:Foo)}}

  * **macro_list**

显示所有可用宏的列表,以及关于宏的描述

  * **代码高亮显示**

代码高亮显示依赖 CodeRay http://coderay.rubychan.de/ ,它是一个完全用Ruby编写的快速的语法高亮显示库. 目前支持的语言: c,html,javascript,rhtml,ruby,scheme,xml
  
**此功能仅在Wiki页面有效**
  
你可以用下面的语法高亮显示你代码

<pre><code>
加入你的代码
</code>