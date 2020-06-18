---
title: HeapByteBuffer, DirectByteBuffer
author: wiloon
type: post
date: 2018-03-21T02:48:23+00:00
url: /?p=12009
categories:
  - Uncategorized

---
https://www.zhihu.com/question/60892134/answer/182225677
  
https://zhuanlan.zhihu.com/p/27625923

http://www.importnew.com/19191.html

而本文要说的一个重点就是HeapByteBuffer与DirectByteBuffer，以及如何合理使用DirectByteBuffer。

1、HeapByteBuffer与DirectByteBuffer，在原理上，前者可以看出分配的buffer是在heap区域的，其实真正flush到远程的时候会先拷贝得到直接内存，再做下一步操作（考虑细节还会到OS级别的内核区直接内存），其实发送静态文件最快速的方法是通过OS级别的send_file，只会经过OS一个内核拷贝，而不会来回拷贝；在NIO的框架下，很多框架会采用DirectByteBuffer来操作，这样分配的内存不再是在java heap上，而是在C heap上，经过性能测试，可以得到非常快速的网络交互，在大量的网络交互下，一般速度会比HeapByteBuffer要快速好几倍。

最基本的情况下

分配HeapByteBuffer的方法是：

1
  
ByteBuffer.allocate(int capacity);参数大小为字节的数量
  
分配DirectByteBuffer的方法是：

1
  
ByteBuffer.allocateDirect(int capacity);//可以看到分配内存是通过unsafe.allocateMemory()来实现的，这个unsafe默认情况下java代码是没有能力可以调用到的，不过你可以通过反射的手段得到实例进而做操作，当然你需要保证的是程序的稳定性，既然叫unsafe的，就是告诉你这不是安全的，其实并不是不安全，而是交给程序员来操作，它可能会因为程序员的能力而导致不安全，而并非它本身不安全。

http://blog.csdn.net/u011262847/article/details/76861974

HeapByteBuffer
  
堆上的ByteBuffer对象，是调用ByteBuffer.allocate（n）所分配出来的，底层是通过new出来的新对象，所以一定在堆上分配的存储空间，属于jvm所能够控制的范围。

public static ByteBuffer allocate(int capacity) {
          
if (capacity < 0)
              
throw new IllegalArgumentException();
          
return new HeapByteBuffer(capacity, capacity);
      
}

DirectByteBuffer
  
对于这种Bytebuffer的创建，我们可以看一下底层源码：

public static ByteBuffer allocateDirect(int capacity) {
          
return new DirectByteBuffer(capacity);
      
}

同样是new出来的对象，我们也认为是在jvm堆上分配的存储空间

但是我们可以查看到DirectByteBuffer底层的实现：

public native long allocateMemory(long var1);
  
...
  
long base = 0;
          
try {
              
base = unsafe.allocateMemory(size);
          
} catch (OutOfMemoryError x) {
              
Bits.unreserveMemory(size, cap);
              
throw x;
          
}
          
unsafe.setMemory(base, size, (byte) 0);
  
...

关键的是，allocateMemory是一个native方法，并不是jvm能够控制的内存区域，通常称为堆外内存，一般是通过c/c++分配的内存（malloc）。

也就是说，对于DirectByteBuffer所生成的ByteBuffer对象，一部分是在jvm堆内存上，一部分是操作系统上的堆内存上，那么为了操作堆外内存，一定在jvm堆上的对象有一个堆外内存的引用:

public abstract class Buffer {

    /**
     * The characteristics of Spliterators that traverse and split elements
     * maintained in Buffers.
     */
    static final int SPLITERATOR_CHARACTERISTICS =
        Spliterator.SIZED | Spliterator.SUBSIZED | Spliterator.ORDERED;
    
    // Invariants: mark <= position <= limit <= capacity
    private int mark = -1;
    private int position = 0;
    private int limit;
    private int capacity;
    
    // Used only by direct buffers
    // NOTE: hoisted here for speed in JNI GetDirectBufferAddress
    long address;
    

在DirectByteBuffer的父类中，可以看到address的一个变量，这个就是表示堆外内存所分配对象的地址，如此一来，jvm堆上的对象就会有一个堆外内存的一个引用，之所以需要这样做，是为了提升堆io的效率。

对于HeapByteBuffer，数据的分配存储都在jvm堆上，当需要和io设备打交道的时候，会将jvm堆上所维护的byte[]拷贝至堆外内存，然后堆外内存直接和io设备交互。如果直接使用DirectByteBuffer，那么就不需要拷贝这一步，将大大提升io的效率,这种称之为零拷贝（zero-copy）。