---
title: android 读取json数据
author: "-"
type: post
date: 2012-06-30T14:40:36+00:00
url: /?p=3701
categories:
  - Uncategorized

---
  
    android 读取json数据（遍历JSONObject和JSONArray）
  


  <a href="http://tangshanxj.blog.163.com/blog/static/30113717201010282318941/">http://tangshanxj.blog.163.com/blog/static/30113717201010282318941/</a>


      public String getJson(){
 String jsonString = "{"FLAG":"flag","MESSAGE":"SUCCESS","name":[{"name":"jack"},{"name":"lucy"}]}";//json字符串
 try {
 JSONObject result = new JSONObject(jsonstring);//转换为JSONObject
 int num = result.length();
 JSONArray nameList = result.getJSONArray("name");//获取JSONArray
 int length = nameList.length();
 String aa = "";
 for(int i = 0; i < length; i++){//遍历JSONArray
 Log.d("debugTest",Integer.toString(i));
 JSONObject oj = nameList.getJSONObject(i);
 aa = aa + oj.getString("name")+"|"; 
  
    }
 Iterator<?> it = result.keys();
 String aa2 = "";
 String bb2 = null;
 while(it.hasNext()){//遍历JSONObject
 bb2 = (String) it.next().toString();
 aa2 = aa2 + result.getString(bb2);
  
  
    }
 return aa;
 } catch (JSONException e) {
 throw new RuntimeException(e);
 }
 }
  
