---
title: Java ClassLoader
author: lcf
date: 2012-09-26T07:02:08+00:00
url: /?p=4316
categories:
  - Java

tags:
  - reprint
---
## Java ClassLoader
不同的JVM的实现不同，本文所描述的内容均只限于Hotspot Jvm.

本文将会从JDK默认的提供的ClassLoader，双亲委托模型，如何自定义ClassLoader以及Java中打破双亲委托机制的场景四个方面入手去讨论和总结一下。

JDK默认ClassLoader
  
JDK 默认提供了如下几种ClassLoader


Bootstrp loader
  
Bootstrp加载器是用C++语言写的，用来加载核心类库，如 java.lang.* 等.它是在Java虚拟机启动后初始化的，它主要负责加载%JAVA_HOME%/jre/lib,-Xbootclasspath参数指定的路径以及%JAVA_HOME%/jre/classes中的类。


ExtClassLoader
  
Bootstrp loader加载ExtClassLoader,并且将ExtClassLoader的父加载器设置为Bootstrp loader.ExtClassLoader是用Java写的，具体来说就是 sun.misc.Launcher$ExtClassLoader，ExtClassLoader主要加载%JAVA_HOME%/jre/lib/ext，此路径下的所有classes目录以及java.ext.dirs系统变量指定的路径中类库。
  
AppClassLoader
  
Bootstrp loader加载完ExtClassLoader后，就会加载AppClassLoader,并且将AppClassLoader的父加载器指定为 ExtClassLoader。AppClassLoader也是用Java写成的，它的实现类是 sun.misc.Launcher$AppClassLoader，另外我们知道ClassLoader中有个getSystemClassLoader方法,此方法返回的正是AppclassLoader.AppClassLoader主要负责加载classpath所指定的位置的类或者是jar文档，它也是Java程序默认的类加载器。
  
综上所述，它们之间的关系可以通过下图形象的描述: 

双亲委托模型
  
Java中ClassLoader的加载采用了双亲委托机制，采用双亲委托机制加载类的时候采用如下的几个步骤: 

当前ClassLoader首先从自己已经加载的类中查询是否此类已经加载，如果已经加载则直接返回原来已经加载的类。

每个类加载器都有自己的加载缓存，当一个类被加载了以后就会放入缓存，等下次加载的时候就可以直接返回了。
  
当前classLoader的缓存中没有找到被加载的类的时候，委托父类加载器去加载，父类加载器采用同样的策略，首先查看自己的缓存，然后委托父类的父类去加载，一直到bootstrp ClassLoader.
  
当所有的父类加载器都没有加载的时候，再由当前的类加载器加载，并将其放入它自己的缓存中，以便下次有加载请求的时候直接返回。
  
说到这里大家可能会想，Java为什么要采用这样的委托机制？理解这个问题，我们引入另外一个关于Classloader的概念"命名空间"， 它是指要确定某一个类，需要类的全限定名以及加载此类的ClassLoader来共同确定。也就是说即使两个类的全限定名是相同的，但是因为不同的 ClassLoader加载了此类，那么在JVM中它是不同的类。明白了命名空间以后，我们再来看看委托模型。采用了委托模型以后加大了不同的 ClassLoader的交互能力，比如上面说的，我们JDK本生提供的类库，比如hashmap,linkedlist等等，这些类由bootstrp 类加载器加载了以后，无论你程序中有多少个类加载器，那么这些类其实都是可以共享的，这样就避免了不同的类加载器加载了同样名字的不同类以后造成混乱。

如何自定义ClassLoader
  
Java除了上面所说的默认提供的classloader以外，它还容许应用程序可以自定义classloader，那么要想自定义classloader我们需要通过继承java.lang.ClassLoader来实现,接下来我们就来看看再自定义Classloader的时候，我们需要注意的几个重要的方法: 

1.loadClass 方法
  
loadClass method declare

public Class<?> loadClass(String name)  throws ClassNotFoundException
  
上面是loadClass方法的原型声明，上面所说的双亲委托机制的实现其实就实在此方法中实现的。下面我们就来看看此方法的代码来看看它到底如何实现双亲委托的。

loadClass method implement

public Class<?> loadClass(String name) throws ClassNotFoundException
  
{
  
return loadClass(name, false);
  
}
  
从上面可以看出loadClass方法调用了loadcClass(name,false)方法，那么接下来我们再来看看另外一个loadClass方法的实现。

Class loadClass(String name, boolean resolve)

protected synchronized Class<?> loadClass(String name, boolean resolve)  throws ClassNotFoundException
  
{  // First, check if the class has already been loaded  Class c = findLoadedClass(name);
  
//检查class是否已经被加载过了  if (c == null)
  
{
  
try {
  
if (parent != null) {
  
c = parent.loadClass(name, false); //如果没有被加载，且指定了父类加载器，则委托父加载器加载。
  
} else {
  
c = findBootstrapClass0(name);//如果没有父类加载器，则委托bootstrap加载器加载      }
  
} catch (ClassNotFoundException e) {
  
// If still not found, then invoke findClass in order
  
// to find the class.
  
c = findClass(name);//如果父类加载没有加载到，则通过自己的findClass来加载。      }
  
}
  
if (resolve)
  
{
  
resolveClass(c);
  
}
  
return c;
  
}
  
上面的代码，我加了注释通过注释可以清晰看出loadClass的双亲委托机制是如何工作的。 这里我们需要注意一点就是public Class<?> loadClass(String name) throws ClassNotFoundException没有被标记为final，也就意味着我们是可以override这个方法的，也就是说双亲委托机制是可以打破的。另外上面注意到有个findClass方法，接下来我们就来说说这个方法到底是搞末子的。

2.findClass
  
我们查看java.lang.ClassLoader的源代码，我们发现findClass的实现如下: 

protected Class<?> findClass(String name) throws ClassNotFoundException
  
{
  
throw new ClassNotFoundException(name);
  
}
  
我们可以看出此方法默认的实现是直接抛出异常，其实这个方法就是留给我们应用程序来override的。那么具体的实现就看你的实现逻辑了，你可以从磁盘读取，也可以从网络上获取class文件的字节流，获取class二进制了以后就可以交给defineClass来实现进一步的加载。defineClass我们再下面再来描述。 ok，通过上面的分析，我们可以得出如下结论: 

我们在写自己的ClassLoader的时候，如果想遵循双亲委托机制，则只需要override findClass.
  
3.defineClass
  
我们首先还是来看看defineClass的源码: 

defineClass

protected final Class<?> defineClass(String name, byte[] b, int off, int len)
  
throws ClassFormatError
  
{
  
return defineClass(name, b, off, len, null);
  
}
  
从上面的代码我们看出此方法被定义为了final，这也就意味着此方法不能被Override，其实这也是jvm留给我们的唯一的入口，通过这个唯 一的入口，jvm保证了类文件必须符合Java虚拟机规范规定的类的定义。此方法最后会调用native的方法来实现真正的类的加载工作。

Ok,通过上面的描述，我们来思考下面一个问题: 
  
假如我们自己写了一个java.lang.String的类，我们是否可以替换调JDK本身的类？

答案是否定的。我们不能实现。为什么呢？我看很多网上解释是说双亲委托机制解决这个问题，其实不是非常的准确。因为双亲委托机制是可以打破的，你完全可以自己写一个classLoader来加载自己写的java.lang.String类，但是你会发现也不会加载成功，具体就是因为针对java.*开头的类，jvm的实现中已经保证了必须由bootstrp来加载。
  
不遵循"双亲委托机制"的场景
  
上面说了双亲委托机制主要是为了实现不同的ClassLoader之间加载的类的交互问题，被大家公用的类就交由父加载器去加载，但是Java中确实也存在父类加载器加载的类需要用到子加载器加载的类的情况。下面我们就来说说这种情况的发生。

Java中有一个SPI(Service Provider Interface)标准,使用了SPI的库，比如JDBC，JNDI等，我们都知道JDBC需要第三方提供的驱动才可以，而驱动的jar包是放在我们应 用程序本身的classpath的，而jdbc 本身的api是jdk提供的一部分，它已经被bootstrp加载了，那第三方厂商提供的实现类怎么加载呢？这里面JAVA引入了线程上下文类加载的概 念，线程类加载器默认会从父线程继承，如果没有指定的话，默认就是系统类加载器 (AppClassLoader) ,这样的话当加载第三方驱动的时候，就可 以通过线程的上下文类加载器来加载。
  
另外为了实现更灵活的类加载器OSGI以及一些Java app server也打破了双亲委托机制。

http://www.javaworld.com/javaworld/jw-10-1996/jw-10-indepth.html?page=1

The class loader concept, one of the cornerstones of the Java virtual machine, describes the behavior of converting a named class into the bits responsible for implementing that class. Because class loaders exist, the Java run time does not need to know anything about files and file systems when running Java programs.

What class loaders do
  
Classes are introduced into the Java environment when they are referenced by name in a class that is already running. There is a bit of magic that goes on to get the first class running (which is why you have to declare the main() method as static, taking a string array as an argument), but once that class is running, future attempts at loading classes are done by the class loader.

At its simplest, a class loader creates a flat name space of class bodies that are referenced by a string name. The method definition is:

  
    
      
        
          
            
              Class r = loadClass(String className, boolean resolveIt);
            
          
        
      
    
  

The variable className contains a string that is understood by the class loader and is used to uniquely identify a class implementation. The variable resolveIt is a flag to tell the class loader that classes referenced by this class name should be resolved (that is, any referenced class should be loaded as well).

All Java virtual machines include one class loader that is embedded in the virtual machine. This embedded loader is called the primordial class loader. It is somewhat special because the virtual machine assumes that it has access to a repository of trusted classes which can be run by the VM without verification.

The primordial class loader implements the default implementation of loadClass(). Thus, this code understands that the class name java.lang.Object is stored in a file with the prefix java/lang/Object.class somewhere in the class path. This code also implements both class path searching and looking into zip files for classes. The really cool thing about the way this is designed is that Java can change its class storage model simply by changing the set of functions that implements the class loader.

Digging around in the guts of the Java virtual machine, you will discover that the primordial class loader is implemented primarily in the functions FindClassFromClass and ResolveClass.

So when are classes loaded? There are exactly two cases: when the new bytecode is executed (for example, FooClass f = new FooClass();) and when the bytecodes make a static reference to a class (for example, System.out).

A non-primordial class loader
  
"So what?" you might ask.

The Java virtual machine has hooks in it to allow a user-defined class loader to be used in place of the primordial one. Furthermore, since the user class loader gets first crack at the class name, the user is able to implement any number of interesting class repositories, not the least of which is HTTP servers — which got Java off the ground in the first place.

There is a cost, however, because the class loader is so powerful (for example, it can replace java.lang.Object with its own version), Java classes like applets are not allowed to instantiate their own loaders. (This is enforced by the class loader, by the way.) This column will not be useful if you are trying to do this stuff with an applet, only with an application running from the trusted class repository (such as local files).

A user class loader gets the chance to load a class before the primordial class loader does. Because of this, it can load the class implementation data from some alternate source, which is how the AppletClassLoader can load classes using the HTTP protocol.

Building a SimpleClassLoader
  
A class loader starts by being a subclass of java.lang.ClassLoader. The only abstract method that must be implemented is loadClass(). The flow of loadClass() is as follows:

Verify class name.
  
Check to see if the class requested has already been loaded.
  
Check to see if the class is a "system" class.
  
Attempt to fetch the class from this class loader's repository.
  
Define the class for the VM.
  
Resolve the class.
  
Return the class to the caller.

Some Java code that implements this flow is taken from the file SimpleClassLoader and appears as follows with descriptions about what it does interspersed with the code.

  
    
      
        
          
            
              public synchronized Class loadClass(String className, boolean resolveIt)
            
            
            
               throws ClassNotFoundException {
            
            
            
               Class result;
            
            
            
               byte classData[];
            
            
            
               System.out.println(" >>>>>> Load class : "+className);
            
            
            
               /* Check our local cache of classes */
            
            
            
               result = (Class)classes.get(className);
            
            
            
               if (result != null) {
            
            
            
               System.out.println(" >>>>>> returning cached result.");
            
            
            
               return result;
            
            
            
               }
            
          
        
      
    
  

The code above is the first section of the loadClass method. As you can see, it takes a class name and searches a local hash table that our class loader is maintaining of classes it has already returned. It is important to keep this hash table around since you must return the same class object reference for the same class name every time you are asked for it. Otherwise the system will believe there are two different classes with the same name and will throw a ClassCastException whenever you assign an object reference between them. It's also important to keep a cache because the loadClass() method is called recursively when a class is being resolved, and you will need to return the cached result rather than chase it down for another copy.

  
    
      
        
          
            
              /* Check with the primordial class loader */
            
            
            
               try {
            
            
            
               result = super.findSystemClass(className);
            
            
            
               System.out.println(" >>>>>> returning system class (in CLASSPATH).");
            
            
            
               return result;
            
            
            
               } catch (ClassNotFoundException e) {
            
            
            
               System.out.println(" >>>>>> Not a system class.");
            
            
            
               }
            
          
        
      
    
  

As you can see in the code above, the next step is to check if the primordial class loader can resolve this class name. This check is essential to both the sanity and security of the system. For example, if you return your own instance of java.lang.Object to the caller, then this object will share no common superclass with any other object! The security of the system can be compromised if your class loader returned its own value of java.lang.SecurityManager, which did not have the same checks as the real one did.

  
    
      
        
          
            
              /* Try to load it from our repository */
            
            
            
               classData = getClassImplFromDataBase(className);
            
            
            
               if (classData == null) {
            
            
            
               throw new ClassNotFoundException();
            
            
            
               }
            
          
        
      
    
  

After the initial checks, we come to the code above which is where the simple class loader gets an opportunity to load an implementation of this class. As you can see from the source code, the SimpleClassLoader has a method getClassImplFromDataBase() which in our simple example merely prefixes the directory "store" to the class name and appends the extension ".impl". I chose this technique in the example so that there would be no question of the primordial class loader finding our class. Note that the sun.applet.AppletClassLoader prefixes the codebase URL from the HTML page where an applet lives to the name and then does an HTTP get request to fetch the bytecodes.

http://www.blogjava.net/realsmy/archive/2007/04/03/108053.html

JAVA中的一切都是以类的形式存在的 (除少数底层的东西，那些我就不清楚是怎么回事了) 。我们运行的接口是一个类，运行中所涉及到的对象也都是类对象。下面，我们来研究下，我所理解的类的加载机制。

比如我们有一个Student类，也就是经过编译后，是一个Student.class文件。当我们的程序运行的过程中，第一次实例化一个student对象的时候，系统首先要做的就是加载Student这个类。也就是把Student.class以字节玛的形势加载到内存中 (并通过defineClass()这个方法转变成Class对象，最终以Class对象的形式存储在内存中) 。这个加载的过程就是由类加载器来完成的。

一般的，在程序启动之后，系统会主要会有三个类加载器: Bootstrap Loader、ExtClassLoader与AppClassLoader。

Bootstrap Loader是由C++撰写的，它主要负责搜索JRE所在目录的classes或lib目录下的.jar文件 (例如rt.jar) 是否需要被加载 (实际上是由系统参数sun.boot.class.path来指定) ；ExtClassLoader主要负责搜索JRE所在目录的lib/ext 目录下的classes或.jar中是否需要被加载 (实际上是由系统参数java.ext.dirs指定) ；AppClassLoader则是搜索 Classpath中是否有指定的classes需要被载入 (由系统参数java.class.path指定) 。

简单的说，Bootstrap Loader、ExtClassLoader这两个类加载器，主要是加载系统类库里的类。我们自己编辑的类一般都是由AppClassLoader来加载。当我们遇到如下代码的时候: 

  
    
      
        
          
            
              Student stu = new Student();
            
            
            
              //实例化一个Student类的对象stu
            
          
        
      
    
  

AppClassLoader首先会到classpath下去寻找Student.class文件。 (找不到则会抛出ClassNotFoundException异常) 找到之后便会把Student这个类以二进制的形式存储到内存中。这个过程也就是对Student类加载的过程。然后用我们加载到内存中的Student类去实例化一个Student对象stu。

以上就是所谓的隐式的类的加载过程。但是有些时候需要我们自定义一个类的加载器，这个时候就需要我们模仿这个过程，显示的加载我们自己所需要的类。比如，我们自定义一个类的加载器MyClassLoader，那我们利用我们自定义的这个加载器，显示的去加载一个类的过程也是这样的: 

1.寻找类文件。
  
这里的灵活性比较大，我们可以自己去设计如何去寻找类文件以及去哪里寻找类文件。比如一些非本地的类文件，通过系统的类加载器无法加载到这些类，这个时候，我们就可以利用自定义的类加载器指定路径去寻找。
  
2.加载类文件。
  
找到我们所要加载的类之后，通过MyClassLoader的defineClass()方法，把这个类加载到指定的内存中。这里我们可以自己设定存储类的内存空间，比如把我们加载的类都统一放到一个变量数组里 (至于系统的类加载到内存中是以什么样的形式存储再内存中的，我还不清楚，只知道是以二进制的形式保存的，可以用一个Class对象去引用) 。
  
3.创建类对象。
  
我接触的时候还不大理解，其实这里是应用我们自己加载到内存中的类，去实例化一个对象。以下代码可以参考: 

  
    
      
        
          
            
              import java.net.MalformedURLException;
            
            
            
               import java.net.URL;
            
            
            
            
            
            
              class MyClassLoader {
            
            
            
               public static void main(String[] args) throws MalformedURLException,
            
            
            
               ClassNotFoundException {
            
            
            
               URL url1 = new URL("file:/d:/workspace/");
            
            
            
               // 指定路径，相当于classpath的意思。
            
            
            
               myClassLoader myClassLoader = new MyClassLoader(new URL[] { url1 });
            
            
            
               // 用这个路径创建一个myClassLoader对象。这里随你所定义的ClassLoader而定。
            
            
            
               Class c1 = myClassLoader.loadClass("Student");
            
            
            
               // 用自定义的类加载器，去显式的加载一个类。返回一个Class对象。
            
            
            
               Student stu = c1.newInstance();
            
            
            
               // 用这个Class对象就可以产生一个ClassLoaderTest的实例。
            
            
            
               }
            
            
            
               }
            
          
        
      
    
  

https://my.oschina.net/aminqiao/blog/262601


```java

public class ClassLoader {

public <T> T loadClass(String fullClassPath) {
   
T clazz = null;
   
try {
   
@SuppressWarnings("unchecked")
   
Class<T> conClass = (Class<T>) Class.forName(fullClassPath);
   
clazz = conClass.newInstance();
   
} catch (Exception e) {
   
throw new ISException(
   
"Cannot load class:"
   
+ fullClassPath
   
+ ". Please confirm the class has a non-parameter constructor.",
   
e);
   
}
   
return clazz;
   
}

}

```