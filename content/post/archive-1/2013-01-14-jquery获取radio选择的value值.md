---
title: 'jQuery获取Radio选择的Value值:'
author: wiloon
type: post
date: 2013-01-14T05:31:27+00:00
url: /?p=5015
categories:
  - Web

---
http://www.cnblogs.com/tangself/archive/2010/04/14/1711684.html

jQuery获取Radio选择的Value值:

var\_name = $(“input[name=&#8217;radio\_name&#8217;]:checked”).val();

1. $("input\[name=&#8217;radio_name&#8217;\]\[checked\]&#8221;).val();  //选择被选中Radio的Value值
  
2. $("#text\_id&#8221;).focus(function(){//code&#8230;});  //事件 当对象text\_id获取焦点时触发
  
3. $("#text\_id&#8221;).blur(function(){//code&#8230;});  //事件 当对象text\_id失去焦点时触发
  
4. $("#text_id&#8221;).select();  //使文本框的Vlaue值成选中状态
  
5. $("input\[name=&#8217;radio_name&#8217;\]\[value=&#8217;要中Radio的Value值&#8217;\]&#8221;).attr("checked&#8221;,true);   jQuery获取CheckBox选择的Value

语法解释：
  
1. $("input\[name=&#8217;checkbox_name&#8217;\]\[checked\]&#8221;);  //选择被选中CheckBox元素的集合 如果你想得到Value值，你需要遍历
  
2. $($("input\[name=&#8217;checkbox_name&#8217;\]\[checked\]&#8221;)).each(function(){arrChk+=this.value + &#8216;,&#8217;;});  //遍历被选中CheckBox元素的集合 得到Value值
  
3. $("#checkbox_id&#8221;).attr("checked&#8221;);  //获取一个CheckBox的状态(有没有被选中,返回true/false)
  
4. $("#checkbox_id&#8221;).attr("checked&#8221;,true);  //设置一个CheckBox的状态为选中(checked=true)
  
5. $("#checkbox_id&#8221;).attr("checked&#8221;,false);  //设置一个CheckBox的状态为不选中(checked=false)
  
6. $("input[name=&#8217;checkbox\_name&#8217;]&#8221;).attr("checked&#8221;,$("#checkbox\_id&#8221;).attr("checked&#8221;));

7. $("#text_id&#8221;).val().split(",&#8221;);  //将Text的Value值以&#8217;,&#8217;分隔 返回一个数组

<a href="http://www.cnblogs.com/bynet/archive/2009/11/13/1602491.html" target="_blank">jQuery&#8211;checkbox全选/取消全选</a>

用JavaScript使页面上的一组checkbox全选/取消全选，逻辑很简单，实现代码也没有太难的语法。但使用jQuery实现则更简单，代码也很简洁，精辟！
  
<input type=&#8221;checkbox&#8221; name=&#8221;chk\_list&#8221; id=&#8221;chk\_list_1" value=&#8221;1" />1<br />
  
<input type=&#8221;checkbox&#8221; name=&#8221;chk\_list&#8221; id=&#8221;chk\_list_2" value=&#8221;2" />2<br />
  
<input type=&#8221;checkbox&#8221; name=&#8221;chk\_list&#8221; id=&#8221;chk\_list_3" value=&#8221;3" />3<br />
  
<input type=&#8221;checkbox&#8221; name=&#8221;chk\_list&#8221; id=&#8221;chk\_list_4" value=&#8221;4" />4<br />
  
<input type=&#8221;checkbox&#8221; name=&#8221;chk\_all&#8221; id=&#8221;chk\_all&#8221; />全选/取消全选
  
<script type=&#8221;text/javascript&#8221;>

$("#chk\_all&#8221;).click(function() {  $("input[name=&#8217;chk\_list&#8217;]&#8221;).attr("checked&#8221;,$(this).attr("checked&#8221;));});
  
</script>

jQuery.attr  获取/设置对象的属性值,如：

$("input[name=&#8217;chk\_list&#8217;]&#8221;).attr("checked&#8221;);     //读取所有name为&#8217;chk\_list&#8217;对象的状态（是否选中）

$("input[name=&#8217;chk\_list&#8217;]&#8221;).attr("checked&#8221;,true);      //设置所有name为&#8217;chk\_list&#8217;对象的checked为true

再如：

$("#img\_1&#8221;).attr("src&#8221;,&#8221;test.jpg&#8221;);    //设置ID为img\_1的<img>src的值为&#8217;test.jpg&#8217;
  
$("#img\_1&#8221;).attr("src&#8221;);     //读取ID为img\_1的<img>src值

下面的代码是获取上面实例中选中的checkbox的value值:
  
<script type=&#8221;text/javascript&#8221;> //获取到所有name为&#8217;chk_list&#8217;并选中的checkbox(集合)

var arrChk=$("input[name=&#8217;chk_list]:checked&#8221;);    //遍历得到每个checkbox的value值

for (var i=0;i<arrChk.length;i++){     alert(arrChk[i].value); }
  
</script>

<script type=&#8221;text/javascript&#8221;>

var arrChk=$("input[name=&#8217;chk_list&#8217;]:checked&#8221;); $(arrChk).each(function() {   window.alert(this.value);  }); });</script>

<a href="http://www.cnblogs.com/bynet/archive/2009/11/16/1603769.html" target="_blank">jQuery-对Select的操作集合[终结篇]</a>

jQuery获取Select选择的Text和Value:

语法解释：
  
1. $("#select_id&#8221;).change(function(){//code&#8230;});   //为Select添加事件，当选择其中一项时触发
  
2. var checkText=$("#select_id&#8221;).find("option:selected&#8221;).text();  //获取Select选择的Text
  
3. var checkValue=$("#select_id&#8221;).val();  //获取Select选择的Value
  
4. var checkIndex=$("#select_id ").get(0).selectedIndex;  //获取Select选择的索引值
  
5. var maxIndex=$("#select_id option:last&#8221;).attr("index&#8221;);  //获取Select最大的索引值
  
jQuery设置Select选择的Text和Value:
  
语法解释：
  
1. $("#select_id ").get(0).selectedIndex=1;  //设置Select索引值为1的项选中
  
2. $("#select_id ").val(4);   //设置Select的Value值为4的项选中
  
3. $("#select_id option

\[text language=&#8221;jQuery&#8221;\]\[/text\]

").attr("selected&#8221;, true);   //设置Select的Text值为jQuery的项选中

jQuery添加/删除Select的Option项：

点击一次，Select将追加一个Option
  
点击将在Select第一个位置插入一个Option
  
点击将删除Select中索引值最大Option(最后一个)
  
1. $("#select_id&#8221;).append("<option value='Value'>Text</option>");  //为Select追加一个Option(下拉项)
  
2. $("#select_id&#8221;).prepend("<option value='0'>请选择</option>");  //为Select插入一个Option(第一个位置)
  
3. $("#select_id option:last&#8221;).remove();  //删除Select中索引值最大Option(最后一个)
  
4. $("#select_id option[index=&#8217;0&#8242;]&#8221;).remove();  //删除Select中索引值为0的Option(第一个)
  
5. $("#select_id option[value=&#8217;3&#8242;]&#8221;).remove();  //删除Select中Value=&#8217;3&#8217;的Option
  
5. $("#select_id option

\[text language=&#8221;4&#8221;\]\[/text\]

").remove();  //删除Select中Text=&#8217;4&#8217;的Option

<a href="http://www.cnblogs.com/top5/archive/2009/11/12/1601543.html" target="_blank">JQUERY获取text,areatext,radio,checkbox,select值</a>

jquery radio取值，checkbox取值，select取值，radio选中，checkbox选中，select选中，及其相关
  
获取一组radio被选中项的值
  
var item = $(&#8216;input\[@name=items\]\[@checked\]&#8217;).val();
  
获取select被选中项的文本
  
var item = $("select[@name=items] option[@selected]&#8221;).text();
  
select下拉框的第二个元素为当前选中值
  
$(&#8216;#select_id&#8217;)[0].selectedIndex = 1;
  
radio单选组的第二个元素为当前选中值
  
$(&#8216;input[@name=items]&#8217;).get(1).checked = true;
  
获取值：
  
文本框，文本区域：$("#txt&#8221;).attr("value&#8221;)；
  
多选框checkbox：$("#checkbox_id&#8221;).attr("value&#8221;)；
  
单选组radio：   $("input\[@type=radio\]\[@checked\]&#8221;).val();
  
下拉框select： $(&#8216;#sel&#8217;).val();
  
控制表单元素：
  
文本框，文本区域：$("#txt&#8221;).attr("value&#8221;,&#8221;);//清空内容
  
$("#txt&#8221;).attr("value&#8221;,&#8217;11&#8217;);//填充内容
  
多选框checkbox： $("#chk1&#8221;).attr("checked&#8221;,&#8221;);//不打勾
  
$("#chk2&#8221;).attr("checked&#8221;,true);//打勾
  
if($("#chk1&#8221;).attr(&#8216;checked&#8217;)==undefined) //判断是否已经打勾

单选组radio：    $("input[@type=radio]&#8221;).attr("checked&#8221;,&#8217;2&#8242;);//设置value=2的项目为当前选中项
  
下拉框select：   $("#sel&#8221;).attr("value&#8221;,&#8217;-sel3&#8242;);//设置value=-sel3的项目为当前选中项
  
$("<option value=&#8217;1&#8242;>1111</option><option value=&#8217;2&#8242;>2222</option>&#8221;).appendTo("#sel&#8221;)//添加下拉框的option
  
$("#sel&#8221;).empty()；//清空下拉框

&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;&#8212;-

//遍历option和添加、移除option
  
function changeShipMethod(shipping){
  
var len = $("select[@name=ISHIPTYPE] option&#8221;).length
  
if(shipping.value != "CA&#8221;){
  
$("select[@name=ISHIPTYPE] option&#8221;).each(function(){
  
if($(this).val() == 111){
  
$(this).remove();
  
}
  
});
  
}else{$("<option value=&#8217;111&#8242;>UPS Ground</option>&#8221;).appendTo($("select[@name=ISHIPTYPE]&#8221;));}}
  
//取得下拉選單的選取值

$(#testSelect option:selected&#8217;).text();
  
或$("#testSelect&#8221;).find(&#8216;option:selected&#8217;).text();
  
或$("#testSelect&#8221;).val();
  
//////////////////////////////////////////////////////////////////
  
记性不好的可以收藏下：
  
1,下拉框:

var cc1 = $(".formc select[@name=&#8217;country&#8217;] option[@selected]&#8221;).text(); //得到下拉菜单的选中项的文本(注意中间有空格)
  
var cc2 = $(&#8216;.formc select[@name=&#8221;country&#8221;]&#8217;).val(); //得到下拉菜单的选中项的值
  
var cc3 = $(&#8216;.formc select[@name=&#8221;country&#8221;]&#8217;).attr("id&#8221;); //得到下拉菜单的选中项的ID属性值
  
$("#select&#8221;).empty();//清空下拉框//$("#select&#8221;).html(&#8221;);
  
$("<option value=&#8217;1&#8242;>1111</option>&#8221;).appendTo("#select&#8221;)//添加下拉框的option

稍微解释一下:
  
1.select[@name=&#8217;country&#8217;] option[@selected] 表示具有name 属性，
  
并且该属性值为&#8217;country&#8217; 的select元素 里面的具有selected 属性的option 元素；
  
可以看出有@开头的就表示后面跟的是属性。

2,单选框:
  
$("input\[@type=radio\]\[@checked\]&#8221;).val(); //得到单选框的选中项的值(注意中间没有空格)
  
$("input\[@type=radio\]\[@value=2\]&#8221;).attr("checked&#8221;,&#8217;checked&#8217;); //设置单选框value=2的为选中状态.(注意中间没有空格)

3,复选框:
  
$("input\[@type=checkbox\]\[@checked\]&#8221;).val(); //得到复选框的选中的第一项的值
  
$("input\[@type=checkbox\]\[@checked\]&#8221;).each(function(){ //由于复选框一般选中的是多个,所以可以循环输出
  
alert($(this).val());
  
});

$("#chk1&#8221;).attr("checked&#8221;,&#8221;);//不打勾
  
$("#chk2&#8221;).attr("checked&#8221;,true);//打勾
  
if($("#chk1").attr(&#8216;checked&#8217;)==undefined){} //判断是否已经打勾
  
当然jquery的选择器是强大的. 还有很多方法.

<script src=&#8221;jquery-1.2.1.js&#8221; type=&#8221;text/javascript&#8221;></script>
  
<script language=&#8221;javascript&#8221; type=&#8221;text/javascript&#8221;>
  
$(document).ready(function(){
  
$("#selectTest&#8221;).change(function()
  
{//alert("Hello&#8221;);//alert($("#selectTest&#8221;).attr("name&#8221;));//$("a&#8221;).attr("href&#8221;,&#8221;xx.html&#8221;);//window.location.href=&#8221;xx.html&#8221;;
  
//alert($("#selectTest&#8221;).val());
  
alert($("#selectTest option[@selected]&#8221;).text());
  
$("#selectTest&#8221;).attr("value&#8221;, "2&#8221;);

});
  
});
  
</script>
  
<a href=&#8221;#&#8221;>aaass</a>

<!&#8211;下拉框&#8211;>
  
<select id=&#8221;selectTest&#8221; name=&#8221;selectTest&#8221;>
  
<option value=&#8221;1">11</option><option value=&#8221;2">22</option><option value=&#8221;3">33</option>
  
<option value=&#8221;4">44</option><option value=&#8221;5">55</option><option value=&#8221;6">66</option>
  
</select>
  
jquery radio取值，checkbox取值，select取值，radio选中，checkbox选中，select选中，及其相关获取一组radio被选中项的值
  
var item = $(&#8216;input\[@name=items\]\[@checked\]&#8217;).val();
  
获取select被选中项的文本
  
var item = $("select[@name=items] option[@selected]&#8221;).text();
  
select下拉框的第二个元素为当前选中值
  
$(&#8216;#select_id&#8217;)[0].selectedIndex = 1;
  
radio单选组的第二个元素为当前选中值
  
$(&#8216;input[@name=items]&#8217;).get(1).checked = true;
  
获取值：
  
文本框，文本区域：$("#txt&#8221;).attr("value&#8221;)；
  
多选框checkbox：$("#checkbox_id&#8221;).attr("value&#8221;)；
  
单选组radio： $("input\[@type=radio\]\[@checked\]&#8221;).val();
  
下拉框select： $(&#8216;#sel&#8217;).val();
  
控制表单元素：
  
文本框，文本区域：$("#txt&#8221;).attr("value&#8221;,&#8221;);//清空内容
  
$("#txt&#8221;).attr("value&#8221;,&#8217;11&#8217;);//填充内容
  
多选框checkbox： $("#chk1&#8221;).attr("checked&#8221;,&#8221;);//不打勾
  
$("#chk2&#8221;).attr("checked&#8221;,true);//打勾
  
if($("#chk1&#8221;).attr(&#8216;checked&#8217;)==undefined) //判断是否已经打勾
  
单选组radio： $("input[@type=radio]&#8221;).attr("checked&#8221;,&#8217;2&#8242;);//设置value=2的项目为当前选中项
  
下拉框select： $("#sel&#8221;).attr("value&#8221;,&#8217;-sel3&#8242;);//设置value=-sel3的项目为当前选中项
  
$("<optionvalue=&#8217;1&#8242;>1111</option><optionvalue=&#8217;2&#8242;>2222</option>&#8221;).appendTo("#sel&#8221;)//添加下拉框的option
  
$("#sel&#8221;).empty()；//清空下拉框

获取一组radio被选中项的值
  
var item = $(&#8216;input\[@name=items\]\[@checked\]&#8217;).val();
  
获取select被选中项的文本
  
var item = $("select[@name=items] option[@selected]&#8221;).text();
  
select下拉框的第二个元素为当前选中值
  
$(&#8216;#select_id&#8217;)[0].selectedIndex = 1;
  
radio单选组的第二个元素为当前选中值
  
$(&#8216;input[@name=items]&#8217;).get(1).checked = true;
  
获取值：
  
文本框，文本区域：$("#txt&#8221;).attr("value&#8221;)；
  
多选框checkbox：$("#checkbox_id&#8221;).attr("value&#8221;)；
  
单选组radio： $("input\[@type=radio\]\[@checked\]&#8221;).val();
  
下拉框select： $(&#8216;#sel&#8217;).val();
  
控制表单元素：
  
文本框，文本区域：$("#txt&#8221;).attr("value&#8221;,&#8221;);//清空内容
  
$("#txt&#8221;).attr("value&#8221;,&#8217;11&#8217;);//填充内容
  
多选框checkbox： $("#chk1&#8221;).attr("checked&#8221;,&#8221;);//不打勾
  
$("#chk2&#8221;).attr("checked&#8221;,true);//打勾
  
if($("#chk1&#8221;).attr(&#8216;checked&#8217;)==undefined) //判断是否已经打勾
  
单选组radio： $("input[@type=radio]&#8221;).attr("checked&#8221;,&#8217;2&#8242;);//设置value=2的项目为当前选中项
  
下拉框select： $("#sel&#8221;).attr("value&#8221;,&#8217;-sel3&#8242;);//设置value=-sel3的项目为当前选中项
  
$("<option value=&#8217;1&#8242;>1111</option><option value=&#8217;2&#8242;>2222</option>&#8221;).appendTo("#sel&#8221;)//添加下拉框的option
  
$("#sel&#8221;).empty()；//清空下拉框

<a href="http://www.cnblogs.com/greatverve/archive/2010/02/03/1662565.html" target="_blank">jQuery取得select选中的值</a>

记录一下。

本来以为jQuery("#select1&#8221;).val();是取得选中的值，

那么jQuery("#select1&#8221;).text();就是取得的文本。

这是不正确的，正确做法是：

jQuery("#select1  option:selected&#8221;).text();

**<a href="http://www.cnblogs.com/top5/archive/2009/11/12/1601675.html" target="_blank">两个select之间option的互相添加操作(jquery实现)</a>**

两个select,将其中一个select选中的选项添加到另一个select中,或者点击全部添加按钮将所有的option都添加过去.
  
自己写了一个很简单的jquery插件,在页面中调用其中的函数就可实现.
  
插件源代码(listtolist.js):

Js代码

/**

fromid:源list的id.

toid:目标list的id.

moveOrAppend参数("move&#8221;或者是&#8221;append&#8221;):

move &#8212; 源list中选中的option会删除.源list中选中的option移动到目标list中,若目标list中已存在则该option不添加.

append &#8212; 源list中选中的option不会删除.源list中选中的option添加到目标list的后面,若目标list中已存在则该option不添加.

isAll参数(true或者false):是否全部移动或添加

*/

jQuery.listTolist = function(fromid,toid,moveOrAppend,isAll) {

if(moveOrAppend.toLowerCase() == "move&#8221;) {  //移动

if(isAll == true) { //全部移动

$("#&#8221;+fromid+&#8221; option&#8221;).each(function() {

//将源list中的option添加到目标list,当目标list中已有该option时不做任何操作.

$(this).appendTo($("#&#8221;+toid+&#8221;:not(:has(option[value=&#8221;+$(this).val()+&#8221;]))&#8221;));

});

$("#&#8221;+fromid).empty();  //清空源list

}

else if(isAll == false) {

$("#&#8221;+fromid+&#8221; option:selected&#8221;).each(function() {

//将源list中的option添加到目标list,当目标list中已有该option时不做任何操作.

$(this).appendTo($("#&#8221;+toid+&#8221;:not(:has(option[value=&#8221;+$(this).val()+&#8221;]))&#8221;));

//目标list中已经存在的option并没有移动,仍旧在源list中,将其清空.

if($("#&#8221;+fromid+&#8221; option[value=&#8221;+$(this).val()+&#8221;]&#8221;).length > 0) {

$("#&#8221;+fromid).get(0)

.removeChild($("#&#8221;+fromid+&#8221; option[value=&#8221;+$(this).val()+&#8221;]&#8221;).get(0));

}

});

}

}

else if(moveOrAppend.toLowerCase() == "append&#8221;) {

if(isAll == true) {

$("#&#8221;+fromid+&#8221; option&#8221;).each(function() {

$("<option></option>&#8221;)

.val($(this).val())

.text($(this).text())

.appendTo($("#&#8221;+toid+&#8221;:not(:has(option[value=&#8221;+$(this).val()+&#8221;]))&#8221;));

});

}

else if(isAll == false) {

$("#&#8221;+fromid+&#8221; option:selected&#8221;).each(function() {

$("<option></option>&#8221;)

.val($(this).val())

.text($(this).text())

.appendTo($("#&#8221;+toid+&#8221;:not(:has(option[value=&#8221;+$(this).val()+&#8221;]))&#8221;));

});

}

}

};

/**

功能大体同上("move&#8221;).

不同之处在于当源list中的选中option在目标list中存在时,源list中的option不会删除.

isAll参数(true或者false):是否全部移动或添加

*/

jQuery.list2list = function(fromid,toid,isAll) {

if(isAll == true) {

$("#&#8221;+fromid+&#8221; option&#8221;).each(function() {

$(this).appendTo($("#&#8221;+toid+&#8221;:not(:has(option[value=&#8221;+$(this).val()+&#8221;]))&#8221;));

});

}

else if(isAll == false) {

$("#&#8221;+fromid+&#8221; option:selected&#8221;).each(function() {

$(this).appendTo($("#&#8221;+toid+&#8221;:not(:has(option[value=&#8221;+$(this).val()+&#8221;]))&#8221;));

});

}

};

<script type=&#8221;text/javascript&#8221;>
  
jQuery(function($)
  
{         //获取select文本和值
  
$("#submitBut&#8221;).click(function(){     //注意空格
  
//var strText = $("select[@name=fselect] option[@selected]&#8221;).text();
  
// var strValue = $("select[@name=fselect] option[@selected]&#8221;).val();
  
//alert(strText + ":&#8221; + strValue);
  
//选中值为t3项
  
$("#fselect&#8221;).attr("value&#8221;, "t3&#8221;);     //选中第二项
  
$(&#8216;#fselect&#8217;)[0].selectedIndex = 1;
  
alert($("#fselect&#8221;)[0].length);
  
});
  
//select改变时获取当前选项的值和文本
  
$("#fselect&#8221;).change(function(){      //获取总的选项
  
//alert($(this)[0].length);
  
//获取的所有的文本       var strText = $(this).text();
  
//获取当前选中值     var strValue = $(this).val();
  
//alert(strText + ":&#8221; + strValue);
  
//选中值为t3项    //选中第二项
  
//$(this)[0].selectedIndex = 3;       //$(this).attr("value&#8221;, "t3&#8221;);       / /$("#fselect&#8221;)[0].options[2].selected = true;
  
//获得当前选中的文本
  
//显示索引为2的文本
  
var nCurrent = $(this)[0].selectedIndex;
  
alert($("#fselect&#8221;)[0].options[nCurrent].text);
  
alert(strValue);
  
});

//增加select
  
$("#add&#8221;).click(function(){
  
var nLength = $("#fselect&#8221;)[0].length;
  
var option = document.createElement("option&#8221;);;
  
option.text = "Text&#8221; + (nLength+1).toString();
  
option.value = "t&#8221; + (nLength+1).toString();
  
$("#fselect&#8221;)[0].options.add(option);
  
//$("#fselect&#8221;).addOption("Text&#8221; + (nLength+1).toString(), "t&#8221; + (nLength+1).toString(), true);
  
});            //清空select
  
$("#clear&#8221;).click(function(){
  
$("#fselect&#8221;).empty();
  
});       //清空一项
  
$("#remove&#8221;).click(function(){
  
var index = $("#fselect&#8221;)[0].selectedIndex;
  
//$("#fselect&#8221;)[0].remove(index);
  
$("#fselect&#8221;)[0].options[index] = null;
  
});
  
})
  
</script>

其他有关select的取值或赋值方式：
  
获取select被选中项的文本
  
var item = $("select[@name= stsoft] option[@selected]&#8221;).text();
  
select下拉框的第二个元素为当前选中值
  
$(&#8216;#stsoft&#8217;)[0].selectedIndex = 1;
  
获取value值
  
$(&#8216;#stsoft&#8217;).val();
  
设置value=1的项目为当前选中项
  
$("#stsoft&#8221;).attr("value&#8221;,“1”);
  
$(&#8216;#stsoft&#8217;).val(“1”);

Js代码

<p align="left">
  1.     /**


<p align="left">
  2.     fromid:源list的id.


<p align="left">
  3.     toid:目标list的id.


<p align="left">
  4.     moveOrAppend参数("move&#8221;或者是&#8221;append&#8221;):


<p align="left">
  5.     move &#8212; 源list中选中的option会删除.源list中选中的option移动到目标list中,若目标list中已存在则该option不添加.


<p align="left">
  6.     append &#8212; 源list中选中的option不会删除.源list中选中的option添加到目标list的后面,若目标list中已存在则该option不添加.


<p align="left">
  7.


<p align="left">
  8.     isAll参数(true或者false):是否全部移动或添加


<p align="left">
  9.     */


<p align="left">
  10. jQuery.listTolist = function(fromid,toid,moveOrAppend,isAll) {


<p align="left">
  11.     if(moveOrAppend.toLowerCase() == "move&#8221;) {  //移动


<p align="left">
  12.         if(isAll == true) { //全部移动


<p align="left">
  13.             $("#&#8221;+fromid+&#8221; option&#8221;).each(function() {


<p align="left">
  14.                 //将源list中的option添加到目标list,当目标list中已有该option时不做任何操作.


<p align="left">
  15.                 $(this).appendTo($("#&#8221;+toid+&#8221;:not(:has(option[value=&#8221;+$(this).val()+&#8221;]))&#8221;));


<p align="left">
  16.             });


<p align="left">
  17.             $("#&#8221;+fromid).empty();  //清空源list


<p align="left">
  18.         }


<p align="left">
  19.         else if(isAll == false) {


<p align="left">
  20.             $("#&#8221;+fromid+&#8221; option:selected&#8221;).each(function() {


<p align="left">
  21.                 //将源list中的option添加到目标list,当目标list中已有该option时不做任何操作.


<p align="left">
  22.                 $(this).appendTo($("#&#8221;+toid+&#8221;:not(:has(option[value=&#8221;+$(this).val()+&#8221;]))&#8221;));


<p align="left">
  23.                 //目标list中已经存在的option并没有移动,仍旧在源list中,将其清空.


<p align="left">
  24.                 if($("#&#8221;+fromid+&#8221; option[value=&#8221;+$(this).val()+&#8221;]&#8221;).length > 0) {


<p align="left">
  25.                     $("#&#8221;+fromid).get(0)


<p align="left">
  26.                     .removeChild($("#&#8221;+fromid+&#8221; option[value=&#8221;+$(this).val()+&#8221;]&#8221;).get(0));


<p align="left">
  27.                 }


<p align="left">
  28.             });


<p align="left">
  29.         }


<p align="left">
  30.     }


<p align="left">
  31.     else if(moveOrAppend.toLowerCase() == "append&#8221;) {


<p align="left">
  32.         if(isAll == true) {


<p align="left">
  33.             $("#&#8221;+fromid+&#8221; option&#8221;).each(function() {


<p align="left">
  34.                 $("<option></option>&#8221;)


<p align="left">
  35.                 .val($(this).val())


<p align="left">
  36.                 .text($(this).text())


<p align="left">
  37.                 .appendTo($("#&#8221;+toid+&#8221;:not(:has(option[value=&#8221;+$(this).val()+&#8221;]))&#8221;));


<p align="left">
  38.             });


<p align="left">
  39.         }


<p align="left">
  40.         else if(isAll == false) {


<p align="left">
  41.             $("#&#8221;+fromid+&#8221; option:selected&#8221;).each(function() {


<p align="left">
  42.                 $("<option></option>&#8221;)


<p align="left">
  43.                 .val($(this).val())


<p align="left">
  44.                 .text($(this).text())


<p align="left">
  45.                 .appendTo($("#&#8221;+toid+&#8221;:not(:has(option[value=&#8221;+$(this).val()+&#8221;]))&#8221;));


<p align="left">
  46.             });


<p align="left">
  47.         }


<p align="left">
  48.     }


<p align="left">
  49. };   /**


<p align="left">
  50. 功能大体同上("move&#8221;).


<p align="left">
  51. 不同之处在于当源list中的选中option在目标list中存在时,源list中的option不会删除.


<p align="left">
  52. isAll参数(true或者false):是否全部移动或添加


<p align="left">
  53. jQuery.list2list = function(fromid,toid,isAll) {


<p align="left">
  54.     if(isAll == true) {


<p align="left">
  55.         $("#&#8221;+fromid+&#8221; option&#8221;).each(function() {


<p align="left">
  56.             $(this).appendTo($("#&#8221;+toid+&#8221;:not(:has(option[value=&#8221;+$(this).val()+&#8221;]))&#8221;));


<p align="left">
  57.         });


<p align="left">
  58.     }


<p align="left">
  59.     else if(isAll == false) {


<p align="left">
  60.         $("#&#8221;+fromid+&#8221; option:selected&#8221;).each(function() {


<p align="left">
  61.             $(this).appendTo($("#&#8221;+toid+&#8221;:not(:has(option[value=&#8221;+$(this).val()+&#8221;]))&#8221;));


<p align="left">
  62.         });


<p align="left">
  63.     }


<p align="left">
  64. };


isAllif(isAll == true) { //$("#"+fromid+" option").each(function() {      //$(this).appendTo($("#"+toid+":not(:has(option[value="+$(this).val()+"]))"));     });     $("#"+fromid).empty(); //}    else if(isAll == false) {     $("#"+fromid+" option:selected").each(function() {      //$(this).appendTo($("#"+toid+":not(:has(option[value="+$(this).val()+"]))"));      //if($("#"+fromid+" option[value="+$(this).val()+"]").length &gt; 0) {       $("#"+fromid).get(0)       .removeChild($("#"+fromid+" option[value="+$(this).val()+"]").get(0));      }     });    }  }  else if(moveOrAppend.toLowerCase() == "append") {    if(isAll == true) {     $("#"+fromid+" option").each(function() {      $("&lt;option&gt;&lt;/option&gt;")      .val($(this).val())      .text($(this).text())      .appendTo($("#"+toid+":not(:has(option[value="+$(this).val()+"]))"));     });    }    else if(isAll == false) {     $("#"+fromid+" option:selected").each(function() {      $("&lt;option&gt;&lt;/option&gt;")      .val($(this).val())      .text($(this).text())      .appendTo($("#"+toid+":not(:has(option[value="+$(this).val()+"]))"));     });    }  } }; /** isAll$("#"+fromid+" option").each(function() {     $(this).appendTo($("#"+toid+":not(:has(option[value="+$(this).val()+"]))"));    });  }  else if(isAll == false) {    $("#"+fromid+" option:selected").each(function() {     $(this).appendTo($("#"+toid+":not(:has(option[value="+$(this).val()+"]))"));    });  } };