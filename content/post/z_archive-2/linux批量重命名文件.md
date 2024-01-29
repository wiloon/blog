---
title: Linux批量重命名文件
author: "-"
date: 2016-05-13T12:26:05+00:00
url: /?p=8987
categories:
  - Inbox
tags:
  - reprint
---
## Linux批量重命名文件
```bash
  
#在前面添加 _hoho_
  
for i in \`ls\`; do mv -f $i \`echo "_hoho_"$i\`; done

#修改前面5个字母为zhaozh
  
for i in \`ls\`; do mv -f $i \`echo $i | sed 's/^...../zhaozh/'\`; done

```


Linux批量重命名文件会涉及到改变一个字母、改变一些相连字母、改变某些位置的字母、在最前面加上某些字母、或者改变字母的大小写。完成这里五个方法基本上就会解决了Linux批量重命名的工作。

1. 我想把它们的名字的第一个1个字母变为"q",其它的不变

[root@pps mailqueue]# for i in \`ls\`; do mv -f $i \`echo $i | sed 's/^./q/'\`; done

或者写个脚本,显得更加清晰: 
  
for file in \`ls\`
  
do
  
newfile =\`echo $i | sed 's/^./q/'\`
  
mv $file $newfile
  
done
  
2. 修改前面5个字母为zhaozh

[root@pps mailqueue]# for i in \`ls\`; do mv -f $i \`echo $i | sed 's/^...../zhaozh/'\`; done

3. 修改后面5个字母为snail

[root@pps mailqueue]# for i in \`ls\`; do mv -f $i \`echo $i | sed 's/.....$/snail/'\`; done

4. 在前面添加 _hoho_

[root@pps mailqueue]# for i in \`ls\`; do mv -f $i \`echo "_hoho_"$i\`; done

5. 所有的小写字母变大写字母

[root@pps mailqueue]# for i in \`ls\`; do mv -f $i \`echo $i | tr a-z A-Z\`; done

上面是五中完成有关Linux批量重命名方法。