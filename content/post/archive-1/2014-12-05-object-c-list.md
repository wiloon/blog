---
title: 自旋锁、排队自旋锁、MCS锁、CLH锁
author: wiloon
type: post
date: 2014-12-05T01:05:56+00:00
url: /?p=7099
categories:
  - Uncategorized

---
自旋锁

<blockquote data-secret="FazEXCjmAy" class="wp-embedded-content">
  
    <a href="http://www.wiloon.com/wordpress/?p=10215">自旋锁/Spin lock</a>
  
</blockquote>

<iframe class="wp-embedded-content" sandbox="allow-scripts" security="restricted" style="position: absolute; clip: rect(1px, 1px, 1px, 1px);" src="http://www.wiloon.com/wordpress/?p=10215&#038;embed=true#?secret=FazEXCjmAy" data-secret="FazEXCjmAy" width="600" height="338" title=""自旋锁/Spin lock" - w1100n" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>

排队自旋锁

<blockquote data-secret="dvWR0yOf3D" class="wp-embedded-content">
  
    <a href="http://www.wiloon.com/wordpress/?p=5496">排队自旋锁/Ticket Lock</a>
  
</blockquote>

<iframe class="wp-embedded-content" sandbox="allow-scripts" security="restricted" style="position: absolute; clip: rect(1px, 1px, 1px, 1px);" src="http://www.wiloon.com/wordpress/?p=5496&#038;embed=true#?secret=dvWR0yOf3D" data-secret="dvWR0yOf3D" width="600" height="338" title=""排队自旋锁/Ticket Lock" - w1100n" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>

MCS锁

<blockquote data-secret="nvFCYYcuyH" class="wp-embedded-content">
  
    <a href="http://www.wiloon.com/wordpress/?p=5493">MCS锁/MCS Spinlock</a>
  
</blockquote>

<iframe class="wp-embedded-content" sandbox="allow-scripts" security="restricted" style="position: absolute; clip: rect(1px, 1px, 1px, 1px);" src="http://www.wiloon.com/wordpress/?p=5493&#038;embed=true#?secret=nvFCYYcuyH" data-secret="nvFCYYcuyH" width="600" height="338" title=""MCS锁/MCS Spinlock" - w1100n" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>

CLH锁

<blockquote data-secret="qftAW3eZtB" class="wp-embedded-content">
  
    <a href="http://www.wiloon.com/wordpress/?p=10307">CLH</a>
  
</blockquote>

<iframe class="wp-embedded-content" sandbox="allow-scripts" security="restricted" style="position: absolute; clip: rect(1px, 1px, 1px, 1px);" src="http://www.wiloon.com/wordpress/?p=10307&#038;embed=true#?secret=qftAW3eZtB" data-secret="qftAW3eZtB" width="600" height="338" title=""CLH" - w1100n" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>

差异：

从代码实现来看，CLH比MCS要简单得多。
  
从自旋的条件来看，CLH是在前驱节点的属性上自旋，而MCS是在本地属性变量上自旋。
  
从链表队列来看，CLH的队列是隐式的，CLHNode并不实际持有下一个节点；MCS的队列是物理存在的。
  
CLH锁释放时只需要改变自己的属性，MCS锁释放则需要改变后继节点的属性。
  
注意：这里实现的锁都是独占的，且不能重入的。

<blockquote data-secret="S6ykvE6LpW" class="wp-embedded-content">
  
    <a href="https://coderbee.net/index.php/concurrent/20131115/577">自旋锁、排队自旋锁、MCS锁、CLH锁</a>
  
</blockquote>

<iframe class="wp-embedded-content" sandbox="allow-scripts" security="restricted" style="position: absolute; clip: rect(1px, 1px, 1px, 1px);" src="https://coderbee.net/index.php/concurrent/20131115/577/embed#?secret=S6ykvE6LpW" data-secret="S6ykvE6LpW" width="600" height="338" title="《自旋锁、排队自旋锁、MCS锁、CLH锁》—码蜂笔记" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>