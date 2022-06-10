---
title: 二分法, binary search algorithm
author: "-"
date: 2012-06-25T05:31:56+00:00
url: /?p=3667
categories:
  - Algorithm
tags:
  - reprint

---
## 二分法, binary search algorithm

## 二分法

一，学习别人的总结与讲解
本部分的参考见末尾，本部分文字是在其基础上的二度总结 (节约时间和精力）。

### 典型的二分法

算法：当数据量很大适宜采用该方法。采用二分法查找时，数据需是排好序的。

基本思想：假设数据是按升序排序的，对于给定值key，从序列的中间位置k开始比较，

如果当前位置`arr[k]`值等于key，则查找成功；

若key小于当前位置值`arr[k]`，则在数列的前半段中查找,`arr[low,mid-1]`；

若key大于当前位置值`arr[k]`，则在数列的后半段中继续查找`arr[mid+1,high]`，

直到找到为止,时间复杂度:`O(log(n))`。

上面的思想就是最最简单的二分法，即从一个排好序的数组之查找一个key值。 如下面的程序：

```c
int search(int *arr, int n, int key)
{
    int left = 0, right = n-1;
    while(left<=right) { //慎重截止条件，根据指针移动条件来看，这里需要将数组判断到空为止
        int mid = left + ((right - left) >> 1); //防止溢出
        if (arr[mid] == key) //找到了
            return mid; 
        else if(arr[mid] > key) 
            right = mid - 1; //给定值key一定在左边，并且不包括当前这个中间值
        else 
            left = mid + 1; //给定值key一定在右边，并且不包括当前这个中间值
    }
    return -1;
}
```

### 证明二分算法正确性

循环不变式：
如果key存在于数组中，始终只可能存在于当前的`array[left,right]`数组段中。

初始化：  
第一轮循环开始之前，`array[left,right]`就是原始数组，这时循环不变式显然成立。

迭代保持：  
每次循环开始前，如果key存在，则只可能在待处理数组`array[left, ..., right]`中。  
对于`array[mid]<key`，`array[left, ..., mid]`均小于key，key只可能存在于`array[mid+1, ..., right]`中；  
对于`array[mid]>key`，`array[mid, ..., right]`均大于key，key只可能存在于a`rray[left, ..., mid-1]`中；  
对于`array[mid]==key`，查找到了key对应的下标，直接返回结果。  
显然如果没找到key，下一次继续查找时我们设定的循环不变式依然正确。  
死循环否？在前两种情况中，数组长度每次至少减少1 (实际减少的长度分别是`mid-left+1`和`right-mid+1`），直到由`left==right`变为`left>right` (数组段长度由1-0）--->截止了，所以一定不会死循环。

终止：  
结束时发生了什么？`left>right`,被压缩的数组段为空，表示key不存在于所有步骤的待处理数组，再结合每一步排除的部分数组中也不可能有key，因此key不存在于原数组。因此我们得到了符合要求的解，此算法正确。

如果条件稍微变化一下，还会写吗？其实，二分法真的不那么简单，尤其是二分法的各个变种。

### 二分法的变种1

数组之中的数据可能可以重复，要求返回匹配的数据的最小 (或最大）的下标；更近一步，需要找出数组中第一个大于key的元素 (也就是最小的大于key的元素的）下标，等等。 这些，虽然只有一点点的变化，实现的时候确实要更加的细心。

下面列出了这些二分检索变种的实现

a. 找出第一个与key相等的元素的位置

快速思考四个问题：

1）通过什么条件来移动两个指针？与中间位置进行大小比较。

当`arr[mid]<key`时，当前位置一定不是解，解一定只可能在`arr[mid+1,high]`，即右边

当`arr[mid]>key`时，当前位置一定不是解，解一定只可能在`arr[low,mid-1]`，即左边

当`arr[mid]==key`呢？mid有可能是解，也可能在`arr[low,mid-1]`即左边,但可以肯定的是解一定只可能在`arr[low,mid]`中。

2）两个指针的意义？缩小范围，如果key存在于数组中，最终将low移动到目的位置。

3）程序的出口？截止条件就是出口，唯一的出口。

4）那截止条件应该如何写？这得看怎么移动的！

```c
int searchFirstEqual(int *arr, int n, int key)
{
    int left = 0, right = n-1;
    while(left < right)//根据两指针的意义，如果key存在于数组，left==right相等时已经得到解
    {
        int mid = (left+right)/2;
        if(arr[mid] > key)//一定在mid为止的左边，并且不包含当前位置
            right = mid - 1;
        else if(arr[mid] < key) 
            left = mid + 1;//一定在mid位置的右边，并且不包括当前mid位置
        else
            right=mid;//故意写得和参考博文不一样，下面有证明
    }
    if(arr[left] == key) 
            return left;
    return -1;
}
```

证明变种二分a的正确性：

循环不变式：
　　如果key存在于数组，那么key第一次出现的下标x只可能在[left,right]中，并且始终有array[left]<=key, array[right]>=key

初始化：
　　第一轮循环开始之前，数组段就是原数组，这时循环不变式显然成立。

迭代保持：
　　每次循环开始前，如果key存在于原数组，那么位置x只可能存在于待查找数组array[left, ..., right]中。
　　如果array[mid]<key，array[left, ..., mid]均小于key，x只可能存在于array[mid+1, ..., right]中。数组减少的长度为mid-left+1，至少为1。
　　如果array[mid]>key, array[mid, ..., right]均大于key的元素，x只可能存在于array[left, ..., mid-1]中.数组减少的长度为right-mid+1，至少为1。
对于array[mid]==key, array[mid, ..., right]均大于或者等于key的元素，x只可能存在于array[left, ..., mid]中，这里长度减少多少呢？见下面死循环分析。

显然迭代过程始终保持了循环不变式的性质。

死循环否？前两个条件至少减少1，但是后一个条件当两个指针的相距为2及其以上时 (比如2->5，距离为2）

长度至少减少1，然而当相距为1时将无法减少长度，但是聪明的我们将其截止了，所以不会出现死循环。

终止：

结束时发生了什么？即left==right时，根据循环不变式始终有array[left]<=key, array[right]>=key (否则就不应该在这里找）。显然我们把两个指针缩小到left==right的情况，只要检查array[left]==key即可得到满足问题的解。因此算法是正确的。

b. 找出最后一个与key相等的元素的位置

```c
int searchLastEqual(int *arr, int n, int key)
{
    int left = 0, right = n-1;
    while(left<right-1) {
        int mid = (left+right)/2;
        if(arr[mid] > key) 
            right = mid - 1;//key一定在mid位置的左边，并且不包括当前mid位置
        else if(arr[mid] < key) 
            left = mid + 1; //key一定在mid位置的右边，相等时答案有可能是当前mid位置
        else
            left=mid;//故意写得和参考博客不一样，见下面证明
    }
    if( arr[left]<=key && arr[right] == key) 
        return right;
    if( arr[left] == key && arr[right] > key)
        return left;
    return -1;
}
```

循环不变式：

　　如果key存在于数组，那么key最后一次出现的下标x只可能在[left,right]中，并且和上一题一样始终有array[left]<=key, array[right]>=key

初始化：
　　第一轮循环开始之前，数组段就是原数组，这时循环不变式显然成立。

迭代保持：
　　每次循环开始前，如果key存在于原数组，那么位置x只可能存在于待查找数组array[left, ..., right]中。
　　如果array[mid]<key，array[left, ..., mid]均小于key，x只可能存在于array[mid+1, ..., right]中。数组减少的长度为mid-left+1，至少为1。
　　如果array[mid]>key, array[mid, ..., right]均大于key的元素，x只可能存在于array[left, ..., mid-1]中.数组减少的长度为right-mid+1，至少为1。
对于array[mid]==key, array[mid, ..., right]均大于或者等于key的元素，x只可能存在于array[mid, ...,right]中，长度减少情况见下面死循环分析。

迭代过程始终保持了循环不变式。

死循环否？前两个条件至少减少1，但是后一个条件当两个指针的相距为3及其以上时 (比如2->5->7，距离为3）

长度至少减少1，然而当相距为2时将无法减少长度，但是聪明的我们利用left<right-1将其截止了，所以不会出现死循环。

终止：

结束时发生了什么？即left==right-1时，根据循环不变式始终有array[left]<=key, array[right]>=key (否则就不应该在这里找）。显然我们把两个指针缩小到只有left和right两个情况，只要检查两个位置的值与key相等与否即可得到满足问题的解。因此算法是正确的。

以上两个算法尽管参考别人博客，但是证明以及具体二分写法都不一样，可以仔细对比学习。

### 二分法的变种2

a. 查找第一个等于或者大于Key的元素的位置
int searchFirstEqualOrLarger(int *arr, int n, int key)
{
    int left=0, right=n-1;
    while(left<=right)
    {
        int mid = (left+right)/2;
        if(arr[mid] >= key)
            right = mid-1;
        else if (arr[mid] < key)
            left = mid+1;
    }
    return left;
}

b. 查找第一个大于key的元素的位置
int searchFirstLarger(int *arr, int n, int key)
{
    int left=0, right=n-1;
    while(left<=right)
    {
        int mid = (left+right)/2;
        if(arr[mid] > key)
            right = mid-1;
        else if (arr[mid] <= key)
            left = mid+1;
    }
    return left;
}

### 二分法的变种3

a. 查找最后一个等于或者小于key的元素的位置
int searchLastEqualOrSmaller(int *arr, int n, int key)
{
    int left=0, right=n-1;
    while(left<=right)
    {
        int m = (left+right)/2;
        if(arr[m] > key)
             right = m-1;
        else if (arr[m] <= key)
             left = m+1;
    }
    return right;
}

b. 查找最后一个小于key的元素的位置

int searchLastSmaller(int *arr, int n, int key)
{
    int left=0, right=n-1;
    while(left<=right) {
        int mid = (left+right)/2;
        if(arr[mid] >= key)
             right = mid-1;
        else if (arr[mid] < key)
             left = mid+1;
    }
    return right;
}
下面是一个测试的例子：
int main(void)
{
    int arr[17] = {1,
                   2, 2, 5, 5, 5,
                   5, 5, 5, 5, 5,
                   5, 5, 6, 6, 7};
    printf("First Equal           : %2d \n", searchFirstEqual(arr, 16, 5));
    printf("Last Equal            : %2d \n", searchLastEqual(arr, 16, 5));
    printf("First Equal or Larger : %2d \n", searchFirstEqualOrLarger(arr, 16, 5));
    printf("First Larger          : %2d \n", searchFirstLarger(arr, 16, 5));
    printf("Last Equal or Smaller : %2d \n", searchLastEqualOrSmaller(arr, 16, 5));
    printf("Last Smaller          : %2d \n", searchLastSmaller(arr, 16, 5));
    system("pause");
    return 0;
}
最后输出结果是：
First Equal           :  3
Last Equal            : 12
First Equal or Larger :  3
First Larger          : 13
Last Equal or Smaller : 12
Last Smaller          :  2
很多的时候，应用二分检索的地方都不是直接的查找和key相等的元素，而是使用上面提到的二分检索的各个变种，熟练掌握了这些变种，当你再次使用二分检索的检索的时候就会感觉的更加的得心应手了。

二，个人经验总结
首先一个基本的事实就是二分法一定有两个指针 (low和high）在移动和一个中间位置mid (要是没有还能算二分法？），二分法实际上就是在通过迭代这两个指针到指定的位置，只是迭代的条件可能式多样的 (不一定像经典二分法那样与中间值比较）。而迭代的而过程使劲的在淘汰当前确定不是解 (最终有可能是解）的某个范围。务必利用循环不变式快速理清三个条件：

1，确定循环不变式

这个一定得根据具体的问题正确设定，在每次循环时一定要继续保持这个条件成立。

2，二分移动条件是什么？
即我们应该以什么样的条件进行范围淘汰？最重要的事情是理清移动的具体意义，到底该不该跨步移动，即+1或者-1 (我称之为跨步移动）？
1）首先快速判断基于当前mid位置不是解得情况，那么将相应指针直接跨步移动，即+1或者-1
2）但是如果这个位置有可能是解也有可能不是解怎么办？无论怎么样，1中循环不变式一定要满足。

最重要的就是弄清楚二分法中移动的意义，确定当前一定正确的移动因素
a）如果全是确定移动因素二分算法就简单了，只看截止条件的设定即可。
b）如果具有不定的移动因素，没关系，只要移动不破坏循环不变式即可。

3，截止条件是什么？

截止条件的作用就是在截止后我们就可以判断出我们想要的答案了。

截止后一定要满足两个点：

a）我们的范围已经被压缩到很小的范围，可以很容易确定问题的解

b）一定要判断死循环与否，这是最重要的。

4，最后利用循环不变式验证二分算法的正确性

结合《算法导论》循环不变式断言我们写的二分算法的正确性。

形式上很类似与数学归纳法，它是一个需要保证正确断言。对于循环不变式，必须证明它的三个性质；

初始化：它在循环的第一轮迭代开始之前，应该是正确的。

保持：如果在循环的某一次迭代开始之前它是正确的，那么，在下一次迭代开始之前，它也应该保持正确。

终止：循环能够终止，并且可以得到期望的结果 (这一步是最重要的）。
证明这一步必须做，上面三步简单分析即可，这一步决定正确性。验证时特别要注意我们要的解在被压缩的范围中arr[low....high]中的关系和意义。

其实二分法难度还好，想想当年多么难的数学------《数学物理方程》《高等数学》都学了，这些与之相比就是“渣”。

例子1
在一个有序数组中查找要插入的位置

原文地址，`<LeetCode OJ> 35. Search Insert Position`

用low来记录答案

```java
class Solution {  
public:  
    int searchInsert(vector<int>& nums, int target) {  //数组不能空
        int low=0,high=nums.size()-1;  
        while(low<=high)  //相等时也需要判断一次
        {  
            int mid=(low+high)/2;  
            if(nums[mid]<target)  
                low=mid+1;//  确定移动因素，一定在右边nums[mid+1,high]
            if(nums[mid]>target)  
                high=mid-1;//  确定移动因素，一定在左边nums[low,mid-1]
            if(nums[mid]==target)  
                return mid;//确定因素，找到了  
        }  
        return low;  
    }  
};
```

例子2
任意相邻元素不相等的数组中，寻找峰位置 (任意一个峰都行）

原文地址，`<LeetCode OJ> 162. Find Peak Element`

注意：题目说了相邻元素不会相等，这个条件很重要。

a)   nums[mid] < nums[mid + 1]，

说明mid与后一个位置形成递增区间，则mid后面一定存在峰且当前mid一定不是峰，则low=mid+1 (这个位置就有可能是峰了）

b)   nums[mid] > nums[mid + 1]，

说明mid与后一个位置形成递减区间，则当前位置mid就有可能是峰 (也可能在其前面），则high左移动到mid

当low和high相等时是否能得到结果了？即是否应该截止？

因为high与后一位一定满足arr[high]>arr[high+1] (越界了就是负无穷）,即总是下降的；

而low正好相反，其前面一定是上升的，

所以当两者被压缩到相等时，就不需要再继续压缩范围，已经可以得到结果。

用low来记录最终答案

```bash
class Solution {  
public:  
    int findPeakElement(vector<int>& nums) {  
        int low = 0,high = nums.size()-1;
        while(low < high)  //根据移动情况，当两者相等时已经可以确定解  
        {
            int mid = (low+high)/2;
            if(nums[mid] < nums[mid+1])
                low = mid+1;  //确定移动因素，因为mid位置一定不是峰，而low=mid+1才可能是峰  
            else
                high = mid;      //不定移动因素
        }

        return low;   
    }  
};
```

例子3
在有序数组中，寻找第一个坏的版本

原文地址，`<LeetCode OJ> 278. First Bad Version`

用low来记录解

// Forward declaration of isBadVersion API.  
bool isBadVersion(int version);  
  
class Solution {  
public:  
    int firstBadVersion(int n) {  
        int low=1,high=n;  
        while(low<=high)  
        {  
            int mid=low+(high-low)/2;//测试案例有超大数，这样写更安全  
            if(isBadVersion(mid))//如果是坏的版本  
                high=mid-1; //不定移动因素，此时有可能是第一个坏版本
            else
                low=mid+1;//确定移动因素，一定在mid右边
        }  
        return low;  
    }  
};  

因为存在不确定移动因素，所以发现也可写成如下版本

// Forward declaration of isBadVersion API.  
bool isBadVersion(int version);  
  
class Solution {  
public:  
    int firstBadVersion(int n) {  
        int low=1, high=n;
        while(low<high) {
            int mid=low + (high-low)/2;
            if(isBadVersion(mid))
                high = mid;  //不定移动因素，
            else
                low = mid + 1;  //确定移动因素  
        }
        return low;
    }  
};

例子4
在每一行有序的二维数组中寻找值

原文地址，`<LeetCode OJ> 74. / 240. Search a 2D Matrix  (I / II）`

```java
class Solution {  
public:  
    bool searchMatrix(vector<vector<int>>& matrix, int target) {  
        int row=matrix.size();//行
        int col=matrix[0].size();

        for(int i=0;i<row;i++)//对每一行进行二分查找    
        {    
            int low=0,high=col-1;    
            //不可能在此行找到，此处算是一个小小的优化条件  
            if(matrix[i][high]<target)  
                continue;  
            //在此行查找      
            while(low <= high)//注意此处条件是根据low和high的移动情况来定的，可以断言必须每一行判断到空为止    
            {    
                int mid=(low+high)/2;    
                if(matrix[i][mid] > target)//确定移动因素，说明在mid位置的右边    
                    high=mid-1;    
                else if(matrix[i][mid] < target)  //确定移动因素  
                    low=mid+1;    
                else    //确定因素，找到了
                    return true;    
            }    
        }    
        return false;   
    }  
};  
```

未完待续，持续学习二分法中........

注：本博文为EbowTang原创，后续可能继续更新本文。如果转载，请务必复制本条信息！

原文地址：<http://blog.csdn.net/ebowtang/article/details/50770315>

原作者博客：<http://blog.csdn.net/ebowtang>

本博客LeetCode题解索引：<http://blog.csdn.net/ebowtang/article/details/50668895>

参考资源：

【1】前半部分原作者，liubird，博文地址，<http://blog.chinaunix.net/uid-1844931-id-3337784.html>

【2】循环不变式下的二分法，<http://www.cnblogs.com/wuyuegb2312/archive/2013/05/26/3090369.html>

【3】LeetCode总结--二分查找篇，<http://blog.csdn.net/linhuanmars/article/details/31354941>
————————————————
版权声明：本文为CSDN博主「EbowTang」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：<https://blog.csdn.net/EbowTang/article/details/50770315>
