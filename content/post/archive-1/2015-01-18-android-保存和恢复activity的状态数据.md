---
title: android 保存和恢复activity的状态数据
author: "-"
type: post
date: 2015-01-18T05:43:22+00:00
url: /?p=7259
categories:
  - Uncategorized

---
# android 保存和恢复activity的状态数据

androidjavaactivityonSaveInstanceStateBundle
  
[coolxing按: 转载请注明作者和出处, 如有谬误, 欢迎在评论中指正.]
  
一般来说, 调用onPause()和onStop()方法后的activity实例仍然存在于内存中, activity的所有信息和状态数据不会消失, 当activity重新回到前台之后, 所有的改变都会得到保留.

但是当系统内存不足时, 调用onPause()和onStop()方法后的activity可能会被系统摧毁, 此时内存中就不会存有该activity的实例对象了. 如果之后这个activity重新回到前台, 之前所作的改变就会消失. 为了避免此种情况的发生, 开发者可以覆写onSaveInstanceState()方法. onSaveInstanceState()方法接受一个Bundle类型的参数, 开发者可以将状态数据存储到这个Bundle对象中, 这样即使activity被系统摧毁, 当用户重新启动这个activity而调用它的onCreate()方法时, 上述的Bundle对象会作为实参传递给onCreate()方法, 开发者可以从Bundle对象中取出保存的数据, 然后利用这些数据将activity恢复到被摧毁之前的状态.

Java代码
  
public class MainActivity extends Activity {
  
public static final int SECOND_ACTIVITY = 0;
  
private String temp;

@Override
  
public void onCreate(Bundle savedInstanceState) {
  
super.onCreate(savedInstanceState);
  
// 从savedInstanceState中恢复数据, 如果没有数据需要恢复savedInstanceState为null
  
if (savedInstanceState != null) {
  
temp = savedInstanceState.getString("temp");
  
System.out.println("onCreate: temp = " + temp);
  
}
  
}

public void onResume() {
  
super.onResume();
  
temp = "xing";
  
System.out.println("onResume: temp = " + temp);
  
// 切换屏幕方向会导致activity的摧毁和重建
  
if (getRequestedOrientation() == ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED) {
  
setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);
  
System.out.println("屏幕切换");
  
}
  
}

// 将数据保存到outState对象中, 该对象会在重建activity时传递给onCreate方法
  
@Override
  
protected void onSaveInstanceState(Bundle outState) {
  
super.onSaveInstanceState(outState);
  
outState.putString("temp", temp);
  
}
  
}
  
需要注意的是, onSaveInstanceState()方法并不是一定会被调用的, 因为有些场景是不需要保存状态数据的. 比如用户按下BACK键退出activity时, 用户显然想要关闭这个activity, 此时是没有必要保存数据以供下次恢复的, 也就是onSaveInstanceState()方法不会被调用. 如果调用onSaveInstanceState()方法, 调用将发生在onPause()或onStop()方法之前.
  
onSaveInstanceState()方法的默认实现

如果开发者没有覆写onSaveInstanceState()方法, 此方法的默认实现会自动保存activity中的某些状态数据, 比如activity中各种UI控件的状态. android应用框架中定义的几乎所有UI控件都恰当的实现了onSaveInstanceState()方法, 因此当activity被摧毁和重建时, 这些UI控件会自动保存和恢复状态数据. 比如EditText控件会自动保存和恢复输入的数据, 而CheckBox控件会自动保存和恢复选中状态. 开发者只需要为这些控件指定一个唯一的ID(通过设置android:id属性即可), 剩余的事情就可以自动完成了. 如果没有为控件指定ID, 则这个控件就不会进行自动的数据保存和恢复操作.

由上所述, 如果开发者需要覆写onSaveInstanceState()方法, 一般会在第一行代码中调用该方法的默认实现: super.onSaveInstanceState(outState).
  
是否需要覆写onSaveInstanceState()方法

既然该方法的默认实现可以自动的保存UI控件的状态数据, 那什么时候需要覆写该方法呢?

如果需要保存额外的数据时, 就需要覆写onSaveInstanceState()方法. 如需要保存类中成员变量的值(见上例).
  
onSaveInstanceState()方法适合保存什么数据

由于onSaveInstanceState()方法方法不一定会被调用, 因此不适合在该方法中保存持久化数据, 例如向数据库中插入记录等. 保存持久化数据的操作应该放在onPause()中. onSaveInstanceState()方法只适合保存瞬态数据, 比如UI控件的状态, 成员变量的值等.
  
引发activity摧毁和重建的其他情形

除了系统处于内存不足的原因会摧毁activity之外, 某些系统设置的改变也会导致activity的摧毁和重建. 例如改变屏幕方向(见上例), 改变设备语言设定, 键盘弹出等.


http://blog.csdn.net/lixiang0522/article/details/7565401

http://coolxing.iteye.com/blog/1279447

http://www.cnblogs.com/hanyonglu/archive/2012/03/28/2420515.html