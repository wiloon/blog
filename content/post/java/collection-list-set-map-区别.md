---
title: Collection List Set Map 区别
author: lcf
date: 2012-09-25T06:53:50+00:00
url: collection/list-set-map
categories:
  - Java

tags:
  - reprint
---
## Collection List Set Map 区别


这些都代表了Java中的集合，这里主要从其元素是否有序，是否可重复来进行区别记忆，以便恰当地使用，当然还存在同步方面的差异，见上一篇相关文章。

||有序否|允许元素重复否|
|-|-|-|
|Collection|否|是|
|List|是|是|
|Set|是|是|
|HashSet| | |
|TreeSet| 是 (用二叉树排序) | |
|Map|AbstractMap|否|使用key-value来映射和存储数据，Key必须惟一，value可以重复|
|HashMap|是 (用二叉树排序) ||

http://tb.blog.csdn.net/TrackBack.aspx?PostId=584112

  List接口对Collection进行了简单的扩充，它的具体实现类常用的有ArrayList和LinkedList。你可以将任何东西放到一个List容器中，并在需要时从中取出。ArrayList从其命名中可以看出它是一种类似数组的形式进行存储，因此它的随机访问速度极快，而LinkedList的内部实现是链表，它适合于在链表中间需要频繁进行插入和删除操作。在具体应用时可以根据需要自由选择。前面说的Iterator只能对容器进行向前遍历，而ListIterator则继承了Iterator的思想，并提供了对List进行双向遍历的方法。 
  
Set接口也是Collection的一种扩展，而与List不同的时，在Set中的对象元素不能重复，也就是说你不能把同样的东西两次放入同一个Set容器中。它的常用具体实现有HashSet和TreeSet类。HashSet能快速定位一个元素，但是你放到HashSet中的对象需要实现hashCode()方法，它使用了前面说过的哈希码的算法。而TreeSet则将放入其中的元素按序存放，这就要求你放入其中的对象是可排序的，这就用到了集合框架提供的另外两个实用类Comparable和Comparator。一个类是可排序的，它就应该实现Comparable接口。有时多个类具有相同的排序算法，那就不需要在每分别重复定义相同的排序算法，只要实现Comparator接口即可。集合框架中还有两个很实用的公用类: Collections和Arrays。Collections提供了对一个Collection容器进行诸如排序、复制、查找和填充等一些非常有用的方法，Arrays则是对一个数组进行类似的操作。
  
  
Map是一种把键对象和值对象进行关联的容器，而一个值对象又可以是一个Map，依次类推，这样就可形成一个多级映射。对于键对象来说，像Set一样，一个Map容器中的键对象不允许重复，这是为了保持查找结果的一致性;如果有两个键对象一样，那你想得到那个键对象所对应的值对象时就有问题了，可能你得到的并不是你想的那个值对象，结果会造成混乱，所以键的唯一性很重要，也是符合集合的性质的。当然在使用过程中，某个键所对应的值对象可能会发生变化，这时会按照最后一次修改的值对象与键对应。对于值对象则没有唯一性的要求。你可以将任意多个键都映射到一个值对象上，这不会发生任何问题 (不过对你的使用却可能会造成不便，你不知道你得到的到底是那一个键所对应的值对象) 。Map有两种比较常用的实现: HashMap和TreeMap。HashMap也用到了哈希码的算法，以便快速查找一个键，TreeMap则是对键按序存放，因此它便有一些扩展的方法，比如firstKey(),lastKey()等，你还可以从TreeMap中指定一个范围以取得其子Map。键和值的关联很简单，用pub(Object key,Object value)方法即可将一个键与一个值对象相关联。用get(Object key)可得到与此key对象所对应的值对象。
  


http://zhidao.baidu.com/question/16113509.html
