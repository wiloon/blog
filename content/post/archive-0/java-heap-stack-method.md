---
title: Java, 堆(Heap), 栈/线程栈(Stack), 方法区(method), 常量池
author: "-"
date: 2012-09-21T06:34:15+00:00
url: /?p=4151
categories:
  - Java

---
## Java, 堆(Heap), 栈/线程栈(Stack), 方法区(method Area), 常量池(Constant Pool)

[![4MnMpn.png](https://z3.ax1x.com/2021/09/17/4MnMpn.png)](https://imgtu.com/i/4MnMpn)

### heap, 堆
堆是线程共享的，所有的对象的实例和数组都存放在堆中，任何线程都可以访问。Java的垃圾自动回收机制就是运用这个区域的。

### Stack(栈), thread stacks(线程栈), call stack, Execution stack
栈是线程私有的，每个线程都是自己的栈，每个线程中的每个方法在执行的同时会创建一个栈帧用于保存 PC(程序计数器) 局部变量表、操作数栈、动态链接、方法返回地址等信息。每一个方法从调用到执行完毕的过程，就对应着一个栈帧在虚拟机栈中从入栈到出栈的过程。其中局部变量表，存放基本类型（boolean、byte、char、short、int、float) 、对象的引用等等，对象的引用不是对象实例本身，而是指向对象实例的一个指针。
————————————————
版权声明: 本文为CSDN博主「万猫学社」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接: https://blog.csdn.net/heihaozi/article/details/102752636

内存指令区，存储数据: 基本数据类型, 指令代码,常量,对象的引用地址(2)

Hotspot VM: 
1. 栈内存从概念上分 “线程的栈内存” 和 “JVM的栈内存” 两种。
2. 线程的栈内存: 每新建一个线程时，会分配给这个线程一个栈内存初始值，最大的大小可通过 -Xss 来设置。线程占有的栈内存大小，通过不断执行方法，生成局部变量等操作，栈桢不断增加，该线程的栈内存也不断被使用。最终达到 -Xss 的值时，会抛出 StackOverFlowError。其实这里就是线程的栈内存溢出，背后的概念与 OOME 是一样的，只是jvm设计者取的名字不一样而已。3.JVM的栈内存: 当一个jvm进程启动时，会不断消耗 native memory。我们可以通过参数 -Xmx 等来设置堆内存、方法区内存的最大值，当达到阀值时，jvm就会报OOME。但是栈内存大小，则是物理机器的 native memory，其上限就是native memory的上限。不断建线程消耗native memory待尽时，就会报OOME。

作者: chiukong
链接: https://www.zhihu.com/question/28637033/answer/41677862
来源: 知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
 
1. 保存对象实例，实际上是保存对象实例的属性值，属性的类型和对象本身的类型标记等，并不保存对象的方法（方法是指令，保存在stack中) 。对象实例在heap中分配好以后，需要在stack中保存一个4字节的heap内存地址，用来定位该对象实例在heap中的位置，便于找到该对象实例。 
2. 基本数据类型包括byte、int、char、long、float、double、boolean和short。
  
函数方法属于指令
  引用网上广泛流传的"Java堆和栈的区别"里面对堆和栈的介绍；
  
"Java 的堆是一个运行时数据区, 类的(对象从中分配空间。这些对象通过new、newarray、anewarray和multianewarray等指令建立，它们不需要程序代码来显式的释放。堆是由垃圾回收来负责的，堆的优势是可以动态地分配内存大小，生存期也不必事先告诉编译器，因为它是在运行时动态分配内存的，Java的垃圾收集器会自动收走这些不再使用的数据。但缺点是，由于要在运行时动态分配内存，存取速度较慢。"

"栈的优势是，存取速度比堆要快，仅次于寄存器，栈数据可以共享。但缺点是，存在栈中的数据大小与生存期必须是确定的，缺乏灵活性。栈中主要存放一些基本类型的变量（,int, short, long, byte, float, double, boolean, char) 和对象句柄。 "

可见，垃圾回收GC是针对堆Heap的，而栈因为本身是FILO - first in, last out. 先进后出，能够自动释放。 这样就能明白到new创建的，都是放到堆Heap！

### 方法区
方法区（method area) 只是JVM规范中定义的一个概念, 方法区也是线程共享的，用于存放 类信息（包括类的名称、方法信息、字段信息), 常量(常量池)、静态变量, JIT编译后的代码 以及即时编译器编译后的代码等等。

1. 又叫静态区，跟堆一样，被所有的线程共享。方法区包含所有的class和static变量。
2. 方法区中包含的都是在整个程序中永远唯一的元素，如 class，static 变量。

永久代/方法区 也属于 GC Heap 的一部分。另外，方法区（method area)，具体放在哪里，不同的实现可以放在不同的地方。而永久代是 Hotspot 虚拟机特有的概念，是方法区的一种实现，别的JVM都没有这个东西。

---

在Java 6中，方法区中包含的数据，除了JIT编译生成的代码存放在 native memory 的CodeCache区域，其他都存放在永久代；

在Java 7中，Symbol的存储从PermGen移动到了native memory，并且把静态变量从instanceKlass末尾（位于PermGen内) 移动到了java.lang.Class对象的末尾（位于普通Java heap内) 

在Java 8中，永久代被彻底移除，取而代之的是另一块与堆不相连的本地内存——元空间（Metaspace) ,‑XX:MaxPermSize 参数失去了意义，取而代之的是 -XX:MaxMetaspaceSize。

可参考: 
Chapter 2. The Structure of the Java Virtual Machine
  
JEP 122: Remove the Permanent Generation

在中文里，Stack可以翻译为"堆栈"，所以我直接查找了计算机术语里面堆和栈开头的词语: 
  
堆存储:  heapstorage
  
堆存储分配:  heapstorage allocation
  
堆存储管理:  heap storage management
  
栈编址:  stack addressing
  
栈变换: stack transformation
  
栈存储器: stack memory
  
栈单元:  stack cell
  
接着，总结在Java里面Heap和Stack分别存储数据的不同。
  
Heap(堆):  内存数据区，存储数据: 对象实例(1)

---

基础数据类型直接在栈空间分配， 方法的形式参数，直接在栈空间分配，当方法调用完成后从栈空间回收。 引用数据类型，需要用new来创建，既在栈空间分配一个地址空间，又在堆空间分配对象的类变量 。 方法的引用参数，在栈空间分配一个地址空间，并指向堆空间的对象区，当方法调用完成后从栈空间回收。局部变量 new 出来时，在栈空间和堆空间中分配空间，当局部变量生命周期结束后，栈空间立刻被回收，堆空间区域等待GC回收。 方法调用时传入的 literal 参数，先在栈空间分配，在方法调用完成后从栈空间分配。字符串常量在 DATA 区域分配 ，this 在堆空间分配 。数组既在栈空间分配数组名称， 又在堆空间分配数组实际的大小！
  
哦 对了，补充一下static在DATA区域分配。

从Java的这种分配机制来看,堆栈又可以这样理解:堆栈(Stack)是操作系统在建立某个进程时或者线程(在支持多线程的操作系统中是线程)为这个线程建立的存储区域，该区域具有先进后出的特性。
  
每一个Java应用都唯一对应一个JVM实例，每一个实例唯一对应一个堆。应用程序在运行中所创建的所有类实例或数组都放在这个堆中,并由应用所有的线程共享.跟C/C++不同，Java中分配堆内存是自动初始化的。Java中所有对象的存储空间都是在堆中分配的，但是这个对象的引用却是在堆栈中分配,也就是说在建立一个对象时从两个地方都分配内存，在堆中分配的内存实际建立这个对象，而在堆栈中分配的内存只是一个指向这个堆对象的指针(引用)而已。

<二>
  
JAVA的JVM的内存可分为3个区: 堆(heap)、栈(stack)和方法区(method)

堆区:
  
1.存储的全部是对象，每个对象都包含一个与之对应的class的信息。(class的目的是得到操作指令)
  
2.jvm只有一个堆区(heap)被所有线程共享，堆中不存放基本类型和对象引用，只存放对象本身
  
栈区:
  
1.每个线程包含一个栈区，栈中只保存基础数据类型的对象和自定义对象的引用(不是对象)，对象都存放在堆区中
  
2.每个栈中的数据(原始类型和对象引用)都是私有的，其他栈不能访问。
  
3.栈分为3个部分: 基本类型变量区、执行环境上下文、操作指令区(存放操作指令)。
  

为了更清楚地搞明白发生在运行时数据区里的黑幕，我们来准备2个小道具（2个非常简单的小程序) 。

AppMain.java

public class AppMain //运行时, jvm 把appmain的信息都放入方法区
  
{
  
public static void main(String[] args) //main 方法本身放入方法区。
  
{
  
Sample test1 = new Sample( " 测试1 " ); //test1是引用，所以放到栈区里， Sample是自定义对象应该放到堆里面
  
Sample test2 = new Sample( " 测试2 " );

test1.printName();
  
test2.printName();
  
}
  
} Sample.java

public class Sample //运行时, jvm 把appmain的信息都放入方法区
  
{
  
/*\* 范例名称 */
  
private name; //new Sample实例后， name 引用放入栈区里， name 对象放入堆里

/*\* 构造方法 */
  
public Sample(String name)
  
{
  
this .name = name;
  
}

/*\* 输出 */
  
public void printName() //print方法本身放入 方法区里。
  
{
  
System.out.println(name);
  
}
  
}

OK，让我们开始行动吧，出发指令就是: "java AppMain"，包包里带好我们的行动向导图，Let's GO！

系统收到了我们发出的指令，启动了一个Java虚拟机进程，这个进程首先从classpath中找到AppMain.class文件，读取这个文件中的二进制数据，然后把Appmain类的类信息存放到运行时数据区的方法区中。这一过程称为AppMain类的加载过程。
  
接着，Java虚拟机定位到方法区中AppMain类的Main()方法的字节码，开始执行它的指令。这个main()方法的第一条语句就是: 
  
Sample test1=new Sample("测试1");
  
语句很简单啦，就是让java虚拟机创建一个Sample实例，并且呢，使引用变量test1引用这个实例。貌似小case一桩哦，就让我们来跟踪一下Java虚拟机，看看它究竟是怎么来执行这个任务的: 
  
1.  Java虚拟机一看，不就是建立一个Sample实例吗，简单，于是就直奔方法区而去，先找到Sample类的类型信息再说。结果呢，嘿嘿，没找到@@，这会儿的方法区里还没有Sample类呢。可Java虚拟机也不是一根筋的笨蛋，于是，它发扬"自己动手，丰衣足食"的作风，立马加载了Sample类，把Sample类的类型信息存放在方法区里。
  
2.  好啦，资料找到了，下面就开始干活啦。Java虚拟机做的第一件事情就是在堆区中为一个新的Sample实例分配内存, 这个Sample实例持有着指向方法区的Sample类的类型信息的引用。这里所说的引用，实际上指的是Sample类的类型信息在方法区中的内存地址，其实，就是有点类似于C语言里的指针啦~~，而这个地址呢，就存放了在Sample实例的数据区里。
  
3.  在JAVA虚拟机进程中，每个线程都会拥有一个方法调用栈，用来跟踪线程运行中一系列的方法调用过程，栈中的每一个元素就被称为栈帧，每当线程调用一个方法的时候就会向方法栈压入一个新帧。这里的帧用来存储方法的参数、局部变量和运算过程中的临时数据。OK，原理讲完了，就让我们来继续我们的跟踪行动！位于"="前的Test1是一个在main()方法中定义的变量，可见，它是一个局部变量，因此，它被会添加到了执行main()方法的主线程的JAVA方法调用栈中。而"="将把这个test1变量指向堆区中的Sample实例，也就是说，它持有指向Sample实例的引用。
  
OK，到这里为止呢，JAVA虚拟机就完成了这个简单语句的执行任务。参考我们的行动向导图，我们终于初步摸清了JAVA虚拟机的一点点底细了，COOL！
  
接下来，JAVA虚拟机将继续执行后续指令，在堆区里继续创建另一个Sample实例，然后依次执行它们的printName()方法。当JAVA虚拟机执行test1.printName()方法时，JAVA虚拟机根据局部变量test1持有的引用，定位到堆区中的Sample实例，再根据Sample实例持有的引用，定位到方法去中Sample类的类型信息，从而获得printName()方法的字节码，接着执行printName()方法包含的指令。

<三>

在windows中使用taskmanager查看java进程使用的内存时，发现有时候会超过 -Xmx制定的内存大小， -Xmx指定的是java heap，java还要分配内存做其他的事情，包括为每个线程建立栈。
  
VM的每个线程都有自己的栈空间，栈空间的大小限制vm的线程数量，太大了，实用的线程数减少，太小容易抛出java.lang.StackOverflowError异常。windows默认为1M，linux必须运行ulimit -s 2048。
  
在C语言里堆(heap)和栈(stack)里的区别
  
简单的可以理解为: 
  
heap: 是由malloc之类函数分配的空间所在地。地址是由低向高增长的。
  
stack: 是自动分配变量，以及函数调用的时候所使用的一些空间。地址是由高向低减少。
  
一个由c/C++编译的程序占用的内存分为以下几个部分
  
1. 栈区（stack) — 由编译器自动分配释放 ，存放函数的参数值，局部变量的值等。其操作方式类似于数据结构中的栈。
  
2. 在Java语言里堆(heap)和栈(stack)里的区别
      
1. 栈(stack)与堆(heap)都是Java用来在Ram中存放数据的地方。与C++不同，Java自动管理栈和堆，程序员不能直接地设置栈或堆。
  
2. 栈的优势是，存取速度比堆要快，仅次于直接位于CPU中的寄存器。但缺点是，存在栈中的数据大小与生存期必须是确定的，缺乏灵活性。另外，栈数据可以共享，详见第3点。堆的优势是可以动态地分配内存大小，生存期也不必事先告诉编译器，Java的垃圾收集器会自动收走这些不再使用的数据。但缺点是，由于要在运行时动态分配内存，存取速度较慢。
  
3. Java中的数据类型有两种。
  
一种是基本类型(primitive types), 共有8种，即int, short, long, byte, float, double, boolean, char(注意，并没有string的基本类型)。这种类型的定义是通过诸如int a = 3; long b = 255L;的形式来定义的，称为自动变量。值得注意的是，自动变量存的是字面值，不是类的实例，即不是类的引用，这里并没有类的存在。如int a = 3; 这里的a是一个指向int类型的引用，指向3这个字面值。这些字面值的数据，由于大小可知，生存期可知(这些字面值固定定义在某个程序块里面，程序块退出后，字段值就消失了)，出于追求速度的原因，就存在于栈中。
  
另外，栈有一个很重要的特殊性，就是存在栈中的数据可以共享。假设我们同时定义
  
int a = 3;
  
int b = 3；
  
编译器先处理int a = 3；首先它会在栈中创建一个变量为a的引用，然后查找有没有字面值为3的地址，没找到，就开辟一个存放3这个字面值的地址，然后将a指向3的地址。接着处理int b = 3；在创建完b的引用变量后，由于在栈中已经有3这个字面值，便将b直接指向3的地址。这样，就出现了a与b同时均指向3的情况。
  
特别注意的是，这种字面值的引用与类对象的引用不同。假定两个类对象的引用同时指向一个对象，如果一个对象引用变量修改了这个对象的内部状态，那么另一个对象引用变量也即刻反映出这个变化。相反，通过字面值的引用来修改其值，不会导致另一个指向此字面值的引用的值也跟着改变的情况。如上例，我们定义完a与 b的值后，再令a=4；那么，b不会等于4，还是等于3。在编译器内部，遇到a=4；时，它就会重新搜索栈中是否有4的字面值，如果没有，重新开辟地址存放4的值；如果已经有了，则直接将a指向这个地址。因此a值的改变不会影响到b的值。
  
另一种是包装类数据，如Integer, String, Double等将相应的基本数据类型包装起来的类。这些类数据全部存在于堆中，Java用new()语句来显示地告诉编译器，在运行时才根据需要动态创建，因此比较灵活，但缺点是要占用更多的时间。
  
4.每个JVM的线程都有自己的私有的栈空间，随线程创建而创建，java的stack存放的是frames ，java的stack和c的不同，只是存放本地变量，返回值和调用方法，不允许直接push和pop frames ，因为frames 可能是有heap分配的，所以j为ava的stack分配的内存不需要是连续的。java的heap是所有线程共享的，堆存放所有 runtime data ，里面是所有的对象实例和数组，heap是JVM启动时创建。
  
5. String是一个特殊的包装类数据。即可以用String str = new String("abc");的形式来创建，也可以用String str = "abc"；的形式来创建(作为对比，在JDK 5.0之前，你从未见过Integer i = 3;的表达式，因为类与字面值是不能通用的，除了String。而在JDK 5.0中，这种表达式是可以的！因为编译器在后台进行Integer i = new Integer(3)的转换)。前者是规范的类的创建过程，即在Java中，一切都是对象，而对象是类的实例，全部通过new()的形式来创建。Java 中的有些类，如DateFormat类，可以通过该类的getInstance()方法来返回一个新创建的类，似乎违反了此原则。其实不然。该类运用了单例模式来返回类的实例，只不过这个实例是在该类内部通过new()来创建的，而getInstance()向外部隐藏了此细节。那为什么在String str = "abc"；中，并没有通过new()来创建实例，是不是违反了上述原则？其实没有。
  
5. 关于String str = "abc"的内部工作。Java内部将此语句转化为以下几个步骤: 
  
(1)先定义一个名为str的对String类的对象引用变量: String str；
  
(2)在栈中查找有没有存放值为"abc"的地址，如果没有，则开辟一个存放字面值为"abc"的地址，接着创建一个新的String类的对象o，并将o 的字符串值指向这个地址，而且在栈中这个地址旁边记下这个引用的对象o。如果已经有了值为"abc"的地址，则查找对象o，并返回o的地址。
  
(3)将str指向对象o的地址。
  
值得注意的是，一般String类中字符串值都是直接存值的。但像String str = "abc"；这种场合下，其字符串值却是保存了一个指向存在栈中数据的引用！
  
为了更好地说明这个问题，我们可以通过以下的几个代码进行验证。
  
String str1 = "abc";
  
String str2 = "abc";
  
System.out.println(str1==str2); //true
  
注意，我们这里并不用str1.equals(str2)；的方式，因为这将比较两个字符串的值是否相等。==号，根据JDK的说明，只有在两个引用都指向了同一个对象时才返回真值。而我们在这里要看的是，str1与str2是否都指向了同一个对象。
  
结果说明，JVM创建了两个引用str1和str2，但只创建了一个对象，而且两个引用都指向了这个对象。
  
我们再来更进一步，将以上代码改成: 
  
String str1 = "abc";
  
String str2 = "abc";
  
str1 = "bcd";
  
System.out.println(str1 + "," + str2); //bcd, abc
  
System.out.println(str1==str2); //false
  
这就是说，赋值的变化导致了类对象引用的变化，str1指向了另外一个新对象！而str2仍旧指向原来的对象。上例中，当我们将str1的值改为"bcd"时，JVM发现在栈中没有存放该值的地址，便开辟了这个地址，并创建了一个新的对象，其字符串的值指向这个地址。
  
事实上，String类被设计成为不可改变(immutable)的类。如果你要改变其值，可以，但JVM在运行时根据新值悄悄创建了一个新对象，然后将这个对象的地址返回给原来类的引用。这个创建过程虽说是完全自动进行的，但它毕竟占用了更多的时间。在对时间要求比较敏感的环境中，会带有一定的不良影响。
  
再修改原来代码: 
  
String str1 = "abc";
  
String str2 = "abc";
  
str1 = "bcd";
  
String str3 = str1;
  
System.out.println(str3); //bcd
  
String str4 = "bcd";
  
System.out.println(str1 == str4); //true
  
str3 这个对象的引用直接指向str1所指向的对象(注意，str3并没有创建新对象)。当str1改完其值后，再创建一个String的引用str4，并指向因str1修改值而创建的新的对象。可以发现，这回str4也没有创建新的对象，从而再次实现栈中数据的共享。
  
我们再接着看以下的代码。
  
String str1 = new String("abc");
  
String str2 = "abc";
  
System.out.println(str1==str2); //false
  
创建了两个引用。创建了两个对象。两个引用分别指向不同的两个对象。
  
String str1 = "abc";
  
String str2 = new String("abc");
  
System.out.println(str1==str2); //false
  
创建了两个引用。创建了两个对象。两个引用分别指向不同的两个对象。
  
以上两段代码说明，只要是用new()来新建对象的，都会在堆中创建，而且其字符串是单独存值的，即使与栈中的数据相同，也不会与栈中的数据共享。
  
6. 数据类型包装类的值不可修改。不仅仅是String类的值不可修改，所有的数据类型包装类都不能更改其内部的值。
  
7. 结论与建议: 
  
(1)我们在使用诸如String str = "abc"；的格式定义类时，总是想当然地认为，我们创建了String类的对象str。担心陷阱！对象可能并没有被创建！唯一可以肯定的是，指向 String类的引用被创建了。至于这个引用到底是否指向了一个新的对象，必须根据上下文来考虑，除非你通过new()方法来显要地创建一个新的对象。因此，更为准确的说法是，我们创建了一个指向String类的对象的引用变量str，这个对象引用变量指向了某个值为"abc"的String类。清醒地认识到这一点对排除程序中难以发现的bug是很有帮助的。
  
(2)使用String str = "abc"；的方式，可以在一定程度上提高程序的运行速度，因为JVM会自动根据栈中数据的实际情况来决定是否有必要创建新对象。而对于String str = new String("abc")；的代码，则一概在堆中创建新对象，而不管其字符串值是否相等，是否有必要创建新对象，从而加重了程序的负担。这个思想应该是享元模式的思想，但JDK的内部在这里实现是否应用了这个模式，不得而知。
  
(3)当比较包装类里面的数值是否相等时，用equals()方法；当测试两个包装类的引用是否指向同一个对象时，用==。
  
(4)由于String类的immutable性质，当String变量需要经常变换其值时，应该考虑使用StringBuffer类，以提高程序效率。
  
如果java不能成功分配heap的空间，将抛出OutOfMemoryError

---

http://android.blog.51cto.com/268543/50100
  
http://www.cnblogs.com/kkcheng/archive/2011/02/25/1964521.html

作者: 毛海山
  
链接: https://www.zhihu.com/question/49044988/answer/113961406
  
来源: 知乎
  
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
