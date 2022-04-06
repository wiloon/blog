---
title: java ByteBuffer
author: "-"
date: 2015-08-05T04:32:55+00:00
url: ByteBuffer
categories:
  - java
tags:
  - Java

---
## java ByteBuffer

ByteBuffer 是 NIO 里用得最多的 Buffer, 它包含两个实现方式: HeapByteBuffer 是基于Java堆的实现, 而 DirectByteBuffer 则使用了 unsafe 的 API 进行了堆外的实现。这里只说 HeapByteBuffer。

Buffer 类
  
定义了一个可以线性存放primitive type数据的容器接口。Buffer主要包含了与类型 (byte, char…) 无关的功能。
  
值得注意的是Buffer及其子类都不是线程安全的。

每个Buffer都有以下的属性: 
  
capacity
  
这个Buffer最多能放多少数据。capacity一般在buffer被创建的时候指定。

limit
  
在Buffer上进行的读写操作都不能越过这个下标。当写数据到buffer中时,limit一般和capacity相等,当读数据时,
  
limit代表buffer中有效数据的长度。

position
  
读/写操作的当前下标。当使用buffer的相对位置进行读/写操作时,读/写会从这个下标进行,并在操作完成后,
  
buffer会更新下标的值。

mark
  
一个临时存放的位置下标。调用mark()会将mark设为当前的position的值,以后调用reset()会将position属性设
  
置为mark的值。mark的值总是小于等于position的值,如果将position的值设的比mark小,当前的mark值会被抛弃掉。

这些属性总是满足以下条件: 
  
0 <= mark <= position <= limit <= capacity

limit和position的值除了通过limit()和position()函数来设置,也可以通过下面这些函数来改变: 

Buffer clear()
  
把position设为0,把limit设为capacity,一般在把数据写入Buffer前调用。

Buffer flip()
  
把limit设为当前position,把position设为0,一般在从Buffer读出数据前调用。

Buffer rewind()
  
把position设为0,limit不变,一般在把数据重写入Buffer前调用。

Buffer 对象有可能是只读的, 这时, 任何对该对象的写操作都会触发一个 ReadOnlyBufferException
  
isReadOnly()方法可以用来判断一个Buffer是否只读。

Buffer是一个抽象的基类
  
派生类: ByteBuffer, CharBuffer, DoubleBuffer, FloatBuffer, IntBuffer, LongBuffer, ShortBuffer

ByteBuffer 类
  
在Buffer的子类中,ByteBuffer是一个地位较为特殊的类,因为在java.io.channels中定义的各种channel的IO
  
操作基本上都是围绕ByteBuffer展开的。

ByteBuffer定义了4个static方法来做创建工作: 

ByteBuffer allocate(int capacity) //创建一个指定capacity的ByteBuffer。
  
ByteBuffer allocateDirect(int capacity) //创建一个direct的ByteBuffer,这样的ByteBuffer在参与IO操作时性能会更好
  
ByteBuffer wrap(byte [] array)
  
ByteBuffer wrap(byte [] array, int offset, int length) //把一个byte数组或byte数组的一部分包装成ByteBuffer。

ByteBuffer定义了一系列get和put操作来从中读写byte数据,如下面几个: 
  
byte get()
  
ByteBuffer get(byte [] dst)
  
byte get(int index)
  
ByteBuffer put(byte b)
  
ByteBuffer put(byte [] src)
  
ByteBuffer put(int index, byte b)
  
这些操作可分为绝对定位和相对定为两种,相对定位的读写操作依靠position来定位Buffer中的位置,并在操
  
作完成后会更新position的值。在其它类型的buffer中,也定义了相同的函数来读写数据,唯一不同的就是一
  
些参数和返回值的类型。

除了读写byte类型数据的函数,ByteBuffer的一个特别之处是它还定义了读写其它primitive数据的方法,如: 

int getInt() //从ByteBuffer中读出一个int值。
  
ByteBuffer putInt(int value) // 写入一个int值到ByteBuffer中。

读写其它类型的数据牵涉到字节序问题,ByteBuffer会按其字节序 (大字节序或小字节序) 写入或读出一个其它
  
类型的数据 (int,long…) 。字节序可以用order方法来取得和设置: 
  
ByteOrder order() //返回ByteBuffer的字节序。
  
ByteBuffer order(ByteOrder bo) // 设置ByteBuffer的字节序。

ByteBuffer另一个特别的地方是可以在它的基础上得到其它类型的buffer。如: 
  
CharBuffer asCharBuffer()
  
为当前的ByteBuffer创建一个CharBuffer的视图。在该视图buffer中的读写操作会按照ByteBuffer的字节
  
序作用到ByteBuffer中的数据上。

用这类方法创建出来的buffer会从ByteBuffer的position位置开始到limit位置结束,可以看作是这段数据
  
的视图。视图buffer的readOnly属性和direct属性与ByteBuffer的一致,而且也只有通过这种方法,才可
  
以得到其他数据类型的direct buffer。

ByteOrder
  
用来表示ByteBuffer字节序的类,可将其看成java中的enum类型。主要定义了下面几个static方法和属性: 
  
ByteOrder BIG_ENDIAN 代表大字节序的ByteOrder。
  
ByteOrder LITTLE_ENDIAN 代表小字节序的ByteOrder。
  
ByteOrder nativeOrder() 返回当前硬件平台的字节序。

MappedByteBuffer
  
ByteBuffer的子类,是文件内容在内存中的映射。这个类的实例需要通过FileChannel的map()方法来创建。

接下来看看一个使用ByteBuffer的例子,这个例子从标准输入不停地读入字符,当读满一行后,将收集的字符
  
写到标准输出: 

    public static void main(String [] args)
       throws IOException
    {
       // 创建一个capacity为256的ByteBuffer
       ByteBuffer buf = ByteBuffer.allocate(256);
       while (true) {
           // 从标准输入流读入一个字符
           int c = System.in.read();
           // 当读到输入流结束时,退出循环
           if (c == -1)
              break;
           // 把读入的字符写入ByteBuffer中
           buf.put((byte) c);
           // 当读完一行时,输出收集的字符
           if (c == '\n') {
              // 调用flip()使limit变为当前的position的值,position变为0,
              // 为接下来从ByteBuffer读取做准备
              buf.flip();
              // 构建一个byte数组
              byte [] content = new byte[buf.limit()];
              // 从ByteBuffer中读取数据到byte数组中
              buf.get(content);
               // 把byte数组的内容写到标准输出
              System.out.print(new String(content));
              // 调用clear()使position变为0,limit变为capacity的值,
              // 为接下来写入数据到ByteBuffer中做准备
              buf.clear();
           }
      }
    }
    

DirectByteBuffer
  
堆外内存,堆外内存能减少IO时的内存复制,不需要堆内存Buffer拷贝一份到直接内存中,然后才写入Socket中；而且也没了GC.
  
Netty所用的堆外内存只是Java NIO的 DirectByteBuffer类,还有一些sun.misc.*的类没有源码,得去OpenJdk看。
  
- 堆外内存的限额默认与堆内内存(由-XMX 设定)相仿,可用 -XX:MaxDirectMemorySize 重新设定。

http://calvin1978.blogcn.com/articles/directbytebuffer.html

ByteBuffer是NIO里用得最多的Buffer,它包含两个实现方式: HeapByteBuffer是基于Java堆的实现,而DirectByteBuffer则使用了unsafe的API进行了堆外的实现。这里只说HeapByteBuffer。

使用

ByteBuffer最核心的方法是put(byte)和get()。分别是往ByteBuffer里写一个字节,和读一个字节。

值得注意的是,ByteBuffer的读写模式是分开的,正常的应用场景是: 往ByteBuffer里写一些数据,然后flip(),然后再读出来。

这里插两个Channel方面的对象,以便更好的理解Buffer。

ReadableByteChannel是一个从Channel中读取数据,并保存到ByteBuffer的接口,它包含一个方法: 

public int read(ByteBuffer dst) throws IOException;
  
WritableByteChannel则是从ByteBuffer中读取数据,并输出到Channel的接口: 

public int write(ByteBuffer src) throws IOException;
  
那么,一个ByteBuffer的使用过程是这样的: 

byteBuffer = ByteBuffer.allocate(N);
  
//读取数据,写入byteBuffer
  
readableByteChannel.read(byteBuffer);
  
//变读为写
  
byteBuffer.flip();
  
//读取byteBuffer,写入数据
  
writableByteChannel.write(byteBuffer);
  
看到这里,一般都不太明白flip()干了什么事,先从ByteBuffer结构说起: 

ByteBuffer内部字段

byte[] buff

buff即内部用于缓存的数组。

position

当前读取的位置。

mark

为某一读过的位置做标记,便于某些时候回退到该位置。

capacity
  
初始化时候的容量。

limit
  
读写的上限,limit<=capacity。

put
  
写模式下,往buffer里写一个字节,并把postion移动一位。写模式下,一般limit与capacity相等

flip
  
写完数据,需要开始读的时候,将postion复位到0,并将limit设为当前postion。

get
  
从buffer里读一个字节,并把postion移动一位。上限是limit,即写入数据的最后位置。

clear
  
将position置为0,并不清除buffer内容。

mark相关的方法主要是mark()(标记)和reset()(回到标记)

Netty作为一个优秀网络框架,其高效的内存操作也是使其变得高性能的很重要原因之一。

众所周知,Java的NIO中提供了类ByteBuffer作为字节的容器,但是操作非常的复杂,Netty针对ByteBuffer设计了一个替代类ByteBuf,方便开发者操作字节。

ByteBuf API
  
对于任意一个ByteBuf对象,都拥有三个非常重要的属性: 

readerIndex: 读索引
  
writerIndex: 写索引
  
capacity: 对象容量
  
ByteBuf对象每读取一个byte的数据,readerIndex就会往前推进,直到readerIndex到达capacity的值,所有的数据的数据都被读取完,ByteBuf不可再被读取。可以通过readableBytes()方法获取readerIndex的值。

相同地,writerIndex记录了ByteBuf对象使用了多少数据,可以通过writableBytes()方法获取writerIndex的值。每当ByteBuf被写入了多少数据,writerIndex就会往前推进,直到值到达capacity的值,ByteBuf会自动对空间进行扩容。

对于任意一个ByteBuf对象,我们都可以根据它的索引通过getByte()方法随机访问中间的数据。随机访问不会改变readerIndex的值。

通过array()方法可以直接获取,ByteBuf中的Byte数组信息。

几种ByteBuf模式
  
Netty的"Zero-Copy"设计非常出名,这主要就是依赖了Netty中ByteBuf的设计。ByteBuf主要有以下几种模式: 

1.Heap Buffer模式
  
顾名思义,这个模式下的字节是在Jvm的堆区操作的,也是最常见的内存操作了。

2.Direct Buffer模式
  
在JDK1.4中,Java引入了一种直接内存,NIO可以通过本地方法分配一些堆外的直接内存,这块内存区不受Jvm的控制,理论上的无限的。

对于网络Socket通信来说,这种内存区域的好处是Java在通信中,数据不必从Jvm中拷贝一份到系统的直接内存区上,操作系统的Socket接口可以直接处理这份在直接内存的数据。同时由于数据在堆外,也避免了频繁GC对这块区域的影响。

ByteBuf提供了Direct Buffer模式,我们可以直接通过ByteBuf操作直接内存。

Direct Buffer模式下,由于数据不在堆上面,ByteBuf是不可以直接使用array()方法获取数据的。

3.Composite buffer模式
  
在TCP协议中,一份完整的数据总是被拆成好几个包被发送或者接收,一般情况下,程序会通过内存拷贝的方式将一组数据拷贝到一个大的数组中,形成一份完整的数据。

而Composite buffer模式可以聚合多个ByteBuffer对象,将这组数据的引用收集到一个ByteBuf对象中,避免了数据的拷贝。

// 初始化一个Composite buffer模式的`ByteBuf`
  
CompositeByteBuf compositeByteBuf = Unpooled.compositeBuffer(size);

// 添加byteBuf对象
  
compositeByteBuf.addComponent(byteBuf1);
  
compositeByteBuf.addComponent(byteBuf2);
  
compositeByteBuf.addComponent(byteBuf3);

// 操作compositeByteBuf
  
handle(compositeByteBuf);
  
分配内存的方式
  
当然为了避免Netty本身内存使用过度,Netty内部对所有的内存做了池化。通过ByteBufAllocator类,我们可以分配一块被池化的内存,从而减少分配和释放内存的开销。

ByteBuf buffer = ByteBufAllocator.DEFAULT.buffer();
  
ByteBuf buffer = ByteBufAllocator.DEFAULT.heapBuffer();
  
ByteBuf buffer = ByteBufAllocator.DEFAULT.ioBuffer();
  
ByteBuf buffer = ByteBufAllocator.DEFAULT.directBuffer();
  
ByteBuf buffer = ByteBufAllocator.DEFAULT.compositeBuffer();
  
如果我们希望使用一块新的内存,或者对一个已经存在的内存进行包装,那么我们可以使用Unpooled类来分配内存:

ByteBuf heapBuffer = buffer(128);
  
ByteBuf directBuffer = directBuffer(256);
  
ByteBuf wrappedBuffer = wrappedBuffer(new byte[128], new byte[256]);
  
ByteBuf copiedBuffe r = copiedBuffer(ByteBuffer.allocate(128));

http://www.jianshu.com/p/6db22e7e1230
  
http://blog.csdn.net/mars5337/article/details/6576417

在NIO中,数据的读写操作始终是与缓冲区相关联的.读取时信道(SocketChannel)将数据读入缓冲区,写入时首先要将发送的数据按顺序填入缓冲区.缓冲区是定长的,基本上它只是一个列表,它的所有元素都是基本数据类型.ByteBuffer是最常用的缓冲区,它提供了读写其他数据类型的方法,且信道的读写方法只接收ByteBuffer.因此ByteBuffer的用法是有必要牢固掌握的.

1.创建ByteBuffer
  
1.1 使用allocate()静态方法
  
ByteBuffer buffer=ByteBuffer.allocate(256);
  
以上方法将创建一个容量为256字节的ByteBuffer,如果发现创建的缓冲区容量太小,唯一的选择就是重新创建一个大小合适的缓冲区.

1.2 通过包装一个已有的数组来创建
  
如下,通过包装的方法创建的缓冲区保留了被包装数组内保存的数据.
  
ByteBuffer buffer=ByteBuffer.wrap(byteArray);

如果要将一个字符串存入ByteBuffer,可以如下操作:
  
String sendString="你好,服务器. ";
  
ByteBuffer sendBuffer=ByteBuffer.wrap(sendString.getBytes("UTF-16"));

2.回绕缓冲区
  
buffer.flip();
  
这个方法用来将缓冲区准备为数据传出状态,执行以上方法后,输出通道会从数据的开头而不是末尾开始.回绕保持缓冲区中的数据不变,只是准备写入而不是读取.

3.清除缓冲区
  
buffer.clear();
  
这个方法实际上也不会改变缓冲区的数据,而只是简单的重置了缓冲区的主要索引值.不必为了每次读写都创建新的缓冲区,那样做会降低性能.相反,要重用现在的缓冲区,在再次读取之前要清除缓冲区.

4.从 socket 通道(信道)读取数据
  
int bytesReaded=socketChannel.read(buffer);
  
执行以上方法后,通道会从socket读取的数据填充此缓冲区,它返回成功读取并存储在缓冲区的字节数.在默认情况下,这至少会读取一个字节,或者返回-1指示数据结束.

5.向 socket 通道(信道)写入数据
  
socketChannel.write(buffer);
  
此方法以一个ByteBuffer为参数,试图将该缓冲区中剩余的字节写入信道.

ByteBuffer俗称缓冲器, 是将数据移进移出通道的唯一方式,并且我们只能创建一个独立的基本类型缓冲器,或者使用"as"方法从 ByteBuffer 中获得。ByteBuffer 中存放的是字节,如果要将它们转换成字符串则需要使用 Charset , Charset 是字符编码,它提供了把字节流转换成字符串 ( 解码 ) 和将字符串转换成字节流 ( 编码) 的方法。

private byte[] getBytes (char[] chars) {//将字符转为字节(编码)
  
Charset cs = Charset.forName ("UTF-8");
  
CharBuffer cb = CharBuffer.allocate (chars.length);
  
cb.put (chars);
  
cb.flip ();
  
ByteBuffer bb = cs.encode (cb)
  
return bb.array();
  
}

private char[] getChars (byte[] bytes) {//将字节转为字符(解码)
  
Charset cs = Charset.forName ("UTF-8");
  
ByteBuffer bb = ByteBuffer.allocate (bytes.length);
  
bb.put (bytes);
  
bb.flip ();
  
CharBuffer cb = cs.decode (bb);

return cb.array();
  
}
  
通道也就是FileChannel,可以由FileInputStream,FileOutputStream,RandomAccessFile三个类来产生,例如: FileChannel fc = new FileInputStream().getChannel();与通道交互的一般方式就是使用缓冲器,可以把通道比如为煤矿(数据区),而把缓冲器比如为运煤车,想要得到煤一般都通过运煤车来获取,而不是直接和煤矿取煤。用户想得到数据需要经过几个步骤: 

一、用户与ByteBuffer的交互

向ByteBuffer中输入数据,有两种方式但都必须先为ByteBuffer指定容量

ByteBuffer buff = ByteBuffer.allocate(BSIZE);

a)  buff  =  ByteBuffer.wrap("askjfasjkf".getBytes())注意: wrap方法是静态函数且只能接收byte类型的数据,任何其他类型的数据想通过这种方式传递,需要进行类型的转换。

b)  buff.put();可以根据数据类型做相应调整,如buff.putChar(chars),buff.putDouble(double)等

二、FileChannel 与 ByteBuffer的交互: 

缓冲器向通道输入数据

FileChannel fc = new FileInputStream().getChannel();

fc.write(buff);

fc.close();

三、 用户与ByteBuffer交互

通道向缓冲器送入数据

FileChannel fc =  new FileOutputStream().getChannel();

fc.read( buff);

fc.flip();

四、呈现给用户 (三种方式) 

1)String encoding = System.getProperty("file.encoding");

System.out.println("Decoded using " + encoding + ": "  + Charset.forName(encoding).decode(buff));

2)System.out.println(buff.asCharBuffer());//这种输出时,需要在输入时就进行编码getBytes("UTF-8")

3) System.out.println(buff.asCharBuffer());//通过CharBuffer向ByteBuffer输入 buff.asCharBuffer().put。

fc.rewind();

https://my.oschina.net/flashsword/blog/159613
  
http://blog.csdn.net/jamesliulyc/article/details/6606335


## HeapByteBuffer, DirectByteBuffer
https://www.zhihu.com/question/60892134/answer/182225677
  
https://zhuanlan.zhihu.com/p/27625923

http://www.importnew.com/19191.html

而本文要说的一个重点就是HeapByteBuffer与DirectByteBuffer,以及如何合理使用DirectByteBuffer。

1. HeapByteBuffer 与 DirectByteBuffer, 在原理上, 前者可以看出分配的 buffer 是在 heap 区域的, 其实真正 flush 到远程的时候会先拷贝得到直接内存,再做下一步操作 (考虑细节还会到OS级别的内核区直接内存) , 其实发送静态文件最快速的方法是通过OS级别的 send_file, 只会经过 OS 一个内核拷贝, 而不会来回拷贝；在 NIO 的框架下,很多框架会采用 DirectByteBuffer 来操作,这样分配的内存不再是在java heap上,而是在C heap上,经过性能测试,可以得到非常快速的网络交互,在大量的网络交互下,一般速度会比HeapByteBuffer要快速好几倍。

最基本的情况下

分配HeapByteBuffer的方法是: 

ByteBuffer.allocate(int capacity);参数大小为字节的数量
  
分配DirectByteBuffer的方法是: 

ByteBuffer.allocateDirect(int capacity);//可以看到分配内存是通过unsafe.allocateMemory()来实现的,这个unsafe默认情况下java代码是没有能力可以调用到的,不过你可以通过反射的手段得到实例进而做操作,当然你需要保证的是程序的稳定性,既然叫unsafe的,就是告诉你这不是安全的,其实并不是不安全,而是交给程序员来操作,它可能会因为程序员的能力而导致不安全,而并非它本身不安全。

http://blog.csdn.net/u011262847/article/details/76861974

HeapByteBuffer
  
堆上的ByteBuffer对象,是调用ByteBuffer.allocate (n) 所分配出来的,底层是通过new出来的新对象,所以一定在堆上分配的存储空间,属于jvm所能够控制的范围。

public static ByteBuffer allocate(int capacity) {
          
if (capacity < 0)
              
throw new IllegalArgumentException();
          
return new HeapByteBuffer(capacity, capacity);
      
}

DirectByteBuffer
  
对于这种Bytebuffer的创建,我们可以看一下底层源码: 

public static ByteBuffer allocateDirect(int capacity) {
          
return new DirectByteBuffer(capacity);
      
}

同样是new出来的对象,我们也认为是在jvm堆上分配的存储空间

但是我们可以查看到DirectByteBuffer底层的实现: 

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

关键的是,allocateMemory是一个native方法,并不是jvm能够控制的内存区域,通常称为堆外内存,一般是通过c/c++分配的内存 (malloc) 。

也就是说,对于DirectByteBuffer所生成的ByteBuffer对象,一部分是在jvm堆内存上,一部分是操作系统上的堆内存上,那么为了操作堆外内存,一定在jvm堆上的对象有一个堆外内存的引用:

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
    

在DirectByteBuffer的父类中,可以看到address的一个变量,这个就是表示堆外内存所分配对象的地址,如此一来,jvm堆上的对象就会有一个堆外内存的一个引用,之所以需要这样做,是为了提升堆io的效率。

对于HeapByteBuffer,数据的分配存储都在jvm堆上,当需要和io设备打交道的时候,会将jvm堆上所维护的byte[]拷贝至堆外内存,然后堆外内存直接和io设备交互。如果直接使用DirectByteBuffer,那么就不需要拷贝这一步,将大大提升io的效率,这种称之为零拷贝 (zero-copy) 。
