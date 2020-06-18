---
title: linux test
author: wiloon
type: post
date: 2012-04-01T09:10:06+00:00
url: /?p=2717
categories:
  - Linux

---
<http://www.ibm.com/developerworks/cn/linux/l-bash-test.html>

内置命令 `test` 根据表达式_expr_ 求值的结果返回 0（真）或 1（假）。也可以使用方括号：`test  <em>expr</em> `和 [ _expr_ ] 是等价的。 可以用`$?` 检查返回值；可以使用 && 和 || 操作返回值；也可以用本技巧后面介绍的各种条件结构测试返回值。

<table summary="" width="50%" border="0" cellspacing="0" cellpadding="0">
  <tr valign="top">
    <td>
      -d
    </td>
    
    <td>
      目录
    </td>
  </tr>
  
  <tr valign="top">
    <td>
      -e
    </td>
    
    <td>
      存在（也可以用 -a）
    </td>
  </tr>
  
  <tr valign="top">
    <td>
      -f
    </td>
    
    <td>
      普通文件
    </td>
  </tr>
  
  <tr valign="top">
    <td>
      -h
    </td>
    
    <td>
      符号连接（也可以用 -L）
    </td>
  </tr>
  
  <tr valign="top">
    <td>
      -p
    </td>
    
    <td>
      命名管道
    </td>
  </tr>
  
  <tr valign="top">
    <td>
      -r
    </td>
    
    <td>
      可读
    </td>
  </tr>
  
  <tr valign="top">
    <td>
      -s
    </td>
    
    <td>
      非空
    </td>
  </tr>
  
  <tr valign="top">
    <td>
      -S
    </td>
    
    <td>
      套接字
    </td>
  </tr>
  
  <tr valign="top">
    <td>
      -w
    </td>
    
    <td>
      可写
    </td>
  </tr>
  
  <tr valign="top">
    <td>
      -N
    </td>
    
    <td>
      从上次读取之后已经做过修改
    </td>
  </tr>
</table>



可以用 `-eq`、 -`ne`、`-lt`、 -`le`、 -`gt` 或 -`ge` 比较算术值，它们分别表示等于、不等于、小于、小于等于、大于、大于等于。