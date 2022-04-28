---
title: "Unsafe"
author: "-"
date: "2021-09-20 23:38:32"
url: "unsafe"
categories:
  - Java
tags:
  - inbox
---
## "Unsafe"
# unsafe
Unsafe在sun.misc 下，顾名思义，这是一个不安全的类，因为Unsafe类所操作的并不属于Java标准，Java的一系列内存操作都是交给jvm的，而Unsafe类却能有像C语言的指针一样直接操作内存的能力，同时也会带来了指针的问题。过度使用Unsafe类的话，会使出错率变得更大，因此官方才命名为Unsafe，并且不建议使用，连注释的没有。
而为了安全使用Unsafe，Unsafe类只允许jdk自带的类使用，从下面的代码中可以看出
```java
public static Unsafe getUnsafe() {
     Class<?> caller = Reflection.getCallerClass();
     if (!VM.isSystemDomainLoader(caller.getClassLoader()))
         throw new SecurityException("Unsafe");
     return theUnsafe;
 }
 ```
 
如果当前Class是非系统加载的(也就是caller.getClassLoader()不为空)，直接抛出SecurityException 。

在java9之后，又出现了一个jdk.internal.misc.Unsafe类，其功能与sun.misc.Unsafe类是一样的，唯一不一样的是在 getSafe() 的时候，jdk.internal.misc.Unsafe是没有做校验的，但是jdk包下的代码，应用开发时是不能直接调用的，而且在java9之后，两个Unsafe类都有充足的注释。

JUC紧密使用了Unsafe的功能。

功能简介
Unsafe类的功能主要分为内存操作、CAS、Class相关、对象操作、数组相关、内存屏障、系统相关、线程调度等功能。

内存操作
堆外(native memory)内存操作
//分配内存，并返回内存地址
public native long allocateMemory(long bytes);
//扩充内存，address可以是allocateMemory方法返回的地址，bytes是扩充的大小
public native long reallocateMemory(long address, long bytes);
//释放内存
public native void freeMemory(long address);
//在给定的内存块设置默认值
public native void setMemory(long address, long bytes, byte value);
//获取指定地址值的byte类型
public native byte getByte(long address);
//设置堆外指定值的byte类型的值
public native void putByte(long address, byte x);

堆内内存操作
//在给定的内存块设置默认值
public native void setMemory(Object o, long offset, long bytes, byte value);
//内存拷贝
public native void copyMemory(Object srcBase, long srcOffset, Object destBase, long destOffset, long bytes);
//获取指定地址的值，offset为o对象某个field的偏移量，类似有: getInt,getDouble,getLong,getChar等
public native Object getObject(Object o, long offset);
//设置值，offset为o对象某个field的偏移量，类似的还有 putInt,putDouble,putLong,putChar等
public native void putObject(Object o, long offset, Object x);

通常，在java创建的对象都是在堆内存中的，堆内存是有JVM所托管，并且都遵循JVM内存管理机制。与之相对的是JAVA管核之外的堆外内存，是依赖Unsafe提供的操作堆外内存的native方法处理。

java带的NIO中的java.nio.DirectByteBuffer中就是用Unsafe的堆外内存函数来操作堆外内存。使用方法

ByteBuffer.allocateDirect(1024);
最终在 DirectByteBuffer** 的构造函数中调用 UNSAFE 来分配并初始化内存。

long base = 0;
try {
    base = UNSAFE.allocateMemory(size);
} catch (OutOfMemoryError x) {
    Bits.unreserveMemory(size, cap);
    throw x;
}
UNSAFE.setMemory(base, size, (byte) 0);

使用案例
堆外内存

Field theUnsafeField = Unsafe.class.getDeclaredField("theUnsafe");
theUnsafeField.setAccessible(true);
Unsafe unsafe = (Unsafe) theUnsafeField.get(Unsafe.class);
long address = unsafe.allocateMemory(1024);
unsafe.setMemory(address, 1024, (byte) 0);
unsafe.putInt(address, 1);
System.out.println(unsafe.getInt(address));
unsafe.freeMemory(address);
堆内内存

public class Demo {
    private static String name = "jfound";
    private int age = 10;
}
//-----------
Field theUnsafeField = Unsafe.class.getDeclaredField("theUnsafe");
theUnsafeField.setAccessible(true);
Unsafe unsafe = (Unsafe) theUnsafeField.get(Unsafe.class);

Demo demo = new Demo();
Field ageField = Demo.class.getDeclaredField("age");
ageField.setAccessible(true);
long ageFieldAddress = unsafe.objectFieldOffset(ageField);
System.out.println(unsafe.getInt(demo, ageFieldAddress));
Field nameField = Demo.class.getDeclaredField("name");
nameField.setAccessible(true);

unsafe.ensureClassInitialized(Demo.class); //初始化，否则name为null
long nameAddress = unsafe.staticFieldOffset(nameField);
System.out.println(unsafe.getObject(Demo.class, nameAddress)); //输出jfound

CAS
CAS，较并替换，CAS操作包含三个操作数——内存位置、预期原值及新值。执行CAS操作的时候，将内存位置的值与预期原值比较，如果相匹配，那么处理器会自动将该位置值更新为新值，否则，处理器不做任何操作。

此操作是CPU指令cmpxchg，是属于指令级别的，具有原子性 ，典型的 atomic下的类，AQS系列的锁都是借用Unsafe下的CAS的api来实现的。


Class相关
api
//获取给定静态字段的内存地址偏移量，这个值对于给定的字段是唯一且固定不变的
public native long staticFieldOffset(Field f);
//获取一个静态类中给定字段的对象指针
public native Object staticFieldBase(Field f);
//判断是否需要初始化一个类，通常在获取一个类的静态属性的时候 (因为一个类如果没初始化，它的静态属性也不会初始化) 使用。 当且仅当ensureClassInitialized方法不生效时返回false。
public native boolean shouldBeInitialized(Class<?> c);
//检测给定的类是否已经初始化。通常在获取一个类的静态属性的时候 (因为一个类如果没初始化，它的静态属性也不会初始化) 使用。
public native void ensureClassInitialized(Class<?> c);
//定义一个类，此方法会跳过JVM的所有安全检查，默认情况下，ClassLoader (类加载器) 和ProtectionDomain (保护域) 实例来源于调用者
public native Class<?> defineClass(String name, byte[] b, int off, int len, ClassLoader loader, ProtectionDomain protectionDomain);
//定义一个匿名类
public native Class<?> defineAnonymousClass(Class<?> hostClass, byte[] data, Object[] cpPatches);


对象操作
api
//返回对象成员属性在内存地址相对于此对象的内存地址的偏移量
public native long objectFieldOffset(Field f);
//获得给定对象的指定地址偏移量的值，与此类似操作还有: getInt，getDouble，getLong，getChar等
public native Object getObject(Object o, long offset);
//给定对象的指定地址偏移量设值，与此类似操作还有: putInt，putDouble，putLong，putChar等
public native void putObject(Object o, long offset, Object x);
//从对象的指定偏移量处获取变量的引用，使用volatile的加载语义
public native Object getObjectVolatile(Object o, long offset);
//存储变量的引用到对象的指定的偏移量处，使用volatile的存储语义
public native void putObjectVolatile(Object o, long offset, Object x);
//有序、延迟版本的putObjectVolatile方法，不保证值的改变被其他线程立即看到。只有在field被volatile修饰符修饰时有效
public native void putOrderedObject(Object o, long offset, Object x);
//绕过构造方法、初始化代码来创建对象,这个厉害吧
public native Object allocateInstance(Class<?> cls) throws InstantiationException;

数组相关
api
//返回数组中第一个元素的偏移地址
public native int arrayBaseOffset(Class<?> arrayClass);
//返回数组中一个元素占用的大小
public native int arrayIndexScale(Class<?> arrayClass);


内存屏障
api
//内存屏障，禁止load操作重排序。屏障前的load操作不能被重排序到屏障后，屏障后的load操作不能被重排序到屏障前
public native void loadFence();
//内存屏障，禁止store操作重排序。屏障前的store操作不能被重排序到屏障后，屏障后的store操作不能被重排序到屏障前
public native void storeFence();
//内存屏障，禁止load、store操作重排序
public native void fullFence();


系统相关
//返回系统指针的大小。返回值为4 (32位系统) 或 8 (64位系统) 。
public native int addressSize();  
//内存页的大小，此值为2的幂次方。
public native int pageSize();

线程调度
这部分包括了线程的挂起、回复、锁等方法，

api
//阻塞线程
public native void park(boolean isAbsolute, long time);
//取消阻塞线程
public native void unpark(Object thread);

park

阻塞当前线程直到一个unpark方法出现(被调用)、一个用于unpark方法已经出现过(在此park方法调用之前已经调用过)、线程被中断或者time时间到期(也就是阻塞超时)。在time非零的情况下，如果isAbsolute为true，time是相对于新纪元之后的毫秒，否则time表示纳秒

unpark

释放被park创建的在一个线程上的阻塞。这个方法也可以被使用来终止一个先前调用park导致的阻塞。这个操作是不安全的，因此必须保证线程是存活的(thread has not been destroyed)。


> https://zhuanlan.zhihu.com/p/144740005