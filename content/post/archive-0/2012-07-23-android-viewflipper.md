---
title: Android ViewFlipper
author: wiloon
type: post
date: 2012-07-23T04:54:14+00:00
url: /?p=3875
categories:
  - Uncategorized

---
http://www.itivy.com/android/archive/2012/5/4/634717451517462189.html

有一些场景，我们需要向用户展示一系列的页面。比如我们正在开发一个看漫画的应用，可能就需要向用户展示一张一张的漫画图片，用户使用手指滑动屏幕，可以在前一幅漫画和后一幅漫画之间切换。这个时候ViewFlipper就是一个很好的选择。


1）View切换的控件—ViewFlipper介绍

ViewFilpper类继承于ViewAnimator类。而ViewAnimator类继承于FrameLayout。

查看ViewAnimator类的源码可以看出此类的作用主要是为其中的View切换提供动画效果。该类有如下几个和动画相关的方法。

setInAnimation：设置View进入屏幕时候使用的动画。该方法有两个重载方法，即可以直接传入Animation对象，也可以传入定义的Animation文件的resourceID。

setOutAnimation：设置View退出屏幕时候使用的动画。使用方法和setInAnimation方法一样。

showNext：调用该方法可以显示FrameLayout里面的下一个View。

showPrevious：调用该方法可以来显示FrameLayout里面的上一个View。

查看ViewFlipper的源码可以看到，ViewFlipper主要用来实现View的自动切换。该类提供了如下几个主要的方法。

setFilpInterval：设置View切换的时间间隔。参数为毫秒。

startFlipping：开始进行View的切换，时间间隔是上述方法设置的间隔数。切换会循环进行。

stopFlipping：停止View切换。

setAutoStart：设置是否自动开始。如果设置为"true"，当ViewFlipper显示的时候View的切换会自动开始。

一般情况下，我们都会使用ViewFilpper类实现View的切换，而不使用它的父类ViewAnimator类。

2）实现滑动—GestureDetector介绍

如果想要实现滑动翻页的效果，就要了解另外一个类：android.view.GestureDetector类。GestureDetector类中可以用来检测各种手势事件。该类有两个回调接口，分别用来通知具体的事件。

GestureDetector.OnDoubleTapListener：用来通知DoubleTap事件，类似于PC上面的鼠标的双击事件。

GestureDetector.OnGestureListener：用来通知普通的手势事件，该接口有六个回调方法，具体的可以查看API。这里想要实现滑动的判断，就需要用到其中的onFling()方法。

3）具体的实现

下面的代码片段详细说明了如何实现滑动翻页。

```java

public class ViewFlipperActivity extends Activity implements OnGestureListener {

private static final int FLING\_MIN\_DISTANCE = 100;

private ViewFlipper flipper;

private GestureDetector detector;

@Override

protected void onCreate(Bundle savedInstanceState) {

super.onCreate(savedInstanceState);

setContentView(R.layout.viewflipper);

// 注册一个GestureDetector

detector = new GestureDetector(this);

flipper = (ViewFlipper) findViewById(R.id.ViewFlipper);

ImageView image1 = new ImageView(this);

image1.setBackgroundResource(R.drawable.image1);

// 增加第一个view

flipper.addView(image1);

ImageView image2 = new ImageView(this);

image2.setBackgroundResource(R.drawable.image2);

// 增加第二个view

flipper.addView(image2);

}

@Override

public boolean onTouchEvent(MotionEvent event) {

// 将触屏事件交给手势识别类处理

return this.detector.onTouchEvent(event);

}

@Override

public boolean onDown(MotionEvent e) {

return false;

}

@Override

public void onShowPress(MotionEvent e) {

}

@Override

public boolean onSingleTapUp(MotionEvent e) {

return false;

}

@Override

public boolean onScroll(MotionEvent e1, MotionEvent e2, float distanceX,

float distanceY) {

return false;

}

@Override

public void onLongPress(MotionEvent e) {

}

@Override

public boolean onFling(MotionEvent e1, MotionEvent e2, float velocityX,

float velocityY) {

if (e1.getX() - e2.getX() > FLING\_MIN\_DISTANCE) {

//设置View进入和退出的动画效果

this.flipper.setInAnimation(AnimationUtils.loadAnimation(this,

R.anim.left_in));

this.flipper.setOutAnimation(AnimationUtils.loadAnimation(this,

R.anim.left_out));

this.flipper.showNext();

return true;

}

if (e1.getX() - e2.getX() < -FLING\_MIN\_DISTANCE) {

this.flipper.setInAnimation(AnimationUtils.loadAnimation(this,

R.anim.right_in));

this.flipper.setOutAnimation(AnimationUtils.loadAnimation(this,

R.anim.right_out));

this.flipper.showPrevious();

return true;

}

return false;

}

}

```

在这段代码里，创建了两个IamgeView（用来显示图片），加入到了ViewFlipper中。程序运行后，当用手指在屏幕上向左滑动，会显示前一个图片，用手指在屏幕上向右滑动，会显示下一个图片。实现滑动切换的主要代码都在onFling()方法中，用户按下触摸屏，快速移动后松开，就会触发这个事件。在这段代码示例中，对手指滑动的距离进行了计算，如果滑动距离大于100像素，就做切换动作，否则不做任何切换动作。

可以看到，onFling()方法有四个参数，e1和e2上面代码用到了，比较好理解。参数velocityX和velocityY是做什么用的呢？velocityX和velocityY实际上是X轴和Y轴上的移动速度，单位是像素/秒。结合这两个参数，可以判断滑动的速度，从而做更多的处理。

为了显示出滑动的效果，这里调用了ViewFlipper的setInAnimation()和setOutAnimation()方法设置了View进入和退出的动画。对于动画的使用，这里不再赘述，也不再给出具体的XML文件代码了。

另外，在上面的代码基础上说些额外的话题。

在Xml布局文件中，我们既可以设置像素px，也可以设置dp（或者dip）。

一般情况下，我们都会选择使用dp，这样可以保证不同屏幕分辨率的手机上布局一致。但是在代码中，一般是无法直接使用dp的。

拿上面的代码为例，代码中定义了滑动的距离阀值为100像素。这就会导致不同分辨率的手机上效果有差别。比如在240X320的机型上，和在480X800的机型上，想要切换View，需要手指滑动的距离是不同的。所以，一般情况下，建议在代码中，也不要用像素，也用dp。

那么既然无法直接用dp，就需要从px转换成dp了。其实px和dp之间是有公式可以相互转换的。前面我的博客中（http://blog.csdn.net/arui319/article/details/6777133）已经写过了，可以直接参考。