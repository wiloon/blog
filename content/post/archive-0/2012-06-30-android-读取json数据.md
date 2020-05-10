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
      public String getJson(){<br /> String jsonString = &#8220;{&#8220;FLAG&#8221;:&#8221;flag&#8221;,&#8221;MESSAGE&#8221;:&#8221;SUCCESS&#8221;,&#8221;name&#8221;:[{&#8220;name&#8221;:&#8221;jack&#8221;},{&#8220;name&#8221;:&#8221;lucy&#8221;}]}&#8221;;//json字符串<br /> try {<br /> JSONObject result = new JSONObject(jsonstring);//转换为JSONObject<br /> int num = result.length();<br /> JSONArray nameList = result.getJSONArray(&#8220;name&#8221;);//获取JSONArray<br /> int length = nameList.length();<br /> String aa = &#8220;&#8221;;<br /> for(int i = 0; i < length; i++){//遍历JSONArray<br /> Log.d(&#8220;debugTest&#8221;,Integer.toString(i));<br /> JSONObject oj = nameList.getJSONObject(i);<br /> aa = aa + oj.getString(&#8220;name&#8221;)+&#8221;|&#8221;;</p> 
  
  <p>
    }<br /> Iterator<?> it = result.keys();<br /> String aa2 = &#8220;&#8221;;<br /> String bb2 = null;<br /> while(it.hasNext()){//遍历JSONObject<br /> bb2 = (String) it.next().toString();<br /> aa2 = aa2 + result.getString(bb2);
  </p>
  
  <p>
    }<br /> return aa;<br /> } catch (JSONException e) {<br /> throw new RuntimeException(e);<br /> }<br /> }
  </p>
</div>