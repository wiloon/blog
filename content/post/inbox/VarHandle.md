---
title: "VarHandle"
author: "-"
date: "2021-09-21 00:13:12"
url: "VarHandle"
categories:
  - inbox
tags:
  - inbox
---
## "VarHandle"

VarHandle 的出现替代了java.util.concurrent.atomic和sun.misc.Unsafe的部分操作。并且提供了一系列标准的内存屏障操作，用于更加细粒度的控制内存排序。在安全性、可用性、性能上都要优于现有的API。VarHandle 可以与任何字段、数组元素或静态变量关联，支持在不同访问模型下对这些类型变量的访问，包括简单的 read/write 访问，volatile 类型的 read/write 访问，和 CAS(compare-and-swap)等。

Unsafe 是不建议开发者直接使用的，因为 Unsafe 所操作的并不属于Java标准，会容易带来一些安全性的问题。JDK9 之后，官方推荐使用 java.lang.invoke.Varhandle 来替代 Unsafe 大部分功能，对比 Unsafe ，Varhandle 有着相似的功能，但会更加安全，并且，在并发方面也提高了不少性能。

Varhandle是对变量或参数定义的变量系列的动态强类型引用，包括静态字段，非静态字段，数组元素或堆外数据结构的组件。 在各种访问模式下都支持访问这些变量，包括简单的读/写访问，volatile 的读/写访问以及 CAS (compare-and-set)访问。简单来说 Variable 就是对这些变量进行绑定，通过 Varhandle 直接对这些变量进行操作。

```java
import java.lang.invoke.MethodHandles;
import java.lang.invoke.VarHandle;
import java.util.Arrays;

public class VarHandleX {
    public int publicVar = 1;
    protected int protectedVar = 2;
    @SuppressWarnings("FieldMayBeFinal")
    private int privateVar = 3;
    public int[] arrayData = new int[]{1, 2, 3};

    @Override
    public String toString() {
        return "VarHandleX{" +
                "publicVar=" + publicVar +
                ", protectedVar=" + protectedVar +
                ", privateVar=" + privateVar +
                ", arrayData=" + Arrays.toString(arrayData) +
                '}';
    }

    public static void main(String[] args) {
        try {
            VarHandleX instance = new VarHandleX();
            VarHandle varHandle = MethodHandles.privateLookupIn(VarHandleX.class, MethodHandles.lookup())
                    .findVarHandle(VarHandleX.class, "privateVar", int.class);
            varHandle.set(instance, 33);
            System.out.println(instance);

            protectedDemo();
            protectedDemo2();
            publicDemo();
            arrayDemo();
        } catch (NoSuchFieldException | IllegalAccessException e) {
            e.printStackTrace();
        }
    }

    private static void protectedDemo() throws NoSuchFieldException, IllegalAccessException {
        VarHandleX instance = new VarHandleX();

        VarHandle varHandle = MethodHandles.privateLookupIn(VarHandleX.class, MethodHandles.lookup())
                .findVarHandle(VarHandleX.class, "protectedVar", int.class);


        varHandle.set(instance, 22);
        System.out.println("protected: " + instance);
    }

    private static void protectedDemo2() throws NoSuchFieldException, IllegalAccessException {
        VarHandleX instance = new VarHandleX();

        VarHandle varHandle = MethodHandles.lookup()
                .in(VarHandleX.class)
                .findVarHandle(VarHandleX.class, "protectedVar", int.class);
        varHandle.set(instance, 22);
        System.out.println("protected 2: " + instance);
    }

    private static void publicDemo() throws NoSuchFieldException, IllegalAccessException {
        VarHandleX instance = new VarHandleX();
        VarHandle varHandle = MethodHandles.lookup()
                .in(VarHandleX.class)
                .findVarHandle(VarHandleX.class, "publicVar", int.class);
        varHandle.set(instance, 11);
        System.out.println("public: " + instance);
    }

    private static void arrayDemo() throws NoSuchFieldException, IllegalAccessException {
        VarHandleX instance = new VarHandleX();
        VarHandle arrayVarHandle = MethodHandles.arrayElementVarHandle(int[].class);
        arrayVarHandle.compareAndSet(instance.arrayData, 0, 1, 11);
        arrayVarHandle.compareAndSet(instance.arrayData, 1, 2, 22);
        arrayVarHandle.compareAndSet(instance.arrayData, 2, 3, 33);
        System.out.println("array: " + instance);
    }
}
```

获取Varhandle方式汇总
MethodHandles.privateLookupIn(class, MethodHandles.lookup())获取访问私有变量的Lookup
MethodHandles.lookup() 获取访问protected、public的Lookup
findVarHandle: 用于创建对象中非静态字段的VarHandle。接收参数有三个，第一个为接收者的class对象，第二个是字段名称，第三个是字段类型。
findStaticVarHandle: 用于创建对象中静态字段的VarHandle，接收参数与findVarHandle一致。
unreflectVarHandle: 通过反射字段Field创建VarHandle。
MethodHandles.arrayElementVarHandle(int[].class) 获取管理数组的 Varhandle
功能
VarHandle来使用plain、opaque、release/acquire和volatile四种共享内存的访问模式，根据这四种共享内存的访问模式又分为写入访问模式、读取访问模式、原子更新访问模式、数值更新访问模式、按位原子更新访问模式。

写入访问模式(write access modes)
获取指定内存排序效果下的变量值，包含的方法有get、getVolatile、getAcquire、getOpaque 。

读取访问模式(read access modes)
在指定的内存排序效果下设置变量的值，包含的方法有set、setVolatile、 setRelease, setOpaque 。

### setRelease

Sets the value of a variable to the newValue, and ensures that prior loads and stores are not reordered after this access
给变量赋新值, 并且保证在此之前的load 和 store命令不会重排序到到setRelease 之后。

### getAcquire

返回一个变量 的值，并且保证随后的load 和 store 不会被重排序到此命令之前

### setOpaque

opaque 确保程序执行顺序，但不保证其它线程的可见顺序

### compareAndSet

### weakCompareAndSet

原子更新模式(atomic update access modes)
原子更新访问模式，例如，在指定的内存排序效果下，原子的比较和设置变量的值，包含的方法有compareAndSet、weakCompareAndSetPlain、weakCompareAndSet、weakCompareAndSetAcquire、weakCompareAndSetRelease、compareAndExchangeAcquire、compareAndExchange、compareAndExchangeRelease、getAndSet、getAndSetAcquire、getAndSetRelease 。

数值更新访问模式(numeric atomic update access modes)
数字原子更新访问模式，例如，通过在指定的内存排序效果下添加变量的值，以原子方式获取和设置。 包含的方法有getAndAdd、getAndAddAcquire、getAndAddRelease 。

按位原子更新访问模式(bitwise atomic update access modes )
按位原子更新访问模式，例如，在指定的内存排序效果下，以原子方式获取和按位OR变量的值。 包含的方法有getAndBitwiseOr、getAndBitwiseOrAcquire、getAndBitwiseOrRelease、 getAndBitwiseAnd、getAndBitwiseAndAcquire、getAndBitwiseAndRelease、getAndBitwiseXor、getAndBitwiseXorAcquire ， getAndBitwiseXorRelease 。

内存屏障
VarHandle 除了支持各种访问模式下访问变量之外，还提供了一套内存屏障方法，目的是为了给内存排序提供更细粒度的控制。主要如下几个方法:

public static void fullFence() {
    UNSAFE.fullFence();
}
public static void acquireFence() {
    UNSAFE.loadFence();
}
public static void releaseFence() {
    UNSAFE.storeFence();
}
public static void loadLoadFence() {
    UNSAFE.loadLoadFence();
}
public static void storeStoreFence() {
    UNSAFE.storeStoreFence();
}
小结
在 java9 之后，对一些变量的并发操作时，可以考虑用 java.lang.invoke.VarHandle 来处理，而不是通过 Unsafe 类来处理，毕竟 Unsafe 不太适合直接使用。

### weakCompareAndSet

jdk 8 的官方文档的java.util.concurrent.atomic上找到这么二段话:

The atomic classes also support method weakCompareAndSet, which has limited applicability. On some platforms, the weak version may be more efficient than compareAndSet in the normal case, but differs in that any given invocation of the weakCompareAndSet method may return false spuriously (that is, for no apparent reason). A false return means only that the operation may be retried if desired, relying on the guarantee that repeated invocation when the variable holds expectedValue and no other thread is also attempting to set the variable will eventually succeed. (Such spurious failures may for example be due to memory contention effects that are unrelated to whether the expected and current values are equal.) Additionally weakCompareAndSet does not provide ordering guarantees that are usually needed for synchronization control. However, the method may be useful for updating counters and statistics when such updates are unrelated to the other happens-before orderings of a program. When a thread sees an update to an atomic variable caused by a weakCompareAndSet, it does not necessarily see updates to any other variables that occurred before the weakCompareAndSet. This may be acceptable when, for example, updating performance statistics, but rarely otherwise.

一个原子类也支持weakCompareAndSet方法，该方法有适用性的限制。在一些平台上，在正常情况下weak版本比compareAndSet更高效，但是不同的是任何给定的weakCompareAndSet方法的调用都可能会返回一个虚假的失败( 无任何明显的原因 )。一个失败的返回意味着，操作将会重新执行如果需要的话，重复操作依赖的保证是当变量持有expectedValue的值并且没有其他的线程也尝试设置这个值将最终操作成功。( 一个虚假的失败可能是由于内存冲突的影响，而和预期值(expectedValue)和当前的值是否相等无关 )。此外weakCompareAndSet并不会提供排序的保证，即通常需要用于同步控制的排序保证。然而，这个方法可能在修改计数器或者统计，这种修改无关于其他happens-before的程序中非常有用。当一个线程看到一个通过weakCompareAndSet修改的原子变量时，它不被要求看到其他变量的修改，即便该变量的修改在weakCompareAndSet操作之前。

weakCompareAndSet atomically reads and conditionally writes a variable but does not create any happens-before orderings, so provides no guarantees with respect to previous or subsequent reads and writes of any variables other than the target of the weakCompareAndSet.

weakCompareAndSet实现了一个变量原子的读操作和有条件的原子写操作，但是它不会创建任何happen-before排序，所以该方法不提供对weakCompareAndSet操作的目标变量以外的变量的在之前或在之后的读或写操作的有序保证。

这二段话是什么意思了，也就是说weakCompareAndSet底层不会创建任何happen-before的保证，也就是不会对volatile字段操作的前后加入内存屏障。因此就无法保证多线程操作下对除了weakCompareAndSet操作的目标变量( 该目标变量一定是一个volatile变量 )之其他的变量读取和写入数据的正确性。

普通变量、opaque、release/acquire、volatile之间的区别

普通变量是不确保内存可见的，opaque、release/acquire、volatile是可以保证内存可见的
opaque 确保程序执行顺序，但不保证其它线程的可见顺序
release/acquire 保证程序执行顺序，setRelease 确保前面的load和store不会被重排序到后面，但不确保后面的load和store重排序到前面；getAcquire 确保后面的load和store不会被重排序到前面，但不确保前面的load和store被重排序。
volatile确保程序执行顺序，能保证变量之间的不被重排序。

作者: tomas家的小拨浪鼓
链接: [https://www.jianshu.com/p/55a66113bc54](https://www.jianshu.com/p/55a66113bc54)
来源: 简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

>[https://zhuanlan.zhihu.com/p/144741342](https://zhuanlan.zhihu.com/p/144741342)
>[https://zhuanlan.zhihu.com/p/145654924](https://zhuanlan.zhihu.com/p/145654924)
>[https://mingshan.fun/2018/10/05/use-variablehandles-to-replace-unsafe/](https://mingshan.fun/2018/10/05/use-variablehandles-to-replace-unsafe/)
>[https://www.jianshu.com/p/e231042a52dd](https://www.jianshu.com/p/e231042a52dd)
