---
title: "中断, interrupts"
author: "-"
date: ""
url: ""
categories:
  - inbox
tags:
  - inbox
---
## "中断, interrupts"

- IRQ: Interrupt ReQuest, 中断请求
- IDT，Interrupt Descriptor Table，中断描述符表

### 中断/interrupts

中断指当出现需要时，CPU暂时停止当前程序的执行转而执行处理新情况的程序和执行过程。即在程序运行过程中，系统出现了一个必须由CPU立即处理的情况，此时，CPU暂时中止程序的执行转而处理这个新的情况的过程就叫做中断。

### 为什么需要中断

如果让内核定期对设备进行轮询，以便处理设备请求，那会做很多无用功，因为外设的处理速度一般慢于CPU，而CPU不能一直等待外部事件。所以能让设备在需要内核时主动通知内核，会是一个聪明的方式，这便是中断。

[https://blog.csdn.net/oathevil/article/details/6007655](https://blog.csdn.net/oathevil/article/details/6007655)

### 中断分类

1. 外中断
由 CPU 执行指令以外的事件引起，如 I/O 完成中断，表示设备输入/输出处理已经完成，处理器能够发送下一个输入/输出请求。此外还有时钟中断、控制台中断等。

1. 异常
由 CPU 执行指令的内部事件引起，如非法操作码、地址越界、算术溢出等。

1. 陷入
在用户程序中使用系统调用

#### 中断是什么

中断的汉语解释是半中间发生阻隔、停顿或故障而断开。那么，在计算机系统中，我们为什么需要"阻隔、停顿和断开"呢？

举个日常生活中的例子，比如说我正在厨房用煤气烧一壶水，这样就只能守在厨房里，苦苦等着水开——如果水溢出来浇灭了煤气，有可能就要发生一场灾难了。等啊等啊，外边突然传来了惊奇的叫声"怎么不关水龙头？"于是我惭愧的发现，刚才接水之后只顾着抱怨这份无聊的差事，居然忘了这事，于是慌慌张张的冲向水管，三下两下关了龙头，声音又传到耳边，"怎么干什么都是这么马虎？"。伸伸舌头，这件小事就这么过去了，我落寞的眼神又落在了水壶上。

门外忽然又传来了铿锵有力的歌声，我最喜欢的古装剧要开演了，真想夺门而出，然而，听着水壶发出"咕嘟咕嘟"的声音，我清楚: 除非等到水开，否则没有我享受人生的时候。

这个场景跟中断有什么关系呢？

如果说我专心致志等待水开是一个过程的话，那么叫声、电视里传出的音乐不都让这个过程"半中间发生阻隔、停顿或故障而断开"了吗？这不就是活生生的"中断"吗？

在这个场景中，我是唯一具有处理能力的主体，不管是烧水、关水龙头还是看电视，同一个时间点上我只能干一件事情。但是，在我专心致志干一件事情时，总有许多或紧迫或不紧迫的事情突然出现在面前，都需要去关注，有些还需要我停下手头的工作马上去处理。只有在处理完之后，方能回头完成先前的任务，"把一壶水彻底烧开！"

中断机制不仅赋予了我处理意外情况的能力，如果我能充分发挥这个机制的妙用，就可以"同时"完成多个任务了。回到烧水的例子，实际上，无论我在不在厨房，煤气灶总是会把水烧开的，我要做的，只不过是及时关掉煤气灶而已，为了这么一个一秒钟就能完成的动作，却让我死死地守候在厨房里，在10分钟的时间里不停地看壶嘴是不是冒蒸气，怎么说都不划算。我决定安下心来看电视。当然，在有生之年，我都不希望让厨房成为火海，于是我上了闹钟，10分钟以后它会发出"尖叫"，提醒我炉子上的水烧开了，那时我再去关煤气也完全来得及。我用一个中断信号——闹铃——换来了10分钟的欢乐时光，心里不禁由衷地感叹: 中断机制真是个好东西。

正是由于中断机制，我才能有条不紊地"同时"完成多个任务，中断机制实质上帮助我提高了并发"处理"能力。它也能给计算机系统带来同样的好处: 如果在键盘按下的时候会得到一个中断信号，CPU就不必死守着等待键盘输入了；如果硬盘读写完成后发送一个中断信号，CPU就可以腾出手来集中精力"服务大众"了——无论是人类敲打键盘的指尖还是来回读写介质的磁头，跟CPU的处理速度相比，都太慢了。没有中断机制，就像我们苦守厨房一样，计算机谈不上有什么并行处理能力。

跟人相似，CPU也一样要面对纷繁芜杂的局面——现实中的意外是无处不在的——有可能是用户等得不耐烦，猛敲键盘；有可能是运算中碰到了0除数；还有可能网卡突然接收到了一个新的数据包。这些都需要CPU具体情况具体分析，要么马上处理，要么暂缓响应，要么置之不理。无论如何应对，都需要CPU暂停"手头"的工作，拿出一种对策，只有在响应之后，方能回头完成先前的使命，"把一壶水彻底烧开！"

先让我们感受一下中断机制对并发处理带来的帮助。

让我们用程序来探讨一下烧水问题，如果没有"中断" (注意，我们这里只是模仿中断的场景，实际上是用异步事件——消息——处理机制来展示中断产生的效果。毕竟，在用户空间没有办法与实际中断产生直接联系，不过操作系统为用户空间提供的异步事件机制，可以看作是模仿中断的产物) ，设计如下:  

    void StayInKitchen() 
    { 
    bool WaterIsBoiled = false; 
    while ( WaterIsBoiled != true ) 
    { 
    bool VaporGavenOff = false; 
    if (VaporGavenOff ) 
    WaterIsBoiled = true; 
    else 
    WaterIsBoiled = false; 
    } 

    // 关煤气炉 
    printf("Close gas oven./n"); 

    // 一切安定下来，终于可以看电视了，10分钟的宝贵时间啊，逝者如斯夫… 
    watching_tv(); 
    return; 
    } 

可以看出，整个流程如同我们前面描述的一样，所有工作要顺序执行，没有办法完成并发任务。

如果用"中断"，在开始烧水的时候设定一个10分钟的"闹铃"，然后让CPU去看电视 (有点难度，具体实现不在我们关心的范围之内，留给读者自行解决吧: >) 。等闹钟响的时候再去厨房关炉子。

＃i nclude
＃i nclude
＃i nclude
＃i nclude
＃i nclude

// 闹钟到时会执行此程序

void sig_alarm(int signo)

{

//关煤气炉

printf("Close gas oven./n");

}

void watching_tv()

{

while(1)

{

// 呵呵，悠哉悠哉

}

}

int main()

{

// 点火后设置定时中断

printf("Start to boil water, set Alarm");

if (signal( SIGALRM, sig_alrm ) == SIG_ERR)

{

perror("signal(SIGALRM) error");

return -1;

}

// 然后就可以欣赏电视节目了

printf("Watching TV!/n");

watching_tv();

return 0;

}

这两段程序都在用户空间执行。第二段程序跟中断也没有太大的关系，实际上它只用了信号机制而已。但是，通过这两个程序的对比，我们可以清楚地看到异步事件的处理机制是如何提升并发处理能力的。

Alarm定时器: alarm相当于系统中的一个定时器，如果我们调用alarm(5)，那么5秒钟后就会"响起一个闹铃" (实际上靠信号机制实现的，我们这里不想深入细节，如果你对此很感兴趣，请参考Richard Stevens不朽著作《Unix环境高级编程》) 。在闹铃响起的时候会发生什么呢?系统会执行一个函数，至于到底是什么函数，系统允许程序自行决定。程序员编写一个函数，并调用signal对该函数进行注册，这样一旦定时到来，系统就会调用程序员提供的函数 (CallBack函数？没错，不过在这里如何实现并不关键，我们就不引入新的概念和细节了) 。上面的例子里我们提供的函数是sig_alarm，所做的工作很简单，打印"关闭煤气灶"消息。

上面的两个例子很简单，但很能说明问题，首先，它证明采用异步的消息处理机制可以提高系统的并发处理能力。更重要的是，它揭示了这种处理机制的模式。用户根据需要设计处理程序，并可以将该程序和特定的外部事件绑定起来，在外部事件发生时系统自动调用处理程序，完成相关工作。这种模式给系统带来了统一的管理方法，也带来无尽的功能扩展空间。

计算机系统实现中断机制是非常复杂的一件工作，再怎么说人都是高度智能化的生物，而计算机作为一个铁疙瘩，没有程序的教导就一事无成。而处理一个中断过程，它受到的限制和需要学习的东西太多了。

首先，计算机能够接收的外部信号形式非常有限。中断是由外部的输入引起的，可以说是一种刺激。在烧水的场景中，这些输入是叫声和电视的音乐，我们这里只以声音为例。其实现实世界中能输入人类CPU——大脑的信号很多，图像、气味一样能被我们接受，人的信息接口很完善。而计算机则不然，接受外部信号的途径越多，设计实现就越复杂，代价就越高。因此个人计算机 (PC) 给所有的外部刺激只留了一种输入方式——特定格式的电信号，并对这种信号的格式、接入方法、响应方法、处理步骤都做了规约 (具体内容本文后面部分会继续详解) ，这种信号就是中断或中断信号，而这一整套机制就是中断机制。

其次，计算机不懂得如何应对信号。人类的大脑可以自行处理外部输入，我从来不用去担心闹钟响时会手足无措——走进厨房关煤气，这简直是天经地义的事情，还用大脑想啊，小腿肚子都知道——可惜计算机不行，没有程序，它就纹丝不动。因此，必须有机制保证外部中断信号到来后，有正确的程序在正确的时候被执行。

还有，计算机不懂得如何保持工作的持续性。我在看电视的时候如果去厨房关了煤气，回来以后能继续将电视进行到底，不受太大的影响。而计算机则不然，如果放下手头的工作直接去处理"意外"的中断，那么它就再也没有办法想起来曾经作过什么，做到什么程度了。自然也就没有什么"重操旧业"的机会了。这样的处理方式就不是并发执行，而是东一榔头，西一棒槌了。

那么，通用的计算机系统是如何解决这些问题的呢？它是靠硬件和软件配合来协同实现中断处理的全过程的。我们将通过Intel X86架构的实现来介绍这一过程。

CPU执行完一条指令后，下一条指令的逻辑地址存放在cs和eip这对寄存器中。在执行新指令前，控制单元会检查在执行前一条指令的过程中是否有中断或异常发生。如果有，控制单元就会抛下指令，进入下面的流程:  

1. 确定与中断或异常关联的向量i (0£i£255)
2. 寻找向量对应的处理程序
3. 保存当前的"工作现场"，执行中断或异常的处理程序
4. 处理程序执行完毕后，把控制权交还给控制单元
5. 控制单元恢复现场，返回继续执行原程序

#### 让我们深入这个流程，看看都有什么问题需要面对

1. 异常是什么概念？
在处理器执行到由于编程失误而导致的错误指令 (例如除数是0) 的时候，或者在执行期间出现特殊情况 (例如缺页) ，需要靠操作系统来处理的时候，处理器就会产生一个异常。对大部分处理器体系结构来说，处理异常和处理中断的方式基本是相同的，x86架构的CPU也是如此。异常与中断还是有些区别，异常的产生必须考虑与处理器时钟的同步。实际上，异常往往被称为同步中断。

2. 中断向量是什么？
中断向量代表的是中断源——从某种程度上讲，可以看作是中断或异常的类型。中断和异常的种类很多，比如说被0除是一种异常，缺页又是一种异常，网卡会产生中断，声卡也会产生中断，CPU如何区分它们呢？中断向量的概念就是由此引出的，其实它就是一个被送通往CPU数据线的一个整数。CPU给每个IRQ分配了一个类型号，通过这个整数CPU来识别不同类型的中断。这里可能很多朋友会寻问为什么还要弄个中断向量这么麻烦的东西？为什么不直接用IRQ0~IRQ15就完了？比如就让IRQ0为0，IRQ1为1……，这不是要简单得多么？其实这里体现了模块化设计规则，及节约规则。

首先我们先谈谈节约规则，所谓节约规则就是所使用的信号线数越少越好，这样如果每个IRQ都独立使用一根数据线，如IRQ0用0号线，IRQ1用1号线……这样，16个IRQ就会用16根线，这显然是一种浪费。那么也许马上就有朋友会说: 那么只用4根线不就行了吗？ (2^4=16) 。

这个问题，体现了模块设计规则。我们在前面就说过中断有很多类，可能是外部硬件触发，也可能是由软件触发，然而对于CPU来说中断就是中断，只有一种，CPU不用管它到底是由外部硬件触发的还是由运行的软件本身触发的，因为对于CPU来说，中断处理的过程都是一样的: 中断现行程序，转到中断服务程序处执行，回到被中断的程序继续执行。CPU总共可以处理256种中断，而并不知道，也不应当让CPU知道这是硬件来的中断还是软件来的中断，这样，就可以使CPU的设计独立于中断控制器的设计，这样CPU所需完成的工作就很单纯了。CPU对于其它的模块只提供了一种接口，这就是256个中断处理向量，也称为中断号。由这些中断控制器自行去使用这256个中断号中的一个与CPU进行交互，比如，硬件中断可以使用前128个号，软件中断使用后128个号，也可以软件中断使用前128个号，硬件中断使用后128个号，这与CPU完全无关了，当你需要处理的时候，只需告诉CPU你用的是哪个中断号就行，而不需告诉CPU你是来自哪儿的中断。这样也方便了以后的扩充，比如现在机器里又加了一片8259芯片，那么这个芯片就可以使用空闲的中断号，看哪一个空闲就使用哪一个，而不是必须要使用第0号，或第1号中断号了。其实这相当于一种映射机制，把IRQ信号映射到不同的中断号上，IRQ的排列或说编号是固定的，但通过改变映射机制，就可以让IRQ映射到不同的中断号，也可以说调用不同的中断服务程序。

3. 什么是中断服务程序？
在响应一个特定中断的时候，内核会执行一个函数，该函数叫做中断处理程序 (interrupt handler) 或中断服务程序 (interrupt service routine(ISR)) 。产生中断的每个设备都有相应的中断处理程序。例如，由一个函数专门处理来自系统时钟的中断，而另外一个函数专门处理由键盘产生的中断。

一般来说，中断服务程序要负责与硬件进行交互，告诉该设备中断已被接收。此外，还需要完成其他相关工作。比如说网络设备的中断服务程序除了要对硬件应答，还要把来自硬件的网络数据包拷贝到内存，对其进行处理后再交给合适的协议栈或应用程序。每个中断服务程序根据其要完成的任务，复杂程度各不相同。

一般来说，**一个设备的中断服务程序是它的设备驱动程序 (device driver) 的一部分** --- 设备驱动程序是用于对设备进行管理的内核代码。

4. 隔离变化

不知道您有没有意识到，中断处理前面这部分的设计是何等的简单优美。人是高度智能化的，能够对遇到的各种意外情况做有针对性的处理，计算机相比就差距甚远了，它只能根据预定的程序进行操作。对于计算机来说，硬件支持的，只能是中断这种电信号传播的方式和CPU对这种信号的接收方法，而具体如何处理这个中断，必须得靠操作系统实现。操作系统支持所有事先能够预料到的中断信号，理论上都不存在太大的挑战，但在操作系统安装到计算机设备上以后，肯定会时常有新的外围设备被加入系统，这可能会带来安装系统时根本无法预料的"意外"中断。如何支持这种扩展，是整个系统必须面对的。

而硬件和软件在这里的协作，给我们带来了完美的答案。当新的设备引入新类型的中断时，CPU和操作系统不用关注如何处理它。CPU只负责接收中断信号，并引用中断服务程序；而操作系统提供默认的中断服务——一般来说就是不理会这个信号，返回就可以了——并负责提供接口，让用户通过该接口注册根据设备具体功能而编制的中断服务程序。如果用户注册了对应于一个中断的服务程序，那么CPU就会在该中断到来时调用用户注册的服务程序。这样，在中断来临时系统需要如何操作硬件、如何实现硬件功能这部分工作就完全独立于CPU架构和操作系统的设计了。

而当你需要加入新设备的时候，只需要告诉操作系统该设备占用的中断号、按照操作系统要求的接口格式撰写中断服务程序，用操作系统提供的函数注册该服务程序，设备的中断就被系统支持了。

中断和对中断的处理被解除了耦合。这样，无论是你在需要加入新的中断时，还是在你需要改变现有中断的服务程序时、又或是取消对某个中断支持的时候，CPU架构和操作系统都无需作改变。

5. 保存当前工作"现场"
在中断处理完毕后，计算机一般来说还要回头处理原先手头正做的工作。这给中断的概念带来些额外的"内涵"。注一"回头"不是指从头再来重新做，而是要接着刚才的进度继续做。这就需要在处理中断信号之前保留工作"现场"。"现场"这个词比较晦涩，其实就是指一个信息集，它能反映某个时间点上任务的状态，并能保证按照这些信息就能恢复任务到该状态，继续执行下去。再直白一点，现场不过就是一组寄存器值。而如何保护现场和恢复场景是中断机制需要考虑的重点之一。

#### 每个中断处理都要经历这个保存和恢复过程，我们可以抽象出其中的步骤  

1. 保存现场
2. 执行具体的中断服务程序
3. 从中断服务返回
4. 恢复现场

上面说过了，"现场"看似在不断变化，没有哪个瞬间相同。但实际上组成现场的要素却不会有任何改变。也就是说，只要我们保存了相关的寄存器状态，现场就能保存下来。而恢复"现场"就是重新载入这些寄存器。换句话说，对于任何一个中断，保护现场和恢复现场所做的都是完全相同的操作。

既然操作相同，实现操作的过程和代码就相同。减少代码的冗余是模块化设计的基本准则，实在没有道理让所有的中断服务程序都重复实现这样的功能，应该将它作为一种基本的结构由底层的操作系统或硬件完成。而对中断的处理过程需要迅速完成，因此，Intel CPU的控制器就承担了这个任务，非但如此，上面的所有步骤次序都被固化下来，由控制器驱动完成。保存现场和恢复现场都由硬件自动完成，大大减轻了操作系统和设备驱动程序的负担。

6. 硬件对中断支持的细节
下面的部分，本来应该介绍8259、中断控制器编程、中断描述符表等内容，可是我看到了潇寒写的"保护模式下的8259A芯片编程及中断处理探究" (见参考资料1) ，前人之述备矣，读者直接读它好了。
从外而内，Linux对中断的支持

在Linux中，中断处理程序看起来就是普普通通的**C函数**。只不过这些函数必须按照特定的类型声明，以便内核能够以标准的方式传递处理程序的信息，在其他方面，它们与一般的函数看起来别无二致。中断处理程序与其它内核函数的真正区别在于，**中断处理程序是被内核调用来响应中断的**，而它们运行于我们称之为中断上下文的特殊上下文中。关于中断上下文，我们将在后面讨论。

中断可能随时发生，因此中断处理程序也就随时可能执行。所以必须保证中断处理程序能够快速执行，这样才能保证尽可能快地恢复被中断代码的执行。因此，尽管对硬件而言，迅速对其中断进行服务非常重要。但对系统的其它部分而言，让中断处理程序在尽可能短的时间内完成执行也同样重要。

即使最精简版的中断服务程序，它也要与硬件进行交互，告诉该设备中断已被接收。但通常我们不能像这样给中断服务程序随意减负，相反，我们要靠它完成大量的其它工作。作为一个例子，我们可以考虑一下网络设备的中断处理程序面临的挑战。该处理程序除了要对硬件应答，还要把来自硬件的网络数据包拷贝到内存，对其进行处理后再交给合适的协议栈或应用程序。显而易见，这种运动量不会太小。

#### 现在我们来分析一下Linux操作系统为了支持中断机制，具体都需要做些什么工作

首先，操作系统必须保证新的中断能够被支持。计算机系统硬件留给外设的是一个统一的中断信号接口。它固化了中断信号的接入和传递方法，拿PC机来说，中断机制是靠两块8259和CPU协作实现的。外设要做的只是把中断信号发送到8259的某个特定引脚上，这样8259就会为此中断分配一个标识——也就是通常所说的中断向量，通过中断向量，CPU就能够在以中断向量为索引的表 --- 中断向量表, 里找到中断服务程序，由它决定具体如何处理中断。 (具体细节还请查阅参考资料1，对于为何采用这种机制，该资料有精彩描述) 这是硬件规定的机制，软件只能无条件服从。

因此，操作系统对新中断的支持，说简单点，就是维护中断向量表。新的外围设备加入系统，首先得明确自己的中断向量号是多少，还得提供自身中断的服务程序，然后利用Linux的内核调用接口，把〈中断向量号、中断服务程序〉这对信息填写到中断向量表中去。这样CPU在接收到中断信号时就会自动调用中断服务程序了。这种注册操作一般是由设备驱动程序完成的。

其次，操作系统必须提供给程序员简单可靠的编程接口来支持中断。中断的基本流程前面已经讲了，它会打断当前正在进行的工作去执行中断服务程序，然后再回到先前的任务继续执行。这中间有大量需要解决问题: 如何保护现场、嵌套中断如何处理等等，操作系统要一一化解。程序员，即使是驱动程序的开发人员，在写中断服务程序的时候也很少需要对被打断的进程心存怜悯。 (当然，出于提高系统效率的考虑，编写驱动程序要比编写用户级程序多一些条条框框，谁让我们顶着系统程序员的光环呢？)  

操作系统为我们屏蔽了这些与中断相关硬件机制打交道的细节，提供了一套精简的接口，让我们用极为简单的方式实现对实际中断的支持，Linux是怎么完美的做到这一点的呢？

### CPU对中断处理的流程  

我们首先必须了解CPU在接收到中断信号时会做什么。没办法，操作系统必须了解硬件的机制，不配合硬件就寸步难行。现在我们假定内核已被初始化，CPU在保护模式下运行。

CPU执行完一条指令后，下一条指令的逻辑地址存放在cs和eip这对寄存器中。在执行新指令前，控制单元会检查在执行前一条指令的过程中是否有中断或异常发生。如果有，控制单元就会抛下指令，进入下面的流程:  

1. 确定与中断或异常关联的向量i (0£i£255)。
2. 籍由idtr寄存器从IDT表中读取第i项 (在下面的描述中，我们假定该IDT表项中包含的是一个中断门或一个陷阱门) 。
3. 从gdtr寄存器获得GDT的基地址，并在GDT表中查找，以读取IDT表项中的选择符所标识的段描述符。这个描述符指定中断或异常处理程序所在段的基地址。
4. 确信中断是由授权的 (中断) 发生源发出的。首先将当前特权级CPL (存放在cs寄存器的低两位) 与段描述符 (即DPL，存放在GDT中) 的描述符特权级比较，如果CPL小于DPL，就产生一个"通用保护"异常，因为中断处理程序的特权不能低于引起中断的程序的特权。对于编程异常，则做进一步的安全检查: 比较CPL与处于IDT中的门描述符的DPL，如果DPL小于CPL，就产生一个"通用保护"异常。这最后一个检查可以避免用户应用程序访问特殊的陷阱门或中断门。
5. 查是否发生了特权级的变化，也就是说， CPL是否不同于所选择的段描述符的DPL。如果是，控制单元必须开始使用与新的特权级相关的栈。通过执行以下步骤来做到这点:  
a. 读tr寄存器，以访问运行进程的TSS段。

b.用与新特权级相关的栈段和栈指针的正确值装载ss和esp寄存器。这些值可以在TSS中找到 (参见第三章的"任务状态段"一节) 。

c.在新的栈中保存ss和esp以前的值，这些值定义了与旧特权级相关的栈的逻辑地址。

6. 如果故障已发生，用引起异常的指令地址装载cs和eip寄存器，从而使得这条指令能再次被执行。

7.在栈中保存eflag、cs及eip的内容。

8.如果异常产生了一个硬错误码，则将它保存在栈中。

9.装载cs和eip寄存器，其值分别是IDT表中第i项门描述符的段选择符和偏移量域。这些值给出了中断或者异常处理程序的第一条指令的逻辑地址。

控制单元所执行的最后一步就是跳转到中断或者异常处理程序。换句话说，处理完中断信号后，控制单元所执行的指令就是被选中的处理程序的第一条指令。

中断或异常被处理完后，相应的处理程序必须产生一条iret指令，把控制权转交给被中断的进程，这将迫使控制单元:  

1.用保存在栈中的值装载cs、eip、或eflag寄存器。如果一个硬错误码曾被压入栈中，并且在eip内容的上面，那么，执行iret指令前必须先弹出这个硬错误码。

2.检查处理程序的CPL是否等于cs中最低两位的值 (这意味着被中断的进程与处理程序运行在同一特权级) 。如果是，iret终止执行；否则，转入下一步。

3. 从栈中装载ss和esp寄存器，因此，返回到与旧特权级相关的栈。

4. 检查ds、es、fs及gs段寄存器的内容，如果其中一个寄存器包含的选择符是一个段描述符，并且其DPL值小于CPL，那么，清相应的段寄存器。控制单元这么做是为了禁止用户态的程序 (CPL=3) 利用内核以前所用的段寄存器 (DPL=0) 。如果不清这些寄存器，怀有恶意的用户程序就可能利用它们来访问内核地址空间。

### 再次，操作系统必须保证中断信息能够高效可靠的传递

注一: 那么PowerOff (关机) 算不算中断呢？如果从字面上讲，肯定符合汉语对中断的定义，但是从信号格式、处理方法等方面来看，就很难符合我们的理解了。Intel怎么说的呢？该中断没有采用通用的中断处理机制。那么到底是不是中断呢？我也说不上来:  (

注二: 更详细的内容和其它一些注意事项请参考内核源代码包中Documentations/rtc.txt

注三: 之所以这里使用汇编而不是 C 来实现这些函数，是因为C编译器会在函数的实现中推入额外的栈信息。而 CPU 在中断来临时保存和恢复现场都按照严格的格式进行，一个字节的变化都不能有。

参考资料

1 "保护模式下的8259A芯片编程及中断处理探究" 潇寒 哈工大纯C论坛 [http://purec.binghua.com/Article/ShowArticle.asp?ArticleID=91](http://purec.binghua.com/Article/ShowArticle.asp?ArticleID=91)

2 "80x86 IBM PC及兼容计算机 (卷I和卷II): 汇编语言、设计与接口技术" Muhammad Ali Mazidi等著 张波等译 清华大学出版社

3 "编写操作系统之键盘交互的实现" 潇寒 哈工大纯C论坛 [http://purec.binghua.com/Article/ShowArticle.asp?ArticleID=104](http://purec.binghua.com/Article/ShowArticle.asp?ArticleID=104)

### 中断处理程序

在响应一个特定中断时，内核会执行一个函数 --- 中断处理程序。中断处理程序与其他内核函数的区别在于，中断处理程序是被内核调用来响应中断的，而它们运行于我们称之为中断上下文的特殊上下文中。

中断处理程序就是普通的C代码。特别之处在于中断处理程序是在中断上下文中运行的,它的行为受到某些限制:

1. 不能向用户空间发送或接受数据
2. 不能使用可能引起阻塞的函数
3. 不能使用可能引起调度的函数

### 上下半部机制

我们期望让中断处理程序运行得快，并想让它完成的工作量多，这两个目标相互制约，如何解决——上下半部机制。

我们把中断处理切为两半。中断处理程序是上半部 --- 接受中断，他就立即开始执行，但只有做严格时限的工作。能够被允许稍后完成的工作会推迟到下半部去，此后，在合适的时机，下半部会被开终端执行。上半部简单快速，执行时禁止一些或者全部中断。下半部稍后执行，而且执行期间可以响应所有的中断。这种设计可以使系统处于中断屏蔽状态的时间尽可能的短，以此来提高系统的响应能力。上半部只有中断处理程序机制，而下半部的实现有软中断实现，tasklet实现和工作队列实现。

我们用网卡来解释一下这两半。当网卡接受到数据包时，通知内核，触发中断，所谓的上半部就是，及时读取数据包到内存，防止因为延迟导致丢失，这是很急迫的工作。读到内存后，对这些数据的处理不再紧迫，此时内核可以去执行中断前运行的程序，而对网络数据包的处理则交给下半部处理。

### 上下半部划分原则

1. 如果一个任务对时间非常敏感，将其放在中断处理程序中执行；
2. 如果一个任务和硬件有关，将其放在中断处理程序中执行；
3. 如果一个任务要保证不被其他中断打断，将其放在中断处理程序中执行；
4. 其他所有任务，考虑放置在下半部执行。

### 下半部实现机制之软中断

软中断作为下半部机制的代表，是随着SMP (share memoryprocessor) 的出现应运而生的，它也是tasklet实现的基础 (tasklet实际上只是在软中断的基础上添加了一定的机制) 。软中断一般是"可延迟函数"的总称，有时候也包括了tasklet (请读者在遇到的时候根据上下文推断是否包含tasklet) 。它的出现就是因为要满足上面所提出的上半部和下半部的区别，使得对时间不敏感的任务延后执行，软中断执行中断处理程序留给它去完成的剩余任务，而且可以在多个CPU上并行执行，使得总的系统效率可以更高。它的特性包括:

a) 产生后并不是马上可以执行，必须要等待内核的调度才能执行。软中断不能被自己打断，只能被硬件中断打断 (上半部) 。

b) 可以并发运行在多个CPU上 (即使同一类型的也可以) 。所以软中断必须设计为可重入的函数 (允许多个CPU同时操作) ，因此也需要使用自旋锁来保护其数据结构。

### 下半部实现机制之tasklet

tasklet是通过软中断实现的，所以它本身也是软中断。

软中断用轮询的方式处理。假如正好是最后一种中断，则必须循环完所有的中断类型，才能最终执行对应的处理函数。显然当年开发人员为了保证轮询的效率，于是限制中断个数为32个。

为了提高中断处理数量，顺道改进处理效率，于是产生了tasklet机制。

Tasklet采用无差别的队列机制，有中断时才执行，免去了循环查表之苦。Tasklet作为一种新机制，显然可以承担更多的优点。正好这时候SMP越来越火了，因此又在tasklet中加入了SMP机制，保证同种中断只能在一个cpu上执行。在软中断时代，显然没有这种考虑。因此同一种软中断可以在两个cpu上同时执行，很可能造成冲突。

总结下tasklet的优点:

 (1) 无类型数量限制；

 (2) 效率高，无需循环查表；

 (3) 支持SMP机制；

它的特性如下:

1) 一种特定类型的tasklet只能运行在一个CPU上，不能并行，只能串行执行。

2) 多个不同类型的tasklet可以并行在多个CPU上。

3) 软中断是静态分配的，在内核编译好之后，就不能改变。但tasklet就灵活许多，可以在运行时改变 (比如添加模块时) 。

### 下半部实现机制之工作队列 (work queue)

上面我们介绍的可延迟函数运行在中断上下文中 (软中断的一个检查点就是do_IRQ退出的时候) ，于是导致了一些问题: 软中断不能睡眠、不能阻塞。由于中断上下文出于内核态，没有进程切换，所以如果软中断一旦睡眠或者阻塞，将无法退出这种状态，导致内核会整个僵死。但可阻塞函数不能用在中断上下文中实现，必须要运行在进程上下文中，例如访问磁盘数据块的函数。因此，可阻塞函数不能用软中断来实现。但是它们往往又具有可延迟的特性。

上面我们介绍的可延迟函数运行在中断上下文中，于是导致了一些问题，说明它们不可挂起，也就是说软中断不能睡眠、不能阻塞，原因是由于中断上下文出于内核态，没有进程切换，所以如果软中断一旦睡眠或者阻塞，将无法退出这种状态，导致内核会整个僵死。因此，可阻塞函数不能用软中断来实现。但是它们往往又具有可延迟的特性。而且由于是串行执行，因此只要有一个处理时间较长，则会导致其他中断响应的延迟。为了完成这些不可能完成的任务，于是出现了工作队列，它能够在不同的进程间切换，以完成不同的工作。

如果推后执行的任务需要睡眠，那么就选择工作队列，如果不需要睡眠，那么就选择软中断或tasklet。工作队列能运行在进程上下文，它将工作托付给一个内核线程。工作队列说白了就是一组内核线程，作为中断守护线程来使用。多个中断可以放在一个线程中，也可以每个中断分配一个线程。我们用结构体workqueue_struct表示工作者线程，工作者线程是用内核线程实现的。而工作者线程是如何执行被推后的工作——有这样一个链表，它由结构体work_struct组成，而这个work_struct则描述了一个工作，一旦这个工作被执行完，相应的work_struct对象就从链表上移去，当链表上不再有对象时，工作者线程就会继续休眠。因为工作队列是线程，所以我们可以使用所有可以在线程中使用的方法。

### Linux 软中断和工作队列的作用是什么

Linux中的软中断和工作队列是中断上下部机制中的下半部实现机制。

1. 软中断一般是"可延迟函数"的总称，它不能睡眠，不能阻塞，它处于中断上下文，不能进程切换，软中断不能被自己打断，只能被硬件中断打断 (上半部) ，可以并发的运行在多个CPU上。所以软中断必须设计成可重入的函数，因此也需要自旋锁来保护其数据结构。
2. 工作队列中的函数处在进程上下文中，它可以睡眠，也能被阻塞，能够在不同的进程间切换，以完成不同的工作。

可延迟函数和工作队列都不能访问用户的进程空间，可延时函数在执行时不可能有任何正在运行的进程，工作队列的函数有内核线程执行，他不能访问用户空间地址。

### 硬件中断 hardirq

硬件中断是一个异步信号, 表明需要注意, 或需要改变在执行一个同步事件.
硬件中断是由与系统相连的外设(比如网卡 硬盘 键盘等)自动产生的. 每个设备或设备集都有他自己的IRQ(中断请求), 基于IRQ, CPU可以将相应的请求分发到相应的硬件驱动上(注: 硬件驱动通常是内核中的一个子程序, 而不是一个独立的进程). 比如当网卡受到一个数据包的时候, 就会发出一个中断.
处理中断的驱动是需要运行在CPU上的, 因此, 当中断产生时, CPU会暂时停止当前程序的程序转而执行中断请求. 一个中断只能中断一颗CPU(也有一种特殊情况, 就是在大型主机上是有硬件通道的, 它可以在没有主CPU的支持下, 同时处理多个中断).
硬件中断可以直接中断CPU. 它会引起内核中相关代码被触发. 对于那些需要花费时间去处理的进程, 中断代码本身也可以被其他的硬件中断中断.
对于时钟中断, 内核调度代码会将当前正在运行的代码挂起, 从而让其他代码来运行. 它的存在时为了让调度代码(或称为调度器)可以调度多任务.

### 软中断 softirq

软中断的处理类似于硬中断. 但是软中断仅仅由当前运行的进程产生.
通常软中断是对一些I/O的请求.
软中断仅与内核相联系, 而内核主要负责对需要运行的任何其他进程进行调度.
软中断不会直接中断CPU, 也只有当前正在运行的代码(或进程)才会产生软中断. 软中断是一种需要内核为正在运行的进程去做一些事情(通常为I/O)的请求.
有一个特殊的软中断是Yield调用, 它的作用是请求内核调度器去查看是否有一些其他的进程可以运行.
硬件中断和软中断的区别
硬件中断是由外设引发的, 软中断是执行中断指令产生的.
硬件中断的中断号是由中断控制器提供的, 软中断的中断号由指令直接指出, 无需使用中断控制器.
硬件中断是可屏蔽的, 软中断不可屏蔽.
硬件中断处理程序要确保它能快速地完成任务, 这样程序执行时才不会等待较长时间, 称为上半部.
软中断处理硬中断未完成的工作, 是一种推后执行的机制, 属于下半部.

### 保护模式下 8259A芯片编程及中断处理探究

保护模式下

8259A芯片编程及中断处理探究 (上)

Version 0.02

哈尔滨工业大学 并行计算实验室 谢煜波[1]

简介

中断处理是操作系统必须完成的任务，在IBM PC中，常用一块中断控制芯片 (PIC) ——8259A来辅助CPU完成中断管理。在实模式下，中断控制芯片 (PIC) 8259A的初始化是由BIOS自动完成的，然而在保护模式下却需要我们自行编程初始化。本篇拟从操作系统的编写角度详细描述下笔者在此方向上所做的摸索，并在最后通过pyos进行实验验证。此是这部份内容的上篇，将详细描述8259A芯片的编程部份，对于操作系统中的中断处理以及程序验证将在下篇里面详细描述。

此文只是我在进行操作系统实验过程中的一点心得体会，记下来，避免自己忘记。对于其中可能出现的错误，欢迎你来信指证。

一、中断概述

相信大家对于中断一点都不陌生，这里也不准备详细介绍中断的所有内容，只简单做下概要介绍，这样使对中断没有概念的朋友能建立起一点概念。

计算机除了CPU外，还有很多外围设备，然而我们都知道CPU的运行速度是很快的，而外围设备的运行速度却不是很快了。假设我们现在需要从磁盘上读入十个字节，而这需要10秒钟 (很夸张，但这只是一个例子) ，那么在这10秒钟之内，CPU就无所事事，不得不等待磁盘如蜗牛般的读入这十个字节，如果在这10秒钟之内，CPU转去运行其它的程序，不就可以防止浪费CPU的时间了吗？但是这就出现了一个问题，CPU怎么知道磁盘已经读完数据了呢？实际上，这时磁盘的控制器会向CPU发送一个信号，CPU收到信号之后，就知道磁盘已经读完数据了，于是它就中断正在运行的程序，重新回到原先等待磁盘输入的程序上来继续执行。这只是一个很简单的例子，也只是中断应用的一个很简单的方面，但基本上可以说明问题。可以这么认为: 中断就是外部设备或程序同CPU通信的一种方式。CPU在接收到中断信号时，会中断正在运行的程序，转到对中断的处理上，而这个对中断的处理程序常常称为中断服务程序，当中断服务程序处理完中断后，CPU再返回到原先被中断的程序上继续执行。整个过程如下图所示:

 (图1)

中断有很多类型，比如可屏蔽中断 (顾名思义，对此种中断，CPU可以不响应) 、不可屏蔽中断；软中断 (一般由运行中的程序触发) 、硬中断……等很多分类方法。中断可以完成的任务也很多，比如设备准备完毕、设备运行故障、程序运行故障……，这许多突发事件都可以以中断的方式通知CPU进行处理。

二、认识中断号及8259A芯片

我们都知道计算机可以挂接上许多外部设备，比如键盘、磁盘驱动器、鼠标、声卡……等等一系列设备，而这些设备都可能在同一时刻向CPU发出中断信号，那么CPU到底应当响应哪一个设备的中断信号呢？这都通过另外一个芯片来控制，在IBM PC机中，这个芯片常常被称作: 可编程中断控制器 (PIC) 8259A，说它可编程，是因为我们可以通过编程来改变它的功能。比如我可以通过编程设定CPU应当优先响应哪一个中断，屏蔽哪些中断等等一系列事件。

一个8259A芯片共有中断请求 (IRQ) 信号线: IRQ0~IRQ7，共8根。在PC机中，共有两片8259A芯片，通过把它们联结起来使用，就有IRQ0~IRQ15，共16根中断信号线，每个外部设备使用一根或多个外部设备共用一根中断信号线，它们通过IRQ发送中断请求，8259A芯片接到中断请求后就对中断进行优先级选定，然后对多个中断中具有最高优先级的中断进行处理，将其所对应的中断向量送上通往CPU的数据线，并通知CPU有中断到来。

这里出现了一个中断向量的概念，其实它就是一个被送往CPU数据线的一个整数。CPU给每个IRQ分配了一个类型号，通过这个整数，CPU来识别不同类型的中断。这里可能很多朋友会寻问为什么还要弄个中断向量这么麻烦的东西？为什么不直接用IRQ0~IRQ15就完了？比如就让IRQ0为0，IRQ1为1……，这不是要简单的多么？其实这里体现了模块化设计规则以及节约规则。

首先我们先谈谈节约规则，所谓节约规则就是所使用的信号线数越少越好，这样如果每个IRQ都独立使用一根数据线，如IRQ0用0号线，IRQ1用1号线……这样，16个IRQ就会用16根线，这显然是一种浪费。那么也许马上就有朋友会说: 那么只用4根线不就行了吗 (24=16) ？

对于这个问题，则体现了模块设计规则。我们在前面就说过中断有很多类，可能是外部硬件触发，也可能是由软件触发，然而对于CPU来说中断就是中断，只有一种，CPU不用管它到底是由外部硬件触发的还是由运行的软件本身触发的，因为对于CPU来说，中断处理的过程都是一样的: 中断现行程序，转到中断服务程序处执行，回到被中断的程序继续执行。CPU总共可以处理256种中断，而并不知道，也不应当让CPU知道这是硬件来的中断还是软件来的中断，这样，就可以使CPU的设计独立于中断控制器的设计，因为CPU所需完成的工作就很单纯了。CPU对于其它的模块只提供了一种接口，这就是256个中断处理向量，也称为中断号。由这些中断控制器自行去使用这256个中断号中的一个与CPU进行交互。比如，硬件中断可以使用前128个号，软件中断使用后128个号，也可以软件中断使用前128个号，硬件中断使用后128个号，这于CPU完全无关了，当你需要处理的时候，只需告诉CPU你用的是哪个中断号就行，而不需告诉CPU你是来自哪儿的中断。这样也方便了以后的扩充，比如现在机器里又加了一片8259芯片，那么这个芯片就可以使用空闲的中断号，看哪一个空闲就使用哪一个，而不是必须要使用第0号，或第1号中断。其实这相当于一种映射机制，把IRQ信号映射到不同的中断号上，IRQ的排列或说编号是固定的，但通过改变映射机制，就可以让IRQ映射到不同的中断号，也可以说调用不同的中断服务程序，因为中断号是与中断服务程序一一对应的，这一点我们将在随后的内容中详细描述。8259A将中断号通知CPU后，它的任务就完成了，至于CPU使用此中断号去调用什么程序它就不管了。下图就是8259A芯片的结构:

 (图2 来源《Linux 0.11 内核完全注释》)

上图就是PC机中两片8259A的联结及IRQ分配示意图。从图中我们可以看到，两片8259A芯片是级联工作的，一个为主片，一个为从片，从片的INT端口与主片的IRQ2相连。主片通过0x20及0x21两个端口访问，而从片通过0xA0及0xA1这两个端口访问。

至于为什么从片的INT需要与主片的IRQ2相连而不是与其它的IRQ相联，很遗憾，我目前无法回答这个问题: (，如果你知道答案，非常希望你能来信指教！不过幸运的是，我们只要知道计算机是的确是这样联的，并且这样连它就可以正常工作就行了！

### 8259A

可编程中断控制器
可编程中断控制器 (PIC - Programmable Interrupt Controller)是微机系统中管理设备中断请求的管理者。当PIC向处理器的INT引脚发出一个中断信号时，处理器会立刻停下当时所做的事情并询问PIC需要执行哪个中断服务请求。PIC则通过向数据总线发出与中断请求对应的中断号来告知处理器要执行哪个中断服务过程。处理器则根据读取的中断号通过查询中断向量表 (在32位保护模式下是中断描述符表) 取得相关设备的中断向量 (即中断服务程序的地址) 并开始执行中断服务程序。当中断服务程序执行结束，处理器就继续执行被中断信号打断的程序。

3.3 初始化 pyos 的中断向量表

从中断初始化的代码中我们可以清楚的看见，pyos在进行完8259A的初始化后，调用InitInterruptTable()对中断向量表进行了初始化，这可是本篇的核心内容，我们这就来看看这个核心函数:

/*中断描述符结构*/

struct struct_pyos_InterruptItem{

unsigned short Offset_0_15 ; // 偏移量的0~15位

unsigned short SegSelector ; // 段选择符

unsigned char UnUsed ; // 未使用，须设为全零

unsigned char Saved_1_1_0 : 3 ; // 保留，需设为 110

unsigned char D : 1 ; // D 位

unsigned char Saved_0 : 1 ; // 保留，需设为0

unsigned char DPL : 2 ; // 特权位

unsigned char P : 1 ; // P 位

unsigned short Offset_16_31 ; // 偏移量的16~31位

} ;

/*IDTR所用结构*/

struct struct_pyos_Idtr{

unsigned short IdtLengthLimit ;

struct_pyos_InterruptItem* IdtAddr ;

} ;

static struct_pyos_InterruptItem m_Idt[ 256 ] ; // 中断描述符表项

static struct_pyos_Idtr m_Idtr ; // 中断描述符寄存器所用对象

extern "C" void pyos_asm_interrupt_handle_for_default() ; // 默认中断处理函数

/*初始化中断向量表*/

void class_pyos_Interrupt::InitInterruptTable()

{

/*设置中断描述符，指向一个哑中断，在需要的时候再填写*/

struct_pyos_InterruptItem tmp ;

tmp.Offset_0_15 = ( unsigned int )pyos_asm_interrupt_handle_for_default ;

tmp.Offset_16_31 = ( unsigned int )pyos_asm_interrupt_handle_for_default >> 16 ;

tmp.SegSelector = 0x8 ; // 代码段

tmp.UnUsed = 0 ;

tmp.P = 1 ;

tmp.DPL = 0 ;

tmp.Saved_1_1_0 = 6 ;

tmp.Saved_0 = 0 ;

tmp.D = 1 ;

for( int i = 0 ; i < 256 ; ++i ){

m_Idt[ i ] = tmp ;

}

m_Idtr.IdtAddr = m_Idt ;

m_Idtr.IdtLengthLimit = 256 * 8 - 1 ; // 共 256项，每项占8个字节

// 内嵌汇编，载入 ldt

**asm**( "lidt %0" : "=m"( m_Idtr ) ) ; //载入GDT表

}

程序首先说明了两个结构，一个用来描述中断描述符，一个用来描述中断描述符寄存器。大家可以对照前面的描述看看这两个结构中的成员分别对应硬件系统中的哪一位。之后，程序建立了一个中断描述符数组m_Idt，它共有256项，这是因为CPU可以处理256个中断。程序还建立了一个中断描述符寄存器所用的对象。随后，程序开始为这些变量赋值。

从程序中我们可以看出，pyos现在是将每个中断描述符都设成一样的，均指向一个相同的中断处理程序: pyos_asm_interrupt_handle_for_default()，在一个实际的操作系统中，在最初初始化的时候，也常常是这样做的，这个被称之为"默认中断处理程序"的中断服务程序通常是一个什么也不干的"哑中断处理程序"或者是一个只是简单报错的处理程序。而要等到实际需要时，才使用相应的处理程序替换它。

程序在建立"中断描述符表"后，用lidt指令将中断描符述表寄存器所用的内容载入了中断描述符寄存器 (IDTR) 中，对于"中断描述符表"的初始化就完成了，下面我们可以来看看，pyos_asm_interrupt_handle_for_default()这个程序到底做了些什么事:

3.4 中断处理程序的编写

pyos_asm_interrupt_handle_for_default:

;保护现场

pushad

;调用相应的C++处理函数

call pyos_interrupt_handle_for_default

;告诉硬件中断处理完毕，即发送 EOI 消息

mov al , 0x20

out 0x20 , al

out 0xa0 , al

;恢复现场

popad

;返回

iret

这个程序是在一个名为"interrupt.asm"的汇编文件中，显然，它是一个汇编语言写的源程序。为什么这里又要用汇编语言编写而不直接用C++内嵌汇编编写呢，比如写成下面这样:

void pyos_asm_interrupt_handle_for_default()

{

**asm**( "pushad" ) ;

/*do something*/

**asm**( "popad" ) ;

**asm**( "iret" ) ;
}

### 中断向量表和中断描述符表IDT

CPU是根据中断号获取中断向量值，即对应中断服务程序的入口地址值。因此为了让CPU由中断号查找到对应的中断向量，就需要在内存中建立一张查询表，即中断向量表 (在32位保护模式下该表称为中断描述符表) 。80x86微机支持256个中断，对应每个中断需要安排一个中断服务程序。在80x86实模式运行方式下，每个中断向量由4字节组成。这4字节指明了一个中断服务程序的段值和段内偏移值。因此整个向量表的长度为1KB。当80x86微机启动时，ROM BIOS中的程序会在物理内存开始地址0x0000:0x0000处初始化并设置中断向量表，而各中断的默认中断服务程序则在BIOS中给出。由于中断向量表中的向量是按中断号顺序排列，因此给定一个中断号N，那么它对应的中断向量在内存中的位置就是0x0000:N*4，即对应的中断服务程序入口地址保存在物理内存0x0000:N*4位置处。

在BIOS执行初始化操作时，它设置了两个8259A芯片支持的16个硬件中断向量和BIOS提供的中断号为0x10～0x1f的中断调用功能向量等。对于实际没有使用的向量则填入临时的哑中断服务程序的地址。以后在系统引导加载操作系统时会根据实际需要修改某些中断向量的值。例如，对于DOS操作系统，它会重新设置中断0x20～0x2f的中断向量值。而对于Linux系统，除了在刚开始加载内核时需要用到BIOS提供的显示和磁盘读操作中断功能，在内核正常运行之前则会在setup.s程序中重新初始化8259A芯片并且在head.s程序中重新设置一张中断向量表 (中断描述符表) 。完全抛弃了BIOS所提供的中断服务功能。

当Intel CPU运行在32位保护模式下时，需要使用中断描述符表 (Interrupt Descriptor Table，IDT) 来管理中断或异常。IDT是Intel 8086～80186 CPU中使用的中断向量表的直接替代物。其作用也类似于中断向量表，只是其中每个中断描述符项中除了含有中断服务程序地址以外，还包含有关特权级和描述符类别等信息。Linux操作系统工作于80x86的保护模式下，因此它使用中断描述符表来设置和保存各中断的"向量"信息。

另外，保护模式下，关于IDT和GDT的位置。
       IDT表可以驻留在线性地址空间的任何地方，处理器使用IDTR寄存器来定位IDT表的位置。
       GDT可以被放在内存的任何位置，那么当程序员通过段寄存器来引用一个段描述符时，CPU必须知道GDT的入口，也就是基地址放在哪里，所以Intel的设计者门提供了一个寄存器GDTR用来存放GDT的入口地址，程序员将GDT设定在内存中某个位置之后，可以通过LGDT指令将GDT的入口地址装入此寄存器，从此以后，CPU就根据此寄存器中的内容作为GDT的入口来访问GDT了。

---

[https://blog.csdn.net/jwy2014/article/details/89221142](https://blog.csdn.net/jwy2014/article/details/89221142)  
[https://www.cnblogs.com/wuchanming/p/4756756.html](https://www.cnblogs.com/wuchanming/p/4756756.html)  
[https://blog.csdn.net/loafertb/article/details/8849603](https://blog.csdn.net/loafertb/article/details/8849603)
[https://www.geek-share.com/detail/2577873746.html](https://www.geek-share.com/detail/2577873746.html)  
[https://blog.csdn.net/qq_37232329/article/details/85331513](https://blog.csdn.net/qq_37232329/article/details/85331513)  
[https://blog.csdn.net/yxc135/article/details/8734452](https://blog.csdn.net/yxc135/article/details/8734452)  