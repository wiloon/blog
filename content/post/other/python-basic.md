---
title: python basic
author: "-"
date: 2013-03-24T02:25:43+00:00
url: python
categories:
  - Python
tags:
  - reprint
  - remix
---
## python basic

## list array, 列表, 数组

### colon syntax

```Python
# check if two list equal
sorted(a) == sorted(b)

: is the delimiter of the slice syntax to 'slice out' sub-parts in sequences , [start:end]

[1:5] is equivalent to "from 1 to 5" (5 not included)
[1:] is equivalent to "1 to end"
```

```Bash
# Python 合并两个列表
# 法一：
# Python合并两个列表, 相加是拼接
list1=[1,2,3]
list2=[4,5,6,7]
list3=list1+list2
print('list3',list3)#输出[1,2,3,4,5,6,7]

# 注意：Python合并两个NumPy数组，相加时候是对应相加
import numpy as  np
arr1=np.array([1,2,3])
arr2=np.array([4,5,6])
arr3=arr1+arr2
print(arr3)#输出[5 7 9]
#那么NumPy数组怎么拼接呢，使用concatenate
arr4=np.concatenate((arr1,arr2),axis=0)
print('arr4',arr4)

# 法二：
l3=[]
l1=[1,2,3]
l2=[4,5,6]
l3.append(l1)
l3.append(l2)
print('l3',l3)#输出[[1, 2, 3], [4, 5, 6]],注意这里是二维列表,不是我们想要的结果

# 如何才能达到我们要的结果，使用 extend
l1.extend(l2)
print('l1',l1)#[1, 2, 3, 4, 5, 6]

# 总结：
# Python合并两个列表，可用两个列表相加存入新列表，或者使用extend在原列表修改
```

————————————————

版权声明：本文为博主原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接和本声明。

原文链接：https://blog.csdn.net/m0_37690430/article/details/117512661

准确来说 Python 中是没有数组类型的，只有列表(list) 和元组（tuple), 数组是 numpy 库中所定义的，所以在使用数组之前必须下载安装 numpy库。 python中 的list 是python 的内置数据类型，list 中的数据类不必相同的，而 array的中的类型必须全部相同。在list 中的数据类型保存的是数据的存放的地址，简单的说就是指针，并非数据，这样保存一个 list 就太麻烦了，例如 `list1=[1,2,3,'a']` 需要4个指针和四个数据，增加了存储和消耗cpu。numpy中封装的 array 有很强大的功能，里面存放的都是相同的数据类型。

1. 列表的特点
   列表是以方括号 [] 包围的数据集合，不同成员以 “，”分隔。如 L = [1,2,3], 列表 a有3个成员。
   列表是可变的数据类型【可进行增删改查】，列表中可以包含任何数据类型，也可以包含另一个列表。如： L = [1,2,[3,4]]，列表L有3个成员，最后一个成员为一个列表。
   列表可以通过序号（索引）访问其中成员，成员序号从0开始，如：a[0]=1。
   列表没有shape，计算列表中成员（元素）的个数，成员以最外层的[ ]中的逗号“，”来分隔，计算方式是len(L)=3, L = [1,2,[3,4]] ，没有数组中的a.shape操作。
   空列表（0个元素的列表）：L=[], 一个元素的列表：L=[1], 多个元素的列表L=[1,2,3]

负数索引表示从右边往左数，最右边的元素的索引为 -1，倒数第二个元素为 -2

## 字典 dict

- dict 是线程安全的

get(key) 方法在 key（键）不在字典中时，可以返回默认值 None 或者设置的默认值。

dict[key] 在 key（键）不在字典中时，会触发 KeyError 异常。

```python

# 空的花括号代表空的 dict
empty_dict = {}
print(empty_dict)

scores = {'语文': 89, '数学': 92, '英语': 93}
# 打印所有的 key
print(scores.keys())
print(scores)

# 使用元组作为 dict 的 key
dict2 = {(20, 30):'good', 30:'bad'}
print(dict2)

# 生成一个字典
d = {'name':Tom, 'age':10, 'Tel':110}

# 打印返回值，其中 d.keys() 是列出字典所有的key
print 'name' in d.keys()
print 'name' in d

# 两个的结果都是返回 True
del test_dict['Zhihu']
```

### dict 遍历

```py
for key, value in dict_0.items():
    print(f"key: {key}, value: {value}")
 
>>> for key in a.keys():
print(key+':'+a[key])

a:1
b:2
c:3

for kv in dict0.items():
    print(kv)

```

#### check if key is exist

```python
dict_1 = {"a": 1, "b":2, "c":3}
if "a" in dict_1:
    print("Exists")
else:
    print("Does not exist")

```

[http://c.biancheng.net/view/2212.html](http://c.biancheng.net/view/2212.html)

dict() 函数用于创建一个字典

python 字典初始化比较常用的两种方式：dict() 和 {}

性能方面，{} 性能更好。

Python 字典(Dictionary) update() 函数把字典 dict2 的键/值对更新到 dict 里。

To delete a key regardless of whether it is in the dictionary, use the two-argument form of dict.pop():

my_dict.pop('key', None)

obj to dict [https://blog.csdn.net/weixin_42359464/article/details/80882549](https://blog.csdn.net/weixin_42359464/article/details/80882549)


## set, hashset

### create set

```Python
foo=set()
foo=set(1)
foo=set([1,2,3])
foo={1,2,3}
```

### 合并 set

```Python
set1 = {"a", "b" , "c"}
set2 = {1, 2, 3}

set1.update(set2)
print(set1)
# {1, 'b', 'c', 2, 3, 'a'}
```

### 交集, `&`

```Python
x = set([1,2,3])
y = set([3,4,5])  

print(x & y)
# {3}
```

### 差集, `-`

```Python
print(x - y)
# {1, 2}
```

```py
1. < 运算符。
表示 左边是否是右边的子集。

> 运算符。
同理，表示右边是否是左边的子集。

<=和>=同理，只是加入了是否两个集合相等的判断。

myset = {"apple", "banana", "cherry"}

>>> l = set()
>>> l.add(1)
>>> l.add(2)
l.remove(1)

', '.join(set_3)

>>> x = set('spam')  
>>> y = set(['h','a','m'])  
>>> x, y
(set(['a', 'p', 's', 'm']), set(['a', 'h', 'm']))    
  
>>> x | y # 并集  
set(['a', 'p', 's', 'h', 'm'])  

# ---
>>> a = set('abracadabra')
>>> b = set('alacazam')

>>> a ^ b # 不同时包含于a和b的元素, # 对称差集（项在a或b中，但不会同时出现在二者中）  
# 并集减交集
{'r', 'd', 'b', 'm', 'z', 'l'}
```

## 类, class

https://blog.csdn.net/yilulvxing/article/details/85374142

```python
class Class0:
    pass
    
# Student 继承 object 类
class Student(object):
    pass

bart = Student()

class Student1(object):
    # __init__ 相当于构造函数
    def __init__(self, name, score):
        self.name = name
        # public 可见 外部可以访问 无 _
        self.score = score
        # protect 不可见 外部可以访问 _(单下划线)
        self._foo = "value0"
        # private 不可见 不可访问 __ (双下划线)
        self.__bar = "value1"

    def print_score(self):
        print('%s: %s' % (self.name, self.score))

    # 类的方法
    # 类内部访问数据的函数
    def get_grade(self):
        if self.score >= 90:
            return 'A'
        elif self.score >= 60:
            return 'B'
        else:
            return 'C'
    
    # 私有函数
    def __foo(self):
        pass

student = Student1()
# object to dict
vars(student)
```

### `getattr()`

`getattr()` 函数用于返回一个对象属性值。

## pip

### archlinux pip

```Bash
# install pip
pacman -S python-pip
```

### ubuntu pip

```Bash
apt install python3-pip

# pip 默认安装路径是 ~.local/bin, 把它加到环境变量里
vim .zshrc
export PATH="$HOME/.local/bin:$PATH"
```

## commands

```bash


# install specific version
yay -S python36

# 打印包版本
pip list

# -r, --requirement <file>    Install from the given requirements file. This option can be used multiple times.
pip install -r requirements.txt

pip freeze #查看当前安装库版本
# 创建 requirements.txt 文件，其中包含了当前环境中所有包及各自的版本的简单列表
# 按 requirements.txt 安装依赖
pip install -r requirements.txt
pip freeze > requirements.txt
pip uninstall kafka
lsvirtualenv        #列举所有的环境
cdvirtualenv        #导航到当前激活的虚拟环境的目录中，相当于 pushd 目录
cdsitepackages      #和上面的类似，直接进入到 site-packages 目录
lssitepackages      #显示 site-packages 目录中的内容
```

## install python

### archlinux install python3.6

```Bash
yay -S python36
```

### install Python from source code on ubuntu

https://stackoverflow.com/questions/52561997/segmentation-fault-during-installation-of-python-3-6-on-debian-8

https://www.python.org/downloads/source/

https://stackoverflow.com/questions/72102435/how-to-install-python3-6-on-ubuntu-22-04

https://www.python.org/ftp/python/

```Bash
sudo apt update

sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev \
libgdbm-dev libnss3-dev libedit-dev libc6-dev

wget https://www.python.org/ftp/python/3.6.15/Python-3.6.15.tgz

tar -xzf Python-3.6.15.tgz

cd Python-3.6.15
./configure --enable-optimizations  -with-lto  --with-pydebug
make -j 8  # adjust for number of your CPU cores
sudo make altinstall
python3.6 -V
```

### ubuntu install python3

```Bash
apt install python3
```

## 查看包依赖树

```Bash
pip install pipdeptree
pipdeptree -p apscheduler
```

## 查看 python 的版本, python version

```bash
python -V
python --version
```

### ubuntu install python

sudo apt install python3
sudo apt install -y python3-venv
mkdir python3-env
cd python3-env
python3 -m venv my_env
source my_env/bin/activate

[https://www.digitalocean.com/community/tutorials/ubuntu-18-04-python-3-zh](https://www.digitalocean.com/community/tutorials/ubuntu-18-04-python-3-zh)

### archlinux install python

```bash
pacman -S python
```

## windows install python

```bash
# 安装 python 11, 默认路径  C:\Users\ywang6\AppData\Local\Programs\Python\Python311
winget install Python.Python.3.11
# --location 目前不好用 winget 版本 v1.4.11071,  --verbose  在安装 python 的时候并没有输出更多日志
winget install Python.Python.3.11 --location "C:\workspace\apps\python11" --verbose
winget install -e -i --id=Python.Python.3.11
winget uninstall Python.Python.3.11

winget install Python.Python.3.6
```

### boolean variable

直接定义a=True/False就行，示例代码：

定义布尔值类型参数a,b，值分别为True,False

a=True

b=False

print a,b

print type(a),type(b)

## python 遍历目录

[http://www.cnblogs.com/vivilisa/archive/2009/03/01/1400968.html](http://www.cnblogs.com/vivilisa/archive/2009/03/01/1400968.html)

[http://laocao.blog.51cto.com/480714/525140](http://laocao.blog.51cto.com/480714/525140)

```python
# !/usr/bin/python
  
import os,sys
  
dir = '/home/wiloon/tmp'
  
list = os.listdir(dir)
  
print list

for line in list:

path = os.path.join(dir, line)

print path
```

```python
import os
import sys
// 打开文件，只读
f = open("/root/tmp/ip.txt", "r")
// 读取文件
lines = f.readlines()
// 字符串长度
print(len(lines))
// for 循环
for line in lines:
# 去空格
    line = line.strip()
    command = "ansible '" + line + "' -m shell -a 'systemctl start filebeat'"
    print(command)
    // 等待用户 输入
    value = input("press any key to continue:")
    // 判断字符串相等
    if value == "q":
    // 退出
        sys.exit(0)
        // 执行 shwll 命令
    os.system(command)
```

## import

```py
import sys
```

导入 sys 模块后，我们就有了变量 sys 指向该模块，利用 sys 这个变量，就可以访问 sys 模块的所有功能。

```python
# import module_name
# import 搜索路径 sys.path, 运行文件所在的目录

# 打印 sys.path
import sys; print(sys.path)

# Python 会在 sys.path 和运行文件目录这两个地方寻找包，然后导入包中名为module_name的模块。
# from package_name import module_name

```

相对导入和绝对导入

相对导入 `from . import m4`

[https://zhuanlan.zhihu.com/p/63143493](https://zhuanlan.zhihu.com/p/63143493)

内置 dir()函数查看对象的属性

from 模块名 import 语句：

from 模块名 import 子模块 或 函数 或 类 或 变量：使用函数调用

导入的不是整个模块，而是 import 后面的函数或变量

注：在调用导入的模块函数使，不使用模块名.函数名 而是 直接使用函数名进行调用

[https://blog.51cto.com/u_15309669/3154639](https://blog.51cto.com/u_15309669/3154639)

## 下划线

- 单下划线开头: 单下划线开头的变量或方法只在内部使用。PEP 8中定义了这个约定（PEP 8是最常用的Python代码风格指南。详见PEP 8：“Style Guide for Python Code”。

[https://geek-docs.com/python/python-examples/python-underline-double-underline-and-others.html](https://geek-docs.com/python/python-examples/python-underline-double-underline-and-others.html)

## __name__

[https://zhuanlan.zhihu.com/p/57309137](https://zhuanlan.zhihu.com/p/57309137)

## 数据类型

### string

```Python
s1 = '  shark  '
print(f"string: '{s1}'")

s1_remove_leading = s1.lstrip()
print(f"remove leading: '{s1_remove_leading}'")

s1_remove_trailing = s1.rstrip()
print(f"remove trailing: '{s1_remove_trailing}'")

s1_remove_both = s1.strip()
print(f"remove both: '{s1_remove_both}'")
```

## 异常处理

```python
def func1():
    # 相当于 java 的  throw new Exception
    raise Exception("--func1 exception--")


def main():
    try:
        func1()
    except Exception as e:
        print e


if __name__ == '__main__':
    main()

```

[https://www.jianshu.com/p/a8cb5375171a](https://www.jianshu.com/p/a8cb5375171a)

## None

None表示空，但它不等于空字符串、空列表，也不等同于False

[https://zhuanlan.zhihu.com/p/65193194](https://zhuanlan.zhihu.com/p/65193194)

## pickle

pickle 提供了一个简单的持久化功能。可以将对象以文件的形式存放在磁盘上。

pickle 模块只能在python中使用，python中几乎所有的数据类型（列表，字典，集合，类等）都可以用pickle来序列化，

pickle 序列化后的数据，可读性差，人一般无法识别。

pickle.dump(obj, file[, protocol])
　　序列化对象，并将结果数据流写入到文件对象中。参数 protocol 是序列化模式，默认值为 0，表示以文本的形式序列化。protocol 的值还可以是1或2，表示以二进制的形式序列化。

pickle.load(file)
　　反序列化对象。将文件中的数据解析为一个Python对象。

## 元组（Tuple）

元组是以圆括号“()”包围的数据集合,括号（）可以省略，不同成员（元素）以逗号“,”分隔，如：T=（1，2,3）。
元组是不可变序列，即元组一旦创建，元组中的数据一旦确立就不能改变，不能对元组中中的元素进行增删改操作，因此元组没有增加元素append、修改元素、删除元素pop的相关方法，只能通过序号（索引）访问元组中的成员,元组中的成员的起始序号为0，如：T[0]=1, T=（1,2,3）。
元组中可以包含任何数据类型，也可以包含另一个元组，如：T=（1,2,3，('a','b')）
空元组（没有元素的元组）：T=（），含1个元素的元组：T=（1，），注意有逗号,多个元素的元组：T=（1,2,3）
任意无符号的对象，以逗号隔开，默认为元组

[https://zhuanlan.zhihu.com/p/210779471](https://zhuanlan.zhihu.com/p/210779471)

## python 虚拟环境

- venv(推荐): Python 标准库内置的虚拟环境管理工具，Python 3.3 加入，Python 3.5 开始作为管理虚拟环境的推荐工具，用法类似 virtualenv。如果你使用 Python 3，推荐使用 venv 来替代 virtualenv
- archlinux> pyenv
- PyPA：指 Python Packaging Authority，一个维护 Python 打包相关项目的小组，相关项目具体见 [https://github.com/pypa](https://github.com/pypa)。
- pip：Python 包安装器。
- virtualenv: Python 虚拟环境管理工具

### venv

```bash
# 创建指定版本的运行环境
/usr/bin/python3.6 -m venv apps/venv-36
# 激活环境 - linux
source apps/venv-36/bin/activate
# 激活环境 - win
env0/script/activate.bat
# 退出环境
deactivate
```

### 删除环境

没有使用 `virtualenvwrapper` 的情况, 可以直接删除 venv 文件夹来删除环境

## `Virtualenvwrapper`

`Virtaulenvwrapper` 是 virtualenv 的扩展包，用于更方便管理虚拟环境，它可以做: - 将所有虚拟环境整合在一个目录下 - 管理（新增，删除，复制）虚拟环境 - 快速切换虚拟环境

```bash
# 安装
# on macOS / Linux
pip install --user virtualenvwrapper

# win
pip install virtualenvwrapper-win

echo "source virtualenvwrapper.sh" >> ~/.zshrc
source ~/.zshrc

# 创建虚拟环境
# on macOS/Linux:
mkvirtualenv --python=python3.6 env0

workon #列出虚拟环境列表
workon [venv] #切换环境

# 退出环境
deactivate
# 删除环境
rmvirtualenv venv
```

### JetBrains Pycharm

settings> Project Interpreters

## pip install python-ldap failed due to cannot `find -lldap_r`

[https://github.com/python-ldap/python-ldap/issues/432](https://github.com/python-ldap/python-ldap/issues/432)

```bash
cat > /usr/lib64/libldap_r.so << EOF
INPUT ( libldap.so )
EOF
```

## RuntimeError: populate() isn't reentrant

This is caused by a bug in your Django settings somewhere. Unfortunately, Django's hiding the bug behind this generic and un-useful error message.

To reveal the true problem, open django/apps/registry.py and around line 80, replace:

raise RuntimeError("populate() isn't reentrant")
with:

self.app_configs = {}
This will allow Django to continue loading, and reveal the actual error.

[https://stackoverflow.com/questions/27093746/django-stops-working-with-runtimeerror-populate-isnt-reentrant](https://stackoverflow.com/questions/27093746/django-stops-working-with-runtimeerror-populate-isnt-reentrant)

ImportError: `libcrypt.so.1`: cannot open shared object file: No such file or directory

```bash
sudo pacman -S libxcrypt-compat
```

## Python -m

通过python -m 执行一个包内脚本会首先将执行package1的__init__.py文件，并且__package__变量被赋上相应的值；而 python xxx.py方式不会执行__init__.py并且__package__变量为None
两种执行方法的sys.path不同（注意每个path输出中的第一条），Python中的sys.path是Python用来搜索包和模块的路径。通过python -m执行一个脚本时会将当前路径加入到系统路径中,而使用python xxx.py执行脚本则会将脚本所在文件夹加入到系统路径中（如果取消inner.py中的注释会报找不到模块的错误）。

[https://a7744hsc.github.io/python/2018/05/03/Run-python-script.html](https://a7744hsc.github.io/python/2018/05/03/Run-python-script.html)

## Django

```bash
python -m pip install Django
python -m django --version
django-admin startproject project0

# 每一次的访问请求重新载入一遍 Python 代码
python manage.py runserver 0.0.0.0:8888
python manage.py runserver 0:8000
python manage.py startapp polls
```

[https://www.djangoproject.com/](https://www.djangoproject.com/)

## `djano` path re_path

如果遇上路径和转换器语法都不足以定义的URL模式，那么就需要使用正则表达式，这时候就需要使用re_path()，而非path()。

[https://www.jianshu.com/p/cd5a91222e1e](https://www.jianshu.com/p/cd5a91222e1e)

import re re --- 正则表达式操作

## python 里的百分号

python里百分号有2个意思，计算数的时候，它是求余数的意思；另外一个是格式化字符串的作用，如："%d %s" %(12, 'abc') 就把%d换成12， %s换成abc，得到 '12 abc'。(推荐学习：Python视频教程)

第一种：数值运算 1 % 3 是指模运算, 取余数(remainder)>>> 7%2

版权声明：本文为`CSDN`博主「谢仁慈Mercy」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：[https://blog.csdn.net/weixin_42502060/article/details/111985588](https://blog.csdn.net/weixin_42502060/article/details/111985588)

## `parse.urlencode()` 与 parse.unquote()

通过parse.unquote()方法进行解码，把 URL编码字符串，转换回原先字符串。

print(parse.unquote("wd=%E4%BC%A0%E6%99%BA%E6%92%AD%E5%AE%A2"))

## json

json.dumps 序列化, 将 Python 对象编码成 JSON 字符串
json.loads 反序列化, 将已编码的 JSON 字符串解码为 Python 对象
json.loads()：解析一个有效的JSON字符串并将其转换为Python字典
json.load()：从一个文件读取JSON类型的数据，然后转转换成Python字典

obj to json [https://blog.csdn.net/mr_hui_/article/details/82941199](https://blog.csdn.net/mr_hui_/article/details/82941199)

## `isinstance()`

`isinstance()` 函数来判断一个对象是否是一个已知的类型，类似 type()。

```Python
x = isinstance(5, int)
isinstance(whatever, bool)
isinstance(value, str)
```

## type()

打印变量类型

```py
logger.info(f"type of xxx: {type(foo)}")
```

## `@staticmethod`

python `staticmethod` 返回函数的静态方法。

该方法不强制要求传递参数，如下声明一个静态方法：

```py
class C(object):
    @staticmethod
    def f(arg1, arg2, ...):
        pass
```

## reduce()

reduce() 函数会对参数序列中元素进行累积。

函数将一个数据集合（链表，元组等）中的所有数据进行下列操作：用传给 reduce 中的函数 function（有两个参数）先对集合中的第 1、2 个元素进行操作，得到的结果再与第三个数据用 function 函数运算，最后得到一个结果。

## operator

operator 模块提供了一套与Python的内置运算符对应的高效率函数。例如，operator.add(x, y) 与表达式 x+y 相同

operator.or_(a, b)
operator.__or__(a, b)
返回 a 和 b 按位或的结果。

## python函数参数前面单星号（*）和双星号（**）的区别

在python的函数中经常能看到输入的参数前面有一个或者两个星号：例如

def foo(param1, *param2):
def bar(param1, **param2):
这两种用法其实都是用来将任意个数的参数导入到python函数中。

单星号（*）：`*agrs`
将所以参数以元组(tuple)的形式导入：
例如：

>>> def foo(param1, *param2):
        print param1
        print param2
>>> foo(1,2,3,4,5)
1
(2, 3, 4, 5)
双星号（**）：`**kwargs`
将参数以字典的形式导入

```python
>>> def bar(param1, **param2):
        print param1
        print param2
>>> bar(1,a=2,b=3)
```

1
{'a': 2, 'b': 3}

## 元组

Python 的元组与列表类似，不同之处在于元组的元素不能修改。

元组使用小括号，列表使用方括号。

元组创建很简单，只需要在括号中添加元素，并使用逗号隔开即可。

## logging

logging的默认级别是 warn

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("foo")
logger.info('info0: %s', value)

## python 命名规范

1、包名：全部小写字母，中间可以由点分隔开，不推荐使用下划线。作为命名空间，包名应该具有唯一性，推荐采用公司或者组织域名的倒置，如com.apple.quicktime.v2。

2、模块名：全部小写字母，如果是多个单词构成，可以用下划线隔开，如 dummy_threading。

3、类名：总是使用首字母大写单词串。如MyClass。内部类可以使用额外的前导下划线。

类总是使用驼峰格式命名，即所有单词首字母大写其余字母小写。类名应该简明，精确，并足以从中理解类所完成的工作。常见的一个方法是使用表示其类型或者特性的后缀，例如:

SQLEngine、MimeTypes。

4、异常名：异常属于类，命名同类命名，但应该使用Error作为后缀。如FileNotFoundError

5、变量名：变量名：全部小写，由下划线连接各个单词。如color = WHITE，this_is_a_variable = 1

*注意*：

1.不论是类成员变量还是全局变量，均不使用 m 或 g 前缀。

2.私有类成员使用单一下划线前缀标识，如_height。多定义公开成员，少定义私有成员。

3.变量名不应带有类型信息，因为Python是动态类型语言。如 iValue、names_list、dict_obj 等都是不好的命名。

## strip

Python中有三个去除头尾字符、空白符的函数，它们依次为:

strip： 用来去除头尾字符、空白符(包括\n、\r、\t、’ '，即：换行、回车、制表符、空格)
`lstrip`：用来去除开头字符、空白符(包括\n、\r、\t、’ '，即：换行、回车、制表符、空格)
`rstrip`：用来去除结尾字符、空白符(包括\n、\r、\t、’ '，即：换行、回车、制表符、空格)

## Python 三目运算符

```py

if contion:
    exp1
else
    exp2

exp1 if contion else exp2
key0 = value0 if exp0 else value1
```

## 函数, function

### 语法

```python
def functionname( parameters ):
   "函数_文档字符串"
   function_suite
   return [expression]

# 定义数据返回值类型
def greeting(name: str) -> str:
  return 'Hello, {}'.format(name)
```

### 示例

```python
def printme( str ):
   "打印传入的字符串到标准显示设备上"
   print str
   return
```

## kafka-python

- PyKafka and
- confluent-kafka
- kafka-python:

python kafka ssl

[https://dev.to/adityakanekar/connecting-to-kafka-cluster-using-ssl-with-python-k2e](https://dev.to/adityakanekar/connecting-to-kafka-cluster-using-ssl-with-python-k2e)

```bash
pip install kafka-python

```

## unit test

```python
# kafkax.py
def send_to_kafka(msg):
    print("send msg to kafka")
    return

# kafkatest.py
import unittest

from kafkax import send_to_kafka


class TestKafka(unittest.TestCase):

    def test_send(self):
        send_to_kafka("foo")

if __name__ == '__main__':
    unittest.main()
```

## split

```python
>>> u = "www.doiido.com.cn"
 
#使用默认分隔符
>>> print u.split()
['www.doiido.com.cn']
 
#以"."为分隔符
>>> print u.split('.')
['www', 'doiido', 'com', 'cn']
```

## python 字符串 str 和字节数组相互转化

```python
b = b"Hello, world!"  # bytes object  
s = "Hello, world!"   # str object 

print('str --> bytes')
print(bytes(s, encoding="utf8"))    
print(str.encode(s))   # 默认 encoding="utf-8"
print(s.encode())      # 默认 encoding="utf-8"

print('\nbytes --> str')
print(str(b, encoding="utf-8"))

# bytes > string
print(bytes.decode(b))  # 默认 encoding="utf-8"
print(b.decode())       # 默认 encoding="utf-8"

```

## singleton, 单例

https://zhuanlan.zhihu.com/p/37534850

[https://www.birdpython.com/posts/1/71/](https://www.birdpython.com/posts/1/71/)

[https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python?page=1&tab=scoredesc#tab-top](https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python?page=1&tab=scoredesc#tab-top)

```Python
from threading import Lock

class FooMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Class0(metaclass=FooMeta):
    foo = None

    def __init__(self) -> None:
        print('init')
    def get(self, key, sub_key):
        print('func 0')
```

## sqlalchemy

[https://www.jianshu.com/p/cf97d753b117](https://www.jianshu.com/p/cf97d753b117)

- pool_timeout, number of seconds to wait before giving up on getting a connection from the pool
- pool_recycle, this setting causes the pool to recycle connections after the given number of seconds has passed

## python 获取 UTC 时间

```python
from datetime import datetime

# time_in_utc variable will be the utc time 
time_in_utc = datetime.utcnow()

# If you want to make it more fancier:
formatted_time_in_utc = time_in_utc.strftime("%d/%m/%Y %H:%M:%S")
```

## python：获取当前目录、上层目录路径

```python
import os


print("===获取当前文件目录===")
# 当前脚本工作的目录路径
print(os.getcwd())
# os.path.abspath()获得绝对路径
print(os.path.abspath(os.path.dirname(__file__)))

print("=== 获取当前文件上层目录 ===")
print(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
print(os.path.abspath(os.path.dirname(os.getcwd())))
print(os.path.abspath(os.path.join(os.getcwd(), "..")))
print(os.path.dirname(os.getcwd()))
# os.path.join()连接目录名与文件或目录


print("==== 设置路径为当前文件上层目录的test_case文件夹====")
path = os.path.join(os.path.dirname(os.getcwd()), "test_case")
print(path)
```

[https://www.cnblogs.com/juankai/p/11580122.html](https://www.cnblogs.com/juankai/p/11580122.html)

## ModuleNotFoundError: No module named 'xlwt'

[https://pypi.org/project/xlwt/#files](https://pypi.org/project/xlwt/#files)

[https://files.pythonhosted.org/packages/44/48/def306413b25c3d01753603b1a222a011b8621aed27cd7f89cbc27e6b0f4/xlwt-1.3.0-py2.py3-none-any.whl](https://files.pythonhosted.org/packages/44/48/def306413b25c3d01753603b1a222a011b8621aed27cd7f89cbc27e6b0f4/xlwt-1.3.0-py2.py3-none-any.whl)

从 下载好的 .whl 包安装模块 pip install foo.whl

## 环境变量

```python
print(os.environ.keys())
print(os.environ['LANG'])
print(os.environ.get('LANG'))
```

## Python 正则

Python正则表达式前的 r 表示原生字符串（`rawstring`），该字符串声明了引号中的内容表示该内容的原始含义，避免了多次转义造成的反斜杠困扰。

关于反斜杠困扰：与多数编程语言相同，正则表达式中使用“\”作为转义字符，如果需要匹配文本中的字符“\”，在正则表达式中需要4个“\”，首先，前2个“\”和后两个“\”在python解释器中分别转义成一个“\”，然后转义后的2个“\”在正则中被转义成一个“\”。

## `djano`

## get 请求参数

```python
start_time = request.GET.get('start_time', default='')
end_time = request.GET.get('end_time', default='')
```

## python list

```py
list1 = ['physics', 'chemistry', 1997, 2000]
list2 = [1, 2, 3, 4, 5 ]
list3 = ["a", "b", "c", "d"]
```

## enum

```py
from enum import Enum
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

# 1
Color.RED.value

# RED
Color(1).name


```

## string

## substring

```Python
string[start:end]：获取从 start 到 end - 1 的所有字符

string[:end]：获取从字符串开头到 end - 1 的所有字符

string[start:]：获取从 start 到字符串末尾的所有字符
```

### string contains

```py
"secret" in title_cased_file_content

# 字符串 大写, upper
stringVar = "welcome to sparkbyexamples"
print(stringVar.upper())

```

## list > string join

```py
 str=[]  #有的题目要输出字符串，但是有时候list更好操作，于是可以最后list转string提交
 for i in range(0,a):
     str.append('M')              
 str1=''.join(str) 

```

## string replace, 字符串 替换

```py
txt = "I like bananas"

x = txt.replace("bananas", "apples")

print(x)

```

## string format

```python
txt = "For only {price:.2f} dollars!"
print(txt.format(price = 49))

```

## string trim

```py
>>>a=" gho stwwl "
>>>a.lstrip()
'gho stwwl '
>>>a.rstrip()
' gho stwwl'
>>>a.strip()
'gho stwwl'
```

## windows python

[https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe](https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe)

### 默认安装路径

C:\Users\user0\AppData\Local\Programs\Python

### uwsgi

windows 下不需要 uwsgi, 生产环境 linux 环境才需要, windows依赖里可以不安装 uwsgi

## setup.py

- build_ext: build C/C++ extensions (compile/link to build directory)，给python编译一个c、c++的拓展
- `–inplace`: ignore build-lib and put compiled extensions into the source directory alongside your pure Python modules，忽略build-lib，将编译后的扩展放到源目录中，与纯Python模块放在一起

-----------------------------------
©著作权归作者所有：来自51CTO博客作者怡宝2号的原创作品，请联系作者获取转载授权，否则将追究法律责任
【python】——setup.py build_ext `--inplace` 命令解析
[https://blog.51cto.com/u_15357586/3788424](https://blog.51cto.com/u_15357586/3788424)

## `faulthandler`

segmentation fault (core dumped) Python Segmentation fault 错误定位办法

```py
import faulthandler
from core.foo import bar

faulthandler.enable()
if __name__ == '__main__':
    bar()
```

```bash
python -X faulthandler main.py
```

## loop

### for

```py
for i in range(1, 10):
    s = "718"
    h = int(hashlib.sha1(s.encode("utf-8")).hexdigest(), 16)
    print(h % 10)
```

### while

```python
i = 1
while i < 6:
  print(i)
  i += 1

```

## string to int

```py
int("10")
```

## int to string

```py
str(10)
```

## sleep

```py
foo_second=10
time.sleep(foo_second)
```

## Milliseconds

```py
import time
obj = time.gmtime(0)
epoch = time.asctime(obj)
print("The epoch is:",epoch)
curr_time = round(time.time()*1000)
print("milliseconds since epoch:",curr_time)
```

## write file

```py
>>> txt_file = open('/Users/michael/test.txt', 'w')
>>> txt_file.write('Hello, world!')
>>> txt_file.close()

os.remove(path) 
```

## 字符串

### 字符串包含

```py
"llo" in "hello, python"
```

## pip

Python 3 >= 3.4 这些版本的 Python 会一并安装 pip

pip install 命令用于安装包

- -U, --upgrade 更新所有指定的包到最新地可用版本。 依赖项的处理取决于所使用的升级策略

```bash
# install redis
pip install redis

# 安装指定版本的包
pip install sasl==0.2.1
pip install "setuptools<58.0.0"

# 查看某个包是否已经安装
pip show --files package0
# 查看过期的包
pip list --outdated

# pip 升级某个包
pip install --upgrade package0
# 卸载
pip uninstall package0

# 安装 whl
pip install foo.whl
```

### 手动重新安装 pip

```bash
curl -O https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
```

### 输出现有环境依赖包目录

```bash
pip freeze > requirements.txt
```

## python 书

[https://zhuanlan.zhihu.com/p/34378860](https://zhuanlan.zhihu.com/p/34378860)

## `@classmethod`

[https://zhuanlan.zhihu.com/p/35643573](https://zhuanlan.zhihu.com/p/35643573)

## Microsoft Visual C++ 14.0 or greater is required

[https://support.microsoft.com/en-us/topic/the-latest-supported-visual-c-downloads-2647da03-1eea-4433-9aff-95f26a218cc0](https://support.microsoft.com/en-us/topic/the-latest-supported-visual-c-downloads-2647da03-1eea-4433-9aff-95f26a218cc0)

## module package

在Python中，一个.py文件就称之为一个模块（Module）。为了避免模块名冲突，Python又引入了按目录来组织模块的方法，称为包（Package）。每一个包目录下面都会有一个__init__.py的文件，这个文件是必须存在的，否则，Python就把这个目录当成普通目录，而不是一个包。__init__.py可以是空文件，也可以有Python代码，因为__init__.py本身就是一个模块，而它的模块名就是 `mycompany`。类似的，可以有多级目录，组成多级层次的包结构。

## code

```py
# int to string
int("7")
```

## 三元运算符

三元运算符通常在Python里被称为条件表达式，这些表达式基于真（true）/假（false）的条件判断，在 Python 2.4 以上才有了三元操作。

```Python
is_fat = True
state = "fat" if is_fat else "not fat"

#另一个晦涩一点的用法比较少见，它使用了元组, 这之所以能正常工作，是因为在Python中，True 等于1，而 False 等于0，这就相当于在元组中使用0和1来选取数据。
fat = True
fitness = ("skinny", "fat")[fat]
print("Ali is", fitness)
```

## ms

```Bash
import time
import datetime

t = time.time()

print (t)                       #原始时间数据
print (int(t))                  #秒级时间戳
print (int(round(t * 1000)))    #毫秒级时间戳

nowTime = lambda:int(round(t * 1000))
print (nowTime());              #毫秒级时间戳，基于lambda

print (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))   #日期格式化
```

## 补零

```Python
n = "123"
s = n.zfill(5)
assert s == "00123"
```

## 字符串拼接

https://cloud.tencent.com/developer/article/1750006

### 逗号

有某种环境下会打印出奇怪的括号, 输出不太友好

```Python
str_a = 'python'
print('hello', str_a, '!') 
```

运行结果：

>hello python !

用逗号拼接的结果中，相邻的两个字符串之间会有空格。 

### 空格

目前用的这种解决 JetBrains 提示代码行过长的问题

```Python
str_b = 'It is summer ' 'of 2019!'
print(str_b) 
```

## python 函数参数前面单星号（*）和双星号（**）的区别

在 python 的函数中经常能看到输入的参数前面有一个或者两个星号：例如

def foo(param1, *param2):
def bar(param1, **param2):

这两种用法其实都是用来将任意个数的参数导入到python函数中。

单星号（*）：`*agrs`
将所以参数以元组(tuple)的形式导入：
例如：

```Bash
>>> def foo(param1, *param2):
print param1
print param2
>>> foo(1,2,3,4,5)
1
(2, 3, 4, 5)
双星号（**）：**kwargs
将参数以字典的形式导入

>>> def bar(param1, **param2):
print param1
print param2
>>> bar(1,a=2,b=3)
1
{'a': 2, 'b': 3}
此外，单星号的另一个用法是解压参数列表：

>>> def foo(bar, lee):
print bar, lee
>>> l = [1, 2]
>>> foo(*l)
1 2
当然这两个用法可以同时出现在一个函数中：例如

>>> def foo(a, b=10, *args, **kwargs):
print a
print b
print args
print kwargs
>>> foo(1, 2, 3, 4, e=5, f=6, g=7)
1
2
3 4
{'e': 5, 'g': 7, 'f': 6}
```

参考资料： http://stackoverflow.com/questions/36901/what-does-double-star-and-star-do-for-python-parameters

## enumerate()

enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，
同时列出数据和数据下标，一般用在 for 循环当中。

## confluent-kafka

```Bash
pip install confluent-kafka
```

```Python
from confluent_kafka import Consumer

c = Consumer({'bootstrap.servers': 'localhost:9092,localhost:9093,localhost:9094'})
c.subscribe(['mytopic'])

try:
    while True:
        msg = c.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            print('Error occured: {}'.format(msg.error()))
        print('Message: {}'.format(msg.value().decode('utf-8')))

except KeyboardInterrupt:
    pass

finally:
    c.close()
```

## 运算符优先级

| 运算符说明 | Python运算符 | 优先级 | 结合性 |
|-------|-----------|-----|-----|
| 逻辑与   | and       | 3   | 左   |
| 逻辑或   | or        | 2   | 左   | 

## uuid to string

a = uuid.uuid1()
str(a)
--> '448096f0-12b4-11e6-88f1-180373e5e84a'

## remote debug

https://debugtalk.com/post/remote-debugging-with-pycharm/


## pdb --- Python 的调试器

源代码： Lib/pdb.py

pdb 模块定义了一个交互式源代码调试器，用于 Python 程序。它支持在源码行间设置（有条件的）断点和单步执行，检视堆栈帧，列出源码列表，以及在任何堆栈帧的上下文中运行任意 Python 代码。它还支持事后调试，可以在程序控制下调用。

Python将多个空格换为一个空格
最近在文本预处理时遇到这个问题，解决方法如下:

```Python
import re
str1 = '  rwe fdsa    fasf   '
str1_after = re.sub(' +', '', str1)
print(str1_after)
```

## pytest

```Bash
# 在项目根目录执行
python -m pytest

# 输出 print
python -m pytest -s

# select one or moure function
python -m pytest -s -k 'test_func_0'
python -m pytest -s -k 'test_func_0 or test_func_1'
```

## errors

```Bash
sudo apt-get install g++
sudo apt-get install libtool
sudo apt-get install flex
sudo apt-get install bison -y
sudo apt-get install byacc -y
# xlocale.h not found
ln -s /usr/include/locale.h /usr/include/xlocale.h
# psycopg2==2.7.3.2
sudo apt-get install libpq-dev

vim ~/.pip/pip.conf
pip install xxx-utils

```

## if

`5 == len(a) == len(b)` 等价于 `5 == len(a) and len(a) == len(b)`

Unlike C, all comparison operations in Python have the same priority,which is lower than that of any arithmetic, 
shifting or `bit` wise operation.

Comparisons can be chained arbitrarily, e.g.,
"x < y <= z" is equivalent to "x < y and y <= z",​……
————————————————

                            版权声明：本文为博主原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接和本声明。

原文链接：https://blog.csdn.net/u013660169/article/details/44587791

## kill process

```Python
import psutil

PROCNAME = "python.exe"

for proc in psutil.process_iter():
    # check whether the process name matches
    if proc.name() == PROCNAME:
        proc.kill()
```

## exec shell script

https://www.cnblogs.com/songzhenhua/p/9312757.html

```Python
command = "echo hello"
shell_script = subprocess.Popen(command, shell=True)
return_code = shell_script.wait()
print(f"return code: {return_code}")
```