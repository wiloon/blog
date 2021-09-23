---
title: datatable 删除行
author: "-"
type: post
date: 2013-11-08T04:56:16+00:00
url: /?p=5908
categories:
  - Uncategorized

---
先列出正确的写法，如果你只想马上改错就先复制吧，
  
    <img alt="复制代码" src="http://common.cnblogs.com/images/copycode.gif" />
  
  
        protected void deleteDataRow(int RowID,DataTable dt)
 {
 for (int i = dt.Rows.Count - 1; i >= 0; i-)
 {
 if (Convert.ToInt32(dt.Rows[i]["RowID"]) == RowID)
 dt.Rows.RemoveAt(i);
 }
 }
  
  
    <img alt="复制代码" src="http://common.cnblogs.com/images/copycode.gif" />
  


如果你有时间想学习一下就继续看下面列出可能出错的可能性吧。

1.如果只是想删除datatable中的一行，可以用DataRow的delete，但是必须要删除后让DataTable知道，所以就要用到.AcceptChanges()方法，原因是这种删除只是标识性删除，就像我们通常在数据库中用到的IsDelete字段。

2.彻底删除就要用到datatable的.Rows.Remove(DataRow dr)方法，同理也只是删除一行可以，如果要循环删除请继续往下看。

3.循环彻底删除就要用.Rows.RemoveAt(int index)方法，所以如果你是foreach的爱好者，在此请你换换口味，还有如果你是for的i++的忠实fans也希望你能换个思维。先看一下上面程序的正向写法（错误的，不可用) 
  
            for (int i = 0, j = dt.Rows.Count; i < j; i++)
 {
 if (Convert.ToInt32(dt.Rows[i]["RowID"]) == RowID)
 dt.Rows.RemoveAt(i);
 }
  


这个的错误在于datatable的RemoveAt()会在删除后更新dataTable的index，所以你要删除的index可能已经不是你的符合Convert.ToInt32(dt.Rows[i]["RowID"]) == RowID的index了，甚者还会抛出异常，说你访问的index不存在。

所以要从DataTable的下面网上查找删除，这样即使这行符合条件被删除了，上面的行依旧不受影响。

说了这么多，不知道你明白了吗？其实现在写这种文章显得有点"弱智"，技术学多了，越来越觉得自己的基础不够扎实，希望通过在此记录一下可以督促一下自己，也希望能给初学者带去丝丝帮助。

<http://www.cnblogs.com/gudao119/archive/2010/03/12/1684646.html>