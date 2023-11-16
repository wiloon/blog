---
title: Linux动态链接库.so文件
author: "-"
date: 2014-04-14T01:19:17+00:00
url: /?p=6535
categories:
  - Inbox
tags:
  - Linux

---
## Linux动态链接库.so文件

>[http://blog.csdn.net/ithomer/article/details/7346146](http://blog.csdn.net/ithomer/article/details/7346146)

**1. 介绍
  
**

使用GNU的工具我们如何在Linux下创建自己的程序函数库?一个"程序函数库"简单的说就是一个文件包含了一些编译好的代码和数据，这些编译好的代码和数据可以在事后供其他的程序使用。程序函数库可以使整个程序更加模块化，更容易重新编译，而且更方便升级。

程序函数库可分为3种类型: 静态函数库 (static libraries) 、共享函数库 (shared libraries) 、动态加载函数库 (dynamically loaded libraries) :

1. **静态函数库**，是在程序执行前就加入到目标程序中去了；

2. **共享函数库**，则是在程序启动的时候加载到程序中，它可以被不同的程序共享；动态加载函数库则可以在程序运行的任何时候动态的加载。

3. **动态函数库**，并非另外一种库函数格式，区别是动态加载函数库是如何被程序员使用的。

****

**2. 静态函数库
  
**

静态函数库实际上就是简单的一个普通的目标文件的集合，一般来说习惯用".a"作为文件的后缀。可以用ar这个程序来产生静态函数库文件。Ar是archiver的缩写。静态函数库现在已经不在像以前用得那么多了，主要是共享函数库与之相比较有很多的优势的原因。慢慢地，大家都喜欢使用共享函数库了。不过，在一些场所静态函数库仍然在使用，一来是保持一些与以前某些程序的兼容，二来它描述起来也比较简单。

静态库函数允许程序员把程序link起来而不用重新编译代码，节省了重新编译代码的时间。不过，在今天这么快速的计算机面前，一般的程序的重新编译也花费不了多少时间，所以这个优势已经不是像它以前那么明显了。静态函数库对开发者来说还是很有用的，例如你想把自己提供的函数给别人使用，但是又想对函数的源代码进行保密，你就可以给别人提供一个静态函数库文件。理论上说，使用ELF格式的静态库函数生成的代码可以比使用共享函数库 (或者动态函数库) 的程序运行速度上快一些，大概1－5％。

创建一个静态函数库文件，或者往一个已经存在地静态函数库文件添加新的目标代码，可以用下面的命令:

ar rcs my_library.a file1.o file2.o

这个例子中是把目标代码file1.o和file2.o加入到my_library.a这个函数库文件中，如果my_library.a不存在则创建一个新的文件。在用ar命令创建静态库函数的时候，还有其他一些可以选择的参数，可以参加ar的使用帮助。这里不再赘述。

一旦你创建了一个静态函数库，你可以使用它了。你可以把它作为你编译和连接过程中的一部分用来生成你的可执行代码。如果你用gcc来编译产生可执行代码的话，你可以用"-l"参数来指定这个库函数。你也可以用ld来做，使用它的"-l"和"-L"参数选项。具体用法可以参考info:gcc。

****

**3. 共享函数库
  
**

共享函数库中的函数是在当一个可执行程序在启动的时候被加载。如果一个共享函数库正常安装，所有的程序在重新运行的时候都可以自动加载最新的函数库中的函数。对于Linux系统还有更多可以实现的功能:
  
1. 升级了函数库但是仍然允许程序使用老版本的函数库。
  
2. 当执行某个特定程序的时候可以覆盖某个特定的库或者库中指定的函数。
  
3. 可以在库函数被使用的过程中修改这些函数库。

3.1. 一些约定
  
如果你要编写的共享函数库支持所有有用的特性，你在编写的过程中必须遵循一系列约定。你必须理解库的不同的名字间的区别，例如它的"soname"和"real name"之间的区别和它们是如何相互作用的。你同样还要知道你应该把这些库函数放在你文件系统的什么位置等等。下面我们具体看看这些问题。

3.1.1. 共享库的命名

每个共享函数库都有个特殊的名字，称作"soname"。soname名字命名必须以"lib"作为前缀，然后是函数库的名字，然后是".so"，最后是版本号信息。不过有个特例，就是非常底层的C库函数都不是以lib开头这样命名的。
  
每个共享函数库都有一个真正的名字 ("real name") ，它是包含真正库函数代码的文件。真名有一个主版本号，和一个发行版本号。最后一个发行版本号是可选的，可以没有。主版本号和发行版本号使你可以知道你到底是安装了什么版本的库函数。另外，还有一个名字是编译器编译的时候需要的函数库的名字，这个名字就是简单的soname名字，而不包含任何版本号信息。

管理共享函数库的关键是区分好这些名字。当可执行程序需要在自己的程序中列出这些他们需要的共享库函数的时候，它只要用soname就可以了；反过来，当你要创建一个新的共享函数库的时候，你要指定一个特定的文件名，其中包含很细节的版本信息。当你安装一个新版本的函数库的时候，你只要先将这些函数库文件拷贝到一些特定的目录中，运行ldconfig这个实用就可以。ldconfig检查已经存在的库文件，然后创建soname的符号链接到真正的函数库，同时设置/etc/ld.so.cache这个缓冲文件。这个我们稍后再讨论。

ldconfig 并不设置链接的名字，通常的做法是在安装过程中完成这个链接名字的建立，一般来说这个符号链接就简单的指向最新的soname或者最新版本的函数库文件。最好把这个符号链接指向soname，因为通常当你升级你的库函数后，你就可以自动使用新版本的函数库类。

我们来举例看看: /usr/lib/libreadline.so.3 是一个完全的完整的soname，ldconfig可以设置一个符号链接到其他某个真正的函数库文件，例如是/usr/lib/libreadline.so.3.0。同时还必须有一个链接名字，例如 /usr/lib/libreadline.so就是一个符号链接指向/usr/lib/libreadline.so.3。

3.1.2. 文件系统中函数库文件的位置

共享函数库文件必须放在一些特定的目录里，这样通过系统的环境变量设置，应用程序才能正确的使用这些函数库。大部分的源码开发的程序都遵循GNU的一些标准，我们可以看info帮助文件获得相信的说明，info信息的位置是: info:standards#Directory_Variables。GNU标准建议所有的函数库文件都放在/usr/local/lib目录下，而且建议命令可执行程序都放在/usr/local/bin目录下。这都是一些习惯问题，可以改变的。

文件系统层次化标准FHS (Filesystem Hierarchy Standard)  ([http://www.pathname.com/fhs](http://www.pathname.com/fhs)) 规定了在一个发行包中大部分的函数库文件应该安装到/usr/lib目录下，但是如果某些库是在系统启动的时候要加载的，则放到/lib目录下，而那些不是系统本身一部分的库则放到/usr/local/lib下面。

上面两个路径的不同并没有本质的冲突。GNU提出的标准主要对于开发者开发源码的，而FHS的建议则是针对发行版本的路径的。具体的位置信息可以看/etc/ld.so.conf里面的配置信息。

3.2. 这些函数库如何使用

在基于GNU glibc 的系统里，包括所有的linux 系统，启动一个ELF 格式的二进制可执行文件会自动启动和运行一个program loader。对于Linux 系统，这个loader 的名字是 /lib/ld-linux.so.X (X是版本号) 。这个loader 启动后，反过来就会load所有的其他本程序要使用的共享函数库。

到底在哪些目录里查找共享函数库呢？这些定义缺省的是放在 /etc/ld.so.conf 文件里面，我们可以修改这个文件，加入我们自己的一些特殊的路径要求。大多数RedHat系列的发行包的 /etc/ld.so.conf文件里面不包括 /usr/local/lib这个目录，如果没有这个目录的话，我们可以修改 /etc/ld.so.conf，自己手动加上这个条目。

如果你想覆盖某个库中的一些函数，用自己的函数替换它们，同时保留该库中其他的函数的话，你可以在 /etc/ld.so.preload中加入你想要替换的库 (.o结尾的文件) ，这些preloading的库函数将有优先加载的权利。

当程序启动的时候搜索所有的目录显然会效率很低，于是Linux系统实际上用的是一个高速缓冲的做法。ldconfig缺省情况下读出/etc/ld.so.conf相关信息，然后设置适当地符号链接，然后写一个cache到 /etc/ld.so.cache这个文件中，而这个/etc/ld.so.cache则可以被其他程序有效的使用了。这样的做法可以大大提高访问函数库的速度。这就要求每次新增加一个动态加载的函数库的时候，就要运行ldconfig来更新这个cache，如果要删除某个函数库，或者某个函数库的路径修改了，都要重新运行ldconfig来更新这个cache。通常的一些包管理器在安装一个新的函数库的时候就要运行ldconfig。

另外，FreeBSD使用cache的文件不一样。FreeBSD的ELF cache是/var/run/ld-elf.so.hints，而a.out的cache则是/var/run/ld.so.hints。它们同样是通过ldconfig来更新。

3.3. 环境变量

各种各样的环境变量控制着一些关键的过程。例如你可以临时为你特定的程序的一次执行指定一个不同的函数库。Linux系统中，通常变量LD_LIBRARY_PATH就是可以用来指定函数库查找路径的，而且这个路径通常是在查找标准的路径之前查找。这个是很有用的，特别是在调试一个新的函数库的时候，或者在特殊的场合使用一个非标准的函数库的时候。环境变量LD_PRELOAD列出了所有共享函数库中需要优先加载的库文件，功能和/etc/ld.so.preload类似。这些都是有/lib/ld-linux.so这个loader来实现的。值得一提的是，LD_LIBRARY_PATH可以在大部分的UNIX-linke系统下正常起作用，但是并非所有的系统下都可以使用，例如HP－UX系统下，就是用SHLIB_PATH这个变量，而在AIX下则使用LIBPATH这个变量。

LD_LIBRARY_PATH在开发和调试过程中经常大量使用，但是不应该被一个普通用户在安装过程中被安装程序修改，大家可以去参考[http://www.visi.com/~barr/ldpath.html,这里有一个文档专门介绍为什么不使用LD_LIBRARY_PATH](http://www.visi.com/~barr/ldpath.html,这里有一个文档专门介绍为什么不使用LD_LIBRARY_PATH)这个变量。

事实上还有更多的环境变量影响着程序的调入过程，它们的名字通常就是以LD_或者RTLD_打头。大部分这些环境变量的使用的文档都是不全，通常搞得人头昏眼花的，如果要真正弄清楚它们的用法，最好去读loader的源码 (也就是gcc的一部分) 。

允许用户控制动态链接函数库将涉及到setuid/setgid这个函数，如果特殊的功能需要的话。因此，GNU loader通常限制或者忽略用户对这些变量使用setuid和setgid。如果loader通过判断程序的相关环境变量判断程序的是否使用了setuid或者setgid，如果uid和euid不同，或者gid和egid部一样，那么loader就假定程序已经使用了setuid或者setgid，然后就大大的限制器控制这个老链接的权限。如果阅读GNU glibc的库函数源码，就可以清楚地看到这一点。特别的我们可以看elf/rtld.c和sysdeps/generic/dl-sysdep.c这两个文件。这就意味着如果你使得uid和gid与euid和egid分别相等，然后调用一个程序，那么这些变量就可以完全起效。

3.4. 创建一个共享函数库

现在我们开始学习如何创建一个共享函数库。其实创建一个共享函数库非常容易。首先创建object文件，这个文件将加入通过gcc –fPIC参数命令加入到共享函数库里面。PIC的意思是"位置无关代码" (Position Independent Code) 。下面是一个标准的格式:

gcc -shared -Wl,-soname,your_soname -o library_name file_list library_list

下面再给一个例子，它创建两个object文件 (a.o和b.o) ，然后创建一个包含a.o和b.o的共享函数库。例子中"-g"和"－Wall"参数不是必须的。

gcc -fPIC -g -c -Wall a.c

gcc -fPIC -g -c -Wall b.c

gcc -shared -Wl,-soname,liblusterstuff.so.1 -o liblusterstuff.so.1.0.1 a.o b.o -lc

下面是一些需要注意的地方:

不用使用-fomit-frame-pointer这个编译参数除非你不得不这样。虽然使用了这个参数获得的函数库仍然可以使用，但是这使得调试程序几乎没有用，无法跟踪调试。

使用-fPIC来产生代码，而不是-fpic。

某些情况下，使用gcc 来生成object文件，需要使用"-Wl,-export-dynamic"这个选项参数。

通常，动态函数库的符号表里面包含了这些动态的对象的符号。这个选项在创建ELF格式的文件时候，会将所有的符号加入到动态符号表中。可以参考ld的帮助获得更详细的说明。

3.5. 安装和使用共享函数库

一旦你定义了一个共享函数库，你还需要安装它。其实简单的方法就是拷贝你的库文件到指定的标准的目录 (例如/usr/lib) ，然后运行ldconfig。

如果你没有权限去做这件事情，例如你不能修改/usr/lib目录，那么你就只好通过修改你的环境变量来实现这些函数库的使用了。首先，你需要创建这些共享函数库；然后，设置一些必须得符号链接，特别是从soname到真正的函数库文件的符号链接，简单的方法就是运行ldconfig:

ldconfig -n directory_with_shared_libraries
  
然后你就可以设置你的LD_LIBRARY_PATH这个环境变量，它是一个以逗号分隔的路径的集合，这个可以用来指明共享函数库的搜索路径。例如，使用bash，就可以这样来启动一个程序my_program:

LD_LIBRARY_PATH=$LD_LIBRARY_PATH my_program

如果你需要的是重载部分函数，则你就需要创建一个包含需要重载的函数的object文件，然后设置LD_PRELOAD环境变量。

通常你可以很方便的升级你的函数库，如果某个API改变了，创建库的程序会改变soname。然而，如果一个函数升级了某个函数库而保持了原来的soname，你可以强行将老版本的函数库拷贝到某个位置，然后重新命名这个文件 (例如使用原来的名字，然后后面加.orig后缀) ，然后创建一个小的"wrapper"脚本来设置这个库函数和相关的东西。例如下面的例子:

# !/bin/sh export LD_LIBRARY_PATH=/usr/local/my_lib,$LD_LIBRARY_PATH

exec /usr/bin/my_program.orig $*

我们可以通过运行ldd来看某个程序使用的共享函数库。例如你可以看ls这个实用工具使用的函数库:

ldd /bin/ls

libtermcap.so.2 => /lib/libtermcap.so.2 (0x4001c000)

libc.so.6 => /lib/libc.so.6 (0x40020000)

/lib/ld-linux.so.2 => /lib/ld-linux.so.2 (0x40000000)
  
通常我么可以看到一个soname的列表，包括路径。在所有的情况下，你都至少可以看到两个库:

·                   /lib/ld-linux.so.N (N是1或者更大，一般至少2) 。这是这个用于加载其他所有的共享库的库。

·                    libc.so.N(N应该大于或者等于6)。这是C语言函数库。

值得一提的是，不要在对你不信任的程序运行ldd命令。在ldd的manual里面写得很清楚，ldd是通过设置某些特殊的环境变量 (例如，对于ELF对象，设置LD_TRACE_LOADED_OBJECTS) ，然后运行这个程序。这样就有可能使得某地程序可能使得ldd来执行某些意想不到的代码，而产生不安全的隐患。

3.6. 不兼容的函数库

如果一个新版的函数库要和老版本的二进制的库不兼容，则soname需要改变。对于C语言，一共有4个基本的理由使得它们在二进制代码上很难兼容:

一个函数的行文改变了，这样它就可能与最开始的定义不相符合。

·          输出的数据项改变了。

·          某些输出的函数删除了。

·          某些输出函数的接口改变了。
  
如果你能避免这些地方，你就可以保持你的函数库在二进制代码上的兼容，或者说，你可以使得你的程序的应用二进制接口 (ABI: Application Binary Interface) 上兼容。

****

**4. 动态加载的函数库Dynamically Loaded (DL) Libraries
  
**

动态加载的函数库Dynamically loaded (DL) libraries是一类函数库，它可以在程序运行过程中的任何时间加载。它们特别适合在函数中加载一些模块和plugin扩展模块的场合，因为它可以在当程序需要某个plugin模块时才动态的加载。例如，Pluggable Authentication Modules(PAM)系统就是用动态加载函数库来使得管理员可以配置和重新配置身份验证信息。

Linux系统下，DL函数库与其他函数库在格式上没有特殊的区别，我们前面提到过，它们创建的时候是标准的object格式。主要的区别就是这些函数库不是在程序链接的时候或者启动的时候加载，而是通过一个API来打开一个函数库，寻找符号表，处理错误和关闭函数库。通常C语言环境下，需要包含这个头文件。
  
Linux中使用的函数和Solaris中一样，都是dlpoen ()  API。当然不是所有的平台都使用同样的接口，例如HP-UX使用shl_load()机制，而Windows平台用另外的其他的调用接口。如果你的目的是使得你的代码有很强的移植性，你应该使用一些wrapping函数库，这样的wrapping函数库隐藏不同的平台的接口区别。一种方法是使用glibc函数库中的对动态加载模块的支持，它使用一些潜在的动态加载函数库界面使得它们可以夸平台使用。具体可以参考[http://developer.gnome.org/doc/API/glib/glib-dynamic-loading-of-modules.html](http://developer.gnome.org/doc/API/glib/glib-dynamic-loading-of-modules.html). 另外一个方法是使用libltdl，是GNU libtool的一部分，可以进一步参考CORBA相关资料。

4.1. dlopen()
  
dlopen函数打开一个函数库然后为后面的使用做准备。C语言原形是:

void \* dlopen(const char \*filename, int flag);

如果文件名filename是以"/"开头，也就是使用绝对路径，那么dlopne就直接使用它，而不去查找某些环境变量或者系统设置的函数库所在的目录了。否则dlopen () 就会按照下面的次序查找函数库文件:
  
1. 环境变量LD_LIBRARY指明的路径。

2. /etc/ld.so.cache中的函数库列表。

3. /lib目录，然后/usr/lib。不过一些很老的a.out的loader则是采用相反的次序，也就是先查 /usr/lib，然后是/lib。
  
dlopen()函数中，参数flag的值必须是RTLD_LAZY或者RTLD_NOW，RTLD_LAZY的意思是resolve undefined symbols as code from the dynamic library is executed，而RTLD_NOW的含义是resolve all undefined symbols before dlopen() returns and fail if this cannot be done'。
  
如果有好几个函数库，它们之间有一些依赖关系的话，例如X依赖Y，那么你就要先加载那些被依赖的函数。例如先加载Y，然后加载X。

dlopen () 函数的返回值是一个句柄，然后后面的函数就通过使用这个句柄来做进一步的操作。如果打开失败dlopen()就返回一个NULL。如果一个函数库被多次打开，它会返回同样的句柄。
  
如果一个函数库里面有一个输出的函数名字为_init,那么_init就会在dlopen () 这个函数返回前被执行。我们可以利用这个函数在我的函数库里面做一些初始化的工作。我们后面会继续讨论这个问题的。
  
4.2. dlerror()

通过调用dlerror()函数，我们可以获得最后一次调用dlopen()，dlsym()，或者dlclose () 的错误信息。
  
4.3. dlsym()

如果你加载了一个DL函数库而不去使用当然是不可能的了，使用一个DL函数库的最主要的一个函数就是dlsym()，这个函数在一个已经打开的函数库里面查找给定的符号。这个函数如下定义:

void \* dlsym(void \*handle, char *symbol);

函数中的参数handle就是由dlopen打开后返回的句柄，symbol是一个以NIL结尾的字符串。如果dlsym()函数没有找到需要查找的symbol，则返回NULL。如果你知道某个symbol的值不可能是NULL或者0，那么就很好，你就可以根据这个返回结果判断查找的symbol是否存在了；不过，如果某个symbol的值就是NULL，那么这个判断就有问题了。标准的判断方法是先调用dlerror()，清除以前可能存在的错误，然后调用dlsym () 来访问一个symbol，然后再调用dlerror () 来判断是否出现了错误。一个典型的过程如下:
  
      dlerror();      /*clear error code */
    
    
      s = (actual_type)dlsym(handle, symbol_being_searched_for);
    
    
      if((error = dlerror()) != NULL){
    
    
          /* handle error, the symbol wasn't found */
    
    
      } else {
    
    
          /* symbol found, its value is in s */
    
    
      }

4.4. dlclose()

dlopen()函数的反过程就是dlclose () 函数，dlclose () 函数用力关闭一个DL函数库。Dl函数库维持一个资源利用的计数器，当调用dlclose的时候，就把这个计数器的计数减一，如果计数器为0，则真正的释放掉。真正释放的时候，如果函数库里面有_fini()这个函数，则自动调用_fini () 这个函数，做一些必要的处理。Dlclose () 返回0表示成功，其他非0值表示错误。

4.5. DL Library Example

下面是一个例子。例子中调入math函数库，然后打印2.0的余弦函数值。例子中每次都检查是否出错。应该是个不错的范例:
  
      int main(int argc, char *argv){
    
    
              void *handle;
    
    
              char *error;
    
    
    
    
              double (*cosine )(double);
    
    
              handle = dlopen("/lib/libm.so.6", RTLD_LAZY);
    
    
              if(!handle){
    
    
                  fputs(dlerror(), stderr);
    
    
                   exit(1);
    
    
              }
    
    
    
    
              cosine = dlsym(handle, "cos");
    
    
              if((error = dlerror()) != NULL){
    
    
                  fputs(error, stderr);
    
    
                  exit(1);
    
    
              }
    
    
    
    
              printf("%f", (*cosine)(2, 0));
    
    
    
    
              dlclose(handle);
    
    
    
    
              return 0;
    
    
      }

如果这个程序名字叫foo.c,那么用下面的命令来编译:

gcc -o foo foo.c –ldl

**参考推荐:**

Linux动态链接库.so文件的创建与使用

Linux动态库(.so)搜索路径

Linux 动态库与静态库制作及使用详解
