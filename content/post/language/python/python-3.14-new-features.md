---
title: Python 3.14 新特性探索
author: "-"
date: 2025-12-24T16:30:00+08:00
url: python-3.14-new-features
categories:
  - Python
tags:
  - Python
  - AI-assisted
  - remix
---

## Python 3.14 概述

Python 3.14 于 **2025 年 10 月 7 日**正式发布（当前最新版本：**3.14.2**，2025年12月5日），带来多项重大改进和新特性。这是 Python 发展历程中的重要里程碑，包括注解系统的重大变革、模板字符串、多解释器支持等令人期待的功能。

## 核心新特性

### PEP 649 & PEP 749: 延迟注解求值

**Python 3.14 最重大的变化！** 注解不再立即求值，而是存储在特殊的注解函数中，仅在需要时才求值。

**关键改进：**

- 大幅提升运行时性能（注解定义成本最小化）
- 不再需要使用字符串包裹前向引用
- 新增 `annotationlib` 模块用于处理注解

**三种注解格式：**

```python
from annotationlib import get_annotations, Format

def func(arg: Undefined):
    pass

# VALUE 格式：求值为运行时值
try:
    get_annotations(func, format=Format.VALUE)
except NameError:
    print("会抛出 NameError")

# FORWARDREF 格式：未定义的名称替换为特殊标记
print(get_annotations(func, format=Format.FORWARDREF))
# {'arg': ForwardRef('Undefined', owner=<function func>)}

# STRING 格式：以字符串形式返回
print(get_annotations(func, format=Format.STRING))
# {'arg': 'Undefined'}
```

### PEP 734: 标准库中的多解释器支持

**突破性功能！** 在同一进程中运行多个独立 Python 解释器的能力现已暴露给 Python 层。

**核心优势：**

- 新的、人性化的并发模型
- 真正的多核并行能力
- 新增 `concurrent.interpreters` 模块

```python
from concurrent.interpreters import Interpreter

# 创建新解释器
interp = Interpreter()

# 在新解释器中执行代码
code = '''
import sys
print(f"Hello from interpreter {id(sys.modules)}")
'''
interp.exec(code)
```

### PEP 750: 模板字符串（t-strings）

全新的字符串处理机制！t-strings 返回的是模板对象而非简单字符串。

```python
from string.templatelib import Interpolation

variety = 'Stilton'
template = t'Try some {variety} cheese!'

# 访问模板的各个部分
print(list(template))
# ['Try some ', Interpolation('Stilton', 'variety', None, ''), ' cheese!']

# 自定义处理
def lower_upper(template):
    parts = []
    for part in template:
        if isinstance(part, Interpolation):
            parts.append(str(part.value).upper())
        else:
            parts.append(part.lower())
    return ''.join(parts)

name = 'Wensleydale'
print(lower_upper(t'Mister {name}'))  # "mister WENSLEYDALE"
```

**应用场景：** SQL 注入防护、安全的 Shell 操作、HTML/CSS 处理、轻量级 DSL。

### PEP 768: 安全的外部调试器接口

零开销的调试接口，允许调试器安全地附加到运行中的进程：

```python
import sys
from tempfile import NamedTemporaryFile

with NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
    f.write('print("Debug code")')
    f.flush()
    sys.remote_exec(f.name)
```

### 其他语法改进

**PEP 758 - 简化的异常处理：**

```python
# 3.14 新语法 - 不需要括号
try:
    ...
except ValueError, TypeError:
    ...
```

**PEP 765 - finally 块中的控制流：** 改进了 `finally` 块中的控制流处理。

## 新增标准库模块

### annotationlib - 注解内省

```python
from annotationlib import get_annotations, Format

class MyClass:
    x: int
    y: str

annots = get_annotations(MyClass, format=Format.VALUE)
print(annots)  # {'x': <class 'int'>, 'y': <class 'str'>}
```

### compression.zstd - Zstandard 压缩（PEP 784）

```python
import compression.zstd as zstd

data = b"Hello World" * 100
compressed = zstd.compress(data)
decompressed = zstd.decompress(compressed)
```

### concurrent.interpreters

支持多解释器并发（见 PEP 734）。

### string.templatelib

支持 t-strings（见 PEP 750）。

## 标准库重大改进

### asyncio 调用图内省

```python
import asyncio

# 捕获调用图
graph = asyncio.capture_call_graph()

# 打印调用图
asyncio.print_call_graph(graph)
```

### pathlib 增强

```python
from pathlib import Path

path = Path("/home/user/file.txt")
new_path = path.with_stem("newname")  # /home/user/newname.txt
```

## 性能优化

### 自由线程模式正式支持（PEP 779）

**重大里程碑！** 自由线程构建现已正式支持（不再是实验性）。

```bash
# 编译时启用
./configure --disable-gil
make
```

**重要说明：**

- 这是 [Phase II](https://discuss.python.org/t/37075) - 正式支持但可选
- 何时成为默认构建尚未决定

### 实验性 JIT 编译器

**macOS 和 Windows 官方发布版已包含！**

```bash
# 通过环境变量启用
export PYTHON_JIT=1
python your_script.py
```

**性能影响：** -10% 到 +20%（取决于工作负载），不推荐生产环境。

### 增量垃圾回收

```python
import gc

# gc.collect(1) 现在执行一次增量回收
gc.collect(1)  # 行为已改变！
```

### 其他性能改进

- asyncio: 事件循环性能提升
- io、pathlib、uuid: 各模块性能优化

## 弃用和移除

### 移除的模块

以下 19 个模块在 Python 3.14 中被完全移除：

`aifc`, `audioop`, `chunk`, `cgi`, `cgitb`, `crypt`, `imghdr`, `mailcap`, `msilib`, `nis`, `nntplib`, `ossaudiodev`, `pipes`, `sndhdr`, `spwd`, `sunau`, `telnetlib`, `uu`, `xdrlib`

### 重要的弃用

**from \_\_future\_\_ import annotations:**

- 该特性已弃用，预计在 Python 3.13 EOL（2029年）后移除
- 由于 PEP 649，大多数情况下不再需要此 future import

**asyncio.iscoroutinefunction():**

- 弃用，将在 Python 3.16 移除
- 改用 `inspect.iscoroutinefunction()`

## 平台和构建变化

### 官方 Android 二进制发布

现在在 [python.org](https://www.python.org/downloads/android/) 提供官方 Android 发布版本！

### Emscripten 支持（PEP 776）

Emscripten 现在是 [Tier 3](https://peps.python.org/pep-0011/#tier-3) 官方支持平台。

### PGP 签名停用（PEP 761）

**重要：** Python 3.14+ 不再提供 PGP 签名，改用 [Sigstore](https://www.python.org/downloads/metadata/sigstore/) 验证。

### build-details.json

Python 安装现在包含 `build-details.json` 文件，提供静态 JSON 格式的构建详细信息。

## 发布时间表

### 已发布版本

- **3.14.0 final**: 2025-10-07
- **3.14.1**: 2025-12-02
- **3.14.2**: 2025-12-05（当前最新版本）

### 未来版本计划

**Bugfix 版本**（每两个月）：

- 3.14.3: 2026-02-03
- 3.14.4: 2026-04-07
- ... 持续到 2027-10-05（最后一个带二进制安装程序的版本）

**安全修复**：持续到 2030 年 10 月（5 年支持期）

## 迁移指南

### 从 Python 3.13 迁移

1. **检查移除的模块**：确认未使用 19 个已移除的模块
1. **注解迁移**：考虑移除 `from __future__ import annotations`
1. **测试新特性**：在测试环境验证 JIT 和自由线程模式
1. **更新弃用 API**：替换 `asyncio.iscoroutinefunction()` 等

### 兼容性检查

```python
import sys

if sys.version_info >= (3, 14):
    # 使用 Python 3.14 特性
    from annotationlib import get_annotations
else:
    # 回退方案
    pass
```

## 参考资源

### 官方文档

- [Python 3.14 官方文档](https://docs.python.org/3.14/)
- [What's New In Python 3.14](https://docs.python.org/3.14/whatsnew/3.14.html)
- [Python 3.14 下载](https://www.python.org/downloads/)

### 相关 PEP

核心特性：

- [PEP 649](https://peps.python.org/pep-0649/) - 延迟注解求值（使用描述符）
- [PEP 749](https://peps.python.org/pep-0749/) - 实现 PEP 649
- [PEP 734](https://peps.python.org/pep-0734/) - 标准库中的多解释器
- [PEP 750](https://peps.python.org/pep-0750/) - 模板字符串

语法和平台：

- [PEP 758](https://peps.python.org/pep-0758/) - 允许不带括号的 except 表达式
- [PEP 765](https://peps.python.org/pep-0765/) - finally 块中的控制流
- [PEP 768](https://peps.python.org/pep-0768/) - 安全的外部调试器接口
- [PEP 776](https://peps.python.org/pep-0776/) - Emscripten 平台支持

性能和工具：

- [PEP 779](https://peps.python.org/pep-0779/) - 自由线程 Python 正式支持
- [PEP 784](https://peps.python.org/pep-0784/) - Zstandard 支持

发布管理：

- [PEP 745](https://peps.python.org/pep-0745/) - Python 3.14 发布计划
- [PEP 761](https://peps.python.org/pep-0761/) - 停用 PGP 签名

### 其他资源

- [Python 开发者指南](https://devguide.python.org/)
- [Python GitHub 仓库](https://github.com/python/cpython)

## 总结

Python 3.14 是一个里程碑式的版本，带来了多项革命性改进：

### 核心亮点

1. **注解系统重构（PEP 649/749）** - 提升性能，简化前向引用
1. **多解释器支持（PEP 734）** - 开启真正的并发编程新时代
1. **模板字符串（PEP 750）** - 安全、灵活的字符串处理
1. **自由线程正式支持（PEP 779）** - 无 GIL 的多核并行
1. **实验性 JIT** - 性能优化的未来方向

### 迁移建议

- **立即可用**：大多数代码无需修改即可在 3.14 上运行
- **注解优化**：考虑移除 `from __future__ import annotations`
- **性能测试**：在非生产环境测试 JIT 和自由线程模式
- **注意变化**：检查已移除的模块和弃用的 API

### 未来展望

Python 3.14 展示了核心团队在性能、并发和开发者体验方面的雄心。随着 JIT 编译器的成熟和自由线程模式的推广，Python 的性能将迎来质的飞跃。

**建议**：开发者应积极关注这些变化，在测试环境中体验新特性，为未来的生产环境迁移做好准备。
