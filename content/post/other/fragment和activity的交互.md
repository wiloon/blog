---
title: Fragment和Activity的交互
author: "-"
date: 2015-01-20T02:40:43+00:00
url: /?p=7265
categories:
  - Inbox
tags:
  - reprint
---
## Fragment和Activity的交互
http://www.cnblogs.com/mengdd/archive/2013/01/11/2856374.html

一个Fragment的实例总是和包含它的Activity直接相关。

fragment可以通过getActivity() 方法来获得Activity的实例，然后就可以调用一些例如findViewById()之类的方法。

如: 

View listView = getActivity().findViewById(R.id.list);
  
但是注意调用getActivity()时，fragment必须和activity关联 (attached to an activity) ，否则将会返回一个null。


相似的，activity也可以获得一个fragment的引用，从而调用fragment中的方法。

获得fragment的引用要用FragmentManager，之后可以调用findFragmentById() 或者 findFragmentByTag().

比如: 

ExampleFragment fragment = (ExampleFragment) getFragmentManager().findFragmentById(R.id.example_fragment);

创建事件回调
  
一些情况下，可能需要fragment和activity共享事件，一个比较好的做法是在fragment里面定义一个回调接口，然后要求宿主activity实现它。

当activity通过这个接口接收到一个回调，它可以同布局中的其他fragment分享这个信息。

例如，一个新闻显示应用在一个activity中有两个fragment，一个fragment A显示文章题目的列表，一个fragment B显示文章。

所以当一个文章被选择的时候，fragment A必须通知activity，然后activity通知fragment B，让它显示这篇文章。

这个情况下，在fragment A中声明一个这样的接口OnArticleSelectedListener: 
  
public static class FragmentA extends ListFragment {
  
...
  
// Container Activity must implement this interface
  
public interface OnArticleSelectedListener {
  
public void onArticleSelected(Uri articleUri);
  
}
  
...
  
}

之后包含这个fragment的activity实现这个OnArticleSelectedListener接口，用覆写的onArticleSelected()方法将fragment A中发生的事通知fragment B。

为了确保宿主activity实现这个接口，fragment A的onAttach() 方法 (这个方法在fragment 被加入到activity中时由系统调用) 中通过将传入的activity强制类型转换，实例化一个OnArticleSelectedListener对象: 
  
public static class FragmentA extends ListFragment {
  
OnArticleSelectedListener mListener;
  
...
  
@Override
  
public void onAttach(Activity activity) {
  
super.onAttach(activity);
  
try {
  
mListener = (OnArticleSelectedListener) activity;
  
} catch (ClassCastException e) {
  
throw new ClassCastException(activity.toString() + " must implement OnArticleSelectedListener");
  
}
  
}
  
...
  
}

如果activity没有实现这个接口，fragment将会抛出ClassCastException异常，如果成功了，mListener将会是activity实现OnArticleSelectedListener接口的一个引用，所以通过调用OnArticleSelectedListener接口的方法，fragment A可以和activity共享事件。

比如，如果fragment A是ListFragment的子类，每一次用户点击一个列表项目，系统调用fragment中的onListItemClick() 方法，在这个方法中可以调用onArticleSelected()方法与activity共享事件。
  
public static class FragmentA extends ListFragment {
  
OnArticleSelectedListener mListener;
  
...
  
@Override
  
public void onListItemClick(ListView l, View v, int position, long id) {
  
// Append the clicked item's row ID with the content provider Uri
  
Uri noteUri = ContentUris.withAppendedId(ArticleColumns.CONTENT_URI, id);
  
// Send the event and Uri to the host activity
  
mListener.onArticleSelected(noteUri);
  
}
  
...
  
}

处理Fragment的生命周期
  
三种停留状态

管理fragment的生命周期和管理activity的生命周期类似，和activity一样，fragment可以在三种状态下停留: 

Resumed

fragment在running的activity中可见。

Paused

另一个activity在前景运行，并且享有焦点，但是这个fragment所在的activity仍然可见 (前景activity部分遮挡或者是半透明的) 。

Stopped

fragment不可见。可能是因为宿主activity处于stopped状态，或者fragment被remove掉，然后加在了back stack中。

一个处于stopped状态的activity还是存活状态的，所有的状态和成员信息会被系统保持。但是，它不再被用户可见，并且如果宿主activity被kill掉，它也会被kill掉。


数据存储和恢复

和Activity类似，可以用Bundle类对象保存fragment的状态，当activity的进程被kill之后，需要重建activity时，可以用于恢复fragment的状态。

存储时利用onSaveInstanceState()回调函数，恢复时是在 onCreate(), onCreateView(), 或者onActivityCreated()里。
  
Back Stack

activity和fragment生命周期最重要的不同之处是它们如何存储在各自的back stack中。

Activity停止时，是存在一个由系统维护的back stack中，但是当fragment停止 (被remove) 时，需要程序员显示地调用addToBackStack() ，并且fragment是存在一个由宿主activity掌管的back stack中。
  
Fragment和Activity的生命周期

宿主activity的声明周期直接影响到fragment的生命周期，比如activity生命周期的回调函数调用时，所有在其中的fragment的相同的回调函数会同时被调用。

Fragment还有一些额外的生命周期回调函数: 

onAttach()

当fragment和activity被关联时调用。

onCreateView()

当创建fragment的UI被初始化时调用。

onActivityCreated()

当activity的onCreate()方法返回时调用。

onDestroyView()

当fragment的UI被移除的时候调用。

onDetach()

当fragment和activity去关联时调用。

如图: 


从这个图上可以看出activity的状态决定了fragment可能接收到的回调函数。

比如说，当activity接收到它的onCreate()回调函数，那么这个activity中的fragment最多接收到了onActivityCreated()。

当activity处于Resumed状态时，可以自由地添加和移除fragment，也即是说，只有activity在Resumed状态时，fragment的状态可以独立改变。

但是，当activity离开Resumed状态，fragment的生命周期被activity控制。

参考资料
  
API Guides: Fragments

http://developer.android.com/guide/components/fragments.html