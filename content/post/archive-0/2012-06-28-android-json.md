---
title: android json
author: wiloon
type: post
date: 2012-06-28T15:40:21+00:00
url: /?p=3696
categories:
  - Uncategorized

---
<http://blog.csdn.net/aomandeshangxiao/article/details/7000077>



JSON的定义：

一种轻量级的数据交换格式，具有良好的可读和便于快速编写的特性。业内主流技术为其提供了完整的解决方案（有点类似于正则表达式 ，获得了当今大部分语言的支持），从而可以在不同平台间进行数据交换。JSON采用兼容性很高的文本格式，同时也具备类似于C语言体系的行为。 – Json.org

JSON Vs XML

1.JSON和XML的数据可读性基本相同

2.JSON和XML同样拥有丰富的解析手段

3.JSON相对于XML来讲，数据的体积小

4.JSON与JavaScript的交互更加方便

5.JSON对数据的描述性比XML较差

6.JSON的速度要远远快于XML

android2.3提供的json解析类

android的json解析部分都在包org.json下，主要有以下几个类：

JSONObject：可以看作是一个json对象,这是系统中有关JSON定义的基本单元，其包含一对儿(Key/Value)数值。它对外部(External： 应用toString()方法输出的数值)调用的响应体现为一个标准的字符串（例如：{"JSON&#8221;: "Hello, World&#8221;}，最外被大括号包裹，其中的Key和Value被冒号&#8221;:&#8221;分隔）。其对于内部(Internal)行为的操作格式略微，例如：初始化一个JSONObject实例，引用内部的put()方法添加数值：new JSONObject().put("JSON&#8221;, "Hello, World!&#8221;)，在Key和Value之间是以逗号&#8221;,&#8221;分隔。Value的类型包括：Boolean、JSONArray、JSONObject、Number、String或者默认值JSONObject.NULL object 。

JSONStringer：json文本构建类 ，根据官方的解释，这个类可以帮助快速和便捷的创建JSON text。其最大的优点在于可以减少由于 格式的错误导致程序异常，引用这个类可以自动严格按照JSON语法规则（syntax rules）创建JSON text。每个JSONStringer实体只能对应创建一个JSON text。。其最大的优点在于可以减少由于格式的错误导致程序异常，引用这个类可以自动严格按照JSON语法规则（syntax rules）创建JSON text。每个JSONStringer实体只能对应创建一个JSON text。

JSONArray：它代表一组有序的数值。将其转换为String输出(toString)所表现的形式是用方括号包裹，数值以逗号”,”分隔（例如： [value1,value2,value3]，大家可以亲自利用简短的代码更加直观的了解其格式）。这个类的内部同样具有查询行为， get()和opt()两种方法都可以通过index索引返回指定的数值，put()方法用来添加或者替换数值。同样这个类的value类型可以包括：Boolean、JSONArray、JSONObject、Number、String或者默认值JSONObject.NULL object。

JSONTokener：json解析类

JSONException：json中用到的异常

JSONObject, JSONArray来构建json文本

代码

// 假设现在要创建这样一个json文本

// {

// "phone&#8221; : ["12345678&#8221;, "87654321&#8221;], // 数组

// "name&#8221; : "yuanzhifei89&#8221;, // 字符串

// "age&#8221; : 100, // 数值

// "address&#8221; : { "country&#8221; : "china&#8221;, "province&#8221; : "jiangsu&#8221; }, // 对象

// "married&#8221; : false // 布尔值

// }

try {

// 首先最外层是{}，是创建一个对象

JSONObject person = new JSONObject();

// 第一个键phone的值是数组，所以需要创建数组对象

JSONArray phone = new JSONArray();

phone.put("12345678&#8221;).put("87654321&#8221;);

person.put("phone&#8221;, phone);

person.put("name&#8221;, "yuanzhifei89&#8221;);

person.put("age&#8221;, 100);

// 键address的值是对象，所以又要创建一个对象

JSONObject address = new JSONObject();

address.put("country&#8221;, "china&#8221;);

address.put("province&#8221;, "jiangsu&#8221;);

person.put("address&#8221;, address);

person.put("married&#8221;, false);

} catch (JSONException ex) {

// 键为null或使用json不支持的数字格式(NaN, infinities)

throw new RuntimeException(ex);

}

getType和optType api的使用

getType可以将要获取的键的值转换为指定的类型，如果无法转换或没有值则抛出JSONException

optType也是将要获取的键的值转换为指定的类型，无法转换或没有值时返回用户提供或这默认提供的值

代码

try {

// 所有使用的对象都是用上面创建的对象

// 将第一个电话号码转换为数值和将名字转换为数值

phone.getLong(0);

person.getLong("name&#8221;); // 会抛异常，因为名字无法转换为long

phone.optLong(0); // 代码内置的默认值

phone.optLong(0, 1000); // 用户提供的默认值

person.optLong("name&#8221;);

person.optLong("name&#8221;, 1000); // 不像上面那样抛异常，而是返回1000

} catch (JSONException ex) {

// 异常处理代码

}

除了上面的两个类，还可以使用JSONStringer来构建json文本

Java代码

try {

JSONStringer jsonText = new JSONStringer();

// 首先是{，对象开始。object和endObject必须配对使用

jsonText.object();

jsonText.key("phone&#8221;);

// 键phone的值是数组。array和endArray必须配对使用

jsonText.array();

jsonText.value("12345678&#8221;).value("87654321&#8221;);

jsonText.endArray();

jsonText.key("name&#8221;);

jsonText.value("yuanzhifei89&#8221;);

jsonText.key("age&#8221;);

jsonText.value(100);

jsonText.key("address&#8221;);

// 键address的值是对象

jsonText.object();

jsonText.key("country&#8221;);

jsonText.value("china&#8221;);

jsonText.key("province&#8221;);

jsonText.value("jiangsu&#8221;);

jsonText.endObject();

jsonText.key("married&#8221;);

jsonText.value(false);

// }，对象结束

jsonText.endObject();

} catch (JSONException ex) {

throw new RuntimeException(ex);

}

json文本解析类JSONTokener

按照RFC4627规范将json文本解析为相应的对象。

对于将json文本解析为对象，只需要用到该类的两个api：

构造函数

public Object nextValue();

代码

// {

// "phone&#8221; : ["12345678&#8221;, "87654321&#8221;], // 数组

// "name&#8221; : "yuanzhifei89&#8221;, // 字符串

// "age&#8221; : 100, // 数值

// "address&#8221; : { "country&#8221; : "china&#8221;, "province&#8221; : "jiangsu&#8221; }, // 对象

// "married&#8221; : false // 布尔值

// }

private static final String JSON =

"{&#8221; +

&#8221; "phone&#8221; : ["12345678&#8221;, "87654321&#8221;],&#8221; +

&#8221; "name&#8221; : "yuanzhifei89",&#8221; +

&#8221; "age&#8221; : 100,&#8221; +

&#8221; "address&#8221; : { "country&#8221; : "china&#8221;, "province&#8221; : "jiangsu&#8221; },&#8221; +

&#8221; "married&#8221; : false,&#8221; +

"}&#8221;;

try {

JSONTokener jsonParser = new JSONTokener(JSON);

// 此时还未读取任何json文本，直接读取就是一个JSONObject对象。

// 如果此时的读取位置在&#8221;name&#8221; : 了，那么nextValue就是&#8221;yuanzhifei89"（String）

JSONObject person = (JSONObject) jsonParser.nextValue();

// 接下来的就是JSON对象的操作了

person.getJSONArray("phone&#8221;);

person.getString("name&#8221;);

person.getInt("age&#8221;);

person.getJSONObject("address&#8221;);

person.getBoolean("married&#8221;);

} catch (JSONException ex) {

// 异常处理代码

}

其它的api基本就是用来查看json文本中的文本的

代码

try {

JSONTokener jsonParser = new JSONTokener(JSON);

// 继续向下读8个json文本中的字符。此时刚开始，即在{处

jsonParser.next(8); //{ "phone。tab算一个字符

// 继续向下读1个json文本中的字符

jsonParser.next(); //&#8221;

// 继续向下读取一个json文本中的字符。该字符不是空白、同时也不是注视中的字符

jsonParser.nextClean(); //:

// 返回当前的读取位置到第一次遇到&#8217;a&#8217;之间的字符串（不包括a）。

jsonParser.nextString(&#8216;a&#8217;); // ["12345678&#8221;, "87654321&#8221;], "n（前面有两个空格）

// 返回当前读取位置到第一次遇到字符串中(如&#8221;0089&#8221;)任意字符之间的字符串，同时该字符是trimmed的。（此处就是第一次遇到了89）

jsonParser.nextTo("0089"); //me&#8221; : "yuanzhifei

// 读取位置撤销一个

jsonParser.back();

jsonParser.next(); //i

// 读取位置前进到指定字符串处（包括字符串）

jsonParser.skipPast("address&#8221;);

jsonParser.next(8); //&#8221; : { "c

// 读取位置前进到执行字符处（不包括字符）

jsonParser.skipTo(&#8216;m&#8217;);

jsonParser.next(8); //married&#8221;

} catch (JSONException ex) {

// 异常处理代码

}

以下是一个标准的JSON请求实现过程：

\[java\]\[/java\]

view plaincopy

HttpPost request = new HttpPost(url);

// 先封装一个 JSON 对象

JSONObject param = new JSONObject();

param.put("name&#8221;, "rarnu&#8221;);

param.put("password&#8221;, "123456&#8221;);

// 绑定到请求 Entry

StringEntity se = new StringEntity(param.toString());

request.setEntity(se);

// 发送请求

HttpResponse httpResponse = new DefaultHttpClient().execute(request);

// 得到应答的字符串，这也是一个 JSON 格式保存的数据

String retSrc = EntityUtils.toString(httpResponse.getEntity());

// 生成 JSON 对象

JSONObject result = new JSONObject( retSrc);

String token = result.get("token&#8221;);

下面这个是自己修改别人的小例子，主要是加一些注释和讲解，这个例子主要是使用android进行json解析。

\[html\]\[/html\]

view plaincopy

单数据{&#8216;singer&#8217;:{&#8216;id&#8217;:01,&#8217;name&#8217;:&#8217;tom&#8217;,&#8217;gender&#8217;:&#8217;男&#8217;}}

多个数据{"singers&#8221;:[

{&#8216;id&#8217;:02,&#8217;name&#8217;:&#8217;tom&#8217;,&#8217;gender&#8217;:&#8217;男&#8217;},

{&#8216;id&#8217;:03,&#8217;name&#8217;:&#8217;jerry,&#8217;gender&#8217;:&#8217;男&#8217;},

{&#8216;id&#8217;:04,&#8217;name&#8217;:&#8217;jim,&#8217;gender&#8217;:&#8217;男&#8217;},

{&#8216;id&#8217;:05,&#8217;name&#8217;:&#8217;lily,&#8217;gender&#8217;:&#8217;女&#8217;}]}

下面的类主要是解析单个数据parseJson（）和多个数据的方法parseJsonMulti（）:

\[java\]\[/java\]

view plaincopy

</pre><pre name=&#8221;code&#8221; class=&#8221;java&#8221; style=&#8221;text-align: left; font-family: Monaco, &#8216;DejaVu Sans Mono&#8217;, &#8216;Bitstream Vera Sans Mono&#8217;, Consolas, &#8216;Courier New&#8217;, monospace; line-height: 18px; ">public class JsonActivity extends Activity {

/*\* Called when the activity is first created. \*/

private TextView tvJson;

private Button btnJson;

private Button btnJsonMulti;

@Override

public void onCreate(Bundle savedInstanceState) {

super.onCreate(savedInstanceState);

setContentView(R.layout.main);

tvJson = (TextView) this.findViewById(R.id.tvJson);

btnJson = (Button) this.findViewById(R.id.btnJson);

btnJsonMulti = (Button) this.findViewById(R.id.btnJsonMulti);

btnJson.setOnClickListener(new View.OnClickListener() {

@Override

public void onClick(View v) {

// url

// String strUrl = "http://10.158.166.110:8080/AndroidServer/JsonServlet&#8221;;

String strUrl = ServerPageUtil.getStrUrl(UrlsOfServer.JSON_SINGER);

//获得返回的Json字符串

String strResult = connServerForResult(strUrl);

//解析Json字符串

parseJson(strResult);

}

});

btnJsonMulti.setOnClickListener(new View.OnClickListener() {

@Override

public void onClick(View v) {

String strUrl = ServerPageUtil.getStrUrl(UrlsOfServer.JSON_SINGERS);

String strResult = connServerForResult(strUrl);

//获得多个Singer

parseJsonMulti(strResult);

}

});

}

private String connServerForResult(String strUrl) {

// HttpGet对象

HttpGet httpRequest = new HttpGet(strUrl);

String strResult = "&#8221;;

try {

// HttpClient对象

HttpClient httpClient = new DefaultHttpClient();

// 获得HttpResponse对象

HttpResponse httpResponse = httpClient.execute(httpRequest);

if (httpResponse.getStatusLine().getStatusCode() == HttpStatus.SC_OK) {

// 取得返回的数据

strResult = EntityUtils.toString(httpResponse.getEntity());

}

} catch (ClientProtocolException e) {

tvJson.setText("protocol error&#8221;);

e.printStackTrace();

} catch (IOException e) {

tvJson.setText("IO error&#8221;);

e.printStackTrace();

}

return strResult;

}

// 普通Json数据解析

private void parseJson(String strResult) {

try {

JSONObject jsonObj = new JSONObject(strResult).getJSONObject("singer&#8221;);

int id = jsonObj.getInt("id&#8221;);

String name = jsonObj.getString("name&#8221;);

String gender = jsonObj.getString("gender&#8221;);

tvJson.setText("ID号&#8221;+id + ", 姓名：&#8221; + name + ",性别：&#8221; + gender);

} catch (JSONException e) {

System.out.println("Json parse error&#8221;);

e.printStackTrace();

}

}

//解析多个数据的Json

private void parseJsonMulti(String strResult) {

try {

JSONArray jsonObjs = new JSONObject(strResult).getJSONArray("singers&#8221;);

String s = "&#8221;;

for(int i = 0; i < jsonObjs.length() ; i++){

JSONObject jsonObj = ((JSONObject)jsonObjs.opt(i))

.getJSONObject("singer&#8221;);

int id = jsonObj.getInt("id&#8221;);

String name = jsonObj.getString("name&#8221;);

String gender = jsonObj.getString("gender&#8221;);

s += "ID号&#8221;+id + ", 姓名：&#8221; + name + ",性别：&#8221; + gender+ "n&#8221; ;

}

tvJson.setText(s);

} catch (JSONException e) {

System.out.println("Jsons parse error !&#8221;);

e.printStackTrace();

}

}