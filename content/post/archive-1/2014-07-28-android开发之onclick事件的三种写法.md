---
title: Android开发之onClick事件的三种写法
author: wiloon
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
  
/*\* Called when the activity is first created. \*/

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
  
String strTmp=&#8221;点击Button02";
  
Ev1.setText(strTmp);
  
}

};

//第三种方式(Android1.6版本及以后的版本中提供了)
  
public void Btn3OnClick(View view){
  
String strTmp=&#8221;点击Button03";
  
Ev1.setText(strTmp);

}
  
}

\[html\]\[/html\]

view plaincopy
  
<?xml version=&#8221;1.0" encoding=&#8221;utf-8"?>
  
<LinearLayout xmlns:android=&#8221;http://schemas.android.com/apk/res/android&#8221;
  
android:layout\_width=&#8221;fill\_parent&#8221;
  
android:layout\_height=&#8221;fill\_parent&#8221;
  
android:orientation=&#8221;vertical&#8221; >

<TextView
  
android:layout\_width=&#8221;fill\_parent&#8221;
  
android:layout\_height=&#8221;wrap\_content&#8221;
  
android:text=&#8221;@string/hello&#8221; />

<Button
  
android:id=&#8221;@+id/button1"
  
android:layout\_width=&#8221;wrap\_content&#8221;
  
android:layout\_height=&#8221;wrap\_content&#8221;
  
android:text=&#8221;Button1" />

<Button
  
android:id=&#8221;@+id/button2"
  
android:layout\_width=&#8221;wrap\_content&#8221;
  
android:layout\_height=&#8221;wrap\_content&#8221;
  
android:text=&#8221;Button2" />

<Button
  
android:id=&#8221;@+id/button3"
  
android:layout\_width=&#8221;wrap\_content&#8221;
  
android:layout\_height=&#8221;wrap\_content&#8221;
  
android:text=&#8221;Button3"
  
android:onClick=&#8221;Btn3OnClick&#8221;/>

<EditText
  
android:id=&#8221;@+id/editText1"
  
android:layout\_width=&#8221;match\_parent&#8221;
  
android:layout\_height=&#8221;wrap\_content&#8221; >

<requestFocus />
  
</EditText>

</LinearLayout>