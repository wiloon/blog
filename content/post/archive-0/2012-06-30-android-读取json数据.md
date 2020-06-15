---
title: android 读取json数据
author: wiloon
type: post
date: 2012-06-30T14:40:36+00:00
url: /?p=3701
categories:
  - Uncategorized

---
<div>
  <h3>
    android 读取json数据（遍历JSONObject和JSONArray）
  </h3>
</div>

<div>
  <a href="http://tangshanxj.blog.163.com/blog/static/30113717201010282318941/">http://tangshanxj.blog.163.com/blog/static/30113717201010282318941/</a>
</div>

<div>
      public String getJson(){
 String jsonString = "{"FLAG&#8221;:&#8221;flag&#8221;,&#8221;MESSAGE&#8221;:&#8221;SUCCESS&#8221;,&#8221;name&#8221;:[{"name&#8221;:&#8221;jack&#8221;},{"name&#8221;:&#8221;lucy&#8221;}]}&#8221;;//json字符串
 try {
 JSONObject result = new JSONObject(jsonstring);//转换为JSONObject
 int num = result.length();
 JSONArray nameList = result.getJSONArray("name&#8221;);//获取JSONArray
 int length = nameList.length();
 String aa = "&#8221;;
 for(int i = 0; i < length; i++){//遍历JSONArray
 Log.d("debugTest&#8221;,Integer.toString(i));
 JSONObject oj = nameList.getJSONObject(i);
 aa = aa + oj.getString("name&#8221;)+&#8221;|&#8221;;</p> 
  
  <p>
    }
 Iterator<?> it = result.keys();
 String aa2 = "&#8221;;
 String bb2 = null;
 while(it.hasNext()){//遍历JSONObject
 bb2 = (String) it.next().toString();
 aa2 = aa2 + result.getString(bb2);
  </p>
  
  <p>
    }
 return aa;
 } catch (JSONException e) {
 throw new RuntimeException(e);
 }
 }
  </p>
</div>