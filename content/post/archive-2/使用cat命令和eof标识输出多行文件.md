---
title: 用cat命令和EOF标识生成文件
author: "-"
date: 2017-11-13T08:47:49+00:00
url: /?p=11416
categories:
  - shell

tags:
  - reprint
---
## 用cat命令和EOF标识生成文件
http://www.linuxfly.org/post/146/
     
在某些场合,可能我们需要在脚本中生成一个临时文件,然后把该文件作为最终文件放入目录中。 (可参考ntop.spec文件) 这样有几个好处,其中之一就是临时文件不是唯一的,可以通过变量赋值,也可根据不同的判断生成不同的最终文件等等。
  
一、cat和EOF
  
cat命令是linux下的一个文本输出命令,通常是用于观看某个文件的内容的；
  
EOF是"end of file",表示文本结束符。
  
结合这两个标识,即可避免使用多行echo命令的方式,并实现多行输出的结果。
  
二、使用
  
看例子是最快的熟悉方法: 

```bash
cat <<EOF >/etc/profile.d/goroot.sh
export GOROOT=$GOROOT
export GOPATH=$GOPATH
export PATH=\$PATH:$GOROOT/bin:$GOPATH/bin
EOF
```

结果: 
  
引用

# cat test.sh

#!/bin/bash
  
#you Shell script writes here.

可以看到,test.sh的内容就是cat生成的内容。
  
三、其他写法
  
1. 追加文件

# cat << EOF >> test.sh

2. 换一种写法

# cat > test.sh << EOF

3. EOF只是标识,不是固定的

# cat << HHH > iii.txt

> sdlkfjksl
    
> sdkjflk
    
> asdlfj
    
> HHH 

这里的"HHH"就代替了"EOF"的功能。结果是相同的。
  
引用

# cat iii.txt

sdlkfjksl
  
sdkjflk
  
asdlfj

4. 非脚本中
  
如果不是在脚本中,我们可以用Ctrl-D输出EOF的标识

# cat > iii.txt

skldjfklj
  
sdkfjkl
  
kljkljklj
  
kljlk
  
Ctrl-D

结果: 
  
引用

# cat iii.txt

skldjfklj
  
sdkfjkl
  
kljkljklj
  
kljlk

※关于">"、">>"、"<"、"<<"等的意思,请自行查看bash的介绍。