---
title: emacs diff
author: w1100n
type: post
date: 2014-03-08T08:48:40+00:00
url: /?p=6374
categories:
  - Uncategorized
tags:
  - emacs

---
### diff

使用 _Unix_ 的 `diff` 工具程序，你可以找到两个文件的不同之处。所比较的两个文件可能是: 

  * 原始文件与更改之后的文件
  * 不同的两个人编辑的同一个文件(譬如，一个项目中协同工作的两个人编辑的文件)
  * 不同机器上的两个文件(譬如，你的 `.emacs` 文件可能在家和工作场合各有一份拷贝)

对于后面两种文件，两个要比较的文件共有一个原始的文件。此种情况下, `diff3` 程序会轻松的帮你创建一个文件，文件内容是对原始文件所做的修改记录。

### <a id="sec2" name="sec2"></a>Ediff

除非两个文件的不同之处很少，否则 `diff` 的输出将会很难阅读。幸运的是, `Emacs` 提供了一个 `diff` 的接口，称为 `Ediff` ,将此工作变得简单。不仅将 `diff` 的输出变得可读之外， `Emacs` 还提供了合并文件函数以及其他的应用补丁，更多的细节信息，可以参考`Ediff` 的 `info` 文档。 `Emacs` 还能比较不同文件夹下的两个文件，若你在不同地方工作，这个功能可能会非常有用(如你的Lisp配置文件。

### <a id="sec3" name="sec3"></a>用 Ediff 来比较文件

`Ediff` 比较的项目有: ( 可用 M-x 来启动 )

<table border="2" cellpadding="5">
  <tr>
    <th>
      比较项目
    </th>
    
    <th>
      说明
    </th>
  </tr>
  
  <tr>
    <td>
      ediff-regions-linewise, ediff-regions-
    </td>
    
    <td>
      询问两个缓冲区的名字，然后比较相应的区域。不过你只能在每一个缓冲区中选定一个区域，而不能比较一个文件缓冲区的两个区域。( TODO: 第15个小时的内容 "了解文件" ，会提供一个比较同一个文件中的两个区域的方法。)
    </td>
  </tr>
  
  <tr>
    <td>
      ediff-buffers
    </td>
    
    <td>
      询问两个缓冲区的名字，然后比较
    </td>
  </tr>
  
  <tr>
    <td>
      ediff-files
    </td>
    
    <td>
      询问两个文件的名字，加载之，然后比较
    </td>
  </tr>
  
  <tr>
    <td>
      ediff-windows-linewise, ediff-windows-wordwise
    </td>
    
    <td>
      让你选两个窗口，然后比较窗口的内容。 <code>-linewise-</code> 函数比 <code>-wordwise-</code> 函数要快，但另一方面， <code>-wordwise-</code> 工作方式更好，尤其是小区域作业时。 <code>-linewise-</code> 一行一行地比较， <code>-wordwise-</code> 一个单词一个单词地比较。
    </td>
  </tr>
</table>

### <a id="sec4" name="sec4"></a>一些Ediff 控制命令

在 control buffer 中，按键。

<table border="2" cellpadding="5">
  <tr>
    <th>
      快捷键
    </th>
    
    <th>
      命令
    </th>
    
    <th>
      说明
    </th>
  </tr>
  
  <tr>
    <td>
      q
    </td>
    
    <td>
      ediff-quit
    </td>
    
    <td>
      关闭 ediff control buffer， 并退出 ediff
    </td>
  </tr>
  
  <tr>
    <td>
      Space 或 n
    </td>
    
    <td>
      ediff-next-difference
    </td>
    
    <td>
      下一个差异处
    </td>
  </tr>
  
  <tr>
    <td>
      Del 或 p
    </td>
    
    <td>
      ediff-previous-difference
    </td>
    
    <td>
      上一个差异处
    </td>
  </tr>
  
  <tr>
    <td>
      [n]j
    </td>
    
    <td>
      ediff-jump-to-difference
    </td>
    
    <td>
      有数字前缀 [n] 修饰，第n个差异处,n可为负数
    </td>
  </tr>
  
  <tr>
    <td>
      v 或 C-v
    </td>
    
    <td>
      ediff-scroll-vertically
    </td>
    
    <td>
      所有缓冲区同步向下滚动
    </td>
  </tr>
  
  <tr>
    <td>
      V 或 M-v
    </td>
    
    <td>
      ediff-scroll-vertically
    </td>
    
    <td>
      所有缓冲区同步向上滚动
    </td>
  </tr>
  
  <tr>
    <td>
      <
    </td>
    
    <td>
      ediff-scroll-horizontally
    </td>
    
    <td>
      所有缓冲区同步向左滚动
    </td>
  </tr>
  
  <tr>
    <td>
      >
    </td>
    
    <td>
      ediff-scroll-horizontally
    </td>
    
    <td>
      所有缓冲区同步向右滚动
    </td>
  </tr>
  
  <tr>
    <td>
      (vertical bar)
    </td>
    
    <td>
      ediff-toggle-split
    </td>
    
    <td>
      切换缓冲区布局方式, 水平和竖直
    </td>
  </tr>
  
  <tr>
    <td>
      m
    </td>
    
    <td>
      ediff-toggle-wide-display
    </td>
    
    <td>
      在正常 frame 大小和最大化之间切换
    </td>
  </tr>
  
  <tr>
    <td>
      a
    </td>
    
    <td>
      ediff-copy-A-to-B
    </td>
    
    <td>
      把Buffer-A的内容复制到Buffer-B
    </td>
  </tr>
  
  <tr>
    <td>
      b
    </td>
    
    <td>
      ediff-copy-B-to-A
    </td>
    
    <td>
      把Buffer-B的内容复制到Buffer-A
    </td>
  </tr>
  
  <tr>
    <td>
      r a 或 r b
    </td>
    
    <td>
      ediff-restore-diff
    </td>
    
    <td>
      恢复 Buffer-A 或 Buffer-B 差异区域中的被修改的内容
    </td>
  </tr>
  
  <tr>
    <td>
      A 或 B
    </td>
    
    <td>
      ediff-toggle-read-only
    </td>
    
    <td>
      切换 Buffer-A 或 Buffer-B 的只读状态
    </td>
  </tr>
  
  <tr>
    <td>
      g a 或 g b
    </td>
    
    <td>
      ediff-jump-to-difference-at-point
    </td>
    
    <td>
      根据光标在缓冲区中的位置，设置一个离它们最近的差异区域为当前活动区域
    </td>
  </tr>
  
  <tr>
    <td>
      C-l
    </td>
    
    <td>
      ediff-recenter
    </td>
    
    <td>
      恢复先前的所有缓冲区比较的高亮差异区。
    </td>
  </tr>
  
  <tr>
    <td>
      !
    </td>
    
    <td>
      ediff-update-diffs
    </td>
    
    <td>
      重新比较并高亮差异区域
    </td>
  </tr>
  
  <tr>
    <td>
      w a 或 w b
    </td>
    
    <td>
      ediff-save-buffer
    </td>
    
    <td>
      保存 Buffer-A 或 Buffer-B 到磁盘
    </td>
  </tr>
  
  <tr>
    <td>
      E
    </td>
    
    <td>
      ediff-documentation
    </td>
    
    <td>
      打开 Ediff 文档
    </td>
  </tr>
  
  <tr>
    <td>
      z
    </td>
    
    <td>
      ediff-suspend
    </td>
    
    <td>
      关闭 ediff control buffer, 只是挂起，可在以后恢复 ediff 状态
    </td>
  </tr>
</table>

### <a id="sec5" name="sec5"></a>比较三个文件

此种需要大都发生在两个文件共有一个原始的文件。假设 C —> A, C —> B. A与B可能都对C进行了修改，你需要知晓，究竟A和B哪个对C做了什么修改。此时就需要比较三个文件了。

假如A有一部分内容，而在B中不存在，可能是下列两种情况之一: 

  * A 中增添了这部分内容
  * B 中删除了这部分内容

你就应该比较A B C 三个文件来确定究竟是哪种情况。

#### 操作

有两个函数

<table border="2" cellpadding="5">
  <tr>
    <th>
      函数
    </th>
    
    <th>
      说明
    </th>
  </tr>
  
  <tr>
    <td>
      ediff-files3
    </td>
    
    <td>
      比较三个文件
    </td>
  </tr>
  
  <tr>
    <td>
      ediff-buffers3
    </td>
    
    <td>
      比较三个缓冲区
    </td>
  </tr>
</table>

#### 具体操作

比较两个文件或缓冲区的所有操作，几乎都适于三个比较。不过在进行缓冲区差异区从A到B拷贝的操作略有不同: 

<table border="2" cellpadding="5">
  <tr>
    <th>
      快捷键
    </th>
    
    <th>
      说明
    </th>
  </tr>
  
  <tr>
    <td>
      cb
    </td>
    
    <td>
      将 Buffer-C 拷贝到 Buffer-A
    </td>
  </tr>
  
  <tr>
    <td>
      ab
    </td>
    
    <td>
      将 Buffer-A 拷贝到 Buffer-B
    </td>
  </tr>
</table>

以此类推，在 Buffer-A , Buffer-B, Buffer-C之间的操作可以很容易猜出。

### <a id="sec6" name="sec6"></a>Ediff Session

你可能同时要比较好多对文件，你可以同时拥有多个 `Ediff` `Session` 。按 `z` 挂起当前 `Ediff` `session` ,然后启动另一个 `Ediff``session` 就可以了。 此时，在 `control` `buffer` 中按 `R` 或是按下 M-x eregistry, 将会打开一个 `*Ediff` `Registry*` 的缓冲区，此缓冲区包含当前运行的所有 `Ediff` `Sessions`.可以选择一个 `Ediff` `session` 来进入。

### <a id="sec7" name="sec7"></a>合并文件

### <a id="sec8" name="sec8"></a>比较文件目录

### <a id="sec9" name="sec9"></a>与版本控制系统(VC) 一块儿工作

<http://caobeixingqiu.is-programmer.com/posts/6783.html>