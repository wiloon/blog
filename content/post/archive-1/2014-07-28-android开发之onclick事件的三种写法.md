---
title: Android开发之onClick事件的三种写法
author: "-"
type: post
date: 2014-07-28T08:52:43+00:00
url: /?p=6833
categories:
  - Uncategorized

---
http://blog.csdn.net/a9529lty/article/details/7542828

package a.a;

import android.app.Activity;
  
import android.os.Bundle;
  
import android.view.View;
  
import android.widget.Button;
  
import android.widget.EditText;

public class AActivity extends Activity {
  
/*\* Called when the activity is first created. */

EditText Ev1;

@Override
  
public void onCreate(Bundle savedInstanceState) {
  
super.onCreate(savedInstanceState);
  
setContentView(R.layout.main);

Ev1 = (EditText)findViewById(R.id.editText1);

//第一种方式
  
Button Btn1 = (Button)findViewById(R.id.button1);//获取按钮资源
  
Btn1.setOnClickListener(new Button.OnClickListener(){//创建监听
  
public void onClick(View v) {
  
String strTmp = "点击Button01";
  
Ev1.setText(strTmp);
  
}

});

//第二种方式
  
Button Btn2 = (Button) findViewById(R.id.button2);//获取按钮资源
  
Btn2.setOnClickListener(listener);//设置监听

}

Button.OnClickListener listener = new Button.OnClickListener(){//创建监听对象
  
public void onClick(View v){
  
String strTmp="点击Button02";
  
Ev1.setText(strTmp);
  
}

};

//第三种方式(Android1.6版本及以后的版本中提供了)
  
public void Btn3OnClick(View view){
  
String strTmp="点击Button03";
  
Ev1.setText(strTmp);

}
  
}

[html][/html]

view plaincopy
  
<?xml version="1.0" encoding="utf-8"?>
  
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
  
android:layout_width="fill_parent"
  
android:layout_height="fill_parent"
  
android:orientation="vertical" >

<TextView
  
android:layout_width="fill_parent"
  
android:layout_height="wrap_content"
  
android:text="@string/hello" />

<Button
  
android:id="@+id/button1"
  
android:layout_width="wrap_content"
  
android:layout_height="wrap_content"
  
android:text="Button1" />

<Button
  
android:id="@+id/button2"
  
android:layout_width="wrap_content"
  
android:layout_height="wrap_content"
  
android:text="Button2" />

<Button
  
android:id="@+id/button3"
  
android:layout_width="wrap_content"
  
android:layout_height="wrap_content"
  
android:text="Button3"
  
android:onClick="Btn3OnClick"/>

<EditText
  
android:id="@+id/editText1"
  
android:layout_width="match_parent"
  
android:layout_height="wrap_content" >

<requestFocus />
  
</EditText>

</LinearLayout>