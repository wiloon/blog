---
title: python basic
author: "-"
date: 2026-01-29T15:46:00+08:00
url: python
categories:
  - Python
tags:
  - reprint
  - remix
  - AI-assisted
---
## python basic

## 数据类型

### list array, 列表, 数组

#### list/dict str to list/dict

```Python
>>> import ast
>>> x = '[ "A","B","C" , " D"]'
>>> x = ast.literal_eval(x)
>>> x
['A', 'B', 'C', ' D']
>>> x = [n.strip() for n in x]
>>> x
['A', 'B', 'C', 'D']
```

#### colon syntax

```Python
# check if two list equal
sorted(a) == sorted(b)

: is the delimiter of the slice syntax to 'slice out' sub-parts in sequences , [start:end]

[1:5] is equivalent to "from 1 to 5" (5 not included)
[1:] is equivalent to "1 to end"
[:20] from start to 20
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

### string

#### string replace, 字符串 替换

```py
txt = "I like bananas"

x = txt.replace("bananas", "apples")

print(x)

```

```py
str_0 = str_0.replace(r"\\\\n", r"\n")
```

#### string format

```python
txt = "For only {price:.2f} dollars!"
print(txt.format(price = 49))

```

#### string trim

```py
>>>a=" gho stwwl "
>>>a.lstrip()
'gho stwwl '
>>>a.rstrip()
' gho stwwl'
>>>a.strip()
'gho stwwl'
```

## json

json.dumps 序列化, 将 Python 对象编码成 JSON 字符串
json.loads 反序列化, 将已编码的 JSON 字符串解码为 Python 对象
json.loads()：解析一个有效的JSON字符串并将其转换为Python字典
json.load()：从一个文件读取JSON类型的数据，然后转转换成Python字典

obj to json [https://blog.csdn.net/mr_hui_/article/details/82941199](https://blog.csdn.net/mr_hui_/article/details/82941199)


## 字典 dict

- dict 是线程安全的

get(key) 方法在 key（键）不在字典中时，可以返回默认值 None 或者设置的默认值。

dict[key] 在 key（键）不在字典中时，会触发 KeyError 异常。

### 判断 key 在 dict 中是否存在

```Python
foo = {'k0': 'v0', 'k1': 'v1'}
print('k0' in foo)
print('k0' in foo.keys())
print('k2' in foo)

True
True
False
```

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



```Python
car = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}

car.clear()

print(car)
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

### 并集 ` x | y`

```Python
print(x | y)
# {1, 2, 3, 4, 5}
```

### 差集, `-`

```Python
print(x - y)
# {1, 2}
```

### 对称差集 `x ^ y`

对称差集 -- 项在 x 或 y 中，但不会同时出现在二者中
不同时包含于 x 和 y 的元素

并集减交集

```Python
print(x ^ y)
# {1, 2, 4, 5}
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
```

## 对象拷贝 copy

### copy.deepcopy() 深拷贝

Python 中的 `copy.deepcopy()` 函数用于创建对象的深拷贝（deep copy）。深拷贝会递归地复制对象及其包含的所有子对象，生成一个完全独立的新对象。

#### 浅拷贝 vs 深拷贝

**浅拷贝（Shallow Copy）**：

- 只复制对象的第一层，嵌套的对象仍然是引用
- 使用 `copy.copy()` 或切片 `[:]` 创建
- 修改嵌套对象会影响原对象

**深拷贝（Deep Copy）**：

- 递归复制对象及所有嵌套对象
- 使用 `copy.deepcopy()` 创建
- 完全独立，修改不影响原对象

#### 基本用法

```python
import copy

# 简单示例
original = [1, 2, [3, 4]]
deep_copied = copy.deepcopy(original)

# 修改深拷贝的嵌套列表
deep_copied[2][0] = 999
print(original)      # [1, 2, [3, 4]]  - 不受影响
print(deep_copied)   # [1, 2, [999, 4]] - 已修改
```

#### 浅拷贝与深拷贝对比

```python
import copy

original = [1, 2, [3, 4]]

# 浅拷贝
shallow = copy.copy(original)
shallow[2][0] = 999
print(original)  # [1, 2, [999, 4]] - 受影响！

# 深拷贝
original = [1, 2, [3, 4]]
deep = copy.deepcopy(original)
deep[2][0] = 888
print(original)  # [1, 2, [3, 4]] - 不受影响
```

#### 复制自定义对象

```python
import copy

class Person:
    def __init__(self, name, friends):
        self.name = name
        self.friends = friends  # 列表引用

# 原始对象
alice = Person("Alice", ["Bob", "Charlie"])

# 浅拷贝
alice_shallow = copy.copy(alice)
alice_shallow.friends.append("David")
print(alice.friends)  # ['Bob', 'Charlie', 'David'] - 受影响

# 深拷贝
alice = Person("Alice", ["Bob", "Charlie"])
alice_deep = copy.deepcopy(alice)
alice_deep.friends.append("Eve")
print(alice.friends)  # ['Bob', 'Charlie'] - 不受影响
print(alice_deep.friends)  # ['Bob', 'Charlie', 'Eve']
```

#### 复制字典

```python
import copy

original_dict = {
    'name': 'John',
    'age': 30,
    'hobbies': ['reading', 'gaming'],
    'address': {'city': 'Beijing', 'country': 'China'}
}

# 深拷贝字典
copied_dict = copy.deepcopy(original_dict)

# 修改嵌套结构
copied_dict['hobbies'].append('swimming')
copied_dict['address']['city'] = 'Shanghai'

print(original_dict['hobbies'])  # ['reading', 'gaming'] - 不受影响
print(original_dict['address'])  # {'city': 'Beijing', 'country': 'China'} - 不受影响
```

#### 性能注意事项

深拷贝的性能开销较大，因为它需要递归遍历所有嵌套对象：

```python
import copy
import time

# 大型嵌套结构
large_list = [[i] * 100 for i in range(1000)]

# 测量深拷贝时间
start = time.time()
deep_copy = copy.deepcopy(large_list)
print(f"深拷贝耗时: {time.time() - start:.4f} 秒")

# 测量浅拷贝时间
start = time.time()
shallow_copy = copy.copy(large_list)
print(f"浅拷贝耗时: {time.time() - start:.4f} 秒")
```

#### 循环引用处理

`copy.deepcopy()` 可以正确处理循环引用的对象：

```python
import copy

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

# 创建循环引用
node1 = Node(1)
node2 = Node(2)
node1.next = node2
node2.next = node1  # 循环引用

# 深拷贝可以正确处理
copied_node1 = copy.deepcopy(node1)
print(copied_node1.value)  # 1
print(copied_node1.next.value)  # 2
print(copied_node1.next.next.value)  # 1
```

#### 何时使用深拷贝

**适合使用深拷贝的场景**：

- 需要完全独立的对象副本
- 对象包含嵌套的可变类型（列表、字典、自定义对象）
- 需要修改副本而不影响原对象
- 处理复杂的数据结构

**不需要深拷贝的场景**：

- 对象只包含不可变类型（int、str、tuple）
- 只需要复制第一层数据
- 性能要求高且不需要完全独立的副本

#### 自定义深拷贝行为

可以通过实现 `__deepcopy__()` 方法自定义深拷贝行为：

```python
import copy

class CustomClass:
    def __init__(self, data):
        self.data = data
    
    def __deepcopy__(self, memo):
        # 自定义深拷贝逻辑
        print("执行自定义深拷贝")
        new_obj = CustomClass(copy.deepcopy(self.data, memo))
        return new_obj

original = CustomClass([1, 2, 3])
copied = copy.deepcopy(original)
# 输出: 执行自定义深拷贝
```

#### 常见陷阱

**1. 文件对象和网络连接无法深拷贝**：

```python
import copy

f = open('file.txt', 'r')
try:
    copied_f = copy.deepcopy(f)  # TypeError: cannot deepcopy file objects
except TypeError as e:
    print(f"错误: {e}")
```

**2. 某些内置类型会返回自身**：

```python
import copy

# 不可变类型的深拷贝返回自身
x = (1, 2, 3)
y = copy.deepcopy(x)
print(x is y)  # True - 元组是不可变的，直接返回引用
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

### hasattr

对象是否有某一个属性字段

```Bash
op = hasattr(a,'getValue')
```

## 垃圾回收 (Garbage Collection)

Python 的内存管理主要通过自动垃圾回收机制来实现，它结合了**引用计数**和**分代回收**两种策略。

### 垃圾回收策略

#### 1. 引用计数（Reference Counting）

引用计数是 Python 内存管理的主要机制：

```python
import sys

a = [1, 2, 3]
print(sys.getrefcount(a))  # 2（一个是 a，一个是传递给 getrefcount 的参数）

b = a  # 引用计数增加
print(sys.getrefcount(a))  # 3

del b  # 引用计数减少
print(sys.getrefcount(a))  # 2
```

**引用计数的优缺点**：

- ✅ 优点：实时性好，对象引用计数为 0 时立即回收
- ✅ 优点：实现简单，易于理解
- ❌ 缺点：无法处理循环引用
- ❌ 缺点：维护引用计数有额外开销

#### 2. 分代回收（Generational GC）

Python 使用分代回收来解决循环引用问题，将对象分为三代：

- **第 0 代（Generation 0）**：新创建的对象
- **第 1 代（Generation 1）**：经历过 1 次 GC 存活的对象
- **第 2 代（Generation 2）**：经历过多次 GC 存活的对象

**分代假说**：大多数对象朝生夕死，存活时间越长的对象越不容易被回收。

```python
import gc

# 查看当前 GC 阈值
print(gc.get_threshold())  # (700, 10, 10)
# 700: 第 0 代触发阈值
# 10: 第 1 代触发阈值
# 10: 第 2 代触发阈值
```

#### 3. 循环引用检测

Python 通过标记-清除算法检测并处理循环引用：

```python
import gc

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

# 创建循环引用
node1 = Node(1)
node2 = Node(2)
node1.next = node2
node2.next = node1

# 删除引用
del node1
del node2

# 循环引用的对象不会立即被回收（引用计数不为 0）
# 但会在下次 GC 时被检测到并回收
gc.collect()  # 手动触发垃圾回收
```

### GC 配置与控制

Python 的 `gc` 模块提供了丰富的配置选项：

#### 启用/禁用 GC

```python
import gc

# 检查 GC 是否启用
print(gc.isenabled())  # True

# 禁用自动垃圾回收
gc.disable()

# 启用自动垃圾回收
gc.enable()
```

#### 手动触发垃圾回收

```python
import gc

# 手动执行垃圾回收，返回不可达对象数量
collected = gc.collect()
print(f"回收了 {collected} 个对象")

# 指定回收哪一代
gc.collect(0)  # 只回收第 0 代
gc.collect(1)  # 回收第 0、1 代
gc.collect(2)  # 回收所有代（完全回收）
```

#### 配置 GC 阈值

```python
import gc

# 获取当前阈值
thresholds = gc.get_threshold()
print(f"当前阈值: {thresholds}")  # (700, 10, 10)

# 设置新阈值
# 参数含义：(threshold0, threshold1, threshold2)
gc.set_threshold(1000, 15, 15)

# 阈值说明：
# threshold0: 当新分配对象数 - 释放对象数 > 700 时，触发第 0 代回收
# threshold1: 第 0 代回收 10 次后，触发第 1 代回收
# threshold2: 第 1 代回收 10 次后，触发第 2 代回收
```

#### 查看 GC 统计信息

```python
import gc

# 获取每一代的对象数量
print(gc.get_count())  # (581, 7, 3)
# 581: 第 0 代对象数量
# 7: 距离上次第 1 代回收的次数
# 3: 距离上次第 2 代回收的次数

# 获取 GC 统计信息
for i, stats in enumerate(gc.get_stats()):
    print(f"第 {i} 代统计: {stats}")
```

#### 调试和追踪

```python
import gc

# 设置调试标志
gc.set_debug(gc.DEBUG_STATS | gc.DEBUG_LEAK)

# 常用调试标志：
# gc.DEBUG_STATS: 打印回收统计信息
# gc.DEBUG_LEAK: 打印泄漏的对象
# gc.DEBUG_COLLECTABLE: 打印可回收的对象
# gc.DEBUG_UNCOLLECTABLE: 打印无法回收的对象
# gc.DEBUG_SAVEALL: 保存所有对象到 gc.garbage

# 查看所有被追踪的对象
objects = gc.get_objects()
print(f"当前追踪了 {len(objects)} 个对象")

# 查找特定类型的对象
for obj in gc.get_objects():
    if isinstance(obj, dict):
        print(f"发现字典对象: {id(obj)}")
        break

# 查看无法回收的对象（通常是循环引用）
print(gc.garbage)  # []
```

### 性能优化建议

#### 1. 合理使用 GC 控制

```python
import gc
import time

# 对于批量处理，可以临时禁用 GC
def batch_process(data):
    gc.disable()  # 禁用 GC
    try:
        result = [process_item(item) for item in data]
    finally:
        gc.enable()  # 重新启用 GC
        gc.collect()  # 手动触发一次回收
    return result
```

#### 2. 避免循环引用

```python
import weakref

class Node:
    def __init__(self, value):
        self.value = value
        # 使用弱引用避免循环引用
        self._parent = None
    
    def set_parent(self, parent):
        # 使用弱引用
        self._parent = weakref.ref(parent) if parent else None
    
    def get_parent(self):
        return self._parent() if self._parent else None
```

#### 3. 使用上下文管理器

```python
from contextlib import contextmanager
import gc

@contextmanager
def no_gc():
    """临时禁用 GC 的上下文管理器"""
    gc_enabled = gc.isenabled()
    gc.disable()
    try:
        yield
    finally:
        if gc_enabled:
            gc.enable()
            gc.collect()

# 使用示例
with no_gc():
    # 在这里执行不需要 GC 的代码
    big_list = [i for i in range(1000000)]
```

#### 4. 监控内存使用

```python
import gc
import sys

def get_size(obj):
    """递归计算对象大小"""
    size = sys.getsizeof(obj)
    if isinstance(obj, dict):
        size += sum([get_size(v) for v in obj.values()])
        size += sum([get_size(k) for k in obj.keys()])
    elif isinstance(obj, (list, tuple, set)):
        size += sum([get_size(i) for i in obj])
    return size

# 查找内存占用最大的对象
def find_large_objects(limit=10):
    objects = gc.get_objects()
    sizes = [(obj, sys.getsizeof(obj)) for obj in objects]
    sizes.sort(key=lambda x: x[1], reverse=True)
    
    for i, (obj, size) in enumerate(sizes[:limit], 1):
        print(f"{i}. {type(obj).__name__}: {size} bytes")
```

### 实际应用场景

#### 1. 长期运行的服务

```python
import gc
import time

def main_loop():
    gc.set_threshold(1000, 15, 15)  # 调整阈值减少 GC 频率
    
    while True:
        # 处理请求
        process_requests()
        
        # 每小时执行一次完全回收
        if time.time() % 3600 < 1:
            gc.collect(2)
```

#### 2. 内存密集型应用

```python
import gc

def memory_intensive_task():
    # 处理大量数据时禁用 GC
    gc.disable()
    
    try:
        # 创建大量临时对象
        data = process_large_dataset()
        result = analyze_data(data)
    finally:
        # 手动清理并触发回收
        del data
        gc.enable()
        gc.collect()
    
    return result
```

#### 3. 内存泄漏检测

```python
import gc
import sys

def detect_memory_leak():
    # 强制回收所有代
    gc.collect()
    
    # 记录初始对象数
    before = len(gc.get_objects())
    
    # 执行可能泄漏的代码
    suspicious_function()
    
    # 再次回收
    gc.collect()
    
    # 检查对象数变化
    after = len(gc.get_objects())
    leaked = after - before
    
    if leaked > 100:
        print(f"警告：可能存在内存泄漏，增加了 {leaked} 个对象")
        
        # 查找新增的对象类型
        objects = gc.get_objects()[before:after]
        types = {}
        for obj in objects:
            t = type(obj).__name__
            types[t] = types.get(t, 0) + 1
        
        print("新增对象类型：")
        for t, count in sorted(types.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {t}: {count}")
```

### 检查运行中应用的 GC 配置

对于已经在生产环境运行的 Python 应用，有多种方式可以检查其 GC 配置：

#### 1. 通过代码内置检查

最简单的方法是在应用启动时或特定端点输出 GC 配置信息：

```python
import gc
import json

def get_gc_config():
    """获取当前 GC 配置信息"""
    config = {
        "enabled": gc.isenabled(),
        "threshold": gc.get_threshold(),
        "count": gc.get_count(),
        "debug_flags": gc.get_debug(),
        "tracked_objects": len(gc.get_objects()),
        "garbage_objects": len(gc.garbage),
    }
    return config

# 在应用启动时记录
print("GC Configuration:", json.dumps(get_gc_config(), indent=2))

# 或者提供一个健康检查端点（Flask 示例）
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/health/gc')
def gc_status():
    return jsonify(get_gc_config())
```

#### 2. 使用信号处理器实时查看

在运行中的应用中注册信号处理器，通过发送信号来输出 GC 信息：

```python
import gc
import signal
import sys
import json

def handle_gc_info(signum, frame):
    """信号处理器：输出 GC 配置信息"""
    info = {
        "enabled": gc.isenabled(),
        "threshold": gc.get_threshold(),
        "count": gc.get_count(),
        "stats": gc.get_stats(),
    }
    print("\n=== GC Configuration ===", file=sys.stderr)
    print(json.dumps(info, indent=2), file=sys.stderr)
    print("=" * 25 + "\n", file=sys.stderr)

# 注册信号处理器（Unix/Linux）
# SIGUSR1 (信号 10) 用于用户自定义
signal.signal(signal.SIGUSR1, handle_gc_info)

print(f"Process PID: {os.getpid()}")
print("Send SIGUSR1 to view GC info: kill -USR1 <PID>")

# 应用主循环
while True:
    # 你的应用逻辑
    time.sleep(1)
```

使用方法：
```bash
# 查找进程 PID
ps aux | grep python

# 发送信号查看 GC 配置
kill -USR1 <PID>

# 或者使用 pkill
pkill -USR1 -f "your_app.py"
```

#### 3. 使用 Python 调试器 (pdb/ipdb)

如果应用允许，可以附加调试器：

```python
# 在代码中添加远程调试入口
import pdb
import signal

def debug_handler(signum, frame):
    """信号触发调试器"""
    pdb.set_trace()

signal.signal(signal.SIGUSR2, debug_handler)

# 发送信号后在调试器中执行：
# >>> import gc
# >>> gc.isenabled()
# >>> gc.get_threshold()
# >>> gc.get_count()
```

#### 4. 使用 py-spy 性能分析工具

`py-spy` 可以附加到运行中的进程而不修改代码：

```bash
# 安装 py-spy
pip install py-spy

# 查看进程信息（需要 root 权限或进程所有者）
sudo py-spy dump --pid <PID>

# 生成火焰图
sudo py-spy record -o profile.svg --pid <PID>
```

虽然 py-spy 主要用于性能分析，但可以观察到 GC 的影响。

#### 5. 使用日志记录 GC 事件

配置应用定期记录 GC 信息到日志文件：

```python
import gc
import logging
import threading
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gc_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('gc_monitor')

def monitor_gc(interval=60):
    """定期监控 GC 状态"""
    while True:
        info = {
            "enabled": gc.isenabled(),
            "threshold": gc.get_threshold(),
            "count": gc.get_count(),
            "collections": gc.get_stats(),
        }
        logger.info(f"GC Status: {info}")
        time.sleep(interval)

# 启动监控线程
monitor_thread = threading.Thread(target=monitor_gc, args=(300,), daemon=True)
monitor_thread.start()
```

#### 6. 通过 Python 的 gc 回调

设置 GC 回调函数来监控每次垃圾回收：

```python
import gc
import time

def gc_callback(phase, info):
    """
    GC 回调函数
    phase: 'start' 或 'stop'
    info: 包含 generation 和 collected/uncollectable 对象数
    """
    if phase == 'stop':
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] "
              f"GC Generation {info['generation']} completed: "
              f"collected={info['collected']}, "
              f"uncollectable={info['uncollectable']}")

# 设置回调（Python 3.3+）
gc.callbacks.append(gc_callback)
```

#### 7. 使用系统监控工具

结合系统工具监控内存使用情况：

```python
import gc
import psutil
import os

def get_memory_info():
    """获取进程内存和 GC 信息"""
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    
    return {
        "rss_mb": mem_info.rss / 1024 / 1024,  # 物理内存
        "vms_mb": mem_info.vms / 1024 / 1024,  # 虚拟内存
        "gc_enabled": gc.isenabled(),
        "gc_threshold": gc.get_threshold(),
        "gc_count": gc.get_count(),
        "tracked_objects": len(gc.get_objects()),
    }

# 定期输出
import json
while True:
    print(json.dumps(get_memory_info(), indent=2))
    time.sleep(60)
```

#### 8. 在容器环境中检查

如果应用运行在 Docker 容器中：

```bash
# 进入容器
docker exec -it <container_id> bash

# 启动 Python REPL 并附加到进程（需要 pyrasite）
pip install pyrasite
echo "import gc; print(gc.get_threshold())" | pyrasite-shell <PID>

# 或者使用 docker logs 查看输出
docker logs -f <container_id> | grep -i "gc"
```

#### 9. 环境变量检查

某些 GC 行为可以通过环境变量控制：

```bash
# 查看进程环境变量
cat /proc/<PID>/environ | tr '\0' '\n' | grep PYTHON

# 相关环境变量：
# PYTHONGC - 控制 GC 行为
# PYTHONDEBUG - 调试模式
# PYTHONMALLOC - 内存分配器
```

#### 10. 使用专业 APM 工具

生产环境推荐使用专业的应用性能监控工具：

```python
# 使用 Datadog APM
from ddtrace import tracer, patch_all
patch_all()

# 使用 New Relic
import newrelic.agent
newrelic.agent.initialize('newrelic.ini')

# 使用 Prometheus + Python client
from prometheus_client import Gauge, start_http_server
import gc

gc_objects = Gauge('python_gc_objects_tracked', 'Number of objects tracked by GC')
gc_collections = Gauge('python_gc_collections', 'GC collection count', ['generation'])

def update_gc_metrics():
    gc_objects.set(len(gc.get_objects()))
    counts = gc.get_count()
    for gen, count in enumerate(counts):
        gc_collections.labels(generation=gen).set(count)

# 定期更新指标
start_http_server(8000)
while True:
    update_gc_metrics()
    time.sleep(10)
```

#### 实用命令行工具

```bash
# 1. 使用 strace 监控系统调用（间接观察 GC 行为）
strace -p <PID> -e trace=brk,mmap,munmap

# 2. 使用 gdb 附加到进程
gdb -p <PID>
(gdb) call PyGILState_Ensure()
(gdb) call PyRun_SimpleString("import gc; print(gc.get_threshold())")

# 3. 使用 lsof 查看进程打开的文件（包括日志）
lsof -p <PID> | grep log
```

### 生产环境最佳实践

1. **预先内置监控**：在应用中提前加入 GC 监控代码
2. **健康检查端点**：暴露 `/health/gc` 端点便于查看
3. **结构化日志**：使用 JSON 格式记录 GC 信息
4. **定期快照**：每小时记录一次完整的 GC 状态
5. **告警机制**：设置阈值，GC 异常时触发告警
6. **性能基线**：记录正常情况下的 GC 指标作为基线

```python
# 生产环境监控模板
import gc
import logging
import time
from datetime import datetime

class GCMonitor:
    def __init__(self, check_interval=300):
        self.check_interval = check_interval
        self.logger = logging.getLogger('gc_monitor')
        self.baseline = self._get_gc_snapshot()
    
    def _get_gc_snapshot(self):
        return {
            "timestamp": datetime.now().isoformat(),
            "enabled": gc.isenabled(),
            "threshold": gc.get_threshold(),
            "count": gc.get_count(),
            "stats": gc.get_stats(),
            "tracked": len(gc.get_objects()),
            "garbage": len(gc.garbage),
        }
    
    def check_and_alert(self):
        current = self._get_gc_snapshot()
        
        # 检查异常情况
        if current["garbage"] > 0:
            self.logger.warning(f"发现无法回收的对象: {current['garbage']}")
        
        tracked_increase = current["tracked"] - self.baseline["tracked"]
        if tracked_increase > 10000:
            self.logger.warning(
                f"追踪对象数异常增长: {tracked_increase}"
            )
        
        self.logger.info(f"GC Status: {current}")
        return current
    
    def run(self):
        while True:
            self.check_and_alert()
            time.sleep(self.check_interval)

# 使用示例
if __name__ == "__main__":
    monitor = GCMonitor(check_interval=300)  # 每5分钟检查一次
    monitor.run()
```

### 关键要点总结

**GC 策略**：
1. 主要依赖引用计数（实时回收）
2. 分代回收处理循环引用
3. 标记-清除算法检测循环引用

**是否可配置**：
✅ 可以配置：
- 启用/禁用 GC
- 调整阈值参数
- 手动触发回收
- 设置调试标志
- 选择回收哪一代

**最佳实践**：
- 大多数情况下使用默认配置即可
- 批量处理时可临时禁用 GC
- 避免手动管理内存，除非有性能瓶颈
- 使用弱引用避免循环引用
- 定期监控内存使用情况

## pip

pip 是 Python 的包管理工具，全称是 “Pip Installs Packages”。它用于安装、更新、卸载 Python 包（也叫模块、库）。

```Bash
# 查看是否安装了 pip
pip --version
# archlinux install pip
pacman -S python-pip

# 使用普通用户安装包（用户级安装）
python3.14 -m pip install --user package_name

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
pip list | grep requests

# 查看某一个包的信息
pip show django

# -r, --requirement <file>    Install from the given requirements file. This option can be used multiple times.
pip install -r requirements.txt

sudo pip install --proxy http://<usr_name>:<password>@<proxyserver_name>:<port#> <pkg_name> 

pip freeze #查看当前安装库版本

pip freeze |grep 
# 创建 requirements.txt 文件，其中包含了当前环境中所有包及各自的版本的简单列表
# 按 requirements.txt 安装依赖
pip install -r requirements.txt
# [SSL: CERTIFICATE_VERIFY_FAILED]
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org <package_name>
pip freeze > requirements.txt
pip uninstall kafka
lsvirtualenv        #列举所有的环境
cdvirtualenv        #导航到当前激活的虚拟环境的目录中，相当于 pushd 目录
cdsitepackages      #和上面的类似，直接进入到 site-packages 目录
lssitepackages      #显示 site-packages 目录中的内容
```

## install python

```Bash
# archlinux install python3.6
yay -S python36
```

## ubuntu24.04 install python3.6

install Python from source code on ubuntu

https://stackoverflow.com/questions/52561997/segmentation-fault-during-installation-of-python-3-6-on-debian-8

https://www.python.org/downloads/source/

https://stackoverflow.com/questions/72102435/how-to-install-python3-6-on-ubuntu-22-04

https://www.python.org/ftp/python/

```Bash
sudo apt update && sudo apt upgrade

wget https://www.python.org/ftp/python/3.6.15/Python-3.6.15.tgz
tar -xzf Python-3.6.15.tgz
cd Python-3.6.15

sudo apt install -y \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libgdbm-dev \
    libdb5.3-dev \
    libbz2-dev \
    libexpat1-dev \
    liblzma-dev \
    tk-dev \
    libffi-dev \
    wget

./configure --prefix=/opt/python3.6 --with-openssl=/usr
make -j$(nproc)
sudo make install
/opt/python3.6/bin/python3.6 -V

---
./configure --with-pydebug --enable-loadable-sqlite-extensions
./configure --with-pydebug
./configure --enable-optimizations  -with-lto  --with-pydebug

# adjust for number of your CPU cores
make -j 8
sudo make altinstall
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

[https://www.digitalocean.com/community/tutorials/ubuntu-18-04-python-3-zh](https://www.digitalocean.com/community/tutorials/ubuntu-18-04-python-3-zh)

```bash
# archlinux install python
pacman -S python
```

## windows install python

```bash
# 安装 python 11, 默认路径  C:\Users\user_0\AppData\Local\Programs\Python\Python311
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
class FooException(Exception):
    pass

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

Python 生态系统中有多个工具用于管理 Python 版本和虚拟环境，它们各有特点和适用场景。

### Python 环境管理工具概览

#### 工具分类与职责

Python 生态系统中的工具可以按功能分为四个层次：

**1. Python 版本管理**
- **pyenv** ⭐：管理多个 Python 版本的安装和切换（推荐单语言）
  - 功能：安装 Python 3.10、3.11、3.12 等不同版本
  - 适用：只需要管理 Python 版本
  - 优势：专注 Python，简单易用
- **asdf** ⭐：通用的多语言版本管理器（推荐多语言开发者）
  - 功能：管理多种语言的版本（Python、Node.js、Ruby、Go 等）
  - 适用：多语言项目、全栈开发
  - 优势：统一工具管理所有语言版本
  - 插件系统：通过插件支持 150+ 语言和工具

**2. 虚拟环境管理**
- **venv** ⭐：Python 标准库内置，轻量级（推荐）
  - 功能：创建项目级的独立 Python 环境
  - 适用：一般项目开发
  - Python 3.3+ 内置
- **virtualenv**：功能更强大的虚拟环境工具
  - 功能：与 venv 类似，但支持更多 Python 版本
  - 适用：需要支持 Python 2.x 或旧版本 Python 3

**3. 项目管理工具**
- **pdm** ⭐：现代化的项目管理器（推荐 Python 3.9+）
  - 功能：依赖管理 + 锁文件 + 构建 + 发布
  - 遵循：PEP 582、PEP 621 标准
  - 适用：完整的项目生命周期管理
  - 可配合 uv 使用
- **poetry**：另一个流行的项目管理工具
  - 功能：与 pdm 类似，依赖管理和构建
  - 生态：社区大、插件多
- **pipenv**：较早的项目管理工具
  - 状态：不太推荐（维护不够活跃）

**4. 包安装工具**
- **pip**：Python 官方包安装器
  - 功能：从 PyPI 安装和管理包
  - 维护：Python Package Authority (PyPA)
  - 状态：标准工具，但速度较慢
- **uv** ⭐：极速包安装器（推荐）
  - 功能：完全替代 pip，速度快 10-100 倍
  - 技术：Rust 编写，兼容 pip 接口
  - 适用：追求性能、大型项目、CI/CD
  - 可配合 venv、pdm 使用

**5. 其他工具**
- **PyPA**：Python Packaging Authority，维护 Python 打包相关项目的小组
  - 项目：pip、virtualenv、setuptools、wheel 等
  - 网站：[https://github.com/pypa](https://github.com/pypa)

#### 快速选择指南

```
需要多个 Python 版本？        → pyenv
需要项目环境隔离？           → venv (标准) 或 virtualenv
需要完整项目管理？           → pdm 或 poetry
需要快速安装包？             → uv（替代 pip）
简单脚本？                  → pip（默认即可）
```

#### 是否冲突？

| 工具 A | 工具 B | 是否冲突 | 说明 |
|--------|--------|---------|------|
| pyenv | venv | ❌ 不冲突 | 配合使用，pyenv 选版本，venv 创建环境 |
| pyenv | pdm | ❌ 不冲突 | 配合使用，pyenv 选版本，pdm 管理项目 |
| pyenv | uv | ❌ 不冲突 | 配合使用，pyenv 选版本，uv 安装包 |
| venv | pdm | ⚠️ 部分重叠 | pdm 可不用 venv（PEP 582），但也可配合 |
| pdm | uv | ❌ 不冲突 | 配合使用，pdm 管理项目，uv 加速安装 |
| pip | uv | ✅ 互斥 | uv 完全替代 pip，二选一 |
| venv | virtualenv | ✅ 互斥 | 功能相同，选一个即可 |

### pyenv - Python 版本管理（推荐）

**pyenv** 是管理多个 Python 版本的**首选工具**，特别适合需要在本地同时安装和使用多个 Python 版本的场景。

#### 为什么推荐 pyenv？

1. **版本隔离完美**
   - 每个 Python 版本独立安装在 `~/.pyenv/versions/` 目录
   - 不会影响系统自带的 Python
   - 不需要 root/sudo 权限

2. **灵活的版本切换**
   - 全局版本：整个系统的默认 Python 版本
   - 本地版本：特定项目目录使用的版本（通过 `.python-version` 文件）
   - Shell 版本：当前终端会话的临时版本

3. **支持多种 Python 实现**
   - CPython（官方实现）
   - PyPy（JIT 编译器）
   - Anaconda、Miniconda
   - Jython、IronPython 等

4. **自动版本切换**
   - 进入项目目录时自动切换到该项目指定的 Python 版本
   - 通过 `.python-version` 文件实现

5. **与其他工具完美配合**
   - 可以与 venv、virtualenv、pdm 等虚拟环境工具配合使用
   - 与 pipenv、poetry 等包管理工具兼容

#### 基本用法

```bash
# 安装 pyenv (macOS/Linux)
curl https://pyenv.run | bash

# 配置环境变量（添加到 ~/.bashrc 或 ~/.zshrc）
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# archlinux 安装 pyenv
yay -S pyenv

# 列出可安装的 Python 版本
pyenv install --list

# 列出可安装的 CPython 版本
pyenv install --list | grep "^  3\."

# 安装指定版本
pyenv install 3.12.0
pyenv install 3.11.5
pyenv install 3.10.13

# 列出已安装的版本
pyenv versions

# 查看当前使用的版本
pyenv version

# 设置全局 Python 版本（整个系统默认）
pyenv global 3.12.0

# 设置当前项目的 Python 版本（创建 .python-version 文件）
cd /path/to/project
pyenv local 3.11.0

# 设置 shell 会话的 Python 版本（临时）
pyenv shell 3.10.0

# 取消 shell 版本设置
pyenv shell --unset

# 卸载指定版本
pyenv uninstall 3.10.0

# 更新 pyenv
cd ~/.pyenv && git pull
```

#### 实际使用场景

**场景 1：不同项目使用不同 Python 版本**

```bash
# 项目 A 使用 Python 3.11
cd ~/projects/project-a
pyenv local 3.11.5
python --version  # Python 3.11.5

# 项目 B 使用 Python 3.12
cd ~/projects/project-b
pyenv local 3.12.0
python --version  # Python 3.12.0

# 自动切换：每次进入目录，pyenv 自动切换版本
```

**场景 2：测试代码在多个 Python 版本的兼容性**

```bash
# 在 Python 3.10 下测试
pyenv shell 3.10.13
python test.py

# 在 Python 3.11 下测试
pyenv shell 3.11.5
python test.py

# 在 Python 3.12 下测试
pyenv shell 3.12.0
python test.py
```

**场景 3：配合虚拟环境使用**

```bash
# 先用 pyenv 选择 Python 版本
pyenv local 3.11.5

# 再创建虚拟环境
python -m venv .venv
source .venv/bin/activate

# 虚拟环境使用的是 pyenv 指定的 Python 3.11.5
python --version
```

#### Python 版本管理工具对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **pyenv** ⭐ | 专注 Python、易用、隔离好 | 需要编译安装（较慢） | **只用 Python 的开发者** |
| **asdf** ⭐ | 统一管理多语言版本 | 配置相对复杂 | **多语言开发者** |
| **系统包管理器** | 安装快速 | 版本选择少、可能冲突 | 简单脚本 |
| **官方安装包** | 官方支持 | 多版本共存麻烦 | Windows 用户 |
| **Anaconda/Miniconda** | 包含科学计算包 | 体积大、环境复杂 | 数据科学项目 |
| **Docker** | 完全隔离 | 开销大、复杂 | 生产环境测试 |

#### pyenv 安装依赖

在某些系统上，安装 Python 需要编译依赖：

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
libffi-dev liblzma-dev

# CentOS/Fedora
sudo yum install gcc zlib-devel bzip2 bzip2-devel readline-devel \
sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel

# macOS (需要 Homebrew)
brew install openssl readline sqlite3 xz zlib
```

#### 总结

**pyenv 是在本地管理多个 Python 版本的最佳选择**，因为它：
- ✅ 简单易用，学习曲线平缓
- ✅ 版本隔离完美，不影响系统 Python
- ✅ 灵活的版本切换机制（全局/项目/临时）
- ✅ 与虚拟环境工具完美配合
- ✅ 活跃的社区支持和维护

**推荐组合**：`pyenv + venv + pip`（或 `pyenv + pdm`）用于日常 Python 开发。

### asdf - 通用版本管理器

**asdf** 是一个可扩展的通用版本管理器，通过插件系统支持管理多种编程语言和工具的版本。

#### 什么是 asdf？

**asdf** 设计理念是"一个工具管理所有语言版本"，适合需要同时使用多种编程语言的开发者。

**核心特点：**
- 📦 统一管理多种语言版本（Python、Node.js、Ruby、Go、Java 等）
- 🔌 插件系统：150+ 官方和社区插件
- 📁 项目级版本控制（.tool-versions 文件）
- 🔄 自动版本切换
- 🌐 跨平台支持（Linux、macOS）

#### asdf vs pyenv

| 特性 | pyenv | asdf |
|------|-------|------|
| 管理语言 | 仅 Python | 多语言（Python、Node.js、Ruby 等） |
| 使用复杂度 | 简单 | 中等（需要了解插件） |
| Python 专注度 | 高 | 低（通用工具） |
| 适用场景 | 纯 Python 开发 | 多语言/全栈开发 |
| 配置文件 | `.python-version` | `.tool-versions` |
| 社区活跃度 | 高（Python） | 高（多语言） |

#### 何时选择 asdf？

**推荐使用 asdf 的场景：**
- ✅ 全栈开发（前端 Node.js + 后端 Python）
- ✅ 微服务项目（多种语言混合）
- ✅ 需要管理多种工具版本（Terraform、kubectl 等）
- ✅ 统一团队的版本管理工具

**不推荐使用 asdf 的场景：**
- ❌ 只用 Python（pyenv 更简单）
- ❌ 新手学习 Python（增加学习负担）
- ❌ Windows 用户（asdf 不支持 Windows）

#### 安装 asdf

```bash
# macOS/Linux - Git 安装方式
git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.13.1

# 配置环境变量（添加到 ~/.bashrc 或 ~/.zshrc）
. "$HOME/.asdf/asdf.sh"
. "$HOME/.asdf/completions/asdf.bash"

# macOS - Homebrew 安装
brew install asdf

# Ubuntu - 使用包管理器
sudo apt install asdf

# 验证安装
asdf --version
```

#### 使用 asdf 管理 Python

```bash
# 1. 安装 Python 插件
asdf plugin add python

# 2. 列出可安装的 Python 版本
asdf list all python

# 3. 安装指定版本
asdf install python 3.12.0
asdf install python 3.11.5
asdf install python 3.10.13

# 4. 设置全局版本
asdf global python 3.12.0

# 5. 设置项目本地版本
cd /path/to/project
asdf local python 3.11.5

# 6. 设置 shell 临时版本
asdf shell python 3.10.13

# 7. 列出已安装的版本
asdf list python

# 8. 查看当前版本
asdf current python

# 9. 卸载指定版本
asdf uninstall python 3.10.0
```

#### 管理多种语言

**asdf 的核心优势：统一管理多种语言**

```bash
# 安装 Node.js 插件
asdf plugin add nodejs
asdf install nodejs 20.10.0
asdf global nodejs 20.10.0

# 安装 Ruby 插件
asdf plugin add ruby
asdf install ruby 3.2.0
asdf global ruby 3.2.0

# 安装 Go 插件
asdf plugin add golang
asdf install golang 1.21.5
asdf global golang 1.21.5

# 查看所有已安装的插件
asdf plugin list

# 查看所有语言的当前版本
asdf current
```

#### .tool-versions 文件

**项目级版本控制：**

```bash
# 在项目根目录创建 .tool-versions 文件
cd /path/to/project
cat > .tool-versions << EOF
python 3.11.5
nodejs 20.10.0
ruby 3.2.0
EOF

# 进入项目目录，asdf 自动切换所有工具版本
cd /path/to/project
python --version  # 3.11.5
node --version    # 20.10.0
ruby --version    # 3.2.0

# 团队成员只需：
git clone <repo>
cd <repo>
asdf install  # 自动安装 .tool-versions 中的所有版本
```

#### 实际使用场景

**场景 1：全栈项目（Python + Node.js）**

```bash
# 项目目录
cd ~/projects/fullstack-app

# 配置版本
asdf local python 3.12.0
asdf local nodejs 20.10.0

# .tool-versions 文件内容
cat .tool-versions
# python 3.12.0
# nodejs 20.10.0

# 每次进入项目，版本自动切换
cd ~/projects/fullstack-app
python --version  # 3.12.0
node --version    # 20.10.0
```

**场景 2：DevOps 工具管理**

```bash
# 管理各种 DevOps 工具的版本
asdf plugin add terraform
asdf plugin add kubectl
asdf plugin add helm

asdf install terraform 1.6.0
asdf install kubectl 1.28.0
asdf install helm 3.13.0

asdf global terraform 1.6.0
asdf global kubectl 1.28.0
asdf global helm 3.13.0
```

#### asdf 配置 Python 编译依赖

使用 asdf 安装 Python 时，也需要编译依赖（与 pyenv 相同）：

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
libffi-dev liblzma-dev

# macOS
brew install openssl readline sqlite3 xz zlib
```

#### pyenv vs asdf：如何选择？

**选择 pyenv，如果你：**
- 🐍 主要或只使用 Python
- 📚 刚开始学习 Python
- 🎯 需要专注的 Python 工具
- ⚡ 想要更简单的配置

**选择 asdf，如果你：**
- 🌐 使用多种编程语言（Python、Node.js、Ruby 等）
- 🔧 需要管理多种工具版本（Terraform、kubectl 等）
- 👥 团队使用多种语言
- 🎨 全栈开发
- 📦 希望统一版本管理工具

#### 总结

**asdf 适合多语言开发者：**
- ✅ 一个工具管理所有语言版本
- ✅ 统一的 `.tool-versions` 文件
- ✅ 强大的插件生态
- ⚠️ 配置相对复杂
- ⚠️ 不支持 Windows

**推荐组合：**
- 纯 Python 开发：`pyenv + venv + uv`
- 多语言开发：`asdf + venv + uv`
- 全栈项目：`asdf`（管理 Python + Node.js + 其他工具）

### venv - 标准库虚拟环境

**venv** 是 Python 3.3+ 内置的虚拟环境模块，推荐用于替代 virtualenv。

**主要特点：**
- Python 标准库内置，无需额外安装
- 轻量级，功能足够日常使用
- 为每个项目创建独立的 Python 环境
- 隔离项目依赖，避免包冲突

**基本用法：**

```bash
# 安装 venv (某些发行版需要)
sudo apt install -y python3-venv

# 创建虚拟环境
python3 -m venv myenv

# 创建指定 Python 版本的虚拟环境
/usr/bin/python3.6 -m venv apps/venv-36

# 激活环境 - Linux/macOS
source myenv/bin/activate

# 激活环境 - Windows
myenv\Scripts\activate.bat

# 退出环境
deactivate

# 删除环境（直接删除目录）
rm -rf myenv

# 判断当前是否在虚拟环境里
which python
```

### pdm - 现代化包管理器

**pdm** 是新一代 Python 项目管理工具，遵循 PEP 582 标准，提供完整的项目生命周期管理。

#### pdm 的设计目标

**pdm 解决的问题：**
- ✅ 项目依赖管理（添加、更新、锁定）
- ✅ 项目元数据管理（pyproject.toml）
- ✅ 构建和发布 Python 包
- ✅ 脚本和任务管理
- ✅ 开发依赖分组管理
- ❌ **不提供** Python 版本安装功能
- ⚠️ 依赖安装速度不如 uv（但可以配合使用）

**主要特点：**
- 不需要虚拟环境，使用 `__pypackages__` 目录（PEP 582）
- 内置依赖解析器，生成锁文件（类似 npm/yarn）
- 支持 PEP 621 项目元数据标准
- 快速的依赖安装和解析
- 支持插件系统
- 要求 Python 3.9+

#### 基本用法

```bash
# 安装 pdm
pip install --user pdm

# 初始化项目
pdm init

# 添加依赖
pdm add requests
pdm add pytest --dev  # 开发依赖
pdm add -G docs sphinx  # 添加到 docs 组

# 安装所有依赖
pdm install

# 只安装生产依赖
pdm install --prod

# 运行脚本
pdm run python script.py

# 运行自定义命令（定义在 pyproject.toml）
pdm run test
pdm run lint

# 更新依赖
pdm update
pdm update requests  # 只更新指定包

# 列出依赖
pdm list
pdm list --tree  # 树形显示依赖

# 显示依赖信息
pdm show requests

# 移除依赖
pdm remove requests

# 导出 requirements.txt
pdm export -o requirements.txt
```

**项目结构：**
```
myproject/
├── pyproject.toml      # 项目配置和依赖
├── pdm.lock           # 锁文件（确保一致性）
└── __pypackages__/    # 依赖包目录（PEP 582）
```

#### pdm 配合 uv 使用

**重要**：pdm 和 uv 功能互补，可以一起使用！

**pdm 的优势：**
- 完整的项目管理功能
- 依赖分组（开发、测试、文档等）
- 脚本和任务管理
- 构建和发布包

**uv 的优势：**
- 极快的包安装速度

**配合使用：**

```bash
# 方案 1：pdm 使用 uv 作为安装后端
# 在 pyproject.toml 中配置
[tool.pdm]
install.cache = true
install.cache-method = "symlink"

# pdm 会自动检测并使用 uv（如果已安装）
pdm install

# 方案 2：手动结合使用
# 用 pdm 管理依赖，用 uv 安装
pdm export -o requirements.txt
uv pip install -r requirements.txt

# 方案 3：pdm 配置使用 uv
pdm config install.use-uv true
```

#### pdm 的完整工作流

```bash
# 1. 初始化项目
pdm init

# 2. 添加依赖
pdm add fastapi uvicorn
pdm add pytest pytest-cov --dev

# 3. 配置脚本（在 pyproject.toml 中）
[tool.pdm.scripts]
start = "uvicorn main:app --reload"
test = "pytest tests/"
lint = "ruff check ."

# 4. 运行项目
pdm run start

# 5. 运行测试
pdm run test

# 6. 锁定依赖
pdm lock

# 7. 在其他环境安装（使用锁文件）
pdm install
```

### uv - 极速包安装器

**uv** 是用 Rust 编写的超快速 Python 包安装器和解析器，由 Astral 团队开发（ruff 的开发者）。

#### uv 的设计目标

⚠️ **重要说明**：uv 的核心目标是**快速安装和解析 Python 包**，而不是管理多个 Python 版本。

**uv 解决的问题：**
- ✅ 加速包的安装过程（比 pip 快 10-100 倍）
- ✅ 快速依赖解析
- ✅ 可靠的依赖锁定
- ✅ 虚拟环境管理
- ❌ **不提供** Python 版本安装和管理功能

**主要特点：**
- 比 pip 快 10-100 倍（用 Rust 编写）
- **完全兼容 pip 命令**，可作为 pip 的直接替代品
- 内置快速的依赖解析器
- 支持虚拟环境创建和管理
- 跨平台支持（Linux、macOS、Windows）
- 零 Python 依赖（独立二进制文件）
- 支持 pip-tools 风格的工作流

#### uv 可以完全替代 pip

**是的，uv 设计为 pip 的即插即用替代品！**

所有 `pip` 命令都可以用 `uv pip` 替代：

```bash
# pip 命令               →  uv 命令
pip install requests     →  uv pip install requests
pip install -r req.txt   →  uv pip install -r req.txt
pip install -e .         →  uv pip install -e .
pip uninstall package    →  uv pip uninstall package
pip list                 →  uv pip list
pip show package         →  uv pip show package
pip freeze               →  uv pip freeze
pip search term          →  uv pip search term
```

**几乎所有 pip 的功能 uv 都支持：**
- ✅ 从 PyPI 安装包
- ✅ 安装本地包（wheel、源码）
- ✅ 从 Git 仓库安装
- ✅ requirements.txt 支持
- ✅ 可编辑模式安装（-e）
- ✅ 约束文件（constraints.txt）
- ✅ 环境变量和配置文件
- ✅ 代理和认证支持

#### 使用场景

**适合 uv 的场景：**
- 大型项目需要安装大量依赖包
- CI/CD 流水线中加速依赖安装
- 频繁切换项目和重建环境
- 需要精确的依赖锁定

**不适合 uv 的场景：**
- ❌ 需要安装和管理多个 Python 版本（用 pyenv）
- ❌ 需要完整的项目管理功能（用 pdm、poetry）

#### 基本用法

```bash
# ============ 安装 uv ============
# 方式 1：官方安装脚本（推荐）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 方式 2：使用 pip 安装
pip install uv

# 方式 3：使用包管理器
# macOS
brew install uv
# Arch Linux
yay -S uv

# ============ 创建虚拟环境 ============
# 创建虚拟环境（使用当前系统的 Python）
uv venv

# 创建指定名称的虚拟环境
uv venv myenv

# 使用指定 Python 版本创建环境（前提：该版本已安装）
uv venv --python python3.11
uv venv --python 3.12

# ============ 安装包（替代 pip install）============
# 基本安装
uv pip install requests

# 安装多个包
uv pip install requests pandas numpy

# 指定版本
uv pip install "requests==2.31.0"
uv pip install "django>=4.0,<5.0"

# 从 requirements.txt 安装
uv pip install -r requirements.txt

# 可编辑模式安装（开发模式）
uv pip install -e .
uv pip install -e .[dev]

# 从 Git 安装
uv pip install git+https://github.com/user/repo.git

# ============ 其他常用命令 ============
# 升级包
uv pip install --upgrade requests
uv pip install -U requests

# 列出已安装的包
uv pip list
uv pip list --format json

# 显示包信息
uv pip show requests

# 导出已安装的包
uv pip freeze
uv pip freeze > requirements.txt

# 卸载包
uv pip uninstall requests
uv pip uninstall -r requirements.txt

# ============ 高级功能 ============
# 编译依赖（生成锁定的 requirements.txt）
uv pip compile pyproject.toml -o requirements.txt
uv pip compile requirements.in -o requirements.txt

# 同步依赖（安装并移除不需要的包）
uv pip sync requirements.txt

# 检查包的兼容性
uv pip check
```

#### 直接替代 pip 的方法

**方式 1：命令行别名（推荐用于学习）**

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
alias pip='uv pip'

# 之后就可以直接用 pip 命令，实际执行的是 uv
pip install requests  # 实际执行：uv pip install requests
```

**方式 2：使用 uv 的 pip 子命令**

```bash
# 始终使用 uv pip 前缀
uv pip install requests
uv pip list
uv pip uninstall requests
```

**方式 3：创建软链接（不推荐）**

```bash
# 可能会导致混淆，不推荐
ln -s $(which uv) /usr/local/bin/pip
```

#### 与 pip 的性能对比

**真实场景测试：**

```bash
# 场景 1：安装 Django 及其依赖
pip install django          # ~15 秒
uv pip install django       # ~1-2 秒
# 速度提升：8-15 倍

# 场景 2：安装 pandas（含 numpy 等依赖）
pip install pandas          # ~25 秒
uv pip install pandas       # ~2-3 秒
# 速度提升：8-12 倍

# 场景 3：从 requirements.txt 安装 50 个包
pip install -r requirements.txt    # ~120 秒
uv pip install -r requirements.txt # ~8-10 秒
# 速度提升：12-15 倍

# 场景 4：重新安装（有缓存）
pip install --force-reinstall requests  # ~5 秒
uv pip install --reinstall requests     # ~0.5 秒
# 速度提升：10 倍
```

**为什么 uv 这么快？**
- 🦀 用 Rust 编写（原生性能）
- 📦 并行下载和安装
- 💾 高效的缓存机制
- 🔧 更快的依赖解析算法

#### pip 和 uv 的功能对比

| 功能 | pip | uv | 说明 |
|------|-----|-----|------|
| 安装包 | ✅ | ✅ | `uv pip install` |
| 卸载包 | ✅ | ✅ | `uv pip uninstall` |
| 列出包 | ✅ | ✅ | `uv pip list` |
| 导出依赖 | ✅ | ✅ | `uv pip freeze` |
| requirements.txt | ✅ | ✅ | 完全兼容 |
| 可编辑安装 | ✅ | ✅ | `uv pip install -e .` |
| Git 安装 | ✅ | ✅ | 支持 |
| 依赖锁定 | ❌ | ✅ | `uv pip compile` |
| 依赖同步 | ❌ | ✅ | `uv pip sync` |
| 速度 | 慢 | **极快** | 10-100 倍提升 |
| 内存占用 | 高 | 低 | Rust 优化 |

#### 何时使用 uv 替代 pip？

**推荐使用 uv 的场景：**
- ✅ 大型项目（依赖包多）
- ✅ CI/CD 流水线（加速构建）
- ✅ 频繁安装依赖的开发环境
- ✅ 需要依赖锁定的项目
- ✅ 追求性能优化

**仍使用 pip 的场景：**
- 🤔 极简单的脚本（1-2 个依赖）
- 🤔 受限环境无法安装 uv
- 🤔 团队成员不熟悉 uv

**过渡建议：**
```bash
# 方案 1：渐进式迁移
# 保持 pip，在个人机器上试用 uv
uv pip install -r requirements.txt

# 方案 2：团队采用
# 在 CI/CD 中先使用 uv 加速
# GitHub Actions 示例：
- name: Install dependencies
  run: |
    pip install uv
    uv pip install -r requirements.txt

# 方案 3：完全替代
# 设置别名，全面使用 uv
alias pip='uv pip'
```

#### 配合 pyenv 使用

**推荐组合**：`pyenv + uv`，发挥各自优势

```bash
# 1. 使用 pyenv 管理 Python 版本
pyenv install 3.12.0
pyenv local 3.12.0

# 2. 使用 uv 创建虚拟环境和安装依赖
uv venv
source .venv/bin/activate

# 3. 使用 uv 快速安装依赖
uv pip install -r requirements.txt
```

#### uv vs pip vs pdm

| 工具 | 类型 | Python 版本管理 | 包安装速度 | 依赖锁定 | 项目管理 | 适用场景 |
|------|------|----------------|-----------|---------|---------|---------|
| **pip** | 包安装器 | ❌ | 慢 | ❌ | ❌ | 传统项目 |
| **uv** | 包安装器 | ❌ | **极快** | ✅ | ❌ | 追求速度 |
| **pdm** | 项目管理器 | ❌ | 快 | ✅ | ✅ | 完整项目管理 |
| **pyenv** | 版本管理器 | ✅ | - | - | ❌ | 管理 Python 版本 |

**功能互补性：**
- ✅ **pdm + uv**：pdm 管理项目，uv 加速安装（可配合使用）
- ✅ **pyenv + pdm**：pyenv 管理版本，pdm 管理项目
- ✅ **pyenv + uv**：pyenv 管理版本，uv 加速安装
- ✅ **pyenv + pdm + uv**：完美组合

### 工具对比与选择

| 工具 | 类型 | Python 版本管理 | 主要用途 | 核心功能 | 适用场景 |
|------|------|----------------|----------|---------|----------|
| **pyenv** ⭐ | 版本管理器 | ✅ | 管理多个 Python 版本 | 安装/切换 Python | **需要多个 Python 版本** |
| **venv** | 虚拟环境工具 | ❌ | 项目环境隔离 | 创建隔离环境 | 一般项目开发 |
| **pdm** | 项目管理器 | ❌ | 项目全生命周期管理 | 依赖管理+构建+发布 | 完整项目管理 |
| **uv** | 包安装器 | ❌ | 快速包安装 | 加速安装依赖 | 追求速度、CI/CD |

#### 关键区别与功能层次

```
[Python 版本层] pyenv          安装和切换 Python 3.10、3.11、3.12 等
                  ↓
[环境隔离层]   venv/virtualenv  基于已有 Python 创建隔离环境
                  ↓
[项目管理层]   pdm             管理依赖、构建、发布（完整项目管理）
                  ↓
[包安装层]     uv/pip          实际下载和安装包（底层执行）
```

#### 功能互补性说明

**pdm 和 uv 不冲突，可以配合使用：**

- **pdm 负责**：
  - 📦 定义项目依赖（pyproject.toml）
  - 🔒 生成锁文件（pdm.lock）
  - 📋 管理依赖组（dev/test/docs）
  - 🛠️ 项目脚本和任务
  - 📤 构建和发布包

- **uv 负责**：
  - ⚡ 快速下载和安装包
  - 🔧 解析依赖关系
  - 💾 高效缓存管理

**实际使用：**
```bash
# pdm 可以配置使用 uv 作为后端
pdm config install.use-uv true

# 这样就能享受 pdm 的项目管理 + uv 的安装速度
pdm install  # 内部使用 uv 加速
```

### 工具组合使用

这些工具可以组合使用，发挥各自优势：

1. **pyenv + venv**
   ```bash
   pyenv install 3.12.0
   pyenv local 3.12.0
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **pyenv + pdm**
   ```bash
   pyenv install 3.12.0
   pyenv local 3.12.0
   pdm init
   ```

3. **venv + uv**（快速安装依赖）
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

### 推荐选择

#### 按需求场景选择

1. **需要管理多个 Python 版本？**
   - ✅ 使用 **pyenv**（这是它的核心功能）
   - ❌ uv、venv、pdm 都不提供此功能

2. **追求包安装速度？**
   - ✅ 使用 **uv** 替代 pip
   - 组合：`pyenv + venv + uv`

3. **追求现代化项目管理？**
   - ✅ 使用 **pdm**
   - 组合：`pyenv + pdm`

4. **简单快速开始？**
   - ✅ 使用 **venv + pip**（标准库内置）

#### 推荐工具组合

1. **新手或一般项目**
   - 组合：`pyenv + venv + pip`
   - 理由：简单、稳定、标准

2. **追求安装速度**
   - 组合：`pyenv + venv + uv` ⚡
   - 理由：uv 比 pip 快 10-100 倍

3. **现代化项目管理**
   - 组合：`pyenv + pdm` 📦
   - 理由：完整的项目管理功能

4. **追求极致性能**
   - 组合：`pyenv + pdm + uv` 🚀
   - 理由：pdm 管理项目，uv 加速安装
   - 配置：`pdm config install.use-uv true`

5. **大型项目或 CI/CD**
   - 组合：`pyenv + uv`
   - 理由：快速构建和部署

#### 核心原则与层次

```
┌─────────────────────────────────────┐
│  [Python 版本]                      │
│  pyenv install 3.12.0               │  ← 安装 Python
│  pyenv local 3.12.0                 │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  [环境隔离（可选）]                 │
│  python -m venv .venv               │  ← 创建隔离环境
│  source .venv/bin/activate          │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  [项目管理（二选一）]               │
│  • pdm（完整管理）                  │  ← 管理依赖和项目
│  • 手动管理（requirements.txt）     │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  [包安装（二选一）]                 │
│  • uv pip install（快）             │  ← 安装包
│  • pip install（标准）              │
└─────────────────────────────────────┘
```

#### 不同场景的最佳实践

**场景 1：个人学习项目**
```bash
pyenv local 3.12.0
python -m venv .venv
source .venv/bin/activate
pip install requests
```

**场景 2：团队协作项目**
```bash
pyenv local 3.12.0
pdm init
pdm add requests
pdm add pytest --dev
# 团队成员只需：pdm install
```

**场景 3：追求极致速度**
```bash
pyenv local 3.12.0
pdm config install.use-uv true
pdm add requests  # 使用 uv 加速
```

**场景 4：CI/CD 流水线**
```bash
pyenv install 3.12.0
pyenv global 3.12.0
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt  # 快速安装
```

```Bash
# install venv
sudo apt install -y python3-venv
# 判断当时是否在虚拟环境里
which python
```

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

#### import 报错

right click, mark directory as source root

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

```
+ 对它前面的正则式匹配 1 到任意次重复。 ab+ 会匹配 'a' 后面跟随 1 个以上到任意个 'b'，它不会匹配 'a'。
? 对它前面的正则式匹配0到1次重复。 ab? 会匹配 'a' 或者 'ab'。
+? 以 非贪婪 或 最小 风格来执行匹配；
. 任意一个字符除了 \n
[] 匹配[]中列举的字符
\d 匹配数字, 0-9
\s 匹配空白, 即空格, tab

```

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

string.isdecimal()    如果 string 只包含十进制数字(整数)，则返回 True 否则返回 False.

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

### for else

```py
# 示例：检查列表中是否包含某个值
numbers = [1, 2, 3, 4, 5]
target = 6

for number in numbers:
    if number == target:
        print("找到了目标值!")
        break
else:
    print("目标值不在列表中。")

# 结果: 目标值不在列表中。
```

```py
# 示例：检查列表中是否包含某个值
numbers = [1, 2, 3, 4, 5]
target = 3

for number in numbers:
    if number == target:
        print("找到了目标值!")
        break
else:
    print("目标值不在列表中。")

# 结果: 目找到了目标值!
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

https://blog.csdn.net/wuShiJingZuo/article/details/136631668

```Bash
# -U Upgrade all specified packages
pip install -U pytest
# 在项目根目录执行
python -m pytest

# 输出 print
python -m pytest -s

# select one or moure function
python -m pytest -s -k 'test_func_0'
python -m pytest -s -k 'test_func_0 or test_func_1'

py.test path/to/test.py
```

### pytest windows

```Bash
# python 3.6 虚拟环境
C:\workspace\python-env-36\Scripts\activate.bat
# 安装 pytest
pip install -U pytest
# cd c:\path\to\project\root\dir\
# 配置环境变量
# set foo=bar
python -m pytest -s -k test_
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
"x < y <= z" is equivalent to "x < y and y <= z",……
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

## whl download

python -m pip download --only-binary=:all: --platform amd64 --python-version 36 cython

## config logger by code

https://www.cnblogs.com/yyds/p/6885182.html

```Python
# 创建一个日志器logger并设置其日志级别为DEBUG
logger = logging.getLogger('simple_logger')
logger.setLevel(logging.DEBUG)

# 创建一个流处理器handler并设置其日志级别为DEBUG
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

# 创建一个格式器formatter并将其添加到处理器handler
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

# 为日志器logger添加上面创建的处理器handler
logger.addHandler(handler)

# 日志输出
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')
```

## Segmentation fault

https://blog.csdn.net/ARPOSPF/article/details/130248065

```Bash
python -X faulthandler your_script.py
```

## Converting an object into a subclass

```Python
class A(object):
    def __init__(self):
        self.x = 1

class B(A):
    def __init__(self):
        super(B, self).__init__()
        self._init_B()
    def _init_B(self):
        self.x += 1

a = A()
b = a
b.__class__ = B
b._init_B()

assert b.x == 2
```

##  * 星号

星号在python中的用法主要可分为三类：一是作为函数的可变参数标志以及在函数参数的语境下对可迭代对象进行解包并进行参数传递（参数解包），二是作为赋值语句中的可变变量标志，三是在非函数参数的其他特定的语境中直接对可迭代对象进行解包操作。这三种用法是在不同的python版本中不断的添加进去的，其中后两种用法只在3.x版本中可以使用，具体的讲，用法一是在2.x和3.x都可以使用的，第二种用法是在3.0版本添加进去的，第三种用法是在3.5版本中添加进去的，所以在使用星号的不同用法时，还需要注意python的版本，以免出错。下面对每种用法进行详细的说明。

一、作为函数的可变参数标志以及参数解包
在函数的参数中，当以*标记一个参数时，表明这个参数是可变参数，具体来讲，用单星号*标记参数，表示其是可变的位置参数，并且以元组的形式将外部的多个位置参数返回给该参数变量，如果用双星号**标记，表示其看是可变的关键词参数，并且会以字典的形式将外部的多组关键词参数和值返回给该参数变量。如下所示。

def f1(a,*b,**c):
print(a)
print(b)
print(c)

f1(1,2,(3,4),k1=5,k2=6)

# output:
# 1
# (2,(3,4))
# {'k1':5,'k2':6}
'
运行运行
此外，如果我们要将一个可迭代对象作为参数传给一个函数，在这种语境下，可以直接利用*iterable语法对可迭代对象解包，并把解包后的内容传给函数，如下所示。要注意的是，如果解包之后的元素个数不和函数位置参数的个数相等的话，是会抛出异常的，所以一般情况下，不建议在不含可变参数的函数中使用这种传参方式。

def f2(a,b):
print(a)
print(b)

f2(*[1,2])

# output:
# 1
# 2

f2(*[1,2,3]) # TypeError: f2() takes 2 positional argument but 3 were given


def f3(a,*b):
print(a)
print(b)

f3(*(1,2,3))

# output:
# 1
# (2,3)

二、赋值语句中作为可变变量标志
当我们想要对一个可迭代对象进行拆分，并赋值给相应的变量时，我们可以用星号标记某个变量，这个变量表示可变变量，意思表示其内容是不定的，内容根据其他的变量的个数决定。因为其原理就是优先赋值给其他确定的变量，然后剩下的内容再赋值给可变变量，实际上，可变变量的内容就是对可迭代对象剩下内容解包后得到的内容，并以列表list对象返回给变量，如下所示。

a,*b=(1,2,3,4,5)
*c,d=range(5)

print(a) # output: 1
print(b) # output: [2,3,4,5]
print(c) # output: [0,1,2,3]
print(d) # output: 4
'
运行运行
三、在除函数参数语境外的其他语境下对可迭代对象进行解包
在3.5版本开始，python对星号增加新的适用场景，即在元组、列表、集合和字典内部进行对可迭代参数直接解包，这里需要一再强调的是，这里是在上述四个场景下才可以对可迭代参数直接解包，在其他场景下进行可迭代对象的星号解包操作时不允许的，如下所示。

a=*range(3),
b=*range(3),3
c=[*range(3)]
d={*range(3)}
e={**{'y':1}}

print(a) # output: (0,1,2)
print(b) # output: (0,1,2,3)
print(c) # output: [0,1,2]
print(d) # output: {0,1,2}
print(e) # output: {'y':1}
'
运行运行
还要注意的是，由于这里只能在这些指定的场景下对可迭代对象直接解包，如果直接*range(3)是会报错的，要区别于上述的第一条语句，注意上述第一条语句中*range(3)后面是有逗号的，所以这就表示在元组的场景下进行解包，所以是允许的。
————————————————

                            版权声明：本文为博主原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接和本声明。

原文链接：https://blog.csdn.net/S_o_l_o_n/article/details/102823490

## print exception trace

```Python
import traceback

def do_stuff():
    raise Exception("test exception")

try:
    do_stuff()
except Exception:
    print(traceback.format_exc())
```

## 性能分析工具

https://blog.csdn.net/Bit_Coders/article/details/120154767

https://www.jetbrains.com/help/pycharm/profiler.html

https://github.com/sumerc/yappi

pycharm 专业版，从 Run 中点击 Profile，即可对当前 python 脚本进行性能分析

```Bash
pip install yappi

# 安装 vmprof 之后 pstat 不能打印函数名了...
pip install vmprof

# /usr/bin/ld: cannot find -lunwind: No such file or directory
sudo apt-get install -y libunwind-dev
```

## pytest performance

https://pypi.org/project/pytest-benchmark/

```Bash
pip install pytest-benchmark
```

```Python
def something(duration=0.000001):
    """
    Function that needs some serious benchmarking.
    """
    time.sleep(duration)
    # You may return anything you want, like the result of a computation
    return 123

def test_my_stuff(benchmark):
    # benchmark something
    result = benchmark(something)

    # Extra code, to verify that the run completed correctly.
    # Sometimes you may want to check the result, fast functions
    # are no good if they return incorrect results :-)
    assert result == 123
```

```Bash
python -m pytest -s -k "test_my_stuff"
```

## pytest profiling

```Bash
pip install pytest-profiling
pip install gprof2dot
sudo apt install inkscape

# GNOME image viewer
eog combined.svg

/usr/bin/google-chrome-stable combined.svg
inkscape combined.svg
inkview combined.svg
```

## Python 性能调试工具 py-spy

## func

```Python
# 获取对象的内存地址, 返回对象的唯一标识符，标识符是一个整数。
id()
```

## PYTHONUNBUFFERED

ENV PYTHONUNBUFFERED 1

相当于设置 python 命令行的 -u 选项
不缓冲stdin、stdout和stderr，默认是缓冲的

设置python的stdout为无缓存模式
#!/usr/bin/env python
import sys

sys.stdout.write("stdout1 ")
sys.stderr.write("stderr1 ")
sys.stdout.write("stdout2 ")
sys.stderr.write("stderr2 ")
其中的sys.stdout.write也可以换成print。
运行这程序，你觉得会输出什么？试验一下，就会发现，其实输出并不是
'''stdout1 stderr1  stdout2 stderr2'''
而是：
'''stderr1 stderr2 stdout1  stdout2'''
究其原因，是因为缓存：虽然stderr和stdout默认都是指向屏幕的，但是stderr是无缓存的，程序往stderr输出一个字符，就会在屏幕上显示一个；而stdout是有缓存的，只有遇到换行或者积累到一定的大小，才会显示出来。这就是为什么上面的会显示两个stderr的原因了。
然而，有时候，你可能还是希望stdout的行为和stderr一样，能不能实现呢？当然是可以的，而且对于python，实现起来还特别方便，以下是两个方法：

python -u stderr_stdout.py
PYTHONUNBUFFERED=1 python stderr_stdout.py
第一种方法是给python指定 -u 参数，第二种方法是在python运行时，指定 PYTHONUNBUFFERED 环境变量，这两种方法其实是等效的。
当然，也可以在程序的第一行指定 #!/usr/bin/python -u 然后程序加可执行权限来运行，或者把 export PYTHONUNBUFFERED=1 写到 .bashrc 里去。

## @classmethod

@classmethod 是一个装饰器，用于定义类方法（class method）。类方法是绑定到类而不是实例的方法，这意味着它们可以访问类本身而不是某个实例的数据。类方法的第一个参数通常被命名为 cls，代表类本身。

## PEP

https://peps.python.org/pep-0582/

## ruff

python 代码静态检查

```Bash
pip install ruff
ruff check
```

## 私有变量

```PY
class Counter:
    def __init__(self):
        self.__count = 0  # 私有变量，带双下划线

    def increment(self):
        self.__count += 1
        return self.__count

c = Counter()
print(c.increment())  # 输出 1
print(c.increment())  # 输出 2

```

## GIL

GIL的全称是Global Interpreter Lock (全局解释器锁)

在 CPython，GIL 是一个全局互斥锁, 保证同一时间只有一个线程在执行 Python 字节码。所以 python 线程同时只能有一个线程在一个 cpu 核心上执行, 其他线程只能等待, 这就导致了 python 的多线程并不能真正的实现多核并行。 所以Python 解释器层面的多线程执行 = 单核轮流跑。

对 CPU 密集型任务，你说的完全正确，Python 多线程无法多核并行。

对 I/O 密集型任务，GIL 在执行 I/O 时会被释放（read/write/socket 调用期间），这时候其他线程可以抢到 GIL 继续运行，所以多线程对 I/O 密集场景依然是有用的。

## python-benchmark

```bash
-------------------------------------------------------------- benchmark: 1 tests --------------------------------------------------------------
Name (time in ms)                               Min       Max      Mean     StdDev   Median   IQR        Outliers   OPS       Rounds  Iterations
------------------------------------------------------------------------------------------------------------------------------------------------
test_foo                                        36.9506  154.7800  55.8549  24.3072  51.1331  9.4252     11;13      17.9035   189           1
------------------------------------------------------------------------------------------------------------------------------------------------
```

- Min: 最小执行时间
- Max: 最大执行时间
- Mean: 平均执行时间
- StdDev: 标准差
- Median: 中位数
- IQR: 四分位间距
- Outliers: 异常值数量
- OPS: 每秒操作数 (Operations Per Second)
- Rounds: 测试轮数
- Iterations: 每轮迭代次数

## 生成器表达式（Generator Expression）

Python 2.4+

是 Python 中一种内存高效的创建生成器的方式，它的语法类似于列表推导式，但使用圆括号 () 而不是方括号 []。

```Python
data = ['1', '2', '3', '4', '5']
integers = (int(x) for x in data)
```

## any() 函数

any() 是 Python 的内置函数，用于判断可迭代对象中是否至少有一个元素为真（True）。

```Python
any([False, False, True])
```
