---
title: jquery validation
author: "-"
date: 2013-01-30T12:12:48+00:00
url: /?p=5091
categories:
  - Web

tags:
  - reprint
---
## jquery validation
**jQuery验证框架** **六、框架内建的验证方法( List of built-in Validation methods )** **[1]  required( ) **      返回: Boolean 说明: 让表单元素必须填写 (选择) 。 如果表单元素为空(text input)或未选择(radio/checkbox)或选择了一个空值(select)。 作用于text inputs, selects, checkboxes and radio buttons. 当select提供了一个空值选项<option value="">Choose...</option>则强迫用户去选择一个不为空的值。
  
    
      Js代码
  
  
  
    
      $("#myform").validate({
    
    
        rules: {
    
    
          fruit: "required"
    
    
        }
    
    
      });
    
  

**[2]  required( dependency-expression ) **      返回: Boolean 参数 dependency-expression     类型: String    在form上下文中的一个表达式( String ),表单元素是否需要填写依赖于该表达式返回一个或多个元素。 说明: 让表单元素必须填写 (选择) ,依赖于参数的返回值。 表达式中像#foo:checked, #foo:filled, #foo:visible这样的选择过滤器将经常用到。
  
    
      Js代码
  
  
  
    
      $("#myform").validate({
    
    
        rules: {
    
    
          details: {
    
    
            required: "#other:checked"
    
    
          }
    
    
        }, debug:true
    
    
      });
    
    
      $("#other").click(function() {
    
    
         $("#details").valid();
    
    
      });
    
  

**[3]  required( dependency-callback ) **      返回: Boolean 参数 dependency-callback     类型: Callback   该回函数以待验证表单元素作为其唯一的参数。当该回调函数返回true,则该表单元素是必须的。 说明: 让表单元素必须填写 (选择) ,依赖于参数的返回值。 表达式中像#foo:checked, #foo:filled, #foo:visible这样的选择过滤器将经常用到。
  
    
      Js代码
  
  
  
    
      $("#myform").validate({
    
    
        rules: {
    
    
          age: {
    
    
            required: true,
    
    
            min: 3
    
    
          },
    
    
          parent: {
    
    
            required: function(element) {
    
    
              return $("#age").val() < 13;
    
    
            }
    
    
          }
    
    
        }
    
    
      });
    
    
      $("#age").blur(function() {
    
    
          $("#parent").valid();
    
    
      });
    
  

**[4]  remote( options ) **      返回: Boolean 参数 options      类型: String, Options    请求服务器端资源的url(String)。或$.ajax()方法中的选项(Options)。 说明: 请求服务器端资源验证。 服务器端的资源通过$.ajax (XMLHttpRequest)获取key/value对,响应返回true则表单通过验证。
  
    
      Js代码
  
  
  
    
      $("#myform").validate({
    
    
        rules: {
    
    
          email: {
    
    
            required: true,
    
    
            email: true,
    
    
            remote: "check-email.php"
    
    
          }
    
    
        }
    
    
      });
    
  

**[5]  minlength( length ) **      返回: Boolean 参数 length      类型: Integer    至少需要多少个字符数。 说明: 确保表单元素满足给定的最小字符数。 在文本框(text input)中输入的字符太少、没有选中足够的复选框(checkbox)、一个选择框(select)中没有选中足够的选项。这以上三种情况中该方法返回false。
  
    
      Js代码
  
  
  
    
      $("#myform").validate({
    
    
        rules: {
    
    
          field: {
    
    
            required: true,
    
    
            minlength: 3
    
    
          }
    
    
        }
    
    
      });
    
  

**[6]  maxlength( length ) **      返回: Boolean 参数 length      类型: Integer    允许输入的最大字符数。 说明: 确保表单元素的文本不超过给定的最大字符数。 在文本框(text input)中输入的字符太多、选择太多的复选框(checkbox)、一个选择框(select)中没有选中太多的选项。这以上三种情况中该方法返回false。
  
    
      Js代码
  
  
  
    
      $("#myform").validate({
    
    
        rules: {
    
    
          field: {
    
    
            required: true,
    
    
            maxlength: 4
    
    
          }
    
    
        }
    
    
      });
    
  

**[7]  rangelength( range ) **      返回: Boolean 参数 range      类型: Array<integer>    允许输入的字符数范围。 说明: 确保表单元素的文本字符数在给定的范围当中。 在文本框(text input)中输入的字符数不在给定范围内、选择的复选框(checkbox)不在给在的范围内、一个选择框(select)选中的选项不在给定的范围内。这以上三种情况中该方法返回false。
  
    
      Js代码
  
  
  
    
      $("#myform").validate({
    
    
        rules: {
    
    
          field: {
    
    
            required: true,
    
    
            rangelength: [2, 6]
    
    
          }
    
    
        }
    
    
      });
    
  

**[8]  min( value ) **      返回: Boolean 参数 value      类型: Integer    需要输入的最小整数。 说明: 确保表单元素的值大于等于给定的最小整数。 该方法只在文本输入框(text input)下有效。
  
    
      Js代码
  
  
  
    
      $("#myform").validate({
    
    
        rules: {
    
    
          field: {
    
    
            required: true,
    
    
            min: 13
    
    
          }
    
    
        }
    
    
      });
    
  

**[9]  max( value ) **      返回: Boolean 参数 value      类型: Integer    给定的最大整数。 说明: 确保表单元素的值小于等于给定的最大整数。 该方法只在文本输入框(text input)下有效。
  
    
      Js代码
  
  
  
    
      $("#myform").validate({
    
    
        rules: {
    
    
          field: {
    
    
            required: true,
    
    
            max: 23
    
    
          }
    
    
        }
    
    
      });
    
  

**[10]  range( range ) **      返回: Boolean 参数 range     类型: Array<integer>    给定的整数范围。 说明: 确保表单元素的值在给定的范围当中。 该方法只在文本输入框(text input)下有效。
  
    
      Js代码
  
  
  
    
      $("#myform").validate({
    
    
        rules: {
    
    
          field: {
    
    
            required: true,
    
    
            range: [13, 23]
    
    
          }
    
    
        }
    
    
      });
    
  

**[11]  email( ) **      返回: Boolean 说明: 确保表单元素的值为一个有效的email地址。 如果值为一个有效的email地址,则返回true。该方法只在文本输入框(text input)下有效。
  
    
      Js代码
  
  
  
    
      $("#myform").validate({
    
    
        rules: {
    
    
          field: {
    
    
            required: true,
    
    
            email: true
    
    
          }
    
    
        }
    
    
      });
    
  

**[12]  url( ) **      返回: Boolean 说明: 确保表单元素的值为一个有效的URL地址(http://www.mydomain.com)。 如果值为一个有效的url地址,则返回true。该方法只在文本输入框(text input)下有效。
  
    
      Js代码
  
  
  
    
      $("#myform").validate({
    
    
        rules: {
    
    
          field: {
    
    
            required: true,
    
    
            url: true
    
    
          }
    
    
        }
    
    
      });
    
  

**[13]  date( )  dateISO( )  dateDE( )**      返回: Boolean 说明: 用来验证有效的日期。这三个函数分别验证的日期格式为(mm/dd/yyyy)、(yyyy-mm-dd,yyyy/mm/dd)、(mm.dd.yyyy)。
  
    
      Js代码
  
  
  
    
      $("#myform").validate({
    
    
        rules: {
    
    
          field: {
    
    
            required: true,
    
    
            date: true
    
    
            /*dateISO: true
    
    
              dateDE: true*/
    
    
          }
    
    
        }
    
    
      });
    
  

**[14]  number( )  numberDE()**      返回: Boolean 说明: 用来验证小数。number()的小数点为圆点( . ),numberDE()的小数点为英文逗号( , )。
  
    
      Js代码
  
  
  
    
      $("#myform").validate({
    
    
        rules: {
    
    
          field: {
    
    
            required: true,
    
    
            number: true
    
    
            //numberDE: true
    
    
          }
    
    
        }
    
    
      });
    
  

**[15]  digits()**      返回: Boolean 说明: 确保文本框中的值为数字。
  
    
      Js代码
  
  
  
    
      $("#myform").validate({
    
    
        rules: {
    
    
          field: {
    
    
            required: true,
    
    
            digits: true
    
    
          }
    
    
        }
    
    
      });
    
  

**[16]  digits()**      返回: Boolean 说明: 确保文本框中的值为数字。
  
    
      Js代码
  
  
  
    
      $("#myform").validate({
    
    
        rules: {
    
    
          field: {
    
    
            required: true,
    
    
            digits: true
    
    
          }
    
    
        }
    
    
      });
    
  

**[17]  accept( [extension] ) **      返回: Boolean 参数 extension(Optional)     类型: String    允许的文件后缀名,用"|"或","分割。默认为"png|jpe?g|gif" 说明: 确保表单元素接收给定的文件后缀名的文件。如果没有指定参数,则只有图片是允许的(png,jpeg,gif)。
  
    
      Js代码
  
  
  
    
      $("#myform").validate({
    
    
        rules: {
    
    
          field: {
    
    
            required: true,
    
    
            accept: "xls|csv"
    
    
          }
    
    
        }
    
    
      });
    
  

**[18]  equalTo( other ) **      返回: Boolean 参数 other      类型: Selector    要与当前值比较的另一个表单元素。 说明: 确保两个表单元素的值是一致的。
  
    
      Js代码
  
  
  
    
      $("#myform").validate({
    
    
        rules: {
    
    
          password: "required",
    
    
          password_again: {
    
    
            equalTo: "#password"
    
    
          }
    
    
        }
    
    
      });
    
  

$("#aspnetForm").validate({ ignore: "",  
rules: {

check the fields which attr display is none.

// 验证值小数位数不能超过两位
  
jQuery.validator.addMethod("decimal", function(value, element) {
  
var decimal = /^-?d+(&#46;d{1,2})?$/;
  
return this.optional(element) || (decimal.test(value));
  
}, $.validator.format("小数位数不能超过两位!"));