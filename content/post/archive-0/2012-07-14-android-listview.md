---
title: android ListView
author: wiloon
type: post
date: 2012-07-14T12:24:31+00:00
url: /?p=3850
categories:
  - Uncategorized

---
本文来自http://blog.csdn.net/hellogv/

ListView是一个经常用到的控件，ListView里面的每个子项Item可以使一个字符串，也可以是一个组合控件。先说说ListView的实现：

1.准备ListView要显示的**数据** ；

2.使用 一维或多维 **动态数组 **保存数据；

2.构建**适配器** ， 简单地来说， 适配器就是 **Item数组 **， **动态数组 **有多少元素就生成多少个Item；

3.把 **适配器** 添加到ListView,并显示出来。

接下来，就开始UI的XML代码：

main.xml代码如下，很简单，也不需要多做解释了：

<div>
  <div>
    <p>
      [xml]</div><br /> <div><?xml version="1.0" encoding="utf-8"?></div><br /> <div><LinearLayout</div><br /> <div>android:id="@+id/LinearLayout01"<br /> android:layout_width="fill_parent"<br /> android:layout_height="fill_parent"<br /> xmlns:android="http://schemas.android.com/apk/res/android">
    </p>
    
    <p>
      <ListView android:layout_width="wrap_content"<br /> android:layout_height="wrap_content"<br /> android:id="@+id/MyListView"><br /> </ListView><br /> </LinearLayout><br /> <div>[/xml]
    </p>
  </div>
</div>

<div>
  my_listitem.xml的代码如下，my_listitem.xml用于设计ListView的Item：</p> 
  
  <p>
    [xml]</div><br /> <div>
  </p>
  
  <p>
    <?xml version="1.0" encoding="utf-8"?><br /> <LinearLayout<br /> android:layout_width="fill_parent"<br /> xmlns:android="http://schemas.android.com/apk/res/android"<br /> android:orientation="vertical"<br /> android:layout_height="wrap_content"<br /> android:id="@+id/MyListItem"<br /> android:paddingBottom="3dip"<br /> android:paddingLeft="10dip"><br /> <TextView<br /> android:layout_height="wrap_content"<br /> android:layout_width="fill_parent"<br /> android:id="@+id/ItemTitle"<br /> android:textSize="30dip"><br /> </TextView><br /> <TextView<br /> android:layout_height="wrap_content"<br /> android:layout_width="fill_parent"<br /> android:id="@+id/ItemText"><br /> </TextView><br /> </LinearLayout>
  </p>
  
  <p>
    </div><br /> <div>[/xml]
  </p>
</div>

解释一下，里面用到的一些属性：

1.paddingBottom=&#8221;3dip&#8221;，Layout往底部留出3个像素的空白区域

2.paddingLeft=&#8221;10dip&#8221;，Layout往左边留出10个像素的空白区域

3.textSize=&#8221;30dip&#8221;，TextView的字体为30个像素那么大。

最后就是JAVA的源代码：

<div>
  <div>
    <div>
      <p>
        [java][/java]
      </p>
      
      <p>
        <a title="view plain" href="http://blog.csdn.net/hellogv/article/details/4542668#">view plain</a><a title="copy" href="http://blog.csdn.net/hellogv/article/details/4542668#">copy</a><a title="print" href="http://blog.csdn.net/hellogv/article/details/4542668#">print</a><a title="?" href="http://blog.csdn.net/hellogv/article/details/4542668#">?</a>
      </p>
      
      <div>
      </div>
    </div>
  </div>
  
  <ol start="1">
    <li>
      public void onCreate(Bundle savedInstanceState) {
    </li>
    <li>
          super.onCreate(savedInstanceState);
    </li>
    <li>
          setContentView(R.layout.main);
    </li>
    <li>
          //绑定XML中的ListView，作为Item的容器
    </li>
    <li>
          ListView list = (ListView) findViewById(R.id.MyListView);
    </li>
    <li>
          //生成动态数组，并且转载数据
    </li>
    <li>
          ArrayList<HashMap<String, String>> mylist = new ArrayList<HashMap<String, String>>();
    </li>
    <li>
          for(int i=0;i<30;i++)
    </li>
    <li>
          {
    </li>
    <li>
              HashMap<String, String> map = new HashMap<String, String>();
    </li>
    <li>
              map.put("ItemTitle&#8221;, "This is Title&#8230;..&#8221;);
    </li>
    <li>
              map.put("ItemText&#8221;, "This is text&#8230;..&#8221;);
    </li>
    <li>
              mylist.add(map);
    </li>
    <li>
          }
    </li>
    <li>
          //生成适配器，数组===》ListItem
    </li>
    <li>
          SimpleAdapter mSchedule = new SimpleAdapter(this, //没什么解释
    </li>
    <li>
                                                      mylist,//数据来源
    </li>
    <li>
                                                      R.layout.my_listitem,//ListItem的XML实现
    </li>
    <li>
                                                      //动态数组与ListItem对应的子项
    </li>
    <li>
                                                      new String[] {"ItemTitle&#8221;, "ItemText&#8221;},
    </li>
    <li>
                                                      //ListItem的XML文件里面的两个TextView ID
    </li>
    <li>
                                                      new int[] {R.id.ItemTitle,R.id.ItemText});
    </li>
    <li>
          //添加并且显示
    </li>
    <li>
          list.setAdapter(mSchedule);
    </li>
    <li>
      }
    </li>
  </ol>
  
  <p>
    
  </p>
  
  <p>
    <a href="http://www.vogella.com/articles/AndroidListView/article.html">http://www.vogella.com/articles/AndroidListView/article.html</a>
  </p>
  
  <p>
    http://www.iteye.com/topic/540423
  </p>
</div>