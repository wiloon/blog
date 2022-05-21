---
title: shell map
author: "-"
date: 2013-02-19T06:14:59+00:00
url: shell/map
categories:
  - shell
tags:
  - reprint
---
## shell map

## Map定义

在使用map时，需要先声明，否则结果可能与预期不同，array 可以不声明

方式1：

```bash
declare -A myMap
myMap["my03"]="03"
```

方式2：

```bash
declare -A myMap=(["my01"]="01" ["my02"]="02")
myMap["my03"]="03"
myMap["my04"]="04"
```

Map初始化：
与array类似，可以使用括号直接初始化，也可以通过添加的方式来初始化数据，与array不同的是，括号直接初始化时使用的为一个键值对，添加元素时，下标可以不是整数

myMap["my03"]="03"
myMap["my04"]="04"
输出Map所有的key、value、长度：
复制代码

输出所有的key
#若未使用declare声明map，则此处将输出0，与预期输出不符，此处输出语句格式比arry多了一个！
echo ${!myMap[@]}
#2）输出所有value
#与array输出格式相同
echo ${myMap[@]}
#3）输出map长度
#与array输出格式相同
echo ${#myMap[@]}
复制代码
Map遍历：
复制代码
#1)遍历，根据key找到对应的value
for key in ${!myMap[*]};do
  echo $key
  echo ${myMap[$key]}
done
#2)遍历所有的key
for key in ${!myMap[@]};do
  echo $key
  echo ${myMap[$key]}
done
#3)遍历所有的value
for val in ${myMap[@]};do
  echo $val
done
复制代码
Map测试：
复制代码
[root@cdh-143 shell-test]# more map-test.sh
#!/bin/sh

echo "一、定义Map:declare -A myMap=([\"myMap00\"]=\"00\" [\"myMap01\"]=\"01\")"
declare -A myMap=(["my00"]="00" ["my01"]="01")
myMap["my02"]="02"
myMap["my03"]="03"

echo "二、输出所有的key:"
echo ${!myMap[@]}

echo "三、输出所有value:"
echo ${myMap[@]}

echo "四、输出map的长度:"
echo ${#myMap[@]}

echo "五、遍历，根据key找到对应的value:"
for key in ${!myMap[*]};do
  echo "key:"$key
  echo "value:"${myMap[$key]}
done

echo "六、遍历所有的key:"
for key in ${!myMap[@]};do
  echo "key:"$key
  echo "value:"${myMap[$key]}
done

echo "七、遍历所有value:"
for val in ${myMap[@]};do
  echo "value:"$val
done
复制代码
输出：

复制代码
[root@cdh-143 shell-test]# ./map-test.sh
一、定义Map:declare -A myMap=(["myMap00"]="00" ["myMap01"]="01")
二、输出所有的key:
my02 my03 my00 my01
三、输出所有value:
02 03 00 01
四、输出map的长度:
4
五、遍历，根据key找到对应的value:
key:my02
value:02
key:my03
value:03
key:my00
value:00
key:my01
value:01
六、遍历所有的key:
key:my02
value:02
key:my03
value:03
key:my00
value:00
key:my01
value:01
七、遍历所有value:
value:02
value:03
value:00
value:01
[root@cdh-143 shell-test]#

<https://www.cnblogs.com/yy3b2007com/p/11267237.html>