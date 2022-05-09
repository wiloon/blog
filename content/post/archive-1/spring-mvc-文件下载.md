---
title: Spring MVC 文件下载
author: "-"
date: 2014-02-26T05:57:21+00:00
url: /?p=6289
categories:
  - Inbox
tags:
  - Spring

---
## Spring MVC 文件下载

<http://mayday85.iteye.com/blog/1622445>

不知道起这个标题是不是因为我有妄想症

坐等拍砖

私以为

在使用一个框架时，程序员分为三种级别

1.看demo开发

2.看文档开发

3.看源码开发

明显1不如2,2不如3

但是考虑时间成本3不如2,2不如1

我的原则是

有好的demo不看文档，有好的文档不看源码

对于文件下载，再简单不过了，但我比较傻，不会自己写

于是在google搜索"Spring mvc 3 download"，demo版本都差不多

Java代码 收藏代码

@RequestMapping("download")

public void download(HttpServletResponse res) throws IOException {

OutputStream os = res.getOutputStream();

try {

res.reset();

res.setHeader("Content-Disposition", "attachment; filename=dict.txt");

res.setContentType("application/octet-stream; charset=utf-8");

os.write(FileUtils.readFileToByteArray(getDictionaryFile()));

os.flush();

} finally {

if (os != null) {

os.close();

}

}

}

因为鄙人强烈的精神洁癖，心中大骂

"这样的狗屁代码也贴在网上？"

既然使用了mvc，怎么还能暴露HttpServletResponse这样的j2ee接口出来！

我相信spring提供了更好的方式，于是开始翻阅文档，得出如下代码

Java代码 收藏代码

@RequestMapping("download")

public ResponseEntity<byte[]> download() throws IOException {

HttpHeaders headers = new HttpHeaders();

headers.setContentType(MediaType.APPLICATION_OCTET_STREAM);

headers.setContentDispositionFormData("attachment", "dict.txt");

return new ResponseEntity<byte[]>(FileUtils.readFileToByteArray(getDictionaryFile()),

headers, HttpStatus.CREATED);

}

理论上没问题，实现上很优雅

但是文件下载后内容如下

Java代码 收藏代码

"YWEJMQ0KdnYJMg0KaGgJMw=="

正确内容为

Java代码 收藏代码

aa 1

vv 2

hh 3

我把代码改为

Java代码 收藏代码

ResponseEntity<String>

输出如下

Java代码 收藏代码

"aa 1\n\tvv 2\n\thh 3"

相信很多人看到这已经知道了发生了什么

但是因为本人狗屎一样的基础知识，又浪费了几小时

先去看了ByteArrayHttpMessageConverter的源码

Java代码 收藏代码

public ByteArrayHttpMessageConverter() {

super(new MediaType("application", "octet-stream"), MediaType.ALL);

}

...

protected void writeInternal(byte[] bytes, HttpOutputMessage outputMessage) throws IOException {

FileCopyUtils.copy(bytes, outputMessage.getBody());

}

没感觉到有任何问题

捉耳挠腮了一阵子，又去看AnnotationMethodHandlerAdapter

Java代码 收藏代码

public AnnotationMethodHandlerAdapter() {

// no restriction of by default

super(false);

// See SPR-7316

StringHttpMessageConverter stringHttpMessageConverter = new StringHttpMessageConverter();

stringHttpMessageConverter.setWriteAcceptCharset(false);

this.messageConverters = new HttpMessageConverter[]{new ByteArrayHttpMessageConverter(), stringHttpMessageConverter,

new SourceHttpMessageConverter(), new XmlAwareFormHttpMessageConverter()};

}

public void setMessageConverters(HttpMessageConverter<?>[] messageConverters) {

this.messageConverters = messageConverters;

}

再去看MappingJacksonHttpMessageConverter

Java代码 收藏代码

extends AbstractHttpMessageConverter[color=red]<Object>[/color]

突然有一种自己是个傻逼的感觉，浪费了大概3、4个小时

修改xml

Java代码 收藏代码

<bean class="org.springframework.web.servlet.mvc.annotation.AnnotationMethodHandlerAdapter">

<property name="messageConverters">

[color=red]<bean class="org.springframework.http.converter.ByteArrayHttpMessageConverter"/>[/color]

<bean id="jsonHttpMessageConverter" class="org.springframework.http.converter.json.MappingJacksonHttpMessageConverter" >

<property name = "supportedMediaTypes">

<value>text/plain;charset=UTF-8</value>

</list>

</property>

</bean>

</list>

</property>

</bean>

终于如我所愿了

记录一下我这几个小时干的蠢事

顺便想说，每个例子和demo最好都以最佳实践去写

这样我这种菜鸟程序员就没机会去看源码了~
