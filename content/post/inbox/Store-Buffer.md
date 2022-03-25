---
title: "Store Buffer"
author: "-"
date: "2021-07-10 10:50:24"
url: "Store-Buffer"
categories:
  - inbox
tags:
  - inbox
---
## "Store Buffer"

就像spinlock的进化史，软件工程师会对自己的代码做足够的优化以提高性能。同样，硬件工程也不甘示弱，尽最大的努力设计硬件以获取更好的性能。我们引入高速缓存的目的就是为了降低内存访问的延迟，谁知硬件工程师依然不满足于高速缓存带来的延迟，当然软件工程师或许也不满足。为了进一步加快内存访问速度，硬件引入了新的缓存 - store buffer。随着store buffer的引入，彻底刷新了软件工程师对代码执行流的认知。store buffer又是怎么刷新我们的认知呢？

文章测试代码已经开源，可以点击这里查看。
store buffer是什么
在之前的文章介绍中，我们了解到每个CPU都会有自己私有L1 Cache。从我了解的资料来说，L1 Cache命中的情况下，访问数据一般需要2个指令周期。而且当CPU遭遇写数据cache未命中时，内存访问延迟增加很多。硬件工程师为了追求极致的性能，在CPU和L1 Cache之间又加入一级缓存，我们称之为store buffer。store buffer和L1 Cache还有点区别，store buffer只缓存CPU的写操作。store buffer访问一般只需要1个指令周期，这在一定程度上降低了内存写延迟。不管cache是否命中，CPU都是将数据写入store buffer。store buffer负责后续以FIFO次序写入L1 Cache。store buffer大小一般只有几十个字节。大小和L1 Cache相比，确实是小巫见大巫了。


store buffer对程序的影响
我们现在知道，当存在store buffer的情况下。针对写操作，CPU直接把数据扔给store buffer。后续store buffer负责以FIFO次序写回L1 Cache。这会对我们的程序产生什么影响呢？我们来看个例子。

static int x = 0, y = 0;
static int r1, r2;


static void int thread_cpu0(void)
{
        x = 1;    /* 1) */
        r1 = y;   /* 2) */
}


static void int thread_cpu1(void)
{
        y = 1;    /* 3) */
        r2 = x;   /* 4) */
}


static void check_after_assign(void)
{
        printk("r1 = %d, r2 = %d\n", r1, r2);
}
假设thread_cpu0在CPU0上执行，thread_cpu1在CPU1上执行。在多核系统上，我们知道两个函数4条操作执行可以互相交错。理论上来我们有以下6种排列组合。

1) 2) 3) 4)
1) 3) 2) 4)
1) 3) 4) 2)
3) 4) 1) 2)
3) 1) 4) 2)
3) 1) 2) 4)
当我们确保thread_cpu0和thread_cpu1执行完成后，调用check_after_assign()会打印什么提示信息呢？根据以上6种组合，我们可能会得到如下3种结果。

r1 = 1, r2 = 1
r1 = 0, r2 = 1
r1 = 1, r2 = 0
这个结果是符合我们的认知的。当我们考虑store buffer时，会是怎样的结果呢？我们就以1) 3) 2) 4)的执行次序说明问题。当CPU0执行x = 1时，x的值会被写入CPU0的store buffer。CPU1指令y = 1操作，同样y的值会被写入CPU1的store buffer。接下来，r1 = y执行时，CPU0读取y的值，由于y的新值依然在CPU1的store buffer里面，所以CPU0看到y的值依然是0。所以r1的值是0。为什么CPU0看到r1的值是0呢？因为硬件MESI协议只会保证Cache一致性，只要值没有被写入Cache(依然躺在store buffer里面)，MESI就管不着。同样的道理，r2的值也会是0。此时我们看到了一个意外的结果。这里有个注意点，虽然store buffer主要是用来缓存CPU的写操作，但是CPU读取数据时也会检查私有store buffer是否命中，如果没有命中才会查找L1 Cache。这主要是为了CPU自己看到自己写进store buffer的值。所以CPU0是可以看到x值更新，但是CPU1不能及时看到x。同样，CPU1可以看到y值更新，但是CPU0不能及时看到y。所以，我们经常说“单核乱序对程序员是透明的，只有其他核才会受到乱序影响”。

r1 = 0, r2 = 0
TSO模型
我们应该如何去理解这样的结果呢？我们先简单了解下一致性问题。一致性分为两种，一种是cache一致性。cache一致性是我们之前文章中一直关注的点。而这里举例出现的问题属于内存一致性范畴。cache一致性和内存一致性有什么区别呢？我的总结是，cache一致性关注的是多个CPU看到一个地址的数据是否一致。而内存一致性关注的是多个CPU看到多个地址数据读写的次序。一个关注的是一个地址，一个关注的是多个地址的顺序。还是有点区别。为什么内存一致性关注的是多个地址的顺序呢？一个地址不会有问题吗？由于store buffer的存在，CPU0对一个地址数据的操作，其他CPU并不能及时看见，但是这又有什么影响呢？顶多相当于CPU0迟一点更新这个地址的数据而已。因此考虑多个地址数据的操作次序才有意义。针对内存一致性问题，我们提出内存模型的概念。为什么需要内存模型呢？我觉得主要是为了方便软件工程师在不理解硬件的情况下，还能理解代码执行是怎么回事，并编写正确的并行代码。

现在我们开始尝试遗忘store buffer吧！我们如何从内存模型的角度理解这个例子呢？上面的例子出现r1 = 0, r2 = 0的结果，这个结果和2) 4) 1) 3)的执行结果吻合。在其他CPU看来，CPU0似乎是1)和2)指令互换，CPU1似乎是3)和4)指令互换，执行的结果。我们针对写操作称之为store，读操作称之为load。所以我们可以这么理解，CPU0的store-load操作，在别的CPU看来乱序执行了，变成了load-store次序。这种内存模型，我们称之为完全存储定序(Total Store Order)，简称TSO。store和load的组合有4种。分别是store-store，store-load，load-load和load-store。TSO模型中，只存在store-load存在乱序，另外3种内存操作不存在乱序。当我们知道了一个CPU的内存模型，就可以根据具体的模型考虑问题。而不用纠结硬件实现的机制，也不用关心硬件做了什么操作导致的乱序。我们只关心内存模型。所以内存够模型更像是一种理论，一种标准，CPU设计之初就需要遵循的法则。当我们知道一款CPU的内存模型，在编写并发代码时就需要时刻考虑乱序带来的影响。我们常见的PC处理器x86-64就是常见的TSO模型。

看的见的乱序
我们就以x86-64为例，展示看得见的乱序。我们现在需要做的是构造测试环境。我们参考上面的举例构造2个CPU分别执行的两个函数。

static void ordering_thread_fn_cpu0(void)
{
        down(&sem_x);
        x = 1;
        /* Prevent compiler reordering. */
        barrier();
        r1 = y;
        up(&sem_end);
}


static void ordering_thread_fn_cpu1(void)
{
        down(&sem_y);
        y = 1;
        /* Prevent compiler reordering. */
        barrier();
        r2 = x;
        up(&sem_end);
}
代码看起来应该很熟悉，就是和上面的例子代码一致。barrier()是编译器屏障，后续会有文章介绍。这里先忽略吧，你可以理解成防止编译器优化。现在我们需要一个观察者，我们就利用CPU2作为观察者。

static void ordering_thread_fn_cpu2(void)
{
        static unsigned int detected;


        /* Reset x and y. */
        x = 0;
        y = 0;


        up(&sem_x);
        up(&sem_y);


        down(&sem_end);
        down(&sem_end);


        if (r1 == 0 && r2 == 0)
                pr_info("%d reorders detected\n", ++detected);
}
我们通过sem_x和sem_y两个信号量通知CPU0和CPU1执行代码，目的是为了CPU0和CPU1的代码执行交织在一起。数据存储在store buffer里面是短暂的。所以要创造并行执行的环境才容易看得到乱序。sem_end作用是通知观察者CPU2，可以查看结果了。

如何保证顺序性
如果我们确实不希望看到r1 = 0, r2 = 0的结果，我们该怎么办呢？很幸运，当然也很不幸运，硬件提供了内存屏障指令保证顺序一致性。幸运的是我们有方法阻止这种情况发生，不幸的是，看起来像是硬件工程师把锅甩给软件工程师。具体的指令细节，我们当然不关注。毕竟每个arch的指令都不一样。Linux内核中提供了smp_mb()宏对不同架构的指令进行封装，smp_mb()的作用是阻止它后面的读写操作不会乱序到宏前面的指令前执行。他就像是个屏障一样，不容逾越。

store---------------------+
load----------+           |
              |           |
              v           v
-----------------smp_mb()--------------
              ^           ^
              |           |
load----------+           |
store---------------------+
smp_mb()就像是不可逾越的屏障，后面的load/store绝不允许越过smp_mb()前执行。当然面前的load/store也不能越界到它的后面执行。但是smp_mb()前面的load/store操作怎么乱序就管不着了，同样smp_mb()后面的load/store操作也管不着。例如下面的代码。第1行和第2行，依然可能乱序。同样，第4行和第5行也可能乱序。但是绝不会出现第1行或者第2行跑到smp_mb()后面，同样第4行或者第5行也不会跑到smp_mb()前面。

a = 1;
b = c;
smp_mb();
d = 1;
e = f;
如何fix以上的例子呢？我们只需要简单的将barrier()替换成smp_mb()操作即可。

void ordering_thread_fn_cpu0(void)
{
        x = 1;
        smp_mb();
        r1 = y;
}      


static void ordering_thread_fn_cpu1(void)
{
        y = 1;
        smp_mb();
        r2 = x;
}
现在的代码我们可以这么理解，r1 = y不会比x = 1先执行。同样r2 = x不会在y = 1前执行。这样的话，就不会出现上述2) 4) 1) 3)执行流的结果。自然也不会出现r1 = 0, r2 = 0的结果。

总结
我们引出store buffer的存在只是为了让你有个概念。初衷并不是为了解释内存屏障指令的工作原理。当我们思考内存一致性问题时，我们应该关注的是内存模型。根据内存模型理论，就可以指导我们写出正确的代码。你可能会还有疑问，我们什么情况下需要考虑内存乱序呢？我觉得可以总结以下几点: 

是否有共享数据？私有数据不存在竞争，所以就不需要考虑内存序。
共享数据是否可能被多个CPU并行访问？这里是“并行”，不是并发。并行是指多个CPU可能同时访问共享数据。这里有两点需要注意。1) 例如spinlock保护的数据访问，并不属于并发访问，因为同一时间只有一个人进入临界区。所以并不存在并发。不需要考虑乱序。2) 如果共享数据只会被一个CPU访问 (例如绑核或者per cpu变量) ，也不需要考虑乱序。之前说了“单核乱序对程序员是透明的，只有其他核才会受到乱序影响”，一个CPU的情况，就不会出现其他观察者。
是否有多个共享数据？多个数据之间的读写访问，是否需要保证一定的次序？如果需要保证次序，就需要考虑乱序。如果不care访问次序，那就没必要考虑乱序。


---

https://zhuanlan.zhihu.com/p/141655129
