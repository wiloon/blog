---
title: ExpandableListView
author: "-"
type: post
date: 2014-08-13T07:33:32+00:00
url: /?p=6936
categories:
  - Uncategorized

---
# ExpandableListView
http://www.cnblogs.com/eyu8874521/archive/2012/08/16/2642605.html

关于ExpandableListView用法的一个简单小例子
  
喜欢显示好友QQ那样的列表，可以展开，可以收起，在android中，以往用的比较多的是listview，虽然可以实现列表的展示，但在某些情况下，我们还是希望用到可以分组并实现收缩的列表，那就要用到android的ExpandableListView，今天研究了一下这个的用法，也参考了很多资料动手写了一个小demo，实现了基本的功能，但界面优化方面做得还不够好，有待改进，素材采用了Q版三国杀武将的图片，很有爱哈哈，下面直接上效果图以及源代码~！


main.xml的布局很简单啦，只是一个ExpandableListView 就OK了

但值得简单说下的是 android:cacheColorHint="#00000000"，这个设置可以去除拖动view时背景变成黑色的效果

android:listSelector="#00000000" ，可以去除选中时的黄色底色


复制代码
  
1 <?xml version="1.0" encoding="utf-8"?>
  
2 <LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
  
3 android:layout_width="fill_parent"
  
4 android:layout_height="fill_parent"
  
5 android:orientation="vertical" >
  
6 <ExpandableListView
  
7 android:id="@+id/list"
  
8 android:layout_width="fill_parent"
  
9 android:layout_height="fill_parent"
  
10 android:background="#ffffff"
  
11 android:cacheColorHint="#00000000"
  
12 android:listSelector="#00000000"
  
13 >
  
14 </ExpandableListView>
  
15 </LinearLayout>
  
复制代码


java代码: 


复制代码
  
package com.eyu.activity_test;

import android.app.Activity;
  
import android.graphics.Color;
  
import android.os.Bundle;
  
import android.view.Gravity;
  
import android.view.View;
  
import android.view.ViewGroup;
  
import android.view.Window;
  
import android.widget.AbsListView;
  
import android.widget.BaseExpandableListAdapter;
  
import android.widget.ExpandableListAdapter;
  
import android.widget.ExpandableListView;
  
import android.widget.ExpandableListView.OnChildClickListener;
  
import android.widget.ImageView;
  
import android.widget.LinearLayout;
  
import android.widget.TextView;
  
import android.widget.Toast;

public class ExpandableList extends Activity{

protected void onCreate(Bundle savedInstanceState) {
  
// TODO Auto-generated method stub
  
super.onCreate(savedInstanceState);
  
requestWindowFeature(Window.FEATURE_NO_TITLE);
  
setContentView(R.layout.main);

final ExpandableListAdapter adapter = new BaseExpandableListAdapter() {
  
//设置组视图的图片
  
int[] logos = new int[] { R.drawable.wei, R.drawable.shu,R.drawable.wu};
  
//设置组视图的显示文字
  
private String[] generalsTypes = new String[] { "魏", "蜀", "吴" };
  
//子视图显示文字
  
private String[][] generals = new String[][] {
  
{ "夏侯惇", "甄姬", "许褚", "郭嘉", "司马懿", "杨修" },
  
{ "马超", "张飞", "刘备", "诸葛亮", "黄月英", "赵云" },
  
{ "吕蒙", "陆逊", "孙权", "周瑜", "孙尚香" }

};
  
//子视图图片
  
public int[][] generallogos = new int[][] {
  
{ R.drawable.xiahoudun, R.drawable.zhenji,
  
R.drawable.xuchu, R.drawable.guojia,
  
R.drawable.simayi, R.drawable.yangxiu },
  
{ R.drawable.machao, R.drawable.zhangfei,
  
R.drawable.liubei, R.drawable.zhugeliang,
  
R.drawable.huangyueying, R.drawable.zhaoyun },
  
{ R.drawable.lvmeng, R.drawable.luxun, R.drawable.sunquan,
  
R.drawable.zhouyu, R.drawable.sunshangxiang } };

//自己定义一个获得文字信息的方法
  
TextView getTextView() {
  
AbsListView.LayoutParams lp = new AbsListView.LayoutParams(
  
ViewGroup.LayoutParams.FILL_PARENT, 64);
  
TextView textView = new TextView(
  
ExpandableList.this);
  
textView.setLayoutParams(lp);
  
textView.setGravity(Gravity.CENTER_VERTICAL);
  
textView.setPadding(36, 0, 0, 0);
  
textView.setTextSize(20);
  
textView.setTextColor(Color.BLACK);
  
return textView;
  
}
  
//重写ExpandableListAdapter中的各个方法
  
@Override
  
public int getGroupCount() {
  
// TODO Auto-generated method stub
  
return generalsTypes.length;
  
}

@Override
  
public Object getGroup(int groupPosition) {
  
// TODO Auto-generated method stub
  
return generalsTypes[groupPosition];
  
}

@Override
  
public long getGroupId(int groupPosition) {
  
// TODO Auto-generated method stub
  
return groupPosition;
  
}

@Override
  
public int getChildrenCount(int groupPosition) {
  
// TODO Auto-generated method stub
  
return generals[groupPosition].length;
  
}

@Override
  
public Object getChild(int groupPosition, int childPosition) {
  
// TODO Auto-generated method stub
  
return generals[groupPosition][childPosition];
  
}

@Override
  
public long getChildId(int groupPosition, int childPosition) {
  
// TODO Auto-generated method stub
  
return childPosition;
  
}

@Override
  
public boolean hasStableIds() {
  
// TODO Auto-generated method stub
  
return true;
  
}

@Override
  
public View getGroupView(int groupPosition, boolean isExpanded,
  
View convertView, ViewGroup parent) {
  
// TODO Auto-generated method stub
  
LinearLayout ll = new LinearLayout(
  
ExpandableList.this);
  
ll.setOrientation(0);
  
ImageView logo = new ImageView(ExpandableList.this);
  
logo.setImageResource(logos[groupPosition]);
  
logo.setPadding(50, 0, 0, 0);
  
ll.addView(logo);
  
TextView textView = getTextView();
  
textView.setTextColor(Color.BLACK);
  
textView.setText(getGroup(groupPosition).toString());
  
ll.addView(textView);

return ll;
  
}

@Override
  
public View getChildView(int groupPosition, int childPosition,
  
boolean isLastChild, View convertView, ViewGroup parent) {
  
// TODO Auto-generated method stub
  
LinearLayout ll = new LinearLayout(
  
ExpandableList.this);
  
ll.setOrientation(0);
  
ImageView generallogo = new ImageView(
  
ExpandableList.this);
  
generallogo
  
.setImageResource(generallogos[groupPosition][childPosition]);
  
ll.addView(generallogo);
  
TextView textView = getTextView();
  
textView.setText(getChild(groupPosition, childPosition)
  
.toString());
  
ll.addView(textView);
  
return ll;
  
}

@Override
  
public boolean isChildSelectable(int groupPosition,
  
int childPosition) {
  
// TODO Auto-generated method stub
  
return true;
  
}

};

ExpandableListView expandableListView = (ExpandableListView) findViewById(R.id.list);
  
expandableListView.setAdapter(adapter);

//设置item点击的监听器
  
expandableListView.setOnChildClickListener(new OnChildClickListener() {

@Override
  
public boolean onChildClick(ExpandableListView parent, View v,
  
int groupPosition, int childPosition, long id) {

Toast.makeText(
  
ExpandableList.this,
  
"你点击了" + adapter.getChild(groupPosition, childPosition),
  
Toast.LENGTH_SHORT).show();

return false;
  
}
  
});
  
}
  
}
  
复制代码