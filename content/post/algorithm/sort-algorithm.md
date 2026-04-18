---
title: 排序算法, Sorting Algorithm 
author: "-"
date: 2026-04-18T16:16:10+08:00
url: sort-algorithm
categories:
  - Linux
tags:
  - algorithm
  - sort
  - remix
  - AI-assisted
---

常见排序算法：

1. 冒泡排序
1. 选择排序
1. 插入排序
1. 希尔排序
1. 快速排序
1. 归并排序
1. 堆排序
1. 计数排序
1. 桶排序
1. 基数排序

**推荐学习顺序：** 冒泡 → 选择 → 插入 → 快速 → 归并 → 堆

## 冒泡排序 Bubble Sort

相邻元素两两比较，大的往后"冒泡"，每轮将最大值沉到末尾。

- 时间复杂度：O(n²)
- 空间复杂度：O(1)
- 稳定排序

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


# 测试
arr = [64, 34, 25, 12, 22, 11, 90]
print("排序前:", arr)
bubble_sort(arr)
print("排序后:", arr)
```

执行过程（以 `[5, 3, 1]` 为例）：

```
第1轮：
  j=0: 5 > 3，交换 → [3, 5, 1]
  j=1: 5 > 1，交换 → [3, 1, 5]  ← 最大值 5 沉底

第2轮：
  j=0: 3 > 1，交换 → [1, 3, 5]  ← 次大值 3 到位

第3轮：只剩1个，已有序
```

- 外层 `i` 控制轮数，每轮确定一个最大值的位置
- 内层 `n - i - 1` 让已排好的尾部不再参与比较
- `a, b = b, a` 是 Python 交换变量的惯用写法

## 选择排序 Selection Sort

每轮从未排序部分找最小值，放到已排序部分的末尾。

- 时间复杂度：O(n²)
- 空间复杂度：O(1)
- 不稳定排序

```python
def selection_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


# 测试
arr = [64, 34, 25, 12, 22, 11, 90]
print("排序前:", arr)
selection_sort(arr)
print("排序后:", arr)
```

执行过程（以 `[5, 3, 1]` 为例）：

```
第1轮：i=0，从 [5, 3, 1] 中找最小值 1（index=2），与 index=0 交换 → [1, 3, 5]
第2轮：i=1，从 [3, 5] 中找最小值 3（index=1），无需交换 → [1, 3, 5]
第3轮：只剩1个，已有序
```

- 外层 `i` 表示当前要填入最小值的位置
- 内层遍历找到最小值的下标 `min_idx`
- 每轮只做一次交换，交换次数比冒泡排序少
- 不稳定：交换时可能改变相同元素的相对顺序（如 `[5a, 5b, 1]` → `[1, 5b, 5a]`）
